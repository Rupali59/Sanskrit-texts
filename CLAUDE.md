# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Parent context: `~/Documents/GitHub/Vipin Kaushik/CLAUDE.md`

## What this repo is

An open-source corpus of classical Sanskrit texts, digitized for computational access by AstroAcharya. **The JSON is still the source of truth**, and a modelled Postgres store now sits beside it — schema, importer, exporter and a structural publication gate, documented in [`docs/DATABASE.md`](./docs/DATABASE.md). This file said "not a code project, a data repository" until 2026-09-16; `make setup` then `make hello`. Source of truth for proofreading: [sanskritdocuments.org/sanskrit/jyotisha](https://sanskritdocuments.org/sanskrit/jyotisha/) (see `REFERENCES.md`).

**Scope: Jyotiṣa, plus everything that is not Tantra, Mantra, Brāhmaṇa, Āraṇyaka, Śikṣā or Kalpa.** Tantra, Mantra and Kalpa go to `Tushar/Youvan`; Brāhmaṇa and Āraṇyaka are Youvan's too and are **not** a backlog here. The Vedic **Saṃhitā and Upaniṣad layers** belong here. **The line is drawn by LAYER, not by containing work** — seven held Upaniṣads are textually chapters of a Brāhmaṇa or Āraṇyaka and stay, and the Āpastamba Dharmasūtra stays though it is a praśna of a Kalpasūtra, while the Āpastamba Paribhāṣāsūtra left 2026-09-02 because its genre is ritual procedure. Full rule and its history: `../CLAUDE.md` §"Content / texts ownership". `docs/VEDIC_CORPUS.md` maps all 51 Vedic texts; the registry says which are held.

AstroAcharya seeds this data into MongoDB and queries it via a `/texts` API. The `@source(("bphs", chapter, [shlokas]))` decorator in AstroAcharya references `text_id` values from this corpus.

## Layout

**One JSON per text, always** (standardised 2026-08-18). Sources are not in this repo.

```
<Category>/<School?>/<Text>/
    <Text>.json          the text — every chapter, every shloka — and nothing else

Veda/{rigveda,samaveda,atharvaveda,krishna-yajurveda,shukla-yajurveda}/   Upanishad/<veda>/
Hora/{Parashari,Nadi,Prashna,Jaimini}/   Siddhanta/   Samhita/   Muhurta/
Vedanga-Jyotisha/{Rigveda,Yajurveda}/    Dharmashastra/

docs/   INVENTORY.md (the manifest) · DECISIONS.md · BPHS_Master_Lexicon.md · …
```

**The top level carries TWO classification systems, and one word collides across them.**
`Hora/` · `Siddhanta/` · `Samhita/` · `Muhurta/` are the **Jyotiṣa** scheme, so `Samhita/` is
Varāhamihira's Bṛhat Saṃhitā; `Veda/` · `Upanishad/` are the **Vedic layer** scheme, and `Veda/`
holds the five Vedic Saṃhitās. `Vedanga-Jyotisha/` is a **third** axis, the six Vedāṅgas, and is
the only one still here now that `Kalpa/` has gone to Youvan.

**Sources live in `../sanskrit-texts-sources/`**, mirroring the same tree — Devanagari
`.wikitext`/`.html`/`.xml` fetches, transcriptions (`.md`), OCR (`.txt`), scans (`.pdf`) —
and it is a **superset**: it also holds Youvan's Brāhmaṇa/Āraṇyaka. This repo is the translation
layer: `.json` and nothing else. `.gitignore` enforces it; all prose lives in `docs/`.

**Every text is on the one-file rule as of 2026-09-02** — the last holdout, `ApastambaDharmaSutra`, was re-digitised by `scripts/sanskrit-convert/apastamba.py`.

**Acquisition state is a table, not a sentence.** [`docs/INVENTORY.md`](./docs/INVENTORY.md)
§"Acquisition status" gives every pursued text one row and one status — `HELD` · `SOURCED` ·
`REFUSED` · `UNSOURCED` · `LOST` — and `scripts/check_inventory.py` fails if that column and the
corpus disagree. Provenance and terms: [`docs/SOURCES.md`](./docs/SOURCES.md).

## Uniform JSON schema

Every `.json` file in this repo uses this schema — no exceptions:

```json
{
  "text_id": "bphs",
  "title_sa": "बृहत्पाराशरहोराशास्त्रम्",
  "title_en": "Brihat Parashara Hora Shastra",
  "category": "parashari",
  "chapters": [
    {
      "number": 1,
      "title": "सृष्टिक्रमकथनाध्यायः",
      "shlokas": [
        {
          "number": 1,
          "text": "Devanagari shloka, \\n between padas",
          "english": "English translation",
          "hindi": "Hindi translation",
          "status": "translated"
        }
      ]
    }
  ]
}
```

**Field notes:**
- `text_id` — machine-readable slug matching the `@source` decorator in AstroAcharya
- `category` — a plain string, **not** an enum, so the schema rejects nothing. The one thing that rejects a typo is `KNOWN_CATEGORIES` in `astroacharya/scripts/validate_corpus.py`, and **no hook or test here runs it** — so adding a category is a two-repo change, and a misspelt one goes silently invisible to every category filter while all counts stay green. **Do not restate the list here**: this bullet carried its own copy until 2026-09-14 and it had rotted to 10 of the 14 in use. **G51**.
- `status` — `"translated"` (both languages present) | `"partial"` (one language) | `"untranslated"` (neither) | `"drafted"` (machine-drafted, **not yet verified**)
- `english_draft` / `hindi_draft` — **optional, and the whole publication gate.** Machine-drafted
  translation lives here and **never** in `english`/`hindi`. Verification *promotes* a draft into
  the served field, flips `status` to `translated`, and clears the draft it consumed. The gate is
  **structural, not a flag** — nothing filters on `status`; `seed_texts.py`'s `_normalize_shloka`
  is an allowlist that cannot copy a draft field. **Never widen it.** The two innocuous-looking
  edits that publish every draft in the corpus, and the test pinning them: **G50**.
- `number` — integer for most shlokas/chapters; **string** for valid source sub-divisions: `"1/2"` for half-shlokas, and a Devanagari-suffixed chapter like `"63अ"` / `"63ब"` for a sub-divided chapter
- Files covering a single chapter still use the `chapters` array (one element) — uniform iteration in the seed script

**Do not add back** `source`, `header`, `book`, `english_meaning`, `hindi_meaning`, `source_file`, `source_chunk`, `is_duplicate` — these were pre-normalization artifacts.

## text_id registry

**[`docs/INVENTORY.md`](./docs/INVENTORY.md) is the registry**, and [`docs/README.md`](./docs/README.md) indexes every other doc (`plans/` and `archive/` as directories) — every text's `text_id`, path, chapter and shloka
counts, translation state and count-authority tier, in one table. **Per-text caveats are in
[`docs/CANONICAL_COUNTS.md`](./docs/CANONICAL_COUNTS.md)** §"Per-text caveats"; they were
inline here until 2026-08-24 and took this file 58 lines over its cap.

**Derive the totals, never restate them:** `python3 scripts/check_inventory.py` prints texts,
chapters, shlokas, categories and dedupe loss, and **exits 1 if INVENTORY disagrees with the
corpus**. Written 2026-09-14, after the registry's Totals line sat 12 texts stale above 66
correct rows with nothing able to tell the difference.

**Never write which texts are translated, or any percentage, in this file.** Derive it:
`python3 scripts/check_inventory.py`. This paragraph enumerated the list twice and was wrong
both times — first after nine days, then after **hours**, when 67,820 served "translations"
turned out to be the Sanskrit with an English prefix glued on and were moved to
`english_draft`/`hindi_draft` (2026-09-16). **A non-empty `english` field is not a
translation**: `status` and the served fields can disagree, and the Mongo seeder reads the
fields, not `status` (G50). (Caught both times by the `docs/INVENTORY.md → CLAUDE.md` edge.)

### ⚠ ~70 shlokas never reach AstroAcharya — derive the number, never trust this heading

**This heading said 71 until 2026-09-15 and the tool said 70.** A count in a heading rots faster
than the paragraph under it; the figure below is whatever `check_inventory.py` last printed, and
the command is the authority.

`seed_texts.py` dedupes by `(chapter, shloka)`, later file wins — so INVENTORY's Shlokas column
counts what is *present*, not what is **ingestible** (G8). All of them are intra-chapter and
pre-existing; `python3 scripts/check_inventory.py` prints the current loss and names every text
carrying it. **The converter cannot add to it** — it refuses a text with a duplicate
`(chapter, number)` rather than writing it, so a collision blocks the conversion instead of
quietly never ingesting.

### Off-schema — CLOSED 2026-09-02

**Nothing in this corpus is off-schema.** `apastamba_dharma_sutra` was the last, re-digitised
from `4617.txt` by `scripts/sanskrit-convert/apastamba.py` — 1,315 sūtras, citation
`praśna.khaṇḍa.sūtra`, landing `untranslated`; **46 sūtras are ABSENT from the OCR and were
recorded, never invented.** Closure record and the two departures: INVENTORY §"Dharmashastra —
off-schema remainder". **Check for a clean source before characterising damaged data** —
Manusmṛti's damage analysis cost two sessions and was discarded when SARIT yielded it whole in
one pass; SARIT has no Āpastamba, so that route was not available here.

## Translation workflow

**Adding/updating translations:** Edit `english` and `hindi` fields directly in the JSON file. Update `status` accordingly (`"translated"` when both are present, `"partial"` if only one, `"untranslated"` if neither). Do not leave status stale.

**Proofreading Devanagari text:** Edit the source file in `../sanskrit-texts-sources/` (same tree, see §Layout) and re-convert. The source is canonical for the Sanskrit; `.json` is derived. Sources are **not** in this repo — `.gitignore` enforces it.

**Do not commit processing scripts** (batch*.py, inject*.py etc.) to this repo — they were throwaway tools and have been removed. Future translation patches should directly update JSON.

## Conventions

- Sub-divided chapters keep the Devanagari suffix in the chapter `number` (`"63अ"` / `"63ब"`) — do not renumber them to integers. **There are no per-chapter files**: `BPHS0110.json` and `MS_063अ.json` were retired by the one-file rule (2026-08-18) and this section named both until 2026-09-02
- Devanagari shloka boundary markers (`॥ १२॥`) must be preserved in `.md` files
- Commit messages: `feat: Added <Lang> translations for <Text> ch<N>` or `fix: Corrected <Text> ch<N> shloka <M>`

## Code exploration

This is a **JSON data corpus**, so the callers/impact/tests tools don't apply to the data — use **Grep / Read / the Explore agent**. A `code-review-graph` graph does exist here — **derive its freshness with `code-review-graph status`, never restate it.** But `.git/hooks/pre-commit` is **DEAD**: this repo sets `core.hooksPath=.githooks`, so nothing rebuilds the graph on commit and no stale graph "self-heals". This section asserted both until 2026-09-14; the `fatal: unable to read <sha>` bursts it invoked as evidence are **G25 — narrowed, not solved**, and G25 explicitly rules out the graph hook as their cause. See `rule:tool-priority`.

## State management

See `rule:state-and-decisions`. **`STATE.md`, `DECISIONS.md` and `GOTCHAS.md` live in the
WORKSPACE** at `../propagation/state/sanskrit-texts/`. The `STATE.md`
and `docs/DECISIONS.md` still in this repo are 14-line stubs headed "moved"; this section
described them as the real files until 2026-09-10. Pre-move history, including the `TODO.md`
absorbed into STATE.md and deleted 2026-08-17: `git log --follow -- STATE.md`.
