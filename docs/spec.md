# Smṛti-Kaustubha Digital Edition: Spec

Status: draft, 2026-09-29. Open questions are listed in §9.

## 1. Goals and non-goals

Build one proof-read, structured master text of Anantadeva's Smṛti-Kaustubha (Nirṇaya Sāgara Press, 2nd ed.,
1931) and publish it two ways from that single source: a hi-fi print PDF with modern indices, and a living website
that renders in any Indic or Roman script.

**Goals**

- **Accurate text.** Every word proof-read against the page images, with OCR errors fixed and every editorial
  change recorded. Target: under 1 error per 2,000 akṣaras after two proof-reading passes.
- **Structure, not just text.** Dīdhiti → prakaraṇa → topic → paragraph/verse, with each quotation tagged by its
  source (Bhaviṣya, Hemādri, Mādhava…) and each verse marked as a verse.
- **Hi-fi PDF.** Devanāgarī typeset to a modern standard: running heads, 1931 page numbers in the margin, and the
  indices in §8.
- **Living website.** A Hugo site in the style of stotrasamhita.github.io: one page per topic, a script switcher,
  search, deep links to paragraph and verse level, and a "suggest a correction" link on every page.
- **Reuse.** Other projects can consume the text: adyatithi festivals link to the exact paragraph behind each rule,
  and the verse data can be exported as TEI/JSON.

**Non-goals (for now)**

- A critical edition collating manuscripts. We reproduce the 1931 text and record only the variant readings it
  prints itself.
- A full translation. Short English topic summaries are in scope later; running translation is optional.
- Other dīdhitis of the Kaustubha that are not in this volume.

**Who it serves:** practitioners and pañcāṅga makers who need the nirṇaya for a festival; students who want to read
the text in their own script; the jyotisha/adyatithi maintainers, who need stable citations.

## 2. Source material and current state

We start from one OCR text dump of about 3 MB, split into 620 scan pages (`### 001.json` … `### 620.json`).
It is readable but noisy, with no structure beyond page breaks. Details, page mapping and checksum:
[`source/README.md`](../source/README.md).

| Part | Scan pages | Printed pages | Contents |
|---|---|---|---|
| Front matter | 001–007 | – | Library slip, title, imprint |
| Prāstāvikam | 008–011 | 5–8 | Editor's Sanskrit introduction; notes on the kuṇḍa diagrams |
| Viṣayānukrama | 012–019 | 9–16 | Printed topic list for the whole volume (multi-column, scrambled by OCR) |
| Tithi-dīdhiti | 020–101 | 1–82 | General tithi-nirṇaya, ekādaśī, eclipses, dantadhāvana… |
| Saṃvatsara-dīdhiti | 102–597 | 83–580 | Month-by-month rites, adhika-māsa, saura/nākṣatra material |
| Āśauca-dīdhiti | 598–613 | 581–596 | Impurity rules |
| Pāṭhāntara | 614–617 | – | Corrected readings from a Kāśī manuscript, keyed by page and line |
| Back matter | 618–620 | – | Blank pages, library slip |

**Known OCR problems** ([`ocr-errors.md`](ocr-errors.md)):

- The printed/scan page offset drifts (−19 early, −17 later); read the page number from the running head.
- Recurring errors: conjuncts broken or merged (ष्ट/प्ट, द्ध/दध, स्न/स), avagraha dropped, स्न read as स/ल,
  ह्ण read as ले, repha lost; running heads and page numbers mixed into the text.
- Too garbled to proof-read from the OCR alone: p.283, scan 460–461 and 478–491 (kuṇḍa geometry, numeric
  tables), p.552, and the pāṭhāntara tables.
- The kuṇḍa and maṇḍapa figures are lost entirely.

