# STATE.md — 2026-09-14 drain

Full text removed from `propagation/state/sanskrit-texts/STATE.md` on 2026-09-14 (task S2,
workspace hygiene drain — STATE.md was 1,309 lines against a 200-line cap; see
`~/Documents/GitHub/Vipin Kaushik/docs/conventions/CONTEXT-BUDGET.md` for the cap). Moved
verbatim, in chronological order — search here for detail rather than trusting a summary.
STATE.md keeps: the header, the single live **OPEN** item (Sāravalī re-ingestion), the
"Now (in flight)" / "Active initiatives" / "Known signal" shells, and pointers to
`docs/INVENTORY.md` and this file.

**Two findings below exist ONLY here, not duplicated in `GOTCHAS.md` or
`CANONICAL_COUNTS.md`:** the cross-pass OCR agreement instrument (diffing `-l san` vs `-l hin`
readings of the same page images as mutual witnesses, no external witness needed) and the
duplicate-subagent-write process finding — both under "2026-09-04 · Eight parallel lanes"
below. A third finding worth flagging the same way, under the Pending block's "RESOLVED
2026-09-04 — `brihadaranyaka.py`" entry: the sandhi-echo alignment technique (`F_i` is `C_i`
with sandhi undone; the marker resets the recursion so an error cannot propagate past the next
mantra) is likewise not recorded elsewhere. Two other findings that look unique on a first read
are NOT — "a source that looks markerless is a claim about the PROBE" is also in
`sanskrit-texts/docs/CANONICAL_COUNTS.md:1858`, and the G-numbered gotchas (G6–G48) referenced
throughout are all filed in `propagation/state/sanskrit-texts/GOTCHAS.md`.

*Ordered oldest to newest below by each block's own date. The first block (`## Completed`) is
an undated legacy list — placed first as the oldest, pre-dating the commit log that follows.*

---

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

---

## Recently shipped

Five commits on `main` since the last update (all 2026-07-17 except the last), clean tree:

- `1cccca6` `refactor(corpus):` recategorize Hora into schools + ingest new texts — ~194 renames. New tree: `Hora/Parashari/` (BrihatJataka, BrihatParasharaHoraShastra, Chamatkarchintamani, Jatakaparijatah, JatakaTattvam, Laghujatakam, MinarajaYavanajataka, Phaladeepika, Saravali, SarvarthaChintamani, Shatpanchashika, UttaraKalamrita, VarahamihirDaivagnavallabh), `Hora/Nadi/` (Bhrigusootram + ChandraKalaNadi `.placeholder`), `Hora/Prashna/` (PrashnaMarga), `Hora/Jaimini/` (JaiminiSutras `.placeholder`). Also added new digitized chapter stores + new category trees (`Dharmashastra/`, `Muhurta/`) and committed `scripts/digitize.py` + `scripts/translate.py`. See `docs/DECISIONS.md` 2026-08-12 (backfilled).
- `4258491` `feat(corpus):` Apastamba sutras, Kalpa Grhyasutra, Saravali chapters — +22,027 lines. New top-level `Kalpa/` category.
- `c2cc99b` `docs:` corpus wiki — `docs/INVENTORY.md` + `docs/README.md` front page; root `.propagates.yml` declares `docs/INVENTORY.md` → astroacharya `reference.md` + `DATA_GAPS.md`. (The generator this commit added, `scripts/gen_inventory.py`, was retired 2026-08-17 — see DECISIONS.)
- `b4aa78f` `chore:` gitignore source scans — `*.pdf` + `**/raw/`; source-out-of-git policy.
- `7fbfae1` (2026-08-10) `feat(corpus):` four new raw Dharmashastra source texts (`Dharmashastra/{4605,4607,4609,4617}.txt`) — raw, NOT yet chunked into JSON. Also re-tagged two `hora_acharya` targets in `.propagates.yml` to `kind: prose`. See `docs/DECISIONS.md` 2026-08-12 (backfilled).

**Corpus size: derive it, never read it here** — the command is in `CLAUDE.md`, and `docs/INVENTORY.md` is the registry. This line asserted `57 / 927 / 91,782` on 2026-08-24 and `58 / 930 / 92,832` twelve lines below at the same moment; on 2026-08-25 the true figure was **56 / 918 / 92,166** and both were stale. Two hand-maintained counts in one file, disagreeing with each other and with the data, is exactly what `rule:state-and-decisions` names as the fastest-rotting thing in a state file — the old "all 14 texts 100%" claim in the 2026-06-20 entry below is obsolete. Corrected 2026-08-17: this read "240 chapter files" because `gen_inventory.py` counted `*.json` and labelled it "Chapters". That was invisibly wrong while most texts were one file per chapter, and became plainly wrong when BPHS was consolidated and reported **1** chapter for a 97-chapter work. The generator now counts real `chapters[]` entries; all 23 rows verified against the data.

---

## Now (in flight)

### 2026-08-24 (PD) — Mānasāra lands from the source's own headings

**Corpus 49 → 50 texts · 48,289 shlokas · 10 categories.** Validator failing list unchanged
(8); dedupe loss still exactly 71.

- **Mānasāra: 70 chapters = canonical 70**, 5,169 verses, 0 duplicates, with a Devanagari
  chapter title for each. From its **71 named headings**, not from verse numbers.
- **The parallel manual work turned out to be unnecessary.** Both Mānasāra and Mayamata
  state their structure in `==` headings; the plan's Phase B is obsolete.
- **G20 recorded**: do not delete headings — `strip_code` keeps their words, so the fix for
  the title leaking into verse 1 is to remove the NODE, not to abandon the structure.
- **Mayamata: structure solved, blocked on source quality.** 36 chapters from its own
  numbered headings, appendix excluded, 22 of 36 clean — but **69 duplicate verse numbers**
  across 14 chapters (37 in ch 25 alone). Ingesting would lose 69 verses silently (G8).

**Next:** Mayamata needs **69 verses checked against a printed edition** — known positions,
3 of them uniquely determined by their neighbours (ch 7 verse 42 is transcribed `1`). That
is the whole remaining task. Suśruta is still unassessed.

### 2026-08-24 (PA–PC) — G16 fixed at the root; `bare` grammar added; Caraka BLOCKED

Corpus unchanged at **49 texts · 43,120 shlokas**; validator failing list unchanged (8);
dedupe loss still 71.

- **G16 fixed structurally, 25 → 3.** `sd_body()` scopes to `<pre itemprop="text">` and
  drops the `<h2 itemprop="name">` inside it — verified 28/28 files. The three that remain
  each have a stated reason. Gated by a before/after diff over all 43,049 verse keys.
- **The diff gate caught G17 on the first attempt.** Python's `\d` is Unicode-aware, so a
  strip written for ASCII line numbers ate Taittirīya's anuvāka numbers — **3,023 verses
  changed that should not have**, with counts, contiguity, `ref` round-trip and validator
  all still green. Reverted, fixed, re-run clean.
- **`bare` grammar added, opt-in only.** A count threshold was not enough: per-unit
  detection flipped 4 of the Rigveda's 1,027 sūktas and moved it 10,449 → 10,464. It is now
  a property of the wikisource path, passed explicitly.
- **`parse_wikisource` had NO CALLER** since it was written — `main` globbed only
  `*.json`/`*.html`. Now returns content and is wired in.
- **Caraka BLOCKED (tier `defect`)** — its markers number Cakrapāṇidatta's commentary, not
  the mūla. G18.

**Next:** Suśruta, Mānasāra and Mayamata are unblocked by the `bare` grammar — **but check
each for the Caraka problem first** (grep the commentary's name, compare the inferred
chapter count against canon). Mānasāra's 408k characters and Mayamata are mūla-shaped on
inspection; Suśruta is unverified.

### 2026-08-24 (P1) — taxonomy verified and corrected; Kalpa to Youvan

**Corpus 49 → 48 texts · 42,893 shlokas · 8 categories.** Validator's failing list unchanged
(8, pre-existing); dedupe loss still 71.

Started from "is the Rigveda divided into 4 puruṣārtha and some skills?" — puruṣārtha is not
a textual division of anything, and the "skills" are the six **Vedāṅga**, limbs serving all
four Vedas. Checking that against the tree found two real defects, both now fixed:

- **`Samhita/` held two unrelated senses of one word.** It is the Jyotiṣa skandha (Horā /
  Siddhānta / Saṃhitā); the five Vedic Saṃhitās moved to **`Veda/`**. Audit now shows one
  category per directory, none split.
- **Nothing recorded that `Kalpa/` and `Vedanga-Jyotisha/` are one axis** — two of six
  Vedāṅgas were held while `VEDIC_CORPUS.md` said one.
- **Kalpa → Youvan** (ritual-adjacent split), 394 verses, committed there before removal.
- **Latent case bug (G14)** and the corpus/sources mirror hazard (G15) recorded.

**Found and fixed en route:** `Tushar/Youvan/texts/Stotra/` was **untracked** — the
2026-08-23 GargaSamhita relocation was logged as done but never committed, leaving 127
shlokas with no other copy anywhere. Now committed.

**Next:** P2 is the publication gate — drafts must never occupy `english`/`hindi`, because
nothing filters on `status` today and the API would serve unverified machine text. That
blocks all translation work.

### 2026-08-24 (later) — TODO 1 and TODO 2 closed; the second witness found a real defect

**Corpus 43,263 → 43,287 shlokas.** Validator's failing list unchanged (8, all
pre-existing); dedupe loss re-measured, still exactly 71.

- **TODO 1 — `acquire.py` writes as it fetches and resumes.** The docstring's "reconciler
  … already present is skipped without touching the network" was true of no code path;
  every run re-fetched everything and wrote only at the end, so a failure at page 900 of
  1,028 discarded all 900. Resume is safe because the write is atomic. `--verify-only` now
  *raises* rather than reaching the network. 8 new tests, 4 mutations checked. Measured: 40
  Śukla YV pages from disk in 2.5s where the old code timed out at 120s.
- **TODO 2 — done as a SELECTIVE re-fetch (3 pages), per the 2026-08-23 decision**, not the
  ~1,700-request bulk fetch that decision stopped.
  - **RV 8.66 was mislabelled, not missing.** The ODbL source's `sukta: 67` record is
    8.66's text (byline `कलि: प्रागाथ:`, `१५ अनुष्टुप्`), and the real 8.67 (21 verses) was
    absent. Relabelled + supplied. Maṇḍala 8 is now 103 sūktas, no gaps. **A count check
    could never have found this** — 102 present, one gap, everything self-consistent.
  - **AV 20.3 filled** (source carried the header and no verse text).
  - **AV 20.13 stays BLOCKED**: Wikisource's `०१३` page is an orphaned duplicate of 20.012.
    Filling from it would have put sūkta 12's text under 13 and still passed every count
    check. Declared in `known_gaps`; needs a third witness. See GOTCHAS G12.
- **24 verses are now CC BY-SA 4.0 inside otherwise-ODbL files.** Declared per-file in
  `structure.secondary_sources`. **Open decision, not resolved** — `docs/LICENSES.md`.

### 2026-08-24 — the Vedic corpus lands; INVENTORY becomes the single registry

**49 texts · 775 chapters · 43,263 shlokas · 9 categories.** Derive it, never restate it —
the command is in `CLAUDE.md` §text_id registry. Up from 20 / 17,835 on 2026-08-22.

- **All five Saṃhitās convert.** Rigveda 10,449 · Atharvaveda 6,088 · Śukla YV 1,965 ·
  Taittirīya 2,294 · Sāmaveda 1,866. Plus 24 Upaniṣads.
