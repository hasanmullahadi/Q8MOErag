# Q8MOErag Extraction Status

Kuwait Ministry of Education textbook knowledge base — extracted from official PDFs for use by the Autodidactic AI tutor.

**Last updated:** 2026-04-11

## Source

PDFs are obtained manually from the **Kuwait Ministry of Education Digital Library**:
https://elibrary.moe.edu.kw/pages/digitallibrary

Navigate by grade and subject to download each book. PDFs are **not tracked in this repo** (too large — see `.gitignore`). The repo stores only the extracted knowledge (outlines, lesson JSONs, and rendered images).

### Known MOE library mislabeling

The MOE digital library has multiple mislabeling/duplication issues. The repo uses actual content as the source of truth:

| MOE file ID | Filename label / cover | **Actual content** |
|---|---|---|
| **3124** | Math Grade 3 Sem 2 Part 1 | **Duplicate of 3387** — same Part 1 content. Not stored separately; see `3124-DUPLICATE-OF-3387.txt` |
| **3387** | Math Grade 3 Sem 2 Part 2 (label was wrong) | **Math Grade 3 Sem 2 Part 1** — stored in `books/grade3/3387-math-sem2-part1.pdf` |
| **3399** | Math Grade 7 Sem 2 Part 1 | **Arabic Grade 5 Sem 2 Part 1** — stored in `books/grade5/3399-arabic-sem2-part1.pdf` |
| **3407** | Arabic Grade 5 Sem 2 Part 1 | **Math Grade 7 Sem 2 Part 2** — stored in `books/grade7/3407-math-sem2-part2.pdf` |

**Missing books (unavailable from MOE digital library):**
- Math Grade 3 Sem 2 **Part 2** — no working file ID found (3387 was mislabeled as Part 2 but serves Part 1)

## Summary

| Metric | Count |
|--------|-------|
| Total unique books in repo | 14 (3124 was a duplicate of 3387) |
| Fully extracted (lessons + images) | 14 |
| Outlines written (no lessons yet) | 0 |
| **Total lessons written** | **312** |
| **Total images extracted** | **3,811** (3399 new: 116, 3387 re-extracted: 134, 3407 new: 328) |

## Books by Grade

### Grade 3 (5 unique books)

| ID | Subject | Lessons | Images | Status |
|----|---------|---------|--------|--------|
| 2854 | Arabic Language (Sem 1) | 11/11 | 533 | Complete |
| 3043 | English (3B) | 20/20 | 302 | Complete |
| 3211 | Science (Sem 2 Part 2) | 9/9 | 190 | Complete |
| **3387** | **Mathematics (Sem 2 Part 1)** | **25/25** | **134** | **Complete** |
| 3390 | Arabic Language (Sem 2 Part 1) | 11/11 | 297 | Complete |

~~3124~~ — duplicate of 3387, removed. See `books/grade3/3124-DUPLICATE-OF-3387.txt`.

### Grade 5 (6 books)

| ID | Subject | Lessons | Images | Status |
|----|---------|---------|--------|--------|
| 2970 | Science (Sem 2 Part 1) | 12/12 | 384 | Complete |
| 3074 | English (5B) | 20/20 | 262 | Complete |
| 3099 | My Country Kuwait (Social Studies) | 24/24 | 220 | Complete |
| 3212 | Science (Sem 2 Part 2) | 12/12 | 599 | Complete |
| **3399** | **Arabic Language (Sem 2 Part 1)** | **39/39** | **116** | **Complete. Units 5-6 with full skill breakdown (poem, listening, reading, vocab, rhetoric, spelling, calligraphy, grammar, speaking, writing, assessment, free reading)** |
| 3412 | Mathematics (Sem 2 Part 1) | 23/23 | 66 | Complete |

### Grade 7 (3 books)

| ID | Subject | Lessons | Images | Status |
|----|---------|---------|--------|--------|
| 3068 | English (7B) | 28/28 | 160 | Complete |
| 3349 | Arabic Language (Sem 2 Part 1) | 42/42 | 106 | Complete |
| **3407** | **Mathematics (Sem 2 FULL — both Parts 1 & 2)** | **36/36** | **328** | **Complete. Single PDF contains both Part 1 (Units 5-6) and Part 2 (Units 7-8). Stored in `3407-math-sem2-full/`** |

**Correction from prior session:** Math Grade 7 Sem 2 Part 1 is **NOT missing** — it's bundled into the same PDF as Part 2 under file ID 3407 (pages 1-130 = Part 1, pages 131-224 = Part 2).

## Pending Work

All 14 books are now fully extracted. No pending lesson extraction work.

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
