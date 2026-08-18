# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Parent context: `~/Documents/GitHub/Vipin Kaushik/CLAUDE.md`

## What this repo is

An open-source corpus of classical Sanskrit Jyotisha (Vedic astrology) texts, digitized for computational access by AstroAcharya. **Not a code project** — this is a data repository. Source of truth for proofreading: [sanskritdocuments.org/sanskrit/jyotisha](https://sanskritdocuments.org/sanskrit/jyotisha/) (see `REFERENCES.md`).

AstroAcharya seeds this data into MongoDB and queries it via a `/texts` API. The `@source(("bphs", chapter, [shlokas]))` decorator in AstroAcharya references `text_id` values from this corpus.

## Layout

**One JSON per text, always** (standardised 2026-08-18). Sources are not in this repo.

```
<Category>/<School?>/<Text>/
    <Text>.json          the text — every chapter, every shloka
    README.md            per-text metadata (optional)

Hora/{Parashari,Nadi,Prashna,Jaimini}/   Siddhanta/   Samhita/
Vedanga-Jyotisha/{Rigveda,Yajurveda}/    Dharmashastra/   Kalpa/Grhyasutra/   Muhurta/

docs/   INVENTORY.md (the manifest) · DECISIONS.md · BPHS_Master_Lexicon.md · …
```

**Sources live in `../sanskrit-texts-sources/`**, mirroring the same tree — Devanagari
transcriptions (`.md`), raw OCR (`.txt`), scans (`.pdf`). This repo is the translation
layer: `.json` + `README.md` and nothing else. `.gitignore` enforces it.

**3 texts do not yet follow the one-file rule** —
`Dharmashastra/{ManuSmriti,ApastambaDharmaSutra,ApastambaParibhashaSutra}/chapters/`, still
on the `sutras[]` shape. See `docs/DECISIONS.md` 2026-08-18.

**13 text directories are undigitised** — a `README.md` and nothing else, so
`docs/INVENTORY.md` cannot see them by construction (it defines a text as a dir holding
JSON): `JaiminiSutras`, `ChandraKalaNadi`, `JatakaTattvam`, `SarvarthaChintamani`,
`PrashnaMarga`, `BrahmasphutaSiddhanta`, `SiddhantaShiromani`, `GargaSamhita`,
`Atharvaveda`, `Samaveda`, `Dharmasindhu`, `NirnayaSindhu`, `MuhurtaMartanda`.
`GargaSamhita` and `MuhurtaMartanda` already have sources waiting in
`../sanskrit-texts-sources/`.

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
- `category` — `"parashari"` | `"nadi"` | `"siddhanta"` | `"samhita"` | `"vedanga_jyotisha"` | `"muhurta"` | `"dharmashastra"` | `"kalpa"`. **Corrected 2026-08-17**, derived from the data rather than restated: this line read `"hora" | "samhita" | "vedanga_jyotisha" | "siddhanta"`, but commit `1cccca6` split `hora` into schools and added four trees. `hora` survived in exactly one file (`SV_FULL.json`) and is now gone. `prashna` and `jaimini` trees exist but hold only placeholders, so no file declares them yet.
- `status` — `"translated"` (both languages present) | `"partial"` (one language) | `"untranslated"` (neither)
- `number` — integer for most shlokas/chapters; **string** for valid source sub-divisions: `"1/2"` for half-shlokas, and a Devanagari-suffixed chapter like `"63अ"` / `"63ब"` for a sub-divided chapter (stored in files `MS_063अ.json` / `MS_063ब.json`)
- Files covering a single chapter still use the `chapters` array (one element) — uniform iteration in the seed script

**Do not add back** `source`, `header`, `book`, `english_meaning`, `hindi_meaning`, `source_file`, `source_chunk`, `is_duplicate` — these were pre-normalization artifacts.

## text_id registry

> Every row re-derived from the JSON. `docs/INVENTORY.md` is the manifest and wins on paths;
> this table holds what it does not carry — `text_id`, counts, translation state.

| text_id | Directory | Shlokas | Translation |
|---------|-----------|---------|-------------|
| `bphs` | Hora/Parashari/BrihatParasharaHoraShastra/ | 3937 | 99.9% ⚑ |
| `brihat_jataka` | Hora/Parashari/BrihatJataka/ | 409 | 100% |
| `bhrigu_sutram` | Hora/Nadi/Bhrigusootram/ | 568 | 100% |
| `chamatkar_chintamani` | Hora/Parashari/Chamatkarchintamani/ | 112 | 100% |
| `jataka_parijata` | Hora/Parashari/Jatakaparijatah/ | 1947 | 100% |
| `laghu_jatakam` | Hora/Parashari/Laghujatakam/ | 182 | 100% |
| `minaraja_yavana_jataka` | Hora/Parashari/MinarajaYavanajataka/ | 4027 | 100% |
| `phaladeepika` | Hora/Parashari/Phaladeepika/ | 851 | 100% |
| `shatpanchashika` | Hora/Parashari/Shatpanchashika/ | 56 | 100% |
| `varahamihir_daivagnavallabh` | Hora/Parashari/VarahamihirDaivagnavallabh/ | 248 | 100% |
| `uttara_kalamrita` | Hora/Parashari/UttaraKalamrita/ | 324 | 100% |
| `muhurta_chintamani` | Muhurta/MuhurtaChintamani/ | 206 | 82% ⚑ |
| `saravali` | Hora/Parashari/Saravali/ | 1163 | 100% |
| `asvalayana_grhya_sutra` | Kalpa/Grhyasutra/Asvalayana/ | 394 | 100% |
| `arch_jyotisham` | Vedanga-Jyotisha/Rigveda/Aarchjyotisham/ | 36 | 100% |
| `yajusha_jyotisham` | Vedanga-Jyotisha/Yajurveda/Yajushajyotisham/ | 45 | 100% |
| `brihat_samhita` | Samhita/BrihatSamhita/ | 2771 | 100% |
| `aryabhatiya` | Siddhanta/Aryabhatiya/ | 121 | 100% |
| `panchasiddhantika` | Siddhanta/Panchasiddhantika/ | 166 | 100% |
| `surya_siddhanta` | Siddhanta/SuryaSiddhanta/ | 272 | 100% |

**21 texts on the normalized schema · 20,564 shlokas.** Rationale for every figure below:
`docs/DECISIONS.md`, three entries dated 2026-08-17.

⚑ **`bphs`** — one file since 2026-08-17 (was 11 chunks declaring 102 chapters for a
97-chapter work). 4 mis-split chapters repaired, 5 shlokas recovered; ingests **3937 of
3937**. Its whole translation backlog is those 5 — `12.11`, `53.20`, `61.55`, `66.43`,
`66.65` — Sanskrit only. Separately, **ch 25 shloka 16 is absent from the digitisation**
and was not invented, and ch 60's parenthesised duplicate is now `"12अ"` (a variant reading).

⚑ **`muhurta_chintamani` is 82%, not 100%** — `MC_001`'s 37 shlokas have English but no
Hindi (`status: "partial"`). Its numbers run 11–32, 1–7, 37–44: distinct, so they ingest,
but the sequence is wrong and needs the source.

Not defects, and handled — do not "fix" them into breakage: `MinarajaYavanajataka` numbers
variant chapters `"24अ"`/`"63अ"`/`"63ब"`; `Jatakaparijatah` numbers half-shlokas `"N 1/2"`.

### ⚠ 71 shlokas never reach AstroAcharya

`seed_texts.py:92-94` dedupes by `(chapter, shloka)`, later file wins — the Shlokas column
counts what is *present*, not what is ingestible. Was **2,800**; `brihat_samhita` was 2,729 of
it and is now **0**, its two files consolidated 2026-08-18. They were never two recensions:
2,574 of 2,711 shared keys differed only in **sandhi** (`प्रसूतिः विश्वात्मा` vs
`प्रसूतिर्विश्वात्मा`) — one text digitised twice. Ingestion unchanged at 2,771.

Remaining, all intra-chapter and pre-existing: `jataka_parijata` 55, `laghu_jatakam` 14,
`minaraja_yavana_jataka` 1, `yajusha_jyotisham` 1.

### Off-schema — needs RE-DIGITISATION, not renumbering

`manu_smriti` (12 files), `apastamba_dharma_sutra`, `apastamba_paribhasha_sutra` — 14 files,
4,737 records over 1,520 distinct keys. Checked against the canonical structures 2026-08-18
(Manusmriti = 12 adhyāyas / ~2,684 verses; Apastamba = Praśna→Paṭala→Khaṇḍa→sūtra, so `1.1.1`
is a *correct citation*). **The data cannot be mapped onto either**: Manusmriti's leading
component runs 1–33 and `MS_001` holds 89 fragmentary cycles; Apastamba has 219 bare-integer
records and 15 literal `X.X.21` placeholders — the digitiser recording "prefix unknown".
**Not a renumbering job — needs re-digitisation.** Detail and sources: `docs/DECISIONS.md`.

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
