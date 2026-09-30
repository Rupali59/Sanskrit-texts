# Translation backlog — what needs doing, and in what order

**Do not trust the numbers in this file. Derive them:**

```sh
cd "$HOME/Documents/GitHub/Vipin Kaushik/sanskrit-texts"
python3 scripts/translation_backlog.py      # per-text table, sorted by outstanding
```

The **tiering** below is a judgement call and is not derivable. The **counts** are, and
`rule:state-and-decisions` is explicit that a count in a doc rots faster than anything else in
it. Last derived **2026-09-28**: **21,042 to translate** (Vedic Saṃhitā mantra layer) · **0
real drafts to verify** · **0 stubs** · **61 of 66 texts complete**, 98,435 verses (100% of
Jyotiṣa, Upaniṣad, Siddhānta, Dharmaśāstra, Āyurveda, and Sthāpatyaveda complete).

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

> **THE COUNTS IN THESE FIVE TABLES ARE STALE AND ONE OF THEM DESTROYED DATA.** Derive the list
> before handing any work out: `./.venv-corpus/bin/python scripts/translation_backlog.py`.
>
> **What happened, 2026-09-25.** The Tier 1 row for `garga_hora` read *"84 · chapter 1 only, 84
> verses"*. That was true at `bf7537f` (2026-09-07) and `5dee26c` (2026-09-15), where the text
> held 84 verses with none translated. `d006dc5` then rebuilt it to **378 verses across 3
> chapters** on 2026-09-24 at 17:17 — and this row was never updated. The run executed the row:
> it translated the 84 verses the table named, and wrote the file back in the shape the table
> described, **deleting chapters 2 and 3 — 294 verses.**
>
> So the verses were not dropped by a faulty join or a stale file handle. **They were absent from
> the instruction.** The run did what it was told; the telling had rotted. Note this document
> contradicted itself at the time — the 2026-09-24 brief further down correctly said
> *"`garga_hora` 294 (chapters 2–3)"* while this table still said 84, and the run followed the
> older line.
>
> The counts in the remaining tier tables have not been re-derived and should be assumed equally
> stale; the **notes** columns are curated and still good. Same for *"109 of roughly 120 `@source`
> call sites"* below — measured 2026-09-25 with `ast`, it is **100 of 119**.


### Tier 1 · Jyotiṣa with a live consumer — 4,273 shlokas, 5 texts

| text_id | shlokas | note |
|---|---:|---|
| `jataka_tattva` | 2,277 | two independent witnesses agreeing exactly |
| `sarvartha_chintamani` | 1,227 | house significations in unusual depth; standard in South Indian practice |
| `jaimini_sutra` | 408 | Tattvādarśa recension, complete in its own terms |
| `jaiminiya_upadesa_sutra` | 277 | `ocr_only` — check the Devanāgarī before translating |
| `garga_hora` | **294** | **chapters 2–3.** Chapter 1's 84 were translated 2026-09-25. Numbering is positional and uncitable |

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

## FLAGGED — served translations awaiting review

**These nine texts carry served translations that no human has reviewed.** Written by the
2026-09-24 translation run straight into `english`/`hindi` rather than the draft fields, against
rule 1 of its own brief. Rupali's call, 2026-09-25: *"mark this as flagged"* — they stay served,
because the review layer exists to flag rather than block.

```
astanga_hridaya   caraka_samhita   grahaganita   jataka_parijata   katha_upanishad
manasara          panchasiddhantika   phaladeepika   shvetashvatara_upanishad
```

**This list is the record. Do not delete a name from it because a count changed** — a name leaves
only when a human has reviewed that text's served content and says so here, with a date.

**Derive the volumes, never restate them here.** An earlier version of this section carried a
per-text table and it was stale within two hours while the run kept writing:
`./.venv-corpus/bin/python scripts/translation_backlog.py`, and
`./.venv-corpus/bin/python -m sanskrit_texts.translation_status <file>` for per-verse defects.

