# Extraction Workflow

How to extract structured knowledge from Kuwait MOE textbook PDFs using Claude (Opus).

## Proven Process (tested on book 3387)

### Step 1: Read the TOC visually

Open the PDF in Claude, read the table of contents pages (usually pages 5-15). Claude reads the Arabic perfectly from the visual — no OCR needed.

### Step 2: Create outline.json

From the TOC, create the book outline with all units and lessons:

```
books/grade{N}/{ID}-{subject}/outline.json
```

### Step 3: Read each lesson (2-3 pages each)

For each lesson, open its pages in Claude and extract:
- **objectives** (from "سأتعلم في هذا الدرس")
- **vocabulary** (from "المفردات" sidebar) — Arabic term + English + definition
- **key_concepts** — the core teaching explanation
- **examples** (from "لنتعلم معاً") — worked examples with step-by-step solutions
- **exercises** (from "تدرب", "حاول", "تفكير ناقد", "تقييم ذاتي") — with answers
- **teaching_notes** — pedagogical guidance for the AI tutor

Save as: `lessons/{NN}-{code}-{title-slug}.json`

### Step 4: Extract images

Use PyMuPDF to render full pages at 200 DPI and extract embedded figures:

```python
import fitz
doc = fitz.open("book.pdf")
for page_num in lesson_pages:
    page = doc[page_num - 1]
    pix = page.get_pixmap(dpi=200)
    pix.save(f"images/p{page_num:02d}_{code}.png")
    # Also extract large embedded figures (>15KB)
    for img in page.get_images(full=True):
        base = doc.extract_image(img[0])
        if base and len(base["image"]) > 15000:
            with open(f"images/p{page_num:02d}_{code}_fig{idx}.{base['ext']}", "wb") as f:
                f.write(base["image"])
```

### Step 5: Parallelize with agents

For efficiency, launch multiple Claude agents in parallel — each handling 4-6 lessons. One agent reads the TOC and creates the outline, others create lesson JSONs from the page content you describe to them.

### Step 6: Commit and push

```bash
git add books/grade{N}/{ID}-{subject}/
git commit -m "Complete extraction of book {ID}"
git push
```

## File Structure

```
books/grade3/3387-math-sem2-part2/
├── outline.json                    # Book structure
├── lessons/
│   ├── 01-5-1-exploring-division.json
│   ├── 02-5-2-repeated-subtraction.json
│   └── ... (one per lesson)
└── images/
    ├── p18_5-1.png                 # Full page render (200 DPI)
    ├── p18_5-1_fig2.jpeg           # Extracted figure
    └── ...
```

## JSON Schemas

### outline.json

```json
{
  "book_id": "3387",
  "subject": "الرياضيات",
  "subject_en": "Mathematics",
  "grade": 3, "semester": 2, "part": 2,
  "country": "Kuwait",
  "publisher": "وزارة التربية - دولة الكويت",
  "year": "2025-2026",
  "total_pages": 165,
  "units": [{
    "unit_number": 5,
    "unit_title": "القسمة",
    "unit_title_en": "Division",
    "page_start": 14,
    "lessons": [
      {"code": "5-1", "title": "...", "title_en": "...", "page": 17, "page_end": 19}
    ]
  }]
}
```

### lessons/{NN}-{code}-{slug}.json

```json
{
  "code": "5-1",
  "title": "استكشاف القسمة (التوزيع بالتساوي)",
  "title_en": "Exploring Division (Equal Distribution)",
  "page_start": 17, "page_end": 19,
  "objectives": ["..."],
  "vocabulary": [
    {"term": "القسمة", "term_en": "division", "definition": "..."}
  ],
  "key_concepts": [
    {"concept": "...", "explanation": "..."}
  ],
  "examples": [{
    "problem": "...",
    "solution_steps": ["step 1", "step 2"],
    "answer": "...",
    "visual_description": "..."
  }],
  "exercises": [
    {"id": 1, "type": "...", "problem": "...", "answer": "..."}
  ],
  "images": {
    "pages": ["images/p18_5-1.png"],
    "figures": [{"file": "images/p18_fig2.jpeg", "description": "..."}]
  },
  "teaching_notes": "..."
}
```

## Extraction Stats (book 3387)

| Metric | Count |
|--------|-------|
| Lessons | 21 |
| Lesson JSONs | 21 files |
| Page images | 42 (full pages at 200 DPI) |
| Figure images | 76 (embedded illustrations) |
| Total image files | 118 |
| Total size | 28 MB |
| Time to extract | ~30 min with parallel agents |

## How Autodidactic Uses This

1. Parent uploads a book → system checks this repo by book ID
2. If found → loads `outline.json` as study plan, `lessons/*.json` for content
3. Miss Noor teaches using the actual textbook examples and exercises
4. Textbook page images displayed alongside the chat
5. No OCR, no vision model, no garbled Arabic — just clean pre-extracted JSON
