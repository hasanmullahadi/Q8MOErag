# Extraction Workflow

How to extract structured knowledge from a Kuwait MOE textbook PDF.

## Prerequisites

- Claude (Opus) access — used for visual PDF reading
- The textbook PDF file

## Step 1: Add the PDF

Place the PDF in the appropriate folder:

```
books/grade{N}/{MOE_ID}-{subject}-sem{S}-part{P}.pdf
```

Example: `books/grade3/3387-math-sem2-part2.pdf`

## Step 2: Extract Outline (with Claude)

Open the PDF's **table of contents pages** (usually pages 5-15) in Claude and ask:

```
Read the table of contents from this textbook. For each lesson, extract:
1. Lesson number and code (e.g. 5-1)
2. Lesson title in Arabic
3. Page number
4. Which unit it belongs to

Return as JSON:
{
  "book_id": "3387",
  "subject": "الرياضيات",
  "grade": 3,
  "semester": 2,
  "part": 2,
  "units": [
    {
      "unit_number": 5,
      "unit_title": "...",
      "lessons": [
        {"code": "5-1", "title": "...", "page": 17},
        ...
      ]
    }
  ]
}
```

Save as `books/grade3/3387-math-sem2-part2/outline.json`

## Step 3: Extract Lesson Content (with Claude)

For each lesson, open the lesson's pages in Claude and extract:

```
Read pages {start}-{end} of this textbook lesson. Extract:
1. title: Lesson title
2. objectives: What the student should learn
3. key_concepts: Core concepts explained (in Arabic)
4. vocabulary: New terms with definitions
5. examples: Worked examples from the textbook (step by step)
6. exercises: Practice problems (without answers)
7. images: Describe any important diagrams/figures with page references
```

Save as `books/grade3/3387-math-sem2-part2/lessons/01-lesson-title.json`

## Step 4: Extract Referenced Images

For each lesson that has important diagrams, figures, or visual aids:

1. Take a screenshot or extract the image from the PDF
2. Save as `books/grade3/3387-math-sem2-part2/images/p{PAGE}_fig{N}.png`
3. Reference the filename in the lesson JSON under `images`

## Step 5: Commit and PR

```bash
git add books/grade{N}/
git commit -m "Add {subject} grade {N} semester {S} part {P}"
git push
```

If contributing to the public repo, submit a Pull Request.

## JSON Schema

### outline.json

```json
{
  "book_id": "3387",
  "subject": "الرياضيات",
  "subject_en": "Mathematics",
  "grade": 3,
  "semester": 2,
  "part": 2,
  "country": "Kuwait",
  "publisher": "وزارة التربية - دولة الكويت",
  "year": "2025-2026",
  "total_pages": 165,
  "units": [
    {
      "unit_number": 5,
      "unit_title": "القسمة",
      "page_start": 14,
      "lessons": [
        {
          "code": "5-1",
          "title": "استكشاف القسمة (التوزيع بالتساوي)",
          "page": 17,
          "objectives": ["..."],
          "vocabulary": ["القسمة", "التوزيع بالتساوي", "المقسوم", "المقسوم عليه"]
        }
      ]
    }
  ]
}
```

### lessons/{NN}-title.json

```json
{
  "code": "5-1",
  "title": "استكشاف القسمة (التوزيع بالتساوي)",
  "page_start": 17,
  "page_end": 19,
  "objectives": [
    "أن يتعرف المتعلم على مفهوم القسمة كتوزيع بالتساوي"
  ],
  "key_concepts": [
    {
      "concept": "القسمة",
      "explanation": "توزيع عدد من الأشياء بالتساوي على مجموعات"
    }
  ],
  "vocabulary": [
    {"term": "المقسوم", "definition": "العدد الذي يتم تقسيمه"},
    {"term": "المقسوم عليه", "definition": "العدد الذي نقسم عليه"},
    {"term": "ناتج القسمة", "definition": "نتيجة عملية القسمة"}
  ],
  "examples": [
    {
      "problem": "وزعت الأم 10 أساور على 5 بنات بالتساوي. كم سواراً لكل بنت؟",
      "solution_steps": [
        "المقسوم = 10",
        "المقسوم عليه = 5",
        "10 ÷ 5 = 2",
        "كل بنت تحصل على سوارين"
      ],
      "answer": "2"
    }
  ],
  "exercises": [
    {"problem": "12 قلماً توزع على 3 أصدقاء. كم لكل صديق؟", "answer": "4"},
    {"problem": "8 حلويات توزع على 4 أطفال. كم لكل طفل؟", "answer": "2"}
  ],
  "images": [
    {"file": "p17_fig1.png", "description": "رسم توضيحي لتوزيع 10 أساور على 5 مجموعات"}
  ]
}
```

## How Autodidactic Uses This

1. Parent uploads a book → system checks this repo for pre-extracted data
2. If found → loads `outline.json` as the study plan, `lessons/*.json` for teaching content
3. Miss Noor (the AI tutor) uses the extracted examples and exercises directly — no OCR needed
4. Images are served alongside the lesson for visual reference
