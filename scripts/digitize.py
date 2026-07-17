#!/usr/bin/env python3
"""
digitize.py — Parse raw Sanskrit source text into the corpus JSON schema.

Handles three source types:
  1. Unicode Devanagari .md/.txt files (from sanskritdocuments.org — most common)
  2. Text-layer PDFs (Unicode PDFs; use -p/--pdf)
  3. Scanned image PDFs (OCR via Google Vision; use -p/--pdf --ocr-backend=vision)

Output is a draft JSON with status="untranslated" for every shloka, ready for
translate.py to fill in English + Hindi.

Usage:
  python scripts/digitize.py SOURCE_FILE \\
    --text-id saravali \\
    --title-sa "सारावली" \\
    --title-en "Saravali" \\
    --category hora \\
    --output Hora/Saravali/saravali.json

  # Single-chapter mode (one JSON per chapter, like BrihatJataka):
  python scripts/digitize.py SOURCE_FILE --text-id saravali --per-chapter \\
    --output-dir Hora/Saravali/chapters/

Dependencies (install as needed):
  pip install pymupdf          # PDF text extraction (text-layer PDFs)
  pip install google-cloud-vision pillow  # scanned image OCR
"""

import argparse
import json
import re
import sys
from pathlib import Path


# ── Shloka boundary detection ──────────────────────────────────────────────

# Matches: ॥ 12॥  or  ॥१२॥  or  ॥ 12 ॥  (Devanagari + ASCII digits)
SHLOKA_END_RE = re.compile(
    r'॥\s*([०-९\d]+(?:[/][०-९\d]+)?[अ-ह]?)\s*॥'
)

# Sanskrit ordinal words → chapter number
_ORDINALS = {
    'प्रथम': 1, 'द्वितीय': 2, 'तृतीय': 3, 'चतुर्थ': 4, 'पञ्चम': 5,
    'षष्ठ': 6, 'सप्तम': 7, 'अष्टम': 8, 'नवम': 9, 'दशम': 10,
    'एकादश': 11, 'द्वादश': 12, 'त्रयोदश': 13, 'चतुर्दश': 14, 'पञ्चदश': 15,
    'षोडश': 16, 'सप्तदश': 17, 'अष्टादश': 18, 'एकोनविंश': 19, 'विंश': 20,
}
_ORDINAL_RE = re.compile('|'.join(re.escape(k) for k in _ORDINALS))

# Matches the tail of chapter heading lines:
#   अध्याय N  /  अध्यायः N  /  ...अध्यायः (ordinal compound)  /  Chapter N
# Note: ordinal sandhi forms end in ध्यायः (avagraha elides the leading अ),
#       so we match both अध्याय and ध्याय as the stem.
_CH_NUMERIC_RE = re.compile(r'अध्याय[ः\s]*([०-९\d]+)|chapter\s+(\d+)', re.IGNORECASE)
_CH_ORDINAL_RE = re.compile(r'ध्यायः?\s*$')   # line ending with dhyāya(ḥ)


def _parse_chapter_heading(line: str) -> tuple[int | None, str]:
    """
    Try to extract (chapter_number, title) from a single line.
    Returns (None, '') if the line is not a chapter heading.
    """
    stripped = line.strip()
    # Ignore shloka markers and blank lines
    if not stripped or '॥' in stripped:
        return None, ''

    # Case 1: numeric form — अध्याय 5 / Chapter 5
    m = _CH_NUMERIC_RE.search(stripped)
    if m:
        raw = m.group(1) or m.group(2)
        return int(devanagari_to_int(raw)), stripped

    # Case 2: ordinal form — प्रथमोऽध्यायः / द्वितीयोऽध्यायः
    if _CH_ORDINAL_RE.search(stripped):
        m2 = _ORDINAL_RE.search(stripped)
        if m2:
            num = _ORDINALS.get(m2.group(0))
            if num:
                return num, stripped

    return None, ''