**Still needed:** 400 dpi page images (record the scan's identifier and checksums), and ideally a second copy of
the 1931 printing to check damaged pages.

## 3. Architecture

There is exactly one thing people edit: a Git repo of structured Devanāgarī text. The website, the PDF and the
data exports are built from it by CI, so a fix made once shows up everywhere.

```
  Page images            OCR text (current)       Authority lists
  400 dpi + pages.toml   620 scan pages, noisy    sources, festivals, glossary
        │                       │                                          │
        └───────────────────────┼────────────────────────┘
                                ▼
  Digitization pipeline: re-OCR ×2, cleanup, verse / quotation / topic
  tagging, two proof-reading passes (each change a pull request)
                                │
                                ▼
  ┌──────────────────────────────────────────────────────────────────┐
  │ Canonical text: this repo, the only thing people edit            │
  │ Markdown per topic + TOML front matter + shortcodes; data/       │
  └──────────────────────────────────────────────────────────────────┘
        │                       │                                          │
        ▼                       ▼                        ▼
  Website (GitHub Pages)   Hi-fi PDF                 Data exports
  Hugo + hugo-book         Pandoc filter, LuaLaTeX   TEI XML, JSON
  12 scripts, Pagefind     apparatus, 7 indices      anchors for adyatithi

  Readers' corrections from the website come back as pull requests.
```

**Layout:** start with this single repo and folders (`content/`, `data/`, `pdf/`, `tools/`, `source/`). Page
images live outside Git (archive.org item or Git LFS). Split into more repos only if the PDF toolchain slows the
site build.

## 4. Canonical text model

The master text is Devanāgarī Markdown, one file per topic, with TOML front matter and a small fixed set of Hugo
shortcodes. Hugo reads it directly; the PDF and the TEI/JSON exports are generated from it, never edited by hand.
Markdown rather than TEI as the master, because proof-readers can edit it in GitHub's web editor and the site builds
from it unchanged. TEI stays an export.

| Unit | How it is marked | Stable ID | Example |
|---|---|---|---|
| Dīdhiti | Top-level folder | `sk.<d>` (`t`, `s`, `a`) | `sk.s` |
| Topic (prakaraṇa) | One `.md` file; heading = printed topic title | `sk.<d>.<slug>` | `sk.s.damanaka-utsavah` |
| Printed page | `{{< pg 87 >}}` at the exact break, even mid-sentence | `p87` | `#p87` |
| Paragraph | Blank line; numbered within its printed page | `p87.3` | `#p87.3` |
| Verse | `{{< shloka >}}` block, one line per half-verse, daṇḍa kept | `p87.v2` | `#p87.v2` |
| Quotation | `{{< q src="bhavishya" >}}…{{< /q >}}` | from its paragraph or verse | – |
| Correction | `{{< corr ocr="सात्वा" >}}स्नात्वा{{< /corr >}}`, a fix the scan supports | – | – |
| Emendation | `{{< em print="…" >}}…{{< /em >}}`, when the 1931 print itself is wrong | – | footnote |
| Variant | `{{< var src="kashi" >}}…{{< /var >}}` from the pāṭhāntara pages | – | footnote with page/line |
| Figure | `{{< fig "kunda-chaturasra" >}}`, redrawn as SVG | `fig.<slug>` | – |

IDs are tied to the printed page, so "SK p.87" and `…/damanaka-utsavah/#p87.3` point to the same place in print and
on the web. A validation script fails the build on a duplicate ID or a missing page marker.

Front matter per topic file:

```toml
title = "दमनकोत्सवः"
id = "sk.s.damanaka-utsavah"
didhiti = "samvatsara"
section = "caitra-krtyam"
pages = [86, 94]          # printed pages
scan_pages = [105, 113]   # json pages
month = 1                 # lunar month, amanta
tithis = [1, 2, 4, 7, 9, 12, 13, 14, 15]
adyatithi = ["sUryasya~damanakapUjA"]
sources = ["bhavishya", "hemadri", "nirnayamrta"]
status = "proofread-1"    # ocr | cleaned | proofread-1 | proofread-2 | final
```

Authority lists in `data/`:

- `sources.toml`: every cited work or author (about 250 expected) with a canonical ID, Devanāgarī name, OCR
  spellings seen, and a type (purāṇa, smṛti, nibandha, gṛhya-sūtra, jyotiṣa).
- `festivals.toml`: vrata/utsava names for the calendar index, mapped to adyatithi IDs.
- `pages.toml`: printed page ↔ scan page ↔ image file, generated from the page markers.
- `glossary.toml`: technical terms with IAST and a one-line English definition.

## 5. Digitization pipeline

Machines do the bulk of the work: two OCR engines, automatic fixes and structure tagging. People proof-read every
page twice against the image. Each topic file moves through `ocr → cleaned → proofread-1 → proofread-2 → final`,
and the site shows that status on every page.

1. **Acquire images.** 400 dpi, stored outside Git; build `pages.toml`.
2. **Re-OCR with two engines.** Google Cloud Vision plus a vision-LLM transcription as a second opinion. Keep word
   coordinates (hOCR) so each word traces back to the image. Words where the engines disagree are marked suspect.
3. **Automatic cleanup.**
    - Strip running heads and page numbers; insert `{{< pg N >}}` markers.
    - Apply the known-error table ([`ocr-errors.md`](ocr-errors.md)) only where the result is a known word.
    - Match quoted verses against existing corpora (GRETIL, sanskritdocuments.org, other nibandhas) and suggest
      readings; never apply them silently.
4. **Structure tagging.**
    - Topics: split on printed headings, checked against the viṣayānukrama (pp.9–16).
    - Verses: detect daṇḍa-closed lines, confirm with a metre checker; verses failing their metre are flagged.
    - Quotations: tag attribution patterns ("… इति भविष्ये", "हेमाद्रौ", "माधवः —") and map to `sources.toml`.
5. **Proof-reading, passes 1 and 2.** A proof-reading page shows the page image beside the editable text with
   suspect words highlighted. Saving opens a pull request. Pass 2 is done by a different person.
6. **Figures and tables.** Redraw kuṇḍa/maṇḍapa diagrams as SVG; re-key numeric tables by hand (scan 460–491).
7. **Freeze and tag v1.0.** The PDF and exports are built from the tag.

| Quality check (every commit) | Target for v1.0 |
|---|---|
| Every printed page 1–596 has exactly one page marker, in order | 100% |
| Verses passing their metre check, or with a recorded exception | 100% |
| Quotations tagged with a known source ID | ≥ 95% |
| Error rate, sampled on 20 random pages against the image | < 1 per 2,000 akṣaras |
| Suspect words left unresolved | 0 |
| Duplicate or broken IDs and links | 0 |

## 6. Website

A Hugo static site on GitHub Pages using the hugo-book theme, in the style of stotrasamhita.github.io. The text is
stored in Devanāgarī and transliterated in the browser, so one build serves every script.

**Navigation and pages**

- Left menu: dīdhiti → section (e.g. Caitra-kṛtyam) → topic, from the front matter; right-hand table of contents.
- One page per topic, with page markers as margin tags ("p.87"); clicking a tag opens that page's scan.
- Every paragraph and verse has a hover link (`#p87.3`) and a "copy citation" button.
- An "Edit / suggest a correction" link on every topic, opening GitHub's web editor.
- A proof-reading status badge at the top of each topic.

**Scripts**

- Header script menu, remembered per browser: Devanāgarī, IAST, ISO 15919, Kannada, Telugu, Tamil, Malayalam,
  Grantha, Bengali, Gujarati, Oḍia, Śāradā.
- Same scheme tables as the Python `indic_transliteration` (sanscript) package, so site and PDF agree.
- Tamil: Grantha-mixed by default, superscript numbers as an option (open question).
- Only Sanskrit content is transliterated; shortcode arguments and Latin text are not.
- Noto Serif web fonts per script, loaded only when that script is chosen.

**Search:** Pagefind (static index, built on Devanāgarī). Queries in any script or in IAST/Harvard-Kyoto are
converted to Devanāgarī first, so "damanaka", "दमनक" and "ದಮನಕ" find the same topic. Filters: dīdhiti, month,
cited source, festival.

**Browse-by pages:** by month and tithi (a 12 × 30 grid), by cited source, and by festival. Each adyatithi festival
links to the SK paragraphs behind it, and adyatithi's `references_primary` links back to the `#p87.3` anchor.

**Non-functional:** pages under 200 kB before fonts; optional offline support; URLs frozen at v1.0 (renames get a
Hugo alias); content licence per §9.

## 7. Hi-fi PDF

Typeset with LuaLaTeX from the same Markdown via a Pandoc filter that turns each shortcode into a LaTeX macro.
LuaLaTeX because HarfBuzz shapes Devanāgarī conjuncts correctly, reledmac handles the apparatus, and upmendex sorts
index entries in Devanāgarī order.

| Aspect | Decision |
|---|---|
| Page size | B5 (176 × 250 mm), one column; A4 variant from the same source |
| Devanāgarī font | Tiro Devanagari Sanskrit (OFL); fallback Siddhanta |
| Roman font | A serif with full IAST/ISO 15919 diacritics (e.g. Gentium or Noto Serif) |
| Verses | Set apart and indented as half-verse pairs, verse numbers in the margin |
| Quotations | Source name in bold (e.g. **भविष्ये**) |
| 1931 page numbers | Outer margin at the exact break ("\|87") |
| Running heads | Left: dīdhiti. Right: current topic |
| Apparatus | Series A: our corrections and emendations. Series B: Kāśī pāṭhāntara readings. Keyed to line numbers |
| Figures | Redrawn kuṇḍa/maṇḍapa SVGs as vector art |
| Navigation | Bookmarks for every topic; index entries and cross-references are live links; topic headings link to the web |
| Copy and paste | Must yield correct Unicode Devanāgarī (ActualText spans); tested in Acrobat, Chrome and pdftotext |
| Front matter | Title page, new English and Sanskrit introduction, conventions, sigla, modern contents, then the 1931 prāstāvikam |
| Outputs | Print PDF (PDF/X, crop marks) and screen PDF (PDF/A-2u); optional IAST edition |

Estimated size: about 700–750 B5 pages including indices, to be checked once the pilot is typeset.

## 8. Modernised indices

The 1931 edition has only a topic list in page order. The new edition adds seven indices, all built from tags in
the text so the PDF and website always match. PDF index page numbers are 1931 page numbers.

| # | Index | Ordered by | Built from | Use |
|---|---|---|---|---|
| 1 | Modern table of contents | Book order, three levels, English glosses | Headings + front matter | Find a topic without the scrambled viṣayānukrama |
| 2 | Calendar index | Lunar month → pakṣa → tithi, then solar months, weekdays, nakṣatras, yogas | `month`/`tithis` + `{{< ix >}}` tags | "What does SK say for Bhādrapada śukla 4?", with adyatithi IDs |
| 3 | Subject index | Devanāgarī, IAST beside each entry, sub-entries | `{{< ix "दमनकोत्सवः" >}}` tags, curated | Look up a rite, concept or object |
| 4 | Index of cited sources | Source, then page | `{{< q src=… >}}` tags | Every place Hemādri or the Bhaviṣya is quoted, with counts |
| 5 | Verse-pāda index | First pāda, Devanāgarī order (web: every pāda) | `{{< shloka >}}` blocks | Trace a half-remembered verse |
| 6 | Glossary | Devanāgarī, IAST, one-line English definition | `data/glossary.toml` | Understand pūrvaviddhā, vyāpti, pradoṣa, karaṇa… |
| 7 | Page concordance | 1931 page | `pages.toml` | Printed page → scan page → web URL; later Nirṇayasindhu/Dharmasindhu parallels |

Rules: headwords in the text's own Sanskrit form, with alternate names as "see" references (भ्रातृद्वितीया → see
यमद्वितीया); bold page numbers where the topic is decided, plain where only mentioned; ICU Devanāgarī collation via
upmendex for the PDF and the same order on the web; web indices are transliterated like any page but keep
Devanāgarī order.

