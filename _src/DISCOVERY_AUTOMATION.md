# Research-library discovery automation

This notifier supports the complementary research library at
`https://yangguanyi.github.io`. The main academic website remains
`https://sites.google.com/site/guanyiyangeconomics`.

The notifier does not publish the site, change Pages settings, modify the
Google Site, run ranking searches, or create accounts or keys. It uses the
existing root IndexNow key. An accepted request is a change notification,
not evidence of indexing, ranking, or an AI citation.

## Local use

An ordinary invocation is an offline dry run. Choose the last notified commit
as the baseline and the intended deployed commit as the head:

```bash
python3 _src/indexnow_submit.py --base-ref BASE_SHA --head-ref HEAD
```

The plan reads committed git objects, not uncommitted working-tree edits. Its
default receipt location is `.openai/indexnow/HEAD_SHA.json`, which is ignored
by git. It never includes the key's value in its receipt.

After publishing, add `--submit` to authorize live checks and one POST:

```bash
python3 _src/indexnow_submit.py --base-ref BASE_SHA --head-ref HEAD --submit
```

Only changed, added, or deleted canonical HTML pages and PDFs under `papers/`
and `pdf/` are eligible. HTML must have a matching self-canonical and appear
in the corresponding commit's sitemap. No notes, source files, verification
files, CSS, or unrelated-domain URLs enter the payload. Renames are treated
as deletion plus addition. The former URL must return 404 or 410; a redirect
requires separate review and is deliberately not followed by this notifier.

Before a POST, the live key must match, every new or changed file must return
HTTP 200 with exactly the expected committed bytes, and deleted files must
return 404 or 410. A stale deployment or an unexpected redirect blocks all
notifications. The script has bounded reads and 20-second request timeouts.
It never retries a POST automatically.

## Automatic trigger and validation

`research-discovery.yml` runs after a successful trusted default-branch
completion of the existing `pages-build-deployment` workflow. The dynamic run is displayed as `pages build and deployment`; both names are accepted, while workflow ID `401756936` is independently required. That name was
read from the repository's active workflow API record, ID `401756936`.
The notifier verifies the event again and skips a superseded deployment.
It checks out only `main`, has read-only contents, Actions and deployment permissions, runs the
offline guardrail tests and existing build validator, checks that rebuilding
leaves the tracked files unchanged, and saves a JSON receipt
as an Actions artifact. It does not run on pull requests or fork code.

Manual and automatic runs also require the latest `github-pages` deployment to have succeeded at the current default-branch commit, with the expected destination and a matching successful trusted Pages run. These conditions are checked again after live-byte verification, immediately before POST.

The first production hook was observed on 9 November 2026: [run 42627666674](https://github.com/yangguanyi/yangguanyi.github.io/actions/runs/42627666674) followed successful Pages run 42627595703, verified the live bytes, and received HTTP 200 acceptance for the 21 changed HTML URLs at commit `ffae0984add96d08a90d66c0af3d4b677e8c8aeb`. Unchanged PDFs were excluded. Receipt artifact: `13680225104`. A manual dispatch on `main` is also available, with `submit=false`
by default. Successful live deployment and HTTP 200 receipt must be reported
separately from merely publishing the workflow file.

The initial notification baseline is commit
`ed6932908c6174d8d6ebab5f52f6f568b0f84775`, whose 21 canonical HTML pages and
11 primary PDFs were accepted by IndexNow on 9 November 2026. Subsequent
automatic runs select the most recent acknowledged ancestor from prior
receipt artifacts, so repeated deployment of an already notified commit
produces no changed URLs. These receipts are retained for 90 days.

## Receipt states and recovery

The subsequent automatic [run 42628723069](https://github.com/yangguanyi/yangguanyi.github.io/actions/runs/42628723069) read the prior receipt, verified Pages deployment 42628647021 at `e4b78e22be84266715bf258349febdc763cd8987`, and recorded `no_changes` without a POST. This confirms the unchanged-content path with production receipt history. The account-provided `BingSiteAuth.xml` is preserved by the builder and excluded from notifications.

- `dry_run`: plan only, with no website or IndexNow HTTP requests.
- `no_changes`: no eligible changed URLs.
- `accepted`: HTTP 200, notifications received.
- `pending_key_validation`: HTTP 202, received but key validation pending.
- `preflight_failed`: live files or key did not match; no POST occurred.
- `rejected`: the one POST returned a non-success status below 500, recorded
  in full. Server-side 5xx responses are classified as `unknown`, since an
  error response cannot establish whether the notification was processed.
- `submitting` or `unknown`: receipt persisted before POST, or the response
  could not be established. Do not assume either failure or success.
- `blocked_uncertain_prior`: a previous ambiguous outcome needs review.

The workflow reads up to 100 recent runs. A surviving acknowledged baseline
covers missing or expired receipts at earlier commits. It fails closed if
later receipt history is missing or expired, or the bounded lookup has no
surviving acknowledged baseline. This is conservative: a failed run without
a surviving receipt may require manual review even if it never reached the
POST. Unreadable artifacts are recorded so they do not permanently prevent
the manual recovery path. Review the earlier run logs and receipts before
using a manual dispatch with an explicit `base_ref`, `submit=true`, and
`retry_uncertain=true`. That last input is an explicit manual retry decision,
not an automatic recovery path. Do not routinely enable it.

Receipts are audit records, not a durable search-engine index. GitHub artifact
retention can expire, and the first deployment must verify the event hook and
artifact retrieval permissions. No daily or weekly URL resubmission is used.

## Verification

```bash
python3 -m unittest discover -s _src -p test_indexnow_submit.py -v
```

Tests use temporary git repositories and a fake HTTP transport. They cover
public URL selection, canonical and host validation, PDF symlinks, dry-run
side effects, deployment mismatches, deletion responses, 200/202/error
classification, uncertainty replay protection, and trusted workflow events.

Primary implementation references:

- https://www.indexnow.org/documentation
- https://www.indexnow.org/faq
- https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#workflow_run
- https://docs.github.com/en/rest/actions/workflow-runs
- https://docs.github.com/en/rest/actions/artifacts
