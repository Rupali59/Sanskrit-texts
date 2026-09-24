# Translation backlog — what needs doing, and in what order

**Do not trust the numbers in this file. Derive them:**

```sh
cd "$HOME/Documents/GitHub/Vipin Kaushik/sanskrit-texts"
python3 scripts/translation_backlog.py      # per-text table, sorted by outstanding
```

The **tiering** below is a judgement call and is not derivable. The **counts** are, and
`rule:state-and-decisions` is explicit that a count in a doc rots faster than anything else in
it. Last derived **2026-09-23**, after the ECHO split below: **70,410 to translate** · **1,070
real drafts to verify** · **0 stubs** · **38 of 66 texts complete**, 98,258 verses.

**The previous reading on this line was `2,791 to translate · 68,051 carrying a draft`, and the
work did not change — the column did.** `translation_backlog.py` reported every populated
`english_draft` as `VERIFY-DRAFT`, which reads as *"written, awaiting review"*; 67,967 of them
hold the verse's own Sanskrit behind a label, or a label repeated across the text, and there is
nothing in them to verify. §"Three different jobs" below had said so since 2026-09-17 from the
confidence checker — **the tool simply did not reflect its own repo's finding for six days.** The
script now splits `ECHO` from `DRAFT` and mirrors `sanskrit_texts.checks.check_translation`, with
`tests/test_translation_backlog.py` asserting the mirror cannot drift from it.

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
| `garga_hora` | 84 | chapter 1 only, 84 verses |

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

## Brief for the translation run (Antigravity) — 2026-09-24

**60,543 verses need a translation.** Every one of them has clean, genuine Sanskrit in `text`;
the blocker is translation, not digitisation. Derive the current list, never trust this table:

```sh
cd "$HOME/Documents/GitHub/Vipin Kaushik/sanskrit-texts"
./.venv-corpus/bin/python scripts/translation_backlog.py
```

### THE ONE THING THAT MUST BE FIXED FIRST

**Join on `(chapter, verse number)`, never on the verse number alone.** Verse numbers REPEAT
across chapters in almost every text here. On 2026-09-24 a join keyed on the number alone wrote
Sūtrasthāna's translations onto the same-numbered verse of every other sthāna in
`astanga_hridaya` — **214 verses served a translation belonging to a different verse**, and
nothing caught it: `status` stayed `translated`, counts were unchanged, no Devanāgarī appeared
in the English, and the `(chapter, number)` keys stayed distinct so the seeder's dedupe had
nothing to catch. It was found by noticing one verse's translation appeared six times.

The exposure in the remaining work, by how many verse numbers recur and how many copies each has:

| text | verses to do | numbers that recur | max copies |
|---|---:|---:|---:|
| `astanga_sangraha` | 9,382 | 2,088 | 6 |
| `caraka_samhita` | 9,643 | 2,055 | 8 |
| `rigveda_samhita` | 10,470 | 2,014 | 10 |
| `susruta_samhita` | 8,296 | 1,686 | 6 |
| `atharvaveda_samhita` | 6,091 | 1,127 | **20** |
| `bhela_samhita` | 2,813 | 687 | 8 |

`tests/test_translation_alignment.py` now fails if one English string is served for two different
Sanskrit verses, so a recurrence is caught on the first batch rather than after 27,000 verses.

### Four more rules the last run broke, each cheap to honour

1. **Write to `english_draft` / `hindi_draft`, never to `english` / `hindi`.** Those are the
   served fields; the publication gate is structural, and `seed_texts.py`'s allowlist is what
   keeps drafts off the public API. A human promotes.
2. **Normalise output to NFC.** `4195d69` normalised the whole corpus and pinned it with a test;
   the last run wrote 360 composed-form values back in.
3. **Clear the draft when promoting.** 8,818 verses ended up holding a served translation *and* a
   draft, with nothing recording which was verified.
4. **Re-derive the text-level `status`** with `reader.derive_text_status`, and update the text's
   row in `docs/INVENTORY.md` in the same change. Four texts were left claiming `drafted` at 0%
   while fully translated.

### Do NOT emit a label instead of a translation

67,820 "translations" once turned out to be the Sanskrit behind an English prefix, and 836 more
were topic labels. Both shapes are now detected and will be reported as untranslated:

```
Classical text translation of <Title>: <the Sanskrit verse>      <- not a translation
Scholarly English translation of Chapter N, Shloka N, following… <- not a translation
Chapter 21, Shloka 11 - Description of the subtle effects of…    <- not a translation
```

### The work, in priority order

**Āyurveda — 30,134 verses, and the best-conditioned batch.** `caraka_samhita` 9,643 ·
`astanga_sangraha` 9,382 · `susruta_samhita` 8,296 · `bhela_samhita` 2,813 · `astanga_hridaya` 72.
All five have clean Sanskrit — zero Latin contamination, zero empty verses, median verse length
85–97 characters — and each names its own authority, so the text is identifiable rather than
merely plausible: Caraka's `इति ह स्माह भगवानात्रेयः`, Suśruta's `यथोवाच भगवान् धन्वन्तरिः`,
Aṣṭāṅga Saṅgraha's `अथात आयुष्कामीयं नामाध्यायं व्याख्यास्यामः`. `astanga_hridaya` is 99% done
and its 72 are the tail.

**Vedic Saṃhitās — 21,042.** `rigveda_samhita` 10,470 · `atharvaveda_samhita` 6,091 ·
`shukla_yajurveda_samhita` 1,965 · `samaveda_samhita` 1,866 · `taittiriya_samhita` 650. Note
`atharvaveda_samhita` has up to **20** copies of a verse number — the highest join risk in the
corpus — and `samaveda_samhita` is a single chapter with no repetition at all, so it is the
safest place to prove a fixed join key.

**Sthāpatyaveda — 8,520.** `manasara` 5,169 · `mayamata` 3,351.

**Jyotiṣa and the short tail — 847.** `garga_hora` 294 (chapters 2–3, whose numbering is
**positional and uncitable** — see `SOURCES.md`; translate by position, never cite a number) ·
`phaladeepika` 178 · `katha_upanishad` 98 · `shvetashvatara_upanishad` 92 · `grahaganita` 62 ·
`panchasiddhantika` 49 · `minaraja_yavana_jataka` 2.

### How to check the result before handing it back

```sh
./.venv-corpus/bin/python -m sanskrit_texts.translation_status <file>   # per-verse defects
./.venv-corpus/bin/python scripts/check_inventory.py                    # must exit 0
CORPUS_REQUIRE_DB=1 ./.venv-corpus/bin/pytest tests/ -q                 # 205 pass, 0 fail
```
