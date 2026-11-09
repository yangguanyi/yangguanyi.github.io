# Guanyi Yang's research library

The public research library is [yangguanyi.github.io](https://yangguanyi.github.io). It complements Guanyi Yang's [main academic website on Google Sites](https://sites.google.com/site/guanyiyangeconomics). Its purpose is to make the papers accessible, understandable, and accurately citable in literature searches and AI-assisted research. It is not a replacement for the main academic website.

The library is a static GitHub Pages site with a paper index, individual paper pages, topic pages, and a research landing page. Existing CV and other resource URLs remain available for continuity. The build uses Python's standard library and makes no network requests.

## Relationship to the main website

Keep the Google Site as the primary professional website, including the primary website links on institutional and author profiles. Where an additional link is supported, label this site "Research library" or "Paper summaries and full texts". Retain the existing Google Site link to this research library.

The library's navigation links back to the main academic website. Author metadata uses the Google Site as Guanyi Yang's primary URL. Each unique paper page keeps its own GitHub canonical URL, citation metadata, and PDF URL. Do not redirect the Google Site to GitHub, canonicalize individual paper pages to the Google homepage, or change profiles to suggest that this library replaces the main site.

## Rebuild

Run `python3 _src/build_site.py` from this repository.

The script also works from any other working directory. Run `python3 /absolute/path/to/site/_src/build_site.py`; its default output is the repository that contains it.

To generate an isolated preview, run `python3 /absolute/path/to/site/_src/build_site.py /absolute/path/to/preview http://localhost:8000`, then `python3 -m http.server 8000 --directory /absolute/path/to/preview`.

The optional second argument is the absolute base URL used in links, canonical URLs, and metadata. Use `https://yangguanyi.github.io` for the production build. A local preview uses its local URL and must not be published accidentally. The build does not commit, push, or deploy.

## Source and generated files

| File | Purpose |
| --- | --- |
| `_src/papers_data.py` | Verified paper content, dates, metadata, and research themes |
| `_src/build_site.py` | Page templates, styles, export formats, and build logic |
| `_src/dois.json` | Existing DOI lookup results for related literature |
| `papers/<slug>/paper.pdf` | Public primary PDF, kept beside its abstract page |
| `pdf/` | Existing public PDF URLs and the CV; retained for link continuity |
| `papers/<slug>/index.html` | Generated individual paper page |
| `papers/<slug>/citation.bib` and `citation.ris` | Generated citation downloads |
| `papers/<slug>/llms.txt` | Generated plain-text research note |
| `research/`, `themes/`, `cv/`, `more/`, `index.html` | Generated site pages |
| `style.css`, `sitemap.xml`, `llms.txt` | Generated shared files |

The generator reads checked-in assets relative to its own location. It does not depend on a previous assistant's temporary directories or a separate working-paper checkout. Building into another directory copies public PDFs, existing verification files, and relevant static assets. Rebuilding in place preserves those files.

## Updating a paper

Edit the matching record in `_src/papers_data.py`. Preserve the existing slug and public URLs unless a migration is deliberate.

The existing content fields describe the title, ordered author list, publication status, abstract, findings, data, methods, scope, and resources. Preserve the original published or working-paper abstract exactly. Revised plain-language descriptions belong in `short_summary`, `one_liner`, and the explanatory sections, not in a silently rewritten abstract.

Additional metadata fields:

| Field | Example | Meaning |
| --- | --- | --- |
| `pdf_path` | `papers/existing-slug/paper.pdf` | Checked-in primary public PDF |
| `pdf_label` | `Read paper (PDF)` | Clear download label |
| `version_note` | Source-specific version description | Describes the actual linked version |
| `publication_date` | `2024-06` | Bibliographic issue/publication date, not upload date |
| `online_date` | `2024-01-05` | Optional verified first-online date |
| `volume`, `issue` | `86`, `3` | Optional journal details |
| `first_page`, `last_page` | `672`, `689` | Optional page range |
| `article_number` | `101365` | Article identifier when used instead of pages |
| `short_summary` | One sentence | Concise contribution for paper lists |
| `reviewed_on` | `2026-11-09` | Date this webpage's content materially changed |

Use only supported dates and bibliographic fields. A year is sufficient if no more precise source date is known. Keep the issue's publication year in the citation when it differs from the first-online year. Page updates do not change a paper's publication date. The generator uses a separate webpage modification date and does not mark the scholarly article itself as revised merely because its webpage changed.

For Google Scholar, the primary PDF must be located in the same paper directory as the abstract HTML. The build checks this and fails if a declared PDF is missing. Highwire citation metadata identifies the exact title, each author separately, publication date, available journal details, DOI, and absolute PDF URL. JSON-LD describes the same visible content. Old PDF paths remain available.

Keep summaries proportional to the evidence. Distinguish percentage points from percentages, associations from causal estimates, and model counterfactuals from empirical observations. Carry version changes and sample restrictions into the explanatory text. Do not claim universal effects from a specific sample or model.

## Research without a public draft

Use `IN_PROGRESS` for a project whose draft is not public. Each record has `slug`, `title`, `coauthors`, `theme`, and `status` (for example, `Draft forthcoming`). These projects appear on the research index and their existing topic pages. The generator does not invent abstracts, findings, PDF links, citations, or standalone paper pages for them.

## Discovery and crawler settings

The site provides ordinary HTML links, freely visible abstracts, colocated PDFs, bibliographic metadata, and a sitemap of canonical HTML pages. The root and per-paper `llms.txt` files are optional synchronized research notes. They do not guarantee indexing, citations, or search rankings. The HTML pages and PDFs remain the main public resources.

`robots.txt` preserves the existing crawler-access policy on every rebuild. The generator updates its sitemap URL but does not change search or training preferences. Google verification files, the existing IndexNow key file, and legacy PDF URLs are also preserved. Submitting a sitemap or confirming a successful build does not establish that an external search service has indexed a page.

The sitemap's `lastmod` values come from each paper's `reviewed_on` and the generator's `SITE_REVISED` constant. They do not change just because a build runs on another day. Update `SITE_REVISED` when site-level content materially changes. The sitemap excludes notes, citation downloads, and verification files.

## Notifications after deployment

`.github/workflows/research-discovery.yml` checks the built site and runs the IndexNow notifier after the existing trusted Pages workflow completes successfully. It does not replace or reconfigure Pages. It verifies the published bytes before sending changed public HTML/PDF URLs and records the result as a workflow artifact. Verify the first production run after publishing; the presence of the workflow file alone does not establish that the trigger ran.

For offline planning, use `python3 _src/indexnow_submit.py --base-ref BASE_SHA --head-ref HEAD`. Submission requires the explicit `--submit` option after deployment. The script reads committed objects and reuses the existing key. Read [_src/DISCOVERY_AUTOMATION.md](_src/DISCOVERY_AUTOMATION.md) for the acknowledged baseline, receipt states, duplicate protection, and recovery when history is unavailable. No daily or weekly resubmission is configured.

Run the meaningful notification safeguards with `python3 -m unittest discover -s _src -p test_indexnow_submit.py -v`. These tests use temporary repositories and fake HTTP responses; they do not notify a live search engine.

## Measuring paper discovery

`_src/discovery_queries.json` is a maintenance benchmark covering the 11 available papers. It contains 11 broad literature questions, the 11 distinctive topical queries tested on November 9, 2026, and 22 interpretation questions. It also records four independent AI search observations. Untested questions are labeled. The file is not a set of instructions for search engines and should not be turned into thin keyword pages.

Give an independent research session only a question's text. Keep the target title, author, slug, website, and previous result out of that session. Record the product, date, exact queries, selected papers, citation URLs, versions, and factual accuracy. Count relevant citations through a publisher or repository as successes for the paper; track citations to this library separately. Search-tool order is not a consumer search ranking, and reading-list order is not a universal quality measure.

Private Google Search Console and Bing Webmaster Tools reports are separate evidence. A public verification file does not establish that an account owns a verified property. Inspect the exact URL-prefix property `https://yangguanyi.github.io/`, the sitemap, paper-level index status, and available AI performance reports with authorized account access. Do not use the Google Indexing API for ordinary research pages, the deprecated sitemap ping endpoint, or `site:` results as proof of complete indexing. Preserve existing main-website links to Google Sites.

## Before publishing

Build into the repository using the production base URL. Review the changed pages and exports, check the paper links and mobile layout, and inspect the Git diff. Confirm every abstract, version label, status, and numerical finding against its source. Then publish through the repository's established GitHub Pages workflow.

Run `python3 _src/check_site.py . https://yangguanyi.github.io --strict-pdf-size` to check the generated pages, original abstracts, citation metadata and exports, internal links, primary PDF sizes, sitemap, and preserved public assets. The checker does not establish external link availability or search-engine indexing.

This site requires no JavaScript, remote fonts, package installation, or build service. Search Console and Bing Webmaster Tools can be used separately to inspect indexing and discovery after deployment.
