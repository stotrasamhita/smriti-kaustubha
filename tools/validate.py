#!/usr/bin/env python3
"""Validate the master text in content/ (spec §4, §5 quality checks).

Fails (exit 1) on:
  - a printed page with no marker, two markers, or markers out of order;
  - a duplicate paragraph or verse ID, or an ID whose page is not the page it starts on,
    or IDs not numbered 1, 2, 3… within a page;
  - unbalanced or unknown shortcodes;
  - a quotation source ID missing from data/sources.toml;
  - missing or malformed front matter.
Warns on front-matter `sources` that disagree with the tags (fix with --fix-sources).
Reports counts of corrections, doubtful readings `[?]` and untagged quotations.

    python3 tools/validate.py [--fix-sources] [--first 85 --last 108]
"""
import argparse
import re
import sys
import tomllib
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
STATUSES = ["ocr", "cleaned", "proofread-1", "proofread-2", "final"]
REQUIRED = ["title", "id", "didhiti", "section", "pages", "scan_pages", "status", "sources"]
PAIRED = {"shloka", "q", "corr", "em", "var", "fn", "mn"}
SINGLE = {"pg", "fig", "ix"}

SHORTCODE = re.compile(r"\{\{<\s*(/?)(\w+)((?:\s+[^>]*?)?)\s*>\}\}")
ATTR = re.compile(r'(\w+)="([^"]*)"')
PARA_ID = re.compile(r"^\{#(p(\d+)\.(\d+))\}$")
VERSE_ID = re.compile(r"^p(\d+)\.v(\d+)$")


def split_front_matter(text, path):
    m = re.match(r"\A\+\+\+\n(.*?)\n\+\+\+\n", text, re.S)
    if not m:
        raise ValueError(f"{path}: no TOML front matter")
    return tomllib.loads(m.group(1)), text[m.end():], text[: m.end()].count("\n")


class Checker:
    def __init__(self, sources):
        self.sources = sources
        self.errors, self.warnings = [], []
        self.pages = []  # (page, file, line)
        self.ids = {}
        self.stats = Counter()
        # Reading state carries across files: a page and its paragraphs can span two topics.
        self.current_page = None
        self.para_seq, self.verse_seq = Counter(), Counter()

    def err(self, where, msg):
        self.errors.append(f"{where}: {msg}")

    def warn(self, where, msg):
        self.warnings.append(f"{where}: {msg}")

    def check_file(self, path, fix_sources=False):
        rel = path.relative_to(ROOT)
        text = path.read_text(encoding="utf-8")
        fm, body, offset = split_front_matter(text, rel)
        for k in REQUIRED:
            if k not in fm:
                self.err(rel, f"front matter lacks `{k}`")
        if fm.get("status") not in STATUSES:
            self.err(rel, f"status must be one of {STATUSES}")

        used, stack = set(), []
        current_page, para_seq, verse_seq = self.current_page, self.para_seq, self.verse_seq
        in_block, para_start_page = False, None
        for n, line in enumerate(body.split("\n"), start=offset + 1):
            where = f"{rel}:{n}"
            stripped = line.strip()
            if not stripped:
                in_block = False
                continue
            new_block = not in_block
            if new_block:
                in_block, para_start_page = True, current_page

            if m := PARA_ID.match(stripped):
                pid, page, k = m.group(1), int(m.group(2)), int(m.group(3))
                self.claim(pid, where)
                if page != para_start_page:
                    self.err(where, f"{pid} starts on p.{para_start_page}, not p.{page}")
                para_seq[page] += 1
                if k != para_seq[page]:
                    self.err(where, f"{pid}: expected p{page}.{para_seq[page]} (paragraphs are numbered in order)")
                continue

            for sm in SHORTCODE.finditer(line):
                closing, name, args = sm.group(1) == "/", sm.group(2), sm.group(3)
                attrs = dict(ATTR.findall(args))
                if name not in PAIRED | SINGLE:
                    self.err(where, f"unknown shortcode `{name}`")
                    continue
                if name == "pg":
                    pos = args.split()
                    if len(pos) != 1 or not pos[0].isdigit():
                        self.err(where, f"bad page marker `{sm.group(0)}`")
                        continue
                    current_page = int(pos[0])
                    self.pages.append((current_page, rel, n))
                    # A marker that opens a paragraph means the paragraph starts on the new page.
                    if new_block and not stripped[: stripped.find(sm.group(0))].strip():
                        para_start_page = current_page
                    continue
                if name in SINGLE:
                    continue
                if closing:
                    if not stack or stack[-1] != name:
                        self.err(where, f"`/{name}` closes {stack[-1] if stack else 'nothing'}")
                    else:
                        stack.pop()
                    continue
                stack.append(name)
                if name == "q":
                    self.stats["quotations"] += 1
                    ids = [attrs.get("src")] if attrs.get("src") else []
                    ids += attrs.get("via", "").split()
                    if not ids:
                        self.stats["quotations without source"] += 1
                    for sid in ids:
                        used.add(sid)
                        if sid not in self.sources:
                            self.err(where, f"source `{sid}` is not in data/sources.toml")
                elif name == "corr":
                    self.stats["corrections"] += 1
                    if "ocr" not in attrs:
                        self.err(where, 'corr needs ocr="…"')
                elif name == "shloka":
                    vid = attrs.get("id")
                    if not vid or not (vm := VERSE_ID.match(vid)):
                        self.err(where, f'shloka needs id="p<page>.v<n>", got {vid!r}')
                    else:
                        page, k = int(vm.group(1)), int(vm.group(2))
                        self.claim(vid, where)
                        if page != current_page:
                            self.err(where, f"{vid} is on p.{current_page}")
                        verse_seq[page] += 1
                        if k != verse_seq[page]:
                            self.err(where, f"{vid}: expected p{page}.v{verse_seq[page]}")
                        self.stats["verses"] += 1
                elif name == "fn":
                    self.stats["1931 footnotes"] += 1
            self.stats["doubtful [?]"] += line.count("[?]")
            # Latin letters are OCR debris; allowed only in the two words before a `[?]` flag.
            if re.search(r"[A-Za-z]", re.sub(r"\S+(?:\s\S+)?\s\[\?\]", "", SHORTCODE.sub("", line))):
                self.err(where, "Latin letters in the text (OCR debris?)")
        if stack:
            self.err(rel, f"unclosed shortcodes: {stack}")
        self.current_page = current_page

        self.check_paragraph_ids(rel, body, offset)
        declared = set(fm.get("sources", []))
        if declared != used:
            if fix_sources:
                order = sorted(used)
                new = re.sub(r"^sources = \[.*\]$", "sources = [" + ", ".join(f'"{s}"' for s in order) + "]",
                             text, count=1, flags=re.M)
                path.write_text(new, encoding="utf-8")
            else:
                self.warn(rel, f"front-matter sources differ from tags: missing {sorted(used - declared)}, "
                               f"unused {sorted(declared - used)}")
        pages = [p for p, f, _ in self.pages if f == rel]
        if pages and "pages" in fm:
            lo, hi = fm["pages"]
            if not (lo <= min(pages) and max(pages) <= hi):
                self.err(rel, f"page markers {min(pages)}–{max(pages)} fall outside pages = [{lo}, {hi}]")

    def check_paragraph_ids(self, rel, body, offset):
        """Every prose paragraph (not a verse block, not a bare marker) ends with an ID line."""
        blocks = re.split(r"\n\s*\n", body.strip())
        for b in blocks:
            lines = [l for l in b.strip().split("\n") if l.strip()]
            if not lines:
                continue
            if lines[0].startswith("{{< shloka") or re.fullmatch(r"\{\{< pg \d+ >\}\}", lines[0].strip()) and len(lines) == 1:
                continue
            if not PARA_ID.match(lines[-1].strip()):
                self.err(rel, f"paragraph without an ID: {lines[0][:60]}…")
            else:
                self.stats["paragraphs"] += 1

    def claim(self, anchor, where):
        if anchor in self.ids:
            self.err(where, f"duplicate ID {anchor} (first at {self.ids[anchor]})")
        self.ids[anchor] = where

    def check_pages(self, first, last):
        seen = [p for p, _, _ in self.pages]
        count = Counter(seen)
        for p in range(first, last + 1):
            if count[p] == 0:
                self.err("pages", f"p.{p} has no page marker")
            elif count[p] > 1:
                self.err("pages", f"p.{p} has {count[p]} page markers")
        for (a, fa, la), (b, fb, lb) in zip(self.pages, self.pages[1:]):
            if b != a + 1:
                self.err(f"{fb}:{lb}", f"page marker p.{b} follows p.{a}")


