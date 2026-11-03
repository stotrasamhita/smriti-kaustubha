# Phase 0 pilot report: Caitra- to Kārttika-kṛtyam (printed pp.85–427)

Status on 2026-11-03. The pilot was planned for the Caitra-kṛtyam (pp.85–108); the Vaiśākha-kṛtyam
(pp.108–117, scan 127–136), the Jyeṣṭha-kṛtyam (pp.117–137, scan 136–156), the Āṣāḍha-kṛtyam
(pp.137–148, scan 156–167), the Śrāvaṇa-kṛtyam (pp.148–200, scan 167–217), the Bhādrapada-kṛtyam
(pp.201–287, scan 218–304), the Āśvina-kṛtyam (pp.287–357, scan 304–374) and the Kārttika-kṛtyam
(pp.358–427, scan 375–444) were added so that whole months can be circulated for comment. The pilot's gate (spec §9) is "pilot site and PDF approved; text model frozen". This report
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
| | Caitra (pp.85–108) | Vaiśākha (pp.108–117) | Jyeṣṭha (pp.117–137) | Āṣāḍha (pp.137–148) | Śrāvaṇa (pp.148–200) | Bhādrapada (pp.201–287) | Āśvina (pp.287–357) | Kārttika (pp.358–427) |
|---|---|---|---|---|---|---|---|---|
| Topic files | 10 | 5 | 8 | 4 | 16 | 37 | 26 | 38 |
| Paragraphs with stable IDs / set verses | 44 / 10 | 19 / 0 | 18 / 0 | 19 / 0 | 86 / 0 | 96 / 0 | 67 / 0 | 67 / 0 |
| Quotations tagged (`q`) | 122 | 48 | 47 | 75 | 231 | 427 | 334 | 224 |
| OCR corrections tagged (`corr`) | 259 | 120 | 281 | 145 | 677 | 1223 | 989 | 1076 |
| Doubtful readings `[?]` | 43 | 18 | 40 | 19 | 65 | 124 | 131 | 125 |
| 1931 footnotes (`fn`) | 29 | 11 | 19 | 4 | 30 | 22 | 23 | 13 |

Cited works in `data/sources.toml`: 138.

Jyeṣṭha notes: the Vaṭa-sāvitrī pūjā (pp.126–128) is a ritual the author copies whole from another manual
("अन्यग्रन्थीया"), so its mantras are not tagged as quotations. The Sāvitrī story (pp.128–134) is introduced as
Skanda-purāṇa but closed as Bhaviṣyottara; it is tagged as Skanda. On pp.118 and 128 the 1931 running head
reads "तिथिदीधितौ" for "संवत्सरदीधितौ", an error in the print, not the OCR.

Āṣāḍha notes: the 1931 edition closes the month with the two colophon verses only, without
"इति आषाढकृत्यम्". The kṛṣṇa-pakṣa vratas at the end (mṛgaśīrṣa, aśūnyaśayana) are described as falling in
Śrāvaṇa: the text reckons that month pūrṇimānta here ("अत्र श्रावणः कृष्णादिः"), so they are amānta Āṣāḍha
kṛṣṇa 1–2 and are tagged as tithis 16–17 of month 4.

Śrāvaṇa notes: **printed pp.150–151 are not in the scan** (scan 168 is p.149, scan 169 is p.152), so the
Vaiṣṇava pavitrāropaṇa and the start of the Devī rite are lost; the text carries both page markers and a
`{{< gap 150 151 >}}` note, and `data/pages.toml` gives them scan 0. They must come from another copy of the
1931 print. Most of the month is dense Mīmāṃsā argument (upākarma, the nature and time of the Janmāṣṭamī vow)
with prayoga lists of Vedic ṛṣi/devatā/chandas that the OCR garbles; those names were restored from the
Ṛgveda anukramaṇī where certain, otherwise flagged `[?]`. The Saṅkaṣṭa-caturthī kathā (51 + 1 numbered verses)
is closed as Brahmāṇḍa-purāṇa and tagged so. The Kaumārī-pūjā passage of p.149 is repeated on p.200; each
copy's OCR was used to check the other, and the readings both lose (कुमारी[र्भो]जयेत्) stay `[?]`. Topic
titles follow the running heads; नागपञ्चम्यादि, रक्षाबन्धविधिः, उत्सर्जनम् and कौमारीपूजा कुशग्रहणं च are
editorial.

