#!/usr/bin/env python3
"""
Extract images from all Q8MOErag textbook PDFs.

For each book that has lesson JSONs but no images yet:
  1. Reads each lesson JSON to get page ranges and codes
  2. Renders full pages at 200 DPI as PNG
  3. Extracts embedded figures >15KB as JPEG/PNG
  4. Saves to the book's images/ directory

Usage:
    python3 extract_all_images.py          # process all books
    python3 extract_all_images.py --force   # re-extract even if images exist
    python3 extract_all_images.py --book 3349  # process specific book only
"""

import fitz  # PyMuPDF
import json
import os
import sys
import time
import glob
import argparse

REPO = "/Users/hasanabdulhadi/Documents/Q8MOErag"
BOOKS_DIR = os.path.join(REPO, "books")
DPI = 200
MIN_FIG_SIZE = 15_000  # 15KB minimum for extracted figures
DELAY_BETWEEN_BOOKS = 2  # seconds between books


def find_books():
    """Find all book directories that have lessons."""
    books = []
    for grade_dir in sorted(glob.glob(os.path.join(BOOKS_DIR, "grade*"))):
        for book_dir in sorted(glob.glob(os.path.join(grade_dir, "*"))):
            if not os.path.isdir(book_dir):
                continue
            lessons_dir = os.path.join(book_dir, "lessons")
            if not os.path.isdir(lessons_dir):
                continue
            lesson_files = sorted(glob.glob(os.path.join(lessons_dir, "*.json")))
            if not lesson_files:
                continue

            book_id = os.path.basename(book_dir).split("-")[0]
            # Find matching PDF (same name as directory)
            pdf_name = os.path.basename(book_dir) + ".pdf"
            pdf_path = os.path.join(grade_dir, pdf_name)
            if not os.path.exists(pdf_path):
                # Try matching by book ID prefix
                for f in os.listdir(grade_dir):
                    if f.startswith(book_id) and f.endswith(".pdf"):
                        pdf_path = os.path.join(grade_dir, f)
                        break

            if not os.path.exists(pdf_path):
                print(f"  SKIP {os.path.basename(book_dir)}: no PDF found")
                continue

            images_dir = os.path.join(book_dir, "images")
            existing_images = len(glob.glob(os.path.join(images_dir, "*"))) if os.path.isdir(images_dir) else 0

            books.append({
                "book_dir": book_dir,
                "book_name": os.path.basename(book_dir),
                "book_id": book_id,
                "pdf_path": pdf_path,
                "lessons_dir": lessons_dir,
                "images_dir": images_dir,
                "lesson_files": lesson_files,
                "existing_images": existing_images,
            })
    return books


def read_lesson_pages(lesson_files):
    """Read all lesson JSONs and return list of (code, page_start, page_end)."""
    lessons = []
    for lf in lesson_files:
        with open(lf) as f:
            data = json.load(f)
        code = data.get("code", "")
        ps = data.get("page_start")
        pe = data.get("page_end", ps)
        if ps and code:
            lessons.append((code, int(ps), int(pe)))
    return lessons


def extract_book_images(book, force=False):
    """Extract all images for a single book."""
    name = book["book_name"]
    images_dir = book["images_dir"]

    if book["existing_images"] > 0 and not force:
        print(f"  SKIP {name}: already has {book['existing_images']} images (use --force to re-extract)")
        return 0

    os.makedirs(images_dir, exist_ok=True)

    lessons = read_lesson_pages(book["lesson_files"])
    if not lessons:
        print(f"  SKIP {name}: no valid lessons found")
        return 0

    # Collect all unique pages with their lesson code
    page_to_code = {}
    for code, ps, pe in lessons:
        for p in range(ps, pe + 1):
            page_to_code[p] = code

    pdf_path = book["pdf_path"]
    pdf_size_mb = os.path.getsize(pdf_path) / (1024 * 1024)
    print(f"  Processing {name} — {len(lessons)} lessons, {len(page_to_code)} pages, PDF {pdf_size_mb:.1f}MB")

    doc = fitz.open(pdf_path)
    total_pdf_pages = len(doc)
    total_images = 0

    for page_num in sorted(page_to_code.keys()):
        if page_num < 1 or page_num > total_pdf_pages:
            print(f"    WARNING: page {page_num} out of range (PDF has {total_pdf_pages} pages)")
            continue

        code = page_to_code[page_num]
        page = doc[page_num - 1]

        # 1. Full page render at 200 DPI
        pix = page.get_pixmap(dpi=DPI)
        page_file = os.path.join(images_dir, f"p{page_num:03d}_{code}.png")
        pix.save(page_file)
        total_images += 1

        # 2. Extract embedded figures >15KB
        try:
            img_list = page.get_images(full=True)
        except Exception:
            img_list = []

        for idx, img in enumerate(img_list, 1):
            xref = img[0]
            try:
                base = doc.extract_image(xref)
            except Exception:
                continue
            if base and len(base["image"]) > MIN_FIG_SIZE:
                ext = base.get("ext", "png")
                fig_file = os.path.join(images_dir, f"p{page_num:03d}_{code}_fig{xref}.{ext}")
                with open(fig_file, "wb") as f:
                    f.write(base["image"])
                total_images += 1

    doc.close()
    print(f"    Done: {total_images} images extracted")
    return total_images


def main():
    parser = argparse.ArgumentParser(description="Extract images from Q8MOErag textbook PDFs")
    parser.add_argument("--force", action="store_true", help="Re-extract even if images exist")
    parser.add_argument("--book", type=str, help="Process only this book ID (e.g., 3349)")
    args = parser.parse_args()

    print(f"Q8MOErag Image Extraction")
    print(f"{'=' * 50}")

    books = find_books()
    if args.book:
        books = [b for b in books if b["book_id"] == args.book]

    print(f"Found {len(books)} books with lessons\n")

    grand_total = 0
    processed = 0

    for i, book in enumerate(books):
        print(f"[{i+1}/{len(books)}] {book['book_name']}:")
        count = extract_book_images(book, force=args.force)
        grand_total += count
        if count > 0:
            processed += 1
            # Delay between books (not after the last one)
            if i < len(books) - 1:
                print(f"    Waiting {DELAY_BETWEEN_BOOKS}s...")
                time.sleep(DELAY_BETWEEN_BOOKS)
        print()

    print(f"{'=' * 50}")
    print(f"Total: {grand_total} images from {processed} books")


if __name__ == "__main__":
    main()
