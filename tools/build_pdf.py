#!/usr/bin/env python3
"""Build the print PDF from content/ (spec §7).

    content/*.md ──(this script: shortcodes → Pandoc spans/divs)──▶ build/pdf/text.md
                 ──(pandoc + pdf/sk.lua + pdf/sk.latex)──────────▶ build/pdf/<name>.tex
                 ──(lualatex ×2)─────────────────────────────────▶ build/pdf/<name>.pdf

The indices (spec §8) are computed here from the same tags, with 1931 page numbers, and appended
as LaTeX. Nothing in build/ is edited by hand.

    python3 tools/build_pdf.py [--section caitra-krtyam,vaisakha-krtyam] [--name sk-caitra-pilot] [--tex-only]
    python3 tools/build_pdf.py --draft              # proof copy: OCR apparatus and [?] marks printed
    python3 tools/build_pdf.py --script iast        # optional IAST edition

By default the PDF is a clean reading copy: corrected text only, no apparatus, no [?] marks. Every
correction and doubtful reading is still in the .tex (as the macro arguments \skcorr{ours}{ocr} and
\skdoubt) and is listed in build/pdf/<name>-corrections.tsv.
"""
import argparse
import re
import shutil
import subprocess
import sys
import tomllib
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate import ATTR, ROOT, content_files, split_front_matter  # noqa: E402

BUILD = ROOT / "build/pdf"
PDF = ROOT / "pdf"
SITE = "https://stotrasamhita.github.io/smriti-kaustubham"
TITHI = ["प्रतिपत्", "द्वितीया", "तृतीया", "चतुर्थी", "पञ्चमी", "षष्ठी", "सप्तमी", "अष्टमी", "नवमी",
         "दशमी", "एकादशी", "द्वादशी", "त्रयोदशी", "चतुर्दशी"]
MONTHS = ["चैत्रः", "वैशाखः", "ज्येष्ठः", "आषाढः", "श्रावणः", "भाद्रपदः", "आश्विनः", "कार्तिकः",
          "मार्गशीर्षः", "पौषः", "माघः", "फाल्गुनः"]


def tithi_name(t):
    """Tithis are numbered 1–30 through the amānta month: 1–15 śukla, 16–29 kṛṣṇa, 30 amāvāsyā."""
    if t == 15:
        return "शुक्ल पूर्णिमा"
    if t == 30:
        return "कृष्ण अमावास्या"
    return ("शुक्ल " if t < 15 else "कृष्ण ") + TITHI[(t - 1) % 15]


def dev_key(s):
    """Devanāgarī sort key: code-point order with anusvāra/visarga sorted before the consonants.
    Good enough for the pilot; the full edition uses ICU collation (upmendex), spec §8."""
    return s.replace("ं", "ऀ").replace("ः", "ँ")


def md_attr(v):
    return v.replace("\\", "\\\\").replace('"', '\\"')


def convert(body):
    """Hugo shortcodes → Pandoc Markdown. Returns the converted text."""
    out, carry = [], ""
    for block in re.split(r"\n\s*\n", body.strip()):
        lines = [l for l in block.split("\n") if l.strip()]
        if not lines:
            continue
        if re.fullmatch(r"\{\{<\s*pg\s+\d+\s*>\}\}", block.strip()):
            carry += block.strip()  # a page marker on its own: attach it to the next block
            continue
        if carry:
            if lines[0].startswith("{{< shloka"):
                out.append(inline(carry))
            else:
                lines[0] = carry + lines[0]
            carry = ""
        if lines[0].startswith("{{< shloka"):
            vid = dict(ATTR.findall(lines[0])).get("id", "")
            verse = [inline(l.strip()) for l in lines[1:-1]]
            out.append(f"::: {{.shloka #{vid}}}\n" + "\n".join(f"| {v}" for v in verse) + "\n:::")
            continue
        pid = None
        if m := re.fullmatch(r"\{#(p\d+\.\d+)\}", lines[-1].strip()):
            pid, lines = m.group(1), lines[:-1]
        text = inline(" ".join(l.strip() for l in lines))
        out.append(f"::: {{.para #{pid}}}\n{text}\n:::" if pid else text)
    return "\n\n".join(out)