Bhādrapada notes: the month is mostly vrata manuals (Haratālikā, Gaṇeśa-caturthī, Ṛṣipañcamī, Mahālakṣmī,
Śravaṇa-dvādaśī, Ananta-caturdaśī, Kapilāṣaṣṭhī) with their kathās and udyāpanas, followed by the Mahālaya
and the other śrāddhas of the dark fortnight. It is split into 37 topic files: the running heads where they
exist, and editorial titles where a vrata, its kathā and its udyāpana share one head. The offset is 17 for the
whole month. Twice the OCR mixes the running head into a word on the page (p.275 "व्य-अविधवा-वस्था", p.285
"विनाशि-कपिला-नीम्"); both are recorded as corrections. The OCR of p.283 (Kapilāṣaṣṭhī arghya rite) is badly
garbled; its prose glosses are left as read and marked `[?]`, and only the verses are restored. The month
closes "इति कौस्तुभे महालयनिर्णयः" and the colophon verses on p.287, where the Āśvina-kṛtyam begins; the second
verse is garbled in the OCR ("योऽनन्तदेवलाभाद्रस्य") and stays `[?]`. The Kapilāṣaṣṭhī (kṛṣṇa 6, amānta tithi
21) is placed by the author after the Āśvina-śukla pratipad śrāddha; the order of the print is kept.

Āśvina notes: most of the month is the Navarātra: whether it is a rite or a count of tithis, who may perform it,
the substitutes, the choice of pratipad, aṣṭamī and navamī, the Bhagavatī and bilva-branch pūjās, the Saptaśatī
recital and homa with a full graha-yajña, the Śatacaṇḍī, the king's lohābhisārika and the horse lustration
(vājinīrājana), then the immersion and pāraṇā. These pages are prayoga lists with Vedic pratīkas and ṛṣi/devatā/
chandas tags, and the OCR garbles many of them; only certain readings are restored, so the share of `[?]` is
higher than in earlier months. After the Upāṅga-lalitā vrata and kathā (128 numbered verses), the Aparājitā and
śamī pūjā of the daśamī and the āśvayujī-karma, the month closes "इत्याश्विनकृत्यम्" on p.357. The running heads
of pp.361–371 still read "आश्विनमासः", but the text has already begun "अथ कार्तिककृत्यम्" on p.358 (the dark
fortnight, amānta Āśvina, reckoned to Kārttika), so those pages are left for the Kārttika section. On p.297 the OCR
misreads the printed page number as 295; the page marker follows the scan offset. The margin note "कोजागर" on
p.355 is read into a verse by the OCR and is restored as a side-heading.

Kārttika notes: the section runs from "अथ कार्तिककृत्यम्" (p.358) to "इति कार्तिकमासकृत्यम्" (p.427), where
"अथ मार्गशीर्षकृत्यं" begins on the same page. The dark-fortnight topics of pp.367–373 (Govatsa-dvādaśī,
Yama-dīpa, Gotrirātra, Naraka-caturdaśī, the Dīpāvalī amāvāsyā) sit under the running head "आश्विनमासः" and close
"इत्याश्विनमासः"; they are tagged month 7 (amānta Āśvina), tithis 16–30, and the rest month 8. After the pratipad
(Govardhana, annakūṭa, Mārgapālī, Bali-pūjā), Yama-dvitīyā and the Prabodhinī, most of the month is vrata
udyāpanas (ekādaśī, Bhīṣma-pañcaka, the Kārttika vow, lakṣa-pradakṣiṇā/namaskāra/pūjā/varti, dhāraṇā-pāraṇā,
Gopadma) and dāna manuals, with the vṛṣotsarga of the full moon (pp.390–405) after Āśvalāyana, the Kālikā-purāṇa,
Baudhāyana, Kātyāyana and the Śāṭyāyanas. The prayoga pages (pp.391–405, 411–414, 418–424) are badly garbled in the
OCR; mantra pratīkas and prose glosses are left as read and marked `[?]` where uncertain, and only certain readings
are restored. On p.373 the OCR puts the last words of the Naraka-caturdaśī topic into the running head, and on
p.404 the syllable "वाय" (of "भवाय"); both are read back into the text. Footnote places that the OCR loses
(pp.376, 385) are marked `[?]`. The two closing verses on p.427 are abbreviated in the print ("येनार्जितानि०",
"योऽनन्तदेव०").

