#!/usr/bin/env python3
"""Check the built academic site for missing research and inconsistent citations.

Usage: python3 _src/check_site.py [output_dir] [base_url] [--strict-pdf-size]

Uses only the standard library and performs no network requests. The source
bibliographic records are the authority for titles, authors, dates and abstracts;
the generated HTML, citation downloads and files are inspected independently of
the builder. This does not certify external links, indexing, or PDF scientific
content. Inline/HTML visibility is checked, not a browser's complete CSS cascade.
"""

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass, field
import hashlib
from html.parser import HTMLParser
import importlib.util
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urljoin, urlsplit
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DEFAULT_BASE = "https://yangguanyi.github.io"
PDF_LIMIT = 5_000_000

# Established public URLs must survive a redesign, even when summaries change.
LEGACY_SLUGS = {
    "dark-skies-great-sand-dunes",
    "racial-disparities-hiring-discrimination",
    "intermittent-college-enrollment",
    "informality-unemployment-small-open-economies",
    "sibling-spillovers-rural-china",
    "left-behind-children-parental-migration-wealth",
    "global-financial-risk-equity-returns-emerging-markets",
    "social-norms-information-green-fee",
    "temporary-employment-us-welfare",
    "schooling-disutility",
    "college-major-chinese-immigrants",
}
# Original publicly linked draft bytes, recorded before the redesign. A new
# version belongs at a new primary PDF URL; do not silently replace an old draft.
PRESERVED_FILES = {
    "pdf/Bansak-Jiang-Yang-2022-Sibling-Spillovers-Rural-China-WP.pdf": "5b4e2cb5758376d1959ffce26e4a41e8300fc5734e0b4b858aba48b9993b48cd",
    "pdf/Eiswerth-Mullen-Yang-2026-Dark-Skies-Valuation-Great-Sand-Dunes-WP.pdf": "c494cb4dc6e84fc5a54312b39adc2ffc53fa34f27bfe8bb3e77b54193d5c6959",
    "pdf/Horvath-Yang-2023-Global-Financial-Risk-Equity-Returns-Emerging-Countries-WP.pdf": "52cf11054eef7aaa7b4f05ae320748037936e223b7b53a39ddcc50010a3d0909",
    "pdf/Murali-Yang-2025-Macroeconomics-of-Racial-Disparities.pdf": "d5df7e4b680c1ee80eae7eedef056ad647a43a9c2893059525b11d2366a43836",
    "pdf/Yang-2025-Better-Late-Than-Never-Intermittent-College-Enrollment-WP.pdf": "6eadc535a102f4c88adced20faa075cf081fc193b3846a462d7c5af89ef380ab",
    "googlee658f0ecd415ab22.html": "d6f340d7a7ea1e2c4d83e69ee21ab3f88a1515f99268636d1c5e94ead4023e83",
    "e3e0886cabc87b7ab0a4bd024ff2937f.txt": "2775dd37b8d6d9ee5a124573781b3e96bdd75bdd648472e0cb533a32a183a7d0",
}
VERIFICATION_HTML = {name for name in PRESERVED_FILES if name.endswith(".html")}
VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
HIDDEN_TAGS = {"head", "script", "style", "template"}
BLOCK_TAGS = {"p", "div", "section", "article", "main", "li", "h1", "h2", "h3", "h4", "dt", "dd", "br", "header", "footer", "nav", "pre"}


def norm(value):
    """Only normalize whitespace; preserve wording and punctuation in abstracts."""
    return " ".join(str(value).split())


def doi_norm(value):
    return re.sub(r"^(?:https?://(?:dx\.)?doi\.org/|doi:\s*)", "", str(value), flags=re.I).strip().lower()


def author_norm(value):
    value = norm(value)
    if "," in value:
        family, given = value.split(",", 1)
        value = norm(given + " " + family)
    return value


def year_of(value):
    match = re.match(r"^(\d{4})(?:$|[-/])", str(value))
    return match.group(1) if match else None


