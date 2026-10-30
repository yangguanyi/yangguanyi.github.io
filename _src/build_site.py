#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the static site: one page per paper, theme hubs, research index, home, CV, machine files.
Usage: python3 build_site.py <output_dir> [base_url]
"""
import sys, json, html, pathlib, re, importlib.util, datetime, shutil

HERE = pathlib.Path(__file__).parent
spec = importlib.util.spec_from_file_location("pd", HERE / "papers_data.py")
pd = importlib.util.module_from_spec(spec); spec.loader.exec_module(pd)
DOIS = json.load(open(HERE / "dois.json"))

OUT = pathlib.Path(sys.argv[1]); BASE = (sys.argv[2] if len(sys.argv) > 2 else "https://yangguanyi.github.io").rstrip("/")
TODAY = datetime.date.today().isoformat()
NAME = "Guanyi Yang"
SCHOLAR = "https://scholar.google.com/citations?user=nlgkEE8AAAAJ&hl=en"
REPEC = "https://ideas.repec.org/f/pya376.html"
GITHUB = "https://github.com/yangguanyi"
GLO = "https://glabor.org/user/gyang/"
EMAIL = "gyang@ColoradoCollege.edu"

# Local PDF copies (descriptive names) -> source file in the Working-papers clone
PDF_MAP = {
 "https://github.com/yangguanyi/Working-papers/raw/master/Search_and_match_and_racial_inequity.pdf": "Murali-Yang-2025-Macroeconomics-of-Racial-Disparities.pdf",
 "https://github.com/yangguanyi/Working-papers/raw/master/College_timing_endowment.pdf": "Yang-2025-Better-Late-Than-Never-Intermittent-College-Enrollment-WP.pdf",
 "https://github.com/yangguanyi/Working-papers/raw/master/Contingent_Behavior_Modeling_for_Dark_Skies_Valuation_at_Great_Sand_Dunes_National_Park.pdf": "Eiswerth-Mullen-Yang-2026-Dark-Skies-Valuation-Great-Sand-Dunes-WP.pdf",
 "https://github.com/yangguanyi/Working-papers/raw/master/GFR_and_equity_returns.pdf": "Horvath-Yang-2023-Global-Financial-Risk-Equity-Returns-Emerging-Countries-WP.pdf",
 "https://github.com/yangguanyi/Working-papers/raw/master/sib_spillover_China.pdf": "Bansak-Jiang-Yang-2022-Sibling-Spillovers-Rural-China-WP.pdf",
}
WP_SRC = pathlib.Path("/tmp/claude-0/-home-claude/87876bce-ade7-545d-96d6-27fe0d1359a3/scratchpad/repos/Working-papers")

def e(s): return html.escape(s, quote=True)
def local_pdf(url):
    return f"{BASE}/pdf/{PDF_MAP[url]}" if url in PDF_MAP else url

CSS = """
:root{--bg:#fff;--fg:#1a1a1a;--muted:#555;--line:#ddd;--accent:#0b4f8a;--soft:#f4f6f8}
@media (prefers-color-scheme:dark){:root{--bg:#121416;--fg:#e8e8e8;--muted:#a9a9a9;--line:#333;--accent:#7fb3e6;--soft:#1c2024}}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--fg);font:17px/1.55 Georgia,"Times New Roman",serif}
header,main,footer{max-width:46rem;margin:0 auto;padding:0 16px}
header{padding-top:18px;padding-bottom:10px;border-bottom:1px solid var(--line);font-family:system-ui,-apple-system,"Segoe UI",Helvetica,Arial,sans-serif;font-size:15px}
header a{color:var(--fg);text-decoration:none;margin-right:16px}header a.site{font-weight:700}
h1{font-size:1.7rem;line-height:1.25;margin:1.2rem 0 .4rem}h2{font-size:1.2rem;margin:1.8rem 0 .5rem;font-family:system-ui,-apple-system,"Segoe UI",Helvetica,Arial,sans-serif}
h3{font-size:1.05rem;margin:1.3rem 0 .3rem}a{color:var(--accent)}p{margin:.6rem 0}ul,ol{padding-left:1.3rem}li{margin:.3rem 0}
.meta{color:var(--muted);font-family:system-ui,-apple-system,"Segoe UI",Helvetica,Arial,sans-serif;font-size:.95rem}
.lead{font-size:1.1rem;border-left:4px solid var(--accent);padding:.3rem 0 .3rem .9rem;margin:1rem 0;background:var(--soft)}
blockquote{margin:.8rem 0;padding:.2rem 0 .2rem 1rem;border-left:3px solid var(--line);color:var(--fg)}
dl{display:grid;grid-template-columns:9rem 1fr;gap:.35rem 1rem}dt{color:var(--muted);font-family:system-ui,sans-serif;font-size:.9rem}dd{margin:0}
@media (max-width:600px){dl{grid-template-columns:1fr}dt{margin-top:.5rem}}
pre{background:var(--soft);padding:.8rem;overflow:auto;font-size:.85rem;border:1px solid var(--line)}
.paperlist li{margin:.9rem 0}.paperlist .t{font-weight:700}.paperlist .one{display:block;color:var(--muted);font-size:.95rem}
footer{border-top:1px solid var(--line);margin-top:3rem;padding:1rem 16px 2rem;color:var(--muted);font-size:.9rem;font-family:system-ui,sans-serif}
.tag{display:inline-block;background:var(--soft);border:1px solid var(--line);border-radius:4px;padding:0 .4rem;margin:0 .25rem .25rem 0;font-size:.85rem;font-family:system-ui,sans-serif}
"""

def page(title, body, desc, path, jsonld=None, extra_head=""):
    canon = f"{BASE}/{path}".rstrip("/") + ("/" if not path.endswith(".html") and path else "")
    ld = f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>' if jsonld else ""
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc[:300])}">
<meta name="author" content="{NAME}"><link rel="canonical" href="{canon}">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc[:300])}"><meta property="og:type" content="article"><meta property="og:url" content="{canon}">
<link rel="stylesheet" href="{BASE}/style.css">{extra_head}{ld}
</head><body>
<header><a class="site" href="{BASE}/">Guanyi Yang</a> <a href="{BASE}/research/">Research</a> <a href="{BASE}/cv/">CV</a> <a href="{BASE}/more/">More</a></header>
<main>
{body}
</main>
<footer>Guanyi Yang · Department of Economics &amp; Business, Colorado College · <a href="mailto:{EMAIL}">{EMAIL}</a><br>
<a href="{SCHOLAR}">Google Scholar</a> · <a href="{REPEC}">RePEc</a> · <a href="{GITHUB}">GitHub</a> · <a href="{BASE}/llms.txt">llms.txt</a> · Updated {TODAY}</footer>
</body></html>"""

def author_str(p, with_aff=False):
    if with_aff: return "; ".join(f"{n} ({a})" for n, a in p["authors"])
    return ", ".join(n for n, a in p["authors"])

def citation(p):
    au = author_str(p)
    if p["kind"] == "article":
        return f"{au} ({p['year']}). {p['title']}. {p['venue']}, {p['venue_detail']}. https://doi.org/{p['doi']}"
    if p["kind"] == "report":
        return f"{au} ({p['year']}). {p['title']}. {p['venue']}, {p['venue_detail']}. https://doi.org/{p['doi']}"
    extra = f" arXiv:{p['arxiv']}." if p.get("arxiv") else ""
    return f"{au} ({p['year']}). {p['title']}. {p['venue']}, {p['venue_detail']}.{extra}"

def bibtex(p):
    key = (p["authors"][0][0].split()[-1] + str(p["year"]) + p["slug"].split("-")[0]).lower()
    au = " and ".join(n for n, a in p["authors"])
    if p["kind"] == "article":
        return f"@article{{{key},\n  title={{{p['title']}}},\n  author={{{au}}},\n  journal={{{p['venue']}}},\n  year={{{p['year']}}},\n  note={{{p['venue_detail']}}},\n  doi={{{p['doi']}}}\n}}"
    if p["kind"] == "report":
        return f"@techreport{{{key},\n  title={{{p['title']}}},\n  author={{{au}}},\n  institution={{{p['venue']}}},\n  year={{{p['year']}}},\n  note={{{p['venue_detail']}}},\n  doi={{{p['doi']}}}\n}}"
    note = p['venue_detail'] + (f"; arXiv:{p['arxiv']}" if p.get("arxiv") else "")
    return f"@unpublished{{{key},\n  title={{{p['title']}}},\n  author={{{au}}},\n  year={{{p['year']}}},\n  note={{{note}}}\n}}"

def rel_link(cite):
    d = DOIS.get(cite)
    if not d: return e(cite)
    url = d if d.startswith("http") else f"https://doi.org/{d}"
    return f'{e(cite)} <a href="{url}">{"link" if d.startswith("http") else "doi:"+e(d)}</a>'

def jsonld_article(p, url):
    typ = "ScholarlyArticle" if p["kind"] != "report" else "Report"
    ld = {"@context":"https://schema.org","@type":typ,"headline":p["title"],"name":p["title"],"url":url,
          "author":[{"@type":"Person","name":n,"affiliation":{"@type":"Organization","name":a}} for n,a in p["authors"]],
          "datePublished":str(p["year"]),"abstract":p["abstract"],"keywords":", ".join(p["keywords"]),
          "description":p["one_liner"],"inLanguage":"en"}
    if p.get("doi"):
        ld["identifier"] = {"@type":"PropertyValue","propertyID":"DOI","value":p["doi"]}
        ld["sameAs"] = [f"https://doi.org/{p['doi']}"]
    if p.get("arxiv"): ld.setdefault("sameAs", []).append(f"https://arxiv.org/abs/{p['arxiv']}")
    if p["kind"] == "article": ld["isPartOf"] = {"@type":"Periodical","name":p["venue"]}
    ld["citation"] = [ {"@type":"CreativeWork","name":c, **({"sameAs": (DOIS[c] if DOIS[c].startswith("http") else "https://doi.org/"+DOIS[c])} if DOIS.get(c) else {})} for c,_ in p["related"] ]
    ld["encoding"] = [{"@type":"MediaObject","contentUrl":local_pdf(u),"encodingFormat":"application/pdf"} for lab,u in p["versions"] if local_pdf(u).endswith(".pdf")]
    return ld

def paper_page(p):
    path = f"papers/{p['slug']}/"; url = f"{BASE}/{path}"
    status = {"article":"Published article","working paper":"Working paper","report":"Policy report"}[p["kind"]]
    venue_line = f"{e(p['venue'])}, {e(p['venue_detail'])}" + (f'. DOI <a href="https://doi.org/{e(p["doi"])}">{e(p["doi"])}</a>' if p.get("doi") else "") + (f'. <a href="https://arxiv.org/abs/{p["arxiv"]}">arXiv:{p["arxiv"]}</a>' if p.get("arxiv") else "")
    theme = pd.THEMES[p["theme"]]
    b = []
    b.append(f"<h1>{e(p['title'])}</h1>")
    b.append(f"<p class='meta'>{e(author_str(p, True))}<br>{status} · {venue_line}<br>Theme: <a href='{BASE}/themes/{p['theme']}/'>{e(theme['title'])}</a></p>")
    b.append(f"<p class='lead'>{e(p['one_liner'])}</p>")
    b.append("<h2>Abstract</h2>" + ("<p class='meta'>No formal abstract is attached to the report; this summary describes it.</p>" if p.get("abstract_is_summary") else "") + f"<blockquote>{e(p['abstract'])}</blockquote>")
    b.append("<h2>What this paper shows</h2><ul>" + "".join(f"<li>{e(x)}</li>" for x in p["findings"]) + "</ul>")
    b.append("<h2>What it does not show</h2><ul>" + "".join(f"<li>{e(x)}</li>" for x in p["limits"]) + "</ul>")
    if p["context"]:
        b.append("<h2>Context and definitions</h2><ul>" + "".join(f"<li>{e(x)}</li>" for x in p["context"]) + "</ul>")
    b.append("<h2>Data, method, contribution</h2><dl>"
             f"<dt>Data</dt><dd>{e(p['data'])}</dd><dt>Method</dt><dd>{e(p['method'])}</dd><dt>What is new</dt><dd>{e(p['whats_new'])}</dd>"
             + (f"<dt>Funding</dt><dd>{e(p['funding'])}</dd>" if p.get("funding") else "") + "</dl>")
    b.append("<h2>Who this is for</h2><ul>" + "".join(f"<li>{e(x)}</li>" for x in p["audiences"]) + "</ul>")
    if p["questions"]:
        b.append("<h2>Questions this paper answers</h2>" + "".join(f"<h3>{e(q)}</h3><p>{e(a)}</p>" for q,a in p["questions"]))
    b.append("<h2>Related work this paper speaks to</h2><ul>" + "".join(f"<li>{rel_link(c)}</li>" for c,_ in p["related"]) + "</ul>")
    b.append("<h2>Versions and links</h2><ul>" + "".join(f"<li><a href='{e(local_pdf(u))}'>{e(lab)}</a></li>" for lab,u in p["versions"]) + f"<li><a href='{BASE}/{path}llms.txt'>llms.txt (plain-text summary for AI assistants)</a></li></ul>")
    jel = "".join(f"<span class='tag'>JEL {e(j)}</span>" for j in p["jel"])
    kw = "".join(f"<span class='tag'>{e(k)}</span>" for k in p["keywords"])
    b.append(f"<h2>Classification</h2><p>{jel}</p>" + (f"<p class='meta'>{e(p['jel_note'])}</p>" if p.get("jel_note") else "") + f"<p>{kw}</p><p class='meta'>{e(p['synonyms'])}</p>")
    b.append(f"<h2>Cite this</h2><p>{e(citation(p))}</p><pre>{e(bibtex(p))}</pre>")
    body = "\n".join(b)
    desc = p["one_liner"]
    return path, page(p["title"], body, desc, path, jsonld_article(p, url))

def llms_txt(p):
    url = f"{BASE}/papers/{p['slug']}/"
    L = [f"# {p['title']}", "", f"> {p['one_liner']}", "",
         f"Authors: {author_str(p, True)}", f"Status: {p['venue']}, {p['venue_detail']}" + (f". DOI {p['doi']}" if p.get('doi') else "") + (f". arXiv:{p['arxiv']}" if p.get('arxiv') else ""),
         f"Page: {url}", "", "## What is this paper about?", "", p["one_liner"], "", "## Abstract", "", p["abstract"], "",
         "## Key results", ""] + [f"- {x}" for x in p["findings"]] + ["", "## Limitations and scope (what the paper does not show)", ""] + [f"- {x}" for x in p["limits"]]
    if p["context"]: L += ["", "## Important context and definitions", ""] + [f"- {x}" for x in p["context"]]
    L += ["", "## Data and methods", "", f"Data: {p['data']}", f"Method: {p['method']}", f"Contribution: {p['whats_new']}", "",
          "## Related work", ""] + [f"- {c}" + (f" https://doi.org/{DOIS[c]}" if DOIS.get(c) and not DOIS[c].startswith('http') else (f" {DOIS[c]}" if DOIS.get(c) else "")) for c,_ in p["related"]]
    L += ["", "## Versions", ""] + [f"- {lab}: {local_pdf(u)}" for lab,u in p["versions"]]
    L += ["", f"JEL: {', '.join(p['jel'])}" if p["jel"] else "", f"Keywords: {', '.join(p['keywords'])}", "", "## Cite", "", citation(p), ""]
    return "\n".join(L)

def paper_li(p):
    return f"<li class='entry'><span class='t'><a href='{BASE}/papers/{p['slug']}/'>{e(p['title'])}</a></span><br><span class='meta'>{e(author_str(p))} · {e(p['venue'])}, {p['year']}</span><span class='one'>{e(p['one_liner'])}</span></li>"

def research_page():
    arts = [p for p in pd.PAPERS if p["kind"]=="article"]; wps = [p for p in pd.PAPERS if p["kind"]=="working paper"]; reps = [p for p in pd.PAPERS if p["kind"]=="report"]
    arts.sort(key=lambda p:-p["year"])
    b = ["<h1>Research</h1>",
         "<p>Each paper has its own page with the abstract, the main numbers, what the paper does and does not show, the literature it speaks to, and every public version. Pages are grouped by theme below; the lists that follow are by publication status.</p>",
         "<h2>Themes</h2><ul>" + "".join(f"<li><a href='{BASE}/themes/{k}/'>{e(v['title'])}</a> · {sum(1 for p in pd.PAPERS if p['theme']==k)} papers</li>" for k,v in pd.THEMES.items()) + "</ul>",
         "<h2>Publications</h2><ul class='paperlist'>" + "".join(paper_li(p) for p in arts) + "</ul>",
         "<h2>Working papers</h2><ul class='paperlist'>" + "".join(paper_li(p) for p in wps) + "</ul>",
         ("<h2>Reports</h2><ul class='paperlist'>" + "".join(paper_li(p) for p in reps) + "</ul>") if reps else "",
         "<h2>Other</h2><ul><li>Yang, G. (2012). A Look at Ohio’s Foreign-Born Population. <i>Economic Trends</i>, Federal Reserve Bank of Cleveland, August 6, 2012. <a href='https://fraser.stlouisfed.org/title/economic-trends-federal-reserve-bank-cleveland-3952/economic-trends-august-2012-493107?page=25'>FRASER</a></li></ul>",
         f"<p class='meta'>Profiles: <a href='{SCHOLAR}'>Google Scholar</a> · <a href='{REPEC}'>RePEc/IDEAS</a> · <a href='https://www.researchgate.net/profile/Guanyi_Yang'>ResearchGate</a></p>"]
    return "research/", page("Research — Guanyi Yang", "\n".join(b), "Publications and working papers by Guanyi Yang, economist at Colorado College: dark skies and light pollution, college access and life-cycle risk, racial disparities, emerging-market business cycles, children and schooling in rural China.", "research/")

def theme_page(k, v):
    ps = [p for p in pd.PAPERS if p["theme"]==k]; ps.sort(key=lambda p:-p["year"])
    wip = [w for w in pd.IN_PROGRESS if w["theme"]==k]
    b = [f"<h1>{e(v['title'])}</h1>", f"<p>{e(v['blurb'])}</p>", "<ul class='paperlist'>" + "".join(paper_li(p) for p in ps) + "</ul>"]
    if wip: b.append("<h2>In progress</h2><ul>" + "".join(f"<li>{e(w['title'])} (with {e(w['coauthors'])}). {e(w['status'])}.</li>" for w in wip) + "</ul>")
    return f"themes/{k}/", page(f"{v['title']} — Guanyi Yang", "\n".join(b), v["blurb"], f"themes/{k}/")

def home_page():
    picks = {p["slug"]:p for p in pd.PAPERS}
    sel = ["dark-skies-great-sand-dunes","intermittent-college-enrollment","racial-disparities-hiring-discrimination","informality-unemployment-small-open-economies","sibling-spillovers-rural-china","global-financial-risk-equity-returns-emerging-markets"]
    ld = {"@context":"https://schema.org","@type":"Person","name":NAME,"givenName":"Guanyi","familyName":"Yang",
          "jobTitle":"Gerald L. Schlessman Assistant Professor of Economics and Business","worksFor":{"@type":"CollegeOrUniversity","name":"Colorado College","address":"14 E. Cache la Poudre St., Colorado Springs, CO 80903"},
          "alumniOf":[{"@type":"CollegeOrUniversity","name":"The Ohio State University"},{"@type":"CollegeOrUniversity","name":"Ohio Wesleyan University"}],
          "email":f"mailto:{EMAIL}","url":BASE+"/","sameAs":[SCHOLAR,REPEC,GITHUB,GLO,"https://www.researchgate.net/profile/Guanyi_Yang","https://sites.google.com/site/guanyiyangeconomics"],
          "knowsAbout":["macroeconomics","labor economics","heterogeneous-agent models","economics of education","environmental valuation","dark sky tourism","racial inequality","emerging market business cycles","informal economy","rural China"]}
    b = ["<h1>Guanyi Yang</h1>",
         "<p class='meta'>Gerald L. Schlessman Assistant Professor of Economics and Business, Colorado College · Research Fellow, Global Labor Organization · Project Director, State of the Rockies · Ph.D. Economics, The Ohio State University (2018)</p>",
         "<p>I am an economist. I build heterogeneous-agent macroeconomic models to study labor markets, human capital and inequality, and I use surveys and microeconometric methods to value environmental goods and study education in China. Current projects measure what dark skies are worth, how flexible access to college changes lifetime welfare, how hiring discrimination shapes racial gaps in jobs and wealth, and why emerging economies’ business cycles behave differently.</p>",
         "<h2>Selected findings</h2><ul>" + "".join(f"<li><a href='{BASE}/papers/{s}/'>{e(picks[s]['title'])}</a> ({picks[s]['year']}). {e(picks[s]['one_liner'])}</li>" for s in sel) + "</ul>",
         f"<p><a href='{BASE}/research/'>All papers, by theme and by status →</a></p>",
         "<h2>Research themes</h2><ul>" + "".join(f"<li><a href='{BASE}/themes/{k}/'>{e(v['title'])}</a></li>" for k,v in pd.THEMES.items()) + "</ul>",
         "<h2>Teaching</h2><p>At Colorado College I teach Principles of Macroeconomics (EC102), Macroeconomic Theory (EC302), Economics of Inequality (EC290) and Economics of Education Policy (EC385), and I direct the State of the Rockies Dark Sky Lab, where undergraduates co-author research. Materials for learning computational macroeconomics are in the <a href='https://github.com/yangguanyi/computational-macroeconomics-starter-kit'>computational macroeconomics starter kit</a>.</p>",
         "<h2>Consulting</h2><p>For applied economics consulting (survey design, causal analysis, policy modeling, economic valuation), see <a href='http://focalizesolutions.com'>Focalize Solutions</a>.</p>",
         f"<h2>Contact</h2><p>Department of Economics &amp; Business, Colorado College, Palmer Hall 114-C, 14 E. Cache la Poudre St., Colorado Springs, CO 80903. <a href='mailto:{EMAIL}'>{EMAIL}</a> · +1 (719) 389-6416</p>",
         f"<p class='meta'><a href='{BASE}/cv/'>CV</a> · <a href='{SCHOLAR}'>Google Scholar</a> · <a href='{REPEC}'>RePEc</a> · <a href='{GITHUB}'>GitHub</a> · <a href='{GLO}'>GLO</a> · <a href='{BASE}/more/'>Media, resources and other things</a></p>"]
    return "", page("Guanyi Yang — Economist, Colorado College", "\n".join(b), "Guanyi Yang is an economist at Colorado College working on heterogeneous-agent macroeconomics, labor and education, and the economics of dark skies and light pollution.", "", ld)

def cv_page():
    b = ["<h1>Curriculum Vitae</h1>",
         f"<p><a href='{BASE}/pdf/Guanyi-Yang-CV.pdf'>Download the CV (PDF)</a>. Summary below; the PDF is the complete record.</p>",
         "<h2>Positions</h2><ul><li>Gerald L. Schlessman Assistant Professor, Department of Economics &amp; Business, Colorado College, since September 2022 (Assistant Professor from August 2021)</li><li>Assistant Professor of Economics, St. Lawrence University, 2018–2021</li><li>Visiting scholar: Georgia State University (Andrew Young School), summer 2019; Renmin University of China, December 2018</li></ul>",
         "<h2>Affiliations</h2><ul><li>Research Fellow, Global Labor Organization (GLO), since 2022</li><li>Project Director, State of the Rockies, Colorado College, since 2023</li></ul>",
         "<h2>Education</h2><ul><li>Ph.D. Economics, The Ohio State University, 2018. Dissertation: Essays on Labor Market Frictions and Macroeconomic Welfare</li><li>M.A. Economics, The Ohio State University, 2014</li><li>B.A. Mathematics and Economics, Ohio Wesleyan University, 2013 (magna cum laude)</li></ul>",
         "<h2>Fields</h2><p>Macroeconomics; labor economics; inequality; heterogeneous-agent models; environmental valuation; economics of education.</p>",
         "<h2>Selected awards and grants</h2><ul><li>Andrew Carnegie Fellows Program, Colorado College’s sole pretenure nominee; final round of national selection, 2025–2026</li><li>Sidney G. Winter Award for excellence in teaching and research in Business and Economics, Colorado College, 2025</li><li>Dean of the Faculty Teaching Excellence Award, Colorado College, 2024</li><li>Jackson Fellowships, Hulbert Center for Southwest Studies, 2023 and 2024</li><li>Faculty-Student Collaborative Research Grant, Colorado College, 2022–2026</li><li>Guangdong Province Philosophy and Social Science Planning Project (Co-PI), 2026</li><li>Elsevier Best Paper Award, 10th International Symposium on Human Capital and Labor Markets, 2018</li></ul>",
         f"<p><a href='{BASE}/research/'>Publications and working papers</a></p>"]
    return "cv/", page("CV — Guanyi Yang", "\n".join(b), "Curriculum vitae of Guanyi Yang, economist at Colorado College.", "cv/")

def more_page():
    b = ["<h1>More</h1>",
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
         "<h2>Outside work</h2><ul><li><a href='https://youtu.be/9T2lSy2hMWo?si=rJOLzE-ZE4Rb1gpE'>Colorado College Concert Band</a> (most recent concert)</li><li><a href='https://www.dropbox.com/sh/cs2gbctzlf430k4/AACbmx7k854AGeuIMGX_6Msva?dl=0'>Photography</a></li></ul>"]
    return "more/", page("More — Guanyi Yang", "\n".join(b), "Media coverage, consulting, resources for students, and other things.", "more/")

def root_llms():
    L = ["# Guanyi Yang — research", "", "> Economist at Colorado College. Heterogeneous-agent macroeconomics, labor and education, environmental valuation (dark skies), emerging-market business cycles, children and schooling in rural China. Each paper below has a page with the abstract, main numbers, scope limits and all public versions, plus a plain-text llms.txt.", "", "## Papers", ""]
    for p in sorted(pd.PAPERS, key=lambda p:-p["year"]):
        L.append(f"- [{p['title']}]({BASE}/papers/{p['slug']}/): {p['one_liner']} ({p['venue']}, {p['year']}). Summary: {BASE}/papers/{p['slug']}/llms.txt")
    L += ["", "## Themes", ""] + [f"- [{v['title']}]({BASE}/themes/{k}/)" for k,v in pd.THEMES.items()]
    L += ["", "## Profiles", "", f"- Google Scholar: {SCHOLAR}", f"- RePEc: {REPEC}", f"- GitHub: {GITHUB}", f"- CV: {BASE}/cv/", ""]
    return "\n".join(L)

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT/".nojekyll").write_text("")
    (OUT/"style.css").write_text(CSS)
    pages = []
    for p in pd.PAPERS:
        path, h = paper_page(p); d = OUT/path; d.mkdir(parents=True, exist_ok=True)
        (d/"index.html").write_text(h, encoding="utf-8"); (d/"llms.txt").write_text(llms_txt(p), encoding="utf-8"); pages.append(path)
    for k,v in pd.THEMES.items():
        path, h = theme_page(k,v); d = OUT/path; d.mkdir(parents=True, exist_ok=True); (d/"index.html").write_text(h, encoding="utf-8"); pages.append(path)
    for fn in (research_page, home_page, cv_page, more_page):
        path, h = fn(); d = OUT/path if path else OUT; d.mkdir(parents=True, exist_ok=True); (d/"index.html").write_text(h, encoding="utf-8"); pages.append(path)
    (OUT/"llms.txt").write_text(root_llms(), encoding="utf-8")
    (OUT/"robots.txt").write_text("User-agent: *\nAllow: /\n\nUser-agent: GPTBot\nAllow: /\nUser-agent: ChatGPT-User\nAllow: /\nUser-agent: OAI-SearchBot\nAllow: /\nUser-agent: ClaudeBot\nAllow: /\nUser-agent: anthropic-ai\nAllow: /\nUser-agent: PerplexityBot\nAllow: /\nUser-agent: Google-Extended\nAllow: /\nUser-agent: CCBot\nAllow: /\nUser-agent: Applebot-Extended\nAllow: /\n\nSitemap: " + BASE + "/sitemap.xml\n")
    urls = "".join(f"<url><loc>{BASE}/{p}</loc><lastmod>{TODAY}</lastmod></url>" for p in pages) + "".join(f"<url><loc>{BASE}/papers/{p['slug']}/llms.txt</loc><lastmod>{TODAY}</lastmod></url>" for p in pd.PAPERS)
    (OUT/"sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')
    # PDFs
    (OUT/"pdf").mkdir(exist_ok=True)
    for src_url, newname in PDF_MAP.items():
        src = WP_SRC / src_url.rsplit("/",1)[1]
        if src.exists(): shutil.copy2(src, OUT/"pdf"/newname)
        else: print("WARN missing", src)
    cv = pathlib.Path("/tmp/claude-0/-home-claude/87876bce-ade7-545d-96d6-27fe0d1359a3/scratchpad/repos/CV/CV.pdf")
    if cv.exists(): shutil.copy2(cv, OUT/"pdf"/"Guanyi-Yang-CV.pdf")
    print("built", len(pages), "pages +", len(pd.PAPERS), "llms.txt files into", OUT)

if __name__ == "__main__":
    main()
