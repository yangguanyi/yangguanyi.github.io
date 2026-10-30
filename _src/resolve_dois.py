#!/usr/bin/env python3
"""Resolve DOIs for related-work citations via Crossref; accept only when the returned title
matches the citation closely and the year is within 1 of the cited year. Writes dois.json."""
import json, re, time, urllib.parse, urllib.request, difflib, pathlib, importlib.util

spec = importlib.util.spec_from_file_location("pd", pathlib.Path(__file__).with_name("papers_data.py"))
pd = importlib.util.module_from_spec(spec); spec.loader.exec_module(pd)

def norm(t):
    t = t.lower().replace("’","'")
    t = re.sub(r"[^a-z0-9 ]+"," ",t)
    return re.sub(r"\s+"," ",t).strip()

def cite_parts(c):
    m = re.match(r"^(.*?)\((\d{4})\)\.\s*(.*?)(?:\.\s+[A-Z].*)?$", c)
    if not m: return None, None, c
    authors, year, rest = m.group(1), int(m.group(2)), m.group(3)
    title = rest.split(". ")[0] if ". " in rest else rest
    return authors, year, title

def lookup(c):
    authors, year, title = cite_parts(c)
    q = urllib.parse.quote(f"{title} {authors.split(',')[0] if authors else ''}")
    url = f"https://api.crossref.org/works?query.bibliographic={q}&rows=3&select=DOI,title,issued,container-title&mailto=guanyi.yang.l@gmail.com"
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            items = json.load(r)["message"]["items"]
    except Exception as e:
        return None, f"ERR {e}"
    best = None
    for it in items:
        t = it.get("title",[""])[0]
        ratio = difflib.SequenceMatcher(None, norm(title), norm(t)).ratio()
        y = (it.get("issued",{}).get("date-parts") or [[None]])[0][0]
        yok = (year is None) or (y is not None and abs(y-year) <= 1)
        if ratio >= 0.85 and yok and (best is None or ratio > best[0]):
            best = (ratio, it["DOI"], t, y, (it.get("container-title") or [""])[0])
    if best: return best[1], f"ok {best[0]:.2f} | {best[2][:70]} | {best[4][:30]} | {best[3]}"
    return None, "no confident match"

out = {}
cache = pathlib.Path("dois.json")
if cache.exists(): out = json.load(open(cache))
for p in pd.PAPERS:
    for cite, given in p["related"]:
        if given: out[cite] = given; continue
        if cite in out and out[cite]: continue
        doi, msg = lookup(cite)
        out[cite] = doi
        print(("FOUND " if doi else "MISS  ") + cite[:60], "->", doi, "|", msg)
        time.sleep(0.4)
json.dump(out, open(cache,"w"), indent=1, ensure_ascii=False)
print("resolved", sum(1 for v in out.values() if v), "of", len(out))