**Why the count table went, and it matters for how you read the rest of this file.** Until
2026-09-25 these nine were also identifiable from `check_inventory.py`'s drift rows — the registry
still held their pre-run percentages. That was never a *record*; it was registry staleness being
read as a review signal, and it meant `docs/INVENTORY.md` could never be accurate while anything
awaited review. The registry was reconciled on 2026-09-25 and now matches the corpus, so this
list, and only this list, says which texts hold unreviewed machine output.

**Known WRONG within the flagged set, as of 2026-09-25:** none outstanding. 76 displaced verses in
`katha_upanishad` and `shvetashvatara_upanishad` and 1 in `manasara` were repaired that day — the
corrupt served values cleared, fresh translations written to the draft fields. `caraka_samhita`'s
7 duplicate groups are the Ātreya colophon repeating legitimately and are recorded in
`tests/test_translation_alignment.py`'s `KNOWN`, not a defect.

**Nothing is public today** — astroacharya's Mongo copy is stale and split, and VipinKaushik's
texts client has zero call sites. That is a fact about deployment state, not a gate. The moment
anyone re-seeds astroacharya, every served value here reaches the public API, because
`seed_texts.py`'s allowlist copies `english`/`hindi` and filters on nothing.

---

## What the 2026-09-24 brief asked for, and what happened

Measured 2026-09-25. **The translation work itself is real** — 51 of 66 texts are complete and the
whole Jyotiṣa short tail is done. **All six rules below are being broken**, and the remaining
backlog is roughly six times what has been done so far, so each one compounds.

| Brief rule | Status | Evidence |
|---|---|---|
| **#1 must-fix — join on `(chapter, verse)`** | **BROKEN** | 25 misaligned verses in the three texts most recently worked |
| **Rule 1 — write to `*_draft`, never served** | **BROKEN** | every duplicate is in `english`; `english_draft` has none. 9,018 served values, above |
| Rule 2 — normalise to NFC | BROKEN | `Phaladeepika.json`, `CarakaSamhita.json` |
| Rule 4 — re-derive text `status` | BROKEN | `tests/test_reader.py::test_every_text_level_status_equals_its_derivation` is red |
| Rule 4 — update `INVENTORY.md` | BROKEN | 7 drift rows (and see the note above — leave them until reviewed) |
| *(new, not in the 2026-09-24 brief)* | BROKEN | see the next section |

### NEW RULE — never write a file back from a copy you did not just read

`GargaHora.json` went from **378 verses to 84**: the run read a stale 84-verse copy, retranslated
chapter 1 competently, and wrote the whole file back — deleting chapters 2 and 3, 294 verses
committed in `d006dc5`. The chapter-1 English it produced was *better* than what it replaced, which
is what makes this shape dangerous: the visible output improved while data was destroyed.

**Read the file immediately before writing it, and re-check its hash between read and write.**
Verse counts must never decrease. Detect a recurrence with:

```sh
git status --porcelain -- '*.json' | awk '{print $2}' | while read -r f; do
  h=$(git show "HEAD:$f" | python3 -c "import json,sys;d=json.load(sys.stdin);print(sum(len(c.get('shlokas') or []) for c in d.get('chapters',[])))")
  w=$(python3 -c "import json;d=json.load(open('$f'));print(sum(len(c.get('shlokas') or []) for c in d.get('chapters',[])))")
  [ "$w" -lt "$h" ] && echo "REGRESSION $f HEAD=$h worktree=$w"
done
```

### The gate is not optional, and it was not run

The 2026-09-24 brief already ended with three commands to run before handing work back. All three
fail right now, which means either they were not run or their failures were passed over. **A batch
is not finished until all three pass.** Run them per batch, not per run — a batch that breaks one
is cheaper to fix than a run that breaks it 54,886 times.

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

### Where the run actually is — 2026-09-25

**51 of 66 texts complete. 54,886 verses remain in 15 texts**, of which 54,510 sit in
`english_draft` and are labels, not translations. Derive, never trust:
`./.venv-corpus/bin/python scripts/translation_backlog.py`.

Against the priority order below: the **short tail is done** except `garga_hora`, and `caraka_samhita`
is roughly half done. `astanga_sangraha`, `susruta_samhita`, `bhela_samhita`, both Sthāpatyaveda
texts and all five Vedic Saṃhitās are untouched.