def weight_of(index_md):
    try:
        fm, _, _ = split_front_matter(index_md.read_text(encoding="utf-8"), index_md)
        return fm.get("weight", 0)
    except (OSError, ValueError):
        return 0


def content_files():
    """Topic files in reading order: dīdhiti, section and topic, each by its `weight`."""
    files = []
    for f in CONTENT.rglob("*.md"):
        # Topic files live at content/<dīdhiti>/<section>/<topic>.md; other pages (search, home) are not text.
        if f.name == "_index.md" or len(f.relative_to(CONTENT).parts) != 3:
            continue
        fm, _, _ = split_front_matter(f.read_text(encoding="utf-8"), f)
        key = (weight_of(f.parent.parent / "_index.md"), weight_of(f.parent / "_index.md"), fm.get("weight", 0), f.name)
        files.append((key, f))
    return [f for _, f in sorted(files)]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--fix-sources", action="store_true", help="rewrite front-matter sources from the tags")
    ap.add_argument("--first", type=int, help="first printed page that must be present (default: first marker)")
    ap.add_argument("--last", type=int, help="last printed page that must be present (default: last marker)")
    args = ap.parse_args()

    sources = tomllib.loads((ROOT / "data/sources.toml").read_text(encoding="utf-8"))
    c = Checker(sources)
    for f in content_files():
        c.check_file(f, args.fix_sources)
    seen = [p for p, _, _ in c.pages]
    args.first = args.first or min(seen)
    args.last = args.last or max(seen)
    c.check_pages(args.first, args.last)

    for w in c.warnings:
        print("warning:", w)
    for e in c.errors:
        print("error:", e)
    print("summary:", ", ".join(f"{k} {v}" for k, v in sorted(c.stats.items())),
          f"| pages {args.first}–{args.last}", f"| {len(c.errors)} errors, {len(c.warnings)} warnings")
    sys.exit(1 if c.errors else 0)


if __name__ == "__main__":
    main()