@dataclass
class Node:
    tag: str
    attrs: dict = field(default_factory=dict)
    parent: object = None
    children: list = field(default_factory=list)

    def has_class(self, name):
        return name in self.attrs.get("class", "").split()

    def concealed(self):
        current = self
        while current is not None:
            if current.tag in HIDDEN_TAGS or "hidden" in current.attrs:
                return True
            if current.attrs.get("aria-hidden", "").lower() == "true":
                return True
            style = current.attrs.get("style", "")
            if re.search(r"(?:^|;)\s*(?:display\s*:\s*none|visibility\s*:\s*hidden|opacity\s*:\s*0(?:\.0*)?(?:\s|;|$))", style, re.I):
                return True
            if current.parent and current.parent.tag == "details" and "open" not in current.parent.attrs and current.tag != "summary":
                return True
            current = current.parent
        return False

    def text(self, visible=False):
        if visible and self.concealed():
            return ""
        parts = []
        for child in self.children:
            if isinstance(child, str):
                parts.append(child)
            else:
                text = child.text(visible)
                parts.append(" " + text + " " if child.tag in BLOCK_TAGS else text)
        return "".join(parts)

    def walk(self):
        yield self
        for child in self.children:
            if isinstance(child, Node):
                yield from child.walk()


class Document(HTMLParser):
    def __init__(self, raw):
        super().__init__(convert_charrefs=True)
        self.root = Node("document")
        self.stack = [self.root]
        self.feed(raw)
        self.close()
        self.nodes = list(self.root.walk())[1:]
        self.meta = defaultdict(list)
        for node in self.nodes:
            if node.tag == "meta":
                name = node.attrs.get("name", "").lower()
                if name:
                    self.meta[name].append(node.attrs.get("content", ""))
        self.ids = Counter(node.attrs["id"] for node in self.nodes if "id" in node.attrs)
        self.anchor_names = {node.attrs["name"] for node in self.nodes if node.tag == "a" and "name" in node.attrs}

    def handle_starttag(self, tag, attrs):
        node = Node(tag, dict(attrs), self.stack[-1])
        self.stack[-1].children.append(node)
        if tag not in VOID_TAGS:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID_TAGS:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == tag:
                del self.stack[index:]
                break

    def handle_data(self, data):
        self.stack[-1].children.append(data)

    def find(self, tag=None, cls=None):
        return [node for node in self.nodes if (tag is None or node.tag == tag) and (cls is None or node.has_class(cls))]

    def canonicals(self):
        return [node.attrs.get("href", "") for node in self.find("link") if "canonical" in node.attrs.get("rel", "").lower().split()]


def typed_objects(value):
    """Walk JSON-LD graphs without assuming a particular serialization layout."""
    if isinstance(value, dict):
        if "@type" in value:
            yield value
        for child in value.values():
            yield from typed_objects(child)
    elif isinstance(value, list):
        for child in value:
            yield from typed_objects(child)


def has_type(obj, name):
    value = obj.get("@type", [])
    return name in (value if isinstance(value, list) else [value])