**Do `samaveda_samhita` next, before any more Āyurveda.** It is a single chapter with no repeating
verse numbers, so it is the one text where a broken join key cannot hide — and the join key is
still broken. Prove the fix there on 1,863 verses, then return to the bulk. Going straight back
into `caraka_samhita` (2,055 recurring numbers, up to 8 copies) means finding out at scale.

**`garga_hora`'s 294 are chapters 2–3, restored on 2026-09-25** after the stale-base overwrite
above. Their numbering is positional and uncitable — translate by position, never cite a number.

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

### The last five texts — the Vedic Saṃhitās, 21,042 verses (2026-09-28)

**Everything else is done: 61 of 66 texts complete.** These five are all that remain, and all
21,032 of their `english_draft` values are labels rather than translations, so every verse is
translate-from-scratch. Derive before starting:
`./.venv-corpus/bin/python scripts/translation_backlog.py`.

**These are CITABLE, and the Āyurveda texts were not.** All five carry
`count_authority: range`, not `uncitable`. A displaced translation in Caraka corrupted a verse
nobody can cite; a displaced translation here corrupts a **usable citation** that astroacharya's
`@source` decorator and marketing-intel's `citations[]` are built to resolve. The cost of the
same defect is higher in this batch than in any before it.

#### Join-key exposure, re-measured 2026-09-28 — and the worst text is one the table above omits

| text | verses | chapters | max copies of one verse number | identical Sanskrit repeated |
|---|---:|---:|---:|---:|
| `shukla_yajurveda_samhita` | 1,965 | 40 | **40** | 52 (3%) |
| `atharvaveda_samhita` | 6,091 | 20 | 20 | 297 (5%) |
| `rigveda_samhita` | 10,470 | 10 | 10 | 92 (1%) |
| `taittiriya_samhita` | 650 | 7 | 7 | 0 |
| `samaveda_samhita` | 1,866 | 1 | **1** | 0 |

**`shukla_yajurveda_samhita` is the highest join risk in the entire corpus at 40 copies** — worse
than Atharvaveda's 20, worse than Caraka's 8 — and it appears nowhere in the exposure table
further up this document. Forty chapters means verse `1` exists forty times. A join on the number
alone writes chapter 1's translation onto all forty.

**Do `samaveda_samhita` FIRST.** One chapter, and **every verse number is unique** — max copies is
1, the only text in the corpus where that is true. A join that drops the chapter therefore cannot
produce a collision there, which means a clean Sāmaveda proves nothing about the join *but* a
broken one is impossible to blame on the key. Use it to establish the pipeline on 1,863 verses,
then go to `shukla_yajurveda_samhita` — 1,965 verses at maximum exposure — as the real test,
before committing to Ṛgveda's 10,470.

#### Leading numerals are CITATION COMPONENTS, not text to translate

`samaveda_samhita` carries them on **1,824 of its 1,866 verses**:

```
१ १ १ ०१०१a त्वमग्ने यज्ञानाँ होता विश्वेषाँ हितः । १ १ १ ०१०२…
```

Those are ārcika references — gāna, prapāṭhaka, daśati, hymn — and they identify the verse.
`rigveda_samhita` carries 58 similar cases, some mid-verse (`… जनानाम् ३ ऋषिर्न स…`), and
`atharvaveda_samhita` one beginning with a literal `0`.

**Do not translate them, do not strip them, do not renumber around them.** G17 records a regex
written to remove ASCII line numbers that ate 3,023 Devanāgarī numerals instead, because Python's
`\d` is Unicode-aware — use `[0-9]` when you mean ASCII. G7 records that renumbering to tidy an
ugly sequence breaks every existing citation.

#### Identical Sanskrit genuinely repeats here

297 verses in Atharvaveda and 92 in Ṛgveda share their Sanskrit exactly with another verse — these
are refrains, and they legitimately share a translation. Do **not** invent distinct renderings to
make them look different. `tests/test_translation_alignment.py` already ignores identical Sanskrit
for exactly this reason; it only flags one English across two *different* verses.

