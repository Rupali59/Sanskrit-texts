# Translation backlog — what needs doing, and in what order

**Do not trust the numbers in this file. Derive them:**

```sh
cd "$HOME/Documents/GitHub/Vipin Kaushik/sanskrit-texts"
python3 scripts/translation_backlog.py      # per-text table, sorted by outstanding
```

The **tiering** below is a judgement call and is not derivable. The **counts** are, and
`rule:state-and-decisions` is explicit that a count in a doc rots faster than anything else in
it. Last derived 2026-09-14: **79,597 untranslated · 1,315 drafted · 178 stubs · 15 texts
complete**.

## Three different jobs, and they must not be handed out as one

| job | scope | what the worker does |
|---|---|---|
| **Translate** | 79,597 shlokas, 50 texts | Sanskrit → English (and Hindi where wanted). The field is empty |
| **Verify a draft** | **1,315**, all `apastamba_dharma_sutra` | A machine draft already sits in `english_draft`. Read the Sanskrit, correct it, **promote** it to `english`, flip `status` to `translated`, clear the draft. **Never copy a draft across unread** |
| **Re-translate a stub** | **178**, all `phaladeepika` | These say `status: translated` and carry a template, not a translation: `Chapter 21, Shloka 11 - Description of the subtle effects of planetary sub-sub-periods…`. The worker is **replacing** text, not filling a blank, and must be told so |

## Order of work

### Tier 1 · Jyotiṣa with a live consumer — 4,273 shlokas, 5 texts

| text_id | shlokas | note |
|---|---:|---|
| `jataka_tattva` | 2,277 | two independent witnesses agreeing exactly |
| `sarvartha_chintamani` | 1,227 | house significations in unusual depth; standard in South Indian practice |
| `jaimini_sutra` | 408 | Tattvādarśa recension, complete in its own terms |
| `jaiminiya_upadesa_sutra` | 277 | `ocr_only` — check the Devanāgarī before translating |
| `garga_hora` | 84 | chapter 1 only of 3 |

**Why first:** astroacharya cites BPHS in 109 of roughly 120 `@source` call sites, and
marketing-intel and astro-studio both want Jyotiṣa. This is the same skandha and the only
untranslated material with a consumer today.

### Tier 2 · The Upaniṣads — 2,094 shlokas, 20 texts

The whole layer, and most of it is small enough to finish in a sitting:

`chandogya` 627 · `brihadaranyaka` 431 · `mahanarayana` 263 · `katha` 120 ·
`shvetashvatara` 113 · `maitri` 99 · `prashna` 67 · `mundaka` 65 · `taittiriya` 51 ·
`kaushitaki` 51 · `kena` 35 · `aitareya` 33 · `atmabodha` 31 · `paingala` 28 ·
`kaivalya` 24 · `isha` 18 · `subala` 15 · `mandukya` 12 · `jabala` 6 · `sarvasara` 5

**Caveats that change the unit being translated.** Four declare `unit_mismatch` —
`taittiriya`, `subala`, `jabala`, `sarvasara` — meaning the held count and the cited count
disagree because the *unit* differs (khaṇḍas held, mantras cited). **Agree the unit with the
translator before they start**, or the work will not map back. `taittiriya` separately needs a
level ABOVE its current chapters: its 31 "chapters" are anuvākas numbered continuously across
three vallīs (12 + 9 + 10 = 31), so the canonical `vallī.anuvāka.mantra` citation is
unrepresentable today.

### Tier 3 · Siddhānta — 2,217 shlokas, 8 texts

`brahmasphuta_siddhanta` 691 · `panchasiddhantika` 386 · `surya_siddhanta` 280 ·
`grahaganita` 272 · `goladhyaya` 241 · `bijaganita` 150 · `lilavati` 117 · `aryabhatiya` 80

**Three of these were once fabricated and replaced** (G31 — `aryabhatiya`, `surya_siddhanta`,
`panchasiddhantika`). Translating them is what finally closes that saga: a translator reading
the Sanskrit is the check that no automated test performed.

### Tier 4 · Dharmaśāstra — 3,615 shlokas, 2 texts

`manu_smriti` 2,684 · `narada_smriti` 931. Plus the 1,315 `apastamba` **drafts to verify**,
which is the other job above.

### Tier 5 · The bulk — 67,139 shlokas, 11 texts

**84% of the backlog**, and nine of these texts exceed 2,800 verses each.

- **Āyurveda 37,577** — `caraka_samhita` 9,643 · `astanga_sangraha` 9,382 · `susruta_samhita`
  8,296 · `astanga_hridaya` 7,443 · `bhela_samhita` 2,813
- **Vedic Saṃhitā 21,042** — `rigveda_samhita` 10,470 · `atharvaveda_samhita` 6,091 ·
  `shukla_yajurveda_samhita` 1,965 · `samaveda_samhita` 1,866 · `taittiriya_samhita` 650
- **Sthāpatyaveda 8,520** — `manasara` 5,169 · `mayamata` 3,351
- `dhanurveda` 227 · `nirnayasindhu` 32

**All five Āyurveda texts and both Sthāpatyaveda texts declare `uncitable`** — nobody has
published a verse count to check them against. That is not a defect and not a blocker; it does
mean a translator's chapter/verse numbering cannot be validated against an external authority,
so **keep the source's own numbering and do not renumber** (G7).

## Before handing any text out

1. **Check `docs/INVENTORY.md` for its `count_authority`.** `ocr_only` means the Devanāgarī
   itself is unverified — the translator is working from possibly-corrupt text and should be
   told to flag rather than guess.
2. **Never renumber.** Verse numbers are live citations; a renumber breaks them silently (G7).
3. **Drafts go in `english_draft`, never in `english`.** The served field is the publication
   gate, and it is enforced by an allowlist in another repo plus a test
   (`astroacharya/tests/test_seed_texts.py::TestDraftPublicationGate`). Writing a machine draft
   into `english` bypasses the only guard there is.
4. **Record absences, never invent.** `apastamba` has 46 sūtras absent from its OCR and they
   were recorded as absent. That is the standard.

## Two texts whose verse keys are about to move

**Do not translate these until their re-ingestion lands**, or the work will be re-keyed under
the translator:

- **`jataka_parijata`** — chapter 17 is to be split to `17अ` / `17ब`, and 13 colophons stored
  as shlokas are to be relocated.
- **`saravali`** — chapters 27–54 are to be added and chapters 1–26 re-keyed from a flat single
  chapter.

Both are already fully translated, so nothing is blocked *by* them — this is only a warning
against starting corrections inside them right now.
