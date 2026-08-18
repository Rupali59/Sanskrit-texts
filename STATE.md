# sanskrit-texts — State

Last updated: 2026-08-17

Convention: `../docs/conventions/STATE_MANAGEMENT.md` (adopted 2026-06-09).
Decisions: [`docs/DECISIONS.md`](./docs/DECISIONS.md) (project `docs/` is tracked).
Plans: [`docs/plans/README.md`](./docs/plans/README.md) (adopted 2026-06-20, 6th sibling).
Supersedes: `TODO.md` — its digitization checklist is subsumed below; the file itself was deleted 2026-08-17 (git history keeps it).

## Recently shipped

Five commits on `main` since the last update (all 2026-07-17 except the last), clean tree:

- `1cccca6` `refactor(corpus):` recategorize Hora into schools + ingest new texts — ~194 renames. New tree: `Hora/Parashari/` (BrihatJataka, BrihatParasharaHoraShastra, Chamatkarchintamani, Jatakaparijatah, JatakaTattvam, Laghujatakam, MinarajaYavanajataka, Phaladeepika, Saravali, SarvarthaChintamani, Shatpanchashika, UttaraKalamrita, VarahamihirDaivagnavallabh), `Hora/Nadi/` (Bhrigusootram + ChandraKalaNadi `.placeholder`), `Hora/Prashna/` (PrashnaMarga), `Hora/Jaimini/` (JaiminiSutras `.placeholder`). Also added new digitized chapter stores + new category trees (`Dharmashastra/`, `Muhurta/`) and committed `scripts/digitize.py` + `scripts/translate.py`. See `docs/DECISIONS.md` 2026-08-12 (backfilled).
- `4258491` `feat(corpus):` Apastamba sutras, Kalpa Grhyasutra, Saravali chapters — +22,027 lines. New top-level `Kalpa/` category.
- `c2cc99b` `docs:` corpus wiki — `docs/INVENTORY.md` + `docs/README.md` front page; root `.propagates.yml` declares `docs/INVENTORY.md` → astroacharya `reference.md` + `DATA_GAPS.md`. (The generator this commit added, `scripts/gen_inventory.py`, was retired 2026-08-17 — see DECISIONS.)
- `b4aa78f` `chore:` gitignore source scans — `*.pdf` + `**/raw/`; source-out-of-git policy.
- `7fbfae1` (2026-08-10) `feat(corpus):` four new raw Dharmashastra source texts (`Dharmashastra/{4605,4607,4609,4617}.txt`) — raw, NOT yet chunked into JSON. Also re-tagged two `hora_acharya` targets in `.propagates.yml` to `kind: prose`. See `docs/DECISIONS.md` 2026-08-12 (backfilled).

**Corpus is now 23 texts / 589 chapters / 7 live categories** (per `docs/INVENTORY.md`) — the old "all 14 texts 100%" claim in the 2026-06-20 entry below is obsolete. Corrected 2026-08-17: this read "240 chapter files" because `gen_inventory.py` counted `*.json` and labelled it "Chapters". That was invisibly wrong while most texts were one file per chapter, and became plainly wrong when BPHS was consolidated and reported **1** chapter for a 97-chapter work. The generator now counts real `chapters[]` entries; all 23 rows verified against the data.

## Now (in flight)

### 2026-08-18 — one format; sources and translations separated

Rationale in [`docs/DECISIONS.md`](./docs/DECISIONS.md) 2026-08-18. What is now true:

- **Every digitised text is one file**: `<Category>/<School?>/<Text>/<Text>.json`.
  230 JSON files → **35**. Data unchanged and proved: chapters **589 → 589**, shlokas
  **25,301 → 25,301**, ingestible **17,764 → 17,764**.
- **Sources are now declared** (2026-08-18): 14 coarse edges, one per text, from
  `../sanskrit-texts-sources/<Text>/<transcription>.md` to the derived `<Text>.json`.
  They sit in **this** repo's tracked sidecar, not in the sources tree — that tree is
  gitignored, so a sidecar there would be lost on a clone. All 14 resolve; they stay
  NEVER_VERIFIED because nobody has yet read a transcription against its JSON.
- **This repo is the translation layer only** — `.json` + `README.md`. All 32 source files
  (14 `.md`, 17 `.txt`, 1 raw `.json`) now live in `../sanskrit-texts-sources/`, mirroring
  the same tree. `.gitignore` enforces it; its two dead rules were removed.
- Saravali's 17MB PDF deleted — byte-identical duplicate of the sources copy. This clears
  the straggler previously flagged here.

**Not yet on the one-file rule, each for a reason:**

| Text | Blocker |
|---|---|
| `ManuSmriti`, both Apastamba | `sutras[]` shape — needs **re-digitisation**, see P1 |

