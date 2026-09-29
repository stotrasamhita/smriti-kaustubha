# Source files

Raw inputs. Nothing in this folder is edited by hand. Corrections go into the structured text under
`content/`, never into these files.

## `ocr/smriti-kaustubha-1931.ocr.txt`

Plain-text OCR of the 1931 Nirṇaya Sāgara Press edition (second edition, ed. W. L. S. Pansīkar),
from the President's Secretariat Library copy.

| | |
|---|---|
| Encoding | UTF-8, LF line endings |
| Size | 25,936 lines, about 3 MB |
| SHA-256 | `fbfb319f3b1c5279582b5dc2e31c8d13cbfef9718d2e3deee5ef4550f6c16387` |
| Page markers | `### 001.json` … `### 620.json`, one per scan page (620 in all) |
| OCR engine | not recorded |

### Scan page → printed page

| Part | Scan pages | Printed pages |
|---|---|---|
| Library slip, title pages, imprint | 001–007 | – |
| प्रास्ताविकम् | 008–011 | 5–8 |
| विषयानुक्रमः (multi-column; badly scrambled by the OCR) | 012–019 | 9–16 |
| तिथिदीधितिः | 020–101 | 1–82 |
| संवत्सरदीधितिः | 102–597 | 83–580 |
| आशौचदीधितिः | 598–613 | 581–596 |
| काशीस्थपुस्तकशुद्धपाठान्तराणि | 614–617 | – |
| Blank pages, library slip | 618–620 | – |

The offset between scan page and printed page is not constant (about −19 early in the Saṃvatsara-dīdhiti,
about −17 later), because of plates and blank pages. Always take the printed page number from the running head.

### Known problems

See [`../docs/ocr-errors.md`](../docs/ocr-errors.md). In short:

- Running heads and page numbers are mixed into the text.
- Conjuncts are often broken or merged, and the avagraha is often lost.
- Scan pages 460–461 and 478–491 (kuṇḍa geometry and numeric tables), printed p.283 and p.552 are too
  garbled to proof-read from this text alone.
- Figures (kuṇḍa and maṇḍapa diagrams) are not in the text at all.

## Still needed

- Page images at 400 dpi or better (archive.org / Digital Library of India). Record the identifier and checksums
  here when added. Large images go outside Git (archive.org item or Git LFS).
