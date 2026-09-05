# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Parent context: `~/Documents/GitHub/Vipin Kaushik/CLAUDE.md`

## What this repo is

An open-source corpus of classical Sanskrit texts, digitized for computational access by AstroAcharya. **Not a code project** — this is a data repository. Source of truth for proofreading: [sanskritdocuments.org/sanskrit/jyotisha](https://sanskritdocuments.org/sanskrit/jyotisha/) (see `REFERENCES.md`).

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
`Hora/` · `Siddhanta/` · `Samhita/` · `Muhurta/` are the **Jyotiṣa** scheme (Horā, Gaṇita,
Saṃhitā, Muhūrta). `Veda/` · `Upanishad/` are the **Vedic layer** scheme. Until 2026-08-24
the five Vedic Saṃhitās sat inside `Samhita/` beside Varāhamihira's Bṛhat Saṃhitā — the same
spelling, two unrelated meanings. `Veda/` split them apart. `Vedanga-Jyotisha/` belongs to a
**third** axis, the six Vedāṅgas, and is the only one of them still here now that `Kalpa/`
has gone to Youvan.

**Sources live in `../sanskrit-texts-sources/`**, mirroring the same tree — Devanagari
`.wikitext`/`.html`/`.xml` fetches, transcriptions (`.md`), OCR (`.txt`), scans (`.pdf`) —
and it is a **superset**: it also holds Youvan's Brāhmaṇa/Āraṇyaka. This repo is the translation
layer: `.json` and nothing else. `.gitignore` enforces it; all prose lives in `docs/`.

**Every text is on the one-file rule as of 2026-09-02** — the last holdout, `ApastambaDharmaSutra`, was re-digitised by `scripts/sanskrit-convert/apastamba.py`.

**Undigitised texts: derive it, never restate it here** — this line said 13 until 2026-09-04,
when four landed in a day. Register: [`docs/INVENTORY.md`](./docs/INVENTORY.md) §"Undigitised";
five more are held but **refused on measured OCR quality**, each with its number in
`propagation/state/sanskrit-texts/STATE.md`. **As of 2026-09-05 no text is unsourced** — only
`GargaSamhita` (omens) lacks one, as it always has; the distinct jyotiṣa `GargaHora` is held.
**How that closed does not generalise:** the seven-channel survey calling these texts absent was
right and stands — none of them carries Muhūrta, Praśna, Jātaka or Nāḍī literature. Rupali
supplied the scans; **for this genre the channel is human.** [`docs/SOURCES.md`](./docs/SOURCES.md).

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
- `category` — `"parashari"` | `"nadi"` | `"siddhanta"` | `"samhita"` | `"veda_samhita"` | `"upanishad"` | `"vedanga_jyotisha"` | `"muhurta"` | `"dharmashastra"` | `"jaimini"`. **Re-derived 2026-08-24** — the Vedic corpus added `veda_samhita` (5 texts) and `upanishad` (24); `kalpa` left with Kalpa/ on 2026-08-24. It is a plain string in the schema, not an enum, so nothing rejects a typo: a misspelt category makes a text silently invisible to any category filter rather than failing. `jaimini` was added 2026-09-04 when `jaimini_sutra` became the first text to declare it — and `astroacharya/scripts/validate_corpus.py`'s `KNOWN_CATEGORIES` had to be widened in the same change, because that allowlist is the ONLY thing checking this field. The `prashna` tree still holds only a placeholder, so nothing declares it yet.
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
- `number` — integer for most shlokas/chapters; **string** for valid source sub-divisions: `"1/2"` for half-shlokas, and a Devanagari-suffixed chapter like `"63अ"` / `"63ब"` for a sub-divided chapter
- Files covering a single chapter still use the `chapters` array (one element) — uniform iteration in the seed script

**Do not add back** `source`, `header`, `book`, `english_meaning`, `hindi_meaning`, `source_file`, `source_chunk`, `is_duplicate` — these were pre-normalization artifacts.

## text_id registry

**[`docs/INVENTORY.md`](./docs/INVENTORY.md) is the registry**, and [`docs/README.md`](./docs/README.md) indexes every other doc — every text's `text_id`, path, chapter and shloka
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

### Off-schema — CLOSED 2026-09-02

`apastamba_dharma_sutra` was the last one. Re-digitised from `4617.txt` by
`scripts/sanskrit-convert/apastamba.py`: **1,315 sūtras**, citation `praśna.khaṇḍa.sūtra`,
externally checked against the canonical opening (1.1 `अथातः…`, 1.2 `धर्मज्ञसमयः प्रमाणम्`,
1.3 `वेदाश्च`). **46 sūtras are ABSENT from the OCR and were recorded, never invented** — the
parser prints every one with its khaṇḍa and line. The prior digitisation's 1,437 records,
including their unverified machine `english_translation`/`hindi_translation`, were discarded
with it; the new text lands `untranslated`.
**Check for a clean source before characterising damaged data**: Manusmṛti's damage analysis
cost two sessions and was thrown away when it was re-acquired whole from SARIT in one pass.
SARIT has no Āpastamba, so that route is not available here. Scope and ordered steps:
[`docs/plans/2026-08-22-dharmashastra-redigitisation.md`](./docs/plans/2026-08-22-dharmashastra-redigitisation.md).
`JaiminiSutras` and `ChandraKalaNadi` are the only surviving stub dirs. None of the 13 undigitised texts has a `text_id`.

## Translation workflow

**Adding/updating translations:** Edit `english` and `hindi` fields directly in the JSON file. Update `status` accordingly (`"translated"` when both are present, `"partial"` if only one, `"untranslated"` if neither). Do not leave status stale.

**Proofreading Devanagari text:** Edit the source file in `../sanskrit-texts-sources/` (same tree, see §Layout) and re-convert. The source is canonical for the Sanskrit; `.json` is derived. Sources are **not** in this repo — `.gitignore` enforces it.

**Do not commit processing scripts** (batch*.py, inject*.py etc.) to this repo — they were throwaway tools and have been removed. Future translation patches should directly update JSON.

## Conventions

- Sub-divided chapters keep the Devanagari suffix in the chapter `number` (`"63अ"` / `"63ब"`) — do not renumber them to integers. **There are no per-chapter files**: `BPHS0110.json` and `MS_063अ.json` were retired by the one-file rule (2026-08-18) and this section named both until 2026-09-02
- Devanagari shloka boundary markers (`॥ १२॥`) must be preserved in `.md` files
- Commit messages: `feat: Added <Lang> translations for <Text> ch<N>` or `fix: Corrected <Text> ch<N> shloka <M>`

## Code exploration

This is a **JSON data corpus**, so the callers/impact/tests tools don't apply to the data — use **Grep / Read / the Explore agent**. This said the `code-review-graph` graph was "empty here (0 nodes)"; it is not, and has not been since the repo gained scripts — **derive it with `code-review-graph status`, never restate it**. A `.git/hooks/pre-commit` rebuilds it on every commit, which is why a stale graph here self-heals; while it WAS stale it emitted `fatal: unable to read <sha>` once per changed file during commits. See `rule:tool-priority`.

## State management

See `rule:state-and-decisions` (`../docs/conventions/STATE_MANAGEMENT.md` is the
long-form convention). Adopted 2026-06-09 — sixth and final sibling.

- [`STATE.md`](./STATE.md) at repo root — subsumed the original `TODO.md`, which was **deleted 2026-08-17** once its 8 items were fully absorbed. Git history keeps it.
- [`docs/DECISIONS.md`](./docs/DECISIONS.md) — lives under `docs/` because `docs/` is tracked here.

Workspace-wide decisions live in `../docs/DECISIONS.md`; cross-project initiatives live
in `../STATE.md` and `../TODOS.md` (legacy).
