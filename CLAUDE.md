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
  VarahamihirDaivagnavallabh/  Varahamihircharita_daivagya_vallabh.json
  [README-only stubs]          Saravali, UttaraKalamrita, SarvarthaChintamani, PrashnaMarga, JatakaTattvam
Samhita/
  BrihatSamhita/               Varahmihir_brihatsamhita.json + brihatsamhita2.json
Vedanga-Jyotisha/
  Rigveda/Aarchjyotisham/      Aarchjyotisham.json
  Yajurveda/Yajushajyotisham/  Yajushajyotisham.json
Siddhanta/                     README stubs only (texts not yet digitized)
SamudrikShastra/               README stubs only
docs/
  BPHS_Master_Lexicon.md
  BPHS_Only_Terminology.md
  TRANSLATION_FLAGS.json       Machine-readable index of all untranslated/partial shlokas
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
- `category` — `"hora"` | `"samhita"` | `"vedanga_jyotisha"` | `"siddhanta"` | `"samudrika"`
- `status` — `"translated"` (both languages present) | `"partial"` (one language) | `"untranslated"` (neither)
- `number` on shlokas — integer for most; string like `"1/2"` for half-shlokas (valid in Sanskrit texts)
- Files covering a single chapter still use the `chapters` array (one element) — uniform iteration in the seed script

**Do not add back** `source`, `header`, `book`, `english_meaning`, `hindi_meaning`, `source_file`, `source_chunk`, `is_duplicate` — these were pre-normalization artifacts.

## text_id registry

| text_id | Directory | Shlokas | Translation |
|---------|-----------|---------|-------------|
| `bphs` | Hora/BrihatParasharaHoraShastra/ | 3867 | 97% |
| `brihat_jataka` | Hora/BrihatJataka/chapters/ | 409 | 100% |
| `bhrigu_sutram` | Hora/Bhrigusootram/chapters/ | 568 | 100% |
| `chamatkar_chintamani` | Hora/Chamatkarchintamani/chapters/ | 112 | 100% |
| `jataka_parijata` | Hora/Jatakaparijatah/chapters/ | 1772 | 88% |
| `laghu_jatakam` | Hora/Laghujatakam/chapters/ | 168 | 100% |
| `minaraja_yavana_jataka` | Hora/MinarajaYavanajataka/chapters/ | 2139 | 99.5% |
| `phaladeepika` | Hora/Phaladeepika/ | 851 | 93% |
| `shatpanchashika` | Hora/Shatpanchashika/ | 56 | 100% |
| `varahamihir_daivagnavallabh` | Hora/VarahamihirDaivagnavallabh/ | 248 | 100% |
| `arch_jyotisham` | Vedanga-Jyotisha/Rigveda/Aarchjyotisham/ | 36 | 100% |
| `yajusha_jyotisham` | Vedanga-Jyotisha/Yajurveda/Yajushajyotisham/ | 44 | 100% |
| `brihat_samhita` | Samhita/BrihatSamhita/ | 2770 | 19% ⚑ |

Note: Shloka counts reflect deduplication by (chapter, shloka) key — BPHS chunks and brihat_samhita
files had overlapping entries that inflated previous counts. Unique counts are authoritative.

⚑ = flagged in `docs/TRANSLATION_FLAGS.json`

## Translation workflow

**Adding/updating translations:** Edit `english` and `hindi` fields directly in the JSON file. Update `status` accordingly (`"translated"` when both are present, `"partial"` if only one, `"untranslated"` if neither). Do not leave status stale.

**Proofreading Devanagari text:** Edit the `.md` source file and re-run the AstroAcharya parser if one exists for the text. The `.md` is the canonical source for the Sanskrit text; `.json` is the derived form.

**Do not commit processing scripts** (batch*.py, inject*.py etc.) to this repo — they were throwaway tools and have been removed. Future translation patches should directly update JSON.

## Conventions

- BPHS is split into 10-chapter chunks (`BPHS0110`, `BPHS1120`, …) — keep that chunking when editing
- Devanagari shloka boundary markers (`॥ १२॥`) must be preserved in `.md` files
- Commit messages: `feat: Added <Lang> translations for <Text> ch<N>` or `fix: Corrected <Text> ch<N> shloka <M>`
