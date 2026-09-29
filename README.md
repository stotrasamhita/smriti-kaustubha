# स्मृतिकौस्तुभः · Smṛti-kaustubhaḥ

A digital edition of the **Smṛti-kaustubha** of Anantadeva (son of Āpadeva), the 17th-century
dharmaśāstra digest (*nibandha*) on tithi-nirṇaya and the observances of the year, month by month.
Part of the [StotraSamhita](https://github.com/stotrasamhita) family of Sanskrit-text projects.

> 🚧 **Work in progress.** The repository holds the raw OCR text and the project spec. The structured text,
> the website and the PDF are being built. See [`docs/spec.md`](docs/spec.md).

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
| संवत्सरदीधितिः | 83–580 | OCR only |
| आशौचदीधितिः | 581–596 | OCR only |
| काशीस्थपुस्तकशुद्धपाठान्तराणि (variant readings) | appendix | OCR only |

## Repository layout

| Path | Contents |
|---|---|
| [`docs/spec.md`](docs/spec.md) | Project spec: text model, pipeline, website, PDF, indices, phases |
| [`docs/ocr-errors.md`](docs/ocr-errors.md) | Recurring OCR errors and known page-specific corrections |
| [`source/`](source/) | Raw inputs, never edited by hand (see [`source/README.md`](source/README.md)) |
| `content/` | *(Phase 0)* The structured master text, one Markdown file per topic |
| `data/` | *(Phase 0)* Authority lists: cited sources, festivals, glossary, page concordance |
| `pdf/` | *(Phase 0)* Pandoc filter and LuaLaTeX class for the PDF |
| `tools/` | *(Phase 1)* OCR, cleanup, tagging and validation scripts |

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