def devanagari_to_int(s: str) -> str:
    """Convert Devanagari numeral string to ASCII, keeping '/' and suffix chars."""
    table = str.maketrans('०१२३४५६७८९', '0123456789')
    return s.translate(table)


def split_into_shlokas(text: str) -> list[dict]:
    """
    Split raw Devanagari text into shloka dicts using ॥N॥ markers.
    Returns list of {number: str|int, text: str}.
    """
    shlokas = []
    # Split on shloka-end markers, keeping the marker in the left chunk
    parts = SHLOKA_END_RE.split(text)
    # parts alternates: [pre-shloka-1, shloka-num-1, pre-shloka-2, shloka-num-2, ...]
    i = 0
    while i < len(parts) - 1:
        body = parts[i].strip()
        num_raw = parts[i + 1]
        num = devanagari_to_int(num_raw.strip())
        if body:
            # Try to convert to int; keep as string for sub-shlokas like "1/2"
            try:
                num_val = int(num)
            except ValueError:
                num_val = num
            shlokas.append({"number": num_val, "text": body})
        i += 2
    return shlokas


def parse_chapters_from_text(raw: str, text_id: str, title_sa: str, title_en: str, category: str) -> dict:
    """
    Parse multi-chapter text into the corpus schema.
    Chapters are detected by common Sanskrit heading patterns.
    """
    # Scan line by line for chapter headings
    lines = raw.splitlines(keepends=True)
    chapter_starts: list[tuple[int, int, str]] = []  # (line_idx, ch_num, title)
    for i, line in enumerate(lines):
        ch_num, title = _parse_chapter_heading(line)
        if ch_num is not None:
            chapter_starts.append((i, ch_num, title))

    if not chapter_starts:
        # Treat the whole text as a single chapter
        shlokas = split_into_shlokas(raw)
        return build_doc(text_id, title_sa, title_en, category, [
            {"number": 1, "title": title_en, "shlokas": shlokas}
        ])

    chapters = []
    for idx, (line_idx, ch_num, ch_title) in enumerate(chapter_starts):
        # Chapter body starts on the line AFTER the heading
        body_start_line = line_idx + 1
        body_end_line = chapter_starts[idx + 1][0] if idx + 1 < len(chapter_starts) else len(lines)
        ch_text = "".join(lines[body_start_line:body_end_line])
        shlokas = split_into_shlokas(ch_text)
        chapters.append({
            "number": ch_num,
            "title": ch_title or f"अध्यायः {ch_num}",
            "shlokas": shlokas,
        })

    return build_doc(text_id, title_sa, title_en, category, chapters)


def build_doc(text_id, title_sa, title_en, category, chapters):
    """Attach schema fields and mark all shlokas untranslated."""
    for ch in chapters:
        for s in ch["shlokas"]:
            s.setdefault("english", "")
            s.setdefault("hindi", "")
            s.setdefault("status", "untranslated")
    return {
        "text_id": text_id,
        "title_sa": title_sa,
        "title_en": title_en,
        "category": category,
        "chapters": chapters,
    }


# ── Source readers ──────────────────────────────────────────────────────────

