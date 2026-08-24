# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Parent context: `~/Documents/GitHub/Vipin Kaushik/CLAUDE.md`

## What this repo is

An open-source corpus of classical Sanskrit texts, digitized for computational access by AstroAcharya. **Not a code project** — this is a data repository. Source of truth for proofreading: [sanskritdocuments.org/sanskrit/jyotisha](https://sanskritdocuments.org/sanskrit/jyotisha/) (see `REFERENCES.md`).

**Scope: Jyotiṣa, plus everything that is not Tantra, Mantra, Brāhmaṇa, Āraṇyaka, Śikṣā or Kalpa** (narrowed 2026-08-23, narrowed again 2026-08-24 — see `../CLAUDE.md` §"Content / texts ownership"). This line read "a corpus of classical Sanskrit **Jyotisha** texts", which was already narrower than the contents — `Dharmashastra/` and `Kalpa/` are not Jyotish — and became more so when Philosophy moved here from Youvan. The Vedic corpus **Saṃhitā and Upaniṣad layers** belong here; **Brāhmaṇa and Āraṇyaka went to Youvan 2026-08-24** (ritual prose — nothing moved on disk, none were held). The line is by LAYER: seven held Upaniṣads are textually chapters of a Brāhmaṇa or Āraṇyaka and stay here — see `../CLAUDE.md` §"Content / texts ownership". `docs/VEDIC_CORPUS.md` maps all 51 texts; **29 are held** as of 2026-08-24 — all 13 mukhya Upaniṣads plus 11 minor, and the primary Saṃhitā of every Veda. Brāhmaṇa and Āraṇyaka are Youvan's, not a backlog here. Tantra and Mantra go to `Tushar/Youvan`.

AstroAcharya seeds this data into MongoDB and queries it via a `/texts` API. The `@source(("bphs", chapter, [shlokas]))` decorator in AstroAcharya references `text_id` values from this corpus.

## Layout

**One JSON per text, always** (standardised 2026-08-18). Sources are not in this repo.

```
<Category>/<School?>/<Text>/
    <Text>.json          the text — every chapter, every shloka
    README.md            per-text metadata (optional)

Veda/{rigveda,samaveda,atharvaveda,krishna-yajurveda,shukla-yajurveda}/   Upanishad/<veda>/
Hora/{Parashari,Nadi,Prashna,Jaimini}/   Siddhanta/   Samhita/   Muhurta/
Vedanga-Jyotisha/{Rigveda,Yajurveda}/    Dharmashastra/

docs/   INVENTORY.md (the manifest) · DECISIONS.md · BPHS_Master_Lexicon.md · …
```

**The top level carries TWO classification systems, and one word collides across them.**
`Hora/` · `Siddhanta/` · `Samhita/` · `Muhurta/` are the **Jyotiṣa** scheme (Horā, Gaṇita,
Saṃhitā, Muhūrta). `Veda/` · `Upanishad/` are the **Vedic layer** scheme. Until 2026-08-24
the five Vedic Saṃhitās sat inside `Samhita/` beside Varāhamihira's Bṛhat Saṃhitā — the same
spelling, two unrelated meanings. `Veda/` split them apart. `Vedanga-Jyotisha/` belongs to a
**third** axis, the six Vedāṅgas, and is the only one of them still here now that `Kalpa/`
has gone to Youvan.

**Sources live in `../sanskrit-texts-sources/`**, mirroring the same tree — Devanagari
transcriptions (`.md`), raw OCR (`.txt`), scans (`.pdf`). This repo is the translation
layer: `.json` + `README.md` and nothing else. `.gitignore` enforces it.

**2 texts do not yet follow the one-file rule** — the two Āpastamba dirs, still on the
`sutras[]` shape; see §"Off-schema" below. `ManuSmriti` left this set 2026-08-24.

**13 text directories are undigitised** — a `README.md` and nothing else, so INVENTORY
cannot see them by construction (it defines a text as a dir holding JSON). They are listed
in [`docs/INVENTORY.md`](./docs/INVENTORY.md) §"Undigitised"; do not restate them here.

**Neither `GargaSamhita` nor `MuhurtaMartanda` has a usable source waiting**, despite older
notes saying so — both claims died on inspection 2026-08-23. Detail:
[`docs/SOURCES.md`](./docs/SOURCES.md) §"Two sources that were not what they looked like".

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
- `category` — `"parashari"` | `"nadi"` | `"siddhanta"` | `"samhita"` | `"veda_samhita"` | `"upanishad"` | `"vedanga_jyotisha"` | `"muhurta"` | `"dharmashastra"`. **Re-derived 2026-08-24** — the Vedic corpus added `veda_samhita` (5 texts) and `upanishad` (24); `kalpa` left with Kalpa/ on 2026-08-24. It is a plain string in the schema, not an enum, so nothing rejects a typo: a misspelt category makes a text silently invisible to any category filter rather than failing. `prashna` and `jaimini` trees exist but hold only placeholders, so no file declares them yet.
- `status` — `"translated"` (both languages present) | `"partial"` (one language) | `"untranslated"` (neither) | `"drafted"` (machine-drafted, **not yet verified**)
- `english_draft` / `hindi_draft` — **optional, and the whole publication gate.** Machine-drafted
  translation lives here and **never** in `english`/`hindi`. Verification *promotes* a draft into
  the served field and flips `status` to `translated`, clearing the draft it consumed.

  **Why the fields are separate rather than a filter.** `app/api/texts.py` returns the Mongo
  document wholesale and filters on **nothing**; `seed_texts.py`'s `_normalize_shloka` is an
  **allowlist** naming `text`/`english`/`hindi`/`status`, so a draft field is simply never copied
  to Mongo and cannot be served. The unsafe path is unreachable rather than merely discouraged —
  `rule:safety-flag-needs-a-test`. Adding a draft field to that allowlist, or rewriting it as
  `{**sh}`, publishes unverified machine text on the public surface and breaks the workspace hard
  rule *"Computation is AI-assisted; meaning is not"*. `tests/test_seed_texts.py` pins it and the
  mutation was checked both ways.
- `number` — integer for most shlokas/chapters; **string** for valid source sub-divisions: `"1/2"` for half-shlokas, and a Devanagari-suffixed chapter like `"63अ"` / `"63ब"` for a sub-divided chapter (stored in files `MS_063अ.json` / `MS_063ब.json`)
- Files covering a single chapter still use the `chapters` array (one element) — uniform iteration in the seed script

**Do not add back** `source`, `header`, `book`, `english_meaning`, `hindi_meaning`, `source_file`, `source_chunk`, `is_duplicate` — these were pre-normalization artifacts.

## text_id registry

**`docs/INVENTORY.md` is the registry** — every text's `text_id`, path, chapter and shloka
counts, translation state and count-authority tier, in one table. **Per-text caveats are in
[`docs/CANONICAL_COUNTS.md`](./docs/CANONICAL_COUNTS.md)** §"Per-text caveats"; they were
inline here until 2026-08-24 and took this file 58 lines over its cap.

**Derive the totals, never restate them:**

```
python3 -c "import json,glob;print(sum(len(c['shlokas']) for p in glob.glob('**/*.json',recursive=True) if not p.startswith('docs/') for c in (json.load(open(p)).get('chapters') or [])))"
```

The Jyotiṣa texts are **100% translated**; the Vedic and Upaveda texts land **untranslated**,
which is why the corpus total is no longer a single percentage. Per-text state is in INVENTORY.

### ⚠ 71 shlokas never reach AstroAcharya

`seed_texts.py:92-94` dedupes by `(chapter, shloka)`, later file wins — so INVENTORY's Shlokas
column counts what is *present*, not what is **ingestible**. All 71 are intra-chapter and
pre-existing: `jataka_parijata` 55, `laghu_jatakam` 14, `minaraja_yavana_jataka` 1,
`yajusha_jyotisham` 1. **The converter cannot add to it** — it rejects a text with a duplicate
`(chapter, number)` rather than writing it, so a collision blocks the conversion instead of
quietly never ingesting. Re-derive:

```
python3 -c "import json,glob,collections;t=0
for p in glob.glob('**/*.json',recursive=True):
 if p.startswith('docs/'): continue
 j=json.load(open(p)); c=collections.Counter()
 for ch in (j.get('chapters') or []):
  for s in ch.get('shlokas',[]): c[(ch['number'],s['number'])]+=1
 t+=sum(v-1 for v in c.values() if v>1)
print(t)"
```

### Off-schema — needs RE-DIGITISATION, not renumbering

`apastamba_dharma_sutra`, `apastamba_paribhasha_sutra` — 2 files on the superseded `sutras[]`
shape, with no `chapters[]` array, so they are absent from every count above and do not ingest.
**Check for a clean source before characterising damaged data**: Manusmṛti's damage analysis
cost two sessions and was thrown away when it was re-acquired whole from SARIT in one pass.
SARIT has no Āpastamba, so that route is not available here. Scope and ordered steps:
[`docs/plans/2026-08-22-dharmashastra-redigitisation.md`](./docs/plans/2026-08-22-dharmashastra-redigitisation.md).

Placeholder-only dirs with no JSON (`JaiminiSutras`, `ChandraKalaNadi`, `JatakaTattvam`,
`SarvarthaChintamani`, `PrashnaMarga`) have no `text_id` and are the only genuine stubs.

## Translation workflow

**Adding/updating translations:** Edit `english` and `hindi` fields directly in the JSON file. Update `status` accordingly (`"translated"` when both are present, `"partial"` if only one, `"untranslated"` if neither). Do not leave status stale.

**Proofreading Devanagari text:** Edit the `.md` source file and re-run the AstroAcharya parser if one exists for the text. The `.md` is the canonical source for the Sanskrit text; `.json` is the derived form.

**Do not commit processing scripts** (batch*.py, inject*.py etc.) to this repo — they were throwaway tools and have been removed. Future translation patches should directly update JSON.

## Conventions

- BPHS is split into 10-chapter chunks (`BPHS0110`, `BPHS1120`, …) — keep that chunking when editing
- Sub-divided chapters keep the Devanagari suffix in both the filename and the chapter `number` (e.g. `MS_063अ.json` → `"number": "63अ"`) — do not renumber them to integers
- Devanagari shloka boundary markers (`॥ १२॥`) must be preserved in `.md` files
- Commit messages: `feat: Added <Lang> translations for <Text> ch<N>` or `fix: Corrected <Text> ch<N> shloka <M>`

## Code exploration

This is a **JSON data corpus, not code** — the `code-review-graph` graph is empty here (0 nodes; nothing to parse), and its callers/impact/tests tools don't apply to data files. Use **Grep / Read / the Explore agent** directly. See `rule:tool-priority` for the general tool-priority ordering (it applies to code-bearing siblings like astroacharya; this repo has no code for it to index).

## State management

See `rule:state-and-decisions` (`../docs/conventions/STATE_MANAGEMENT.md` is the
long-form convention). Adopted 2026-06-09 — sixth and final sibling.

- [`STATE.md`](./STATE.md) at repo root — subsumed the original `TODO.md`, which was **deleted 2026-08-17** once its 8 items were fully absorbed. Git history keeps it.
- [`docs/DECISIONS.md`](./docs/DECISIONS.md) — lives under `docs/` because `docs/` is tracked here.

Workspace-wide decisions live in `../docs/DECISIONS.md`; cross-project initiatives live
in `../STATE.md` and `../TODOS.md` (legacy).