def bib_fields(text):
    """Read one BibTeX entry, respecting nested braces and escaped characters."""
    entry = re.search(r"@([A-Za-z]+)\s*\{\s*([^,{}]+),", text)
    if not entry or len(re.findall(r"(?m)^\s*@", text)) != 1:
        raise ValueError("expected one BibTeX record")
    fields = {}
    pos = entry.end()
    while pos < len(text):
        skip = re.match(r"[\s,]*", text[pos:])
        pos += skip.end()
        if pos == len(text) or text[pos] == "}":
            break
        key = re.match(r"([A-Za-z][A-Za-z0-9_-]*)\s*=\s*", text[pos:])
        if not key:
            raise ValueError("invalid BibTeX field near " + repr(text[pos:pos + 35]))
        name = key.group(1).lower()
        pos += key.end()
        if pos >= len(text):
            raise ValueError("missing BibTeX value")
        opener = text[pos]
        if opener in '{"':
            closer = "}" if opener == "{" else '"'
            start = pos + 1
            pos = start
            depth = 1
            while pos < len(text) and depth:
                if text[pos] == "\\":
                    pos += 2
                    continue
                if opener == "{" and text[pos] == "{":
                    depth += 1
                elif text[pos] == closer:
                    depth -= 1
                if depth:
                    pos += 1
            if depth:
                raise ValueError("unclosed BibTeX value")
            value = text[start:pos]
            pos += 1
        else:
            match = re.match(r"[^,}\n]+", text[pos:])
            if not match:
                raise ValueError("invalid bare BibTeX value")
            value = match.group(0).strip()
            pos += match.end()
        if name in fields:
            raise ValueError("duplicate BibTeX field " + name)
        value = value.replace(r"\textbackslash{}", "\\")
        value = re.sub(r"\\([&%_#$])", r"\1", value)
        fields[name] = value.replace("{", "").replace("}", "")
    return fields


def ris_fields(text):
    fields = defaultdict(list)
    last = None
    for line in text.splitlines():
        match = re.match(r"^([A-Z0-9]{2})  - ?(.*)$", line)
        if match:
            last = match.group(1)
            fields[last].append(match.group(2))
        elif line.strip() and last:
            fields[last][-1] += " " + line.strip()
        elif line.strip():
            raise ValueError("invalid RIS line")
    if len(fields["TY"]) != 1 or len(fields["ER"]) != 1:
        raise ValueError("expected one complete RIS record")
    return fields


