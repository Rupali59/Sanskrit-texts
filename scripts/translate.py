#!/usr/bin/env python3
"""
translate.py — Fill English + Hindi translations into corpus JSON via Claude API.

Works on any JSON file (or directory of JSONs) that has shlokas with
status="untranslated" or status="partial". Processes one chapter per API call
so Claude has neighboring-shloka context. Saves progress after each chapter so
the script is safe to interrupt and resume.

Usage:
  # Single file
  python scripts/translate.py Hora/Saravali/saravali.json

  # All files in a directory
  python scripts/translate.py Hora/Saravali/chapters/

  # Specific chapter only (useful for spot-checking)
  python scripts/translate.py Hora/Saravali/saravali.json --chapter 3

  # Dry run (show what would be sent, don't call the API)
  python scripts/translate.py Hora/Saravali/saravali.json --dry-run

  # Use a different model (default: claude-opus-4-8 for quality; use haiku for speed)
  python scripts/translate.py Hora/Saravali/saravali.json --model claude-haiku-4-5-20251001

Requirements:
  pip install anthropic
  export ANTHROPIC_API_KEY=sk-ant-...
"""

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path


# ── Few-shot example (from BPHS ch1 to anchor the register) ────────────────

FEW_SHOT_EXAMPLE = """Example (from Brihat Parashara Hora Shastra):
Shloka: ऋषयः ऊचुः त्वत्तः शास्त्रमिदं ब्रह्मन् श्रुतं विस्तरशोऽखिलम् ।
       संग्रहेण पुनर्वक्तुमर्हस्यस्मत्कृते द्विज ॥
English: The sages said: O Brahmin, we have heard this scripture from you in full detail.
         Please narrate it again to us in brief, O twice-born.
Hindi: ऋषियों ने कहा: हे ब्राह्मण! यह शास्त्र हमने आपसे विस्तारपूर्वक सुना है।
      हे द्विज! कृपया हमारे लिए इसे संक्षेप में पुनः कहें।"""


SYSTEM_PROMPT = """You are an expert Sanskrit scholar specializing in Vedic Jyotisha (astrology).
You produce accurate, scholarly translations of classical Sanskrit shlokas into English and Hindi.

Rules:
- Preserve technical astrological terminology: graha names (Surya, Chandra, Mangal, Budha,
  Guru, Shukra, Shani, Rahu, Ketu), rashi names, nakshatra names, bhava (house) terms,
  yoga names, and Jyotisha concepts. Use the Sanskrit term if no standard English equivalent exists.
- English: formal but readable scholarly prose. No archaic "thee/thou".
- Hindi: classical literary Hindi (not colloquial). Use Sanskrit loanwords where appropriate.
- Maintain the meaning precisely — this is a scholarly corpus, not a paraphrase.
- Do NOT add interpretations, commentary, or modern psychological framing.

{few_shot}

You will receive a JSON array of shlokas and must return a JSON array of the same length,
where each element adds "english" and "hindi" translation fields."""


USER_PROMPT_TEMPLATE = """{context_line}

Translate these {n} shlokas. Return ONLY a JSON array with this structure:
[
  {{"number": <same as input>, "english": "<translation>", "hindi": "<translation>"}},
  ...
]

Shlokas:
{shlokas_json}"""


# ── API helpers ─────────────────────────────────────────────────────────────

def get_client():
    try:
        import anthropic
    except ImportError:
        sys.exit("anthropic not installed. Run: pip install anthropic")
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        sys.exit("ANTHROPIC_API_KEY environment variable not set.")
    return anthropic.Anthropic(api_key=api_key)


def extract_json(text: str) -> list:
    """Extract JSON array from Claude response, tolerating markdown fences."""
    # Try bare parse first
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    # Strip markdown fences
    fence_match = re.search(r'```(?:json)?\s*(\[.*?\])\s*```', text, re.DOTALL)
    if fence_match:
        return json.loads(fence_match.group(1))
    # Find first [ ... ] block
    bracket_match = re.search(r'\[.*\]', text, re.DOTALL)
    if bracket_match:
        return json.loads(bracket_match.group(0))
    raise ValueError(f"No JSON array found in response:\n{text[:500]}")


