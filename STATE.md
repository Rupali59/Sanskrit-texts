# sanskrit-texts — State

Last updated: 2026-08-17

Convention: `../docs/conventions/STATE_MANAGEMENT.md` (adopted 2026-06-09).
Decisions: [`docs/DECISIONS.md`](./docs/DECISIONS.md) (project `docs/` is tracked).
Plans: [`docs/plans/README.md`](./docs/plans/README.md) (adopted 2026-06-20, 6th sibling).
Supersedes: `TODO.md` (digitization checklist subsumed below; file retained as historical).

## Recently shipped

Five commits on `main` since the last update (all 2026-07-17 except the last), clean tree:

- `1cccca6` `refactor(corpus):` recategorize Hora into schools + ingest new texts — ~194 renames. New tree: `Hora/Parashari/` (BrihatJataka, BrihatParasharaHoraShastra, Chamatkarchintamani, Jatakaparijatah, JatakaTattvam, Laghujatakam, MinarajaYavanajataka, Phaladeepika, Saravali, SarvarthaChintamani, Shatpanchashika, UttaraKalamrita, VarahamihirDaivagnavallabh), `Hora/Nadi/` (Bhrigusootram + ChandraKalaNadi `.placeholder`), `Hora/Prashna/` (PrashnaMarga), `Hora/Jaimini/` (JaiminiSutras `.placeholder`). Also added new digitized chapter stores + new category trees (`Dharmashastra/`, `Muhurta/`) and committed `scripts/digitize.py` + `scripts/translate.py`. See `docs/DECISIONS.md` 2026-08-12 (backfilled).
- `4258491` `feat(corpus):` Apastamba sutras, Kalpa Grhyasutra, Saravali chapters — +22,027 lines. New top-level `Kalpa/` category.
- `c2cc99b` `docs:` corpus wiki — `scripts/gen_inventory.py` (117 lines) generates `docs/INVENTORY.md`; `docs/README.md` is the front page; root `.propagates.yml` declares `docs/INVENTORY.md` → astroacharya `reference.md` + `DATA_GAPS.md`.
- `b4aa78f` `chore:` gitignore source scans — `*.pdf` + `**/raw/`; source-out-of-git policy.
- `7fbfae1` (2026-08-10) `feat(corpus):` four new raw Dharmashastra source texts (`Dharmashastra/{4605,4607,4609,4617}.txt`) — raw, NOT yet chunked into JSON. Also re-tagged two `hora_acharya` targets in `.propagates.yml` to `kind: prose`. See `docs/DECISIONS.md` 2026-08-12 (backfilled).

**Corpus is now 23 texts / 240 chapter files / 7 live categories** (per `docs/INVENTORY.md`) — the old "all 14 texts 100%" claim in the 2026-06-20 entry below is obsolete.

## Now (in flight)

### 2026-08-17 — schema standardisation: 3 texts migrated, 3 stopped, and a bigger defect found

**Migrated onto the uniform schema** (content preserved byte-for-byte, asserted field-by-field
before writing; only names and structure changed):

| File | Records | Change |
|---|---:|---|
| `Hora/Parashari/Saravali/chapters/SV_FULL.json` | 1,163 | `sutras[]`→`chapters[].shlokas[]`, `id "sv_N"`→`number N`, `category` `hora`→`parashari`, `meter` retained |
| `Kalpa/Grhyasutra/Asvalayana/chapters/AGS_001.json` | 394 | same; `category: kalpa` |
| `Muhurta/MuhurtaChintamani/chapters/MC_001.json` | 37 | added all four metadata fields + chapter `number`; **no Hindi → `status: "partial"`** |

Corpus: **222 → 225 conformant files, 18,965 → 20,559 normalized shlokas** (+1,594, exactly the
three files), off-schema 6,331 → 4,737. `hora` was the last stale category value and is gone;
`CLAUDE.md`'s category enum was 4 values against 8 in the data and is corrected.

