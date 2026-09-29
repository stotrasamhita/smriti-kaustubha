# PDF toolchain

`tools/build_pdf.py` turns the Hugo shortcodes in `content/` into Pandoc spans and divs,
`sk.lua` maps those to LaTeX macros, `sk.latex` defines the macros and the page, and LuaLaTeX typesets.

```sh
make pdf     # both copies below, for Caitra- and Vaiśākha-kṛtyam
python3 tools/build_pdf.py --section caitra-krtyam,vaisakha-krtyam --name sk-caitra-vaisakha          # reading copy
python3 tools/build_pdf.py --section caitra-krtyam,vaisakha-krtyam --name sk-caitra-vaisakha-draft --draft
python3 tools/build_pdf.py --script iast --name sk-iast   # optional IAST edition
```

**Two modes.** The default *reading copy* prints the corrected text only: no apparatus, no `[?]` marks. The
corrections are not lost: each stays in the `.tex` as `\skcorr{printed}{OCR reading}` (and each doubt as
`\skdoubt`), and all are listed in `build/pdf/<name>-corrections.tsv` (page, topic, OCR, printed, doubtful).
`--draft` gives the *proof copy*: the same text with apparatus series A ("lemma ] OCR reading") and red `[?]`.
The switch is the template variable `draft`, so the two copies always come from the same text.

Needs: `pandoc` (3.x), TeX Live with LuaLaTeX (`texlive-luatex texlive-latex-recommended texlive-latex-extra`),
`fonts-noto-core`, and `pip install indic_transliteration` for the IAST edition.
Tiro Devanagari Sanskrit (OFL) is used when installed; otherwise Noto Serif Devanagari.

| Shortcode | Print |
|---|---|
| `pg` | grey bar at the break, 1931 page number in the outer margin |
| `shloka` | set apart, half-verses in pairs, second half indented |
| `q` | plain text; collected for the index of cited sources |
| `corr` | corrected text; draft only: apparatus series A gives "lemma ] OCR reading" |
| `em` | emended text; draft only: series A gives the 1931 reading |
| `var` | apparatus series B (Kāśī readings) |
| `fn` | ordinary numbered footnote: the 1931 edition's own notes |
| `mn` | margin note: the 1931 edition's side-headings |
| `[?]` | draft only: red superscript [?] |

The indices are computed by `build_pdf.py` from the same tags and keyed to 1931 page numbers:
cited sources, calendar (month/tithi from front matter), verse-pādas (set verses only) and the page
concordance. The subject index and glossary wait for `ix` tags and `data/glossary.toml`.

Not yet done: apparatus keyed to line numbers (needs reledmac or lineno), ICU collation (upmendex),
PDF/X and PDF/A-2u output profiles, ActualText spans. `pdftotext` already extracts correct Unicode
Devanāgarī from the HarfBuzz output (checked on the pilot).