def read_text_file(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_pdf_text(path: Path) -> str:
    """Extract text layer from a Unicode PDF using pymupdf (fitz)."""
    try:
        import fitz  # pymupdf
    except ImportError:
        sys.exit("pymupdf not installed. Run: pip install pymupdf")
    doc = fitz.open(str(path))
    pages = [page.get_text() for page in doc]
    return "\n".join(pages)


def read_pdf_ocr_vision(path: Path) -> str:
    """OCR a scanned PDF using Google Vision API. Requires GOOGLE_APPLICATION_CREDENTIALS."""
    try:
        import fitz
        from google.cloud import vision
        from PIL import Image
        import io
    except ImportError:
        sys.exit("Missing deps. Run: pip install pymupdf google-cloud-vision pillow")

    client = vision.ImageAnnotatorClient()
    doc = fitz.open(str(path))
    all_text = []

    for page_num, page in enumerate(doc, 1):
        # Render page at 300 DPI
        mat = fitz.Matrix(300 / 72, 300 / 72)
        pix = page.get_pixmap(matrix=mat)
        img_bytes = pix.tobytes("png")

        image = vision.Image(content=img_bytes)
        response = client.document_text_detection(image=image)

        if response.error.message:
            print(f"  Warning page {page_num}: {response.error.message}", file=sys.stderr)
        else:
            all_text.append(response.full_text_annotation.text)
            print(f"  OCR'd page {page_num}/{len(doc)}", file=sys.stderr)

    return "\n".join(all_text)


# ── Per-chapter output mode ─────────────────────────────────────────────────

def write_per_chapter(doc: dict, output_dir: Path, text_id: str):
    """Write one JSON file per chapter, matching BrihatJataka/chapters/ convention."""
    output_dir.mkdir(parents=True, exist_ok=True)
    prefix = text_id.replace("_", "")[:8]  # e.g. "saravali" -> "saraval"
    for ch in doc["chapters"]:
        ch_num = ch["number"]
        filename = f"{prefix}_ch{ch_num:02d}.json"
        single = {
            "text_id": doc["text_id"],
            "title_sa": doc["title_sa"],
            "title_en": doc["title_en"],
            "category": doc["category"],
            "chapters": [ch],
        }
        out_path = output_dir / filename
        out_path.write_text(json.dumps(single, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  wrote {out_path} ({len(ch['shlokas'])} shlokas)")


# ── CLI ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Parse raw Sanskrit source into corpus JSON schema."
    )
    parser.add_argument("source", help="Source file (.md, .txt, or .pdf)")
    parser.add_argument("--text-id", required=True, help="Machine-readable slug, e.g. saravali")
    parser.add_argument("--title-sa", default="", help="Sanskrit title in Devanagari")
    parser.add_argument("--title-en", required=True, help="English title")
    parser.add_argument("--category", default="hora",
                        choices=["hora", "samhita", "vedanga_jyotisha", "siddhanta",
                                 "nadi", "jaimini", "parashari", "prashna"],
                        help="Text category")
    parser.add_argument("--pdf", action="store_true",
                        help="Source is a PDF (text-layer extraction)")
    parser.add_argument("--ocr-backend", choices=["vision"], default=None,
                        help="Use Google Vision OCR for scanned PDFs")
    parser.add_argument("--output", "-o", help="Output JSON path (single file)")
    parser.add_argument("--per-chapter", action="store_true",
                        help="Write one JSON per chapter (like BrihatJataka/chapters/)")
    parser.add_argument("--output-dir", help="Directory for per-chapter output")
    args = parser.parse_args()

    source = Path(args.source)
    if not source.exists():
        sys.exit(f"Source not found: {source}")

    print(f"Reading {source}...", file=sys.stderr)
    if args.pdf or source.suffix.lower() == ".pdf":
        if args.ocr_backend == "vision":
            raw = read_pdf_ocr_vision(source)
        else:
            raw = read_pdf_text(source)
    else:
        raw = read_text_file(source)

    print(f"Parsing shlokas...", file=sys.stderr)
    doc = parse_chapters_from_text(
        raw, args.text_id, args.title_sa, args.title_en, args.category
    )

    total = sum(len(ch["shlokas"]) for ch in doc["chapters"])
    print(f"Found {len(doc['chapters'])} chapter(s), {total} shloka(s)", file=sys.stderr)

    if args.per_chapter:
        out_dir = Path(args.output_dir) if args.output_dir else source.parent / "chapters"
        write_per_chapter(doc, out_dir, args.text_id)
    else:
        out_path = Path(args.output) if args.output else source.with_suffix(".json")
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Written to {out_path}")


if __name__ == "__main__":
    main()
