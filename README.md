# स्मृतिकौस्तुभः · Smṛti-kaustubhaḥ

A digital edition of the **Smṛti-kaustubha** of Anantadeva (son of Āpadeva), the 17th-century
dharmaśāstra digest (*nibandha*) on tithi-nirṇaya and the observances of the year, month by month.
Part of the [StotraSamhita](https://github.com/stotrasamhita) family of Sanskrit-text projects.

> 🚧 **Work in progress: Phase 0 pilot.** The Caitra- and Vaiśākha-kṛtyam (printed pp.85–117) are structured,
> tagged and published as a website and a PDF, **but not yet proof-read against the page images**. See
> [`docs/pilot-report.md`](docs/pilot-report.md) and [`docs/spec.md`](docs/spec.md).

## Goals

- **One proof-read master text** in structured Devanāgarī Markdown, with every edit to the 1931 text recorded.
- **A living website** (Hugo, in the style of [stotrasamhita.github.io](https://stotrasamhita.github.io)),
  readable in Devanāgarī, IAST and the other Indic scripts, with search and paragraph-level deep links.
- **A hi-fi PDF** with 1931 page numbers in the margin, a critical apparatus, and modern indices (calendar,
  subject, cited sources, verse-pādas, glossary).

Both outputs are generated from the same master text.

## Source edition

| | |
|---|---|
| Title | स्मृतिकौस्तुभः (तिथिदीधितिः, संवत्सरदीधितिः, आशौचदीधितिः) |
| Author | Anantadeva, son of Āpadeva |
| Editor | Vāsudeva Lakṣmaṇa Śāstrī Paṇaśīkara (Wāsudev Laxman S'āstrī Pansīkar) |
| Edition | Second edition, Nirṇaya Sāgara Press, Bombay, 1931 (Śaka 1852) |
| Copy scanned | President's Secretariat Library copy |
| Page images | *TODO:* archive.org / Digital Library of India identifier |

## Contents of the volume

| Part | Printed pages | Status |
|---|---|---|
| प्रास्ताविकम् (editor's introduction) and विषयानुक्रमः (topic list) | 5–16 | OCR only |
| तिथिदीधितिः | 1–82 | OCR only |
| संवत्सरदीधितिः | 83–580 | pp.85–117 (Caitra- and Vaiśākha-kṛtyam) cleaned and tagged; rest OCR only |
| आशौचदीधितिः | 581–596 | OCR only |
| काशीस्थपुस्तकशुद्धपाठान्तराणि (variant readings) | appendix | OCR only |

## Repository layout

| Path | Contents |
|---|---|
| [`docs/spec.md`](docs/spec.md) | Project spec: text model, pipeline, website, PDF, indices, phases |
| [`docs/ocr-errors.md`](docs/ocr-errors.md) | Recurring OCR errors and known page-specific corrections |
| [`source/`](source/) | Raw inputs, never edited by hand (see [`source/README.md`](source/README.md)) |
| `content/` | The structured master text, one Markdown file per topic (Caitra-kṛtyam so far) |
| `data/` | Authority lists: `sources.toml` (cited works), `pages.toml` (page concordance, generated) |
| `docs/proofreading/` | Generated checklists of every correction and doubtful reading, by printed page |
| `pdf/` | Pandoc Lua filter and LuaLaTeX template for the PDF ([`pdf/README.md`](pdf/README.md)) |
| `tools/` | Page extraction, validation, PDF build, page concordance and checklist scripts |
| `layouts/`, `static/`, `assets/`, `hugo.toml` | The Hugo site (theme: `themes/hugo-book`, a git submodule) |

## Building

```sh
git submodule update --init           # hugo-book theme
python3 tools/validate.py             # page markers, IDs, shortcodes, source IDs
make pdf                              # build/pdf/sk-caitra-vaisakha.pdf (+ -draft.pdf with OCR apparatus)
make site && hugo server              # site with Pagefind search (Hugo ≥ 0.158 extended)
```

CI (`.github/workflows/build.yml`) runs the same steps and publishes the site, with the PDF under `/pdf/`,
to GitHub Pages from `main`.

## Roadmap

0. **Pilot:** Caitra-kṛtyam (printed pp.85–108) all the way to a finished web page and PDF.
1. **Machine pass:** re-OCR, cleanup and structure tagging of the whole volume.
2. **Proof-reading pass 1**, Saṃvatsara-dīdhiti first.
3. **Proof-reading pass 2**, figures, tables, variant readings.
4. **Indices and release v1.0.**

## Contributing

Corrections are welcome. Open an issue or a pull request with the printed page number and the reading you
propose. Once the site is up, every topic page will have an edit link.

## Related

- [jyotisham/adyatithi](https://github.com/jyotisham/adyatithi): festival data that cites this text.
- [stotrasamhita.github.io](https://stotrasamhita.github.io): sister projects.
