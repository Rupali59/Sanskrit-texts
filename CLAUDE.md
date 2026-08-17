# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Parent context: `~/Documents/GitHub/Vipin Kaushik/CLAUDE.md`

## What this repo is

An open-source corpus of classical Sanskrit Jyotisha (Vedic astrology) texts, digitized for computational access by AstroAcharya. **Not a code project** — this is a data repository. Source of truth for proofreading: [sanskritdocuments.org/sanskrit/jyotisha](https://sanskritdocuments.org/sanskrit/jyotisha/) (see `REFERENCES.md`).

AstroAcharya seeds this data into MongoDB and queries it via a `/texts` API. The `@source(("bphs", chapter, [shlokas]))` decorator in AstroAcharya references `text_id` values from this corpus.

## Layout

```
Hora/                          Natal astrology texts
  BrihatParasharaHoraShastra/  BPHS0110.json … BPHS9197.json  (11 chunks, ~3932 shlokas)
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
  "category": "hora",
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

> **Paths corrected 2026-08-17; every row re-derived from the chapter JSON.** All eleven
> `Hora/` paths were dead — commit `1cccca6` (2026-07-17) recategorised Hora into schools
> (~194 renames) and this table did not follow. The **shloka counts and translation
> percentages were all correct** and are unchanged; only the Directory column had rotted,
> which is the column that duplicates the generated `docs/INVENTORY.md`. The same stale map
> also lived in `../astroacharya/scripts/list_sources.py` and was fixed in the same pass.
>
> `docs/INVENTORY.md` is **generated** (`scripts/gen_inventory.py`) and is the authority on
> paths and layout. This table exists only for what INVENTORY does not emit: `text_id`
> (which is also stamped inside every chapter JSON), shloka counts and translation state.
> **When they disagree, INVENTORY is right.**
>
> Note the layout is not uniform: some texts hold their JSON **directly** in the text
> directory, others under `chapters/`. The trailing path segment below reflects the real one.

| text_id | Directory | Shlokas | Translation |
|---------|-----------|---------|-------------|
| `bphs` | Hora/Parashari/BrihatParasharaHoraShastra/ | 3932 | 100% |
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

**21 texts on the normalized schema · 20,559 shlokas**, derived 2026-08-17 by walking every
JSON and counting `chapters[].shlokas[]`. Three texts were migrated onto the schema that day
(`saravali` 1,163, `asvalayana_grhya_sutra` 394, `MuhurtaChintamani`'s `MC_001` 37) — content
preserved byte-for-byte, only field names and structure changed.

⚑ **`muhurta_chintamani` is 82% translated, not 100%.** `MC_001.json` (37 shlokas, chapter 1)
has English but **no Hindi**, so those shlokas carry `status: "partial"` and an empty `hindi`.
Its shloka numbers also run 11–32, then 1–7, then 37–44 — distinct, so they ingest without
collision, but the sequence is wrong and needs the source text to repair.

Two neighbouring conventions are **not** defects and are handled, listed so they are not
"fixed" into breakage:
- `MinarajaYavanajataka` numbers variant chapters `"24अ"`, `"63अ"`, `"63ब"` (3 files).
- `Jatakaparijatah` numbers half-shlokas `"1/2"` (6 files) — legitimate prosody.

### ⚠ 2,873 shlokas never reach AstroAcharya — a `(chapter, shloka)` key collision

Found 2026-08-17 by simulating `../astroacharya/scripts/seed_texts.py`, which accumulates
shlokas **deduplicated by `(chapter, shloka)`, later file wins** (`:92-94`). Where two records
share a key, one is silently discarded. **The Shlokas column above counts what is present, not
what is ingestible**, and for one text those differ by half:

| text_id | present | ingested | lost |
|---------|--------:|---------:|-----:|
| `brihat_samhita` | 5500 | **2771** | **2729** |
| `bphs` | 3932 | 3867 | 65 |
| `jataka_parijata` | 1947 | 1892 | 55 |
| `laghu_jatakam` | 182 | 168 | 14 |
| `minaraja_yavana_jataka` | 4027 | 4026 | 1 |
| `yajusha_jyotisham` | 45 | 44 | 1 |

BPHS's 65 are the known chunk-boundary overlaps the seeder's own comment describes.

**`brihat_samhita`'s 2,729 are the whole remaining problem, and the fix is a decision, not
code.** `Varahmihir_brihatsamhita.json` and `Varahmihir_brihatsamhita2.json` are **two
recensions of the same work**, both numbering chapters 1–106: 2,711 of 2,750 keys collide,
2,575 of those holding different text. Measured side by side 2026-08-17:

| | chapters | shlokas | translated | avg Sanskrit | avg English |
|---|---:|---:|---|---:|---:|
| `…brihatsamhita.json` | 105 | 2750 | en + hi | 116 | 173 |
| `…brihatsamhita2.json` | **106** — adds ch 38 | 2750 | en + hi | 118 | **193** |

**File 2 is the fuller recension** — it carries a chapter the other lacks and materially
longer translations — **and it is already the one being kept**, because `seed_texts.py:96`
sorts filenames and later wins. So the corpus is not losing its better text; it is discarding
the variant *by filename luck rather than by decision*, which is the actual defect.

**The call:** either drop `Varahmihir_brihatsamhita.json` as superseded, or give it its own
`text_id` to preserve the variant readings. Do not leave it as an accident.

### Digitized but off-schema — blocked on numbering, not on schema

Three texts remain on the pre-normalization shape (14 files). **Converting them is not a
schema problem and must not be attempted mechanically:** their numbering keys collide with
*distinct* content, so a conversion would produce schema-valid files that the seeder then
silently truncates by two-thirds.

| text_id | Files | Records | Distinct keys | Collision |
|---------|------:|--------:|--------------:|-----------|
| `manu_smriti` | 12 | 2,942 | 900 | key `1.1` × 5, all different text; `MS_001` claims chapter 1 but spans 1–5; `MS_012` contains a chapter "13" |
| `apastamba_dharma_sutra` | 1 | 1,437 | 565 | key `1.1.1` × 24, all different text |
| `apastamba_paribhasha_sutra` | 1 | 358 | 55 | key `1` × 15, all different text |

**4,737 records, 1,520 distinct keys.** The content is real and distinct; the *numbers* are
wrong, and repairing them needs the source text — a scholarly act, not a mechanical one.
This is `STATE.md` P1, now with the reason it cannot simply be swept.

Placeholder-only directories with no JSON at all (`JaiminiSutras`, `ChandraKalaNadi`,
`JatakaTattvam`, `SarvarthaChintamani`, `PrashnaMarga`) have no `text_id` and are the only
genuine stubs.

Note: Shloka counts reflect deduplication by (chapter, shloka) key — BPHS chunks and brihat_samhita
files had overlapping entries that inflated previous counts. Unique counts are authoritative.

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