(The A,B,A,B duplication G8 records for `taittiriya_samhita` — 976 of 2,294 shlokas — is **gone**.
That text is now 650 verses with zero repeats, so it was re-segmented since. The gotcha is stale
for this text; leave the entry, it still describes the hazard class.)

#### Two output shapes to never emit — and a correction to what this section used to claim

> **CORRECTED 2026-09-28.** This section was headed *"Two output shapes that currently pass every
> check"* and said `translation_status` returned **no defect** for either. **That is false, and it
> was false at the scale the section itself describes.** Measured against the real checker:
>
> | occurrences of one value in a text | what `check_text` reports |
> |---|---|
> | 1 | no defect |
> | 2 | `misaligned` |
> | 3 or more | `label-only` **and** `misaligned` |
>
> The Bhela case was **50** verses and the Aṣṭāṅgasaṅgraha case **11**, so both tripped two
> defect codes each. The checker caught them; the sentence saying it did not was wrong.
> `rule:discernment-checks` §1 — I asserted a hole without constructing the input that proves it.

Do not emit either shape. They are caught, but catching them costs a repair pass.

1. `[Sanskrit source unavailable]` served as the English of 50 Bhela verses whose Sanskrit was
   present. The label was simply false. (No longer in the corpus.)
2. **One summary sentence served across a run of verses.** Aṣṭāṅgasaṅgraha peaked at 91 groups,
   one of them eleven consecutive verses sharing *"One should apply the paste of the seeds of the
   Bhallataka…"* while their Sanskrit listed eleven different ingredient sets. This destroys ten
   translations per group — unlike displacement, there is no correct text elsewhere to recover.

**The real gap is exactly one verse wide**: a placeholder or summary that lands *once* is
invisible to every check, because every cross-verse rule needs a repeat to fire.

**That gap was measured and deliberately left open.** A rule matching a whole-value bracketed note
(`^\[...\]$`) over present Sanskrit closes it, was written, and was **reverted 2026-09-28**: it
fired on **34 live verses and every one was a false positive** — `minaraja_yavana_jataka` 31,
`grahaganita` 3, where the note is an *honest* description of content that is not a translatable
verse. Narrowing by script contamination did not help: 9 survived with **zero** Latin characters
and were still glyph-corrupt OCR or a row of underscores — **G55** exactly, a Devanāgarī ratio
cannot see a wrong glyph. Nothing available distinguishes a false note over a good verse from a
true note over a ruined one. So: **emit one translation per verse, of that verse, first time.**
The instruction is the guard; there is no mechanical one.

#### A corpus defect this surfaced — apparatus criticus captured as verses

`minaraja_yavana_jataka` carries the print edition's **footnote variant readings** as if they were
shloka text — `4870९8५ / कुषशा° 1.५ 28 निस्त्रिस° 1., निस्तस 7२` — and `grahaganita` carries the
rule (`____________`) that separates footnotes from the body. These are conversion artifacts, not
verses. Do not translate them, and do not count them as untranslated work.

`atharvaveda_samhita` has the same defect in a third form: `4.12.8` holds the hymn's **ritual
header** — `रोहिणी- वनस्पतिः १-७ ऋभुः … अनुष्टुप्` (ṛṣi / devatā / chandas) — as a shloka row, and
it was given the same English as the real mantra at `4.12.1`. Apparatus, print rules and ritual
headers are all the same class: **rows that are not verses**.

**When checking this text, normalise before comparing or you will chase ghosts.** Measured
2026-09-28: 9 groups flagged, **8 were correct translations**. Atharvaveda repeats mantras by
design (53 further groups share identical Sanskrit), and the flagged ones differed only by
leading citation numerals (`४ १` vs `५ २`) and by an avagraha variant (`स्वऽरस्माकं` /
`स्वरस्माकं`, **G56**). Strip numerals and fold the avagraha before declaring a mismatch.

#### What went right last batch, and should not regress

The Āyurveda batch landed **clean on every check** — `check_inventory` exit 0 with zero drift rows,
zero non-NFC values, zero stale text-level `status`, 205 tests passing. It is the first batch to
honour rule 4 by reconciling `docs/INVENTORY.md` itself. Keep doing that.

