# Translation contract — for any agent writing into this corpus

**Read this before writing a single byte.** It is self-contained; you do not need the rest of
the repo's history to follow it.

On 2026-09-14 a translation run corrupted **7 of 66 corpus files** and put 448 translated verses
at risk. Every rule below exists because something specific went wrong. The failures are named,
so you can check you are not repeating them.

---

## 0 · The one rule that caused all the damage

> **Parse the JSON. Mutate the object. Serialise it back. Never edit the file as text.**

```python
import json
from pathlib import Path

p = Path("Upaveda/Ayurveda/CarakaSamhita/CarakaSamhita.json")
doc = json.loads(p.read_text(encoding="utf-8"))     # PARSE

for ch in doc["chapters"]:                           # MUTATE THE OBJECT
    for sh in ch["shlokas"]:
        if sh.get("status") == "untranslated":
            sh["english_draft"] = translate(sh["text"])   # DRAFT, not `english` — see §2
            sh["status"] = "drafted"

p.write_text(                                        # SERIALISE, ONCE
    json.dumps(doc, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
```

**`ensure_ascii=False` and `encoding="utf-8"` are both mandatory.** Omitting the encoding is what
produced `à¤°à¤¾à¤—à¤¾à¤¦à¤¿` where `रागादि` belongs.

### What text-splicing actually did, so you can recognise it

| symptom | what it looked like | cause |
|---|---|---|
| `}` immediately followed by `},` | doubled closing brace | spliced an object without removing the old one |
| `"hindi":` followed directly by `,` | missing value | wrote a key with no value |
| `},` followed by `"number"` | missing `{` | opened an object without its brace |
| a 3-byte Devanāgarī character cut in half | `\xe0\xa4` then whitespace | sliced a string by BYTE offset instead of by character |
| `à¤°à¤¾à¤—à¤¾à¤¦à¤¿` | every character six bytes instead of three | read UTF-8 as latin-1, re-encoded as UTF-8 |

**Never seek to a byte offset in these files. Never regex-replace inside them. Never append.**

---

## 1 · The schema — every file, no exceptions

```json
{
  "text_id": "caraka_samhita",
  "title_sa": "चरकसंहिता",
  "title_en": "Caraka Samhita",
  "category": "upaveda_ayurveda",
  "chapters": [
    {
      "number": 1,
      "title": "…",
      "shlokas": [
        {
          "number": 1,
          "text": "Devanāgarī, \\n between pādas",
          "english": "English translation",
          "hindi": "Hindi translation",
          "status": "translated"
        }
      ]
    }
  ]
}
```

**`status` values and what each means:**

| value | meaning |
|---|---|
| `translated` | **both** `english` and `hindi` are present and human-verified |
| `partial` | exactly one of the two is present |
| `untranslated` | neither |
| `drafted` | a machine draft exists in `english_draft` / `hindi_draft` and **has not been verified** |

### The single most common mistake, measured: `translated` when only English is present

**`translated` means BOTH `english` AND `hindi` are present.** English alone is **`partial`**.

The 2026-09-14 run set `status: "translated"` on **1,620 verses across 20 texts** while leaving
`hindi` empty. The English in them is real and good — this is a one-word label error, not bad
work — but the validator rejects every one of them with *"status asserts a translation that is
not there"*, and downstream anything filtering on `translated` would serve a half-translated
verse as complete.

```python
has_en = bool(sh.get("english", "").strip())
has_hi = bool(sh.get("hindi", "").strip())
sh["status"] = "translated" if (has_en and has_hi) else "partial" if (has_en or has_hi) else "untranslated"
```

**Derive the status from the content. Never set it by hand.**

**Do not add fields.** Specifically never re-add `source`, `header`, `book`, `english_meaning`,
`hindi_meaning`, `source_file`, `source_chunk`, `is_duplicate` — these are pre-normalisation
artifacts and a validator rejects them.

---

## 2 · The publication gate — the rule with the highest cost if broken

**A machine-produced translation goes in `english_draft` / `hindi_draft`. NEVER in `english` /
`hindi`.**

`english` and `hindi` are **served to the public API verbatim**. The consuming service returns
the document wholesale and filters on nothing. The only thing standing between a machine draft
and a public astrology site is that the drafts live in fields the seeder does not copy.