def inline(s):
    s = s.replace("[?]", "\x01")
    s = s.replace("[", "\\[").replace("]", "\\]")  # literal brackets in the OCR text
    s = re.sub(r"\{\{<\s*pg\s+(\d+)\s*>\}\}", r"[\1]{.pg}", s)
    s = re.sub(r"\{\{<\s*fn\s*>\}\}", "^[", s)
    s = re.sub(r"\{\{<\s*/fn\s*>\}\}", "]", s)

    def open_tag(m):
        name, attrs = m.group(1), dict(ATTR.findall(m.group(2)))
        return "\x02" + name + "\x03" + "".join(f' {k}="{md_attr(v)}"' for k, v in attrs.items()) + "\x04"
    s = re.sub(r"\{\{<\s*(q|corr|em|var|mn)((?:\s+\w+=\"[^\"]*\")*)\s*>\}\}", open_tag, s)
    # Close each span with its class and attributes, which Pandoc wants after the brackets.
    stack, res, i = [], [], 0
    for m in re.finditer(r"\x02(\w+)\x03([^\x04]*)\x04|\{\{<\s*/(q|corr|em|var|mn)\s*>\}\}", s):
        res.append(s[i:m.start()])
        if m.group(1):
            stack.append((m.group(1), m.group(2)))
            res.append("[")
        else:
            name, attrs = stack.pop()
            assert name == m.group(3), (name, m.group(3))
            res.append(f"]{{.{name}{attrs}}}")
        i = m.end()
    res.append(s[i:])
    s = "".join(res)
    s = re.sub(r" +([।॥])", "\u00a0\\1", s)  # a daṇḍa never starts a line
    return s.replace("\x01", r"[\[?\]]{.doubt}")


def collect(files):
    """Walk the topics once, recording what the indices need, keyed by 1931 page."""
    idx = {"sources": defaultdict(set), "padas": [], "calendar": defaultdict(list), "pages": {}}
    sources = tomllib.loads((ROOT / "data/sources.toml").read_text(encoding="utf-8"))
    for f in files:
        fm, body, _ = split_front_matter(f.read_text(encoding="utf-8"), f)
        page = fm["pages"][0]
        for t in fm.get("tithis", []):
            idx["calendar"][(fm.get("month", 0), t)].append((fm["title"], fm["pages"]))
        for tok in re.finditer(r"\{\{<\s*pg\s+(\d+)\s*>\}\}|\{\{<\s*q((?:\s+\w+=\"[^\"]*\")*)\s*>\}\}|"
                               r"\{\{<\s*shloka[^>]*>\}\}\n(.*)", body):
            if tok.group(1):
                page = int(tok.group(1))
                idx["pages"].setdefault(page, (f, fm))
            elif tok.group(3) is not None:
                first = re.sub(r"\{\{<[^>]*>\}\}.*?\{\{<\s*/\w+\s*>\}\}|\{\{<[^>]*>\}\}|\[\?\]", "", tok.group(3))
                idx["padas"].append((first.split("।")[0].strip(), page))
            else:
                a = dict(ATTR.findall(tok.group(2)))
                for sid in ([a["src"]] if "src" in a else []) + a.get("via", "").split():
                    idx["sources"][sources[sid]["name"]].add(page)
    return idx


def corrections_log(files):
    """Every correction and [?] with its 1931 page, for the reading copy's side log."""
    tok = re.compile(r'\{\{<\s*pg\s+(\d+)\s*>\}\}|\{\{<\s*corr ocr="([^"]*)"\s*>\}\}(.*?)\{\{<\s*/corr\s*>\}\}(\s*\[\?\])?|\[\?\]')
    rows, page = ["page\ttopic\tocr\tprinted\tdoubtful"], None
    for f in files:
        fm, body, _ = split_front_matter(f.read_text(encoding="utf-8"), f)
        page = page or fm["pages"][0]
        for m in tok.finditer(body):
            if m.group(1):
                page = int(m.group(1))
            elif m.group(2) is not None:
                ours = re.sub(r"\{\{<[^>]*>\}\}", "", m.group(3))
                rows.append(f"{page}\t{fm['id']}\t{m.group(2)}\t{ours}\t{'yes' if m.group(4) else ''}")
            else:
                rows.append(f"{page}\t{fm['id']}\t\t\tyes")
    return "\n".join(rows) + "\n"


