# Notes for Claude sessions

Project: digital edition of the Smṛti-kaustubha (NSP 1931). Read `docs/spec.md` before changing structure.

## Conventions

- `source/` is raw input. Never edit files there; corrections go into `content/`.
- Page numbers: say "p.NNN" for **printed** pages and "scan NNN" for the `### NNN.json` markers in
  `source/ocr/`. They differ by a drifting offset; read the printed number from the running head.
- Master text: Devanāgarī Markdown, one file per topic, TOML front matter, shortcodes as in spec §4.
  Stable IDs are tied to printed pages (`#p87.3`, `#p87.v2`); never renumber after release.
- Never apply an OCR substitution blindly (see `docs/ocr-errors.md`); mark doubtful readings `[?]` for a
  human to check against the page image.
- Transliteration must use the `indic_transliteration` (sanscript) scheme tables so site and PDF agree.

## Current phase

Phase 0 pilot: Caitra-kṛtyam, printed pp.85–108 (scan 104–127), extended at the maintainer's request to the
Vaiśākha-kṛtyam, pp.108–117 (scan 127–136), for circulation. Do not process further sections until the
circulated site and PDF have been reviewed.

Pilot state (see `docs/pilot-report.md`): both sections are in `content/samvatsara/` at status `cleaned`
(machine cleanup + tagging, no proof-reading against images). Site, PDF and indices build. Next: page images,
then proof-reading passes 1 and 2 from `docs/proofreading/<section>.md`.

The PDF has two modes: the default reading copy hides corrections and `[?]` (they stay in the `.tex` and in
`build/pdf/<name>-corrections.tsv`); `--draft` prints the OCR apparatus. Circulate the reading copy.

## Commands

- `python3 tools/validate.py` before every commit (CI runs it). `--fix-sources` rewrites front-matter `sources`.
- `make generated` after editing content: regenerates `data/pages.toml` and the proof-reading checklist (CI diffs them).
- `make pdf` (reading and draft copies), `make site` (needs Hugo ≥ 0.158 extended, pandoc, LuaLaTeX; see `pdf/README.md`).
- `python3 tools/extract_pages.py 104 127` prints a mechanical draft of scan pages as a starting point.