class Audit:
    def __init__(self, output, base, data, strict_size=False):
        self.output = output.resolve()
        self.base = base.rstrip("/")
        self.origin = urlsplit(self.base)
        self.prefix = self.origin.path.rstrip("/") + "/"
        self.data = data
        self.strict_size = strict_size
        self.errors = []
        self.warnings = []
        self.docs = {}
        self.entities = {}
        self.checked_links = set()
        self.paper_checks = 0
        self.pdf_checks = set()
        # A repository may contain a separate preview build. It is not published
        # with the root checkout. When that build is the requested output_dir,
        # inspect its contents normally instead of excluding the target itself.
        self.repository_only_dirs = {"dist", ".git", ".openai", "__pycache__"} if self.output == ROOT.resolve() else set()

    def published_file(self, path):
        parts = path.relative_to(self.output).parts
        return bool(parts) and parts[0] not in self.repository_only_dirs and not any(part.startswith((".", "_")) for part in parts)

    def error(self, where, message):
        self.errors.append(f"{where}: {message}")

    def warning(self, where, message):
        self.warnings.append(f"{where}: {message}")

    def check(self, condition, where, message):
        if not condition:
            self.error(where, message)
        return bool(condition)

    def same(self, actual, expected, where, label):
        return self.check(norm(actual) == norm(expected), where, f"{label} differs: expected {str(expected)!r}, found {str(actual)!r}")

    def absolute(self, relative=""):
        return self.base + "/" + str(relative).lstrip("/")

    def url_for_file(self, relative):
        relative = str(relative).replace("\\", "/")
        return self.absolute(relative[:-10] if relative.endswith("index.html") else relative)

    def load(self, relative):
        relative = Path(relative).as_posix()
        if relative in self.docs:
            return self.docs[relative]
        path = self.output / relative
        if not path.is_file():
            self.error(relative, "missing HTML page")
            return None
        try:
            self.docs[relative] = Document(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, ValueError) as exc:
            self.error(relative, "cannot parse HTML: " + str(exc))
            return None
        return self.docs[relative]

    def local_target(self, ref, from_file):
        """Return (local path, fragment) for same-site URLs; None for external."""
        if not ref or ref.startswith(("mailto:", "tel:", "data:", "javascript:")):
            return None
        parsed = urlsplit(urljoin(self.url_for_file(from_file), ref))
        if parsed.scheme not in {"http", "https"} or parsed.netloc.lower() != self.origin.netloc.lower():
            return None
        path = unquote(parsed.path)
        if not path.startswith(self.prefix):
            self.error(from_file, "same-host link leaves the configured site path: " + ref)
            return None
        relative = Path(path[len(self.prefix):])
        candidate = (self.output / relative).resolve()
        if not candidate.is_relative_to(self.output):
            self.error(from_file, "link escapes output directory: " + ref)
            return None
        if path.endswith("/") or candidate.is_dir():
            candidate /= "index.html"
        return candidate, unquote(parsed.fragment)

    def link(self, ref, from_file):
        key = (str(from_file), ref)
        if key in self.checked_links:
            return
        self.checked_links.add(key)
        target = self.local_target(ref, from_file)
        if target is None:
            return
        path, fragment = target
        if not self.check(path.is_file(), from_file, "broken internal reference: " + ref):
            return
        if fragment and path.suffix.lower() == ".html":
            # Browser text fragments do not require an element ID.
            fragment = fragment.split(":~:text=", 1)[0]
            if fragment:
                relative = path.relative_to(self.output).as_posix()
                doc = self.load(relative)
                if doc:
                    self.check(fragment in doc.ids or fragment in doc.anchor_names, from_file, "missing fragment target: " + ref)

    def pdf(self, relative, primary=False):
        path = self.output / relative
        if not self.check(path.is_file(), relative, "missing PDF"):
            return
        if relative not in self.pdf_checks:
            self.pdf_checks.add(relative)
            with path.open("rb") as handle:
                self.check(handle.read(5) == b"%PDF-", relative, "file does not start with a PDF header")
        if primary and path.stat().st_size >= PDF_LIMIT:
            message = f"primary PDF is {path.stat().st_size:,} bytes; target is below {PDF_LIMIT:,} for scholarly indexing"
            (self.error if self.strict_size else self.warning)(relative, message)

    def general_html(self, relative, doc):
        canonical = self.url_for_file(relative)
        self.check(len(doc.canonicals()) == 1, relative, "expected exactly one canonical link")
        if doc.canonicals():
            self.same(doc.canonicals()[0], canonical, relative, "canonical URL")
        titles = doc.find("title")
        self.check(len(titles) == 1 and bool(norm(titles[0].text())), relative, "missing or duplicate HTML title")
        self.check(any(norm(node.text(True)) for node in doc.find("h1")), relative, "missing visible main heading")
        for value, count in doc.ids.items():
            self.check(count == 1, relative, "duplicate HTML id: " + value)
        objects = []
        for node in doc.find("script"):
            if node.attrs.get("type", "").lower() == "application/ld+json":
                try:
                    objects.extend(typed_objects(json.loads(node.text())))
                except (ValueError, TypeError) as exc:
                    self.error(relative, "invalid JSON-LD: " + str(exc))
        self.entities[relative] = objects
        self.check(bool(objects), relative, "missing parseable JSON-LD")
        for node in doc.nodes:
            for attr in ("href", "src", "poster"):
                if node.attrs.get(attr):
                    self.link(node.attrs[attr], relative)
            if node.attrs.get("srcset") and not node.attrs["srcset"].startswith("data:"):
                for entry in node.attrs["srcset"].split(","):
                    if entry.strip():
                        self.link(entry.strip().split()[0], relative)
        for node in doc.find("meta"):
            if node.attrs.get("name", "").lower() == "robots":
                self.check("noindex" not in node.attrs.get("content", "").lower(), relative, "canonical content is marked noindex")

    def citation_exports(self, paper, folder):
        label = paper["slug"]
        expected_authors = [author_norm(name) for name, _ in paper["authors"]]
        for filename in ("citation.bib", "citation.ris"):
            path = self.output / folder / filename
            if not self.check(path.is_file(), label, "missing citation download: " + filename):
                continue
            try:
                raw = path.read_text(encoding="utf-8")
                fields = bib_fields(raw) if filename.endswith("bib") else ris_fields(raw)
            except (OSError, UnicodeError, ValueError) as exc:
                self.error(label, filename + " cannot be read: " + str(exc))
                continue
            if filename.endswith("bib"):
                self.same(fields.get("title", ""), paper["title"], label, "BibTeX title")
                names = [author_norm(value) for value in re.split(r"\s+and\s+", fields.get("author", ""))]
                self.check(names == expected_authors, label, "BibTeX authors differ from the source record")
                self.same(fields.get("year", ""), paper["year"], label, "BibTeX year")
                self.same(fields.get("url", ""), self.absolute(folder + "/"), label, "BibTeX URL")
                self.same(doi_norm(fields.get("doi", "")), doi_norm(paper.get("doi") or ""), label, "BibTeX DOI")
            else:
                self.same(" ".join(fields.get("TI", fields.get("T1", []))), paper["title"], label, "RIS title")
                self.check([author_norm(value) for value in fields.get("AU", fields.get("A1", []))] == expected_authors, label, "RIS authors differ from the source record")
                dates = fields.get("PY", fields.get("Y1", []))
                self.check(len(dates) == 1 and year_of(dates[0]) == str(paper["year"]), label, "RIS year differs from the source record")
                self.same(" ".join(fields.get("UR", [])), self.absolute(folder + "/"), label, "RIS URL")
                self.same(doi_norm(" ".join(fields.get("DO", []))), doi_norm(paper.get("doi") or ""), label, "RIS DOI")
                self.same(" ".join(fields.get("AB", [])), paper["abstract"], label, "RIS abstract")
                if paper.get("pdf_path"):
                    self.same(" ".join(fields.get("L1", [])), self.absolute(paper["pdf_path"]), label, "RIS PDF URL")

    def paper(self, paper):
        slug = paper["slug"]
        folder = "papers/" + slug
        relative = folder + "/index.html"
        canonical = self.absolute(folder + "/")
        doc = self.docs.get(relative)
        if doc is None:
            return
        self.paper_checks += 1
        titles = doc.find("title")
        if titles:
            self.check(norm(paper["title"]) in norm(titles[0].text()), slug, "HTML title omits the paper's full title")
        self.check(any(norm(node.text(True)) == norm(paper["title"]) for node in doc.find("h1")), slug, "paper title is not a visible h1")
        abstracts = doc.find(cls="abstract")
        self.check(len(abstracts) == 1, slug, "expected one original abstract in the page body")
        if abstracts:
            self.same(abstracts[0].text(True), paper["abstract"], slug, "visible abstract")
        self.check(bool(norm(paper.get("abstract", ""))), slug, "source abstract is empty")
        self.check(doc.meta.get("citation_title") == [paper["title"]], slug, "citation_title is missing, duplicated, or differs from the record")
        authors = [name for name, _ in paper["authors"]]
        self.check(doc.meta.get("citation_author") == authors, slug, "expected one citation_author per author, in bibliographic order")
        dates = doc.meta.get("citation_publication_date", [])
        self.check(len(dates) == 1 and year_of(dates[0]) == str(paper["year"]), slug, "citation publication year differs from bibliographic year")
        if dates and paper.get("publication_date"):
            # Highwire supports a full known date or a year. Do not invent a day
            # merely because a journal record identifies its issue month.
            source_date = str(paper["publication_date"])
            expected_date = source_date if re.fullmatch(r"\d{4}-\d{2}-\d{2}", source_date) else str(paper["year"])
            actual_parts = dates[0].replace("/", "-").split("-")
            expected_parts = expected_date.split("-")
            self.check(all(part.isdigit() for part in actual_parts) and [int(part) for part in actual_parts] == [int(part) for part in expected_parts], slug, "citation publication date must be the known full date or the bibliographic year")
        self.check(doc.meta.get("citation_abstract_html_url") == [canonical], slug, "abstract HTML URL does not match the canonical paper page")
        if paper.get("doi"):
            self.check([doi_norm(value) for value in doc.meta.get("citation_doi", [])] == [doi_norm(paper["doi"])], slug, "citation DOI differs from the record")
        elif doc.meta.get("citation_doi"):
            self.error(slug, "unexpected DOI in citation metadata")
        if paper["kind"] == "article":
            self.check(doc.meta.get("citation_journal_title") == [paper["venue"]], slug, "citation journal differs from the record")
        pdfs = doc.meta.get("citation_pdf_url", [])
        self.check(len(pdfs) == 1, slug, "expected one citation_pdf_url for the full paper")
        self.check(bool(paper.get("pdf_path")), slug, "source record lacks primary pdf_path")
        if pdfs:
            parsed = urlsplit(pdfs[0])
            self.check(parsed.scheme in {"http", "https"} and bool(parsed.netloc), slug, "citation_pdf_url must be absolute")
            self.check(pdfs[0].rsplit("/", 1)[0] + "/" == canonical, slug, "primary PDF must be in the paper page's own subdirectory")
            self.link(pdfs[0], relative)
            if paper.get("pdf_path"):
                self.same(pdfs[0], self.absolute(paper["pdf_path"]), slug, "citation PDF URL")
                self.pdf(paper["pdf_path"], primary=True)
            self.check(any(node.attrs.get("href") == pdfs[0] and norm(node.text(True)) for node in doc.find("a")), slug, "primary PDF lacks a visible download link")
        entities = [obj for obj in self.entities.get(relative, []) if has_type(obj, "ScholarlyArticle") or has_type(obj, "Report")]
        self.check(len(entities) == 1, slug, "expected exactly one scholarly JSON-LD entity")
        if entities:
            entity = entities[0]
            self.same(entity.get("name", ""), paper["title"], slug, "JSON-LD title")
            self.same(entity.get("url", ""), canonical, slug, "JSON-LD URL")
            self.same(entity.get("abstract", ""), paper["abstract"], slug, "JSON-LD abstract")
            self.check(year_of(entity.get("datePublished", "")) == str(paper["year"]), slug, "JSON-LD publication year differs from bibliographic year")
            if paper.get("publication_date"):
                self.same(entity.get("datePublished", ""), paper["publication_date"], slug, "JSON-LD publication date")
            names = entity.get("author", [])
            if isinstance(names, dict):
                names = [names]
            self.check([item.get("name") if isinstance(item, dict) else item for item in names] == authors, slug, "JSON-LD authors differ from the record")
            identifiers = entity.get("identifier", [])
            if not isinstance(identifiers, list):
                identifiers = [identifiers]
            dois = [doi_norm(item.get("value", "")) for item in identifiers if isinstance(item, dict) and str(item.get("propertyID", "")).lower() == "doi"]
            expected_dois = [doi_norm(paper["doi"])] if paper.get("doi") else []
            self.check(dois == expected_dois, slug, "JSON-LD DOI differs from the record")
            media = entity.get("encoding", [])
            if isinstance(media, dict):
                media = [media]
            media_pdfs = [item.get("contentUrl") for item in media if isinstance(item, dict) and item.get("encodingFormat") == "application/pdf"]
            self.check(media_pdfs == pdfs, slug, "JSON-LD PDF differs from citation PDF")
        self.citation_exports(paper, folder)
        note = self.output / folder / "llms.txt"
        if self.check(note.is_file(), slug, "missing plain-text research note"):
            self.check(norm(paper["abstract"]) in norm(note.read_text(encoding="utf-8")), slug, "plain-text note omits or changes the original abstract")

    def progress(self):
        items = self.data.IN_PROGRESS
        self.check(len(items) == 4, "research in progress", f"expected all four supplied projects, found {len(items)}")
        research = self.docs.get("research/index.html")
        if not research:
            return
        sections = [node for node in research.nodes if node.attrs.get("id") == "in-progress"]
        self.check(len(sections) == 1, "research/index.html", "missing or duplicate in-progress section")
        rows = [node for section in sections for node in section.walk() if node.tag == "li" and node.has_class("paper-row")]
        self.check(len(rows) == len(items), "research/index.html", "in-progress row count differs from source records")
        for item in items:
            title = item["title"]
            found = [row for row in rows if any(node.tag in {"h2", "h3"} and norm(node.text(True)) == norm(title) for node in row.walk())]
            self.check(len(found) == 1, title, "project title is missing or duplicated in research in progress")
            for forbidden in ("abstract", "pdf_path", "pdf_url", "doi", "arxiv", "findings"):
                self.check(not item.get(forbidden), title, "unavailable draft has unexpected " + forbidden)
            for row in found:
                self.check(not any(node.has_class("abstract") or node.has_class("paper-summary") for node in row.walk()), title, "unavailable draft has an abstract or summary block")
                # A classless paragraph must not slip an invented result into a
                # title-only project listing. Every visible word should come
                # from the supplied title, coauthors, status, or listing label.
                names = item.get("coauthors", "")
                names = ", ".join(str(name) for name in names) if isinstance(names, list) else str(names)
                remaining = norm(row.text(True))
                allowed = [title, names, item.get("status", "Draft forthcoming"), "In progress", "With"]
                for phrase in sorted((norm(value) for value in allowed if value), key=len, reverse=True):
                    remaining = remaining.replace(phrase, " ")
                self.check(not remaining.strip(" \t\r\n,;:."), title, "project listing contains text beyond the supplied title, coauthors and status")
                for node in row.walk():
                    link = node.attrs.get("href", "")
                    self.check(not re.search(r"\.(?:pdf|bib|ris)(?:[?#]|$)", link, re.I), title, "unavailable draft has a paper/citation download")
            if item.get("slug"):
                self.check(not (self.output / "papers" / item["slug"] / "index.html").exists(), title, "unavailable draft unexpectedly has a standalone paper page")
            for relative, doc in self.docs.items():
                self.check(title not in doc.meta.get("citation_title", []), relative, "unavailable draft has citation metadata: " + title)
                for entity in self.entities.get(relative, []):
                    if has_type(entity, "ScholarlyArticle") or has_type(entity, "Report"):
                        self.check(norm(entity.get("name", "")) != norm(title), relative, "unavailable draft has a scholarly JSON-LD record: " + title)

    def sitemap(self, expected_urls):
        path = self.output / "sitemap.xml"
        if not self.check(path.is_file(), "sitemap.xml", "missing sitemap"):
            return
        try:
            tree = ET.parse(path)
        except (OSError, ET.ParseError) as exc:
            self.error("sitemap.xml", "invalid XML: " + str(exc))
            return
        namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        locs = [element.text or "" for element in tree.findall("sm:url/sm:loc", namespace)]
        self.check(len(locs) == len(set(locs)), "sitemap.xml", "duplicate URLs")
        for missing in sorted(expected_urls - set(locs)):
            self.error("sitemap.xml", "missing canonical HTML page: " + missing)
        for extra in sorted(set(locs) - expected_urls):
            self.error("sitemap.xml", "noncanonical, non-HTML, or unexpected entry: " + extra)
        for entry in tree.findall("sm:url", namespace):
            modified = entry.find("sm:lastmod", namespace)
            if modified is not None:
                self.check(bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", modified.text or "")), "sitemap.xml", "lastmod must be a date, not an invented timestamp")

    def run(self):
        papers = self.data.PAPERS
        slugs = [paper["slug"] for paper in papers]
        self.check(len(slugs) == len(set(slugs)), "papers_data", "duplicate paper slugs")
        for slug in sorted(LEGACY_SLUGS - set(slugs)):
            self.error("papers_data", "established paper record disappeared: " + slug)
        expected_paths = {"index.html", "research/index.html", "cv/index.html", "more/index.html"}
        expected_paths.update("papers/" + slug + "/index.html" for slug in slugs)
        expected_paths.update("themes/" + key + "/index.html" for key in self.data.THEMES)
        discovered_paths = {
            path.relative_to(self.output).as_posix()
            for path in self.output.rglob("*.html")
            if self.published_file(path)
        } - VERIFICATION_HTML
        for relative in sorted(expected_paths | discovered_paths):
            doc = self.load(relative)
            if doc:
                self.general_html(relative, doc)
        canonicals = Counter(value for doc in self.docs.values() for value in doc.canonicals())
        for value, count in canonicals.items():
            self.check(count == 1, "canonical URLs", "duplicate canonical: " + value)
        for relative in sorted(discovered_paths - expected_paths):
            self.error(relative, "unexpected HTML page outside current bibliography/navigation")
        for paper in papers:
            self.paper(paper)
        research = self.docs.get("research/index.html")
        if research:
            text = norm(research.root.text(True))
            for paper in papers:
                self.check(norm(paper["title"]) in text, "research/index.html", "missing visible paper title: " + paper["title"])
                self.check(any(node.attrs.get("href") == self.absolute("papers/" + paper["slug"] + "/") for node in research.find("a")), "research/index.html", "missing paper-detail link: " + paper["slug"])
        for relative, doc in self.docs.items():
            if not relative.startswith("papers/"):
                self.check(not any(name.startswith("citation_") for name in doc.meta), relative, "collection/non-paper page has article citation metadata")
        self.progress()
        self.sitemap({self.url_for_file(relative) for relative in expected_paths})
        for relative, digest in PRESERVED_FILES.items():
            path = self.output / relative
            if self.check(path.is_file(), relative, "established public file is missing"):
                self.check(hashlib.sha256(path.read_bytes()).hexdigest() == digest, relative, "established draft/verification file was altered")
                if relative.endswith(".pdf"):
                    self.pdf(relative)
        # A CV can legitimately change, while its established download URL must work.
        self.pdf("pdf/Guanyi-Yang-CV.pdf")
        for path in self.output.rglob("*.css"):
            if not self.published_file(path):
                continue
            relative = path.relative_to(self.output).as_posix()
            for match in re.finditer(r"url\(\s*['\"]?([^)'\"]+)['\"]?\s*\)", path.read_text(encoding="utf-8")):
                self.link(match.group(1).strip(), relative)
        for message in self.errors:
            print("ERROR: " + message)
        for message in self.warnings:
            print("WARNING: " + message)
        print(f"Checked {len(self.docs)} HTML pages, {self.paper_checks} paper records, {len(self.pdf_checks)} PDFs, and {len(self.checked_links)} link references.")
        print(f"Result: {len(self.errors)} errors, {len(self.warnings)} warnings. External links and search-engine inclusion were not tested.")
        return 1 if self.errors else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_dir", nargs="?", default=str(ROOT))
    parser.add_argument("base_url", nargs="?", default=DEFAULT_BASE)
    parser.add_argument("--strict-pdf-size", action="store_true", help="treat a primary PDF at or above 5,000,000 bytes as an error")
    args = parser.parse_args()
    parsed = urlsplit(args.base_url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc or parsed.query or parsed.fragment:
        parser.error("base_url must be an absolute HTTP(S) URL without query or fragment")
    output = Path(args.output_dir)
    if not output.is_dir():
        parser.error("output_dir does not exist")
    # Do not leave Python cache files in the source checkout during validation.
    sys.dont_write_bytecode = True
    try:
        spec = importlib.util.spec_from_file_location("papers_data", HERE / "papers_data.py")
        data = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(data)
    except (OSError, SyntaxError, ValueError) as exc:
        print("ERROR: cannot load bibliographic records: " + str(exc))
        return 1
    return Audit(output, args.base_url, data, args.strict_pdf_size).run()


if __name__ == "__main__":
    raise SystemExit(main())
