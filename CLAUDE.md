# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Parent context: `~/Documents/GitHub/Vipin Kaushik/CLAUDE.md`

## What this repo is

An open-source corpus of classical Sanskrit Jyotisha (Vedic astrology) texts, digitized for computational access by AstroAcharya. **Not a code project** — this is a data repository. Source of truth for proofreading: [sanskritdocuments.org/sanskrit/jyotisha](https://sanskritdocuments.org/sanskrit/jyotisha/) (see `REFERENCES.md`).

AstroAcharya seeds this data into MongoDB and queries it via a `/texts` API. The `@source(("bphs", chapter, [shlokas]))` decorator in AstroAcharya references `text_id` values from this corpus.

## Layout

```
Hora/                          Natal astrology texts
  BrihatParasharaHoraShastra/  BrihatParasharaHoraShastra.json + .md  (97 chapters, 3937 shlokas)
  BrihatJataka/chapters/       brihmajjataka_ch01…28.json
  Bhrigusootram/chapters/      bhrigustrotram_ch01…08.json
  Chamatkarchintamani/chapters/ CC_001…010.json
  Jatakaparijatah/chapters/    JP_001…018.json
  Laghujatakam/chapters/       LJ_001…016.json
  MinarajaYavanajataka/chapters/ MS_001…039.json
  Phaladeepika/                phaladeepika.json
  Shatpanchashika/             Shatpanchashika.json
  UttaraKalamrita/             uttara_kalamrita.json (9 chapters, 324 shlokas)
  VarahamihirDaivagnavallabh/  Varahamihircharita_daivagya_vallabh.json
  [README-only stubs]          Saravali, SarvarthaChintamani, PrashnaMarga, JatakaTattvam
Samhita/
  BrihatSamhita/               Varahmihir_brihatsamhita.json + Varahmihir_brihatsamhita2.json
Vedanga-Jyotisha/
  Rigveda/Aarchjyotisham/      Aarchjyotisham.json
  Yajurveda/Yajushajyotisham/  Yajushajyotisham.json
Siddhanta/                     Mathematical astronomy texts
  Aryabhatiya/chapters/        AB_001…004.json (4 padas, 121 shlokas)
  Panchasiddhantika/chapters/  PS_001…018.json (18 chapters, 166 shlokas)
docs/
  BPHS_Master_Lexicon.md
  BPHS_Only_Terminology.md
```

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

> **Corrected 2026-08-17 — every row re-derived from the JSON** (11 of 17 `Hora/` paths were
> dead after `1cccca6`). `docs/INVENTORY.md` is **generated** and is the authority on paths;
> this table holds only what it does not emit — `text_id`, counts, translation state. **When
> they disagree, INVENTORY is right.** Some texts hold JSON directly, others under `chapters/`.

| text_id | Directory | Shlokas | Translation |
|---------|-----------|---------|-------------|
| `bphs` | Hora/Parashari/BrihatParasharaHoraShastra/ | 3937 | 99.9% ⚑ |
| `brihat_jataka` | Hora/Parashari/BrihatJataka/chapters/ | 409 | 100% |
| `bhrigu_sutram` | Hora/Nadi/Bhrigusootram/chapters/ | 568 | 100% |
| `chamatkar_chintamani` | Hora/Parashari/Chamatkarchintamani/chapters/ | 112 | 100% |
| `jataka_parijata` | Hora/Parashari/Jatakaparijatah/chapters/ | 1947 | 100% |
| `laghu_jatakam` | Hora/Parashari/Laghujatakam/chapters/ | 182 | 100% |
| `minaraja_yavana_jataka` | Hora/Parashari/MinarajaYavanajataka/chapters/ | 4027 | 100% |
| `phaladeepika` | Hora/Parashari/Phaladeepika/ | 851 | 100% |
| `shatpanchashika` | Hora/Parashari/Shatpanchashika/ | 56 | 100% |
| `varahamihir_daivagnavallabh` | Hora/Parashari/VarahamihirDaivagnavallabh/ | 248 | 100% |
| `uttara_kalamrita` | Hora/Parashari/UttaraKalamrita/ | 324 | 100% |
| `muhurta_chintamani` | Muhurta/MuhurtaChintamani/chapters/ | 206 | 82% ⚑ |
| `saravali` | Hora/Parashari/Saravali/chapters/ | 1163 | 100% |
| `asvalayana_grhya_sutra` | Kalpa/Grhyasutra/Asvalayana/chapters/ | 394 | 100% |
| `arch_jyotisham` | Vedanga-Jyotisha/Rigveda/Aarchjyotisham/ | 36 | 100% |
| `yajusha_jyotisham` | Vedanga-Jyotisha/Yajurveda/Yajushajyotisham/ | 45 | 100% |
| `brihat_samhita` | Samhita/BrihatSamhita/ | 5500 | 100% |
| `aryabhatiya` | Siddhanta/Aryabhatiya/chapters/ | 121 | 100% |
| `panchasiddhantika` | Siddhanta/Panchasiddhantika/chapters/ | 166 | 100% |
| `surya_siddhanta` | Siddhanta/SuryaSiddhanta/chapters/ | 272 | 100% |

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

### ⚠ 2,800 shlokas never reach AstroAcharya

`seed_texts.py:92-94` deduplicates by `(chapter, shloka)`, later file wins — so **the Shlokas
column counts what is present, not what is ingestible.** Corpus ingests **17,764 of 20,564**.

**`brihat_samhita` is 2,729 of that 2,800**, and the fix is a decision, not code: it ships
**two recensions of the same work**, both numbering chapters 1–106 (2,711 keys collide, 2,575
holding different text). File 2 is the fuller one — 106 chapters incl. ch 38, avg English 193
vs 173 — **and already the one kept**, because filenames sort and later wins. So the variant
is discarded by luck rather than by decision. Either drop file 1 as superseded, or give it
its own `text_id`. Remainder: `jataka_parijata` 55, `laghu_jatakam` 14, `minaraja` 1,
`yajusha_jyotisham` 1.

### Digitized but off-schema — blocked on numbering, not schema

`manu_smriti` (12 files), `apastamba_dharma_sutra`, `apastamba_paribhasha_sutra` — **14 files,
4,737 records over 1,520 distinct keys.** Keys collide with *distinct* content (`1.1.1` ×24,
all different). **Do not convert them mechanically:** the result would be schema-valid files
the seeder silently truncates by two-thirds. Repairing the numbering needs the source text.

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

- [`STATE.md`](./STATE.md) at repo root — subsumes the original `TODO.md` (now frozen with a banner).
- [`docs/DECISIONS.md`](./docs/DECISIONS.md) — lives under `docs/` because `docs/` is tracked here.
- [`TODO.md`](./TODO.md) — frozen 2026-06-09. Historical only; new items go to `STATE.md`.

Workspace-wide decisions live in `../docs/DECISIONS.md`; cross-project initiatives live
in `../STATE.md` and `../TODOS.md` (legacy).