- **Two blockers resolved, one exclusion held.** Taittirīya's markers turned out to be
  kāṇḍa.prapāṭhaka.anuvāka citations, and reading them that way matches the researched
  anuvāka counts exactly in 6 of 7 kāṇḍas. Sāmaveda hit a real regex bug (`trailing`
  backtracking into a numeral, so `॥ ११४ ॥` matched as `११`) — see GOTCHAS G11. **Nirvāṇa
  stays excluded** deliberately: prose aphorisms, no verse numbering. **RV 1.65 stays
  open** and is a scholarly decision, not a parser tweak.
- **Nine Sāmaveda verses are absent from the source**, enumerated in
  `structure.known_gaps` rather than renumbered away. Its tier moved `firm` → `range`.
- **`docs/INVENTORY.md` is now the `text_id` registry**; `CLAUDE.md` points at it instead
  of carrying a second copy. The two had drifted to 20 rows against 23.
- **`list_sources.py`'s path map is derived from the corpus**, not hardcoded. astroacharya
  suite green at **1050 passed**.
- **Dedupe loss re-measured across all 49 texts: still exactly 71**, all pre-existing. The
  29 new texts add zero duplicate keys.

**Not done, deliberately:** `.propagates.yml` edges for the new source→corpus couplings.
Deferred by Rupali 2026-08-24 while propagation is being fixed; TODOs follow that work.
Per `rule:adversarial-review-reads-the-ledger`, until those edges exist a green propagate
over this tree means "not looking", not "clean".

### 2026-08-23 — translation backlog closed; two "ready" sources turned out not to be

**The normalized corpus is 20 texts · 17,835 shlokas · 100% translated · zero gaps.**
Derive it, do not restate it:

```
cd <repo> && python3 -c "import json,glob;print(sum(len(c['shlokas']) for p in glob.glob('**/*.json',recursive=True) if not p.startswith('docs/') for c in (json.load(open(p)).get('chapters') or [])))"
```

Four parallel lanes ran against the pending-work audit. Working tree, uncommitted:

