# Q8MOErag Extraction Status

Kuwait Ministry of Education textbook knowledge base — extracted from official PDFs for use by the Autodidactic AI tutor.

**Last updated:** 2026-04-10

## Source

PDFs are obtained manually from the **Kuwait Ministry of Education Digital Library**:
https://elibrary.moe.edu.kw/pages/digitallibrary

Navigate by grade and subject to download each book. PDFs are **not tracked in this repo** (too large — see `.gitignore`). The repo stores only the extracted knowledge (outlines, lesson JSONs, and rendered images).

### Known MOE library mislabeling

The MOE digital library serves the wrong content for two file IDs — the filenames and covers do not match the actual book content inside. The repo uses the actual content as the source of truth:

| MOE file ID | Filename label / cover | **Actual content** |
|---|---|---|
| **3399** | Math Grade 7 Sem 2 Part 1 | **Arabic Grade 5 Sem 2 Part 1** — stored in `books/grade5/3399-arabic-sem2-part1.pdf` |
| **3407** | Arabic Grade 5 Sem 2 Part 1 | **Math Grade 7 Sem 2 Part 2** — stored in `books/grade7/3407-math-sem2-part2.pdf` |

**Missing book:** Math Grade 7 Sem 2 **Part 1** is not served by any known MOE file ID — appears unavailable via the digital library.

## Summary

| Metric | Count |
|--------|-------|
| Total books in repo | 15 |
| Fully extracted (lessons + images) | 12 |
| Outlines written (no lessons yet) | 3 |
| **Total lessons written** | **233** |
| **Total images extracted** | **3,237** |

## Books by Grade

### Grade 3 (6 books)

| ID | Subject | Lessons | Images | Status |
|----|---------|---------|--------|--------|
| 2854 | Arabic Language (Sem 1) | 11/11 | 533 | Complete |
| 3043 | English (3B) | 20/20 | 302 | Complete |
| **3124** | **Mathematics (Sem 2 Part 1)** | **0/21** | **0** | **Outline ready — lessons pending** |
| 3211 | Science (Sem 2 Part 2) | 9/9 | 190 | Complete |
| 3387 | Mathematics (Sem 2 Part 2) | 21/21 | 118 | Complete |
| 3390 | Arabic Language (Sem 2 Part 1) | 11/11 | 297 | Complete |

### Grade 5 (6 books)

| ID | Subject | Lessons | Images | Status |
|----|---------|---------|--------|--------|
| 2970 | Science (Sem 2 Part 1) | 12/12 | 384 | Complete |
| 3074 | English (5B) | 20/20 | 262 | Complete |
| 3099 | My Country Kuwait (Social Studies) | 24/24 | 220 | Complete |
| 3212 | Science (Sem 2 Part 2) | 12/12 | 599 | Complete |
| **3399** | **Arabic Language (Sem 2 Part 1)** | **0/~38** | **0** | **Outline ready — lessons pending (file from MOE ID 3399)** |
| 3412 | Mathematics (Sem 2 Part 1) | 23/23 | 66 | Complete |

### Grade 7 (3 books)

| ID | Subject | Lessons | Images | Status |
|----|---------|---------|--------|--------|
| 3068 | English (7B) | 28/28 | 160 | Complete |
| 3349 | Arabic Language (Sem 2 Part 1) | 42/42 | 106 | Complete |
| **3407** | **Mathematics (Sem 2 Part 2)** | **0/~40** | **0** | **Outline partial (Units 5-6 done, 7-8 pending) — from MOE ID 3407** |

**Missing:** Math Grade 7 Sem 2 Part 1 — not available from MOE digital library.

## Pending Work (3 books with outlines ready)

All three have their directories created and `outline.json` written. Lesson JSON extraction is the next step.

### 1. 3124 Math Grade 3 Sem 2 Part 1

- **21 lessons planned** across 2 units (division, data analysis)
- Unit 5: Division (12 lessons on division by 1-9)
- Unit 6: Division with remainders, even/odd, data organization, graphing
- Total PDF pages: 86
- Theme: Celebrating Kuwait's National Day (February 25) and Liberation Day (February 26)

### 2. 3399 Arabic Grade 5 Sem 2 Part 1

- **~38 lessons planned** across 2 units (2 main reading lessons per unit, each with 8 integrated sub-skills)
- Unit 5: أنشودة الوطن, أعلام من بلدي
- Unit 6: رحلة إلى المطاحن الكويتية, السجايا: المشروع الرائد
- Grammar: المفعول به, حال الفاعل, ظرفي الزمان والمكان
- Spelling: الهمزة المتوسطة, الألف اللينة
- Calligraphy: خط الرقعة (ع-غ-ف-ق-ك-ل-م-ن)
- Total PDF pages: 260

### 3. 3407 Math Grade 7 Sem 2 Part 2 (Units 5-6 outlined, 7-8 pending)

- **~40 lessons planned** across 4 units (outline written for Units 5-6 only)
- Unit 5: Fractions and Operations (9 lessons + evaluation)
- Unit 6: Geometry — Triangles, Parallel Lines, Parallelograms (9 lessons + eval + project)
- Unit 7: Percentages — *TOC not yet read*
- Unit 8: Probability — *TOC not yet read*
- Total PDF pages: 224
- Theme: Clinical Pharmacy (for Unit 5)

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
