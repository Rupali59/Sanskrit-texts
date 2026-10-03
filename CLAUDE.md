# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Parent context: `~/Documents/GitHub/Vipin Kaushik/CLAUDE.md`

## What this repo is

## What this repo is

An open-source corpus of classical Sanskrit texts, digitized for computational access by AstroAcharya. **The JSON is still the source of truth**, and a modelled Postgres store now sits beside it — schema, importer, exporter and a structural publication gate, documented in [`docs/DATABASE.md`](./docs/DATABASE.md). `make setup` then `make hello`. Source of truth for proofreading: [sanskritdocuments.org/sanskrit/jyotisha](https://sanskritdocuments.org/sanskrit/jyotisha/) (see `REFERENCES.md`).

**Scope: Jyotiṣa, plus everything that is not Philosophy (the Upaniṣad layer excepted — it stays here), Tantra, Mantra, Brāhmaṇa, Āraṇyaka, Śikṣā, Kalpa or Gāndharvaveda.** Tantra, Mantra and Kalpa go to `Tushar/Youvan`; Brāhmaṇa and Āraṇyaka are Youvan's too and are **not** a backlog here. The Vedic **Saṃhitā and Upaniṣad layers** belong here. **The line is drawn by LAYER, not by containing work** — seven held Upaniṣads are textually chapters of a Brāhmaṇa or Āraṇyaka and stay, and the Āpastamba Dharmasūtra stays though it is a praśna of a Kalpasūtra, while the Āpastamba Paribhāṣāsūtra left 2026-09-02 because its genre is ritual procedure. Full rule and its history: `../CLAUDE.md` §"Content / texts ownership". `docs/VEDIC_CORPUS.md` maps all 51 Vedic texts; the registry says which are held.

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

**Acquisition state is a table, not a sentence.** [`docs/INVENTORY.md`](./docs/INVENTORY.md) §"Acquisition status" gives every pursued text one row and one status — `HELD` · `SOURCED` · `REFUSED` · `UNSOURCED` · `LOST` — and `scripts/check_inventory.py` fails if that column and the corpus disagree. Provenance and terms: [`docs/SOURCES.md`](./docs/SOURCES.md).

## Uniform JSON schema

Every `.json` file uses one schema — no exceptions: `text_id`, `title_sa`, `title_en`, `category`, `chapters[].{number,title,shlokas[].{number,text,english,hindi,status}}`. The full example, the `text_id` / `category` / `number` notes and the list of fields **not** to add back: [`docs/DATABASE.md`](./docs/DATABASE.md) §"Moved from CLAUDE.md 2026-10-03". Adding a category is a two-repo change (**G51**).

**Field notes:**
- `status` — `"translated"` (both languages present) | `"partial"` (one language) | `"untranslated"` (neither) | `"drafted"` (machine-drafted, **not yet verified**)
- `english_draft` / `hindi_draft` — **optional, and the whole publication gate.** Machine-drafted
  translation lives here and **never** in `english`/`hindi`. Verification *promotes* a draft into
  the served field, flips `status` to `translated`, and clears the draft it consumed. The gate is
  **structural, not a flag** — nothing filters on `status`; `seed_texts.py`'s `_normalize_shloka`
  is an allowlist that cannot copy a draft field. **Never widen it.** The two innocuous-looking
  edits that publish every draft in the corpus, and the test pinning them: **G50**.

## text_id registry

**[`docs/INVENTORY.md`](./docs/INVENTORY.md) is the registry**, and [`docs/README.md`](./docs/README.md) indexes every other doc — every text's `text_id`, path, chapter and shloka counts, translation state and count-authority tier, in one table. **Per-text caveats are in [`docs/CANONICAL_COUNTS.md`](./docs/CANONICAL_COUNTS.md)** §"Per-text caveats".

**Derive the totals, never restate them:** `python3 scripts/check_inventory.py` prints texts, chapters, shlokas, categories and dedupe loss, and **exits 1 if INVENTORY disagrees with the corpus**.

**Never write which texts are translated, or any percentage, in this file.** Derive it: `python3 scripts/check_inventory.py`. **A non-empty `english` field is not a translation**: `status` and the served fields can disagree, and the Mongo seeder reads the fields, not `status` (G50). History of this paragraph: `docs/INVENTORY.md` §"Moved from CLAUDE.md 2026-10-03".

### ~70 shlokas never reach AstroAcharya — derive the number

`seed_texts.py` dedupes by `(chapter, shloka)` (G8), so INVENTORY counts what is *present*, not what is **ingestible**. `python3 scripts/check_inventory.py` prints the current loss and names every text carrying it; the converter refuses to add to it. Full text: `docs/INVENTORY.md` §"Moved from CLAUDE.md 2026-10-03".

### Off-schema — CLOSED 2026-09-02

**Nothing in this corpus is off-schema.** Closure record, the 46 absent sūtras, and the check-for-a-clean-source lesson: `docs/INVENTORY.md` §"Moved from CLAUDE.md 2026-10-03" and §"Dharmashastra — off-schema remainder".

## Translation workflow

**Adding/updating translations:** Edit `english` and `hindi` fields directly in the JSON file. Update `status` accordingly (`"translated"` when both are present, `"partial"` if only one, `"untranslated"` if neither). Do not leave status stale.

**Proofreading Devanagari text:** Edit the source file in `../sanskrit-texts-sources/` (same tree, see §Layout) and re-convert. The source is canonical for the Sanskrit; `.json` is derived. Sources are **not** in this repo — `.gitignore` enforces it.

**Do not commit processing scripts** (batch*.py, inject*.py etc.) to this repo — they were throwaway tools and have been removed. Future translation patches should directly update JSON.

## Conventions

- Sub-divided chapters keep the Devanagari suffix in the chapter `number` (`"63अ"` / `"63ब"`) — do not renumber them to integers. There are no per-chapter files (one-file rule, 2026-08-18).
- Devanagari shloka boundary markers (`॥ १२॥`) must be preserved in `.md` files
- Commit messages: `feat: Added <Lang> translations for <Text> ch<N>` or `fix: Corrected <Text> ch<N> shloka <M>`

## Code exploration

JSON data corpus: use **Grep / Read / the Explore agent**; derive graph freshness with `code-review-graph status`. `.git/hooks/pre-commit` is **DEAD** (`core.hooksPath=.githooks`); G25. Detail: `docs/README.md` §"Moved from CLAUDE.md 2026-10-03". See `rule:tool-priority`.

## State management

See `rule:state-and-decisions`. **`STATE.md`, `DECISIONS.md` and `GOTCHAS.md` live in the WORKSPACE** at `../propagation/state/sanskrit-texts/`; the `STATE.md` and `docs/DECISIONS.md` in this repo are 14-line stubs headed "moved". Pre-move history: `git log --follow -- STATE.md`.