- **Translation gaps closed.** `bphs` 3937/3937 (last 5 — `12.11`, `53.20`, `61.55`,
  `66.43`, `66.65` — translated; all single-pada fragments, a shape occurring 13 other
  times in the text). `muhurta_chintamani` 206/206 (MC_001's 37 missing Hindi supplied).
  Both figures re-measured independently after the lane reported them.
- **`muhurta_chintamani` chapter-1 numbering still wrong** and deliberately not "fixed".
  11–32, 1–7, 37–44 — distinct, so it ingests. `MC_REMAINING_RAW.json` does **not**
  resolve it: pages 53–480, zero textual overlap with chapter 1. Needs the PDF's
  chapter-1 pages against a canonical edition. See GOTCHAS G7.
- **GargaSamhita relocated to Youvan.** Its source was the devotional Vaishnava Purana,
  not the Jyotish work. 127 shlokas now at
  `Tushar/Youvan/texts/Stotra/KrishnaSahasranamaStotram/`; this directory is a stub again
  with **no source waiting**. See DECISIONS 2026-08-23 — including that the 2026-06-20
  SamudrikShastra relocation this followed **never completed its second half**.
- **MuhurtaMartanda cannot be digitised from the held PDF.** OCR was authorised and run
  (154 pages, `tesseract -l san+hin`); no JSON was produced and the raw output stays in
  the sources repo's raw tier. Two blockers: the scan has no text layer and OCRs corrupt
  (94% Devanagari by character class, substantively wrong), and the edition is a
  three-layer commentary edition that marker-splitting cannot separate. Needs sourcing,
  not processing. See DECISIONS 2026-08-23 and GOTCHAS G3–G5.
- **Dharmashastra re-digitisation scoped** — `docs/plans/2026-08-22-dharmashastra-redigitisation.md`.
  Confirms the 2026-08-18 conclusion; corrects the "leading component runs 1–33"
  description (it is invariantly `1`; the *second* component cycles to 315); finds
  `apastamba_paribhasha_sutra` equally broken rather than minor. Sources identified:
  `4605`/`4617` = Apastamba Dharmasutra, `4607` = Apastamba Paribhasha Sutra. **`4609`
  remains unidentified** — a Sravani/Upakarma ritual manual fitting no existing directory;
  left unplaced by decision rather than guessed.
- **`docs/GOTCHAS.md` created** at `propagation/state/sanskrit-texts/GOTCHAS.md` — 10
  entries, this repo's first.

**Translation of the three Dharmashastra texts stays blocked** behind re-digitisation.
Translating 4,737 fragmentary records would produce translations of the wrong units.

### 2026-08-18 — one format; sources and translations separated

Rationale in [`docs/DECISIONS.md`](../DECISIONS.md) 2026-08-18. What is now true:

- **Every digitised text is one file**: `<Category>/<School?>/<Text>/<Text>.json`.
  230 JSON files → **35**. Data unchanged and proved: chapters **589 → 589**, shlokas
  **25,301 → 25,301**, ingestible **17,764 → 17,764**.
- **Sources are now declared** (2026-08-18): 14 coarse edges, one per text, from
  `../sanskrit-texts-sources/<Text>/<transcription>.md` to the derived `<Text>.json`.
  They sit in **this** repo's tracked sidecar, not in the sources tree — that tree is
  gitignored, so a sidecar there would be lost on a clone. All 14 resolve; they stay
  NEVER_VERIFIED because nobody has yet read a transcription against its JSON.
- **This repo is the translation layer only** — `.json` + `README.md`. All 32 source files
  (14 `.md`, 17 `.txt`, 1 raw `.json`) now live in `../../../sanskrit-texts-sources/`, mirroring
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

Full rationale in [`docs/DECISIONS.md`](../DECISIONS.md) (three entries dated 2026-08-17).
Summary of what is now true:

- **BPHS is one file** (`BrihatParasharaHoraShastra.json` + `.md`), 97 chapters, 3,937
  shlokas, ingesting **3937 of 3937** (was 3867 of 3932). 4 mis-split chapters repaired and
  5 shlokas recovered; every affected chapter is contiguous 1..N.
- **3 texts migrated** onto the uniform schema — `saravali` 1,163, `asvalayana_grhya_sutra`
  394, `MC_001` 37. Corpus: **225 conformant files, 20,564 normalised shlokas**.
- `CLAUDE.md`'s `category` enum and `text_id` registry corrected from disk; the same stale
  path map in `../../../astroacharya/scripts/list_sources.py` fixed there.
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

---

## ~~Open decision~~ — RESOLVED 2026-08-24: mixed depth

**This blocks Aṣṭāṅgasaṃgraha and is a live defect in committed Caraka.** It is a key-schema
question, not a parser question: astroacharya's `@source` citations resolve against these
keys, so the answer is a one-way door.

**The situation.** Some SARIT texts carry a level below the adhyāya:

| text | third level | verses affected | state today |
|---|---|---:|---|
| Caraka | 8 pādas of Cikitsā 1–2 | 269 | **merged in the committed file** — key `6.1.81` is 11,211 chars, `6.2.53` is 6,264, against a median of 87 |
| Aṣṭāṅgasaṃgraha | Kalpasthāna Paribhāṣā | 119 | blocked; would glue into one 12,159-char verse |

**The constraint.** `validate_corpus.py:236` requires every key in a text to have exactly
`len(structure.levels) - 1` components. Splitting the subsections out works and gives keys
like `8.1.1` / `1.1.1`, but the rest of each text is depth 2. No depth-2 encoding survives:
`1.1-5` fails `DOTTED` and all three of `HALF_SHLOKA`, `DEVANAGARI_SUFFIXED`, `SUB_NUMBERED`.

**The options, as I see them:**

1. **Allow mixed depth** — relax the validator to `len(comps) <= want` and declare `levels`
   as the maximum. Cheapest, and honest about texts that genuinely vary. Weakens a check
   that currently catches real parse errors.
2. **Uniform depth per text, padding the missing level** — every Caraka key becomes
   `adhyāya.pāda.verse` with a filler where there is no pāda. Keeps the check strict but
   **invents a component**, and renumbers every existing Caraka key.
3. **Extend the accepted key forms** — add a `SUB_NUMBERED`-style pattern that carries the
   subsection inside the verse component. Keeps depth 2 and does not renumber existing keys,
   but adds a fourth special-case key syntax.

**Rupali chose (1)** — `structure.levels` declares the MAXIMUM depth; `validate_corpus.py`
relaxed from `!= want` to `> want`, and a decrease that is a DESCENT into a subsection is no
longer read as a restart. Both directions that catch real defects still fire and are pinned
by tests, mutation-checked.

**Outcome:** Aṣṭāṅgasaṃgraha landed at 9,382 verses; Caraka's merged pādas repaired,
**9,256 → 9,525**, and its two monster verses (11,211 and 6,264 characters) are gone.

**One honest cost, measured rather than buried:** the descent allowance suppresses **34** of
`apastamba_dharma_sutra`'s 1,024 errors. That text is off-schema, already fails, and still
reports 990 errors — no healthy text loses a single finding.

### What is still missing, surveyed 2026-09-02 after the Siddhānta Śiromaṇi work

**Derive it, do not trust this list — the command is the record:**

```sh
python3 - <<'PY'
import os,glob,json
src,cor="sanskrit-texts-sources","sanskrit-texts"
have={os.path.relpath(os.path.dirname(p),cor) for p in glob.glob(f"{cor}/**/*.json",recursive=True) if '/docs/' not in p}
texts=set()
for r,d,f in os.walk(src):
    if not [n for n in f if n.endswith(('.txt','.pdf','.xml','.wikitext'))]: continue
    parts=os.path.relpath(r,src).split(os.sep)
    while parts and parts[-1] in ('raw','sections','images'): parts.pop()
    if parts and parts[0] not in ('.','docs'): texts.add(os.sep.join(parts))
print(sorted(texts-have))
PY
```

**Measured that day: 55 source text-dirs, 41 digitised, 14 not.** Fold `raw/` and `sections/`
into the parent before comparing — a naive directory diff counts every `raw/` as undigitised and
reported 24.

**Nine of the 14 are correctly excluded, not missing:** `TaittiriyaAranyaka` and
`TaittiriyaBrahmana` are **Youvan's scope**; `Amritanada`, `Brahmabindu`, `Tejobindu`,
`Yogatattva` are the four Yoga Upaniṣads that left 2026-08-25; `Nirvana` is a deliberate
exclusion (prose aphorisms, nothing for a verse-numbered schema); `GargaSamhita`'s file is the
Vaiṣṇava Purāṇa; and the four loose `Dharmashastra/*.txt` are the 46xx sources, one of which
became Āpastamba.

**So five are genuinely actionable, ranked by how tractable the numbering is:**

| target | markers | +1 steps | state |
|---|---|---:|---|
| `SarvarthaChintamani` | 1,957 | **78%** | **closest** — see below |
| `Dharmasindhu` | 217 | 50% | mostly Hindi ṭīkā prose; needs the mūla/ṭīkā split |
| `NirnayaSindhu` | 555 | 21% | OCR |
| `MuhurtaMartanda` | 776 | 13% | OCR, numbering poor |
| `GargaHora` | — | — | scan, not yet OCR'd |

~~**OPEN** — **`SarvarthaChintamani` is close but blocked on CHAPTER segmentation.**~~ —
**CLOSED 2026-09-04 (`bd75202`).** The missing chapter witness was inside the source file all
along: **English `CHAPTER-N` running headers in the bilingual edition** — both attempts below
probed only for Devanāgarī markers and never saw it. This is the same transferable finding
already recorded above under "The finding that outlives the texts": *a source that looks
markerless is a claim about the PROBE, not the source.*

`sarvartha_chintamani` is now HELD at **17 chapters / 1,227 units**
(`Hora/Parashari/SarvarthaChintamani/SarvarthaChintamani.json`, verified today),
`count_authority: supported`, cross-checked against the edition's own printed table of
contents (17 titled chapters, gapless page ranges 3–371), character-density across every
inter-boundary span, and the one surviving colophon: chapter 6's closing colophon states verse
count 113, and the parser's 112 content verses + 1 dropped closing colophon matches it exactly.

*Superseded detail, kept for the record — the two segmentation attempts that failed before the
running-header witness was found:*

Reset-based segmentation over-split to **89** chapters while capturing only 223 of the 1,227
candidates. **Retried 2026-09-02 with the technique that solved Pañcasiddhāntikā — the greedy
next-expected walk — and it does NOT transfer.** It produced 39 chapters of 630 verses, every
one perfectly contiguous `1..N`, which looks like success and is not: **the text's own colophon
says chapter 6 ends at verse 113**, and this walk gives chapter 6 nineteen verses. Real chapters
are long; the walk splits them wherever an OCR-lost number breaks the sequence and the next `1`
reads as a fresh chapter. **Perfect contiguity is what a wrong segmentation looks like here**,
because the walk only ever admits consecutive numbers — do not take `1..N` per chapter as
evidence on a new text without first checking for a non-Devanāgarī chapter witness.

**All three fabricated Siddhānta texts were resolved later the same day** — `aryabhatiya`
replaced (80 genuine verses, `822d66c`), `panchasiddhantika` replaced (386 verses, `805fd56`),
`surya_siddhanta` deleted outright. This paragraph asserted they were unchanged until 2026-09-04.
See their P0 items.

---

## Outstanding acquisitions — what is still to get (derived 2026-08-24)

**Held: derive it.** The command is in `CLAUDE.md`. This line used to carry the number as
well as the instruction not to, and the number was wrong — see the note above.

### 0 · The census — 20 texts pending, bucketed by REASON

| Why it is not here | Count | Texts |
|---|---:|---|
| **Blocked but fixable** | **0** | — `narada_smriti` was the last, closed 2026-08-24 |
| **No source in our channels** — surveyed 2026-08-25 | **13** | `GargaSamhita`, `Dharmasindhu`, `NirnayaSindhu`, `BrahmasphutaSiddhanta`, `SiddhantaShiromani`, `MuhurtaMartanda`, `SarvarthaChintamani`, `JatakaTattvam`, `PrashnaMarga`, `JaiminiSutras`, `ChandraKalaNadi`, Nirukta, Samarāṅgaṇa Sūtradhāra |
| Blocked on the sūtra schema — **a source exists** | **4** | Aṣṭādhyāyī, Piṅgala, `apastamba_dharma_sutra`, `apastamba_paribhasha_sutra` |
| Needs investigation first | **1** | `ayurvedasutram` — 5 chapter divs, **zero extractable lines** |
| Deferred by decision | **2** | `kautalyarthasastra`, `mahabharata-devanagari` |
| **Distinct total** | **20** | |

**The column now sums to the total, and that is the point of the change.** It used to bucket
by ARTIFACT — an "undigitised" row (a README and no JSON) beside a "no usable source" row —
so `GargaSamhita` and `MuhurtaMartanda` sat in both, the column summed to 22 against a
distinct 20, and the table needed a paragraph of arithmetic to be read. Bucketing by REASON
removes the overlap: a directory is empty *because* there is no source. Same 20 texts.

**The 13 is a measured result, not a backlog.** All 11 undigitised directories plus Nirukta
and Samarāṅgaṇa (which have no directory at all) were surveyed 2026-08-25 across every
channel this pipeline uses — sanskritdocuments, SARIT, Wikisource, and the archive.org links
on the jyotiṣa index. **None has a machine-readable source.** They are blocked on *sourcing*,
not on parsing, and OCR and new channels were both declined the same day.

**sanskritdocuments' jyotiṣa corpus is exhausted**: 25 stems → 13 texts, all 13 held, 0
unmapped. There is no more Jyotiṣa to take from the channels in use. Method, the stem→id
mapping and the four near-homograph false positives: `docs/SOURCES.md`.

**Before deciding how to fix a text blocked on numbering, score it:**
`python3 scripts/sanskrit-convert/fixability.py <text_key>` — measures affected units,
distinct citation shapes and sibling blast radius, and recommends re-acquire / code /
code-opt-in / manual. `--history` replays the seven decisions already made. Rationale and the
threshold's known weakness: `docs/CANONICAL_COUNTS.md`.

**It has already found work not in the table above:** `caraka_samhita` still has ~13 unread
citation lines in 3 shapes, scored **A=6 S=3 → 2.0 → manual**. Not actioned.

**Two things that look pending and are not.** `Vedanga-Jyotisha/{Samaveda,Atharvaveda}` are
directories for **lost recensions** — no manuscript survives, so they are not work (13 dirs
carry no JSON; 11 are texts anyone could source). And `nirvana_upanishad` is tier `excluded`:
prose aphorisms with no verse numbering, where parsing 0 markers is the correct result, not a
failure.

### 1 · Available right now, same pipeline, nothing to solve

**Empty.** Everything that was here landed 2026-08-24 — Caraka, Suśruta, Manusmṛti, Bhela,
Aṣṭāṅgasaṃgraha and Nārada. Next candidates are in §2; each needs an ownership check first.

### 2 · Available on SARIT, would fix something already broken

- ~~**`manusmrti.xml`**~~ — **done 2026-08-24.** It did retire that plan's Manusmṛti half
  outright: re-acquired whole rather than repaired, 12 adhyāyas / 2,684 verses, 11 of 12
  chapters matching Bühler exactly. Two sessions of damage analysis went unused. **Check for
  a clean source before characterising damaged data** — the lesson now heads the plan doc.
- ~~**`bhelasamhita.xml`**~~ — **done 2026-08-24.** 8 sthānas / 98 adhyāyas / 2,813 verses.
  Incomplete by transmission, not digitisation.
- ~~**`astangasangraha.xml`**~~ — **done 2026-08-24.** 6 sthānas × 150 adhyāyas (canonical
  40/12/16/24/8/50), **9,382 verses**, 0 duplicates, 0 residual IAST, mūla-only by the
  header's own statement. Its Kalpasthāna Paribhāṣā parses as a third-level subsection with
  depth-3 keys `8.1.1`..`8.1.119`.
- **`ayurvedasutram.xml`** — surveyed: 5 `chapter` divs and **zero extractable lines**. Its
  text is not in `<l>`, `<p>` or `<ab>`. Needs a look before it can be scoped; 77 KB, low value.
- ~~**`naradasmrti.xml`**~~ — **done 2026-08-24.** 3 parts / 22 chapters / **931 verses
  against 931 `<lg>`**. The two blocking shapes were a merged chapter (`15-16.001a`, 31
  verses) and a sub-numbered verse (`01.124-1a`, 2). The same fix recovered **118 Caraka**
  prose units that had been hidden inside their preceding verse.
- **`kautalyarthasastra.xml`**, **`mahabharata-devanagari.xml`** — in scope by the letter of
  "everything not Tantra, Mantra, Brāhmaṇa, Āraṇyaka, Śikṣā or Kalpa", but both are a
  **scope decision for Rupali, not a default**: Arthaśāstra is polity and the Mahābhārata is
  itihāsa at ~100,000 verses, which would more than double the corpus.

### 3 · Blocked on the sūtra schema, not on sources

- **Aṣṭādhyāyī** (Vyākaraṇa) — on Wikisource, 30 pages.
- **Piṅgala Chandaḥsūtra** (Chandas).
- **`apastamba_dharma_sutra`**, **`apastamba_paribhasha_sutra`** — off-schema, same shape.
  **SARIT has no Āpastamba** (checked 2026-08-24 against its 85 XML files), so the
  re-acquire route that solved Manusmṛti is not available here; a source hunt has to run
  first.

All four need hierarchical `adhyāya.pāda.sūtra` with no verse markers. Solve once, in
`plans/2026-08-22-dharmashastra-redigitisation.md` — now scoped to Āpastamba only.

### 4 · No source in our channels — surveyed 2026-08-25

**All 13 are in §0's bucket; this section carries only the per-text detail.** The survey
covered sanskritdocuments, SARIT, Wikisource and the archive.org links on the jyotiṣa index.
Method and the four near-homograph false positives: `docs/SOURCES.md`.

- **Nirukta** (Vedāṅga) — absent from sanskritdocuments, Wikisource *and* SARIT. GRETIL has
  it in IAST under no granted licence. Vedic Heritage Portal is the outstanding lead.
- **Samarāṅgaṇa Sūtradhāra** (Sthāpatyaveda) — absent everywhere checked.
- **GargaSamhita** (the Jyotiṣa work) — what we had was the devotional Vaiṣṇava Purāṇa,
  relocated to Youvan. Wikisource has only that same Vaiṣṇava text, confirmed twice.
- **MuhurtaMartanda** — 154-page scan, no text layer, and a commentary edition. SARIT's
  `bhoja-rajamartanda.xml` is **Bhoja's Rājamārtaṇḍa**, a different work.
- **SiddhantaShiromani** — Wikisource's 1.2 MB `सिद्धान्तशिरोमणिः तत्त्वप्रदीपिकासहितः` is
  the Vīraśaiva **Siddhānta Śikhāmaṇi**, not Bhāskara II. Size looked like proof; content
  settled it.
- **SarvarthaChintamani** — SARIT's `pujyapada-sarvarthasiddhi.xml` is a **Jain** commentary.
- **BrahmasphutaSiddhanta** — Wikisource has a **400-byte stub**, not a text.
- **The remaining 6**: `Dharmasindhu`, `NirnayaSindhu`, `JatakaTattvam`, `PrashnaMarga`,
  `JaiminiSutras`, `ChandraKalaNadi` — nothing on any channel.

7 detailed above + 6 = **13**, matching §0. The previous version of this section said
"6 further Jyotiṣa stubs" and then listed **nine**, which is why §0 is now the single place
the count lives.

### 5 · Not backlog — deliberately out

- **Brāhmaṇa (16) and Āraṇyaka (5)** — Youvan's since 2026-08-24.
- **Śikṣā, Kalpa, Gāndharvaveda** — Youvan's.
- **8 alternate Saṃhitā śākhās** — Bāṣkala, Maitrāyaṇī, Kāṭhaka, Kapiṣṭhala, Kāṇva,
  Rāṇāyanīya, Jaiminīya, Paippalāda. Several survive only in fragments; **Kapiṣṭhala is not
  fully extant**. The primary recension of all four Vedas is held.
- **`Vedanga-Jyotisha/Samaveda` and `/Atharvaveda`** — those recensions are **LOST**, with no
  extant manuscript. Directories exist; they are not work.

---

## 2026-08-25 · Two Brāhmaṇa/Āraṇyaka texts sourced for Youvan, and a PDF-recovery probe

**Youvan was owed 21 named Vedic texts since 2026-08-24 and nobody had checked whether they
are obtainable.** Surveyed across sanskritdocuments, SARIT and Wikisource: **2 of 21 are
available. The other 19 are absent from all three** — a sourcing problem, not a digitisation
backlog. Both available texts are now held, in Youvan's tree.

| Text | Sections | Divisions | Verses | Tier |
|---|---|---:|---:|---|
| `taittiriya_brahmana` | 4 (3 aṣṭakas + Kāṭhaka) | 28 prapāṭhakas | 1,832 | `unit_mismatch` |
| `taittiriya_aranyaka` | 2 (Āraṇyaka, Ekāgnikāṇḍa) | 12 praśnas | 638 | `unit_mismatch` |

Both match the citable DIVISION count exactly (28 and 10). Detail:
`sanskrit-texts/docs/CANONICAL_COUNTS.md` Part 7.

**One pipeline, two output roots.** `convert.py:YOUVAN_OWNED` names the destination
literally; the sources repo, the targets file and astroacharya's validator are unchanged and
shared. Forking the pipeline per corpus is how two corpora end up with two conventions.

**`parse_sanskritdocs_sectioned` is a per-text OPT-IN, not a default.** Four already-held
texts carry unnamed `<h2>`s inside the content block — Chandogya, Praśna, Muṇḍaka, Taittirīya
Saṃhitā — and all four already parse correctly through the flat path. Regression measured:
all **39** pre-existing texts byte-identical before and after — 24 `sd`, 10 `gh`/SARIT,
5 `ws`/Wikisource. The full test suite is **144 passed**.

**Two dependencies are missing from every interpreter on this machine, and both bit the
VERIFICATION rather than the code** — `indic_transliteration` (SARIT) and `mwparserfromhell`
(Wikisource). Installed into a scratch venv; then all three branches really ran.

**Worth keeping, because the first pass reported a pass it had not earned.** Before those
installs, `--source ws` diffed clean and was recorded as IDENTICAL. It was worthless: both
the baseline and the new run aborted on the missing import, so the diff compared **two empty
files**. `rule:discernment-checks` §1 — a check that cannot fail reports success. It was
caught only because the full-corpus run printed the traceback. **When a regression diff comes
back clean, check it compared something.**

### `scripts/sanskrit-pdf/` — classify before recovering

**"Needs OCR" was wrong for most of the un-ingested PDFs in both corpora.** Measured across
14 documents: OCR is the answer for **3**, a *font encoding* fault for **7**. Building an OCR
lane first would have solved a fifth of the problem and produced worse text than `pdftotext`
for the rest.

Five tiers — `no-text` · `pua-corrupt` · `matra-stripped` · `latin` · `clean` — plus two
inputs it **refuses** rather than tiering. 32 tests; both thresholds mutation-checked red and
restored green. `scripts/sanskrit-pdf/README.md` carries the measured population.

**The four Sāmagāna books (Gāndharvaveda, Youvan's) are the largest obtainable group still
owed, and all four are `pua-corrupt`, not scans** — ~757,000 Devanagari characters behind a
legacy font that maps conjuncts into the Private Use Area.

**Still not built, and named so it is not mistaken for done:** the per-font PUA remap table,
and OCR. **Tesseract accuracy on Devanagari is still unmeasured** — the one attempt scored
88% CER against `Sandhyavandanam.pdf`'s text layer, then that text layer turned out to be the
corrupt half (G28) and the OCR the correct one, so the number measures nothing. Until a page
with independently-known correct text is scored, OCR output reaches no corpus except through
a draft field.

New gotchas: **G27** (a PUA detector written with PUA literals cannot fire — it called six
corrupt PDFs clean), **G28** (a font that drops every mātrā, invisible to any PUA count),
**G29** (`strip_tags` collapses whitespace, so a `(?m)^`-anchored regex sees one line —
reported 28 verses for a text with 1,834), **G30** (front matter is Roman even in a
Devanagari book).

---

## Pending (by priority) — archived P0/P1/P2 detail, 2026-09-02 through 2026-09-14

### P0 — THREE FABRICATED TEXTS ARE LIVE ON THE CITATION SURFACE

Found 2026-09-02 while looking for OCR ground truth. All three are marked `translated`, all
three are served, and every existing check passes on them because the checks verify numbering
and never words. Evidence and provenance: `docs/CANONICAL_COUNTS.md` §"THREE SIDDHĀNTA TEXTS
ARE FABRICATED". They entered together on 2026-07-17 (`1cccca6`).

**RESOLVED 2026-09-02 — deleted, then REPLACED** with 80 genuine verses from the Parameśvarācārya-ṭīkā edition; the converter refuses to run if the patronymic below is present. *Superseded detail:* **`aryabhatiya` (121 shlokas) — replace or quarantine.** Its 1.1 says
`ब्रह्मगुप्ततनय आर्यभटः`, "Āryabhaṭa son of Brahmagupta" — a father born c. 598 CE for a book
written in 499. Real Gītikāpāda 1 opens `प्रणिपत्यैकमनेकं…` to **Brahman**; ours opens to
**Hari**. *Fix:* acquire a real text (GRETIL and TITUS both hold Brāhmasphuṭasiddhānta but
NOT the Āryabhaṭīya — see `docs/SOURCES.md`; the recorded editions are Clark 1930 and Shukla
& Sarma INSA 1976, both print). Until then it must not be cited.

**RESOLVED 2026-09-02 by DELETION** — the fabricated `surya_siddhanta` was removed from the
corpus on Rupali's instruction; the seeder now walks 63 files, not 64, and `/texts` returns a
404 listing available texts. The replacement remains blocked on OCR quality (below), so this is
a removal of bad data rather than a substitution. **Two corrections to what this item claimed
before deletion, both mine:** `@source` is READ-ONLY (`app/masters/_source.py:77`) — it attaches
metadata and a docstring line and fetches nothing, so no calculation ever computed on this text;
and there were **5** mentions, not 3, two of them provenance strings in `panchanga.py`'s tithi
table rather than decorators. The exposure was the `/texts` API, which is narrower than
"production code" and worse, because it served 272 invented **English translations** too. The
three decorators now dangle, which is correct — do not repoint them.

**Superseded detail, kept for the record —** **`surya_siddhanta` (272 shlokas) — replace or quarantine. THE ONLY ONE OF THE
THREE THAT IS ACTUALLY CITED: 3 live `@source` citations in astroacharya** —
`core/yearly_gochar.py:29` and `core/yearly_calendar.py:26,28`, covering sidereal positions
and the sunrise-to-sunrise day boundary. Those cite invented text today. Note the decorators
use DISPLAY names (`"Surya Siddhanta"`), not `text_id`s, so a grep for `surya_siddhanta`
returns nothing and reads as "not cited" — it was, briefly, until the format was checked.
`aryabhatiya` and `panchasiddhantika` are cited nowhere under any spelling. Real 1.2 is
`अल्पावशिष्टे तु कृते मयो नाम महासुरः`; ours is different and `ब्रह्मा ब्रह्मगिरि ब्रह्ममयं`
is ungrammatical.

**REPLACEMENT SOURCE SECURED 2026-09-02 — OCR complete, and it independently re-confirms the
fabrication.** `1770115260.pdf` (345pp) was OCR'd in full: 311,251 Devanāgarī characters on the
`san` pass, 320,147 on `hin`. Two checks against it, and the second is the one that matters:

1. **The scan is the genuine work.** The attested `अल्पावशिष्टे तु कृते मयो नाम महासुरः` is
   present (`SuryaSiddhanta.san.txt:330`, and again on the `hin` pass) — positive content
   identification, not a title match.
2. **Our held opening `प्रणम्य शिरसा देवं` appears ZERO times in 345 pages of the real text.**
   That is confirmation of the fabrication **from a different instrument** than the one that
   found it — the original finding was incipit reasoning, this is a full-text search of a
   physical witness. `rule:discernment-checks` §4.

**Edition, and it is public domain beyond argument.** *Sūryasiddhānta, edited and provided with
a commentary called Sudhāvarṣiṇī by Mahāmahopādhyāya **Sudhākara Dvivedī***, Asiatic Society of
Bengal, Calcutta, **1925**; first published in Bibliotheca Indica as Nos. 1187 (1909) and 1296
(1911). The prefatory note records **the editor's death in 1922**. No rights question arises —
contrast the Raman and Pathak editions rejected the same day (`docs/SOURCES.md`).

**The uncomfortable part: the genuine text was on disk the whole time.** This scan was already
in the sources tree and was never OCR'd, because the OCR lane was unmeasured and OCR of
commentary editions had been declined. So a fabricated Sūrya Siddhānta was served under three
live citations while its authentic witness sat two directories away.

*Remaining work:* the edition interleaves mūla with the Sanskrit **Sudhāvarṣiṇī** ṭīkā (running
head `सुधावर्षिणी टीका`) — structurally the same problem as Golādhyāya, which was solved
2026-09-02.

**BUT THE OCR IS TOO CORRUPT TO CONVERT, measured 2026-09-02, and this is now the blocker.**
The scan is genuine and public domain; the *reading* of it is not usable for a citation
surface. Character-level corruption hits the majority of occurrences of common words:

| correct | count | corrupt form | count |
|---|---|---:|---:|
| `कृते` | 1 | `कते` | **15** |
| `मयो` | 27 | `म्यो` | **53** |
| `स्वयम्` | 0 | `खयम्` | 1 |
| `आराधयन्` | 0 | `च्राराधयन्` | 1 |

The attested incipit itself reads `अल्पावशिष्टे तु कते म्यो नाम महासुरः` — recognisable, and
wrong in two words. Only **44%** of verse numbers are +1 from the previous (Golādhyāya's clean
text ran near-contiguous), and 10 terminators carry a **Latin** digit. **Converting this would
replace fabricated text with corrupted text**, which is not an improvement on a surface that
exists to be cited, and G6 forbids it besides.

*So the route is one of three, and none is a parser:* proof the OCR against the images (human
work); find a better witness — a clean Devanāgarī text of the Sudhāvarṣiṇī edition, the shape
that made Golādhyāya easy; or **quarantine the fabricated text now, independently of any
replacement.** The third is the only one that stops the harm today, and it is a live-behaviour
decision for Rupali: the three `@source` citations in `yearly_gochar.py` and
`yearly_calendar.py` would then fail loudly rather than return invented scripture. **Failing
loudly is the better failure**, but it is her call, not one to take by default.

**RESOLVED 2026-09-02 — deleted, then REPLACED** with 386 genuine verses from Thibaut & Sudhākara Dvivedī, 11 of 18 chapters exactly on canonical count; the converter refuses to run if the epoch reads 425. *Superseded detail:* **`panchasiddhantika` (166 shlokas) — replace or quarantine.** Genuine for 1.1–1.3
only; 163 of 166 are two-line paraphrase. 1.17 states the epoch as **Śaka 425** where
`CANONICAL_COUNTS.md` records **427**; 13.6 gives earth's circumference 500 yojanas against
diameter 200. *Fix:* a scan exists at
`sanskrit-texts-sources/Siddhanta/Panchasiddhantika/panch_siddhantika_040577_hr6.pdf` (344pp).
**Note its layout before OCR: it is TWO-COLUMN**, printing manuscript and emended readings in
parallel, and `--psm 6` merges them into one line. `--psm 3` separates them.

*[The Sāravalī **OPEN** item that followed here in STATE.md is unchanged and still lives in STATE.md, not here — skipped in this archive to avoid duplication.]*

~~Audit the incipit of every text the Jyotiṣa sweep did not cover~~ — **DONE 2026-09-02.
33 texts, 71,110 shlokas, ALL GENUINE.** Vedic Saṃhitā (5), Upaniṣad (20) and Upaveda (8) all
match their attested incipits, with mid/end spot checks. **Fabrication is confined to the three
Siddhānta texts from the 2026-07-17 hand-ingestion** — everything fetched through the
Wikisource, SARIT and sanskritdocuments pipelines is real, which is the useful conclusion: the
pipelines are trustworthy, the hand-ingestion was not. Two worries cleared: Caraka/Suśruta
prose IS present (G21 did not happen), and none of the seven Brāhmaṇa-embedded Upaniṣads starts
mid-work. Six smaller defects were found and are filed separately above. Detail:
`docs/CANONICAL_COUNTS.md` §"Incipit audit COMPLETE".

**RESOLVED 2026-09-04 by re-parse — see the closing block of this entry.** **`brihadaranyaka_upanishad` held each mantra TWICE, and a mechanical strip was
NOT safe.** Analysed 2026-09-02. It is a sandhi-split study edition: 4,315 `SF` markers over
424 mantras, so `SF` marks each *phrase*, not each verse. The stream alternates
`A_sandhi SF A_free B_sandhi SF B_free …` — **with no delimiter between one phrase's
sandhi-free form and the next phrase's sandhi form.** Splitting on `SF` therefore yields chunks
containing the tail of one mantra and the head of the next, and recovering the canonical half
means guessing the boundary inside a *mukhya* Upaniṣad. Do not attempt it.

Also embedded in the text field: `मन्त्र N` markers (424), bracketed canonical citations
(251, e.g. `[III.i.2]`), adhyāya colophons, and the English header *"SF as marked below is
Sandhi-free text to aid students"*.

**Its chapter structure is CORRECT** — 47 chapters is exactly the canonical 47 brāhmaṇas. Only
the text content is contaminated.

*Fix was to be re-fetch, not repair.* **The GRETIL file was fetched and inspected 2026-09-02,
and it does NOT drop in.** `sa_bRhadAraNyakopaniSadkANva-recension-comm.xml` is the right
recension and is clean of the `SF` contamination — **0 `SF` markers** against our copy's 4,317 —
but two things block it, one of which was not anticipated:

- **It is IAST, not Devanāgarī.** 578,928 Latin characters and 111,710 diacritics; **zero**
  Devanāgarī. The corpus is Devanāgarī, so this needs transliteration — and that pipeline is
  where G22 was paid for (entities surviving tag-stripping and having their digits transliterated,
  1,413 times).
- **It is Śaṅkara's commentary with the mūla embedded**, which was the anticipated caveat and is
  confirmed: the text opens `uṣā vā aśvasya'ityevamādyā vājasaneyibrāhmaṇopaniṣat / tasyā
  iyamalpagranthā vṛttirārabhyate` — "this brief commentary on it is begun". Its TEI carries
  **773 `<div>`s with no attributes at all** — no `n=`, no `type=` — so the adhyāya/brāhmaṇa
  hierarchy is not in the markup and cannot be read off it.

Note also 1,436 `<p>` against 360 `<lg>`: **Bṛhadāraṇyaka is mostly prose**, so reading only
`<l>` would drop most of the text — G21, the Caraka/Suśruta lesson, applies here too.

Licence recorded, not a bar: GRETIL states CC BY-SA with a good-faith copyright disclaimer.

**So this text needs a Devanāgarī mūla edition, which neither the held source nor GRETIL
provides.** Our own `brinew-proofed.html` carries the same 4,317 `SF` markers, so the
contamination is upstream of the corpus, not introduced by digitisation.

**A Devanāgarī edition WAS supplied that evening (`c17ef55`) — and its OCR FAILS the reading
gate, measured 2026-09-04.** `1781600259.pdf`, 989pp, `no-text` tier, OCR'd 2026-09-02 23:34 into
`BriDevanagari.{san,hin}.txt`. It is the right book read by the wrong instrument:

| measure | result |
|---|---|
| Devanāgarī chars, `san` pass | 471,649 — but only **94,863** sit on Devanāgarī-dominant lines. The rest is the edition's **English half misread as Devanāgarī** |
| word accuracy, mantra 1.1.1 | **27 of 53 words (51%)** appear verbatim in the held text; 26 do not |
| systematic substitution | ए→प throughout — `पव` 53, `पवं` 43, `पष` 57 where `एव` / `एवं` / `एष` belong |
| the central figure's name | `याज्ञवल्क्य` correct **5** times, against **12 distinct corrupt spellings** (`याज्षवर्क्येति`, `याज्ञवद्कयेति`, `स्यायाज्ञघतक्य`, …) |
| `hin` pass | **worse** — the attested incipit `उषा वा अश्वस्य` does not occur in it at all |

The incipit reads `उषा वा अश्वस्य मेभ्यस्य शिरः । सू्ेश्वह्ु, धातः प्राणः…` where the text is
`…मेध्यस्य शिरः । सूर्यश्चक्षुर्वातः प्राणो…`. **This is the Sūrya Siddhānta situation exactly** —
a genuine, public-domain, correctly-identified scan whose *reading* would replace contaminated
text with corrupted text. G6 forbids it. Do not convert from this OCR. The scan stays: it is a
proofing witness and, per its commit, the only source that prints the canonical citation in its
running heads.

**But the held copy is more recoverable than this entry said — re-measured 2026-09-04, and two
claims above were too pessimistic.**

- **The `मन्त्र N [ref]` marker is a hard delimiter and it is COMPLETE.** 424 of them, exactly
  the canonical Kāṇva mantra count, and **430 bracketed refs, not the 251 recorded above**.
  Everything before the marker in a shloka is leakage from the previous mantra plus headings;
  the canonical text begins immediately after it. Cutting there involves no guessing at all.
- **The chapter→brāhmaṇa map is already exact, and the citations are already in the file.** Per
  chapter the refs run `1..N`, and the counts reconcile to canon adhyāya by adhyāya: I
  `2,7,28,17,23,3` = **80** · II `20,4,6,14,19,3` = **66** · III = **92** (III.ix.28 spilled into
  ch22) · IV = **92** (IV.iii runs to 38, split across ch25/ch26) · VI = **75**. Each matches the
  file's own front-matter table (`मन्त्राः ८० / ६६ / ९२ / ९२ / ३३ / ७५`).

**What is genuinely fuzzy is only the phrase boundary INSIDE a mantra** — separating `F_i` from
`C_{i+1}` within one ` SF `-split segment. Discriminator measured over 412 known-pure canonical
chunks (the segment between the marker and the first ` SF `) and 824 known-pure sandhi-free
chunks (each shloka's trailing segment, and the leakage at the next shloka's head):

| feature | canonical | sandhi-free |
|---|---:|---:|
| word-final `स्` | 0.9% | **13.1%** |
| halanta-final | 12.0% | **35.4%** |
| contains `ऽ` | **4.6%** | 1.7% |

Real signal, and **far too weak per token to place a boundary in a *mukhya* Upaniṣad**. The
tractable form is an ALIGNMENT rather than a classifier: `F_i` is `C_i` with sandhi undone and
`C_i` is already known, so the split point is where the segment's prefix stops matching the
previous canonical chunk. That is well-posed and testable — it is also new scope, and it edits a
*mukhya* Upaniṣad, so it is Rupali's call and not a default.

**One of the three defects this reconciliation reported is real. Two were the instrument** —
corrected 2026-09-04 the same day, on reading the SOURCE rather than the JSON derived from it.

- **REAL: the roman numerals in the refs must not be parsed.** `I.I` is I.ii, `I.Ii` is I.iii,
  `III.vI` is III.vii, `V.xIi` is V.xiii, and `VI.i` is printed `VI.1` — arabic. The brāhmaṇa
  index is safe to take from chapter ORDER; it is never safe to take from the numeral.
- ~~`VI.i.1` is absent~~ — **it is present.** The JSON's chapter 43 appears to start at `VI.i.2`
  only because the first ref reads `[VI.1.1]` with an ASCII `1`, which a roman-numeral pattern
  does not match. Adhyāya VI parses at exactly the canonical 75.
- ~~Adhyāya V is short two brāhmaṇas~~ — **all 15 are in the source**, each with its own
  `<ordinal> ब्राह्मणम्` heading including `एकादशं` and `द्वादशं`. The JSON held 13 chapters
  because its chapter split had merged them, not because the text lacked them.

**Both wrong claims came from counting the derived JSON's `chapters[]` and calling the result a
property of the text.** `rule:discernment-checks` §4 — the instrument answered a narrower
question than the one asked, and the answers were plausible enough to write down. The source is
the authority for what the source contains; the derived file is evidence about the derivation.

### RESOLVED 2026-09-04 — `scripts/sanskrit-convert/brihadaranyaka.py`

**47 brāhmaṇas against the canonical 47; 431 mantras of 438; adhyāyas III, IV and VI land on
92 / 92 / 75 exactly.** `chapter` is the adhyāya and `number` is `brāhmaṇa.mantra`, so the text
can carry a Bṛhadāraṇyaka citation for the first time. Corpus 932 → 891 chapters and
92,804 → 92,798 shlokas; **dedupe loss still exactly 71**, and the validator returns to its
baseline 8 failing / 105 errors with this text no longer among them.

**No new source was needed.** The apparatus that contaminated the text field was the structural
witness: 424 `मन्त्र N` markers delimit the units exactly, and the 989pp scan — refused above on
its OCR — was not used at all.

**The echo split is an alignment, and it is measurable.** Over 412 known-pure canonical and 824
known-pure sandhi-free chunks the orthographic discriminator was far too weak per token to place
a boundary. The alignment does not classify: `F_i` is `C_i` with sandhi undone and `C_i` is
known, so the boundary is where the prefix stops matching, and a marker resets the recursion 431
times so an error cannot propagate past the next mantra. **The check that it worked is the
output's own orthography** — word-final `स्` came out at **1.15%** against a canonical baseline
of 0.9% and a sandhi-free 13.1%. Had the split drifted, that number would have climbed.

**Three source properties found, all recorded rather than repaired:**

- **4 numbers absent from the source's own sequence** — I.5 skips 5, 8 and 20; II.4 skips 10.
- **V.15 is a unit mismatch, not a gap.** The whole Īśā-parallel passage is present under mantra
  1 where canon subdivides into 4. The content is entire; only the subdivision is missing, so it
  is excluded from `known_gaps` — G12, a "missing" record may be a mislabelled one.
- **6 mantras genuinely end without a terminator**, and **2 more close on the source's RUNNING
  count** (`॥ ११ ॥`, `॥ १२ ॥` for V.11.1 and V.12.1). Those are different facts and the parser
  reports them differently; conflating them would have left a colophon attached to both.

**G32 fired here.** 6.2.13 closes `। १३ ॥` — a *single* daṇḍa on the opening side. A pattern
demanding `॥` on both sides scores it zero and leaves the colophon in the served text. Both
daṇḍa forms are now accepted on the opening side and the guard is mutation-checked.

**11 tests, 4 mutations checked red for their stated reason** (the ASCII digit class → the
Unicode shorthand, the aligner → whole-segment echo, the opening daṇḍa → double-only, the
colophon fallback → removed). Suite green at **111 passed**. `pytest` is absent from every
interpreter on this machine, as `indic_transliteration` and `mwparserfromhell` already were —
a scratch venv is still the way to run this suite.

**Still open on this text:** it lands `untranslated`, like the rest of the Vedic corpus.

**The same `structure`-block gap remains on `mundaka_upanishad` and `taittiriya_samhita`** — both
converted 2026-09-02, both emit dotted numbers with no `structure` block, and both fail
`validate_corpus.py` for exactly the error this text just cleared. One block each; not done here
because they are different texts.

**CLOSED 2026-09-02** — **`mundaka_upanishad` was mis-chaptered by one; `subala_upanishad` is missing shloka
1.** Muṇḍaka's chapter 1 holds only the śānti-pāṭha, pushing the real opening
`ॐ ब्रह्मा देवानां प्रथमः संबभूव` into chapter 2, so every khaṇḍa is offset.

**The fix is fully derivable — verified 2026-09-02.** Chapters 2–7 hold 9, 13, 10, 11, 10, 11
mantras, which matches the canonical six khaṇḍas of Muṇḍaka **exactly** (total 64). So chapters
2–7 are khaṇḍas 1.1, 1.2, 2.1, 2.2, 3.1, 3.2 with no ambiguity. **Nothing cites any Upaniṣad**
(checked across astroacharya), so G7's renumbering hazard does not apply here.

*Decide the citation shape before editing, because the corpus has no convention:* 18 Upaniṣads
number flat, `prashna` uses `1.1`, `chandogya` uses 3-level `1.1.1`. Muṇḍaka's canonical
citation is muṇḍaka.khaṇḍa.mantra, which the flat scheme cannot express — so this is really a
question about all 20, not one.

**Muṇḍaka: RESOLVED 2026-09-02 by re-parse.** All six khaṇḍas come out exactly on the canonical
9/13/10/11/10/11, `chapter` is the muṇḍaka and `number` is `khaṇḍa.mantra`, and `1.1` is now the
real opening `ॐ ब्रह्मा देवानां प्रथमः संबभूव` rather than the śānti. The śānti-pāṭha is kept as
`0.1`, outside the khaṇḍa sequence instead of occupying a slot.

**Subāla: NOT a digitisation defect — it is the source, checked 2026-09-02.** `subAla.html`'s own
markers run `[2, 3, 4 … 16]`; **the file contains no `॥१॥` at all**. The corpus reflects it
faithfully. The content is not missing either: the first entry opens
`अथ सुबालोपनिषत् ॥ बीजाज्ञानमहामोहापह्नवाद्…`, so the title and maṅgala sit before the first
printed marker, and what is absent is the *number*, not the text. **Do not synthesise a khaṇḍa 1**
— that would be inventing a citation the source does not make. GRETIL does not hold Subāla, so
correcting the numbering needs a different edition, not a repair.

**CLOSED 2026-09-02 by re-parse** (`8891088`, 2,294 verses to 650 anuvākas) — **`taittiriya_samhita` duplicated ~49% of its verses, and they all ingested.** 976 of
2,294 are exact duplicates of the shloka two earlier (A,B,A,B); 1,126 duplicate something.
**Zero duplicate `(chapter, number)` keys**, so the seeder's dedupe cannot see them — the
mirror image of G8. True unique content is ~1,168 verses and the corpus total is inflated by
~1,126. The text itself is GENUINE (TS 4.5 is the Śrī Rudram verbatim); this is an ingestion
defect. The other four Saṃhitās are clean and show none of the offset-2 signature.

**Mechanism established 2026-09-02 — one defect with two arities, so the fix is deterministic.**
Every anuvāka's text is emitted **twice**, and the two gap values are the same bug over
different-sized units:

| | unit | slots per anuvāka | signature | count |
|---|---|---|---|---|
| kāṇḍa 1 | 1 chunk | `.1 .2` | `A,A` — gap 1 | 142 |
| kāṇḍas 2–7 | 2 chunks | `.1 .2 .3 .4` | `A,B,A,B` — gap 2, slot 3=1 and 4=2 | 976 |

(plus 8 stragglers; 1,126 total). **No duplicated body crosses a kāṇḍa** — 0 of 1,126 — so the
second emission is always local and the trailing half of each anuvāka's slots is the redundant
copy. That makes it removable by rule rather than by content comparison.

**But de-duplication alone is not the fix.** The `text` fields still carry the source's own
number stranded at the head of the string (`२ यज्ञस्य घोषदसि…`). In prapāṭhaka 1 those run
2, 4, 5, 7, 9, 10, 12, 13, 16, 19, 21, 22, 25 and then reset — a **running mantra count**, whose
differences (2,2,1,2,2,1,2,1,3,3,2,1,3) are per-anuvāka mantra counts. The assigned numbering is
a sequential renumber that does not correspond to it, so dropping the copies would leave
anuvāka-sized blobs still mis-labelled as verses. *Fix:* re-parse from source, splitting on
those embedded numbers — they are the only surviving record of the true segmentation.

**G7 does not apply here:** nothing in astroacharya cites any Vedic Saṃhitā or Upaniṣad
(checked 2026-09-02), so renumbering is safe. Do not "fix" this by deduping alone.

### P1 — Off-schema JSON blocks AstroAcharya ingestion

**CLOSED 2026-09-02** — was **1 JSON file on the pre-normalization shape** — top-level `sutras`/`shlokas` with `sanskrit` / `english_translation`, **no `chapters[]` wrapper**, banned by `docs/DECISIONS.md` 2026-06-20. **Blocks AstroAcharya `/texts` ingestion.** Was 18, then 14; **re-counted 2026-09-02 and it is 2.**

`apastamba_dharma_sutra` was re-digitised from the 1898 Mysore OCR by
`scripts/sanskrit-convert/apastamba.py` — **1,315 sūtras, 2 chapters, 45 absences recorded
and none invented**, citation `praśna.khaṇḍa.sūtra`. **Nothing in the corpus is off-schema
now.** English and Hindi are **drafted for all 1,315** (draft fields, `status: drafted`); the
served fields are empty, so INVENTORY correctly still reports 0% *translated*. Verification —
promoting drafts into `english`/`hindi` — is the next piece of work on this text and is not
started.

**`apastamba_paribhasha_sutra` left for Youvan 2026-09-02** — it is Kalpa, not dharma: praśna
24–25 of the Āpastamba Kalpasūtra, first sūtra `यज्ञं व्याख्यास्यामः`, commentator
Kapardisvāmin who commented on the Kalpasūtra. Now at
`Tushar/Youvan/texts/Kalpa/Paribhasasutra/Apastamba/`, off-schema, defects documented there.
Its sibling the Dharmasūtra stays — the split is by genre, not by containing work.

**Feasibility of the remaining re-parse: measured 2026-09-02, tractable.** `4617.txt` carries
1,313 sūtra markers (~1,364 canonical), 59 khaṇḍa and 20 paṭala colophons in-body, and the
mūla/ṭīkā split is mechanical — sūtra lines end `॥N॥`, Haradatta's commentary ends plain `॥`.
The ~3–4% shortfall is uniform across all three levels: OCR dropout, self-detecting as gaps in
otherwise contiguous runs. Use `4617.txt`, never `4605.txt` (same edition, single-line dump).
Detail and the two remaining unknowns: `docs/plans/2026-08-22-dharmashastra-redigitisation.md`.
No clean source exists — SARIT has no Āpastamba, GRETIL has only its Śulba/Gṛhya/Śrauta sūtras.

**⚠ Both Āpastamba texts are already 100% machine-"translated"** — `ADS_001` is 1,437/1,437 in
`english_translation`/`hindi_translation`, unverified. Not the served field names, so nothing
publishes them; **a schema migration that renames those fields publishes them.** The plan doc's
claim that no record carries English or Hindi is false.

**The twelve `MS_001.json … MS_012.json` this entry listed no longer exist.** Manusmṛti was re-acquired whole from SARIT and is now one file — `Dharmashastra/ManuSmriti/ManuSmriti.json`, 12 chapters, 2,684 shlokas. The fix landed while this entry kept asserting the problem; see `docs/CANONICAL_COUNTS.md` §"Manusmṛti from SARIT". A count in a state file rots faster than anything else in it.

**Cleared:** `Saravali`, `Asvalayana` and `MuhurtaChintamani`'s `MC_001` were migrated onto the schema 2026-08-17; `MC_REMAINING_RAW.json` was raw extraction, not a chapter, and moved to `../../../sanskrit-texts-sources/` 2026-08-18.

**The remaining 14 need RE-DIGITISATION, not renumbering** — checked against the canonical structures 2026-08-18:

- ~~**Manusmriti**: leading component running 1–33, "chapter 1" holding 1,516 records against 119, 89 fragmentary cycles~~ — **moot 2026-08-24**, re-acquired from SARIT rather than repaired. Two sessions of damage analysis were discarded, which is the standing lesson: check for a clean source before characterising damaged data.
- **Apastamba**: the hierarchy is Praśna → Paṭala → Khaṇḍa → sūtra, so **`1.1.1` is a correct citation**, not a broken number. But of 1,437 records, 219 carry a bare integer, 13 are malformed `..10`, and 15 are the literal placeholder **`X.X.21`/`X.X.22`** — the digitiser recording "prefix unknown". 136 restart-cycles of lengths 14, 20, 1, 10, 21, 29, 63…

A first reading of Apastamba's opening 30 records — a clean `1.1.1…1.1.14` run — suggested the numbering was merely truncated and reconstructible. Across the whole file that is false; **a 30-record sample gave the wrong answer about a 1,437-record file.**

Sources are in `../../../sanskrit-texts-sources/Dharmashastra/`, but `manu_clean.txt` is a **2.8MB scanned book on a single line** (1909 Nirnaya Sagar edition, front matter and Kullūka's commentary included). This is a digitisation project, not a patch.

### P1 — Digitization backlog (in scope, not yet sourced or converted)

Corrected 2026-08-12 — the 2026-06-20 list was wrong: **Saravali, Surya Siddhanta, Aryabhatiya, and Panchasiddhantika are now digitized**, not stubs.

~~**OPEN** — reclassified 2026-09-02 from "not yet sourced" to **UNSOURCEABLE on current
terms**.~~ — **CLOSED 2026-09-14: this is recorded state now, not open work.** The
seven-channel survey's CONCLUSION still stands — sanskritdocuments, SARIT, Wikisource,
archive.org, GRETIL, Muktabodha, the Vedic Heritage Portal and the Digital Corpus of Sanskrit
structurally carry no Muhūrta, Praśna, Jātaka, Nāḍī or Nibandha literature, so the original
absences were closures, not failed searches. What changed, starting the same day
(2026-09-02) and continuing through 2026-09-08, was the **acquisition route**: Rupali supplied
scans directly, and for this genre *the channel is human*, not a pipeline —
`brahmasphuta_siddhanta` was separately acquired 2026-09-08 via her own 336-page scan (19 of 24
chapters / 639 verses) rather than through GRETIL/TITUS, whose licence block (`docs/LICENSES.md`
§"The NonCommercial question") is now moot for this text.

Per-text status is no longer tracked here — restating it is exactly how this line went stale.
`sanskrit-texts/docs/INVENTORY.md` §"Acquisition status" is the single current record (one row
per text, one status: `HELD` / `SOURCED` / `REFUSED` / `UNSOURCED` / `LOST`), and
`python3 sanskrit-texts/scripts/check_inventory.py` fails if that table and the corpus
disagree — re-run it rather than trusting this line. Verified 2026-09-14: 66 corpus texts, 13
acquisition rows, exit 0. Of those 13: **HELD 7** (NirnayaSindhu, SarvarthaChintamani,
JatakaTattvam, BrahmasphutaSiddhanta, GargaHora, JaiminiSutras, SiddhantaShiromani) ·
**SOURCED 0** · **REFUSED 3** (Dharmasindhu, MuhurtaMartanda, ChandraKalaNadi) · **UNSOURCED 2**
(PrashnaMarga, GargaSamhita) · **LOST 1** (the Vedāṅga Jyotiṣa Sāmaveda/Atharvaveda
recensions). Only one `.placeholder` directory survives on disk, `Hora/Nadi/ChandraKalaNadi/`.

**Rights are recorded, never grounds to refuse or delete a source** — Rupali's standing
instruction, restated 2026-09-02 after it was overridden four times: *"stop rejecting on the
rights, note it. I told you that."* See `docs/SOURCES.md` §"Rights are RECORDED".

Two Muktabodha sub-collections (Gokarna, IFP) are UNSURVEYED rather than empty — both gated,
both image-scans. TITUS had a single index pass only, so its other ten are UNVERIFIED. **Retitled 2026-09-02: these are no longer "README-only stubs".** The per-text readmes were drained that day and `git rm` took the empty parent directories with them, so eleven of these texts have no directory at all. [`docs/INVENTORY.md`](../../../sanskrit-texts/docs/INVENTORY.md) §"Undigitised" is now the single record, and carries author, period and why-wanted for each — more than the readmes held. Keep this section as the *priority* view; do not re-list the texts here.

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

- ~~`CLAUDE.md` layout block shows the pre-`1cccca6` flat `Hora/<Text>/` paths~~ — **verified closed 2026-09-02**: zero flat `Hora/<Text>` lines remain; it uses `Hora/{Parashari,Nadi,Prashna,Jaimini}/`. Its `[README-only stubs]` line went the same day, with the readmes.
- ~~`CLAUDE.md` `category` enum missing values~~ — **fixed 2026-08-17**: now the 8 values the data uses. `hora` was retired by `1cccca6` and its last user (`SV_FULL.json`) was migrated.
- ~~Root `README.md` ~3 months stale~~ — **rewritten 2026-09-02** (`f0de1b0`). It had described a `texts/` root, `Tantra/` and `SamudrikShastra/` trees, flat `Hora/<Text>/` paths, `BPHS0110.json` chunking and the banned Schema A/B, and marked six digitised texts "not yet digitized". It now points at `docs/INVENTORY.md` for holdings and `CLAUDE.md` for schema instead of duplicating either — duplication is what let it rot.
- ~~`docs/INVENTORY.md` "Source held" stale~~ — **mostly fixed 2026-08-17**: Panchasiddhantika/SuryaSiddhanta/MuhurtaChintamani now read `—`. **Saravali's `pdf` is correct** — it still holds a 17MB `saravaliofkalyan01kalyuoft.pdf` locally (gitignored per the source-out-of-git policy). Maintained by hand now; the generator that regenerated it was retired.
- ~~`.gitignore` lines 8–9 are dead rules~~ — **closed 2026-08-18**; those lines are now a comment recording the removal and the reason. Re-verified 2026-09-02.
- ~~`scripts/digitize.py` + `scripts/translate.py` committed against the "Do not commit processing scripts" rule~~ — **resolved 2026-08-17**: both deleted, along with `scripts/gen_inventory.py`. `scripts/` now holds only `install-hooks.sh`, which wires the hygiene githooks and is not a processing script.
- ~~The 4 raw `Dharmashastra/*.txt`~~ — **CLOSED 2026-09-02, and the count went to zero
  without any of them being converted here.** `4617` became `apastamba_dharma_sutra`; `4605`
  is a second OCR of that same 1898 edition and is the cross-check for its 45 absences, not
  separate work; `4607` is the Paribhāṣāsūtra's source and left with it for Youvan; **`4609`
  is identified as the `Āpastamba-ukta Śrāvaṇī`, a Vedotsarjana/Upākarma prayoga — Kalpa, so
  Youvan's.** Identified by counting genre markers across the file: 13 saṅkalpa resolves and
  zero dharma-determination markers. See DECISIONS 2026-09-02.

### P2 — Translation injection

- None pending. `muhurta_chintamani` is **complete** — re-measured 2026-09-02: **one** file, **206 of 206 translated**, not the "15 files, 169 translated (~82%)" this line asserted. The live defect there is *numbering*, not translation: chapter-1 numbers run 11–32, 1–7, 37–44. Recorded in `docs/CANONICAL_COUNTS.md`; fixing it needs the chapter-1 pages of the source PDF read against a canonical edition.
- Corpus-wide, translation is **17,441 of 92,166 shlokas (18.9%)**, and the split is by scope rather than by backlog: every Jyotiṣa category is 100%, every Vedic/Upaveda category is 0% and was acquired untranslated on purpose. Derive, never restate — the one-liner is in `docs/INVENTORY.md`.

### Possibly migrated from workspace `../../../TODOS.md`

- _None directly owned._ TM-068 (vendor-derived JSON deprecation sweep) mentions `SANSKRIT_TEXTS_PATH` but the work is astroacharya-side. TM-041 (Jyotish texts migration from Youvan into AstroAcharya) treats this repo as the destination — see workspace TODOS TM-041 for the producer side.

---

## 2026-09-04 · Eight parallel lanes — three texts digitised, four refused, one acquired

**Corpus 59 → 62 texts · 92,798 → 96,710 shlokas · dedupe loss still exactly 71 ·
`validate_corpus.py` unchanged at 6 failing / 103 errors · suite 120 → 209 passed.**

| lane | outcome |
|---|---|
| `sarvartha_chintamani` | **DIGITISED** — 17 chapters, 1,227 verses |
| `jataka_tattva` | **DIGITISED** — 17 chapters, 2,277 sūtras (source supplied same day) |
| `jaimini_sutra` | **DIGITISED** — 2 adhyāyas, 408 sūtras (source supplied same day) |
| `brahmasphuta_siddhanta` | **ACQUIRED** to the sources tree as reference; no `text_id` by decision |
| Dharmasindhu · Nirṇayasindhu · MuhūrtaMārtaṇḍa · GargaHorā | **REFUSED**, each with a measurement |

**Unsourced is down to ONE: `ChandraKalaNadi`.** Detail for every text: `docs/CANONICAL_COUNTS.md`
§"Three texts digitised 2026-09-04" and `docs/SOURCES.md`.

**The finding that outlives the texts: a source that looks markerless is a claim about the PROBE.**
All three conversions had been recorded as unsourceable or unsegmentable, and in each the obstacle
was the *shape* of the marker, not the source:

- Jātaka Tattva — `॥ N ॥` and `।। N ।।` both score **zero**; the numbers print as `२०८.`, and
  there are **2,270** of them.
- Sarvārtha Cintāmaṇi — the chapter witness was inside `1267.txt` all along, as **English**
  `CHAPTER-N` headers in a bilingual edition. Two prior attempts probed only for Devanāgarī.
- Jaimini Sūtra — `।। N ।।` only; the `॥ N ॥` probe returns zero.

**Publication scope settled 2026-09-04 (Rupali):** this material is reference for building
astroacharya's logic, not for publication. The distinction that governs: the **sources tree is
gitignored and never published**, so rights never bar acquisition there; the **corpus JSON is a
public repo plus a public API**, and that is publication. Brāhmasphuṭasiddhānta is held on the
first side of that line deliberately.

### Four refusals, each with the number that decided it

- **Dharmasindhu** — its 307 markers number the texts it QUOTES, not itself: 39 resets to 1,
  sequence `19,4,1,2,3,4,1,2,4,1,1,2,2,3,3…`. No author-declared numbering exists for its own
  content, so a `chapter → shlokas` schema has nothing to key on.
- **Nirṇayasindhu** — 1 marker per ~3,570 Devanāgarī characters against 124–252 characters per
  verse in real verse texts, a **~28× gap**. Prose that quotes verses, not a verse text.
- **Muhūrta Mārtaṇḍa** — `मुहूर्त` occurs **0 times correctly** in 188 pages against 21 corrupted
  near-misses (systematic म→स). Left a reusable gate script that exits 1.
- **Garga Horā** — identity **CONFIRMED** as the jyotiṣa Horā by content (`-गर्गः।` named inside
  the text), closing G26's first collision. Chapter 1 has ~84–90 real numbered verses; chapters
  2–3 (85% of the book) carry no verse numbers *in the print edition*, confirmed because both
  independent OCR passes agree.

**New instrument: cross-pass OCR agreement.** Diff the `-l san` and `-l hin` readings of the SAME
page images — no external witness needed, which is what every earlier accuracy estimate lacked.
Measured over 4,000 tokens: Nirṇayasindhu **20.5%**, Dharmasindhu **34.6%**. The `और` probe is its
one-line form: 0 occurrences in a `san` pass over 1,024 pages against 7,184 in the `hin` pass means
the wrong OCR model was used.

**New gotcha G38** — `\b` after a Devanāgarī vowel sign silently never matches
(`re.search(r'इति\b', 'इति सप्तम…')` is `None`). G17 one Unicode level up, and it shipped once in
this session before being caught.

**Process finding, recorded because it cost real tokens:** the harness ran **duplicate agents** —
two on Sarvārtha Cintāmaṇi and second copies of three others. The two Sarvārtha agents wrote
different segmentations to the same path and overwrote each other; the file changed twice
mid-verification and was only caught by re-running the converter and diffing. Later briefs carry a
tripwire — *"if your output files already exist when you start, STOP"* — and that lane reported
cleanly. **Verify a subagent's artifact, never its report** (`rule:delegation-criteria` §4): three
lanes' self-reports disagreed with the tree in some detail.

---

## 2026-09-04 · The repair — Taittirīya's apparatus, and the last two structure blocks

**`validate_corpus.py` failing list 8 → 6**, errors 105 → 103. `mundaka_upanishad` and
`taittiriya_samhita` both clear. Corpus unchanged at 59 texts · 891 chapters · 92,798 shlokas,
dedupe loss still exactly **71**. Suite **120 passed**.

**The Taittirīya defect was six times larger than the probe said, and that is the transferable
part.** I reported "unit 1.1.1 carries front matter". It was **505 of 650 units**, two separate
defects:

- **44 units** — the section heading `प्रथमकाण्डे द्वितीयः प्रश्नः २ १` prints *between* praśnas,
  so it lands at the head of each praśna's first anuvāka, with the śānti-pāṭha and
  `॥ हरिः ओ(४)म् ॥` behind it at a kāṇḍa boundary.
- **461 units** — a repeated citation was skipped without advancing the read cursor, so the
  previous praśna's anukramaṇī *and its citation* were handed to the next anuvāka. This is why
  `7.1.1` opened with the tail of `6.6.11`. Filed as **G37**.

**A probe for the apparatus's visible words found 78.** The other 427 leaks are ordinary-looking
Sanskrit from the neighbouring unit with nothing distinctive to grep for — so the instrument
undercounted by 6×, and a probe is exactly what anyone would reach for. The number came out of a
before/after diff of every unit, not a search.

**The converter's own comment described a fix it had not made** — *"start AFTER the first citation
… otherwise anuvāka 1 swallows the preceding śānti"* — and then rebuilt anuvāka 1 from a fixed
4,000-character window that swallowed it anyway. `rule:safety-flag-needs-a-test`, in a file that
had no tests.

**Gated as a prefix cut.** All 505 changes verified to leave the new text a *suffix* of the old:
0 rewritten, 0 grown, 43,492 characters removed, keys byte-identical so nothing renumbered.
`guard()` now refuses to write if `1.1.1` does not open `इषे त्वोर्जे त्वा` or if any citation,
heading or kāṇḍa front matter survives — **both mutations make the converter exit 1 rather than
emit**, and mutation A independently re-derived the 461.

**The short anuvāka is now located: `1.2.7`.** Praśna 1.2 runs 1..14 with 7 absent from the
source's own citation sequence, in both occurrences. Whether the TEXT is absent or merged into a
neighbour is **undetermined** (G12) — and the accented 981pp scan staged the same day is the
witness that would settle it.

**Structure blocks added to both**, which is what cleared the validator: Taittirīya declares
`kanda / prasna / anuvaka` at `count_authority: range` with `known_gaps: ["1.2.7"]`; Muṇḍaka
declares `mundaka / khanda / mantra` at `firm`, 64 canonical mantras plus the śānti at `0.1`.

**9 new tests, 3 mutations checked red for their stated reason.** `test_taittiriya_samhita.py` is
this text's first.

---

## 2026-09-04 · Two scans supplied, and only one is what the batch implied

Detail, rights and the identification method: `docs/SOURCES.md` §"Supplied 2026-09-04". Both are
`no-text` scans, both staged, neither converted.

| file | is | rights | why it matters |
|---|---|---|---|
| `1784366669.pdf` (981pp) | **Taittirīya Saṃhitā**, accented, with anukramaṇī | **CC-0** — Jangamwadi Math / eGangotri | a MANTRA-level printed witness; the held text is anuvāka-level |
| `Mundaka … Gita Press.pdf` (136pp) | Muṇḍaka, Śāṅkara-bhāṣya + **Hindi** | not established — early leaves OCR blank | proofing, and a Hindi witness for a corpus at 0% translated |

**The unnamed file is not a Muṇḍaka and is not even an Upaniṣad**, despite arriving in the same
batch as one. Identified at its page 979 by colophon —
`इति तैत्तिरीयसंहितायाः सप्तमकाण्डः समाप्तः ॥ ७ ॥`. G26 records nine sources that were a
different text than their NAME implied; this is the same failure with **adjacency** standing in
for a name.

**Neither is needed for structure, and that is the point of saying so.** Muṇḍaka is already
canonical (64 mantras, 2026-09-02) and Taittirīya's 650 anuvākas were verified the same day. What
the Taittirīya scan offers is finer granularity and an accented reading — and **svara marks are
exactly what OCR mangles**, so its gate is accent fidelity, not word accuracy alone.

**One defect found while checking, fixable with no OCR at all:** `taittiriya_samhita`'s unit
`1.1.1` prepends the śānti-pāṭha and the edition's front matter
(`हरिः ओ(३)म् … प्रथमकाण्डे प्रथमः प्रश्नः १ १`) before the true opening `इषे त्वोर्जे त्वा`.
**Not an off-by-one** — nothing is shifted, so it is unlike Muṇḍaka's defect; it is text-field
contamination inside one unit, repairable from the held HTML. That text also still lacks the
`structure` block that fails it in `validate_corpus.py`. Both are one small piece of work.

---

## `../../../sanskrit-texts-sources/` — source scans, kept out of git

Physical form of this repo's source-out-of-git policy (`docs/DECISIONS.md` 2026-07-17). Lives one directory up, at workspace root — nothing in this repo previously named it (fixed here). Now gitignored at the **workspace** level (`../../../.gitignore`).

Contents — **derive the size, never restate it**: `du -sh ../sanskrit-texts-sources`. This read `310MB total` until 2026-09-04, when two supplied scans (Taittirīya Saṃhitā 981pp, Muṇḍaka Gita Press 136pp) took the tree past 2 GB. The list below is likewise partial:

- `Siddhanta/SuryaSiddhanta/1770115260.pdf`
- `Siddhanta/Panchasiddhantika/panch_siddhantika_040577_hr6.pdf`
- `Muhurta/MuhurtaMartanda/1759902040.pdf`
- `Muhurta/MuhurtaChintamani/muhurt_chintamani_002342_hr6.pdf`
- `Hora/Parashari/Saravali/saravaliofkalyan01kalyuoft.pdf`
- `sanskrit-texts-prerewrite-e0613c4.bundle` (156MB) — the pre-history-rewrite safety net referenced in `b4aa78f`'s commit message. The rewrite itself appears complete (`e0613c4` is not present in current `main` history), but no `docs/DECISIONS.md` entry records the completion — noted here since it isn't being backfilled as a full decision entry.

~~**Straggler:** `Hora/Parashari/Saravali/saravaliofkalyan01kalyuoft.pdf` still sits inside this repo too~~ — **cleared, verified 2026-09-04.** That directory now holds only `Saravali.json`, and the sole copy of the PDF is in the sources tree. Re-derive rather than trusting this line:

```sh
find sanskrit-texts -name '*.pdf' -o -name '*.txt' -o -name '*.html' | grep -v /docs/    # expect no output
```

---

## 2026-09-08 · Brahmasphuṭa Siddhānta re-OCR, and a chapter withdrawn on a false claim

**19 of 24 chapters, 639 verses** (was 19 / 578). Re-OCR'd from Rupali's 336pp scan with
`-l script/Devanagari`, which beat `san+script/Devanagari` on the GRETIL-witnessed chapters
(65/66 vs 62/66 on ch.12). Witnessed alignment went 163 → 191 verses, gaps 51 → 23, mean
similarity 0.634 → 0.675, ch.12 v1 fidelity 76% → 80.5%.

**The re-OCR nearly shipped a chapter loss on a false premise, and that is the story worth
keeping.** Chapter 11 was withheld, and `count_authority_reason` asserted its verse 56 was
"printed three times ... confirmed directly against the image, not an OCR misread." The cache
reads p.151 as `५७ ५६ ५६ ६० ६१ ६२`; a second render at fixed 193dpi reads
`५७ ५८ ५९ ६० ६१ ६२`. Tesseract was collapsing **८→६ and ९→६**. No edition prints 57, 56, 56, 60.

The tell was already in the converter's own output and nobody had pivoted it: **verse 9 was
missing from nine different chapters** (2.9, 3.9, 4.9, 5.9, 9.9, 12.9, 14.9, 15.9, 17.9). Nine
lacunae at one ordinal is one misread digit. Recorded as **G44** (a repeated verse number is a
digit collapse before it is an edition defect) and **G45** ("confirmed against the image" nearly
always means confirmed against *one render*; this scan's pages are mixed 185–193 native ppi).

**The fix is corroborated bridging, not a wider bridge.** `repair()`'s `max_bridge=1` ceiling is
deliberate — its docstring records that a wider arithmetic bridge was tried and rejected for
pairing up independent misreads and swapping real verses. So the unconditional ceiling is
unchanged, and a bridge up to 3 slots may fire **only** where a second, independently rendered
OCR pass read the proposed numbers *in order*. The two passes' errors are uncorrelated — across
pp.137–170 they disagreed on 8 of 34 pages with neither dominating — which is precisely what
makes them usable as mutual witnesses. Ch.11's repair (`56→58`, `56→59`, pinned by 57 and 60)
is the only one that fired.

**A third witness settled it independently of both OCR passes:** the recovered chapter runs
1..63 against the source's own `॥६३॥` colophon. A stated colophon count is stronger than either
render and cheap to check — do it after every corroborated repair.

The safety property is the refusal, and it is mutation-tested both ways: with corroboration
disabled, a 2-slot bridge fires uncorroborated and exactly the corroboration tests go red.
374 tests green (was 368), determinism byte-identical, dedupe loss unchanged at 71, validator
baseline unchanged (66 texts / 103 errors / 6 failing).

**ch.13 recovered 2026-09-08 by per-chapter source selection — 20 of 24 chapters, 676 verses.**
Neither OCR pass wins globally: native reads ch.1/10/22 better, the 193dpi pass reads ch.13
better, and rendering each page at its own exact native ppi (the option G41's reasoning
predicts should dominate) came *second* in both chapters tested. The pages are a 185/193 ppi
mix, so any single value is off-native for about half of them. A chapter whose default reading
blocks may now be built from the alternate pass, but only where the two agree on **content** —
never on the terminator digit, which is the one thing an apparatus footnote imitates perfectly
(G47). ch.13 lands 37 verses with 11 honest gaps, not the ~49 its number sequence implied.

**ch.24 recovered 2026-09-08 — 21 of 25 chapters, 691 verses — and it was never an OCR problem.**
The `CHAPTERS` table declared ch.24 as pp.319-336, merging two colophon-separated chapters into
one range; the resulting duplicate block `[1..15]` was recorded as *"numbering genuinely restarts
mid-chapter … needs a `subsection.verse` key this schema does not have."* Nothing restarts —
p.322 carries the Saṃjñādhyāya's colophon and p.323 opens `अथ ब्रह्मगुप्तकृतो
ध्यानग्रहोपदेशाध्यायः`. Split there, **ch.24 is complete at 15 verses with zero gaps**, and the
Dhyānagrahopadeśādhyāya becomes ch.25, which blocks on its own duplicates. No schema change was
needed (G48). `expected_chapters` is now derived from the table rather than hardcoded, and the
25th is a stated ambiguity: the edition numbers the Saṃjñādhyāya 24th, gives the appended section
no ordinal, and declares the work complete twice.

**Still absent:** ch.1, 10, 22, 25.

**Source-tree naming pass, 2026-09-08.** 30 source files carried names identifying nothing — 18
bare sanskritdocuments ids, 8 unix-timestamp PDFs, plus stale descriptors. Each was identified
from its own title page rather than its directory, and the sd id is kept as an `-sdNNNN` suffix so
provenance survives. Mapping: `RENAMES-2026-09-08.tsv` in the gitignored sources tree, which has
no git history to recover a rename from. Three scope findings fell out, all actioned: the
`GargaSamhita` file was the **Vaiṣṇava Purāṇa** (G26's original collision) and was **removed** —
Youvan already holds it digitised as `krishna_sahasranama_stotram_garga`, so nothing was lost; the
Āpastamba **Paribhāṣāsūtra** and **Śrāvaṇī** are Kalpa and **went to Youvan** (YV-036), the former
filling a declared-but-empty stub. The Āpastamba *Dharmasūtra* stays — genre is dharma. None was forced open. Ch.22's guard block is a
*confirmed genuine* source duplicate at v46 — an earlier "recovery" of it was a new OCR misread
masking that, and was correctly reverted rather than shipped. **Re-checked against both passes
2026-09-08 per G45 and it stands:** the alternate pass offers one candidate there, itself
apparatus noise, scoring 0.532 against one of the two genuine texts. That is over the ordinary
0.5 corroboration bar, which is exactly why arbitrating a primary-source duplicate needs a
higher one (0.85). Mutating that bar down admits ch.22 at 35 verses, silently picking a side of
a real, unresolved defect. Ch.24 is structural
(`subsection.verse` segmentation, unbuilt).

**The pre-existing ch.18 defect is FIXED, and its reported form was wrong twice over.** It was
logged as "v77/v79 swapped and a wrong v82", blamed on a repetitive refrain defeating
similarity scoring. Re-derived rather than taken as given: **v82 was never defective** (0.792
against its own number, unambiguously its best match) and the refrain was not the cause.

The real cause is structural. **This edition prints those verses in the reverse order to
GRETIL** — its own printed numbering on p.257 runs `७१ ७२ ७३` and carries GRETIL 79 ahead of
78 and 77 — and `align_to_gretil` is a monotonic Needleman-Wunsch DP, which *cannot represent
a transposition*. Given an order it cannot encode it assigns blobs to consecutive numbers in
printed order and mislabels both, silently: contiguous numbering, right verse count, intact
text, only the labels crossed. An edition difference, not OCR damage — no re-render at any
resolution could have fixed it.

Repaired by `_repair_transpositions`, gated on a similarity margin **and** at least one
confident side (two mutually-noisy verses can improve on each other while neither pairing is
real). Sweeping the whole text found **three, not one**: ch.18 23/25 (+0.497), ch.18 77/79
(+0.459), ch.19 4/5 (+0.926 — 0.294/0.230 as printed, 0.717/0.734 swapped). **Two were
entirely unknown.** 639 verses unchanged; this relabels, it does not add or drop text.

The margin turned out to be the **termination guarantee** as well as a quality gate — mutating
it away did not fail a test, it hung, so a non-positive margin now raises by name. G46.