**Stopped, deliberately — 14 files across 3 texts.** `manu_smriti` (12 files), Apastamba ×2.
Their problem is **numbering, not schema**: keys collide with *distinct* content — `1.1.1`
appears 24 times with 24 different sūtras, `1` appears 15 times with 15. `MS_001.json` claims
chapter 1 but spans 1–5; `MS_012.json` contains a chapter "13" of a 12-chapter work. Converting
them would yield schema-valid files that `seed_texts.py` then **silently truncates from 4,737
records to 1,520**, because it deduplicates by `(chapter, shloka)` with later-file-wins. Fixing
the numbering needs the source text and is a scholarly act. Not attempted.

### ⚠ New, larger, and pre-existing: 2,873 shlokas never reach AstroAcharya

Found by simulating `../astroacharya/scripts/seed_texts.py:92-94` against the **conformant**
corpus — nothing to do with the migration:

- **`brihat_samhita` 5500 present → 2771 ingested, 2,729 lost.**
  `Varahmihir_brihatsamhita.json` and `Varahmihir_brihatsamhita2.json` are **two different
  recensions of the same 106 chapters**, both numbered 1–106. 2,711 of 2,750 keys collide and
  **2,575 of those hold different text.** One recension is discarded at ingest.
- `bphs` −65 (the known chunk-boundary overlap the seeder documents), `jataka_parijata` −55
  (was −63; 8 recovered, below), `laghu_jatakam` −14, `minaraja_yavana_jataka` −1,
  `yajusha_jyotisham` −1.

**Measured side by side, the brihat_samhita call is easy:** file 2 has 106 chapters to file
1's 105 (it carries ch 38), and longer translations (avg English 193 vs 173). Both are fully
en+hi. **File 2 is already the one kept** — `seed_texts.py:96` sorts filenames, later wins —
so the corpus keeps its better text and discards the variant *by filename luck rather than by
decision*. Either drop file 1 as superseded, or give it its own `text_id`.

### Numbering repair — 12 candidates, 11 applied, 1 correctly refused

Repaired only where the neighbours **force** the answer; 506 further disordered records were
left alone, because a heuristic that fixes 2.5% is not a fix and inventing shloka numbers is
worse than the defect.

- 9 bare `"1/2"` half-shlokas → `"46 1/2"`, `"48 1/2"`, `"44 1/2"`, `"33 1/2"`, `"34 1/2"`,
  `"88 1/2"`, `"91 1/2"`, `"94 1/2"` (JP_001/002/003/017). A bare `"1/2"` collides with every
  other bare `"1/2"` in the chapter; the corpus already uses the `"N 1/2"` form.
- 3 records in `JP_002` ch2 numbered 41,42,43 sat between 80 and 84 → **81,82,83**.
- **1 refused by its own guard:** a `Varahmihir_brihatsamhita.json` ch97 change removed no
  duplicate, so the invariant ("a repair must strictly reduce duplicate keys") rejected it.
  It would have been an unjustified edit to the data. The guard also caught an earlier
  invariant of mine that was too strict — it demanded zero duplicates, which trailing
  colophons make impossible.

**Colophons are left numbered as they are.** 8 records in `jataka_parijata` are chapter
colophons ("इति श्री… अध्यायः प्रथमः") whose *chapter ordinal* was parsed as a shloka number,
so 7 of them collide with a real shloka. They are not shlokas, the corpus has no convention
for them, and inventing one is a decision, not a repair.

Net: **17,686 → 17,694 shlokas reach ingestion**; 240 JSON files all still parse.

**The registry's Shlokas column counts what is present, not what is ingestible.** Needs an
editorial call: which recension is canonical, or does the second need its own `text_id`.
Recorded in `CLAUDE.md`; the schema migration cannot fix it.

Full astroacharya suite after the corpus change: **1001 passed**.


### 2026-08-17 — corpus path map was dead in two places; fixed, and the coupling declared

Commit `1cccca6` (2026-07-17) recategorised Hora into schools (~194 renames). **Two
consumers restated those paths and neither followed**, for a month, with no drift row —
because the coupling was never declared.

- **`CLAUDE.md` text_id registry — 11 of 17 directories did not exist.** Every `Hora/` row.
  All corrected against disk; `muhurta_chintamani` added; **23 of 23 paths now resolve.**