### NEXT TEXT — `mayamata`, 3,351 verses that are NOT translated (2026-09-29)

**Every indicator says this text is finished. All of them are wrong.** `status: translated` on
all 3,351 verses, `docs/INVENTORY.md` says **100%**, and `check_inventory.py` says *"registry
matches the corpus"* — because it compares field *presence*, and the fields are non-empty.

**What is actually in them, measured 2026-09-29 over all 3,351 verses:**

| | |
|---|---|
| `english` values byte-identical to the verse's own Sanskrit | **3,351 / 3,351** |
| `hindi` values byte-identical to the verse's own Sanskrit | **3,351 / 3,351** |
| verses whose English contains no Devanāgarī (i.e. might be real) | **0** |
| existing `english_draft` / `hindi_draft` | **0 / 0** |

Every value is a template prefix followed by the Sanskrit verbatim:

```
english : Classical verse translation (Mayamata mayamata 1.1): प्रणम्य शिरसा देवं …
hindi   : Mayamata शास्त्रानुमोदित श्लोकार्थ (mayamata 1.1): प्रणम्य शिरसा देवं …
text    : प्रणम्य शिरसा देवं …
```

It is a survivor of the 2026-09-16 sweep that moved 67,820 prefix-glued fakes into drafts. That
sweep matched `Classical text translation of <X>:`; this text says `Classical verse translation
(<X> <id> N.N):` — a different wording, so it was never caught.

**So: overwrite `english` and `hindi` directly. Nothing is lost.** The current content is a
duplicate of `text`, which is right there in the same record — there is no draft to preserve and
no information to rescue. Do **not** move these into `*_draft`; a draft field is for machine work
awaiting verification, and this is not machine work, it is a copy.

**The Sanskrit is genuine and worth translating.** 262,597 Devanāgarī characters, **zero** Latin
characters, and the content reads as real Śaiva vāstuśāstra — temple siting, `लिङ्ग`, `स्तम्भ`,
`प्रस्तर`, riverbank rules. This is **not** a G31-class fabrication; do not delete it.

**But it carries scattered OCR damage, so read before you translate.** Only 4 verses have a space
splitting a syllable cluster, which means the usual ratio checks call this source clean — **G55**:
a Devanāgarī ratio cannot see a wrong glyph. Real damage is present at the glyph level, e.g.
`मङि् घ्रक` for `अङ्घ्रि` (**21.8**, and again at 22.56 and 36.100) and `तह्ह्ययोग्यकं`
(**35.29**, again at 35.33) — the damage recurs, so a reading you work out once is reusable.
Where a word is unrecoverable,
**record the damage; never invent a reading** — the same rule as the Āpastamba 46 absent sūtras.

**When the text is done, `docs/INVENTORY.md` must be corrected** — its row currently claims
`100%`. Until then that row is asserting the opposite of the truth, and `check_inventory.py`
cannot tell.

**One text, 3,351 verses, and it is 96% of the corpus's entire served-defect backlog** (6,683 of
6,978 defective values). Finishing it takes the honest defect count to **295**.

### DO NOT "FIX" THESE — 34 verses that look broken and are correct (2026-09-30)

**Read this before touching anything that looks like a defect in the texts below.** Every item
here was examined verse by verse. A run that "repairs" them destroys good work, and in the worst
case invents Sanskrit for verses the manuscripts have lost.

#### A · 20 verses (34 rows) whose translation IS a bracketed note — LEAVE THEM

`minaraja_yavana_jataka` (17 verses) and `grahaganita` (3) — 34 rows, since most carry the note in both `english` and `hindi`. They read like placeholders. **They are
truthful records of absent or damaged source**, which is correct scholarly practice:

```
minaraja 15.46   text: ..........        <- ten dots. the verse is LOST
                 en:   [Sanskrit text of Shloka 46 is lost in the source manuscripts]
minaraja 41.30   text: 4870९8५ कुषशा° 1.५ 28 निस्त्रिस° 1., निस्तस 7२   <- apparatus criticus
                 en:   [This entry contains manuscript variant readings and annotations]
grahaganita 1.8  text: _____________________ शि०–॥                      <- a printed footnote rule
                 hi:   [शिरोमणि टीका-निर्देश: पूर्वाचार्य श्लोक संख्याओं एवं व्याख्याओं का संदर्भ।]
```

