#!/usr/bin/env python3
"""Notify IndexNow about verified, changed public research URLs.

Dry run is the default. A POST requires --submit and successful live checks.
Uses Python's standard library. Does not build, publish, or claim indexing.
"""

import argparse
from datetime import datetime, timezone
import hashlib
from html.parser import HTMLParser
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://yangguanyi.github.io"
HOST = "yangguanyi.github.io"
REPOSITORY = "yangguanyi/yangguanyi.github.io"
ENDPOINT = "https://api.indexnow.org/indexnow"
PAGES_WORKFLOW = "pages-build-deployment"
PAGES_WORKFLOW_NAMES = {PAGES_WORKFLOW, "pages build and deployment"}
PAGES_WORKFLOW_ID = 401756936
DISCOVERY_WORKFLOW = "research-discovery.yml"
# All 21 canonical HTML pages and 11 primary PDFs at this commit were accepted
# by IndexNow on 2026-11-09. This is a notification baseline, not an index state.
INITIAL_NOTIFIED_COMMIT = "ed6932908c6174d8d6ebab5f52f6f568b0f84775"
TIMEOUT = 20
MAX_BODY = 32 * 1024 * 1024
MAX_RECEIPT = 1024 * 1024
ACKNOWLEDGED = {"accepted", "pending_key_validation", "no_changes", "already_acknowledged"}
UNCERTAIN = {"submitting", "unknown", "blocked_uncertain_prior"}
MEANING = "Receipt of URL change notifications does not establish crawling, indexing, ranking, or AI citations."


class DiscoveryError(Exception):
    pass


def now():
    return datetime.now(timezone.utc).isoformat()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def git(repo, *args, check=True):
    result = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, check=False)
    if check and result.returncode:
        raise DiscoveryError("Git command failed: " + result.stderr.decode("utf-8", "replace").strip())
    return result


def commit(repo, ref):
    if not ref or ref.startswith("-"):
        raise DiscoveryError("A nonempty commit reference is required.")
    sha = git(repo, "rev-parse", "--verify", "--end-of-options", ref + "^{commit}").stdout.decode().strip()
    if not re.fullmatch(r"[0-9a-f]{40}", sha):
        raise DiscoveryError("Expected a full SHA-1 commit identifier.")
    return sha


def ancestor(repo, older, newer):
    return git(repo, "merge-base", "--is-ancestor", older, newer, check=False).returncode == 0


def tree(repo, ref):
    entries = {}
    for record in git(repo, "ls-tree", "-rz", "--full-tree", ref).stdout.split(b"\0"):
        if not record:
            continue
        metadata, name = record.split(b"\t", 1)
        mode, kind, sha = metadata.decode().split()
        entries[name.decode("utf-8")] = (mode, kind, sha)
    return entries


def blob(repo, entries, path):
    item = entries.get(path)
    if not item or item[0] not in {"100644", "100755"} or item[1] != "blob":
        raise DiscoveryError("Expected a regular tracked file: " + path)
    data = git(repo, "cat-file", "blob", item[2]).stdout
    if len(data) > MAX_BODY:
        raise DiscoveryError("File exceeds notifier's 32 MiB bound: " + path)
    return data


def public_path(path):
    parts = PurePosixPath(path).parts
    return bool(parts) and not path.startswith("/") and all(
        part not in {".", ".."} and not part.startswith((".", "_"))
        and "\\" not in part and not any(ord(c) < 32 for c in part)
        for part in parts
    )


def path_url(path):
    if not public_path(path):
        raise DiscoveryError("Not a public file path: " + path)
    route = path[:-10] if path == "index.html" or path.endswith("/index.html") else path
    return SITE + "/" + urllib.parse.quote(route, safe="/-._~")


def url_path(url):
    p = urllib.parse.urlsplit(url)
    if p.scheme != "https" or p.netloc != HOST or p.query or p.fragment:
        raise DiscoveryError("A canonical URL is not on the configured HTTPS host: " + url)
    path = urllib.parse.unquote(p.path).lstrip("/")
    if p.path.endswith("/"):
        path += "index.html"
    if not path.endswith(".html") or not public_path(path) or path_url(path) != url:
        raise DiscoveryError("Noncanonical or unsupported HTML URL: " + url)
    return path


class CanonicalParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.canonicals = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "link" and "canonical" in attrs.get("rel", "").lower().split():
            self.canonicals.append(attrs.get("href"))


def html_inventory(repo, entries):
    try:
        document = ET.fromstring(blob(repo, entries, "sitemap.xml"))
    except ET.ParseError as exc:
        raise DiscoveryError("Invalid sitemap XML") from exc
    urls = [el.text.strip() for el in document.iter() if el.tag.rsplit("}", 1)[-1] == "loc" and el.text]
    if len(urls) != len(set(urls)):
        raise DiscoveryError("Duplicate canonical URLs in sitemap")
    result = {}
    for url in urls:
        path = url_path(url)
        parser = CanonicalParser()
        parser.feed(blob(repo, entries, path).decode("utf-8"))
        if parser.canonicals != [url]:
            raise DiscoveryError("HTML canonical does not match its sitemap URL: " + path)
        result[path] = url
    return result


def is_public_pdf(path):
    return public_path(path) and path.lower().endswith(".pdf") and path.split("/", 1)[0] in {"papers", "pdf"}


def key_at_head(repo, entries):
    matches = []
    for path in entries:
        if re.fullmatch(r"[0-9a-fA-F]{32}\.txt", path):
            key = path[:-4]
            if blob(repo, entries, path).decode("utf-8").strip() == key:
                matches.append((key, path_url(path)))
    if len(matches) != 1:
        raise DiscoveryError("Expected exactly one existing root IndexNow key file; no key was created.")
    return matches[0]


def make_plan(repo, base_ref, head_ref):
    base, head = commit(repo, base_ref), commit(repo, head_ref)
    if not ancestor(repo, base, head):
        raise DiscoveryError("The notification baseline must be an ancestor of the target commit.")
    old_tree, new_tree = tree(repo, base), tree(repo, head)
    old_html, new_html = html_inventory(repo, old_tree), html_inventory(repo, new_tree)
    key, key_url = key_at_head(repo, new_tree)
    records = []
    changed_paths = git(repo, "diff", "--name-only", "-z", "--no-renames", base, head, "--").stdout.split(b"\0")
    for raw_path in changed_paths:
        if not raw_path:
            continue
        path = raw_path.decode("utf-8")
        deleted = path not in new_tree
        eligible_html = path in (old_html if deleted else new_html)
        eligible_pdf = is_public_pdf(path)
        if not eligible_html and not eligible_pdf:
            continue
        content = blob(repo, old_tree if deleted else new_tree, path)
        if eligible_pdf and not content.startswith(b"%PDF-"):
            raise DiscoveryError("Declared public PDF does not have a PDF header: " + path)
        url = (old_html if deleted else new_html)[path] if eligible_html else path_url(path)
        records.append({"path": path, "url": url, "change": "deleted" if deleted else ("updated" if path in old_tree else "added"),
                        "sha256": None if deleted else digest(content), "bytes": None if deleted else len(content)})
    records.sort(key=lambda r: r["url"])
    if len(records) > 10000 or len({r["url"] for r in records}) != len(records):
        raise DiscoveryError("Invalid submission count or duplicate URLs")
    return {"schema_version": 1, "repository": REPOSITORY, "host": HOST, "base_commit": base, "head_commit": head,
            "key_location": key_url, "changes": records, "fingerprint": digest(json.dumps(records, sort_keys=True).encode()),
            "key": key}


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, msg, headers, newurl):
        return None


def request(url, *, method="GET", data=None, headers=None, limit=MAX_BODY):
    """No redirects or retries. Never forward credentials to another origin."""
    headers = {"User-Agent": "GuanyiYang-ResearchDiscovery/1.0", "Accept-Encoding": "identity", **(headers or {})}
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    opener = urllib.request.build_opener(NoRedirect())
    try:
        with opener.open(req, timeout=TIMEOUT) as response:
            body = response.read(limit + 1)
            if len(body) > limit:
                raise DiscoveryError("HTTP response exceeded the configured byte bound.")
            return response.status, dict(response.headers), body
    except urllib.error.HTTPError as exc:
        return exc.code, dict(exc.headers), exc.read(min(limit, 8192))


