# PDF toolchain

`tools/build_pdf.py` turns the Hugo shortcodes in `content/` into Pandoc spans and divs,
`sk.lua` maps those to LaTeX macros, `sk.latex` defines the macros and the page, and LuaLaTeX typesets.

```sh
python3 tools/build_pdf.py                         # build/pdf/sk-caitra-pilot.pdf
python3 tools/build_pdf.py --script iast --name sk-caitra-pilot-iast   # optional IAST edition
```

Needs: `pandoc` (3.x), TeX Live with LuaLaTeX (`texlive-luatex texlive-latex-recommended texlive-latex-extra`),
`fonts-noto-core`, and `pip install indic_transliteration` for the IAST edition.
Tiro Devanagari Sanskrit (OFL) is used when installed; otherwise Noto Serif Devanagari.

| Shortcode | Print |
|---|---|
| `pg` | grey bar at the break, 1931 page number in the outer margin |
| `shloka` | set apart, half-verses in pairs, second half indented |
| `q` | plain text; collected for the index of cited sources |
| `corr` | corrected text; apparatus series A gives "lemma ] OCR reading" |
| `em` | emended text; series A gives the 1931 reading |
| `var` | apparatus series B (Kāśī readings) |
| `fn` | ordinary numbered footnote: the 1931 edition's own notes |
| `mn` | margin note: the 1931 edition's side-headings |
| `[?]` | red superscript [?] |

The indices are computed by `build_pdf.py` from the same tags and keyed to 1931 page numbers:
cited sources, calendar (month/tithi from front matter), verse-pādas (set verses only) and the page
concordance. The subject index and glossary wait for `ix` tags and `data/glossary.toml`.

Not yet done: apparatus keyed to line numbers (needs reledmac or lineno), ICU collation (upmendex),
PDF/X and PDF/A-2u output profiles, ActualText spans. `pdftotext` already extracts correct Unicode
Devanāgarī from the HarfBuzz output (checked on the pilot).