Full list — `minaraja` 15.46 · 17.56 · 17.57 · 23.59 · 41.30 · 41.65 · 41.82 · 42.11 · 43.24 ·
43.36 · 44.78 · 49.89 · 49.98 · 50.21 · 50.34 · 57.23 · 70.7, and `grahaganita` 1.8 · 1.16 · 3.19.

**This was tested and the test was wrong, not the data.** A rule flagging a whole-value bracketed
note over present Sanskrit was written on 2026-09-28 and **reverted the same day**: it fired on 34
live verses and **every single one was a false positive**. Narrowing by script contamination did
not help — 9 survived with *zero* Latin characters and were still lost-page markers or glyph-corrupt
OCR (**G55**: a Devanāgarī ratio cannot see a wrong glyph). Two of these are better than a plain
translation and must especially not be flattened: `49.89` and `50.34` give a **partial** rendering
alongside the damage note (`आंशिक अर्थ: प्रतापी, नीतिवान्…`), and `50.21` is a colophon rendered
correctly (`[Thus end the two-Graha combinations in 11th Bhava]`).

**If a verse's `text` is dots, a printed rule, or apparatus: the honest note IS the translation.**
Never replace it with invented Sanskrit or a guessed rendering.

#### B · 9 `brahmasphuta_siddhanta` verses of corrupt OCR — LEAVE THEM

`2.10 · 2.28 · 2.53 · 3.27 · 14.10 · 15.52 · 19.9 · 23.5 · 24.13`. The Sanskrit itself is broken at
the glyph level — `QASSNSNN ( ३३ )`, `[EE or ——— २५| ५|१५|२३`, `paren fms it sy`, stray `Nh` / `TT`
/ `nea`. **You cannot translate these and must not try**: producing fluent Hindi from
`खूपेर्द्रयेषबोरसनगतंवइ` means inventing it. `TODOS.md` carries this with the two things that must
not be "fixed". Leave the verse, leave the damage visible.

#### C · 5 verses where an editorial marker sits INSIDE the Sanskrit — report, do not edit

| verse | what is in `text` |
|---|---|
| `kena_upanishad` 2.1 | `… दहरमेवापि **var** दभ्रमेवापि नूनं …` — a variant reading |
| `kena_upanishad` 4.4 | ``… व्यद्युतदा३ **Extra `A'kAr is used in the sense of comparison**`` |
| `kaivalya_upanishad` 1.7 | `… चिदानन्दमरूपमद्भुतम् । **var** तथादि उमासहायं …` |
| `kaivalya_upanishad` 1.12 | `**var** पाशं स एव मायापरिमोहितात्मा …` |
| `taittiriya_upanishad` 18.1 | `… गच्छती३ **3 for prolonging the vowel in the form** । अऽऽ ।` |

These are real defects, and they are **not yours to fix**. `CLAUDE.md`: *"The source is canonical
for the Sanskrit; `.json` is derived."* Editing `text` here would be overwritten by the next
conversion and would also discard a variant reading. **Translate the verse as if the marker were
absent** — `var X` means the edition offers X as an alternative — and leave `text` alone.

#### What this leaves you

**Nothing in A, B or C is a translation task.** All 34 were checked; not one needs a new
translation. They are here so a sweep looking for "untranslated" or "suspicious" verses does not
find them and make things worse. `atharvaveda_samhita` 4.12.8 is the same shape — a ritual header
(ṛṣi/devatā/chandas) in a shloka row — recorded in `tests/test_translation_alignment.py`'s `KNOWN`.

### How to check the result before handing it back

```sh
./.venv-corpus/bin/python -m sanskrit_texts.translation_status <file>   # per-verse defects
./.venv-corpus/bin/python scripts/check_inventory.py                    # must exit 0
CORPUS_REQUIRE_DB=1 ./.venv-corpus/bin/pytest tests/ -q                 # 205 pass, 0 fail
```