def preflight(plan, transport=request):
    checks = []
    status, _, content = transport(plan["key_location"], limit=1024)
    if status != 200 or content.decode("utf-8", "replace").strip() != plan["key"]:
        raise DiscoveryError("The deployed IndexNow key does not match the existing committed key.")
    checks.append({"url": plan["key_location"], "status": status, "matches": True, "kind": "ownership_key"})
    for item in plan["changes"]:
        status, _, body = transport(item["url"], limit=(item["bytes"] + 1) if item["bytes"] is not None else 8192)
        if item["change"] == "deleted":
            matches = status in {404, 410}
        else:
            matches = status == 200 and len(body) == item["bytes"] and digest(body) == item["sha256"]
        checks.append({"url": item["url"], "status": status, "matches": matches,
                       "sha256": digest(body) if status == 200 else None})
        if not matches:
            raise DiscoveryError("Live URL does not match this deployment: " + item["url"] + " (HTTP " + str(status) + ")")
    return checks


def save(path, receipt):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temp.replace(path)


def execute(plan, receipt_path, *, submit=False, transport=request, prior_receipts=(), retry_uncertain=False, metadata=None, before_submit=None):
    receipt = {k: v for k, v in plan.items() if k != "key"}
    receipt.update({"observed_at_utc": now(), "endpoint": ENDPOINT, "meaning": MEANING,
                    "submission_requested": submit, "status": "planned", **(metadata or {})})
    priors = list(prior_receipts)
    if Path(receipt_path).exists():
        priors.append(json.loads(Path(receipt_path).read_text()))
    for prior in priors:
        if prior.get("host") != HOST:
            continue
        if prior.get("fingerprint") == plan["fingerprint"] and prior.get("status") in ACKNOWLEDGED:
            receipt.update({"status": "already_acknowledged", "previous_observed_at_utc": prior.get("observed_at_utc")})
            save(receipt_path, receipt)
            return receipt, 0
        if submit and prior.get("status") in UNCERTAIN and not retry_uncertain:
            receipt.update({"status": "blocked_uncertain_prior", "reason": "Review the earlier uncertain receipt before explicitly authorizing a retry."})
            save(receipt_path, receipt)
            return receipt, 2
    if not plan["changes"]:
        receipt["status"] = "no_changes"
        save(receipt_path, receipt)
        return receipt, 0
    if not submit:
        receipt["status"] = "dry_run"
        receipt["live_checks"] = "Not performed. No HTTP request or POST was made by this dry run."
        save(receipt_path, receipt)
        return receipt, 0
    try:
        receipt["live_checks"] = preflight(plan, transport)
        if before_submit:
            before_submit()
    except (DiscoveryError, OSError, urllib.error.URLError) as exc:
        receipt.update({"status": "preflight_failed", "reason": str(exc)})
        save(receipt_path, receipt)
        return receipt, 2
    payload = {"host": HOST, "key": plan["key"], "keyLocation": plan["key_location"],
               "urlList": [item["url"] for item in plan["changes"]]}
    receipt.update({"status": "submitting", "post_started_at_utc": now(), "manual_uncertain_retry_authorized": retry_uncertain})
    # Persist before the single POST so a process interruption is not mistaken
    # for permission to repeat a request whose result is unknown.
    save(receipt_path, receipt)
    try:
        status, headers, body = transport(ENDPOINT, method="POST", data=json.dumps(payload).encode("utf-8"),
                                          headers={"Content-Type": "application/json; charset=utf-8"}, limit=8192)
        receipt.update({"http_status": status, "response_body": body.decode("utf-8", "replace"),
                        "response_date": headers.get("Date") or headers.get("date")})
        receipt["status"] = {200: "accepted", 202: "pending_key_validation"}.get(status, "unknown" if status >= 500 else "rejected")
        code = 0 if status in {200, 202} else 2
    except (DiscoveryError, OSError, urllib.error.URLError) as exc:
        receipt.update({"status": "unknown", "reason": str(exc)})
        code = 2
    receipt["finished_at_utc"] = now()
    save(receipt_path, receipt)
    return receipt, code


