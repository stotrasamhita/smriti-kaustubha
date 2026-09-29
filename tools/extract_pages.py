#!/usr/bin/env python3
"""Extract scan pages from the raw OCR dump into a draft for hand cleanup.

Mechanical steps only (spec §5.3): split on `### NNN.json`, pull out running heads, printed page
numbers, signature marks and the edition's own footnotes, then rejoin lines hyphenated across a
line break. Nothing is corrected here. The draft is a starting point for a human (or Claude) to
turn into `content/` files; it is never published as is.

    python3 tools/extract_pages.py 104 127 > draft.md
"""
import re
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent / "source/ocr/smriti-kaustubha-1931.ocr.txt"
DEV_DIGITS = str.maketrans("०१२३४५६७८९", "0123456789")
NUM = r"[०-९]+"

LEFT_HEAD = re.compile(rf"^(?:({NUM})\s*)?स्मृतिकौस्तुभे-संवत्सरदीधितौ-\s*$")
RIGHT_HEAD = re.compile(r"^\[[^\]]+\]\s*(.*)$")
# Short lines at the top of a page: a topic title on its own line, or a margin note.
SHORT = re.compile(r"^\S+(?:\s\S+)?\s?[।.]?$")
PAGE_NO = re.compile(rf"^({NUM})$")
SIGNATURE = re.compile(r"^(?:[०-९१.]+\s*)?स्मृ[.०]?\s*कौ[०.]?\s*$|^कौ०$")
FOOTNOTE = re.compile(rf"^{NUM}\s?[.']?\s*\S")


# Scan → printed offset where the running head carries no legible number (checked on neighbours).
OFFSETS = {s: 19 for s in range(104, 137)}  # checked on scan 104–136 (pp.85–117)


def pages(text):
    for m in re.finditer(r"^### (\d{3})\.json\n(.*?)(?=^### |\Z)", text, re.S | re.M):
        yield int(m.group(1)), [l.strip() for l in m.group(2).splitlines() if l.strip() not in ("", "###")]


def split_page(lines):
    head, printed, body, notes = [], None, list(lines), []
    # Running head, page number and margin notes sit in the first three lines.
    for _ in range(4):
        if not body:
            break
        l = body[0]
        if m := LEFT_HEAD.match(l):
            head.append("स्मृतिकौस्तुभे-संवत्सरदीधितौ-")
            printed = printed or (m.group(1) and int(m.group(1).translate(DEV_DIGITS)))
        elif m := RIGHT_HEAD.match(l):
            head.append(l)
        elif m := PAGE_NO.match(l):
            printed = int(m.group(1).translate(DEV_DIGITS))
        elif SHORT.match(l):
            head.append(f"?{l}")  # topic title or margin note: check against the image
        else:
            break
        body.pop(0)
    # Footnotes and signature marks sit at the bottom.
    while body and (SIGNATURE.match(body[-1]) or FOOTNOTE.match(body[-1])):
        l = body.pop()
        if not SIGNATURE.match(l):
            notes.insert(0, l)
    return head, printed, body, notes


def join(lines):
    """Rejoin lines. A trailing '-' is kept as a marker `‹-›` because it is either a hyphen
    (drop it) or the dash that introduces a quotation (keep it); a human decides."""
    out = ""
    for l in lines:
        if out.endswith("-"):
            out = out[:-1] + "‹-›" + l
        elif out.endswith("."):  # OCR reads a hyphen as '.' at some line ends
            out = out[:-1] + "‹.›" + l
        else:
            out = (out + " " + l) if out else l
    return out


def main(first, last):
    text = SRC.read_text(encoding="utf-8")
    for scan, lines in pages(text):
        if not first <= scan <= last:
            continue
        head, printed, body, notes = split_page(lines)
        if printed is None and scan in OFFSETS:
            printed = scan - OFFSETS[scan]
        print(f"<!-- scan {scan:03d} | printed {printed or '?'} | head: {' / '.join(head) or '–'} -->")
        print(f"{{{{< pg {printed or '?'} >}}}}")
        print(join(body))
        for n in notes:
            print(f"<!-- footnote: {n} -->")
        print()


if __name__ == "__main__":
    main(int(sys.argv[1]), int(sys.argv[2]))