- **`../astroacharya/scripts/list_sources.py` — `TEXT_ID_TO_PATH`, 9 of 10 paths dead.**
  Corrected; 10/10 now resolve *and* contain shloka JSON. Its docstring `--canon-dir`
  example also pointed at `../../Youvan/texts/`, a tree that no longer exists.
- **Declared the edges** in `.propagates.yml`: `docs/INVENTORY.md` → `list_sources.py`
  (`kind: code`) and → `CLAUDE.md` (`kind: prose`). INVENTORY is generated, so it moves on
  exactly the changes that invalidate both. Both verified CLEAN.

**Severity was friction, not a wrong answer.** `print_missing` exits 2 naming the directory
rather than reporting "0 shlokas missing" — absence stayed attributable throughout.

### `--missing` rewritten — and the second defect was NOT friction, it was a silent zero

Fixing the paths exposed two further defects in `print_missing`, and **the severity call in
the entry above was wrong for the second one**:

1. **Filename-convention glob.** `canon_dir.glob(f"*_{chapter:03d}*.json")` matches only the
   Siddhanta naming (`AB_001.json`). Hora uses `_chNN`, BPHS uses range-bundled files
   (`BPHS0110.json` holds chapters 1–10), BrihatSamhita is single-file. So `--missing`
   exited 2 for every Hora text.
2. **It read `data.get("shlokas")` — top-level — while the normalized schema nests them
   under `chapters[].shlokas[]`.** For `aryabhatiya:1`, the one family whose filenames the
   glob *did* match, that returned an empty list and printed `missing: —` for a chapter
   with **13 unimplemented shlokas**. A tool reporting full canon coverage because it never
   looked is the S1 shape, not friction.

**Fixed** by `chapter_records()` in `../astroacharya/scripts/list_sources.py`, which selects
on `chapters[].number` and never on the filename, searches both the text dir and
`chapters/`, and **raises rather than returning empty** for unreadable or off-schema files —
a silent `[]` there reads as "canon fully implemented".

**The first version of that fix had two silent defects of its own**, found by running it
against real corpus data rather than fixtures, and both are now pinned:
- It filtered shloka numbers on `isinstance(n, int)`, dropping `Jatakaparijatah`'s
  **half-shlokas** (`"1/2"`, 6 files) — an undercount with no signal. They are now surfaced
  in the output label as `[N unnumbered shloka(s) — not listed]`.
- It matched chapters on `== chapter`, making `MinarajaYavanajataka`'s **variant chapters**
  (`"24अ"`, `"63अ"`, `"63ब"`, 3 files) unreachable. They now match their base number and the
  label discloses the suffix.

Both are legitimate corpus conventions, not data defects — recorded so they are not
"corrected" into breakage. A survey of every `chapters[]`-wrapped file found exactly **one**
genuinely off-schema case, `Muhurta/MuhurtaChintamani/chapters/MC_001.json`, which
`STATE.md` P1 already lists.

Verified on real corpus data, not just fixtures:
- `--missing BPHS:27` → found inside `BPHS2130.json`, **40 shlokas, 15 cited, 25 missing**.
  Previously exit 2.
- `aryabhatiya:1` → **13 missing**. Previously `missing: —`.

`tests/test_list_sources_missing.py` (11 tests) pins all three filename conventions, the
variant and half-shloka numberings, and the off-schema and unreadable cases. The guard was **mutated back to the top-level read** and 4
tests went red including the one naming that defect; the mutation was asserted present in
the file before running, and the restore verified by reading content rather than trusting
the command. Full astroacharya suite: **997 passed**.

### Two measurement errors I made and corrected — both worth keeping

1. **"Five texts have zero shlokas / are not yet digitized" was wrong.** They are digitized
   on the *pre-normalization* schema (top-level `sutras[]`/`shlokas[]`) — **6,294 shlokas**
   my scanner could not see because it only read `chapters[].shlokas[]`. Caught by reading
   **P1 below**, which had recorded Saravali's 1,163 sūtras all along; my independent count
   now matches it exactly. A scanner that understands one schema reports the other as empty.
