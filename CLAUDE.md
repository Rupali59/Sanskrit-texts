# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Parent context: `~/Documents/GitHub/Youvan/CLAUDE.md`

## What this repo is

An open-source corpus of classical Sanskrit Jyotisha (Vedic astrology) texts, digitized for computational access. **Not a code project** — this is a data repository. Source of truth for proof-reading: [sanskritdocuments.org/sanskrit/jyotisha](https://sanskritdocuments.org/sanskrit/jyotisha/) (see `REFERENCES.md`).

## Layout

Each text lives in its own top-level directory and follows a uniform two-file pattern:

- `<Text>.md` — Devanagari source. Shlokas terminated by `॥ N॥`, chapters by `॥ इति … अध्यायः ॥` (varies by text).
- `<Text>.json` — Parsed structure consumed by APIs.

Texts present: `Aarchjyotisham`, `BrihatParasharaHoraShastra` (split BPHS0110…BPHS9197), `Bhahmajjaataka` (md only), `Bhrigusootram`, `Chamatkarchintamani`, `Jatakaparijatah`, `Phaladeepika`, `Varahamihira Brihatsanhita`, `Varahamihircharita daivagya vallabh`.

`docs/` contains lexicon references for BPHS terminology (`BPHS_Master_Lexicon.md`, `BPHS_Only_Terminology.md`).

## JSON schema (uniform across texts)

```
{
  "source": "<filename>.md",
  "header": "...",
  "chapters": [
    {
      "number": 1,
      "title": "<Devanagari title>",
      "shlokas": [
        {
          "number": 1,
          "text": "<Devanagari shloka, \\n between padas>",
          "english_meaning": "...",
          "hindi_meaning": "..."
        }
      ]
    }
  ]
}
```

Translations are not always populated — `Aarchjyotisham` is fully translated; others (e.g. `Bhrigusootram_raw.json`) may have a `_raw` variant containing unparsed extraction. When adding translations, preserve the existing `(chapter, shloka)` keying.

## Working with this repo

### Parsing pipeline

The shared parser lives in the parent workspace, **not here**:

```bash
# from ~/Documents/GitHub/Youvan
source .venv/bin/activate && python scripts/parse_shlokas.py texts/
```

This regenerates JSON from MD. Do not hand-edit JSON shloka structure — edit MD and reparse, or update translations in place.

### One-off translation patching

Some texts ship with bespoke updater scripts (e.g. `Phaladeepika/batch3_update.py`) that merge a hardcoded `(chapter, shloka) → {english, hindi}` map into the JSON. These are throwaway batch tools — when adding new translations, follow the same `updates = {(ch, sh): {...}}` pattern rather than editing JSON by hand.

### Adding a new text

1. Create `<TextName>/<textname>.md` with Devanagari source proof-read against sanskritdocuments.org.
2. Run the workspace parser to generate `<textname>.json`.
3. Translations land in a follow-up commit — usually via a per-text `batch*_update.py` script committed alongside.

## Conventions

- Filenames are inconsistent across texts (`Chamatkarchintamani.json` vs `bhrigustrotram.json` vs `phaladeepika.json`). Match the existing casing of the directory you're editing — do not rename to normalize.
- Devanagari shloka numerals (`॥ १२॥`) are the boundary markers; do not strip them from MD.
- BPHS is split into 10-chapter chunks (`BPHS0110`, `BPHS1120`, …) — keep that chunking when editing; it's how the parser slices output.
- Commit messages follow `feat: Added <X>` / `feat: Added <Lang> translations for <Text>` style (see `git log`).
