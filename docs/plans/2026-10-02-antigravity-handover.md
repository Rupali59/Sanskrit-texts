# Handover to Antigravity — translate 131 verses (2026-10-02)

**Every command below runs from the repo root:**
`cd "$HOME/Documents/GitHub/Vipin Kaushik/sanskrit-texts"`. The background on why these verses need
work is in `docs/TRANSLATION_BACKLOG.md` §"Measured after the 2026-09-28/29 runs"; this file is the
task.

## The task

Write a real, verse-specific English and Hindi translation for each of **131 verses** in four texts:

| text | verses | why they need translating |
|---|---:|---|
| `astanga_sangraha` | 50 | their old "translation" was one sentence pasted over a run of different verses |
| `garga_hora` | 48 | same — e.g. 3.106–3.118 all said "Placement of Saturn in the 12th house…" |
| `astanga_hridaya` | 26 | a template ("Specific Ayurvedic therapeutic principles … involving <words>") |
| `brihadaranyaka_upanishad` | 7 | 1.5.3, 1.5.6, 1.5.21, 1.5.22, 1.5.23, 4.5.6 have no translation anywhere; 4.5.13's draft is a different verse's |

**Do not trust that table — derive the list.** It prints one `text_id <TAB> chapter <TAB> number` per verse
and refuses to print a short list:

```sh
python3 - <<'PY'
import json, sys, pathlib
sys.path.insert(0, ".")
from sanskrit_texts.translation_status import check_text
TEXTS = {"garga_hora", "astanga_sangraha", "astanga_hridaya", "brihadaranyaka_upanishad"}
SKIP = {("brihadaranyaka_upanishad", 2, "4.5")}       # being handled in review, not by this run
EXTRA = {("brihadaranyaka_upanishad", 4, "5.13")}     # draft is the wrong verse's translation
rows = []
for p in sorted(pathlib.Path(".").rglob("*.json")):
    if any(part.startswith(".") or part == "docs" for part in p.parts):
        continue
    d = json.loads(p.read_text(encoding="utf-8"))
    if d.get("text_id") not in TEXTS:
        continue
    shl = [(c["number"], s) for c in d["chapters"] for s in c["shlokas"]]
    for (ch, s), v in zip(shl, check_text(d).verses):
        key = (d["text_id"], ch, str(s["number"]))
        blank = not (s.get("english") or "").strip()
        label = bool(v.draft_defects & {"en:label-only", "en:sanskrit-echo", "en:template-prefix"})
        if key in EXTRA or (blank and key not in SKIP and (label or not s.get("english_draft"))):
            rows.append(key)
if len(rows) < 100:
    sys.exit(f"only {len(rows)} verses found -- the scan has gone blind, it has not found nothing")
for t, ch, n in rows:
    print(f"{t}\t{ch}\t{n}")
print(f"{len(rows)} verses", file=sys.stderr)
PY
```

Expected today: **131 verses**. If you get a different number, stop and report it — do not adjust the
script to match this file.

**Excluded on purpose:** `brihadaranyaka_upanishad` 2.4.5. Its translation was found inside 2.4.4's
draft, split out, reviewed and promoted on 2026-10-02 — it is served now. Do not touch it, or any other
served Bṛhadāraṇyaka verse: 34 were reviewed and promoted the same day.

## The rules — each one was broken by a previous run and cost something

1. **Join on `(text_id, chapter, number)`, and read the verse's own `text` before writing.** Never on
   the number alone, never by position. Bṛhadāraṇyaka's 1.5, 2.4 and 4.5 served their neighbours'
   translations for a month because a run laid translations on by position (G72). Before writing each
   translation, confirm it translates *that* verse's Sanskrit.
2. **One verse, one translation. Never summarise a run of verses into one sentence.** That is exactly
   the defect being repaired here. Repeated wording is fine only where the Sanskrit itself repeats.
3. **Write to `english_draft` and `hindi_draft` only.** Never to `english` / `hindi` — those are
   served, and a human promotes. The 124 Āyurveda / Garga verses already hold a label in their drafts:
   **replace it** (it is not a translation). Do not touch any draft outside the 131.
4. **Leave `text` alone.** The Sanskrit is canonical and derived from `../sanskrit-texts-sources/`.
5. **Set each verse's `status` to `"drafted"`**, then re-derive the text-level `status` with
   `sanskrit_texts.reader.derive_text_status`.
6. **Write the file back in the repo's format:** `sanskrit_texts.export.serialize(doc)`
   (`ensure_ascii=False`, `indent=2`, insertion key order, trailing newline), and NFC-normalise
   every value you write.
7. **Never run a converter's `main()`** in `../scripts/sanskrit-convert/`: it rewrites the corpus file
   with every translation emptied (G65).
8. **Translate, do not interpret.** No commentary, no astrological or medical advice beyond what the
   verse says. Bracketed glosses of a Sanskrit term are fine; paragraphs of explanation are not.

## Before handing back — run all of these

```sh
git diff --stat -- '*.json'                   # exactly the 4 files above, nothing else
python3 scripts/check_inventory.py            # must print "registry matches the corpus"
python3 scripts/translation_backlog.py        # the 4 texts: ECHO and UNTR should fall to 0 for these verses
./.venv-corpus/bin/python -m pytest -q tests/test_translation_status.py tests/test_translation_alignment.py tests/test_translation_backlog.py
```

Then re-run the worklist command above. Once all 131 are done it is EXPECTED to refuse with
`only 1 verses found` — the one is 4.5.13, which the script names explicitly and so always lists.
Report that refusal; it is the success signal, not an error.

`tests/test_translation_alignment.py` fails if one English is served for two different verses. It
reads served fields, so it cannot see your drafts — **you** must check for repeated draft sentences:
`python3 scripts/translation_backlog.py` reports them under DRAFT vs ECHO.

## What to hand back

- The four changed JSON files, uncommitted.
- A list of any verse whose Sanskrit you could not translate confidently (corrupt OCR, unclear term),
  with the reason. Leave those verses' drafts empty rather than guessing.
- The output of the four commands above.

Rupali reviews and promotes. Nothing here goes to the served fields until she does.
