# Handover 3 to Antigravity — retranslate 890 `bphs` verses (2026-10-02)

**Run every command from the repo root:**
`cd "$HOME/Documents/GitHub/Vipin Kaushik/sanskrit-texts"`.

**Read the rules first.** They are §"The rules" and §"Before handing back" of
[`2026-10-02-antigravity-handover.md`](./2026-10-02-antigravity-handover.md). This file does not
restate them, and it adds rules of its own (below).

## The task

890 verses of `bphs` (Bṛhat Parāśara Horā Śāstra) were serving English and Hindi that did not
translate the verse. Every verse in the 28 suspect chapters was read against its Sanskrit, and only
the wrong ones were moved: the old English/Hindi now sits in `english_draft` / `hindi_draft`, and the
served fields are empty. The good verses around them were left served, so most chapters are a mix.

The old drafts are **not a starting point**. Three kinds of failure were found, and all three
read as fluent English:

- **Invented content.** Most of ch. 62–66, 70, 72–80 and 82 is generic or modern astrology
  ("cinema", "digital fields", "investigative journalism", bindu bands of 20/30/40) that the verse
  does not say.
- **Shifted by one.** 78.6–78.9 and 87.1–87.3 carry their neighbour's meaning.
- **Truncated.** 80.10 drops its second half (the Mercury-sign triṃśāṃśas).

So: **translate each verse from its `text` alone.** Read the old draft only to delete it.

Derive the list — do not trust the count above:

```sh
python3 - <<'PY'
import json, pathlib, sys
p = pathlib.Path("Hora/Parashari/BrihatParasharaHoraShastra/BrihatParasharaHoraShastra.json")
d = json.loads(p.read_text(encoding="utf-8"))
rows = [(c["number"], s["number"]) for c in d["chapters"] for s in c["shlokas"]
        if not (s.get("english") or "").strip() and (s.get("english_draft") or "").strip()]
if len(rows) < 800:
    sys.exit(f"only {len(rows)} verses found -- the scan has gone blind, it has not found nothing")
for ch, n in rows:
    print(f"bphs\t{ch}\t{n}")
print(f"{len(rows)} verses", file=sys.stderr)
PY
```

Expected today: **890**. The floor is 800, so the command will refuse once most of the work is done.
That is expected. Lower the floor in your copy as you go and report the final count.

## Rules specific to this text

1. **Numbers come from the verse.** Chapters 66–73 are tables (bindu positions, multipliers, ray
   counts, remedies by bindu total). Every house number, count and multiplier in your English must
   be one the Sanskrit states. Number words used here include सप्तभिः 7, अष्टभिः 8, दशभिः 10,
   रुद्र 11, विश्व 13, तिथि 15, and compound forms like वेदाश्विभिः 24 or अङ्केन्दुभिः 19 (read
   right to left). If you cannot decode a number, write `[number unclear]`. Never insert a
   plausible value.
2. **Several verses only make sense as a pair.** Ch. 66 and 68 run one rule across verse
   boundaries. Translate what each verse says, and let the sentence end where the verse ends.
   Do not move clauses between verses to make each one read complete. That is how the
   shifted-by-one failure happened.
3. **Labels are strings.** Some chapters carry labels like `12अ`. Keep them exactly as they are.
4. **4.15** carried the line *"(wait, let me check the varna in 15)"*. Nothing like it may appear in
   your output.
5. **Do not touch any served verse.** If a neighbour that is still served looks wrong to you, list
   it in your report. Do not edit it.

Promotion is not yours to do. Write your translations into `english_draft` / `hindi_draft`,
replacing the old text, and hand back. They are reviewed and promoted from there.