def translate_chapter(client, chapter: dict, text_meta: dict, model: str, dry_run: bool) -> int:
    """Translate all untranslated shlokas in a chapter. Returns count translated."""
    to_translate = [
        s for s in chapter["shlokas"]
        if s.get("status") in ("untranslated", "partial", "") or not s.get("english")
    ]
    if not to_translate:
        return 0

    context_line = (
        f"Text: {text_meta['title_en']} (text_id={text_meta['text_id']}), "
        f"Chapter {chapter['number']}: {chapter.get('title', '')}"
    )

    shlokas_input = [
        {"number": s["number"], "text": s["text"]}
        for s in to_translate
    ]

    user_content = USER_PROMPT_TEMPLATE.format(
        context_line=context_line,
        n=len(shlokas_input),
        shlokas_json=json.dumps(shlokas_input, ensure_ascii=False, indent=2),
    )

    if dry_run:
        print(f"\n  [DRY RUN] Would translate {len(to_translate)} shlokas in ch {chapter['number']}")
        print(f"  First shloka: {shlokas_input[0]['text'][:80]}...")
        return 0

    system = SYSTEM_PROMPT.format(few_shot=FEW_SHOT_EXAMPLE)
    max_retries = 3
    for attempt in range(1, max_retries + 1):
        try:
            response = client.messages.create(
                model=model,
                max_tokens=8192,
                system=system,
                messages=[{"role": "user", "content": user_content}],
            )
            raw = response.content[0].text
            translations = extract_json(raw)
            break
        except Exception as e:
            if attempt == max_retries:
                print(f"  ERROR after {max_retries} attempts: {e}", file=sys.stderr)
                return 0
            wait = 2 ** attempt
            print(f"  Retry {attempt}/{max_retries} after {wait}s: {e}", file=sys.stderr)
            time.sleep(wait)

    # Apply translations back to the shloka list
    trans_by_num = {str(t["number"]): t for t in translations}
    count = 0
    for shloka in chapter["shlokas"]:
        key = str(shloka["number"])
        if key in trans_by_num:
            t = trans_by_num[key]
            shloka["english"] = t.get("english", shloka.get("english", ""))
            shloka["hindi"] = t.get("hindi", shloka.get("hindi", ""))
            if shloka["english"] and shloka["hindi"]:
                shloka["status"] = "translated"
            elif shloka["english"] or shloka["hindi"]:
                shloka["status"] = "partial"
            count += 1

    return count


# ── Progress tracking ───────────────────────────────────────────────────────

def load_progress(json_path: Path) -> set:
    """Return set of chapter numbers already completed."""
    progress_path = json_path.with_suffix(".progress")
    if progress_path.exists():
        return set(json.loads(progress_path.read_text()))
    return set()


def save_progress(json_path: Path, done_chapters: set):
    progress_path = json_path.with_suffix(".progress")
    progress_path.write_text(json.dumps(sorted(done_chapters)))


def clear_progress(json_path: Path):
    progress_path = json_path.with_suffix(".progress")
    if progress_path.exists():
        progress_path.unlink()


# ── File processor ──────────────────────────────────────────────────────────

def process_file(json_path: Path, client, model: str, chapter_filter: int | None,
                 dry_run: bool, force: bool):
    print(f"\n{'='*60}")
    print(f"Processing: {json_path}")

    doc = json.loads(json_path.read_text(encoding="utf-8"))
    text_meta = {k: doc[k] for k in ("text_id", "title_en", "title_sa", "category")}

    done_chapters = set() if force else load_progress(json_path)
    total_translated = 0

    for ch in doc["chapters"]:
        ch_num = ch["number"]

        if chapter_filter is not None and ch_num != chapter_filter:
            continue

        if ch_num in done_chapters:
            print(f"  Chapter {ch_num}: already done (skip)")
            continue

        untranslated_count = sum(
            1 for s in ch["shlokas"]
            if s.get("status") in ("untranslated", "partial", "") or not s.get("english")
        )
        if untranslated_count == 0:
            print(f"  Chapter {ch_num}: fully translated (skip)")
            done_chapters.add(ch_num)
            continue

        print(f"  Chapter {ch_num}: {untranslated_count} shlokas to translate...", end="", flush=True)
        n = translate_chapter(client, ch, text_meta, model, dry_run)
        print(f" done ({n} translated)")
        total_translated += n

        if not dry_run:
            done_chapters.add(ch_num)
            # Write JSON after each chapter so progress is never lost
            json_path.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
            save_progress(json_path, done_chapters)

        # Polite pause to avoid rate limit bursts
        if not dry_run and len(doc["chapters"]) > 1:
            time.sleep(1)

    if not dry_run:
        clear_progress(json_path)

    untranslated_remaining = sum(
        1 for ch in doc["chapters"]
        for s in ch["shlokas"]
        if s.get("status") != "translated"
    )
    print(f"  Summary: {total_translated} translated this run, {untranslated_remaining} remaining")


# ── CLI ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Translate Sanskrit corpus shlokas via Claude API.")
    parser.add_argument("target", help="JSON file or directory of JSON files")
    parser.add_argument("--chapter", type=int, default=None,
                        help="Translate only this chapter number")
    parser.add_argument("--model", default="claude-opus-4-8",
                        help="Claude model ID (default: claude-opus-4-8 for quality; "
                             "use claude-haiku-4-5-20251001 for speed)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be translated without calling the API")
    parser.add_argument("--force", action="store_true",
                        help="Re-translate even chapters already marked done")
    args = parser.parse_args()

    target = Path(args.target)
    client = None if args.dry_run else get_client()

    if target.is_dir():
        files = sorted(target.glob("**/*.json"))
        if not files:
            sys.exit(f"No JSON files found in {target}")
        for f in files:
            process_file(f, client, args.model, args.chapter, args.dry_run, args.force)
    elif target.is_file():
        process_file(target, client, args.model, args.chapter, args.dry_run, args.force)
    else:
        sys.exit(f"Not found: {target}")

    print("\nDone.")


if __name__ == "__main__":
    main()
