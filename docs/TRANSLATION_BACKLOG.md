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

### How to check the result before handing it back

```sh
./.venv-corpus/bin/python -m sanskrit_texts.translation_status <file>   # per-verse defects
./.venv-corpus/bin/python scripts/check_inventory.py                    # must exit 0
CORPUS_REQUIRE_DB=1 ./.venv-corpus/bin/pytest tests/ -q                 # 205 pass, 0 fail
```