**Carrying known duplicates, consolidated anyway** (layout does not affect them — the
seeder dedupes by `(chapter, shloka)` across all files of a `text_id`):
`Jatakaparijatah` 55, `Laghujatakam` 14, `MinarajaYavanajataka` 1.

**13 undigitised text dirs** are invisible to `docs/INVENTORY.md` by construction — it
defines a text as a dir holding JSON. Listed in `CLAUDE.md`. `GargaSamhita` and
`MuhurtaMartanda` already have sources waiting.


### 2026-08-17 — corpus normalisation + BPHS consolidation

Full rationale in [`docs/DECISIONS.md`](./docs/DECISIONS.md) (three entries dated 2026-08-17).
Summary of what is now true:

- **BPHS is one file** (`BrihatParasharaHoraShastra.json` + `.md`), 97 chapters, 3,937
  shlokas, ingesting **3937 of 3937** (was 3867 of 3932). 4 mis-split chapters repaired and
  5 shlokas recovered; every affected chapter is contiguous 1..N.
- **3 texts migrated** onto the uniform schema — `saravali` 1,163, `asvalayana_grhya_sutra`
  394, `MC_001` 37. Corpus: **225 conformant files, 20,564 normalised shlokas**.
- `CLAUDE.md`'s `category` enum and `text_id` registry corrected from disk; the same stale
  path map in `../astroacharya/scripts/list_sources.py` fixed there.
- `docs/INVENTORY.md` is **hand-maintained**; its generator was retired. Chapter total corrected
  to **589** — the generator counted `MC_REMAINING_RAW.json` (raw `info`/`segments`, not a
  chapter) and had long reported file counts as "chapter files". Verification one-liner is in
  INVENTORY's header; the tree wins when they disagree.

**Open, and none of it mechanical** — see P1 and the 2026-08-17 decisions:

| # | Issue | Needs |
|---|---|---|
| ~~1~~ | ~~`brihat_samhita` two recensions, 2,729 discarded~~ — **resolved 2026-08-18.** Not recensions at all: 2,574 of 2,711 shared keys differed only in sandhi/word-splitting, i.e. one text digitised twice. Consolidated to the union file 2 already won, so ingestion was unchanged at 2,771 and the collision went to **0** | done |
| 2 | 14 files (`manu_smriti` ×12, both Apastamba) blocked on **numbering, not schema** — 4,737 records over 1,520 distinct keys | the source text |
| 3 | ~506 disordered shloka numbers across 25 chapters | the source text |
| 4 | **BPHS translation backlog is exactly 5 shlokas** — 12.11, 53.20, 61.55, 66.43, 66.65 (Sanskrit only). Plus ch 25 shloka 16, absent from the digitisation entirely | translation / digitising |

Corpus ingestion: **17,764 of 20,564** present shlokas.

## Active initiatives

- None.

## Known signal

- `CLAUDE.md` is currently **131 lines / 7,342 bytes** — well under the prior 164/180-line yellow reading (that measurement predated the ⚑-footer trim in the 2026-06-20 data-correctness-audit entry). No size-cap concern right now. The live problem with `CLAUDE.md` is **content staleness**, not size — see Pending below.

## Pending (by priority)

### P1 — Off-schema JSON blocks AstroAcharya ingestion

**14 JSON files use the pre-normalization shape** — top-level `sutras`/`shlokas` with `sanskrit` / `english_translation`, **no `chapters[]` wrapper**, banned by `docs/DECISIONS.md` 2026-06-20. **Blocks AstroAcharya `/texts` ingestion.** Was 18; 4 cleared 2026-08-17/18.

- `Dharmashastra/ManuSmriti/chapters/MS_001.json` … `MS_012.json` (12)
- `Dharmashastra/ApastambaDharmaSutra/chapters/ADS_001.json` (1)
- `Dharmashastra/ApastambaParibhashaSutra/chapters/APS_001.json` (1)

**Cleared:** `Saravali`, `Asvalayana` and `MuhurtaChintamani`'s `MC_001` were migrated onto the schema 2026-08-17; `MC_REMAINING_RAW.json` was raw extraction, not a chapter, and moved to `../sanskrit-texts-sources/` 2026-08-18.

**The remaining 14 need RE-DIGITISATION, not renumbering** — checked against the canonical structures 2026-08-18:

- **Manusmriti**: 12 adhyāyas, ~2,684 verses (ch 1 = 119, ch 2 = 249). The data's leading component runs **1–33**, "chapter 1" holds 1,516 records against 119, and `MS_001` alone contains **89 fragmentary cycles** with gaps (`1.14 → 1.18`) and bare integers mixed in.
- **Apastamba**: the hierarchy is Praśna → Paṭala → Khaṇḍa → sūtra, so **`1.1.1` is a correct citation**, not a broken number. But of 1,437 records, 219 carry a bare integer, 13 are malformed `..10`, and 15 are the literal placeholder **`X.X.21`/`X.X.22`** — the digitiser recording "prefix unknown". 136 restart-cycles of lengths 14, 20, 1, 10, 21, 29, 63…