2. **`muhurta_chintamani`: 206 shlokas present, 169 usable — and my first correction of
   this was also wrong.** `MC_001.json` carries no `text_id`, so a `text_id`-keyed count
   silently dropped its 37 and I "corrected" 169 to 206. But MC_001 is *off-schema*
   (`sanskrit`/`english_translation`, string numbers, no chapter `number`), so its 37 are
   not usable content and 169 was right for the normalized total all along. Both numbers
   are true of different questions; the table now states both. Migration belongs to P1.

Verified totals 2026-08-17: **18,965 normalized · 6,331 off-schema (6,294 whole-file + MC_001's 37) · 25,296 combined.** The
registry's shloka counts and translation percentages were all **already correct** — only the
Directory column, the one duplicating generated `docs/INVENTORY.md`, had rotted.

## Active initiatives

- None.

## Known signal

- `CLAUDE.md` is currently **131 lines / 7,342 bytes** — well under the prior 164/180-line yellow reading (that measurement predated the ⚑-footer trim in the 2026-06-20 data-correctness-audit entry). No size-cap concern right now. The live problem with `CLAUDE.md` is **content staleness**, not size — see Pending below.

## Pending (by priority)

### P1 — Off-schema JSON blocks AstroAcharya ingestion

**18 JSON files use the pre-normalization shape** — top-level `sutras`/`shlokas` with `sanskrit` / `english_translation` / `hindi_translation` / `chapter_number`, **no `status` field, no `chapters[]` wrapper**. This is exactly the shape `docs/DECISIONS.md` 2026-06-20 (uniform-schema normalization sweep) banned. **Blocks AstroAcharya `/texts` ingestion** for these texts until fixed.

- `Hora/Parashari/Saravali/chapters/SV_FULL.json` (1)
- `Dharmashastra/ManuSmriti/chapters/MS_001.json` … `MS_012.json` (12)
- `Dharmashastra/ApastambaDharmaSutra/chapters/ADS_001.json` (1)
- `Dharmashastra/ApastambaParibhashaSutra/chapters/APS_001.json` (1)
- `Kalpa/Grhyasutra/Asvalayana/chapters/AGS_001.json` (1)
- `Muhurta/MuhurtaChintamani/chapters/MC_001.json` and `MC_REMAINING_RAW.json` (2)

Not fixed here — recorded for a follow-up schema-migration pass.

### P1 — Digitization backlog (in-scope, README-only stubs)

Corrected 2026-08-12 — the 2026-06-20 list was wrong: **Saravali, Surya Siddhanta, Aryabhatiya, and Panchasiddhantika are now digitized**, not stubs.

- **Saravali** — digitized but off-schema (see P1 above): `Hora/Parashari/Saravali/chapters/SV_FULL.json`, 1,163 sūtras, single-file (not chapter-split).
- **Surya Siddhanta** — 14 chapters / 272 shlokas / 100% translated.
- **Aryabhatiya** — 4 padas / 121 shlokas / 100% translated.
- **Panchasiddhantika** — 18 chapters / 166 shlokas / 100% translated.

Genuine stubs remaining:

- **Hora (classical Sanskrit):** SarvarthaChintamani (Venkatesa Sharma), PrashnaMarga (Kerala horary, now `Hora/Prashna/`), JatakaTattvam
- **Siddhanta (mathematical astronomy):** Brahmasphuta Siddhanta, Siddhanta Shiromani
- **New since 2026-06-20:** `Muhurta/MuhurtaMartanda/` (README + empty `chapters/`), `Samhita/GargaSamhita/` (README + raw `3003.txt`), `Dharmashastra/Dharmasindhu/`, `Dharmashastra/NirnayaSindhu/`, `Hora/Jaimini/JaiminiSutras/` (`.placeholder`), `Hora/Nadi/ChandraKalaNadi/` (`.placeholder`)
- **Permanently non-digitizable — lost recensions, not backlog:** `Vedanga-Jyotisha/Samaveda/`, `Vedanga-Jyotisha/Atharvaveda/`. Record as such, don't carry as pending work.

### P2 — Corpus hygiene / doc drift (recorded, not fixed here)

- `CLAUDE.md` layout block + text_id registry still show the pre-`1cccca6` flat `Hora/<Text>/` paths — all now wrong (correct tree is `Hora/{Parashari,Nadi,Prashna,Jaimini}/<Text>/`). Its `[README-only stubs]` line is also stale (references texts now digitized).
- `CLAUDE.md` `category` enum is `hora | samhita | vedanga_jyotisha | siddhanta` — missing `muhurta`, `dharmashastra`, `kalpa`, `jaimini`, all now in use by committed files.
- Root `README.md` ~3 months stale: still shows the flat Hora tree, `Tantra/` and `SamudrikShastra/` sections (both removed 2026-06-20), the 4 now-digitized texts listed as "not yet digitized," and the pre-normalization Schema A/B (`english_meaning`, `source`, `header`, `book`) that `docs/DECISIONS.md` 2026-06-20 banned.
- `docs/INVENTORY.md` "Source held" column is stale — lists `pdf` for Saravali/Panchasiddhantika/SuryaSiddhanta/MuhurtaChintamani, but those source scans moved to `../sanskrit-texts-sources/` (see new section below). Needs a `python scripts/gen_inventory.py` regen + commit.
- `.gitignore` lines 8–9 are dead rules — they ignore pre-recategorization paths `Hora/UttaraKalamrita/raw_uttara_kalamrita.txt` and `Hora/UttaraKalamrita/sections/`, but those files moved to `Hora/Parashari/UttaraKalamrita/` in `1cccca6` and the sections were then committed as chapter JSON.
- `scripts/digitize.py` + `scripts/translate.py` are committed (landed in `1cccca6`), against `CLAUDE.md`'s "Do not commit processing scripts" rule.
- The 4 raw `Dharmashastra/{4605,4607,4609,4617}.txt` (from `7fbfae1`) await chunking into per-chapter JSON.

### P2 — Translation injection (from TODO.md)

- None pending on the original 14-text set. `muhurta_chintamani` is the one partially-digitized new text: 15 files, 206 shlokas, 169 translated (~82%).

### Possibly migrated from workspace `../TODOS.md`

- _None directly owned._ TM-068 (vendor-derived JSON deprecation sweep) mentions `SANSKRIT_TEXTS_PATH` but the work is astroacharya-side. TM-041 (Jyotish texts migration from Youvan into AstroAcharya) treats this repo as the destination — see workspace TODOS TM-041 for the producer side.

## `../sanskrit-texts-sources/` — source scans, kept out of git

Physical form of this repo's source-out-of-git policy (`docs/DECISIONS.md` 2026-07-17). Lives one directory up, at workspace root — nothing in this repo previously named it (fixed here). Now gitignored at the **workspace** level (`../.gitignore`).

Contents (310MB total):

- `Siddhanta/SuryaSiddhanta/1770115260.pdf`
- `Siddhanta/Panchasiddhantika/panch_siddhantika_040577_hr6.pdf`
- `Muhurta/MuhurtaMartanda/1759902040.pdf`
- `Muhurta/MuhurtaChintamani/muhurt_chintamani_002342_hr6.pdf`
- `Hora/Parashari/Saravali/saravaliofkalyan01kalyuoft.pdf`
- `sanskrit-texts-prerewrite-e0613c4.bundle` (156MB) — the pre-history-rewrite safety net referenced in `b4aa78f`'s commit message. The rewrite itself appears complete (`e0613c4` is not present in current `main` history), but no `docs/DECISIONS.md` entry records the completion — noted here since it isn't being backfilled as a full decision entry.

**Straggler:** `Hora/Parashari/Saravali/saravaliofkalyan01kalyuoft.pdf` still sits **inside this repo** too (gitignored by `*.pdf`, uncommitted), duplicating the copy in `sanskrit-texts-sources/`. Not cleaned up here — flag for a future pass.

## Completed

- ✅ **Hora recategorized into schools** (`1cccca6`) — flat `Hora/<Text>/` → `Hora/{Parashari,Nadi,Prashna,Jaimini}/<Text>/`, ~194 renames. See `docs/DECISIONS.md` 2026-08-12 (backfilled).
- ✅ **New texts ingested:** Apastamba Dharma Sutra + Apastamba Paribhasha Sutra, Kalpa Grhyasutra (Asvalayana), Saravali chapters (`4258491`); four raw Dharmashastra source texts (`7fbfae1`).
- ✅ **Corpus wiki + generator** — `scripts/gen_inventory.py` → `docs/INVENTORY.md`, `docs/README.md` front page, root `.propagates.yml` producer→consumer edge to astroacharya (`c2cc99b`).
- ✅ **Source-out-of-git policy** — `*.pdf` + `**/raw/` gitignored; canonical form is per-chapter JSON (`b4aa78f`).
- ✅ **All 14 (original-registry) texts at 100% translation** — full registry in `CLAUDE.md`. Shipped 2026-06-20 (`3792b90`).
- ✅ **Uniform-schema normalization sweep** — 137 modified + 165 consolidated files onto the `CLAUDE.md` schema; counts deduplicated by `(chapter, shloka)` (`f2034e2`). See `docs/DECISIONS.md` 2026-06-20. Note: 18 newer files (see P1 above) have since landed off this schema and need a follow-up sweep.
- ✅ **Caught up to workspace conventions** — `docs/plans/README.md`, `.gitignore` un-ignore of `docs/`, and **T33 per-project hygiene hooks** (`b13cd88`, `da480bd`); registered in workspace `docs/conventions/CONTEXT-BUDGET.md [active_lines]`.
- ✅ Digitize and translate Kalidasa's *Uttara Kalamrita* (324 shlokas across 9 chapters) into English and Hindi, bringing the entire text to 100% translated.
- ✅ Translate the Uttarakhanda section (Chapters 40–71) of Minaraja Shrivriddhayavanajataka (1,887 shlokas across 34 JSON files) into English and Hindi, bringing the entire Minaraja text to 100% translated.
- ✅ Digitize the Uttarakhanda section (Chapters 40–71) of Minaraja Shrivriddhayavanajataka (Volume II, Baroda 1976), adding 1,887 shlokas across 34 JSON files.
- ✅ Completed all remaining 270 untranslated shlokas for Brihat Samhita (chapters 93–106) in `Varahmihir_brihatsamhita.json` and all 1026 untranslated shlokas in `Varahmihir_brihatsamhita2.json`, bringing both files to 100% translated.
- ✅ Completed all remaining 152 untranslated shlokas for Jataka Parijata (chapters JP_014, JP_017), bringing it to 100% translated.
- ✅ Completed all remaining 10 untranslated shlokas for Minaraja Shrivriddhayavanajataka (chapters MS_014, MS_015, MS_024अ), bringing it to 100% translated.
- ✅ Completed all remaining 63 untranslated shlokas for Phaladeepika (chapters 24, 26, 27, 28), bringing it to 100% translated.
- ✅ Completed all remaining 49 untranslated shlokas across Chapters 84, 86, 87, 88, 89, and 90 in `BPHS8190.json`, bringing the entire file (Chapters 81–90) to 100% translated.
- ✅ Digitize Phaladeepika (chapters + shlokas JSON).
- ✅ Digitize Shatpanchashika (chapters + shlokas JSON).
- ✅ Digitize Shivasvarodayah (chapters + shlokas JSON).
- ✅ English + Hindi translations for all Aarchjyotisham shlokas (`11d936a`).
- ✅ Reorganize texts into canonical Jyotisha categories (`dbba4f2`).

## Linked plans

- [`REFERENCES.md`](./REFERENCES.md) — source-of-truth proofreading references.
- [`AGENTS.md`](./AGENTS.md) — agent-facing context.
- [`docs/BPHS_Master_Lexicon.md`](./docs/BPHS_Master_Lexicon.md) — BPHS terminology.
- [`docs/BPHS_Only_Terminology.md`](./docs/BPHS_Only_Terminology.md) — BPHS-exclusive terminology.

### Related gstack ledgers (scratch / memory — not plans)

- `~/.gstack/projects/Rupali59-sanskrit-texts/` (if present) — designs / reviews / learnings.
