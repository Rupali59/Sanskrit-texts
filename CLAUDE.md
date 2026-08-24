# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Parent context: `~/Documents/GitHub/Vipin Kaushik/CLAUDE.md`

## What this repo is

An open-source corpus of classical Sanskrit texts, digitized for computational access by AstroAcharya. **Not a code project** — this is a data repository. Source of truth for proofreading: [sanskritdocuments.org/sanskrit/jyotisha](https://sanskritdocuments.org/sanskrit/jyotisha/) (see `REFERENCES.md`).

**Scope: Jyotiṣa, plus everything that is not Tantra, Mantra, Brāhmaṇa or Āraṇyaka** (narrowed 2026-08-23, narrowed again 2026-08-24 — see `../CLAUDE.md` §"Content / texts ownership"). This line read "a corpus of classical Sanskrit **Jyotisha** texts", which was already narrower than the contents — `Dharmashastra/` and `Kalpa/` are not Jyotish — and became more so when Philosophy moved here from Youvan. The Vedic corpus **Saṃhitā and Upaniṣad layers** belong here; **Brāhmaṇa and Āraṇyaka went to Youvan 2026-08-24** (ritual prose — nothing moved on disk, none were held). The line is by LAYER: seven held Upaniṣads are textually chapters of a Brāhmaṇa or Āraṇyaka and stay here — see `../CLAUDE.md` §"Content / texts ownership". `docs/VEDIC_CORPUS.md` maps all 51 texts; **29 are held** as of 2026-08-24 — all 13 mukhya Upaniṣads plus 11 minor, and the primary Saṃhitā of every Veda. Brāhmaṇa and Āraṇyaka are Youvan's, not a backlog here. Tantra and Mantra go to `Tushar/Youvan`.

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

**Neither remaining "source waiting" is what it looked like — corrected 2026-08-23.**
This said `GargaSamhita` and `MuhurtaMartanda` already have sources ready. Both claims
died on inspection:

- **`GargaSamhita`'s `3003.txt` is the wrong Garga Samhita.** Its colophon reads
  `अश्वमेधखण्डे ... अध्याय ५९` — the devotional Vaishnava Purana, not the Jyotish work.
  Digitised, then **relocated to `Tushar/Youvan/texts/Stotra/KrishnaSahasranamaStotram/`**
  (127 shlokas) under the Jyotisha/Youvan ownership split. This directory has **no source
  waiting**; the Jyotish text still needs sourcing.
- **`MuhurtaMartanda`'s PDF has no text layer.** 154 pages of `tiff2pdf`-wrapped CCITT
  bitmaps; `pdftotext` returns 154 bytes — one form-feed per page, zero characters. It is
  a scan, and additionally a *commentary edition* (mula + Sanskrit ṭīkā + Hindi
  bhāṣā-ṭīkā interleaved), so even clean OCR would not yield mula shlokas without
  separating three text layers. See `../propagation/state/sanskrit-texts/GOTCHAS.md`.

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
- `category` — `"parashari"` | `"nadi"` | `"siddhanta"` | `"samhita"` | `"veda_samhita"` | `"upanishad"` | `"vedanga_jyotisha"` | `"muhurta"` | `"dharmashastra"` | `"kalpa"`. **Re-derived 2026-08-24** — the Vedic corpus added `veda_samhita` (5 texts) and `upanishad` (24). It is a plain string in the schema, not an enum, so nothing rejects a typo: a misspelt category makes a text silently invisible to any category filter rather than failing. `prashna` and `jaimini` trees exist but hold only placeholders, so no file declares them yet.
- `status` — `"translated"` (both languages present) | `"partial"` (one language) | `"untranslated"` (neither)
- `number` — integer for most shlokas/chapters; **string** for valid source sub-divisions: `"1/2"` for half-shlokas, and a Devanagari-suffixed chapter like `"63अ"` / `"63ब"` for a sub-divided chapter (stored in files `MS_063अ.json` / `MS_063ब.json`)
- Files covering a single chapter still use the `chapters` array (one element) — uniform iteration in the seed script

**Do not add back** `source`, `header`, `book`, `english_meaning`, `hindi_meaning`, `source_file`, `source_chunk`, `is_duplicate` — these were pre-normalization artifacts.

## text_id registry

**`docs/INVENTORY.md` is the registry.** It carries every text's `text_id`, path, chapter and
shloka counts, translation state and count-authority tier, in one table. This section holds only
what a manifest cannot: the caveats that make a number mean less than it looks like.

**49 texts on the normalized schema · 775 chapters · 43,287 shlokas.** Derive it, never restate it:

```
python3 -c "import json,glob;print(sum(len(c['shlokas']) for p in glob.glob('**/*.json',recursive=True) if not p.startswith('docs/') for c in (json.load(open(p)).get('chapters') or [])))"
```

**Until 2026-08-24 this section duplicated INVENTORY's table** — 20 rows against that file's 23,
each maintained by hand, neither aware of the other. The Vedic corpus would have made it 49 rows
in two places. A second copy of a manifest is not a summary, it is a second thing to be wrong.

The Jyotiṣa texts are **100% translated**; the 29 Vedic texts added 2026-08-23/24 land
**untranslated**, which is why the corpus total is no longer a single percentage. Per-text state
is in INVENTORY.

**`bphs`** — one file since 2026-08-17 (was 11 chunks declaring 102 chapters for a
97-chapter work). 4 mis-split chapters repaired, 5 shlokas recovered; ingests **3937 of
3937**. **Translation backlog closed 2026-08-22** — the last 5 (`12.11`, `53.20`, `61.55`,
`66.43`, `66.65`) are now translated; all are single-pada fragments, a shape that occurs
13 other times in this text. Separately, **ch 25 shloka 16 is absent from the digitisation**
and was not invented, and ch 60's parenthesised duplicate is now `"12अ"` (a variant reading).

**`muhurta_chintamani` — translation complete, numbering still wrong.** `MC_001`'s
Hindi gap closed 2026-08-22 (all 206 shlokas now `"translated"`). Its chapter-1 numbers
still run 11–32, 1–7, 37–44: distinct, so they ingest, but the sequence is wrong.
`MC_REMAINING_RAW.json` in the sources repo does **not** resolve it — checked 2026-08-22,
it covers pages 53–480 with zero textual overlap with chapter 1. Fixing it needs the
chapter-1 pages of `muhurt_chintamani_002342_hr6.pdf` read against a canonical edition.

Not defects, and handled — do not "fix" them into breakage: `MinarajaYavanajataka` numbers
variant chapters `"24अ"`/`"63अ"`/`"63ब"`; `Jatakaparijatah` numbers half-shlokas `"N 1/2"`.

### ⚠ 71 shlokas never reach AstroAcharya

`seed_texts.py:92-94` dedupes by `(chapter, shloka)`, later file wins — INVENTORY's Shlokas
column counts what is *present*, not what is ingestible. Was **2,800**; `brihat_samhita` was 2,729 of
it and is now **0**, its two files consolidated 2026-08-18. They were never two recensions:
2,574 of 2,711 shared keys differed only in **sandhi** (`प्रसूतिः विश्वात्मा` vs
`प्रसूतिर्विश्वात्मा`) — one text digitised twice. Ingestion unchanged at 2,771.

Remaining, all intra-chapter and pre-existing: `jataka_parijata` 55, `laghu_jatakam` 14,
`minaraja_yavana_jataka` 1, `yajusha_jyotisham` 1.

**Re-measured 2026-08-24 across all 49 texts: still exactly 71.** The 29 Vedic texts added
**zero** duplicate keys, which is a property of the converter rather than luck — it rejects a
text with a duplicate `(chapter, number)` instead of writing it, so a collision surfaces as a
blocked conversion rather than as a shloka that quietly never ingests. The four texts above
pre-date it. Re-run the count with:

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

`manu_smriti` (12 files), `apastamba_dharma_sutra`, `apastamba_paribhasha_sutra` — 14 files,
4,737 records over 1,520 distinct keys. Checked against the canonical structures 2026-08-18
(Manusmriti = 12 adhyāyas / ~2,684 verses; Apastamba = Praśna→Paṭala→Khaṇḍa→sūtra, so `1.1.1`
is a *correct citation*). **The data cannot be mapped onto either**: `MS_001` holds ~87
fragmentary cycles; Apastamba has 219 bare-integer records and 15 literal `X.X.21`
placeholders — the digitiser recording "prefix unknown".
**Not a renumbering job — needs re-digitisation.** Detail and sources: `docs/DECISIONS.md`.
Full scope, ordered steps and open questions:
`docs/plans/2026-08-22-dharmashastra-redigitisation.md`.

**Two corrections, 2026-08-23** — re-measured, not restated:

- This said *"Manusmriti's leading component runs 1–33"*. It does not. The leading
  component is invariantly `1` (1514 of 1514 dotted records in `MS_001`); what cycles
  1→~34 and restarts is the **second** component, which reaches 315. The conclusion
  (unrecoverable fragmentation) stands — only the description of the damage was wrong,
  and it would have misled whoever executes the repair.
- **`apastamba_paribhasha_sutra` is equally broken, not a minor sibling.** Every integer
  1–53 is reused as `number` 2–15 times, plus 7 empty-string records.

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