Every correction keeps the OCR reading (`{{< corr ocr="…" >}}`) and shows on the web as a highlight with the OCR
reading on hover. The PDF reading copy prints the corrected text silently and logs every correction in
`<name>-corrections.tsv`; the draft copy (`--draft`) prints them as apparatus notes "lemma ] OCR reading". Corrections were made from context,
grammar and metre only; none has been checked against the page image yet.

The topics follow the 1931 running heads: चान्द्रमासनिर्णयः, कल्पादिनिर्णयः, प्रपादाननिर्णयः, रामदोलोत्सवनिर्णयः,
स्कन्दपूजानिर्णयः, रामनवमीनिर्णयः, श्रीकृष्णदोलोत्सवः, दमनकोत्सवः, नृसिंहदोलोत्सवः, वारुणीयोगः; and
वैशाखमासकृत्यम्, अक्षय्यतृतीया, देवीपूजा, नृसिंहजयन्ती, पौर्णमास्यां कर्तव्यम्. Two Vaiśākha titles are editorial,
since no running head names those pages: वैशाखमासकृत्यम् (from "अथ वैशाखकृत्यम्") and नृसिंहजयन्ती (from
"इति नृसिंहजयन्त्युत्सवः").

## Decisions taken in the pilot (now in spec §4)

- Paragraph IDs are explicit `{#p87.3}` lines, checked by `tools/validate.py`, not computed at build time.
- Three shortcodes added: `fn` (the 1931 edition's own footnotes), `mn` (its margin side-headings) and `gap`
  (printed pages missing from the scan).
- Only verses the 1931 edition sets apart are `shloka` blocks; quoted verses printed as prose are `q` only.
- `tithis` numbered 1–30 through the amānta month.

## For the reviewers

- Site: built by CI and published to GitHub Pages once this is merged to `master` (Pages source must be set to
  "GitHub Actions" in the repository settings). Locally: `make site && hugo server`.
- PDF: CI artifact `sk-samvatsara-pdf`, and `/pdf/sk-samvatsara.pdf` (reading copy) and
  `/pdf/sk-samvatsara-draft.pdf` (with OCR apparatus) on the site. The earlier addresses
  `/pdf/sk-caitra-vaisakha.pdf` and `-draft.pdf` serve the same files.
- Please check in particular: the half-verse layout, the apparatus density (about 11 notes per page), margin
  page numbers, and whether the side-headings belong in the margin on the web.

## Still missing before the gate

1. **Page images** at 400 dpi for scan 104–374, then proof-reading pass 1 and pass 2 (different readers) using
   `docs/proofreading/caitra-krtyam.md`, `vaisakha-krtyam.md`, `jyestha-krtyam.md`, `ashadha-krtyam.md`,
   `shravana-krtyam.md`, `bhadrapada-krtyam.md`, `ashvina-krtyam.md` and `kartika-krtyam.md`; and a copy of the missing pp.150–151. Status moves `cleaned → proofread-1 → proofread-2`.
2. Indices not yet built: subject index and glossary (need `ix` tags and `data/glossary.toml`); the verse-pāda
   index covers set verses only (see the run-in verse question in spec §9).
3. PDF polish: Tiro Devanagari Sanskrit could not be installed in the build environment, so the PDF falls back
   to Noto Serif Devanagari; line-numbered apparatus, ICU collation, PDF/X and PDF/A profiles.
4. `adyatithi` IDs in the front matter (left empty rather than guessed).
5. The open questions in spec §9, including the new ones on run-in verses and apparatus keying.
