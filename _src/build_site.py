#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the checked-in academic website without network access or dependencies.

Usage: python3 /path/to/site/_src/build_site.py [output_dir] [base_url]
The default output is the repository root. All source paths are script-relative.
"""
import argparse
import datetime
import html
import importlib.util
import json
import pathlib
import re
import shutil

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
spec = importlib.util.spec_from_file_location("papers_data", HERE / "papers_data.py")
pd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pd)
with (HERE / "dois.json").open(encoding="utf-8") as handle:
    DOIS = json.load(handle)

BASE = "https://yangguanyi.github.io"
OUT = ROOT
# Change this only when site-level content changes, not on each rebuild.
SITE_REVISED = "2026-11-09"
NAME = "Guanyi Yang"
EMAIL = "gyang@ColoradoCollege.edu"
SCHOLAR = "https://scholar.google.com/citations?user=nlgkEE8AAAAJ&hl=en"
REPEC = "https://ideas.repec.org/f/pya376.html"
GITHUB = "https://github.com/yangguanyi"
GLO = "https://glabor.org/user/gyang/"
STATUS = {
    "article": "Published article",
    "working paper": "Working paper",
    "report": "Policy report",
}
THEME_LABELS = {
    "night-sky": "Night skies",
    "college-lifecycle": "Human capital",
    "race-macro": "Racial inequality",
    "emerging-markets": "Emerging markets",
    "china-education": "Schooling in China",
    "behavior-public-goods": "Behavior and public goods",
}
# Preserve the established public PDF URLs. Copies are already in the repository.
LEGACY_PDFS = {
    "Search_and_match_and_racial_inequity.pdf": "Murali-Yang-2025-Macroeconomics-of-Racial-Disparities.pdf",
    "College_timing_endowment.pdf": "Yang-2025-Better-Late-Than-Never-Intermittent-College-Enrollment-WP.pdf",
    "Contingent_Behavior_Modeling_for_Dark_Skies_Valuation_at_Great_Sand_Dunes_National_Park.pdf": "Eiswerth-Mullen-Yang-2026-Dark-Skies-Valuation-Great-Sand-Dunes-WP.pdf",
    "GFR_and_equity_returns.pdf": "Horvath-Yang-2023-Global-Financial-Risk-Equity-Returns-Emerging-Countries-WP.pdf",
    "sib_spillover_China.pdf": "Bansak-Jiang-Yang-2022-Sibling-Spillovers-Rural-China-WP.pdf",
}

CSS = """
:root{color-scheme:light;--paper:#faf9f5;--white:#fff;--ink:#202c32;--navy:#173c51;--teal:#256b68;--muted:#626b6e;--line:#d9dfdc;--wash:#eef2ed;--serif:Georgia,"Times New Roman",serif;--sans:system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:1.5rem;-webkit-text-size-adjust:100%}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.65 var(--sans);text-rendering:optimizeLegibility}
a{color:var(--navy);text-decoration-thickness:1px;text-underline-offset:.22em}a:hover{color:var(--teal)}
:focus-visible{outline:3px solid var(--teal);outline-offset:5px;border-radius:2px}
.wrap{max-width:1104px;margin:0 auto;padding:0 32px}
.skip-link{position:absolute;top:8px;left:16px;z-index:10;padding:10px 16px;background:var(--navy);color:white;transform:translateY(-160%)}
.skip-link:focus{transform:translateY(0);color:white}
.site-header{border-bottom:1px solid var(--line)}
.header-inner{min-height:94px;display:flex;align-items:center;justify-content:space-between;gap:28px}
.brand{font:600 1.35rem/1.2 var(--serif);letter-spacing:-.035em;text-decoration:none;color:var(--ink)}
.primary-nav{display:flex;align-items:center;gap:30px;font-size:.875rem}
.primary-nav a{text-decoration:none;padding:12px 0;border-bottom:2px solid transparent}
.primary-nav a[aria-current="page"]{border-bottom-color:var(--teal);color:var(--ink)}
main{padding-top:52px!important;padding-bottom:48px!important;min-height:65vh}
h1,h2,h3{font-family:var(--serif);font-weight:400;color:var(--ink)}
h1{font-size:clamp(2.75rem,6vw,4rem);line-height:1.08;letter-spacing:-.045em;margin:0 0 24px}
h2{font-size:2rem;line-height:1.2;letter-spacing:-.025em;margin:0 0 24px}
h3{font-size:1.37rem;line-height:1.36;letter-spacing:-.018em;margin:0 0 10px}
p{margin:0 0 1rem}ul,ol{padding-left:1.25rem;margin:.8rem 0 1.25rem}li{margin:.4rem 0}
.eyebrow{font-size:.72rem;line-height:1.4;font-weight:600;letter-spacing:.13em;text-transform:uppercase;color:var(--teal);margin-bottom:18px}
.lede{font-size:1.18rem;line-height:1.75;max-width:760px;color:#414e54}
.meta{font-size:.86rem;line-height:1.65;color:var(--muted)}
.intro{margin-bottom:32px;max-width:900px}
.intro .lede{margin-bottom:0}
.theme-links{display:flex;flex-wrap:wrap;gap:8px;list-style:none;padding:0;margin:25px 0 28px}
.theme-links li{margin:0}
.theme-links a{display:block;border:1px solid var(--line);border-radius:4px;padding:6px 11px;font-size:.78rem;text-decoration:none;background:transparent;line-height:1.5}
.theme-links a:hover{background:var(--wash);border-color:#a7b8b4}
.jump-links{display:flex;flex-wrap:wrap;gap:10px 25px;border-top:1px solid var(--line);border-bottom:1px solid var(--line);padding:14px 0;margin:0 0 52px;font-size:.8rem}
.jump-links a{text-decoration:none}.jump-links span{font-variant-numeric:tabular-nums;color:var(--muted);margin-left:6px}
.research-section{margin-top:50px;scroll-margin-top:25px}
.section-title{display:flex;align-items:baseline;gap:12px;margin-bottom:4px}
.section-title h2{margin-bottom:16px}.section-count{font-size:.76rem;color:var(--muted)}
.paperlist{list-style:none;padding:0;margin:0}
.paper-row{display:grid;grid-template-columns:72px minmax(0,1fr);gap:24px;padding:28px 0 29px;margin:0;border-top:1px solid var(--line)}
.paper-year{padding-top:5px;color:var(--muted);font-size:.85rem;font-variant-numeric:tabular-nums}
.paper-row h3 a{text-decoration:none}.paper-row h3 a:hover{text-decoration:underline}
.paper-byline{font-size:.84rem;color:var(--muted);margin:0 0 4px}
.paper-venue{font-size:.82rem;color:var(--muted);margin:0 0 9px}
.paper-summary{max-width:790px;color:#414e54;font-size:.94rem;line-height:1.7;margin:8px 0 10px}
.paper-links{display:flex;flex-wrap:wrap;align-items:center;gap:9px 20px;font-size:.78rem;margin-top:10px}
.paper-links a{font-weight:500;text-decoration:none;border-bottom:1px solid #a9bebd;padding-bottom:1px}
.paper-links a:hover{border-bottom-color:var(--teal)}
.draft-status{font-size:.74rem;color:var(--teal);letter-spacing:.025em}
.in-progress .paper-row{grid-template-columns:72px minmax(0,1fr)}
.research-footnote{border-top:1px solid var(--line);padding-top:25px;margin-top:40px}
.breadcrumb{display:flex;flex-wrap:wrap;gap:8px;font-size:.78rem;color:var(--muted);margin:0 0 32px}
.breadcrumb a{text-decoration:none}
.paper-header{max-width:950px;margin-bottom:30px}
.paper-header h1{font-size:clamp(2rem,4.4vw,3.05rem);line-height:1.2;letter-spacing:-.03em;margin-bottom:20px}
.paper-authors{font-size:1rem;margin-bottom:9px;color:#3b4e57}
.paper-status{font-size:.79rem;color:var(--teal);font-weight:500;margin-bottom:6px}
.publication-line{font-size:.88rem;color:var(--muted)}
.download-links{display:flex;flex-wrap:wrap;align-items:center;gap:10px;margin:22px 0 12px}
.download-links a{display:inline-block;font-size:.79rem;font-weight:500;border:1px solid var(--line);border-radius:3px;padding:8px 13px;text-decoration:none;line-height:1.5}
.download-links .primary{background:var(--navy);border-color:var(--navy);color:white}
.download-links .primary:hover{background:var(--teal);border-color:var(--teal)}
.download-links a:not(.primary):hover{background:var(--wash)}
.version-note{max-width:820px;font-size:.78rem;color:var(--muted);line-height:1.7;margin-top:10px}
.paper-body{max-width:850px}
.paper-section{padding-top:29px;margin-top:30px;border-top:1px solid var(--line)}
.paper-section h2{font-size:1.55rem;margin-bottom:17px}
.abstract{font-family:var(--serif);font-size:1.13rem;line-height:1.85;color:#2d3a40}
.paper-section ul{padding-left:1.15rem}.paper-section li{padding-left:4px;margin-bottom:13px}
.evidence-grid{display:grid;grid-template-columns:100px minmax(0,1fr);gap:13px 25px}
.evidence-grid dt{font-size:.8rem;color:var(--teal);font-weight:600}
.evidence-grid dd{margin:0}
.topic-line{font-size:.85rem;color:var(--muted)}
details{border-top:1px solid var(--line);padding:20px 0}
summary{cursor:pointer;font-family:var(--serif);font-size:1.25rem;color:var(--navy)}
details[open] summary{margin-bottom:18px}
pre{padding:18px;background:var(--wash);border:1px solid var(--line);border-radius:3px;white-space:pre-wrap;overflow-wrap:anywhere;font:12px/1.7 ui-monospace,SFMono-Regular,Consolas,monospace}
.citation{font-size:.9rem;overflow-wrap:anywhere}.sources-list{font-size:.89rem}
.paper-note{margin-top:32px;padding-top:18px;border-top:1px solid var(--line)}
.home-hero{display:grid;grid-template-columns:minmax(0,1fr) 245px;gap:75px;padding:10px 0 45px}
.home-hero h1{font-size:clamp(3.4rem,6.8vw,5.3rem);margin-bottom:23px}
.home-role{font-family:var(--serif);font-size:1.24rem;line-height:1.55;max-width:570px}
.home-copy{max-width:665px;font-size:1.05rem;line-height:1.8;color:#414e54;margin-top:23px}
.home-sidebar{align-self:start;border-left:1px solid var(--line);padding-left:25px;margin-top:66px}
.home-sidebar h2{font-family:var(--sans);font-size:.74rem;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--teal);margin:0 0 13px}
.home-sidebar p{font-size:.83rem;line-height:1.8}
.home-sidebar a{overflow-wrap:anywhere}
.profile-links{list-style:none;padding:0;font-size:.83rem;margin-top:20px}
.profile-links li{margin:7px 0}
.cta-links{display:flex;flex-wrap:wrap;align-items:center;gap:15px 25px;margin-top:24px;font-size:.85rem}
.button{display:inline-block;background:var(--navy);color:white;border:1px solid var(--navy);border-radius:3px;padding:10px 18px;text-decoration:none}
.button:hover{background:var(--teal);border-color:var(--teal);color:white}
.home-featured{margin-top:12px}
.section-heading-row{display:flex;align-items:baseline;justify-content:space-between;gap:25px;margin-bottom:16px}
.section-heading-row h2{margin:0}.section-heading-row>a{font-size:.8rem}
.home-bottom{display:grid;grid-template-columns:1.45fr 1fr;gap:65px;border-top:1px solid var(--line);margin-top:40px;padding-top:34px}
.home-bottom h2{font-size:1.45rem;margin-bottom:14px}.home-bottom p{font-size:.91rem;color:#414e54}
.standard-page{max-width:850px}.standard-page h2{font-size:1.55rem;margin:35px 0 15px}.standard-page h1{margin-bottom:24px}
.site-footer{border-top:1px solid var(--line);padding:28px 0 34px;color:var(--muted);font-size:.76rem}
.footer-inner{display:flex;justify-content:space-between;gap:25px;align-items:flex-start}
.footer-inner p{margin:0;line-height:1.8}.footer-links{display:flex;flex-wrap:wrap;gap:7px 18px;justify-content:flex-end}
@media(min-width:1200px){.intro{margin-top:5px}}
@media(max-width:760px){
.wrap{padding:0 22px}.header-inner{min-height:78px;gap:20px}.primary-nav{gap:20px;font-size:.8rem}.brand{font-size:1.23rem}
main{padding-top:36px!important}.lede{font-size:1.04rem}.jump-links{gap:10px 20px;margin-bottom:38px}
.paper-row{grid-template-columns:48px minmax(0,1fr);gap:16px;padding:24px 0}.paper-row h3{font-size:1.25rem}.paper-summary{font-size:.9rem}
.in-progress .paper-row{grid-template-columns:48px minmax(0,1fr)}.paper-year{font-size:.76rem}.section-title h2{font-size:1.7rem}
.home-hero{grid-template-columns:1fr;gap:26px;padding-bottom:30px}.home-hero h1{font-size:3.75rem}.home-role{font-size:1.13rem}
.home-sidebar{margin-top:0;padding:20px 0 0;border-left:0;border-top:1px solid var(--line)}.home-sidebar .profile-links{display:flex;flex-wrap:wrap;gap:8px 20px;margin-bottom:0}
.home-sidebar .profile-links li{margin:0}.home-sidebar p{margin-bottom:8px}.home-sidebar h2{margin-bottom:8px}
.home-bottom{grid-template-columns:1fr;gap:24px}.footer-inner{display:block}.footer-links{justify-content:flex-start;margin-top:15px}
.evidence-grid{grid-template-columns:1fr;gap:5px}.evidence-grid dd{margin-bottom:13px}.paper-header h1{font-size:2.2rem}.abstract{font-size:1.06rem}
}
@media(max-width:420px){
.wrap{padding:0 18px}.header-inner{gap:14px}.primary-nav{gap:15px}.brand{font-size:1.15rem}
.paper-row,.in-progress .paper-row{display:block}.paper-year{margin:0 0 8px;padding:0}.paper-links{gap:9px 16px}.theme-links{gap:7px}.theme-links a{font-size:.73rem}
.section-heading-row{align-items:flex-start;flex-direction:column;gap:10px}.home-hero h1{font-size:3.3rem}.paper-header h1{font-size:1.95rem}
}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}*{transition:none!important;animation:none!important}}
@media print{
body{background:white;color:black}.site-header,.site-footer,.jump-links,.theme-links,.download-links{display:none}
main{padding-top:0!important}.wrap{max-width:none;padding:0}.paper-row{break-inside:avoid}a{color:inherit}h1{font-size:28pt}
}
"""


def e(value):
    return html.escape(str(value), quote=True)


def url(path=""):
    return BASE + "/" + str(path).lstrip("/")


def paper_path(p):
    return f"papers/{p['slug']}/"


def paper_url(p):
    return url(paper_path(p))


def published_date(p):
    return str(p.get("publication_date") or p["year"])


def reviewed_date(p=None):
    return str(p.get("reviewed_on", SITE_REVISED)) if p else SITE_REVISED


def site_page_modified(path):
    """Follow content dependencies without inventing a new date on every build."""
    selected = {"racial-disparities-hiring-discrimination", "intermittent-college-enrollment", "dark-skies-great-sand-dunes"}
    papers, projects = [], []
    if path == "research/":
        papers, projects = pd.PAPERS, pd.IN_PROGRESS
    elif not path:
        papers = [p for p in pd.PAPERS if p["slug"] in selected]
    elif path.startswith("themes/"):
        theme = path.split("/")[1]
        papers = [p for p in pd.PAPERS if p["theme"] == theme]
        projects = [p for p in pd.IN_PROGRESS if p["theme"] == theme]
    return max([SITE_REVISED] + [reviewed_date(p) for p in papers + projects])


def date_label(value):
    try:
        return datetime.date.fromisoformat(value).strftime("%B %d, %Y").replace(" 0", " ")
    except ValueError:
        if re.fullmatch(r"\d{4}-\d{2}", value):
            return datetime.datetime.strptime(value, "%Y-%m").strftime("%B %Y")
        return value


def summary_text(p):
    return p.get("short_summary") or p["one_liner"]


def author_str(p):
    return ", ".join(n for n, _ in p["authors"])


def local_pdf(link):
    basename = link.rsplit("/", 1)[-1]
    if "github.com/yangguanyi/Working-papers/" in link and basename in LEGACY_PDFS:
        return url("pdf/" + LEGACY_PDFS[basename])
    return link


def pdf_url(p):
    return url(p["pdf_path"]) if p.get("pdf_path") else None


def versions(p):
    """Deduplicate resource URLs while keeping the verified primary PDF first."""
    result = []
    if pdf_url(p):
        result.append((p.get("pdf_label", "Read paper (PDF)"), pdf_url(p)))
    seen = {link for _, link in result}
    for label, link in p.get("versions", []):
        link = local_pdf(link)
        if link not in seen:
            result.append((label, link))
            seen.add(link)
    return result


def nav(active):
    items = [("research", "Research", "research/"), ("cv", "CV", "cv/"), ("more", "More", "more/")]
    return "".join(
        f'<a href="{e(url(path))}"' + (' aria-current="page"' if key == active else "") + f">{label}</a>"
        for key, label, path in items
    )


def page(title, body, desc, path, entity=None, extra_head="", active=None, modified=None, page_class=""):
    canon = url(path)
    modified = modified or site_page_modified(path)
    webpage = {
        "@type": "WebPage", "@id": canon + "#webpage", "url": canon,
        "name": title, "description": desc, "inLanguage": "en",
        "dateModified": modified, "isPartOf": {"@id": url() + "#website"},
    }
    if entity:
        webpage["mainEntity"] = {"@id": entity["@id"]}
    graph = [webpage] + ([entity] if entity else [])
    if not path:
        graph.append({"@type": "WebSite", "@id": url() + "#website", "url": url(), "name": NAME})
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False).replace("<", "\\u003c")
    og_type = "article" if path.startswith("papers/") else "website"
    current_home = ' aria-current="page"' if not path else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="author" content="{e(NAME)}">
<link rel="canonical" href="{e(canon)}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:type" content="{og_type}">
<meta property="og:url" content="{e(canon)}">
<meta property="og:site_name" content="{e(NAME)}">
<meta name="twitter:card" content="summary">
<link rel="stylesheet" href="{e(url('style.css'))}">
{extra_head}
<script type="application/ld+json">{ld}</script>
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header"><div class="wrap header-inner">
<a class="brand" href="{e(url())}"{current_home}>Guanyi Yang</a>
<nav class="primary-nav" aria-label="Main navigation">{nav(active)}</nav>
</div></header>
<main id="main" class="wrap {e(page_class)}">
{body}
</main>
<footer class="site-footer"><div class="wrap footer-inner">
<p>Guanyi Yang<br>Department of Economics &amp; Business · Colorado College</p>
<div class="footer-links">
<a href="mailto:{e(EMAIL)}">Email</a>
<a href="{e(SCHOLAR)}">Google Scholar</a>
<a href="{e(REPEC)}">RePEc</a>
<a href="{e(GITHUB)}">GitHub</a>
</div>
</div></footer>
</body>
</html>
"""


def citation(p):
    text = f"{author_str(p)} ({p['year']}). {p['title']}. {p['venue']}"
    if p.get("venue_detail"):
        text += ", " + p["venue_detail"].rstrip(".")
    text += "."
    if p.get("doi"):
        text += " https://doi.org/" + p["doi"]
    elif p.get("arxiv"):
        text += " https://arxiv.org/abs/" + p["arxiv"]
    return text


def bib_escape(value):
    return str(value).replace("\\", r"\textbackslash{}").replace("&", r"\&").replace("%", r"\%").replace("_", r"\_")


def bibtex(p):
    key = re.sub(r"[^a-zA-Z0-9]", "", p["authors"][0][0].split()[-1] + str(p["year"]) + p["slug"].split("-")[0]).lower()
    kind = {"article": "article", "report": "techreport"}.get(p["kind"], "unpublished")
    fields = [
        ("title", p["title"]),
        ("author", " and ".join(n for n, _ in p["authors"])),
        ("year", p["year"]),
    ]
    if p["kind"] == "article":
        fields.append(("journal", p["venue"]))
    elif p["kind"] == "report":
        fields.append(("institution", p["venue"]))
    for source, target in (("volume", "volume"), ("issue", "number")):
        if p.get(source):
            fields.append((target, p[source]))
    if p.get("first_page"):
        pages = str(p["first_page"])
        if p.get("last_page") and str(p["last_page"]) != pages:
            pages += "--" + str(p["last_page"])
        fields.append(("pages", pages))
    elif p.get("article_number"):
        fields.append(("pages", p["article_number"]))
    if p.get("doi"):
        fields.append(("doi", p["doi"]))
    if p.get("arxiv"):
        fields.extend([("eprint", p["arxiv"]), ("archivePrefix", "arXiv")])
    if p["kind"] != "article" and p.get("venue_detail"):
        fields.append(("note", p["venue_detail"]))
    fields.append(("url", paper_url(p)))
    values = ",\n".join("  " + name + " = {" + bib_escape(value) + "}" for name, value in fields)
    return "@" + kind + "{" + key + ",\n" + values + "\n}\n"


def ris(p):
    lines = [("TY", "JOUR" if p["kind"] == "article" else "RPRT"), ("TI", p["title"])]
    for name, _ in p["authors"]:
        parts = name.rsplit(" ", 1)
        ris_name = parts[1] + ", " + parts[0] if len(parts) == 2 and "," not in name else name
        lines.append(("AU", ris_name))
    lines.extend([("PY", str(p["year"])), ("DA", published_date(p).replace("-", "/"))])
    if p["kind"] == "article":
        lines.append(("JO", p["venue"]))
    elif p.get("venue"):
        lines.append(("PB", p["venue"]))
    for source, tag in (("volume", "VL"), ("issue", "IS"), ("first_page", "SP"), ("last_page", "EP"), ("doi", "DO")):
        if p.get(source):
            lines.append((tag, str(p[source])))
    if p.get("article_number") and not p.get("first_page"):
        lines.append(("SP", str(p["article_number"])))
    lines.extend([("UR", paper_url(p)), ("AB", p["abstract"])])
    if pdf_url(p):
        lines.append(("L1", pdf_url(p)))
    if p.get("version_note"):
        lines.append(("N1", p["version_note"]))
    lines.extend(("KW", word) for word in p.get("keywords", []))
    return "\n".join(f"{tag}  - {str(value).replace(chr(10), ' ')}" for tag, value in lines) + "\nER  -\n"


def citation_meta(p):
    tags = [("citation_title", p["title"])]
    tags.extend(("citation_author", name) for name, _ in p["authors"])
    # Scholar documents a complete date when known, or the citation year alone.
    source_date = published_date(p)
    citation_date = source_date.replace("-", "/") if re.fullmatch(r"\d{4}-\d{2}-\d{2}", source_date) else str(p["year"])
    tags.append(("citation_publication_date", citation_date))
    if p.get("online_date"):
        tags.append(("citation_online_date", str(p["online_date"]).replace("-", "/")))
    if p["kind"] == "article":
        tags.append(("citation_journal_title", p["venue"]))
    for source, target in (
        ("volume", "citation_volume"), ("issue", "citation_issue"),
        ("first_page", "citation_firstpage"), ("last_page", "citation_lastpage"),
        ("doi", "citation_doi"), ("issn", "citation_issn"),
    ):
        if p.get(source):
            tags.append((target, p[source]))
    if p.get("article_number") and not p.get("first_page"):
        tags.append(("citation_firstpage", p["article_number"]))
    if pdf_url(p):
        tags.append(("citation_pdf_url", pdf_url(p)))
    tags.extend([("citation_abstract_html_url", paper_url(p)), ("citation_language", "en")])
    return "\n".join(f'<meta name="{name}" content="{e(value)}">' for name, value in tags)


def related_url(cite, supplied=None):
    identifier = supplied or DOIS.get(cite)
    if not identifier:
        return None
    return identifier if identifier.startswith("http") else "https://doi.org/" + identifier


def rel_link(cite, supplied=None):
    link = related_url(cite, supplied)
    return f'<a href="{e(link)}">{e(cite)}</a>' if link else e(cite)


def jsonld_article(p):
    canon = paper_url(p)
    authors = []
    for name, _ in p["authors"]:
        author = {"@type": "Person", "name": name}
        if name == NAME:
            author.update({"@id": url() + "#person", "url": url()})
        authors.append(author)
    ld = {
        "@type": "Report" if p["kind"] == "report" else "ScholarlyArticle",
        "@id": canon + "#article", "url": canon, "name": p["title"], "headline": p["title"],
        "mainEntityOfPage": {"@id": canon + "#webpage"},
        "author": authors, "datePublished": published_date(p),
        "abstract": p["abstract"], "description": summary_text(p), "inLanguage": "en",
        "keywords": p.get("keywords", []),
    }
    if p.get("doi"):
        ld["identifier"] = {"@type": "PropertyValue", "propertyID": "DOI", "value": p["doi"]}
        ld["sameAs"] = ["https://doi.org/" + p["doi"]]
    if p.get("arxiv"):
        ld.setdefault("sameAs", []).append("https://arxiv.org/abs/" + p["arxiv"])
    if p["kind"] == "article":
        container = {"@type": "Periodical", "name": p["venue"]}
        if p.get("issn"):
            container["issn"] = p["issn"]
        if p.get("volume"):
            container = {"@type": "PublicationVolume", "volumeNumber": str(p["volume"]), "isPartOf": container}
        if p.get("issue"):
            container = {"@type": "PublicationIssue", "issueNumber": str(p["issue"]), "isPartOf": container}
        ld["isPartOf"] = container
    if p.get("first_page"):
        ld["pageStart"] = str(p["first_page"])
    if p.get("last_page"):
        ld["pageEnd"] = str(p["last_page"])
    if p.get("article_number"):
        ld["pagination"] = str(p["article_number"])
    if pdf_url(p):
        ld["encoding"] = {
            "@type": "MediaObject", "@id": canon + "#pdf",
            "name": p.get("pdf_label", "Full paper"),
            "contentUrl": pdf_url(p), "encodingFormat": "application/pdf",
        }
        ld["isAccessibleForFree"] = True
    return ld


def detail_links(p):
    links = []
    if pdf_url(p):
        links.append(f'<a class="primary" href="{e(pdf_url(p))}">{e(p.get("pdf_label", "Read paper (PDF)"))}</a>')
    if p.get("doi"):
        label = "Journal article" if p["kind"] == "article" else "Paper DOI"
        links.append(f'<a href="https://doi.org/{e(p["doi"])}">{label}</a>')
    if p.get("arxiv"):
        links.append(f'<a href="https://arxiv.org/abs/{e(p["arxiv"])}">arXiv</a>')
    links.extend([
        f'<a href="{e(paper_url(p))}citation.bib" download>BibTeX</a>',
        f'<a href="{e(paper_url(p))}citation.ris" download>RIS</a>',
    ])
    return '<div class="download-links" aria-label="Paper and citation downloads">' + "".join(links) + "</div>"


def paper_page(p):
    path = paper_path(p)
    theme = pd.THEMES[p["theme"]]
    status = STATUS.get(p["kind"], p["kind"].capitalize())
    venue = p["venue"] + (", " + p["venue_detail"] if p.get("venue_detail") else "")
    body = [
        f'<nav class="breadcrumb" aria-label="Breadcrumb"><a href="{e(url("research/"))}">Research</a><span aria-hidden="true">/</span><a href="{e(url("themes/" + p["theme"] + "/"))}">{e(THEME_LABELS.get(p["theme"], theme["title"]))}</a></nav>',
        '<article>',
        '<header class="paper-header">',
        f'<p class="paper-status">{e(status)} · {e(date_label(published_date(p)))}</p>',
        f'<h1>{e(p["title"])}</h1>',
        f'<p class="paper-authors">{e(author_str(p))}</p>',
        f'<p class="publication-line">{e(venue)}</p>',
        detail_links(p),
    ]
    if p.get("version_note"):
        body.append(f'<p class="version-note">{e(p["version_note"])}</p>')
    body.extend(['</header>', '<div class="paper-body">'])
    abstract_title = "Research summary" if p.get("abstract_is_summary") else "Abstract"
    body.append(f'<section class="paper-section" aria-labelledby="abstract-title"><h2 id="abstract-title">{abstract_title}</h2><p class="abstract">{e(p["abstract"])}</p></section>')
    if p.get("findings"):
        body.append('<section class="paper-section" aria-labelledby="findings-title"><h2 id="findings-title">Main findings</h2><ul>' + "".join(f"<li>{e(x)}</li>" for x in p["findings"]) + "</ul></section>")
    body.append('<section class="paper-section" aria-labelledby="method-title"><h2 id="method-title">Data and approach</h2><dl class="evidence-grid">')
    for label, key in (("Data", "data"), ("Method", "method"), ("Contribution", "whats_new"), ("Funding", "funding")):
        if p.get(key):
            body.append(f"<dt>{label}</dt><dd>{e(p[key])}</dd>")
    body.append("</dl></section>")
    if p.get("limits"):
        body.append('<section class="paper-section" aria-labelledby="scope-title"><h2 id="scope-title">Scope and interpretation</h2><ul>' + "".join(f"<li>{e(x)}</li>" for x in p["limits"]) + "</ul></section>")
    if p.get("context"):
        body.append('<section class="paper-section" aria-labelledby="context-title"><h2 id="context-title">Context</h2><ul>' + "".join(f"<li>{e(x)}</li>" for x in p["context"]) + "</ul></section>")
    if p.get("questions"):
        body.append('<section class="paper-section" aria-labelledby="questions-title"><h2 id="questions-title">Further questions</h2>' + "".join(f"<h3>{e(q)}</h3><p>{e(a)}</p>" for q, a in p["questions"]) + "</section>")
    body.append('<section class="paper-section" aria-labelledby="resources-title"><h2 id="resources-title">Paper and resources</h2><ul class="sources-list">')
    body.extend(f'<li><a href="{e(link)}">{e(label)}</a></li>' for label, link in versions(p))
    body.append(f'<li><a href="{e(paper_url(p))}llms.txt">Research note (plain text)</a></li></ul>')
    if p.get("keywords"):
        body.append(f'<p class="topic-line"><strong>Topics:</strong> {e("; ".join(p["keywords"]))}.</p>')
    if p.get("jel"):
        body.append(f'<p class="topic-line"><strong>JEL:</strong> {e(", ".join(p["jel"]))}.</p>')
    if p.get("jel_note"):
        body.append(f'<p class="meta">{e(p["jel_note"])}</p>')
    body.append("</section>")
    if p.get("related"):
        body.append('<details><summary>Related literature</summary><ul class="sources-list">' + "".join(f"<li>{rel_link(cite, doi)}</li>" for cite, doi in p["related"]) + "</ul></details>")
    body.append(f'<details id="citation"><summary>Citation and export</summary><p class="citation">{e(citation(p))}</p><p class="meta"><a href="{e(paper_url(p))}citation.bib" download>Download BibTeX</a> · <a href="{e(paper_url(p))}citation.ris" download>Download RIS</a></p><pre>{e(bibtex(p))}</pre></details>')
    body.append(f'<p class="meta paper-note">Page updated {e(date_label(reviewed_date(p)))}. <a href="{e(url("research/"))}">View all research</a>.</p></div></article>')
    extra = citation_meta(p) + f'\n<link rel="alternate" type="text/plain" title="Research note" href="{e(paper_url(p))}llms.txt">'
    return path, page(p["title"] + " | Guanyi Yang", "\n".join(body), summary_text(p), path, jsonld_article(p), extra, "research", reviewed_date(p))


def paper_li(p):
    links = []
    if pdf_url(p):
        links.append(f'<a href="{e(pdf_url(p))}" aria-label="{e(p.get("pdf_label", "PDF") + ": " + p["title"])}">PDF</a>')
    if p.get("doi"):
        links.append(f'<a href="https://doi.org/{e(p["doi"])}">DOI</a>')
    elif p.get("arxiv"):
        links.append(f'<a href="https://arxiv.org/abs/{e(p["arxiv"])}">arXiv</a>')
    links.append(f'<a href="{e(paper_url(p))}">Abstract and details</a>')
    venue = p["venue"]
    if p["kind"] == "article" and p.get("volume"):
        venue += " " + str(p["volume"])
        if p.get("issue"):
            venue += "(" + str(p["issue"]) + ")"
    return f"""<li class="paper-row">
<div class="paper-year">{e(p["year"])}</div>
<div><h3><a href="{e(paper_url(p))}">{e(p["title"])}</a></h3>
<p class="paper-byline">{e(author_str(p))}</p>
<p class="paper-venue">{e(venue)}</p>
<p class="paper-summary">{e(summary_text(p))}</p>
<div class="paper-links">{"".join(links)}</div></div>
</li>"""


def coauthor_text(item):
    names = item.get("coauthors", "")
    if isinstance(names, list):
        names = ", ".join(str(name) for name in names)
    return "With " + names if names else ""


def in_progress_li(item):
    authors = coauthor_text(item)
    return f'<li class="paper-row"><div class="paper-year"><span class="draft-status">In progress</span></div><div><h3>{e(item["title"])}</h3>' + (f'<p class="paper-byline">{e(authors)}</p>' if authors else "") + f'<p class="meta">{e(item.get("status", "Draft forthcoming"))}</p></div></li>'


def theme_links():
    return '<ul class="theme-links" aria-label="Research themes">' + "".join(
        f'<li><a href="{e(url("themes/" + key + "/"))}" title="{e(value["title"])}">{e(THEME_LABELS.get(key, value["title"]))}</a></li>'
        for key, value in pd.THEMES.items()
    ) + "</ul>"


def paper_section(title, anchor, papers):
    if not papers:
        return ""
    return f'<section class="research-section" id="{anchor}" aria-labelledby="{anchor}-heading"><div class="section-title"><h2 id="{anchor}-heading">{title}</h2><span class="section-count">{len(papers)}</span></div><ul class="paperlist">' + "".join(paper_li(p) for p in papers) + "</ul></section>"


def progress_section(items):
    if not items:
        return ""
    return f'<section class="research-section in-progress" id="in-progress" aria-labelledby="progress-heading"><div class="section-title"><h2 id="progress-heading">Research in progress</h2><span class="section-count">{len(items)}</span></div><ul class="paperlist">' + "".join(in_progress_li(p) for p in items) + "</ul></section>"


def research_page():
    papers = sorted(pd.PAPERS, key=lambda p: (-int(p["year"]), p["title"]))
    groups = [
        ("Working papers", "working-papers", [p for p in papers if p["kind"] == "working paper"]),
        ("Publications", "publications", [p for p in papers if p["kind"] == "article"]),
        ("Reports", "reports", [p for p in papers if p["kind"] == "report"]),
    ]
    jump = [f'<a href="#{anchor}">{title}<span>{len(items)}</span></a>' for title, anchor, items in groups if items]
    if pd.IN_PROGRESS:
        jump.append(f'<a href="#in-progress">In progress<span>{len(pd.IN_PROGRESS)}</span></a>')
    body = [
        '<div class="intro"><p class="eyebrow">Guanyi Yang · Economics</p><h1>Research</h1>',
        '<p class="lede">I study how labor markets, education, and unequal resources shape economic opportunity. My work combines quantitative macroeconomic models with empirical research on families, emerging economies, and the value of the natural environment.</p></div>',
        theme_links(),
        '<nav class="jump-links" aria-label="Research sections">' + "".join(jump) + "</nav>",
    ]
    body.extend(paper_section(title, anchor, items) for title, anchor, items in groups)
    body.append(progress_section(pd.IN_PROGRESS))
    body.append('<section class="research-section" id="other-writing"><h2>Other writing</h2><p class="meta">Yang, G. (2012). <a href="https://fraser.stlouisfed.org/title/economic-trends-federal-reserve-bank-cleveland-3952/economic-trends-august-2012-493107?page=25">A Look at Ohio’s Foreign-Born Population</a>. <em>Economic Trends</em>, Federal Reserve Bank of Cleveland, August 6, 2012.</p></section>')
    body.append(f'<p class="meta research-footnote">Full publication records: <a href="{e(SCHOLAR)}">Google Scholar</a> · <a href="{e(REPEC)}">RePEc / IDEAS</a> · <a href="{e(url("cv/"))}">CV</a></p>')
    desc = "Publications and working papers by Guanyi Yang on labor markets, education, inequality, emerging economies, and environmental valuation."
    return "research/", page("Research | Guanyi Yang", "\n".join(body), desc, "research/", active="research")


def theme_page(key, value):
    papers = sorted((p for p in pd.PAPERS if p["theme"] == key), key=lambda p: (-int(p["year"]), p["title"]))
    wips = [p for p in pd.IN_PROGRESS if p["theme"] == key]
    body = [
        f'<nav class="breadcrumb" aria-label="Breadcrumb"><a href="{e(url("research/"))}">Research</a><span aria-hidden="true">/</span><span>{e(THEME_LABELS.get(key, value["title"]))}</span></nav>',
        f'<div class="intro"><p class="eyebrow">Research theme</p><h1>{e(value["title"])}</h1><p class="lede">{e(value["blurb"])}</p></div>',
        paper_section("Working papers", "working-papers", [p for p in papers if p["kind"] == "working paper"]),
        paper_section("Publications", "publications", [p for p in papers if p["kind"] == "article"]),
        paper_section("Reports", "reports", [p for p in papers if p["kind"] == "report"]),
        progress_section(wips),
        f'<p class="meta research-footnote"><a href="{e(url("research/"))}">View all research</a></p>',
    ]
    path = f"themes/{key}/"
    modified = site_page_modified(path)
    return path, page(value["title"] + " | Guanyi Yang", "\n".join(body), value["blurb"], path, active="research", modified=modified)


def home_page():
    by_slug = {p["slug"]: p for p in pd.PAPERS}
    selected = [by_slug[s] for s in (
        "racial-disparities-hiring-discrimination",
        "intermittent-college-enrollment",
        "dark-skies-great-sand-dunes",
    ) if s in by_slug]
    person = {
        "@type": "Person", "@id": url() + "#person", "name": NAME,
        "givenName": "Guanyi", "familyName": "Yang",
        "jobTitle": "Gerald L. Schlessman Assistant Professor of Economics and Business",
        "worksFor": {"@type": "CollegeOrUniversity", "name": "Colorado College", "url": "https://www.coloradocollege.edu/"},
        "alumniOf": [{"@type": "CollegeOrUniversity", "name": "The Ohio State University"}, {"@type": "CollegeOrUniversity", "name": "Ohio Wesleyan University"}],
        "email": "mailto:" + EMAIL, "url": url(),
        "sameAs": [SCHOLAR, REPEC, GITHUB, GLO, "https://www.researchgate.net/profile/Guanyi_Yang", "https://sites.google.com/site/guanyiyangeconomics"],
        "knowsAbout": ["Macroeconomics", "Labor economics", "Heterogeneous-agent models", "Economics of education", "Environmental valuation", "Racial inequality", "Emerging-market business cycles"],
    }
    body = [
        '<div class="home-hero"><section aria-labelledby="name-heading"><p class="eyebrow">Economics · Colorado College</p>',
        '<h1 id="name-heading">Guanyi Yang</h1>',
        '<p class="home-role">Gerald L. Schlessman Assistant Professor<br>of Economics and Business</p>',
        '<p class="home-copy">I study labor markets, human capital, and inequality using heterogeneous-agent macroeconomic models. My empirical work examines education and families in China, emerging-market business cycles, and the economic value of dark skies.</p>',
        f'<div class="cta-links"><a class="button" href="{e(url("research/"))}">Explore my research</a><a href="{e(url("pdf/Guanyi-Yang-CV.pdf"))}">Download CV</a></div></section>',
        '<aside class="home-sidebar" aria-label="Affiliations and contact"><h2>Affiliations</h2>',
        '<p>Research Fellow<br>Global Labor Organization</p><p>Project Director<br>State of the Rockies</p>',
        f'<h2 style="margin-top:25px">Contact</h2><p><a href="mailto:{e(EMAIL)}">{e(EMAIL)}</a></p>',
        f'<ul class="profile-links"><li><a href="{e(SCHOLAR)}">Google Scholar</a></li><li><a href="{e(REPEC)}">RePEc / IDEAS</a></li><li><a href="{e(GITHUB)}">GitHub</a></li></ul></aside></div>',
        '<section class="home-featured" aria-labelledby="selected-heading"><div class="section-heading-row"><h2 id="selected-heading">Selected research</h2>',
        f'<a href="{e(url("research/"))}">All publications and working papers</a></div><ul class="paperlist">' + "".join(paper_li(p) for p in selected) + "</ul></section>",
        '<section class="research-section" aria-labelledby="themes-heading"><h2 id="themes-heading">Areas of research</h2>' + theme_links() + "</section>",
        '<div class="home-bottom"><section><h2>Teaching and student research</h2><p>At Colorado College, I teach macroeconomics, inequality, and education policy. I also direct the State of the Rockies Dark Sky Lab, where undergraduates collaborate on environmental research.</p><p><a href="https://github.com/yangguanyi/computational-macroeconomics-starter-kit">Computational macroeconomics starter kit</a></p></section>',
        '<section><h2>Applied economics</h2><p>My consulting work includes survey design, economic valuation, causal analysis, and policy modeling.</p><p><a href="http://focalizesolutions.com">Focalize Solutions</a></p></section></div>',
    ]
    desc = "Guanyi Yang is an economist at Colorado College studying labor markets, human capital, inequality, emerging economies, and environmental valuation."
    return "", page("Guanyi Yang | Economist, Colorado College", "\n".join(body), desc, "", person, page_class="home-page")


def cv_page():
    body = [
        '<div class="standard-page"><p class="eyebrow">Guanyi Yang</p><h1>Curriculum vitae</h1>',
        f'<p><a href="{e(url("pdf/Guanyi-Yang-CV.pdf"))}">Download the CV (PDF)</a>. Summary below; the PDF is the complete record.</p>',
        "<h2>Positions</h2><ul><li>Gerald L. Schlessman Assistant Professor, Department of Economics &amp; Business, Colorado College, since September 2022 (Assistant Professor from August 2021)</li><li>Assistant Professor of Economics, St. Lawrence University, 2018–2021</li><li>Visiting scholar: Georgia State University (Andrew Young School), summer 2019; Renmin University of China, December 2018</li></ul>",
        "<h2>Affiliations</h2><ul><li>Research Fellow, Global Labor Organization (GLO), since 2022</li><li>Project Director, State of the Rockies, Colorado College, since 2023</li></ul>",
        "<h2>Education</h2><ul><li>Ph.D. Economics, The Ohio State University, 2018. Dissertation: Essays on Labor Market Frictions and Macroeconomic Welfare</li><li>M.A. Economics, The Ohio State University, 2014</li><li>B.A. Mathematics and Economics, Ohio Wesleyan University, 2013 (magna cum laude)</li></ul>",
        "<h2>Fields</h2><p>Macroeconomics; labor economics; inequality; heterogeneous-agent models; environmental valuation; economics of education.</p>",
        "<h2>Selected awards and grants</h2><ul><li>Andrew Carnegie Fellows Program, Colorado College’s sole pretenure nominee; final round of national selection, 2025–2026</li><li>Sidney G. Winter Award for excellence in teaching and research in Business and Economics, Colorado College, 2025</li><li>Dean of the Faculty Teaching Excellence Award, Colorado College, 2024</li><li>Jackson Fellowships, Hulbert Center for Southwest Studies, 2023 and 2024</li><li>Faculty-Student Collaborative Research Grant, Colorado College, 2022–2026</li><li>Guangdong Province Philosophy and Social Science Planning Project (Co-PI), 2026</li><li>Elsevier Best Paper Award, 10th International Symposium on Human Capital and Labor Markets, 2018</li></ul>",
        f'<p><a href="{e(url("research/"))}">Publications and working papers</a></p></div>',
    ]
    return "cv/", page("CV | Guanyi Yang", "\n".join(body), "Curriculum vitae of Guanyi Yang, economist at Colorado College.", "cv/", active="cv")


def more_page():
    body = [
        '<div class="standard-page"><p class="eyebrow">Guanyi Yang</p><h1>More</h1>',
        "<h2>Media and public writing</h2><ul>"
        "<li><a href='https://www.coloradocollege.edu/other/stateoftherockies/_documents/2024-anthropogenic-article-pdfs/The%20Economics%20of%20the%20Night%20Sky%202024.pdf'>The Economics of the Night Sky</a> (State of the Rockies, 2024)</li>"
        "<li><a href='https://thepeak.coloradocollege.edu/2024/01/09/cc-and-unc-team-research-dark-sky-tourism/'>CC and UNC Team Research Dark Sky Tourism</a> (The Peak, January 2024)</li>"
        "<li><a href='https://thepeak.coloradocollege.edu/2023/09/15/macroeconomics-class-emphasizes-community-engaged-learning/'>Macroeconomics Class Emphasizes Community-Engaged Learning</a> (The Peak, September 2023)</li></ul>",
        "<h2>Consulting</h2><p><a href='http://focalizesolutions.com'>Focalize Solutions</a>.</p>",
        "<h2>Resources for students and researchers</h2><ul>"
        "<li><a href='https://github.com/yangguanyi/computational-macroeconomics-starter-kit'>Computational macroeconomics starter kit</a> (lecture notes and MATLAB code)</li>"
        "<li><a href='https://www.researchincolor.org/'>Research in Color Foundation</a></li>"
        "<li><a href='https://www.aeaweb.org/resources/online-seminars'>AEA list of online seminars</a></li>"
        "<li><a href='https://twitter.com/econ_ra'>RA and internship listings (@econ_ra)</a></li>"
        "<li><a href='https://docs.google.com/spreadsheets/d/17UlG3Er7MD1EajGIyiiI-adCw77RfWTkFeU9kpp2-zI/edit#gid=0'>Grant opportunities for graduate students and early-career economists</a></li>"
        "<li><a href='https://www.briancjenkins.com/teaching.html'>Brian Jenkins’ undergraduate macroeconomic simulation package</a></li>"
        "<li><a href='https://sites.google.com/view/pankabencsik/econbrew'>#EconBrew</a></li></ul>",
        "<h2>Outside work</h2><ul><li><a href='https://youtu.be/9T2lSy2hMWo?si=rJOLzE-ZE4Rb1gpE'>Colorado College Concert Band</a></li><li><a href='https://www.dropbox.com/sh/cs2gbctzlf430k4/AACbmx7k854AGeuIMGX_6Msva?dl=0'>Photography</a></li></ul></div>",
    ]
    return "more/", page("More | Guanyi Yang", "\n".join(body), "Media coverage, consulting, resources for students, and other interests.", "more/", active="more")


def llms_txt(p):
    lines = [
        "# " + p["title"], "", "> " + summary_text(p), "",
        "Authors: " + author_str(p),
        "Status: " + STATUS.get(p["kind"], p["kind"]),
        "Publication: " + p["venue"] + (", " + p["venue_detail"] if p.get("venue_detail") else ""),
        "Publication date: " + published_date(p),
        "Page: " + paper_url(p),
        "Research note updated: " + reviewed_date(p),
    ]
    if p.get("doi"):
        lines.append("DOI: https://doi.org/" + p["doi"])
    if p.get("version_note"):
        lines.append("Version: " + p["version_note"])
    lines.extend(["", "## " + ("Research summary" if p.get("abstract_is_summary") else "Abstract"), "", p["abstract"]])
    for heading, field in (("Key findings", "findings"), ("Scope and interpretation", "limits"), ("Context", "context")):
        if p.get(field):
            lines.extend(["", "## " + heading, ""] + ["- " + value for value in p[field]])
    lines.extend(["", "## Data and approach", "", "Data: " + p["data"], "", "Method: " + p["method"], "", "Contribution: " + p["whats_new"]])
    if p.get("funding"):
        lines.extend(["", "Funding: " + p["funding"]])
    lines.extend(["", "## Paper and resources", ""] + [f"- [{label}]({link})" for label, link in versions(p)])
    if p.get("related"):
        lines.extend(["", "## Related literature", ""])
        for cite, identifier in p["related"]:
            link = related_url(cite, identifier)
            lines.append("- " + cite + (" " + link if link else ""))
    lines.extend(["", "## Citation", "", citation(p), "", "BibTeX: " + paper_url(p) + "citation.bib", "RIS: " + paper_url(p) + "citation.ris", ""])
    return "\n".join(lines)


def root_llms():
    lines = [
        "# Guanyi Yang: research", "",
        "> Economist at Colorado College. Research on labor markets, human capital, inequality, emerging economies, and environmental valuation.", "",
        "The HTML paper pages, PDFs, and plain-text research notes below describe the same research. Publication status, version information, and scope are recorded on each page.", "",
        "Research index: " + url("research/"), "", "## Papers", "",
    ]
    for p in sorted(pd.PAPERS, key=lambda p: (-int(p["year"]), p["title"])):
        lines.append(f"- [{p['title']}]({paper_url(p)}): {summary_text(p)} ({p['venue']}, {p['year']}). Research note: {paper_url(p)}llms.txt")
    if pd.IN_PROGRESS:
        lines.extend(["", "## Research in progress", ""])
        for item in pd.IN_PROGRESS:
            line = "- " + item["title"]
            if coauthor_text(item):
                line += ". " + coauthor_text(item) + "."
            line += " " + item.get("status", "Draft forthcoming") + "."
            lines.append(line)
    lines.extend(["", "## Themes", ""] + [f"- [{v['title']}]({url('themes/' + k + '/')})" for k, v in pd.THEMES.items()])
    lines.extend(["", "## Profiles", "", "- Google Scholar: " + SCHOLAR, "- RePEc: " + REPEC, "- CV: " + url("cv/"), ""])
    return "\n".join(lines)


def validate_source():
    slugs = set()
    for p in pd.PAPERS:
        slug = p["slug"]
        if slug in slugs or not re.fullmatch(r"[a-z0-9-]+", slug):
            raise ValueError("Duplicate or invalid paper slug: " + slug)
        slugs.add(slug)
        if p["theme"] not in pd.THEMES:
            raise ValueError("Unknown paper theme: " + p["theme"])
        for field in ("publication_date", "online_date", "reviewed_on"):
            if p.get(field) and not re.fullmatch(r"\d{4}(?:-\d{2}(?:-\d{2})?)?", str(p[field])):
                raise ValueError("Invalid source date " + field + " for " + slug)
        if p.get("pdf_path"):
            relative = pathlib.PurePosixPath(p["pdf_path"])
            if relative.is_absolute() or ".." in relative.parts or relative.parent != pathlib.PurePosixPath(paper_path(p)):
                raise ValueError("The primary PDF must be in the paper's own directory: " + slug)
            if not (ROOT / p["pdf_path"]).is_file():
                raise FileNotFoundError("Missing checked-in primary PDF: " + p["pdf_path"])
    for item in pd.IN_PROGRESS:
        if item["slug"] in slugs:
            raise ValueError("A forthcoming project duplicates a public paper: " + item["slug"])
        if item["theme"] not in pd.THEMES:
            raise ValueError("Unknown forthcoming-project theme: " + item["theme"])


def copy_file(source, target):
    if source.resolve() == target.resolve():
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def copy_assets():
    if OUT.resolve() == ROOT.resolve():
        return
    for name in ("pdf", "assets", "images", ".well-known"):
        source = ROOT / name
        if source.is_dir():
            shutil.copytree(source, OUT / name, dirs_exist_ok=True)
    for p in pd.PAPERS:
        if p.get("pdf_path"):
            copy_file(ROOT / p["pdf_path"], OUT / p["pdf_path"])
    for source in ROOT.iterdir():
        if source.is_file() and (
            source.name == "CNAME"
            or source.name.startswith("favicon")
            or (source.suffix in (".html", ".txt") and source.name not in ("index.html", "llms.txt", "robots.txt"))
        ):
            copy_file(source, OUT / source.name)


def robots_text():
    source = ROOT / "robots.txt"
    text = source.read_text(encoding="utf-8") if source.exists() else "User-agent: *\nAllow: /\n"
    sitemap = "Sitemap: " + url("sitemap.xml")
    if re.search(r"(?im)^Sitemap:.*?/sitemap\.xml\s*$", text):
        text = re.sub(r"(?im)^Sitemap:.*?/sitemap\.xml\s*$", sitemap, text)
    elif sitemap not in text:
        text = text.rstrip() + "\n\n" + sitemap
    return text.rstrip() + "\n"


def main():
    global BASE, OUT
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_dir", nargs="?", default=str(ROOT))
    parser.add_argument("base_url", nargs="?", default=BASE)
    args = parser.parse_args()
    OUT = pathlib.Path(args.output_dir).resolve()
    BASE = args.base_url.rstrip("/")
    if not BASE.startswith(("https://", "http://")):
        parser.error("base_url must be an absolute HTTP(S) URL")
    validate_source()
    OUT.mkdir(parents=True, exist_ok=True)
    # Read crawler policy before writing, including when rebuilding in place.
    robots = robots_text()
    copy_assets()
    (OUT / ".nojekyll").write_text("", encoding="utf-8")
    (OUT / "style.css").write_text(CSS.strip() + "\n", encoding="utf-8")
    sitemap = {}
    for p in pd.PAPERS:
        path, rendered = paper_page(p)
        folder = OUT / path
        folder.mkdir(parents=True, exist_ok=True)
        for filename, contents in (
            ("index.html", rendered), ("llms.txt", llms_txt(p)),
            ("citation.bib", bibtex(p)), ("citation.ris", ris(p)),
        ):
            (folder / filename).write_text(contents, encoding="utf-8")
        sitemap[path] = reviewed_date(p)
    for key, value in pd.THEMES.items():
        path, rendered = theme_page(key, value)
        folder = OUT / path
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "index.html").write_text(rendered, encoding="utf-8")
        sitemap[path] = site_page_modified(path)
    for fn in (research_page, home_page, cv_page, more_page):
        path, rendered = fn()
        folder = OUT / path
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "index.html").write_text(rendered, encoding="utf-8")
        sitemap[path] = site_page_modified(path)
    (OUT / "llms.txt").write_text(root_llms(), encoding="utf-8")
    (OUT / "robots.txt").write_text(robots, encoding="utf-8")
    entries = "\n".join(
        f"  <url><loc>{e(url(path))}</loc><lastmod>{e(modified)}</lastmod></url>"
        for path, modified in sorted(sitemap.items())
    )
    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + entries + "\n</urlset>\n", encoding="utf-8",
    )
    print(f"Built {len(sitemap)} HTML pages, {len(pd.PAPERS)} paper notes, and BibTeX/RIS exports in {OUT}")


if __name__ == "__main__":
    main()