class GitHub:
    def __init__(self, token):
        self.headers = {"Accept": "application/vnd.github+json"}
        if token:
            self.headers["Authorization"] = "Bearer " + token

    def get(self, path):
        status, _, body = request("https://api.github.com/repos/" + REPOSITORY + "/" + path,
                                   headers=self.headers, limit=4 * 1024 * 1024)
        if status != 200:
            raise DiscoveryError("GitHub read failed with HTTP " + str(status) + ": " + path)
        return json.loads(body)

    def artifact(self, artifact):
        if artifact.get("expired") or artifact.get("size_in_bytes", 0) > 4 * MAX_RECEIPT:
            raise DiscoveryError("A prior receipt artifact expired or exceeded the size bound.")
        url = "https://api.github.com/repos/" + REPOSITORY + "/actions/artifacts/" + str(artifact["id"]) + "/zip"
        status, headers, body = request(url, headers=self.headers, limit=4 * MAX_RECEIPT)
        if status == 302:
            location = headers.get("Location") or headers.get("location")
            parsed = urllib.parse.urlsplit(location or "")
            if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
                raise DiscoveryError("Invalid GitHub artifact download redirect")
            # Signed download URL receives no GitHub Authorization header.
            status, _, body = request(location, limit=4 * MAX_RECEIPT)
        if status != 200:
            raise DiscoveryError("Could not read a prior receipt artifact (HTTP " + str(status) + ").")
        with zipfile.ZipFile(io.BytesIO(body)) as archive:
            files = [i for i in archive.infolist() if i.filename == "indexnow-receipt.json"]
            if len(files) != 1 or files[0].file_size > MAX_RECEIPT:
                raise DiscoveryError("Invalid prior receipt archive")
            return json.loads(archive.read(files[0]))


def verified_deployment(api, head):
    """Require the current default-branch SHA and latest successful Pages deployment."""
    if api.get("git/ref/heads/main")["object"]["sha"] != head:
        raise DiscoveryError("The deployment was superseded before notification.")
    deployments = api.get("deployments?environment=github-pages&per_page=1")
    if not deployments or deployments[0].get("sha") != head:
        raise DiscoveryError("The target commit is not the latest GitHub Pages deployment.")
    deployment = deployments[0]
    statuses = api.get("deployments/" + str(deployment["id"]) + "/statuses?per_page=1")
    if not statuses or statuses[0].get("state") != "success":
        raise DiscoveryError("GitHub Pages has not successfully deployed the target commit.")
    if statuses[0].get("environment_url", "").rstrip("/") != SITE:
        raise DiscoveryError("The deployment URL does not match this research library.")
    runs = api.get("actions/workflows/" + str(PAGES_WORKFLOW_ID) + "/runs?head_sha=" + head + "&per_page=10")
    matching = [r for r in runs.get("workflow_runs", [])
                if r.get("head_sha") == head and r.get("head_branch") == "main"
                and r.get("conclusion") == "success"
                and r.get("workflow_id") == PAGES_WORKFLOW_ID
                and r.get("event") not in {"pull_request", "pull_request_target"}]
    if not matching:
        raise DiscoveryError("No successful trusted Pages workflow run matches the deployed commit.")
    return {"deployment_id": deployment["id"], "pages_run_id": matching[0]["id"]}


