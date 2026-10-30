# yangguanyi.github.io

Static research site for Guanyi Yang. One page per paper, with abstract, headline numbers, scope limits, related work (DOIs), all versions, JSON-LD, and a per-paper `llms.txt`.

## Rebuild
```
python3 _src/build_site.py . https://yangguanyi.github.io
```
Edit `_src/papers_data.py` to add or change a paper, then rebuild and commit. `_src/resolve_dois.py` looks up DOIs for related-work citations via Crossref (title-match checked).

Files: `papers/<slug>/index.html` + `llms.txt`; `themes/<slug>/`; `research/`; `cv/`; `more/`; `pdf/` (working papers, descriptive filenames); `llms.txt`, `sitemap.xml`, `robots.txt` at the root.
