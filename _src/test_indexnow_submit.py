#!/usr/bin/env python3
"""Offline guardrail tests. No requests to IndexNow or the public website."""

import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import indexnow_submit as notifier


KEY = "0123456789abcdef0123456789abcdef"


class Fixture(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.receipt = self.root / ".openai" / "receipt.json"
        self.run_git("init", "-q")
        self.run_git("config", "user.name", "Fixture")
        self.run_git("config", "user.email", "fixture@example.invalid")
        self.write(KEY + ".txt", KEY + "\n")
        self.html("index.html", "old home")
        self.html("papers/retired/index.html", "retired")
        self.write("papers/example/paper.pdf", b"%PDF-1.4\nold paper\n")
        self.write("pdf/retired.pdf", b"%PDF-1.4\nretired paper\n")
        self.write("googleproof.html", "verification old")
        self.write("llms.txt", "old note")
        self.write("_src/private.pdf", b"%PDF-1.4\nnot an eligible public path")
        self.sitemap(["index.html", "papers/retired/index.html"])
        self.base = self.commit()
        self.html("index.html", "new home")
        self.html("papers/new/index.html", "new abstract")
        (self.root / "papers/retired/index.html").unlink()
        (self.root / "pdf/retired.pdf").unlink()
        self.write("papers/example/paper.pdf", b"%PDF-1.4\nnew paper\n")
        self.write("papers/new/paper.pdf", b"%PDF-1.4\nnewly available paper\n")
        self.write("googleproof.html", "verification new")
        self.write("llms.txt", "new note")
        self.write("style.css", "body {color: black}")
        self.write("_src/private.pdf", b"%PDF-1.4\nchanged internal source")
        self.sitemap(["index.html", "papers/new/index.html"])
        self.head = self.commit()
        self.plan = notifier.make_plan(self.root, self.base, self.head)
        self.calls = []

    def run_git(self, *args):
        return subprocess.run(["git", "-C", str(self.root), *args], check=True, capture_output=True).stdout.decode().strip()

    def write(self, path, content):
        destination = self.root / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(content.encode() if isinstance(content, str) else content)

    def html(self, path, text, canonical=None):
        self.write(path, '<!doctype html><html><head><link rel="canonical" href="' + (canonical or notifier.path_url(path))
                   + '"></head><body>' + text + '</body></html>')

    def sitemap(self, paths):
        self.write("sitemap.xml", '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' +
                   "".join("<url><loc>" + notifier.path_url(p) + "</loc></url>" for p in paths) + "</urlset>")

    def commit(self):
        self.run_git("add", "-A")
        self.run_git("commit", "-qm", "fixture")
        return self.run_git("rev-parse", "HEAD")

    def transport(self, url, *, method="GET", data=None, headers=None, limit=None):
        self.calls.append((method, url, data))
        if method == "POST":
            return 200, {"Date": "fixture"}, b""
        if url == self.plan["key_location"]:
            return 200, {}, KEY.encode()
        item = next(c for c in self.plan["changes"] if c["url"] == url)
        if item["change"] == "deleted":
            return 404, {}, b"not found"
        return 200, {}, (self.root / item["path"]).read_bytes()

    def execute(self, **kw):
        return notifier.execute(self.plan, self.receipt, transport=kw.pop("transport", self.transport), **kw)


class PlanningTests(Fixture):
    def test_only_canonical_changed_html_and_public_pdfs(self):
        self.assertEqual({r["path"] for r in self.plan["changes"]}, {
            "index.html", "papers/new/index.html", "papers/retired/index.html",
            "papers/example/paper.pdf", "papers/new/paper.pdf", "pdf/retired.pdf"})
        self.assertTrue(all(r["url"].startswith(notifier.SITE + "/") for r in self.plan["changes"]))
        self.assertEqual({r["url"] for r in self.plan["changes"] if r["change"] == "deleted"},
                         {notifier.SITE + "/papers/retired/", notifier.SITE + "/pdf/retired.pdf"})

    def test_off_host_canonical_rejected(self):
        self.html("index.html", "new", "https://example.invalid/")
        with self.assertRaisesRegex(notifier.DiscoveryError, "canonical"):
            notifier.make_plan(self.root, self.base, self.commit())

    def test_sitemap_cannot_repoint_to_other_host(self):
        self.write("sitemap.xml", '<urlset><url><loc>https://example.invalid/</loc></url></urlset>')
        with self.assertRaisesRegex(notifier.DiscoveryError, "host"):
            notifier.make_plan(self.root, self.base, self.commit())

    def test_pdf_symlink_rejected(self):
        p = self.root / "papers/example/paper.pdf"
        p.unlink()
        p.symlink_to("../../_src/private.pdf")
        with self.assertRaisesRegex(notifier.DiscoveryError, "regular"):
            notifier.make_plan(self.root, self.base, self.commit())

    def test_sibling_filename_ending_in_index_not_mapped_as_directory(self):
        self.assertEqual(notifier.path_url("someindex.html"), notifier.SITE + "/someindex.html")

    def test_nonancestor_baseline_rejected(self):
        with self.assertRaisesRegex(notifier.DiscoveryError, "ancestor"):
            notifier.make_plan(self.root, self.head, self.base)


class SubmissionTests(Fixture):
    def test_superseded_during_live_checks_prevents_post(self):
        def stale():
            raise notifier.DiscoveryError("superseded")
        receipt, code = self.execute(submit=True, before_submit=stale)
        self.assertEqual((receipt["status"], code), ("preflight_failed", 2))
        self.assertFalse(any(method == "POST" for method, _, _ in self.calls))

    def test_dry_run_makes_no_network_requests(self):
        receipt, code = self.execute()
        self.assertEqual((receipt["status"], code), ("dry_run", 0))
        self.assertEqual(self.calls, [])
        self.assertNotIn("key", json.loads(self.receipt.read_text()))

    def test_live_mismatch_refuses_post(self):
        def wrong(url, **kw):
            status, headers, body = self.transport(url, **kw)
            if url == notifier.SITE + "/":
                body = b"stale deployment"
            return status, headers, body
        receipt, code = self.execute(submit=True, transport=wrong)
        self.assertEqual((receipt["status"], code), ("preflight_failed", 2))
        self.assertFalse(any(method == "POST" for method, _, _ in self.calls))

    def test_key_mismatch_refuses_post(self):
        def wrong(url, **kw):
            status, headers, body = self.transport(url, **kw)
            return (status, headers, b"other key") if url == self.plan["key_location"] else (status, headers, body)
        receipt, code = self.execute(submit=True, transport=wrong)
        self.assertEqual((receipt["status"], code), ("preflight_failed", 2))
        self.assertEqual(len(self.calls), 1)

    def test_deleted_url_must_actually_be_gone(self):
        def stale(url, **kw):
            status, headers, body = self.transport(url, **kw)
            return (200, {}, b"still live") if status == 404 else (status, headers, body)
        receipt, code = self.execute(submit=True, transport=stale)
        self.assertEqual((receipt["status"], code), ("preflight_failed", 2))
        self.assertFalse(any(method == "POST" for method, _, _ in self.calls))

    def test_success_is_single_receipt_and_repeated_submission_is_skipped(self):
        receipt, code = self.execute(submit=True)
        self.assertEqual((receipt["status"], code), ("accepted", 0))
        posts = [data for method, _, data in self.calls if method == "POST"]
        self.assertEqual(len(posts), 1)
        body = json.loads(posts[0])
        self.assertEqual(body["host"], notifier.HOST)
        self.assertEqual(body["key"], KEY)
        self.assertEqual(len(body["urlList"]), 6)
        self.calls.clear()
        for _ in range(3):
            receipt, code = self.execute(submit=True)
            self.assertEqual((receipt["status"], code), ("already_acknowledged", 0))
        self.assertEqual(self.calls, [])

    def test_pending_key_and_error_statuses_are_distinct(self):
        for status in [202, 400, 403, 422, 429, 500, 302]:
            with self.subTest(status=status):
                self.receipt.unlink(missing_ok=True)
                self.calls.clear()
                def response(url, **kw):
                    original = self.transport(url, **kw)
                    return (status, {}, b"response") if kw.get("method") == "POST" else original
                receipt, code = self.execute(submit=True, transport=response)
                expected = "pending_key_validation" if status == 202 else ("unknown" if status >= 500 else "rejected")
                self.assertEqual(receipt["status"], expected)
                self.assertEqual(code, 0 if status == 202 else 2)
                self.assertEqual(sum(method == "POST" for method, _, _ in self.calls), 1)

    def test_unknown_post_is_not_blindly_retried(self):
        def timeout(url, **kw):
            result = self.transport(url, **kw)
            if kw.get("method") == "POST":
                raise TimeoutError("unknown outcome")
            return result
        receipt, code = self.execute(submit=True, transport=timeout)
        self.assertEqual((receipt["status"], code), ("unknown", 2))
        self.calls.clear()
        for _ in range(2):
            receipt, code = self.execute(submit=True)
            self.assertEqual((receipt["status"], code), ("blocked_uncertain_prior", 2))
        self.assertEqual(self.calls, [])
        receipt, code = self.execute(submit=True, retry_uncertain=True)
        self.assertEqual((receipt["status"], code), ("accepted", 0))

    def test_410_deletion_is_allowed(self):
        def gone(url, **kw):
            status, headers, body = self.transport(url, **kw)
            return (410, headers, body) if status == 404 else (status, headers, body)
        receipt, code = self.execute(submit=True, transport=gone)
        self.assertEqual((receipt["status"], code), ("accepted", 0))

    def test_unchanged_commit_has_no_requests(self):
        plan = notifier.make_plan(self.root, self.head, self.head)
        receipt, code = notifier.execute(plan, self.receipt, submit=True, transport=self.transport)
        self.assertEqual((receipt["status"], code), ("no_changes", 0))
        self.assertEqual(self.calls, [])


def deployment_fixture(path, head):
    if path == "deployments?environment=github-pages&per_page=1":
        return [{"id": 100, "sha": head}]
    if path == "deployments/100/statuses?per_page=1":
        return [{"state": "success", "environment_url": notifier.SITE + "/"}]
    if path.startswith("actions/workflows/" + str(notifier.PAGES_WORKFLOW_ID) + "/runs?"):
        return {"workflow_runs": [{"id": 200, "head_sha": head, "head_branch": "main", "conclusion": "success",
                                   "workflow_id": notifier.PAGES_WORKFLOW_ID, "event": "dynamic"}]}
    return None


class WorkflowGuards(Fixture):
    def context(self, **run_changes):
        event = {"repository": {"full_name": notifier.REPOSITORY, "default_branch": "main"},
                 "workflow_run": {"name": notifier.PAGES_WORKFLOW, "workflow_id": notifier.PAGES_WORKFLOW_ID, "conclusion": "success", "head_branch": "main",
                                  "head_repository": {"full_name": notifier.REPOSITORY}, "event": "push", "head_sha": self.head}}
        event["workflow_run"].update(run_changes)
        env = {"GITHUB_REPOSITORY": notifier.REPOSITORY, "GITHUB_EVENT_NAME": "workflow_run", "GITHUB_RUN_ID": "99"}
        root = self
        class API:
            def get(self, path):
                deployed = deployment_fixture(path, root.head)
                if deployed is not None:
                    return deployed
                if path == "git/ref/heads/main":
                    return {"object": {"sha": root.head}}
                if path.startswith("actions/workflows/"):
                    return {"workflow_runs": [], "total_count": 0}
                raise AssertionError(path)
        return notifier.github_context(self.root, event, env, API())

    def test_trusted_success_is_accepted(self):
        self.assertEqual(self.context()["head"], self.head)

    def test_dynamic_pages_display_name_is_accepted(self):
        self.assertEqual(self.context(name="pages build and deployment")["head"], self.head)

    def test_same_name_with_wrong_workflow_id_is_rejected(self):
        with self.assertRaises(notifier.DiscoveryError):
            self.context(workflow_id=123)

    def test_failed_pages_cannot_submit(self):
        with self.assertRaises(notifier.DiscoveryError):
            self.context(conclusion="failure")

    def test_pr_and_fork_cannot_submit(self):
        with self.assertRaises(notifier.DiscoveryError):
            self.context(event="pull_request")
        with self.assertRaises(notifier.DiscoveryError):
            self.context(head_repository={"full_name": "someone/fork"})

    def test_superseded_deployment_is_skipped(self):
        self.assertIn("skip", self.context(head_sha=self.base))

    def test_expired_old_receipts_are_covered_by_later_acknowledgement(self):
        ctx = {"unavailable_receipts": [{"run_id": 1, "head_commit": self.base, "reason": "expired"}],
               "history_truncated": True, "receipts": [{"status": "accepted", "head_commit": self.head}]}
        self.assertEqual(notifier.unresolved_history(self.root, ctx, self.head), [])

    def test_missing_newer_receipts_need_review(self):
        ctx = {"unavailable_receipts": [{"run_id": 2, "head_commit": self.head, "reason": "expired"}],
               "history_truncated": False, "receipts": [{"status": "accepted", "head_commit": self.base}]}
        self.assertEqual(len(notifier.unresolved_history(self.root, ctx, self.base)), 1)

    def test_unreadable_artifact_is_recorded_instead_of_preventing_manual_recovery(self):
        root = self
        class API:
            def get(self, path):
                deployed = deployment_fixture(path, root.head)
                if deployed is not None:
                    return deployed
                if path == "git/ref/heads/main":
                    return {"object": {"sha": root.head}}
                if path.startswith("actions/workflows/"):
                    return {"workflow_runs": [{"id": 1, "status": "completed", "event": "workflow_run", "conclusion": "success", "head_sha": root.base}], "total_count": 1}
                return {"artifacts": [{"name": "indexnow-receipt-1-1", "expired": True}]}
            def artifact(self, artifact):
                raise notifier.DiscoveryError("expired")
        event = {"repository": {"full_name": notifier.REPOSITORY, "default_branch": "main"}}
        env = {"GITHUB_REPOSITORY": notifier.REPOSITORY, "GITHUB_EVENT_NAME": "workflow_dispatch", "GITHUB_RUN_ID": "99", "GITHUB_REF": "refs/heads/main", "GITHUB_SHA": self.head}
        ctx = notifier.github_context(self.root, event, env, API())
        self.assertEqual(ctx["unavailable_receipts"][0]["reason"], "expired")
        self.assertEqual(notifier.unresolved_history(self.root, ctx, self.base), [])

    def test_explicit_reviewed_manual_recovery_reaches_dry_run(self):
        event_path = self.root / ".openai" / "event.json"
        event_path.parent.mkdir(exist_ok=True)
        event_path.write_text(json.dumps({"repository": {"full_name": notifier.REPOSITORY, "default_branch": "main"}}))
        ctx = {"head": self.head, "receipts": [], "history_truncated": False,
               "unavailable_receipts": [{"run_id": 1, "head_commit": self.head, "reason": "expired"}]}
        with patch.dict(notifier.os.environ, {"GITHUB_EVENT_NAME": "workflow_dispatch"}), \
             patch.object(notifier, "github_context", return_value=ctx), patch("builtins.print"):
            code = notifier.main(["--repo", str(self.root), "--github-event", str(event_path),
                                  "--base-ref", self.base, "--retry-uncertain", "--receipt", str(self.receipt)])
        self.assertEqual(code, 0)
        receipt = json.loads(self.receipt.read_text())
        self.assertEqual(receipt["status"], "dry_run")
        self.assertTrue(receipt["history_reviewed_recovery"])


class DeploymentGuards(Fixture):
    def check(self, **changes):
        root = self
        class API:
            def get(self, path):
                if path == "git/ref/heads/main":
                    return {"object": {"sha": changes.get("default_sha", root.head)}}
                value = deployment_fixture(path, root.head)
                if path.startswith("deployments?") and "deployed_sha" in changes:
                    value[0]["sha"] = changes["deployed_sha"]
                if "/statuses?" in path:
                    value[0].update(changes.get("status", {}))
                if path.startswith("actions/workflows/") and changes.get("missing_success"):
                    value = {"workflow_runs": []}
                return value
        return notifier.verified_deployment(API(), self.head)

    def test_success_requires_actual_pages_deployment(self):
        self.assertEqual(self.check()["deployment_id"], 100)

    def test_pending_deployment_is_not_published(self):
        with self.assertRaises(notifier.DiscoveryError):
            self.check(status={"state": "in_progress"})

    def test_old_deployment_cannot_submit_from_manual_dispatch(self):
        with self.assertRaises(notifier.DiscoveryError):
            self.check(deployed_sha=self.base)

    def test_other_deployment_destination_is_rejected(self):
        with self.assertRaises(notifier.DiscoveryError):
            self.check(status={"environment_url": "https://example.invalid"})

    def test_successful_status_needs_trusted_pages_run(self):
        with self.assertRaises(notifier.DiscoveryError):
            self.check(missing_success=True)


if __name__ == "__main__":
    unittest.main()