A first reading of Apastamba's opening 30 records — a clean `1.1.1…1.1.14` run — suggested the numbering was merely truncated and reconstructible. Across the whole file that is false; **a 30-record sample gave the wrong answer about a 1,437-record file.**

Sources are in `../sanskrit-texts-sources/Dharmashastra/`, but `manu_clean.txt` is a **2.8MB scanned book on a single line** (1909 Nirnaya Sagar edition, front matter and Kullūka's commentary included). This is a digitisation project, not a patch.

### P1 — Digitization backlog (in-scope, README-only stubs)

Corrected 2026-08-12 — the 2026-06-20 list was wrong: **Saravali, Surya Siddhanta, Aryabhatiya, and Panchasiddhantika are now digitized**, not stubs.

- **Saravali** — digitized, on-schema since 2026-08-17: `Hora/Parashari/Saravali/Saravali.json`, 1,163 sūtras, single chapter (not chapter-split).
- **Surya Siddhanta** — 14 chapters / 272 shlokas / 100% translated.
- **Aryabhatiya** — 4 padas / 121 shlokas / 100% translated.
- **Panchasiddhantika** — 18 chapters / 166 shlokas / 100% translated.

Genuine stubs remaining:

- **Hora (classical Sanskrit):** SarvarthaChintamani (Venkatesa Sharma), PrashnaMarga (Kerala horary, now `Hora/Prashna/`), JatakaTattvam
- **Siddhanta (mathematical astronomy):** Brahmasphuta Siddhanta, Siddhanta Shiromani
- **New since 2026-06-20:** `Muhurta/MuhurtaMartanda/` (README; its empty `chapters/` removed 2026-08-18, PDF waiting in sources), `Samhita/GargaSamhita/` (README; raw `3003.txt` now in sources), `Dharmashastra/Dharmasindhu/`, `Dharmashastra/NirnayaSindhu/`, `Hora/Jaimini/JaiminiSutras/` (`.placeholder`), `Hora/Nadi/ChandraKalaNadi/` (`.placeholder`)
- **Permanently non-digitizable — lost recensions, not backlog:** `Vedanga-Jyotisha/Samaveda/`, `Vedanga-Jyotisha/Atharvaveda/`. Record as such, don't carry as pending work.

### P2 — Corpus hygiene / doc drift (recorded, not fixed here)

- `CLAUDE.md` layout block + text_id registry still show the pre-`1cccca6` flat `Hora/<Text>/` paths — all now wrong (correct tree is `Hora/{Parashari,Nadi,Prashna,Jaimini}/<Text>/`). Its `[README-only stubs]` line is also stale (references texts now digitized).
- ~~`CLAUDE.md` `category` enum missing values~~ — **fixed 2026-08-17**: now the 8 values the data uses. `hora` was retired by `1cccca6` and its last user (`SV_FULL.json`) was migrated.
- Root `README.md` ~3 months stale: still shows the flat Hora tree, `Tantra/` and `SamudrikShastra/` sections (both removed 2026-06-20), the 4 now-digitized texts listed as "not yet digitized," and the pre-normalization Schema A/B (`english_meaning`, `source`, `header`, `book`) that `docs/DECISIONS.md` 2026-06-20 banned.
- ~~`docs/INVENTORY.md` "Source held" stale~~ — **mostly fixed 2026-08-17**: Panchasiddhantika/SuryaSiddhanta/MuhurtaChintamani now read `—`. **Saravali's `pdf` is correct** — it still holds a 17MB `saravaliofkalyan01kalyuoft.pdf` locally (gitignored per the source-out-of-git policy). Maintained by hand now; the generator that regenerated it was retired.
- `.gitignore` lines 8–9 are dead rules — they ignore pre-recategorization paths `Hora/UttaraKalamrita/raw_uttara_kalamrita.txt` and `Hora/UttaraKalamrita/sections/`, but those files moved to `Hora/Parashari/UttaraKalamrita/` in `1cccca6` and the sections were then committed as chapter JSON.
- ~~`scripts/digitize.py` + `scripts/translate.py` committed against the "Do not commit processing scripts" rule~~ — **resolved 2026-08-17**: both deleted, along with `scripts/gen_inventory.py`. `scripts/` now holds only `install-hooks.sh`, which wires the hygiene githooks and is not a processing script.
- The 4 raw `Dharmashastra/{4605,4607,4609,4617}.txt` (from `7fbfae1`) await chunking into per-chapter JSON.

### P2 — Translation injection

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
- ✅ **Corpus wiki** — `docs/INVENTORY.md`, `docs/README.md` front page, root `.propagates.yml` producer→consumer edge to astroacharya (`c2cc99b`). The generator shipped alongside it was **retired 2026-08-17**; INVENTORY is hand-maintained.
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
