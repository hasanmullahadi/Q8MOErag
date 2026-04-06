# Q8 MOE RAG - Kuwait Ministry of Education Textbook Knowledge Base

Pre-extracted knowledge from Kuwait Ministry of Education (MOE) textbooks for use with RAG-based AI tutoring systems.

## What This Is

Parents upload school textbooks (PDFs) and we extract structured knowledge using Claude (Opus) — creating clean lesson outlines, examples, and image references that any AI tutor can use without needing OCR or vision models at runtime.

**This is a one-time extraction.** The output is committed to this repo so other parents with the same textbooks can skip the extraction step entirely.

## Structure

```
books/
└── grade3/
    ├── 3124-math-sem2-part1.pdf          # Source PDF
    ├── 3124-math-sem2-part1/             # Extracted knowledge
    │   ├── outline.json                  # Lesson structure + topics
    │   ├── lessons/
    │   │   ├── 01-lesson-title.json      # Lesson content, examples, exercises
    │   │   ├── 02-lesson-title.json
    │   │   └── ...
    │   └── images/                       # Referenced images from textbook
    │       ├── p17_fig1.png
    │       └── ...
    ├── 3387-math-sem2-part2.pdf
    ├── 3387-math-sem2-part2/
    │   └── ...
    └── ...
```

## Books Included

### Grade 3 (الصف الثالث)
| ID | Subject | Semester | Part |
|----|---------|----------|------|
| 2854 | لغتي العربية (Arabic) | 1 | 1 |
| 3043 | Skyline English 3B | 2 | - |
| 3124 | الرياضيات (Math) | 2 | 1 |
| 3387 | الرياضيات (Math) | 2 | 2 |
| 3390 | العلوم (Science) | 2 | 1 |
| 3211 | العلوم (Science) | 2 | 2 |

### Grade 5 (الصف الخامس)
| ID | Subject | Semester | Part |
|----|---------|----------|------|
| 3407 | لغتي العربية (Arabic) | 2 | 1 |
| 3074 | Skyline English 5B | 2 | - |
| 3412 | الرياضيات (Math) | 2 | 1 |
| 2970 | العلوم (Science) | 2 | 1 |
| 3212 | العلوم (Science) | 2 | 2 |
| 3099 | وطني الكويت (Social Studies) | 2 | - |

### Grade 7 (الصف السابع)
| ID | Subject | Semester | Part |
|----|---------|----------|------|
| 3349 | لغتي العربية (Arabic) | 2 | 1 |
| 3068 | English Pearls 7B | 2 | - |
| 3399 | الرياضيات (Math) | 2 | 1 |

## How to Use

1. Check if your textbook is already extracted here
2. If yes — point your AI tutor at the `outline.json` and `lessons/` directory
3. If no — follow the [WORKFLOW.md](WORKFLOW.md) to extract your own and submit a PR

## For Autodidactic

This repo feeds into [Autodidactic](https://github.com/hasanmullahadi/Autodidactic) — a local AI tutor for kids running on llama.cpp. Instead of fighting with PDF OCR at runtime, Autodidactic loads pre-extracted lesson data from this repo.

## License

The textbook content belongs to Kuwait Ministry of Education. This repo contains structured extractions for educational use only.