def github_context(repo, event, env, api):
    """Return trusted current head and recorded receipts; never run PR code."""
    if env.get("GITHUB_REPOSITORY") != REPOSITORY or event.get("repository", {}).get("full_name") != REPOSITORY:
        raise DiscoveryError("This workflow is configured only for the research-library repository.")
    default = event["repository"].get("default_branch")
    if default != "main":
        raise DiscoveryError("The default branch changed; review the workflow before submitting.")
    head = commit(repo, "HEAD")
    live_head = api.get("git/ref/heads/main")["object"]["sha"]
    event_name = env.get("GITHUB_EVENT_NAME")
    if event_name == "workflow_run":
        run = event.get("workflow_run", {})
        if not (run.get("name") in PAGES_WORKFLOW_NAMES and run.get("workflow_id") == PAGES_WORKFLOW_ID
                and run.get("conclusion") == "success"
                and run.get("head_branch") == default
                and run.get("head_repository", {}).get("full_name") == REPOSITORY
                and run.get("event") not in {"pull_request", "pull_request_target"}):
            raise DiscoveryError("Not a successful trusted default-branch Pages completion.")
        requested_head = run.get("head_sha")
    elif event_name == "workflow_dispatch":
        if env.get("GITHUB_REF") != "refs/heads/main":
            raise DiscoveryError("Manual execution must use the default branch.")
        requested_head = env.get("GITHUB_SHA")
    else:
        raise DiscoveryError("Only Pages completion and manual dispatch are supported.")
    if head != requested_head or head != live_head:
        return {"skip": "Deployment was superseded or does not match the checked-out default branch.", "head": head}
    deployment = verified_deployment(api, head)
    current_run = int(env["GITHUB_RUN_ID"])
    history = api.get("actions/workflows/" + DISCOVERY_WORKFLOW + "/runs?per_page=100&branch=main")
    runs = history.get("workflow_runs", [])
    # Do not silently discard old notification state if activity outgrows this
    # bounded lookup. An explicit reviewed manual baseline is then required.
    receipts = []
    unavailable = []
    for run in runs:
        if run["id"] != current_run and run.get("status") != "completed":
            continue
        if run.get("event") not in {"workflow_run", "workflow_dispatch"}:
            continue
        try:
            artifacts = api.get("actions/runs/" + str(run["id"]) + "/artifacts?per_page=100")["artifacts"]
        except (DiscoveryError, OSError, ValueError, urllib.error.URLError) as exc:
            unavailable.append({"run_id": run["id"], "head_commit": run.get("head_sha"), "reason": str(exc)})
            continue
        candidates = [a for a in artifacts if a["name"].startswith("indexnow-receipt-")]
        if not candidates and run["id"] != current_run and run.get("conclusion") != "skipped":
            unavailable.append({"run_id": run["id"], "head_commit": run.get("head_sha"), "reason": "No surviving receipt artifact"})
        for artifact in candidates:
            try:
                receipt = api.artifact(artifact)
            except (DiscoveryError, OSError, ValueError, zipfile.BadZipFile, urllib.error.URLError) as exc:
                unavailable.append({"run_id": run["id"], "head_commit": run.get("head_sha"), "reason": str(exc)})
                continue
            receipt["github_run_id"] = run["id"]
            if receipt.get("status") == "not_started":
                continue
            if receipt.get("repository") != REPOSITORY or receipt.get("host") != HOST:
                raise DiscoveryError("A prior receipt belongs to a different repository or host.")
            receipts.append(receipt)
    return {"head": head, "receipts": receipts, "unavailable_receipts": unavailable, "deployment": deployment,
            "history_truncated": history.get("total_count", len(runs)) > len(runs)}


def choose_baseline(repo, head, receipts, explicit=None):
    if explicit:
        return commit(repo, explicit)
    candidates = [INITIAL_NOTIFIED_COMMIT]
    for receipt in receipts:
        sha = receipt.get("head_commit", "")
        if receipt.get("status") in ACKNOWLEDGED and re.fullmatch(r"[0-9a-f]{40}", sha) and ancestor(repo, sha, head):
            candidates.append(sha)
    usable = [sha for sha in candidates if ancestor(repo, sha, head)]
    if not usable:
        raise DiscoveryError("No known notification baseline is an ancestor; supply a reviewed --base-ref.")
    return min(usable, key=lambda sha: int(git(repo, "rev-list", "--count", sha + ".." + head).stdout))


