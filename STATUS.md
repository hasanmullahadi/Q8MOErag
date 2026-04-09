# Q8MOErag Extraction Status

Kuwait Ministry of Education textbook knowledge base — extracted from official PDFs for use by the Autodidactic AI tutor.

**Last updated:** 2026-04-09

## Source

PDFs are obtained manually from the **Kuwait Ministry of Education Digital Library**:
https://elibrary.moe.edu.kw/pages/digitallibrary

Navigate by grade and subject to download each book. PDFs are **not tracked in this repo** (too large — see `.gitignore`). The repo stores only the extracted knowledge (outlines, lesson JSONs, and rendered images).

## Summary

| Metric | Count |
|--------|-------|
| Total books in repo | 15 |
| Fully extracted | 12 |
| Pending extraction | 1 |
| PDF swap issues | 2 |
| **Total lessons written** | **233** |
| **Total images extracted** | **3,237** |
| Total PDF size | 710 MB |
| Total images size | 824 MB |

## Books by Grade

### Grade 3 (6 books)

| ID | Subject | Lessons | Images | PDF | Status |
|----|---------|---------|--------|-----|--------|
| 2854 | Arabic Language (Sem 1) | 11/11 | 533 | 92 MB | Complete |
| 3043 | English (3B) | 20/20 | 302 | 43 MB | Complete |
| 3124 | Mathematics (Sem 2 Part 1) | — | — | 23 MB | Not started |
| 3211 | Science (Sem 2 Part 2) | 9/9 | 190 | 47 MB | Complete |
| 3387 | Mathematics (Sem 2 Part 2) | 21/21 | 118 | 21 MB | Complete |
| 3390 | Arabic Language (Sem 2 Part 1) | 11/11 | 297 | 194 MB | Complete |

### Grade 5 (6 books)

| ID | Subject | Lessons | Images | PDF | Status |
|----|---------|---------|--------|-----|--------|
| 2970 | Science (Sem 2 Part 1) | 12/12 | 384 | 39 MB | Complete |
| 3074 | English (5B) | 20/20 | 262 | 32 MB | Complete |
| 3099 | My Country Kuwait (Sem 2) | 24/24 | 220 | 47 MB | Complete |
| 3212 | Science (Sem 2 Part 2) | 12/12 | 599 | 73 MB | Complete |
| 3407 | Arabic Language (Sem 2 Part 1) | — | — | 35 MB | PDF swap issue |
| 3412 | Mathematics (Sem 2 Part 1) | 23/23 | 66 | 38 MB | Complete |

### Grade 7 (3 books)

| ID | Subject | Lessons | Images | PDF | Status |
|----|---------|---------|--------|-----|--------|
| 3068 | English (7B) | 28/28 | 160 | 18 MB | Complete |
| 3349 | Arabic Language (Sem 2 Part 1) | 42/42 | 106 | 4 MB | Complete |
| 3399 | Mathematics (Sem 2 Part 1) | — | — | 6 MB | PDF swap issue |

## Fully Extracted Books (12)

Each of these has a complete `outline.json`, all lesson JSONs in `lessons/`, and all page/figure images in `images/`.

1. **3387 Math G3** — 21 lessons, 118 images. Division, Multiplication, Geometry, Measurement.
2. **3211 Science G3** — 9 lessons, 190 images. (Units per outline.)
3. **3043 English G3** — 20 lessons, 302 images. Units 5-8.
4. **2854 Arabic G3** — 11 lessons, 533 images. Unit 1 (قمراً, طريق النجاح), Unit 2 (حزام الأمان, hadith).
5. **3390 Arabic G3** — 11 lessons, 297 images. Units 5-6 (رحلة إلى البر, يوم دراسي في رمضان, فرحة وطن, صلة الرحم).
6. **3074 English G5** — 20 lessons, 262 images. Units 5-8: Our Passport To The World, Active And Smart, The Culture Compass, Healthy Habits Better Life.
7. **3412 Math G5** — 23 lessons, 66 images. 2 units: Fractions (10), Operations on Fractions (13).
8. **2970 Science G5** — 12 lessons, 384 images. 3 chapters: Matter Secrets, Electrical Energy, Forces.
9. **3212 Science G5** — 12 lessons, 599 images. 2 chapters: Earth's Treasures, Astronaut Journey.
10. **3099 Social Studies G5** — 24 lessons, 220 images. 4 units: History of Renaissance, Population, Regional Organizations, Land of Giving.
11. **3068 English G7** — 28 lessons, 160 images. 4 units (5-8), 7 lessons per unit. "English Pearls of Kuwait".
12. **3349 Arabic G7** — 42 lessons, 106 images. 2 units × 2 topics. Grammar: بناء الفعل الماضي/المضارع/الأمر. Rhetoric: النداء (حقيقي/بلاغي). Spelling: الهمزة المتطرفة.

## Pending Work

### 1. Not yet started (1 book)

- **3124 Math G3 Sem 2 Part 1** — No extraction directory yet. PDF is 22.6 MB. Next book to tackle.

### 2. PDF swap issues (2 books)

The following PDFs are misfiled and contain the wrong content:

- `books/grade5/3407-arabic-sem2-part1.pdf` → actually contains **Math Grade 7** (30 lessons, 4 units: Fractions, Geometry, Percentages, Probability).
- `books/grade7/3399-math-sem2-part1.pdf` → actually contains **Arabic Grade 5**.

**Action needed:** User should swap or rename these PDFs. Once fixed, extraction can proceed normally.

## Extraction Process

1. **Outline** — Read TOC pages visually, write `outline.json` with all units/lessons and page ranges.
2. **Lessons** — For each lesson, read 2-3 PDF pages visually and write lesson JSON (objectives, vocabulary, key_concepts, examples, exercises, teaching_notes).
3. **Images** — Run `extract_all_images.py` to render full pages at 200 DPI and extract embedded figures >15KB.

See `WORKFLOW.md` for full details and JSON schemas.

## Image Extraction Script

The `extract_all_images.py` script automates image extraction for all books:

```bash
python3 extract_all_images.py          # process all books (skips ones already done)
python3 extract_all_images.py --force   # re-extract even if images exist
python3 extract_all_images.py --book 3349  # process specific book only
```

It reads each lesson's `page_start`/`page_end` fields, renders pages via PyMuPDF at 200 DPI, and extracts embedded figures larger than 15 KB. A 2-second delay between books keeps resource usage reasonable.

## How This Feeds Autodidactic

1. Parent uploads a Kuwait MOE book → Autodidactic looks up the book ID in this repo
2. If found → loads `outline.json` as study plan, `lessons/*.json` for content
3. Miss Noor (the AI tutor) teaches using the actual textbook examples and exercises
4. Textbook page images are displayed alongside the chat
5. No OCR, no vision model, no garbled Arabic — just clean pre-extracted JSON