## 9. Phases, effort and open questions

Start with a 24-page pilot on Caitra-kṛtyam (pp.85–108), taken all the way to a finished web page and PDF, before
processing the rest.

| Phase | Work | Gate |
|---|---|---|
| 0 · Pilot | Repo skeleton, pp.85–108 proof-read twice, site with script menu, 24-page PDF with indices | Pilot site and PDF approved; text model frozen |
| 1 · Machine pass | Page images, re-OCR, cleanup, tagging of the whole volume; site live as draft | Every page marker present; suspect words listed |
| 2 · Proof-reading pass 1 | Saṃvatsara-dīdhiti first (it backs adyatithi), then Tithi and Āśauca | All files at `proofread-1` |
| 3 · Pass 2, figures, tables, variants | Second reader; redraw figures; re-key tables; add Kāśī pāṭhāntara | Quality targets met on the 20-page sample |
| 4 · Indices and v1.0 | Index tags, glossary, introduction; print and screen PDFs; tag v1.0 | URLs frozen; adyatithi switches to deep links |
| After v1.0 (optional) | English topic summaries, Nirṇayasindhu/Dharmasindhu concordance, more scripts | – |

| Work | Size | Assumed rate | Effort (estimate) |
|---|---|---|---|
| Proof-reading pass 1 | 596 printed pages | 20–30 min/page | 200–300 h |
| Proof-reading pass 2 | 596 printed pages | 10–15 min/page | 100–150 h |
| Figures and numeric tables | scan 460–491 | by hand | 30–50 h |
| Index tagging and glossary | about 600 topics | curation | 60–100 h |
| Tooling: OCR, tagging, Hugo theme, PDF class | – | engineering | 80–120 h |

**Open questions**

- [ ] Page images: which scan, and can we get 400 dpi? Is the Digital Library of India copy our OCR source?
- [ ] Copyright of the 1931 edition in India and abroad: decides the licence and whether page images can be shown.
- [ ] Proof-readers: who are the first 3–5 volunteers; do we want a style guide before the pilot?
- [ ] Scope of v1.0: all three dīdhitis, or the Saṃvatsara-dīdhiti first as v0.5?
- [ ] Tamil rendering: Grantha-mixed or superscript numbers by default?
- [ ] English topic summaries in v1.0, or only after?
- [ ] Master format: Markdown + shortcodes (assumed here) or TEI/XML?
