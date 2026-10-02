# Handover 2 to Antigravity — translate 103 `garga_hora` verses (2026-10-02)

**Run every command from the repo root:**
`cd "$HOME/Documents/GitHub/Vipin Kaushik/sanskrit-texts"`.

**Read the rules first.** They are §"The rules" and §"Before handing back" of
[`2026-10-02-antigravity-handover.md`](./2026-10-02-antigravity-handover.md). This file does not
restate them, and it adds one rule of its own (below). The first run followed them exactly; do the same.

## The task

103 verses of `garga_hora` — nearly all of chapter 3, the planet-by-house results — served English
and Hindi that were **not translations**: one generated sentence, *"Placement of <planet> in the
<N>th house: According to Garga Hora, when <planet> occupies the <N>th house, it produces specific
results regarding physical health, wealth, courage…"*, with the planet and house filled in **by
position**. It is now in `english_draft` / `hindi_draft` and is to be **replaced**, not edited.

Derive the list — do not trust the count above:

```sh
python3 - <<'PY'
import json, pathlib, sys
GEN = "it produces specific results regarding physical health"
d = json.loads(pathlib.Path("Hora/Parashari/GargaHora/GargaHora.json").read_text(encoding="utf-8"))
rows = [(c["number"], s["number"]) for c in d["chapters"] for s in c["shlokas"]
        if not (s.get("english") or "").strip() and GEN in (s.get("english_draft") or "")]
if len(rows) < 90:
    sys.exit(f"only {len(rows)} verses found -- the scan has gone blind, it has not found nothing")
for ch, n in rows:
    print(f"garga_hora\t{ch}\t{n}")
print(f"{len(rows)} verses", file=sys.stderr)
PY
```

Expected today: **103**. Once all are done the same command is EXPECTED to refuse with
`only 0 verses found` — that is the success signal.

## The rule specific to this text

**Take the planet AND the house from the verse's Sanskrit, never from its position or its number.**
The filler got the house wrong in most verses precisely because it counted: 3.3 is
`धनभावगते सूर्ये` — the Sun in the **2nd** (dhana) — and the filler called it the 3rd. House words
in this text: तनु/लग्न 1 · धन 2 · सहज/विक्रम/भ्रातृ 3 · बन्धु/सुख 4 · सुत/पुत्र/पञ्चम 5 · रिपु/शत्रु/षष्ठ 6 ·
जाया/युवति/सप्तम/कलत्र 7 · मृत्यु/रन्ध्र/निधन/अष्टम 8 · धर्म/भाग्य/नवम 9 · कर्म/मान/मेषूरण/दशम 10 ·
लाभ/आय 11 · व्यय 12. A verse that is an introduction or a general rule (e.g. 3.1) names no house —
translate what it says.

Much of this chapter's OCR is damaged. Where a phrase is unreadable, translate what is legible and
mark the gap `[illegible]`; never fill it with a plausible guess. **Never write a sentence about
"specific results regarding health, wealth, courage…"** — that is the output being replaced.

Also: 3.130 no longer exists (it was Hindi commentary, removed). 3.129 → 3.131 is correct.