def indices_tex(idx, scan_of):
    L = [r"\skindices"]
    L += [r"\skindex{उद्धृतग्रन्थसूची}{Index of cited sources}", r"\begin{skindexlist}"]
    for name in sorted(idx["sources"], key=dev_key):
        L.append(rf"\item {name} \dotfill {', '.join(map(str, sorted(idx['sources'][name])))}")
    L += [r"\end{skindexlist}"]
    L += [r"\skindex{तिथिसूची}{Calendar index}", r"\begin{skindexlist}"]
    for (month, t) in sorted(idx["calendar"]):
        refs = "; ".join(f"{title} {a}–{b}" if a != b else f"{title} {a}" for title, (a, b) in idx["calendar"][(month, t)])
        L.append(rf"\item {MONTHS[month - 1]} {tithi_name(t)} \dotfill {refs}")
    L += [r"\end{skindexlist}"]
    L += [r"\skindex{श्लोकपादसूची}{Index of verse-pādas (set verses only)}", r"\begin{skindexlist}"]
    for pada, page in sorted(idx["padas"], key=lambda x: dev_key(x[0])):
        L.append(rf"\item {pada} \dotfill {page}")
    L += [r"\end{skindexlist}"]
    L += [r"\skindex{पृष्ठानुक्रमः}{Page concordance}", r"\begin{skconcordance}"]
    for page in sorted(idx["pages"]):
        f, fm = idx["pages"][page]
        slug = fm.get("slug") or f.stem
        url = f"{SITE}/{fm['didhiti']}/{fm['section']}/{slug}/#p{page}"
        L.append(rf"{page} & {scan_of(page)} & \href{{{url}}}{{\texttt{{{slug}\#p{page}}}}} \\")
    L += [r"\end{skconcordance}"]
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--section", default="caitra-krtyam", help="one section, or several separated by commas")
    ap.add_argument("--draft", action="store_true", help="print the OCR apparatus and [?] marks (proof copy)")
    ap.add_argument("--name", default="sk-caitra-pilot")
    ap.add_argument("--script", default="devanagari", help="devanagari (default) or iast")
    ap.add_argument("--tex-only", action="store_true")
    args = ap.parse_args()

    sections = args.section.split(",")
    files = [f for f in content_files() if f.parent.name in sections]
    missing = [s for s in sections if not any(f.parent.name == s for f in files)]
    if missing:
        sys.exit(f"no topics in section(s) {', '.join(missing)}")
    BUILD.mkdir(parents=True, exist_ok=True)

    index = {}
    for f in files:
        if f.parent not in index:
            index[f.parent] = tomllib.loads((f.parent / "_index.md").read_text(encoding="utf-8").split("+++")[1])
    heads = list(index.values())

    parts, seen = [], set()
    for f in files:
        if f.parent not in seen and len(heads) > 1:
            seen.add(f.parent)
            parts.append(f"```{{=latex}}\n\\sksection{{{index[f.parent]['title']}}}\n```")
        fm, body, _ = split_front_matter(f.read_text(encoding="utf-8"), f)
        slug = fm.get("slug") or f.stem
        url = f"{SITE}/{fm['didhiti']}/{fm['section']}/{slug}/"
        parts.append(f'# {fm["title"]} {{#{fm["id"]} url="{url}" status="{fm["status"]}"}}\n\n{convert(body)}')
    text = "\n\n".join(parts) + "\n"

    scans = {v["printed"]: v["scan"] for v in
             tomllib.loads((ROOT / "data/pages.toml").read_text(encoding="utf-8")).values()}
    tex_idx = indices_tex(collect(files), lambda p: scans.get(p, "–"))
    title = ", ".join(h["title"] for h in heads)
    pages = f"{heads[0]['pages'][0]}–{heads[-1]['pages'][1]}"

    if args.script != "devanagari":
        from indic_transliteration import sanscript
        protect = re.compile(r"(\{[^}]*\}|\\[a-zA-Z]+|https?://\S+)")
        def xl(s):
            return "".join(p if protect.fullmatch(p) else sanscript.transliterate(p, sanscript.DEVANAGARI, args.script)
                           for p in protect.split(s))
        text, tex_idx = xl(text), xl(tex_idx)

    (BUILD / "text.md").write_text(text, encoding="utf-8")
    (BUILD / "indices.tex").write_text(tex_idx, encoding="utf-8")
    (BUILD / f"{args.name}-corrections.tsv").write_text(corrections_log(files), encoding="utf-8")
    tex = BUILD / f"{args.name}.tex"
    subprocess.run(["pandoc", str(BUILD / "text.md"), "-f", "markdown-smart-auto_identifiers",
                    "--lua-filter", str(PDF / "sk.lua"), "--template", str(PDF / "sk.latex"),
                    "-V", f"section-title={title}", "-V", f"pages={pages}",
                    "-V", f"script={args.script}", *(["-V", "draft=true"] if args.draft else []), "--include-after-body", str(BUILD / "indices.tex"),
                    "-o", str(tex)], check=True)
    if args.tex_only:
        print(tex)
        return
    if not shutil.which("lualatex"):
        sys.exit("lualatex not found; install TeX Live (see pdf/README.md)")
    for _ in range(2):
        r = subprocess.run(["lualatex", "-interaction=nonstopmode", "-halt-on-error", tex.name],
                           cwd=BUILD, capture_output=True, text=True)
        if r.returncode:
            sys.exit(r.stdout[-3000:])
    print(BUILD / f"{args.name}.pdf")


if __name__ == "__main__":
    main()
