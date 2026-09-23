# Translation backlog — what needs doing, and in what order

**Do not trust the numbers in this file. Derive them:**

```sh
cd "$HOME/Documents/GitHub/Vipin Kaushik/sanskrit-texts"
python3 scripts/translation_backlog.py      # per-text table, sorted by outstanding
```

The **tiering** below is a judgement call and is not derivable. The **counts** are, and
`rule:state-and-decisions` is explicit that a count in a doc rots faster than anything else in
it. Last derived **2026-09-23**: **2,791 to translate** (2,675 empty + 116 one language missing) ·
**68,051 verses carrying a draft** · **0 stubs** · **44 of 66 texts complete**, 98,142 verses.

(Read 48 of 70 on 2026-09-17. **Only the denominators moved**: four unregistered texts left the
corpus on 2026-09-23 — `deva_keralam` and `dharmasindhu` quarantined, the two Taittirīya texts
handed to Youvan — and all four counted as "complete", because their `english`/`hindi` fields
were full of material that was not a translation. The outstanding-work figures are untouched,
which is the tell that none of it was ever real work. G62.)
(2026-09-14 read 79,597 · 1,315 · 178. The swing is not new work: on 2026-09-16/17 the fake served
"translations" were moved OFF the served fields into drafts, so most of the corpus changed column.)

## Three different jobs, and they must not be handed out as one

**A draft is not necessarily a translation.** Run the confidence checker before assigning drafts —
`python -m sanskrit_texts.checks` — and split by its level (2026-09-17, English drafts):
**67,228 fail** (`template-prefix` "Classical text translation of X: <the Sanskrit>", or
`sanskrit-echo`) and are **translate-from-scratch** work despite sitting in a draft field;
**1,692 show no defect** and are the real verify queue. Handing the 67,228 out as "verify" asks a
reviewer to approve Sanskrit wearing an English prefix.

| job | scope (2026-09-17) | what the worker does |
|---|---|---|
| **Translate** | **2,791** empty or one-language verses, plus the **67,228** failing drafts | Sanskrit → English (and Hindi where wanted). For a failing draft, ignore the draft entirely |
| **Verify a draft** | **1,692** English drafts with `no-defect-found` | Read the Sanskrit, correct the draft, then promote with `python -m sanskrit_texts.promote --to approved --author <name> --confidence certain|probable|tentative`. **Never copy a draft across unread**; `no-defect-found` means no known defect shape, not correct (G55) |
| **Re-translate a stub** | **0** — the 178 `phaladeepika` templates are now drafts that fail `template-prefix`, i.e. in the Translate row | — |

**Tier counts below were written 2026-09-14 and are shlokas held, not outstanding work.** Four texts
have since changed size from the SARIT relabel (G64): `manu_smriti` 2,688 · `caraka_samhita` 9,654 ·
`susruta_samhita` 8,347 · `astanga_hridaya` 7,725. Derive outstanding per text with the script above.

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
