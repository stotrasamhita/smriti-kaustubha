# Phase 0 pilot report: Caitra-kṛtyam (printed pp.85–108)

Status on 2026-09-29. The pilot's gate (spec §9) is "pilot site and PDF approved; text model frozen". This report
says what is ready for that review and what is still missing.

## Deliverables

| Phase 0 item (spec §9) | State |
|---|---|
| Repo skeleton | Done: `content/`, `data/`, `pdf/`, `tools/`, Hugo site, CI |
| pp.85–108 as structured text | Done at status `cleaned`: 10 topic files, all 24 page markers |
| Proof-read twice | **Not started.** Needs the page images (spec §2); checklist ready in `docs/proofreading/` |
| Site with script menu | Done: hugo-book, the 12 scripts of spec §6 via Sanscript, Pagefind search in any script, copy citation |
| 24-page PDF with indices | Done: 23 B5 pages, apparatus, margin page numbers, 4 of the 7 indices |

## What is in the text

| | Count |
|---|---|
| Topic files (one per 1931 running head) | 10 |
| Paragraphs with stable IDs / set verses | 44 / 10 |
| Quotations tagged (`q`) / with a named source | 122 / 91 |
| Cited works in `data/sources.toml` | 38 |
| OCR corrections tagged (`corr`) | 259 |
| Doubtful readings `[?]` for a human | 43 |
| 1931 footnotes (`fn`) / margin side-headings (`mn`) | 29 / 9 |

Every correction keeps the OCR reading (`{{< corr ocr="…" >}}`), shows on the web as a highlight with the OCR
reading on hover, and in the PDF as an apparatus note "lemma ] OCR reading". Corrections were made from context,
grammar and metre only; none has been checked against the page image yet.

The topics follow the 1931 running heads: चान्द्रमासनिर्णयः, कल्पादिनिर्णयः, प्रपादाननिर्णयः, रामदोलोत्सवनिर्णयः,
स्कन्दपूजानिर्णयः, रामनवमीनिर्णयः, श्रीकृष्णदोलोत्सवः, दमनकोत्सवः, नृसिंहदोलोत्सवः, वारुणीयोगः.

## Decisions taken in the pilot (now in spec §4)

- Paragraph IDs are explicit `{#p87.3}` lines, checked by `tools/validate.py`, not computed at build time.
- Two shortcodes added: `fn` (the 1931 edition's own footnotes) and `mn` (its margin side-headings).
- Only verses the 1931 edition sets apart are `shloka` blocks; quoted verses printed as prose are `q` only.
- `tithis` numbered 1–30 through the amānta month.

## For the reviewers

- Site: built by CI and published to GitHub Pages once this is merged to `main` (Pages source must be set to
  "GitHub Actions" in the repository settings). Locally: `make site && hugo server`.
- PDF: CI artifact `sk-caitra-pilot-pdf`, and `/pdf/sk-caitra-pilot.pdf` on the site.
- Please check in particular: the half-verse layout, the apparatus density (about 11 notes per page), margin
  page numbers, and whether the side-headings belong in the margin on the web.

## Still missing before the gate

1. **Page images** at 400 dpi for scan 104–127, then proof-reading pass 1 and pass 2 (different readers) using
   `docs/proofreading/caitra-krtyam.md`. Status moves `cleaned → proofread-1 → proofread-2`.
2. Indices not yet built: subject index and glossary (need `ix` tags and `data/glossary.toml`); the verse-pāda
   index covers set verses only (see the run-in verse question in spec §9).
3. PDF polish: Tiro Devanagari Sanskrit could not be installed in the build environment, so the PDF falls back
   to Noto Serif Devanagari; line-numbered apparatus, ICU collation, PDF/X and PDF/A profiles.
4. `adyatithi` IDs in the front matter (left empty rather than guessed).
5. The open questions in spec §9, including the new ones on run-in verses and apparatus keying.