def unresolved_history(repo, ctx, base):
    """A later acknowledged baseline covers receipts at older commits."""
    unresolved = []
    for missing in ctx["unavailable_receipts"]:
        sha = missing.get("head_commit")
        if not sha or not ancestor(repo, sha, base):
            unresolved.append(missing)
    has_saved_baseline = any(r.get("head_commit") == base and r.get("status") in ACKNOWLEDGED for r in ctx["receipts"])
    if ctx["history_truncated"] and not has_saved_baseline:
        unresolved.append({"reason": "Older history exceeds the 100-run bound and no acknowledged baseline survives in the inspected records."})
    return unresolved


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=ROOT)
    parser.add_argument("--base-ref", help="Previously notified commit; required outside GitHub workflow mode")
    parser.add_argument("--head-ref", default="HEAD")
    parser.add_argument("--receipt", type=Path, help="Output JSON receipt; default .openai/indexnow/<head>.json")
    parser.add_argument("--previous-receipt", action="append", default=[], type=Path)
    parser.add_argument("--submit", action="store_true", help="Perform live verification and one IndexNow POST")
    parser.add_argument("--github-event", type=Path, help="Trusted GitHub workflow event JSON")
    parser.add_argument("--retry-uncertain", action="store_true", help="Explicit manual retry after reviewing an earlier uncertain outcome")
    args = parser.parse_args(argv)
    head = commit(args.repo, args.head_ref)
    receipt_path = args.receipt or args.repo / ".openai" / "indexnow" / (head + ".json")
    metadata = {}
    before_submit = None
    prior = [json.loads(path.read_text()) for path in args.previous_receipt]
    try:
        if args.github_event:
            event = json.loads(args.github_event.read_text())
            api = GitHub(os.environ.get("GITHUB_TOKEN"))
            ctx = github_context(args.repo, event, os.environ, api)
            if ctx.get("skip"):
                receipt = {"schema_version": 1, "repository": REPOSITORY, "host": HOST, "head_commit": head,
                           "status": "skipped_superseded", "reason": ctx["skip"], "observed_at_utc": now(), "meaning": MEANING}
                save(receipt_path, receipt)
                print(json.dumps(receipt, indent=2))
                return 0
            if args.retry_uncertain and os.environ.get("GITHUB_EVENT_NAME") != "workflow_dispatch":
                raise DiscoveryError("Uncertain retries require an explicit manual dispatch.")
            explicit = args.base_ref or event.get("inputs", {}).get("base_ref")
            base = choose_baseline(args.repo, head, ctx["receipts"], explicit)
            unresolved = unresolved_history(args.repo, ctx, base)
            if unresolved and not (explicit and args.retry_uncertain):
                raise DiscoveryError("Notification history after the acknowledged baseline is incomplete. Review previous runs and use an explicit manual baseline and retry acknowledgement.")
            # A later acknowledged baseline already covers earlier uncertainty.
            for receipt in ctx["receipts"]:
                sha = receipt.get("head_commit", "")
                if receipt.get("status") in UNCERTAIN and sha and ancestor(args.repo, sha, base):
                    continue
                prior.append(receipt)
            metadata = {"github_run_id": os.environ.get("GITHUB_RUN_ID"),
                        "github_run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT"),
                        "github_event": os.environ.get("GITHUB_EVENT_NAME"),
                        "history_unavailable_receipts": ctx["unavailable_receipts"],
                        "history_reviewed_recovery": bool(unresolved and explicit and args.retry_uncertain),
                        "verified_deployment": ctx.get("deployment")}
            before_submit = lambda: verified_deployment(api, head)
        else:
            if not args.base_ref:
                raise DiscoveryError("--base-ref is required outside GitHub workflow mode.")
            base = args.base_ref
        plan = make_plan(args.repo, base, head)
        receipt, code = execute(plan, receipt_path, submit=args.submit, prior_receipts=prior,
                                retry_uncertain=args.retry_uncertain, metadata=metadata, before_submit=before_submit)
    except (DiscoveryError, OSError, ValueError, zipfile.BadZipFile, urllib.error.URLError) as exc:
        receipt = {"schema_version": 1, "repository": REPOSITORY, "host": HOST, "head_commit": head,
                   "observed_at_utc": now(), "status": "blocked_before_submission", "reason": str(exc), "meaning": MEANING}
        if receipt_path.exists():
            previous = json.loads(receipt_path.read_text())
            if previous.get("status") in UNCERTAIN:
                receipt.update({"status": "blocked_uncertain_prior", "previous_uncertain_receipt": previous})
        save(receipt_path, receipt)
        code = 2
    print(json.dumps({k: v for k, v in receipt.items() if k != "response_body"}, indent=2))
    return code


if __name__ == "__main__":
    sys.exit(main())