The project's hard rule is: **"Computation is AI-assisted; meaning is not."** A machine may draft
a translation. A machine may not publish one.

```python
sh["english_draft"] = machine_output      # correct
sh["status"] = "drafted"

sh["english"] = machine_output            # WRONG — this publishes it
```

**`status` is a label, not a gate.** Nothing filters on it. Putting machine text in `english` and
setting `status: "drafted"` still publishes it.

---

## 3 · Never renumber. Ever.

`chapter.number` and `shloka.number` are **live citations**. Code elsewhere references
`(text_id, chapter, shloka)` triples. Changing a number silently breaks every reference to that
verse, with no error anywhere.

- If numbering looks wrong, **report it — do not fix it.**
- If two verses share a number, **report it — do not renumber one.** A duplicate
  `(chapter, number)` means one of them silently never reaches the database, which is a real
  defect, but renumbering trades a detectable problem for an undetectable one.
- `number` is usually an integer but is **legitimately a string** in places: `"1/2"` for a half
  shloka, `"63अ"` for a sub-divided chapter, `"1.1"` / `"praśna.khaṇḍa.sūtra"` for depth-3 texts.
  **Do not "normalise" these to integers.** 60% of the corpus uses compound keys.

---

## 4 · Never invent. Record absences.

If the Sanskrit is illegible, missing, or you cannot translate it with confidence:

- **Leave `english` empty and `status: "untranslated"`.** That is a true statement.
- **Do not guess.** Do not paraphrase the surrounding verses. Do not produce a summary.

**Do not write a placeholder that looks like a translation.** A prior run left 178 verses reading
`Chapter 21, Shloka 11 - Description of the subtle effects of planetary sub-sub-periods…` with
`status: "translated"`. Those are not translations; they are now a defect that has to be found
and undone, and every automated check passed on them.

The standard to copy: one text has **46 sūtras absent from its source OCR, recorded as absent**.
That is the correct behaviour.

---

## 5 · Three different jobs. Know which one you are doing.

| job | how to spot it | what to do |
|---|---|---|
| **Translate** | `status: "untranslated"`, `english` empty | Write the draft to `english_draft`, set `status: "drafted"` |
| **Verify a draft** | `status: "drafted"`, `english_draft` populated | Read the Sanskrit. Correct the draft. **Promote** it to `english`, set `status`, **clear** the draft field. Never copy across unread |
| **Re-translate a stub** | `status: "translated"` but `english` is a generated template | You are **replacing** text, not filling a blank. Do not skip these as done |

---

## 6 · Verify before you hand back — and report the output

```sh
cd "<repo root>"                       # both scripts resolve paths relative to cwd

# every file parses, and the registry agrees with the corpus
python3 scripts/check_inventory.py ; echo "EXIT=$?"

# schema, status values, banned fields, key distinctness, the draft gate
python3 ../astroacharya/scripts/validate_corpus.py --path .   # --path IS REQUIRED, else exit 2
```

**`check_inventory.py` exit codes:** `0` clean · `1` the registry disagrees with the corpus ·
`2` could not run. **A non-zero exit because you changed a verse count is expected** — report the
new counts; do not edit `docs/INVENTORY.md` yourself.

**And check the thing neither script checks:**

```python
# every file is still valid UTF-8 and still parses — the failure that happened
import glob, json
for p in glob.glob("**/*.json", recursive=True):
    if p.startswith("docs/"): continue
    json.loads(open(p, encoding="utf-8").read())   # raises on both failure modes
```

**Assert the verse count is unchanged.** A translation job fills fields; it must not change how
many shlokas exist. If your run changes a total, you have duplicated or dropped data.

---

## 7 · Do not touch these

- **`Hora/Parashari/Jatakaparijatah/Jatakaparijatah.json`** and
  **`Hora/Parashari/Saravali/Saravali.json`** — both are fully translated already, and both are
  scheduled for a re-keying that will move their verse numbers. Work inside them will be lost.
- **Any file you did not open in this run.** Write only what you touched.

---

## 8 · Scope

**Work one text at a time. Write it. Verify it. Then move on.** A run that opens 29 files and
writes them all at the end has 29 files to lose when it fails — which is exactly what happened.

Report, per text: the text_id, how many verses you changed, the before and after counts by
`status`, and the verification output. If you skipped verses, say how many and why.
