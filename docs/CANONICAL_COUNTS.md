# Canonical counts and marker grammars

The acceptance thresholds the converter checks against, and the verse-terminator grammars
it must handle. Researched 2026-08-24.

**Read the citation-strength column before trusting a number.** A wrong threshold rejects
a correct parse or accepts a broken one, so a figure's provenance matters more here than
its precision. Most figures below trace to Wikipedia *citing* Deussen, Hume or Aiyar, not
to a primary edition opened directly. That is recorded, not smoothed over.

---

## Part 1 — Marker grammars

There is no single verse-terminator convention. **Five distinct grammars occur across the
sources we hold**, and choosing the wrong one does not raise: it yields almost nothing,
which reads as "this text is short" rather than "the parser is wrong".

| Grammar | Shape | Example | Used by | Measured |
|---|---|---|---|---|
| `double` | `॥ N॥` | `॥ १॥` | Rigveda, Atharvaveda, most Upaniṣads | RV 10,462 |
| `single_pair` | `।। N ।।` | `।। १।।` | Śukla Yajurveda | 1,965 |
| `dotted` | `॥ N.M.K॥` | `॥ १.१.१॥` | Chāndogya | 627 |
| `danda_sep` | `॥ N। M। K॥` | `॥ १। १। ६॥` | Taittirīya Saṃhitā | 2,296 |
| `trailing` | `॥ N` (no close) | `॥ १५६७` | Sāmaveda Kauthuma | 1,876 |

**Three failures this taxonomy prevents, all measured on the real files:**

- `double` alone on the **Śukla Yajurveda** found **0 markers across all 40 adhyāyas**.
  An entire Veda would have converted to nothing, silently.
- `double` alone on the **Sāmaveda** found **6** markers in 157,404 Devanagari characters.
- `double` alone on the **Taittirīya Saṃhitā** found **2** in 1,351,568 characters.

### Grammar is detected PER UNIT, not per text

A source can be internally inconsistent, and the Rigveda is. **27 of its 1,027 sūktas end
verses with `॥१` (trailing) while the other 1,000 use `॥१॥`** — for example maṇḍala 1
sūktas 38, 39, 167 and 173. Detecting once per file and applying that grammar to every
unit in it made those 27 sūktas invisible.

Per-unit detection recovered **261 verses**, moving the Rigveda from 10,201 to **10,462**
against a canonical 10,552. The Atharvaveda is likewise mixed: 733 units `double`, 1
`single_pair`, 2 with no detectable grammar.

So a text showing two grammars in the converter's output is not necessarily a defect. It
may be an honest description of a source that changes convention partway through.

**Detection order is load-bearing.** `trailing` is a prefix of `double`, so testing it
first matches the opening daṇḍa of every `॥ N॥` and mis-classifies the whole corpus. It is
tested last, and `detect_grammar()` returns the match count alongside the name so a grammar
"winning" with 6 matches in a large text is distinguishable from a genuinely short one.

Implementation: `scripts/sanskrit-common/sanskrit_common.py` `MARKER_GRAMMARS` /
`detect_grammar()`. Pinned by 38 tests in `scripts/sanskrit-acquire/tests/`.

---

## Part 2 — Citation strength tiers

The converter gates differently per tier. This is the third authority tier alongside
`cross-source` and `contiguity` (see `DECISIONS.md` 2026-08-23).

| Tier | Meaning | Converter behaviour |
|---|---|---|
| **firm** | Cited figure, and our parse matches it | Hard gate. A mismatch BLOCKS the text |
| **range** | Published sources disagree; a range is recorded | Gate on range membership, not a point value |
| **unit-mismatch** | The cited figure counts a different unit than we parse | No count gate. Contiguity only |
| **uncitable** | No published count found | No count gate. Contiguity only |
| **excluded** | Text has no conventional verse numbering | Not converted at all |

---

## Part 3 — Upaniṣads

| Text | Ours | Cited | Tier | Source | Note |
|---|---:|---:|---|---|---|
| Īśa | **18** | 18 | firm | Radhakrishnan/Deussen via WP | Kāṇva=18, Mādhyandina=17. Ours is Kāṇva |
| Kena | **35** | 35 | firm | Deussen pp.207–213 | |
| Māṇḍūkya | **12** | 12 | firm | Deussen vol.2 pp.605–637 | |
| Śvetāśvatara | **113** | 113 | firm | Hume 1921 pp.394–411 | 110 main + 3 epilogue |
| Kaivalya | **24** | 24 | firm | Deussen pp.791–795; Aiyar pp.31–32 | Atharva recension; a KYV recension has 26 |
| Brahmabindu | **22** | 22 | firm | Ayyangar 1938 pp.17–22 | Adyar recension; Deussen's has 38 |
| Yogatattva | **142** | 142 | firm | Ayyangar 1938 pp.301–325 | Long/Telugu recension; short one has 15 |
| Chāndogya | **627** | 627–628 | range | 154-khaṇḍa structure cited; totals are not | In range |
| Kaṭha | **120** | 118 / 119 / 121 | range | WP sum=118; 119 widely repeated; 121 with disputed 2.6.16–18 | **Ours matches none of the three** |
| Aitareya | **33** | 33 | range | WP, no named edition | Corroborated, weakly sourced |
| Praśna | **67** | 67 | range | WP + WisdomLib; praśnas 3–6 uncorroborated | |
| Tejobindu | **466** | 465 | range | Ayyangar 1938 pp.27–87 | +1. Long recension confirmed (short has 14) |
| Amṛtanāda | **39** | 38 | range | Deussen pp.691–698 | +1, **and the text's identity vs Amṛtabindu is unsettled** |
| Muṇḍaka | **67** | 64 | **DISAGREE** | Müller, *SBE* / Dover 1962 | **+3, unexplained — see below** |
| Kauśītaki | **53** | 50 | **DISAGREE** | Deussen/Hume/Müller/Cowell via WP | **+3, unexplained — see below** |
| Ātmabodha | **31** | 18 | **defect** | WP infobox, weakly cited | 31 markers, **30 distinct, duplicate `१`** — two numbered sequences in one file |
| Sarvasāra | **5** | 23 | unit-mismatch | Deussen pp.657–661; Aiyar pp.13–17 | Source numbers 5 sections; the citation counts 23 Q&A pairs |
| Jābāla | **6** | 6 khaṇḍas / 14 mantras | unit-mismatch | Deussen, Bedekar & Palsule pp.757–761 | Source numbers 6 khaṇḍas; the citation counts mantras within them |
| Subāla | **15** | 16 khaṇḍas | unit-mismatch | Aiyar pp.61–77 | Section count, off by one. Mantra total uncitable |
| Taittirīya Up. | **51** | 31 anuvākas | unit-mismatch | Deussen vol.1 pp.217–246 | 31 is anuvākas; ours is verses within them |
| Bṛhadāraṇyaka | **437** | — | uncitable | Only per-brāhmaṇa structure cited | Kāṇva vs Mādhyandina differ substantially |
| Maitri | **99** | — | uncitable | Hume 1921 pp.412–458 | Manuscripts "vary considerably" |
| Mahānārāyaṇa | **263** | — | uncitable | — | Recensions give 64/80/84/25 **chapters**, never a mantra total |
| Paiṅgala | **29** | — | uncitable | Deussen pp.915–916 | 4 chapters attested, no verse total |
| **Nirvāṇa** | **0** | 82 / 61 / 62 sūtras | **excluded** | Olivelle 1992 pp.227–235 | Prose aphorisms, no verse numbering. Correctly not converted |

### The +3 discrepancies, and a hypothesis that failed

Muṇḍaka and Kauśītaki are each **exactly +3** over their cited figures. The obvious
explanation is śānti-pāṭha (peace invocations) being counted as verses.

**I tested it and it is wrong.** Scanning our parsed verses for invocation formulae
(`शान्तिः शान्तिः`, `सह नाववतु`, `पूर्णमदः`, `भद्रं कर्णेभिः`, `आप्यायन्तु`):

```
mundaka      ours= 67  cited= 64  diff=+3   shanti-bearing verses: 1
kaushitaki   ours= 53  cited= 50  diff=+3   shanti-bearing verses: 0
katha        ours=120  cited=118  diff=+2   shanti-bearing verses: 2
isha         ours= 18  cited= 18  diff= 0   shanti-bearing verses: 1
```

Kauśītaki has **zero** invocation-bearing verses and is still +3. Īśa has one and is
exactly right. So the invocation count does not correlate with the discrepancy at all.

### SOLVED 2026-08-24: colophons were being counted as verses

The śānti-pāṭha hypothesis was wrong, but the cause turned out to be structural and
visible in the marker sequence. Muṇḍaka's runs:

```
[1, 1, 2 … 13, →2←, 1, 2 … 11, →3←, 1, 2 … 11]
  ↑ site chrome    ↑ colophon       ↑ colophon
```

Index 0 is navigation text (`Home upanishhat ITX Devanagari PDF…`) terminated by a marker.
The arrowed entries are **colophons**:
`॥ इति मुण्डकोपनिषदि प्रथममुण्डके द्वितीयः खण्डः ॥ २॥` — where the trailing number is the
*muṇḍaka's* number, not a verse's. Those three phantoms are the whole of the +3, and they
also produced 3 spurious chapter splits.

**The fix took three attempts, and the two failures are worth recording:**

1. *Discard any segment starting with a colophon* — wrong. A segment is
   `[previous colophon][heading][verse]`, so discarding it threw away the real verse
   behind it. Kena dropped 35 → 32, breaking a text that had been exactly right.
2. *Strip colophons terminated by `॥` **or end-of-segment*** — wrong. `इति…$` also matches
   real verses that legitimately open with इति. Chāndogya lost one (627 → 626) and
   Tejobindu five (466 → 461).
3. *Strip `॥`-terminated colophons, and separately discard a segment that opens with इति
   **and names a section*** (`खण्डः`, `अध्यायः`, `वल्ली`, `प्रपाठकः`, `ब्राह्मणम्`…) —
   correct. Structural rather than length-based, because a colophon and a verse opening
   with इति are otherwise identical.

Result: Tejobindu, Paiṅgala, Chāndogya and Kena all back to correct; Muṇḍaka 67 → 65
against a cited 64. **Kauśītaki's colophons do not use those section nouns and it remains
at 53 against a cited 50.** Both still block, but the cause is now known rather than
mysterious.

---

## Part 4 — Saṃhitās

| Saṃhitā | Ours | Cited | Tier | Source |
|---|---:|---:|---|---|
| Rigveda, sūktas | — | **1,028** | firm | Aufrecht 1877, per-maṇḍala table below |
| Rigveda, ṛcs | 10,462 | 10,552 | range | Aufrecht; some sources round to ~10,600 |
| Śukla YV | 1,965 | 1,951 *or* 1,975 | range | Unresolved; likely kaṇḍikās vs verses |
| Atharvaveda | 6,088 | 5,977 / 5,987 / 6,015 / ~6,000 | range | No edition-cited figure found |
| Sāmaveda | 1,876 | **1,875** | firm | Pūrvārcika 650 + Uttarārcika 1,225 |
| Taittirīya Saṃhitā | 2,296 | 2,197–2,198 | range | 7 kāṇḍas / 44 praśnas / 651 anuvākas |

### Rigveda per-maṇḍala sūktas — confirmed

`191, 43, 62, 58, 87, 75, 104, 103, 114, 191` = **1,028**. Independently confirmed against
Aufrecht-derived sources. A competing table giving maṇḍala 8=92 and 9=144 **fails its own
sum check** (1,047) and is discarded as internally inconsistent, not treated as a variant.

Our parse has **1,027**, missing **maṇḍala 8 sūkta 66** — a single gap in an otherwise
contiguous 1..103. Wikisource holds that sūkta; see the deferred TODO.

### Taittirīya Saṃhitā per-kāṇḍa

| Kāṇḍa | 1 | 2 | 3 | 4 | 5 | 6 | 7 | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Praśnas | 8 | 6 | 5 | 7 | 7 | 6 | 5 | 44 |
| Anuvākas | 146 | 75 | 55 | 82 | 120 | 66 | 107 | 651 |
| Verses | 342 | 384 | 206 | 279 | 402–403 | 333 | 251 | 2,197–2,198 |

A competing figure of 82 praśnas / 1,235 anuvākas / 4,593 mantras is roughly double and
probably folds in the Brāhmaṇa and Āraṇyaka. Unresolved; the 44/651/2,198 table is
internally consistent and preferred.

### Per-chapter tables that could NOT be sourced

Stated explicitly so nobody assumes they were checked:

- **Śukla YV per-adhyāya (1–40)** — the one most needed, since a recalled table was wrong
  before (adhyāya 1 given as 22; the text has 31). Needs Weber 1849 directly.
- **Rigveda per-maṇḍala ṛc counts** — only sūkta counts are web-sourceable.
- **Atharvaveda per-kāṇḍa** — needs Whitney's HOS 7–8 introduction table.
- **Sāmaveda Uttarārcika per-prapāṭhaka.**

---

## Part 5 — The rules the converter applies

1. **Detect the marker grammar per source.** Never assume `double`. If no grammar matches,
   the text is unparsed, not empty.
2. **Gate by tier.** `firm` blocks on any mismatch. `range` blocks only outside the range.
   `unit-mismatch` and `uncitable` fall through to contiguity. `excluded` is not converted.
3. **Contiguity always applies**, whatever the tier: numbers must run `1..max` with no
   gaps. Its blind spot is a dropped final verse, which stays contiguous.
4. **A blocked text is a good outcome.** Nothing is invented to satisfy a threshold.
5. **Record which tier authorised each text** in its `structure.count_authority`, so
   coverage is never overstated by a number that was never really checked.

### What blocks, and a mislabelling corrected

**Three of the five "parser defects" I first recorded were not defects.** They were filed
on the research summary's framing, before I opened the source files. Reading them showed:

- **Jābāla** — the source carries exactly 6 numbered markers. It numbers *khaṇḍas*; the
  cited 14 counts mantras inside them. Our parse of 6 is faithful to the source.
- **Sarvasāra** — exactly 5 numbered markers. The cited 23 counts question/answer pairs,
  which this edition does not number. Our parse of 5 is faithful.

Both are `unit_mismatch`, not defects. **Labelling a correct parse a defect is how a gate
stops being believed**, so the classification was corrected rather than left conservative.

Genuinely blocking:

| Text | Reason |
|---|---|
| Ātmabodha | 31 markers, 30 distinct, **duplicate `१`** — a prose section ending at marker 1, then a fresh verse run 1..30. Needs splitting into two chapters; a duplicate key is dropped **silently** at ingest (G8) |
| Muṇḍaka, Kauśītaki | +3 each, cause unknown, śānti-pāṭha hypothesis tested and disproved |
| Sāmaveda | 1,876 against a firm 1,875 |
| Nirvāṇa | Excluded: prose aphorisms, no verse numbering |

The mechanism is working: real problems surface before anything is written, and the ones
that turned out not to be problems were reclassified rather than left to erode trust in
the gate.


---

## Part 6 — Saṃhitā verse numbering, and two hypotheses that failed

13 of the Rigveda's 1,027 sūktas carry duplicate marker values, which blocks them on the
key-distinctness check. Two structural explanations were tested and **both are wrong**;
recording them so the next person does not re-derive them.

**Rejected 1: "the printed values interleave pada numbers with verse numbers, so keep the
contiguous 1..N sub-sequence."** This came from inspecting RV 1.65, where the markers read
`१,१,३,२,५,३,७,४,९,५` — apparently padas 1,3,5,7,9 interleaved with verses 1,2,3,4,5.
Tested against all 13, the rule recovers the canonical count for **1 of 13**. RV 1.164
yields 34 where it should yield 52; 1.68, 1.69, 1.70 and 9.109 collapse to a run of 1.

**Rejected 2: "the metre metadata identifies them."** RV 1.65 declares `द्विपदा विराट्`,
which would explain half-verse marking. But **22 sūktas declare द्विपदा and only 5 have
duplicate markers**, while **8 duplicate-marker sūktas do not declare it**. Neither
necessary nor sufficient.

**What the data actually shows.** In every case with a checkable figure except one, the
marker COUNT equals the canonical verse count and only the printed VALUES are garbled:

| Sūkta | Markers | Canonical verses |
|---|---:|---:|
| 1.68 | 10 | 10 |
| 1.69 | 10 | 10 |
| 1.70 | 11 | 11 |
| 1.164 | 52 | 52 |
| 1.191 | 16 | 16 |
| **1.65** | **10** | **5** |

RV 1.68 prints `1, 12, 3, 24, 5, 3, 7, 4, 9, 5` for ten verses — the positions are right,
the numbers are not. So a unit whose marker values contain duplicates is **renumbered
1..N by position**.

**The risk this accepts, stated plainly:** if a marker is genuinely MISSING from the
source, renumbering hides it behind a clean run and contiguity can no longer detect it.
That is why it runs only where the values are already known-bad.

**RV 1.65 is a named exception, not a rule**, because no structural signal separates it:
its marker count is twice its verse count, and every other duplicate-marker sūkta with a
checkable figure has a count equal to its verse count. It blocks rather than silently
converting to ten verses.

### Saṃhitā status

| Saṃhitā | Verses | Status |
|---|---:|---|
| Rigveda Śākala | 10,450 | converted; 1.65 blocked, ~90 short of the cited 10,552 |
| Atharvaveda Śaunaka | 6,088 | converted; 8 units renumbered positionally |
| Śukla YV Vājasaneyi | 1,965 | converted; 2 units renumbered positionally |
| Sāmaveda Kauthuma | 1,866 | converted, with 8 gaps recorded in `structure.known_gaps` |
| Taittirīya Saṃhitā | 2,294 | converted; kāṇḍa is the chapter, anuvāka labels get a positional suffix |

### Sāmaveda: a source with real holes, and a regex bug that hid them

Two separate problems, only one of them ours.

**Ours: `trailing` matched a PREFIX of a longer number.** `॥ ११४ ॥` matched as `११` —
the greedy numeral run took `११४`, the "not followed by a daṇḍa" lookahead failed, and the
engine backtracked to `११`, where the next character is `४` and the lookahead passes. That
silently invented markers. Fixed with `(?![०-९])`, which forbids backtracking into the
numeral. It applied wherever `trailing` is used, including 27 Rigveda sūktas.

**Also ours: ārcika positional indices read as markers.** The Sāmaveda interleaves
`॥ ४ ९ ३ ०९०३e` positional references. Since `trailing` numbering is a single running
count, a marker that goes backwards cannot be one; dropping non-increasing values removed
exactly 4 (`११८०, ११८१, १२१, ४`) and left zero duplicate keys.

**Not ours: the source is incomplete.** After both fixes it carries **1,866 verses,
running to 1,874 with gaps at 114, 466, 585, 640, 650, 1179, 1180, 1211 and no 1875** —
nine short of the canonical total. Those are absent from the source. They are enumerated
in `structure.known_gaps` so the corpus states the hole instead of hiding it, and the
tier moved from `firm 1875` to `range 1866–1875` to record the fact rather than to make a
number pass.

### Taittirīya: the marker IS the citation

`॥ १। १। ६॥` is kāṇḍa.prapāṭhaka.anuvāka. Treating the first component as the chapter
recovers **650 anuvākas, matching the researched per-kāṇḍa counts EXACTLY in 6 of 7
kāṇḍas** (kāṇḍa 1 gives 145 against 146, accounted for by two markers that lost a
component and read `१.२`).

Each label repeats **exactly 2 or exactly 4 times** (153 labels ×2, 497 ×4) because the
source runs each kāṇḍa through more than once. So the label alone is not unique and gets a
positional suffix, and verses are ordered by **citation rather than file position** — file
order runs 1.1.1 … 8.22.1 and then back to 1.1.2.


## The second witness earns its keep — 2026-08-24

The 2026-08-23 decision kept the Wikisource copies of the Rigveda and Atharvaveda
alongside the ODbL primary, on the argument that "two witnesses is the point, not
redundancy." This is what the second witness found. **Three requests, three findings, two
of them fixes the primary source could never have produced on its own.**

### RV 8.66 was not missing — it was MISLABELLED as 8.67

The primary source has 102 sūktas in maṇḍala 8, running 1..103 with 66 absent, which reads
as one dropped sūkta. It is not. Its record labelled `sukta: 67` opens
`१५ कलि: प्रागाथ: … १५ अनुष्टुप्` and `तरोभिर्वो विदद्वसुमिन्द्रं` — and Wikisource's
**8.66** carries byline `कलिः प्रागाथः`, note `१५ अनुष्टुप्`, and the same opening verse.
So the record was 8.66 wearing 8.67's number, and **the real 8.67 (21 verses, `मत्स्यः
साम्मदः`, devatā Ādityāḥ) was absent entirely.**

Fixed: the 15 verses were relabelled 66, and 8.67's 21 verses supplied from Wikisource
(oldid 299570). Maṇḍala 8 is now 103 sūktas with no gaps, 1,706 verses; the Rigveda is
**10,470**.

**Why a count check alone would never have caught this.** 102 present, max 103, exactly one
missing — contiguity flags a gap and stops. Every downstream number was self-consistent.
Only a witness carrying *bylines* could show that a present record was the wrong sūkta, and
that is an argument for keeping metadata, not only verse text.

### AV 20.3 was header-only, and Wikisource had exactly what the header promised

The primary carries `१-३ इरिम्बिठिः । इन्द्रः।` and **no verse text** — 26 characters, zero
markers. Wikisource supplied precisely the 3 verses that header declares (oldid 323600).
Exactly two of kāṇḍa 20's 143 records are header-only this way: 3 and 13.

### AV 20.13 stays BLOCKED, and the witness is why

`013` pages are unreliable in this text. Wikisource's `काण्डं २०/सूक्तम् ०१३` holds 7 real
verses opening `उदु ब्रह्माण्यैरत श्रवस्येन्द्रं` — which is **20.12 verse 1**. It is an
orphaned duplicate of 20.012, not the missing sūkta. Ingesting it would have put sūkta 12's
text under 13 and produced a corpus that passed every count check while being wrong.

`sanskrit_common.py`'s `REDIRECT` comment already recorded this shape for **kāṇḍa 8 sūktam
013** and said it "holds real wikitext and still needs a manual pass". Both instances are
`013`. Treat any `013` page in this text as suspect until compared with its neighbour.

So 20.13 is absent from both witnesses and is declared in `structure.known_gaps` with the
reason, rather than filled from the nearest plausible text. It needs a third witness —
Whitney/Griffith, or a printed Śaunaka edition.

### Licence consequence, stated rather than buried

24 verses in two otherwise-ODbL files are **CC BY-SA 4.0**. Both licences are share-alike,
but they are not the same licence, and the mix is now declared per-file in
`structure.secondary_sources` with the oldid of each page. **This needs a licensing call
before redistribution** — see `LICENSES.md`.


## Vedāṅga / Upaveda acquisition — source research, 2026-08-24

**Done before fetching anything, and it invalidated three assumptions in the plan.** Recorded
here rather than discovered mid-wave.

### 1 · GRETIL cannot be the primary source — it is transliteration, and unlicensed

The plan named GRETIL first. Measured across three files
(`sa_yAska-nirukta`, `sa_pANini-aSTAdhyAyI`, `sa_agniveza-carakasaMhitA-parts-comm`):
**zero Devanagari characters in each**, against 27,307 / 13,548 / 47,933 IAST diacritics.
They are romanised.

`LICENSES.md` already said both halves — *"GRETIL's Vedic files are frequently IAST Roman,
not Devanagari"* (§3) and *"Licence: not granted. Reference use only, terms inherited per
file."* **A file already in this repo refuted the plan step.** GRETIL stays useful as a
*witness for counts and structure*, never as corpus text.

**Corrected order: sanskritdocuments (Devanagari, permission-based) → Wikisource (CC BY-SA,
Devanagari) → GRETIL for cross-checking only.**

### 2 · Almost everything Devanagari-available on this axis belongs to Youvan

Searched sanskritdocuments' `doc_z_misc_major_works/` (232 documents) and `doc_veda/` (82):

| Text | Axis | Owner | Available |
|---|---|---|---|
| `pANinIyashikShA` | Vedāṅga Śikṣā | **Youvan** | yes, Devanagari |
| `natya01`–`natya37` | Upaveda Gāndharvaveda (Nāṭyaśāstra, 37 ch) | **Youvan** | yes, Devanagari |
| `aShTAdhyAyI` | Vedāṅga Vyākaraṇa | Vipin | yes — but **sūtra shape, blocked** |
| `dhanurveda` | **Upaveda Dhanurveda** | **Vipin** | **yes, Devanagari** |
| Nirukta, Caraka, Suśruta, Aṣṭāṅgahṛdaya, Mānasāra, Mayamata | — | Vipin | **absent** from both indexes |

So **Vipin's entire acquirable Wave 1 on this axis is one text.** The Āyurveda and
Sthāpatyaveda material is not on sanskritdocuments at all, and the GRETIL copies are
transliteration under no licence — the scale warning in the plan turns out to be moot for
now, because the texts are not obtainable in the required form from the established sources.

### 3 · `dhanurveda` — 227 verses, contiguous, and it exposed a sixth marker variant

`sanskritdocuments.org/doc_veda/dhanurveda.html`, encoded by Ravi Mahadevappa. 18,399
Devanagari characters, unaccented, one file.

The `double` grammar found **217 markers over a span of 227**, missing
`10, 20, 30, 40, 50, 128, 130, 181, 197, 203`. **The first five being exact multiples of ten
is a parser smell, not a source property**, and it was: every one of the ten is terminated
`॥ N ।` — opening double daṇḍa, closing **single**. Verse 10 reads `॥ १० ।`, not `॥ १०॥`.

Tolerating a single-daṇḍa close gives **227 markers · 227 distinct · max 227 · zero gaps ·
zero duplicates** — a perfectly contiguous 1..227.

**Tier: `contiguity`, not `firm`.** The count is derived and internally perfect, but **no
published canonical figure was found to check it against**, so it is not citable. Saying so
is the point; `uncitable` and `firm` are different claims.

**Also present and harmless: stray ASCII line numbers** (`1714`, `1715`, …) after each
marker — 217 of them, artefacts of the source edition's line numbering. `MARKER` matches
Devanagari numerals here, so they do not interfere, but a parser widened to ASCII digits
would ingest them as verse numbers.


## Caraka Saṃhitā — BLOCKED, and the count was the least of it (2026-08-24)

Wikisource's Caraka parses cleanly to **3,560 verses** and is **not ingestible**. The count
check said nothing: contiguity held, the grammars detected, the validator passed.

### What is actually in those pages

| Sthāna | Commentary markers | Structured citations | Adhyāyas covered | Canonical |
|---|---:|---:|---:|---:|
| Sūtra | **125** | 399 (`।। चसं-N,M.K ।।`) | 5 | 30 |
| Nidāna | 0 | 14 | 1 | 8 |
| Vimāna | **41** | 29 | 1 | 8 |
| Śārīra | 0 | 29 (dotted `॥५.१.१॥`) | 4 | 8 |
| Indriya · Kalpa · Siddhi | 0 | **0** | **0** | 12 each |
| Cikitsā | — | — | — | 30 — the page is a **REDIRECT** |

**Only 11 of the 78 non-Cikitsā adhyāyas carry a structured citation at all.**

### The finding that matters: the markers number the COMMENTARY

Sūtrasthāna opens `अथातो दीर्घंजीवितीयम् … ।। चसं-१,१.१ ।।` — the mūla, citing itself as
Caraka Saṃhitā 1, adhyāya 1, verse 1. Immediately after comes `; आयुर्वेददीपिका` and then
`।। १ ।।`, `।। २ ।।`, `।। ३ ।।` — **Cakrapāṇidatta's commentary, separately numbered.**

`detect_grammar` picked `single_pair` and found **1,191 markers** in Sūtrasthāna. Those are
overwhelmingly commentary verses. A naive ingest would have put the Āyurvedadīpikā into the
corpus **as Caraka**, under chapter numbers inferred from where the commentary happens to
restart.

The inferred structure was visibly wrong and that is what prompted looking: chapter counts
came out **125 for Sūtrasthāna against a canonical 30**, 196 for Śārīra against 8. Neither
"split on any decrease" nor "split on restart-at-1" recovers the real structure, because the
numbers being split on are not the text's.

### Why it is blocked rather than partially ingested

The citable subset is ~9% of the work, and it sits **interleaved with commentary in exactly
the sthānas that have it**. A corpus is a citation surface: someone resolving
`caraka_samhita 1.5.3` would get *something*, and it might be Cakrapāṇidatta. That is the
Dharmaśāstra failure — a hierarchy flattened, the citation components destroyed, invisible
for months — and G7 is the rule against it.

Tier `defect`, which BLOCKS. Not `uncitable`, because the problem is not a missing figure:
**our parse is known wrong.**

### What would unblock it

A mūla-only edition, or a parser that keys on `।। चसं-N,M.K ।।` and the dotted `॥N.M.K॥`
form and **discards everything not carrying one**. That is real work and it recovers 11
adhyāyas; the rest of the text is simply not on Wikisource.


## The bare-numbered Wikisource texts all block on CHAPTER structure (2026-08-24)

Three candidates, three blocks, one shared cause. **None was written; the validator stopped
each before it reached the corpus.**

| Text | Verses parsed | Structural signal | Why it blocks |
|---|---:|---|---|
| Caraka Saṃhitā | 3,560 | — | markers number the **commentary**; 125 chapters inferred against a canonical 30 |
| Mayamata | 2,666 | 6 of 7 pages pass the bare gate | pages declaring 5 adhyāyas parse to 6, so page `०६-१०` collides with page `११-१५` — **82 duplicate keys** |
| Mānasāra | 5,167 | **100%** in ascending runs, 68 chunks vs canonical 70 | numbering repeats **without returning to 1**, so restart-at-1 cannot separate the chapters — **138 duplicate keys** |

**The verse-level parse is fine in all three.** What fails is the level above it. Mānasāra
is the clearest case: the strongest structural signal of any candidate — every numeral
inside an ascending run, 68 chunks against a canonical 70 — and it still produces 138
duplicate keys, because a chapter boundary is not always a return to 1.

**Why this matters more than a count.** `seed_texts.py` drops duplicate keys **silently**
(G8), so an ingest would have lost ~2.7% of Mānasāra's verses between the corpus and the
API, with no error anywhere. The count would still have read 5,167.

### What the bare grammar did and did not buy

It works: it finds the verses, and `bare_structure_ok` correctly separates real verse
numbering from incidental numerals. **It does not recover chapter boundaries**, and on these
transcriptions nothing available does — the pages carry no headings (Mānasāra has none for
68 adhyāyas), and Wikisource's own declared ranges disagree with the parse on 2 of 7
Mayamata pages.

### What would unblock them

An edition with explicit adhyāya headings, or per-verse citations of the kind Caraka's mūla
carries (`।। चसं-१,१.१ ।।`) and Śārīrasthāna's dotted `॥५.१.१॥`. Inferring the hierarchy from
verse numbers alone is what destroyed the Dharmaśāstra data, and G7 is the rule against
repeating it.


## The source stated its own structure all along (2026-08-24)

**Mānasāra and Mayamata carry explicit adhyāya headings, and I nearly deleted them.**

The first pass removed `==` headings as page furniture, because `strip_code` keeps their
words and the page title was leaking into verse 1. Removing them also destroyed the only
reliable statement of where chapters begin — and the number-inferred boundaries that
replaced them were subtly wrong: Mānasāra chapters 7, 11, 15 and 40 came out starting at
**verse 2**, their verse 1 absorbed into the chapter before.

| Text | Headings | Result |
|---|---:|---|
| **Mānasāra** | **71**, named (`वास्तुप्रकरणम्`, `विमानलक्षणम्`) | 70 carry verses — the 71st, `सन्दर्भः`, is a reference list. **70 chapters = canonical 70, 5,169 verses, 0 duplicates** |
| **Mayamata** | 5 or 6 per page, numbered (`अथ द्वितीयोऽध्यायः`) | matches the page's declared adhyāya range on **6 of 7** pages; the 7th's extra is `अथ कत्नपारम्भः`, an appendix. **36 chapters = canonical 36** |
| Caraka | 5 in Sūtrasthāna for 30 adhyāyas, 1 in Vimāna, 0 elsewhere | too sparse to help; blocked on the commentary problem regardless |

**This is the third time in one session that inferring structure from verse numbers was the
wrong instrument while the source stated it plainly.** The others were Caraka (`।। चसं-१,१.१ ।।`
mūla citations, ignored in favour of counting commentary markers) and Taittirīya (the marker
*is* the citation).

### Mayamata: structure solved, blocked on transcription quality

With headings, its 36 chapters are right and **22 of them are clean**. What blocks is the
source: **69 duplicate verse numbers across 14 chapters**, 37 of them in chapter 25 alone.
`seed_texts.py` drops duplicate keys silently (G8), so ingesting would lose 69 verses
invisibly.

Three are uniquely-determined typos — chapter 7's verse 42 is transcribed `1`, sitting
between 41 and 43, so its correct value is pinned by its neighbours. The remaining 66 need
checking against a printed edition. **That is the whole remaining task: 69 verses, each at a
known position** — not 21 chapters of boundary work, which is what it looked like before the
headings were used.


## Suśruta — blocked on a structural decision, not on data (2026-08-24)

The best-conditioned candidate of the four, and it still does not land.

**What is good:** mūla-only — **zero** Nibandhasaṅgraha/Ḍalhaṇa hits across 17 pages, unlike
Caraka. 100% of numerals inside ascending runs on every page that parses. Nidāna (16),
Śārīra (10) and Kalpa (8) recover their canonical adhyāya counts exactly, and two pages
carry headings that match exactly (Uttaratantra 41–66 with 26; Śārīra with 10).

**What blocks it is a shape this converter has not had to decide before.** Suśruta's pages
**mix two forms**:

| Page form | Example | Yields |
|---|---|---|
| whole sthāna | `सुश्रुतसंहिता/कल्पस्थानम्` | chapter = sthāna, adhyāya as a **sub-level** |
| adhyāya range | `सुश्रुतसंहिता/उत्तरतन्त्रम्/अध्याय ०१-२०` | chapter = **adhyāya**, no sub-level |

Both are correct readings of their own page. Together they give **inconsistent citation
depth inside one text**, which the validator reported 3,522 times as *"number 1 has 1
component(s), structure.levels implies 2"*. That is my design, not the source's fault.

**It needs a per-text sthāna → adhyāya normalisation** — every page mapped into
sthāna.adhyāya.verse regardless of which form its title takes — before it can be ingested.
Canonically that is Sūtra 46 · Nidāna 16 · Śārīra 10 · Cikitsā 40 · Kalpa 8 · Uttaratantra
66 = **186 adhyāyas**.

**Two smaller things to handle in the same pass:** four pages miss their declared range by
one (Uttaratantra 1–20 parses 21; Cikitsā 35–40 parses 5 for 6), and three near-empty stub
pages carry ranges that **overlap** real pages — `चिकित्सास्थानम्/अध्याय २१-४०` at 49
characters against the real 21–25, 26–30, 31–35 and 35–40.


### Suśruta, second pass: the depth problem is fixed (3,522 errors → 6)

A **per-text sthāna map** replaced the per-page decision. Every page is now normalised to
`sthāna.adhyāya.verse` regardless of whether its title names a whole sthāna
(`सुश्रुतसंहिता/कल्पस्थानम्`) or an adhyāya range (`उत्तरतन्त्रम्/अध्याय ०१-२०`). Caraka and
Suśruta each get their own order — they do not share one; Caraka has Vimāna/Indriya/Siddhi
where Suśruta has Uttaratantra.

**Two things remain, and one of them is not our bug.**

**The page titles are sometimes wrong.** `चिकित्सास्थानम्/अध्याय ३५-४०` carries the text's own
colophons for adhyāyas **36..40**, and the preceding page ends
`इति सुश्रुतसंहितायां चिकित्सास्थाने … पञ्चत्रिंशोऽध्यायः ३५`. So that page is really 36–40 —
5 adhyāyas, exactly what the parse found — and the declared-range bound was rejecting a
**correct** parse on the strength of a mislabelled Wikisource title. Three other pages fail
the bound and need the same check.

**And 6 duplicate verse keys remain** (e.g. Śārīra 8.8), the same class as Mayamata's 69.

### The fourth instance: colophons

Suśruta carries **101 explicit `इति सुश्रुतसंहितायां … ऽध्यायः N` colophons**, naming each
adhyāya in words *and* digits. They are incomplete — none at all in Uttaratantra — so they
cannot be the sole structure source, but **where present they are authoritative**, and they
are what proved the `३५-४०` mislabel.

That makes four texts in one session where the source stated its structure and inference was
the wrong instrument: Caraka's `।। चसं-१,१.१ ।।` mūla citations, Taittirīya's marker-as-citation,
Mānasāra and Mayamata's headings, and now Suśruta's colophons. **Look for the statement
before inferring.**

Only 4,296 of 8,338 verses parse today, so ingesting now would leave Sūtrasthāna absent.
The next pass should trust colophons over page titles.


## Mayamata lands — and 68 of its 69 "duplicates" were my parser (2026-08-24)

**36 chapters = canonical 36, 3,351 verses, zero duplicate keys.**

The earlier record here said Mayamata needed *"69 verses checked against a printed
edition"*. That was wrong, and the correction came from a parallel review that was asked to
report a disagreement rather than resolve it.

**The `bare` grammar was eating a hyphen.** The source writes 68 of its markers as
sub-numbers — `41-2<br>`, `42-1<br>` — and the pattern's leading `[^\d०-९]` matched the
hyphen, so the capture took only the digits *after* it. `42-1` parsed as `1`, `41-2` as `2`,
and the prefix was left inside the verse body. That manufactured 68 of the 69 duplicates.

**It also invented a transcription typo that never existed.** This document previously
recorded *"chapter 7's verse 42 is transcribed `1`"*. The raw marker is `42-1`. The 42 was
never lost; the parser dropped it.

Independent confirmation: `grep -ohE '[0-9०-९] *- *[0-9०-९]'` finds **68** hyphenated markers
across the 7 pages, distributed 1 / 40 / 12 / 15 — and **zero** on the three pages that
already parsed clean. Widening the capture changes the marker count on **zero** pages, so
the verse segmentation is untouched and only the key differs.

**The sub-numbers are real, not noise.** For 31 of the 68, the plain `41` *also* exists in
the same chapter — the source is saying "verse 41, part 2". Stripping the suffix would
collide them and lose a verse silently (G8), so the whole marker is kept as a string key,
exactly as `MinarajaYavanajataka`'s `"24अ"` and `Jatakaparijatah`'s `"N 1/2"` already are.

**Chapter 25's 37 duplicates had one cause, not 37.** Two contiguous runs of `N-2` markers
(16 and 21), each coinciding with a metre change from two-line anuṣṭubh to long four-line
stanzas. The transcriber suffixed `-2` through a metre-shifted passage.

**One genuine defect remained**, and only one: adhyāya 21 runs `1..9, 20, 11..19, 20` with
`10` absent. Neighbours pin it. It is fixed through `SOURCE_CORRECTIONS` in `convert.py` —
a version-controlled table with the reason, **not** an edit to the gitignored source file,
which would be unreviewable and reverted by `--refetch`.


## Aṣṭāṅgahṛdaya from SARIT — the first source that stated everything (2026-08-24)

**6 sthānas · 7,443 verses · 0 duplicate keys · 798,682 Devanagari characters · 0 residual
IAST.**

SARIT's TEI carries `<div type="part">` × **6** and `<div type="chapter">` × **120**,
distributed **30 · 6 · 16 · 22 · 6 · 40** — precisely the canonical Sūtra/Śārīra/Nidāna/
Cikitsā/Kalpasiddhi/Uttara division. **Nothing was inferred.** Every other Upaveda text in
this corpus had to have its structure guessed from verse numbers, and the guessing is what
blocked Caraka, Mayamata and Suśruta in turn.

Each `<l>` also carries its own citation — `Ah.1.1.001a` is sthāna.adhyāya.verse.pāda — so
the `a` and `c` pādas of one verse rejoin into one verse rather than becoming two.

**Transliteration.** IAST → Devanagari, verified by round-tripping SARIT's own text before
trusting it: Caraka 17,086/17,090 and Suśruta 6,188/6,191 return byte-identical, and every
failure is a citation label or a stray capital in the source. The `ṁ` → `ṃ` normalisation is
required, not cosmetic.

### One thing preserved deliberately, and flagged

**46,227 hyphens across 98% of verses.** SARIT marks compound boundaries in IAST
(`rāgādi-rogān`) and they transliterate through as `रागादि-रोगान्`. Devanagari orthography
does not use them, and no other text in this corpus does at this rate — the next highest is
`minaraja_yavana_jataka` with 411 in total.

They are **editorial apparatus, not the mūla as printed**. They are kept unedited for now
because stripping is trivial and reversible while un-stripping is not, and because removing
46,227 characters from a text is an edit that should be a decision rather than a side
effect. **Open: strip on ingest, or keep as SARIT's compound analysis.**


## Caraka and Suśruta land from SARIT — and the first parse was half a text (2026-08-24)

| Text | Sthānas | Adhyāyas | Units |
|---|---|---|---:|
| Carakasaṃhitā | **8 / 8** | **120 / 120** | 9,131 |
| Suśrutasaṃhitā | **6 / 6** | **186 / 186** | 8,298 |
| Aṣṭāṅgahṛdaya | 6 / 6 | 120 / 120 | 7,443 |

All three: zero duplicate keys, zero residual IAST, structure taken from the TEI rather
than inferred.

**The first parse looked fine and was less than half the text.** Reading only `<l>` gave
Caraka 119 of 120 adhyāyas and Suśruta **79 of 186** — counts that were internally
consistent, validated cleanly, and dropped most of the work. Measured properly: only **46%**
of Caraka's text and **22%** of Suśruta's sits in `<l>`. They are mixed verse-and-prose
śāstra; the prose lives in `<p>` (Caraka, 2,474 blocks) and `<ab>` (Suśruta, 6,822), and it
carries its citation at the END — `… // Su.1.1.18` — where verse carries it at the start.

**Aṣṭāṅgahṛdaya was unaffected and that is why it was worth checking rather than assuming.**
Only 7,194 characters sit outside its `<l>` elements, and they are the TEI header, chapter
headings and page breaks. It is verse throughout.

**A second defect the counts also could not see: XML entities were never decoded.**
`&#x2020;` — a critical-apparatus dagger — survived tag-stripping, and the transliterator
then rendered its *digits* in Devanagari, producing `&#x२०२०;` **1,413 times** in Suśruta.
Decoding entities before transliteration fixes it; the 1,413 daggers are now the character
they always were.

**Two pieces of editorial apparatus are preserved and flagged, not silently removed:**
Suśruta's 1,413 daggers, and Aṣṭāṅgahṛdaya's 46,227 compound hyphens. Both are the
editions' apparatus rather than the mūla as printed. Stripping either is trivial and
reversible; un-stripping is not.

## Manusmṛti from SARIT — 11 of 12 chapters exact, and a citation form that hid 801 verses (2026-08-24)

**Tier `range`: 2,680–2,700. Parsed 2,684 across 12 adhyāyas, zero duplicate keys.**

`manu_smriti` was the last of the three off-schema Dharmaśāstra texts. It was not repaired —
it was replaced, from SARIT's `manusmrti.xml` (CC BY-SA 3.0, with a Kyoto Joint Seminar
copyright attribution). The 12 legacy `MS_*.json` files were deleted in the same change.

### Verified before acquiring, not after

- **12 `<div type="chapter">`** in the TEI, matching the canonical 12 adhyāyas.
- **Mūla-only.** 391 of 394 commentary hits (Medhātithi, Kullūka) sit inside `<note>`
  variant-reading apparatus; stripping notes leaves 3. This is the check G18 exists to
  force — Wikisource's Caraka failed exactly here.
- **Licence** is SARIT's CC BY-SA 3.0.

### Per-chapter agreement with Bühler

| adhyāya | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| parsed | 119 | 249 | 286 | 260 | 169 | 97 | 226 | 420 | 336 | 131 | **265** | 126 |
| Bühler | 119 | 249 | 286 | 260 | 169 | 97 | 226 | 420 | 336 | 131 | **266** | 126 |

**Eleven of twelve are exact.** Adhyāya 11 is contiguous 1–265 with no gap, no duplicate,
and no merged verse — its verses carry the same pāda shape as adhyāya 10, which matches
canon exactly.

**Stated as a limit rather than resolved** ([`GOTCHAS.md`](../../propagation/state/sanskrit-texts/GOTCHAS.md) G12): this rules out a dropped
verse leaving a hole and a mislabelled number producing one. It does **not** distinguish
"this edition numbers 265" from "one verse is absent and everything after was renumbered."
Contiguity cannot see the second. Settling it needs a verse-by-verse comparison against
Bühler that has not been done — which is why the tier is `range` and not `firm`.

### The defect: 1,602 lines that parsed cleanly into the wrong verses

First parse gave **1,887 verses against 2,688 `<lg>` in the same file.** Cause:
SARIT's Manusmṛti writes a cross-reference to a second edition's numbering immediately
after the citation with no separating space —

```
3.67a[57Ma] vaivāhike 'gnau kurvīta gṛhyaṃ karma yathāvidhi |
[M7.87Ma] deśa.kālavidhānena dravyaṃ śraddhāsamanvitam |      ← 8 lines: bracket is the ONLY citation
```

— and `SARIT_CITE` required whitespace directly after the citation. 1,602 of 5,376 lines
failed to match and fell through to the `order[-1]` continuation branch, which appended each
as tail text to the preceding verse. `1,594/2 + 8/2 = 801`, and `1,887 + 801 = 2,688`: the
gap is exactly those lines.

**Nothing errored, nothing was lost, and every verse was well-formed.** The chapter count
was already correct at 12 of 12. Only the verse total against the file's own `<lg>` count
could see it. Recorded as **G23**, whose trigger fires on the three call-site forms.

The fix consumes the bracket *inside* the citation match, so no separate stripping pass is
needed and brackets that are genuinely text are untouched. It is `sarit_cite()`, which
handles all four observed forms and returns `(citation, index where text begins)`.

### Regression, because the same regex serves four texts

Widening it left Caraka at **9,256**, Suśruta at **8,295** and Aṣṭāṅgahṛdaya at **7,443** —
byte-identical to their pre-change values — and all 36 other converting targets unchanged.
`nirvana_upanishad` still blocks at 0, which is its deliberate exclusion (prose aphorisms,
no verse numbering), identical before and after.

### What it settled about the re-digitisation plan

Two sessions were spent characterising *how* Manusmṛti's numbering was damaged, including a
careful 2026-08-23 correction about which citation component cycled. All of it was accurate;
none of it was used. **Look for a clean source before characterising damaged data.** SARIT
was already surveyed in `SOURCES.md` and already held this text while the plan to repair it
by hand was being written.

That route is **not** available for the two remaining Āpastamba texts: SARIT's 85 XML files
contain no Āpastamba (checked 2026-08-24). For those, the source hunt has to run first.

## Bhela Saṃhitā from SARIT — and the numbering bug it exposed in four earlier texts (2026-08-24)

**Tier `uncitable`. 8 sthānas · 98 adhyāyas · 2,813 verses · 0 duplicate keys.**
The TEI declares the structure itself — 24/7/5/7/12/28/8/7 — and the parse matches exactly.

**It is incomplete by transmission, not by digitisation.** Bhela survives in a single
damaged Tanjore manuscript. 98 adhyāyas is what is *extant*; do not read the shortfall
against Caraka's 120 as a gap to fill, and do not cite a total for the whole work.

### The finding: chapter numbers were positional, and that is wrong here

`parse_sarit` numbered chapters by their **position** among the div siblings. **6 of Bhela's
8 sthānas are non-positional** — the sūtrasthāna begins at adhyāya **4** (1–3 are lost),
sthāna 3 skips 2, sthāna 7 skips 2, sthāna 8 skips 3. Positional numbering files adhyāya 4
as adhyāya 1 and silently breaks every citation in the text (G7).

**It would have validated perfectly** — 98 chapters, zero duplicates, contiguous 1..N per
sthāna, correct verse totals. Nothing in the corpus checks could have seen it. What exposed
it was a *residual-Latin* check pointing at a verse the parse called `1.3.11` while the
source called it `BS.1.6.11`.

**Every earlier SARIT text is per-sthāna contiguous**, so positional and declared numbering
agreed and the defect was invisible: Aṣṭāṅgahṛdaya 6×`part`/120×`chapter`, Caraka
8×`level1`/120×`level2`, Suśruta 6×`sthāna`/186×`adhyāyaḥ`, Manusmṛti 12×`chapter`. Correct
by luck, in four texts, for as long as the parser has existed.

Chapter numbers now come from the div's declared `n`, falling back to position only when
absent. **The full dry-run is unchanged across all 36 other targets**, which is what
confirms it is a no-op wherever the divs are contiguous.

### The citation form, and why it is opt-in

Bhela writes the citation with **no separator** — `1.4.3nimbaṃ nataṃ ...` — on 272 lines
that otherwise fall through to the `order[-1]` continuation branch and join the preceding
verse (G23, the second instance in one session).

**Enabling a zero-width separator globally is destructive in both directions**, measured:

| Change | Effect |
|---|---|
| Allow it on **prefixed** citations | Cuts compound forms mid-citation — `Ca.1.18.7.-1` → `Ca.1.18.7` with `.-1` left as verse text. Mis-split **480** Aṣṭāṅgahṛdaya, **131** Caraka, **8** Suśruta lines, one into an EMPTY verse. Showed in the totals as a harmless **+6 / +11 / +5** |
| Allow it on **bare** citations | Matches line-initial numerals in Caraka's and Suśruta's prose that are not citations. **Caraka 9,256 → 8,193; Suśruta 8,295 → 6,898** |

So it is a per-text opt-in, `SARIT_NO_SPACE_TEXTS`, exactly like `detect_grammar(allow_bare=)`.
**A looser rule that is right for one text and wrong for its siblings belongs behind an
opt-in, never in the default.** Both directions are pinned by tests and mutation-checked.

### Two defects in the source, neither invented away

- **`<label>5.1.0" cert="low</label>`** — the label content was generated by string-copying
  the element's *attributes*. It is legitimate element content, so no amount of correct XML
  handling removes it; left alone the `"` breaks the citation and `५.१.०" चेर्त्="लो` lands
  transliterated inside verse 1 (G22). Stripped by a rule narrow enough that it cannot fire
  on Sanskrit, which contains no ASCII double quotes.
- **`dhavaṃ palāśaw nyagrodhaw`** at 1.6.11 — a stray `w`, twice, in SARIT's transcription.
  **Preserved.** The correct reading is not known, and guessing one is how a corpus acquires
  errors that look like data (G7).

## Aṣṭāṅgasaṃgraha — and the schema decision it forced, which also fixed Caraka (2026-08-24)

> **RESOLVED the same day.** Rupali chose **mixed depth**: `structure.levels` now declares
> the MAXIMUM depth rather than a uniform one. Aṣṭāṅgasaṃgraha landed at **9,382** verses
> and Caraka's merged pādas were repaired, **9,256 → 9,525**. The section below is kept as
> written because the measurements are the argument for the decision.

**Tier `uncitable`. 9,382 verses.** The parse is: **6 sthānas × 150 adhyāyas**
matching the canonical 40/12/16/24/8/50, 9,382 verses, **zero duplicate keys, zero residual
IAST**, and **mūla-only by the header's own statement**, said twice — *"omitting the
commentary of Indu"*. Licence CC BY-SA 3.0 via SARIT.

### Three parser defects it exposed, all fixed and all no-ops elsewhere

1. **`sarit_levels` chose the outer division by RARITY.** Aṣṭāṅgasaṃgraha has `level2`×150,
   `level1`×6 and `level3`×1, so rarity picks **`level3` — a single subsection — as the
   outer division of a 150-adhyāya text**. Caraka has `level1`×8 *and* `level3`×8, a tie
   `min()` resolved by dict iteration order, so that text has been parsing correctly by
   luck. The real relationship is **containment**, not rarity, and it is now measured.
2. **The citation prefix was a hardcoded `Ca|Su|Ah`**, which matched **0 of Aṣṭāṅgasaṃgraha's
   22,671 lines**. Its six sthāna abbreviations are `AS.Sū` / `AS.Śā` / `AS.ni` / `AS.Ci` /
   `AS.Ka` / `AS.Utt`. Now a general short dotted-token prefix.
3. **`n` may be compound.** Aṣṭāṅgasaṃgraha writes `n="1.1"` (sthāna.adhyāya); Bhela writes
   `n="4"`. A digits-only pattern silently misses the compound form and falls back to
   position — correct for Aṣṭāṅgasaṃgraha only by accident (G24 again, one level down).

### What blocks it, and why it is not a parser question

The Kalpasthāna **Paribhāṣā** is a *third structural level* — `<div type="level3" n="5.8.1">`
— and its **119 verses cite `AS.Ka.Paribh.N`, a single numeric component** no pattern
matches. They fall through to the `order[-1]` continuation branch and glue onto Kalpa
adhyāya 8 verse 33: **12,159 characters against a corpus median of 87** (G23, third instance
this session).

Splitting them into their own unit **works** and produces depth-3 keys (`8.1.1`…`8.1.119`),
which `validate_corpus.py:236` rejects — `structure.levels` declares **one depth per text**
and the rest of Aṣṭāṅgasaṃgraha is depth 2. There is no depth-preserving encoding: `1.1-5`
fails `DOTTED` and all three of `HALF_SHLOKA` / `DEVANAGARI_SUFFIXED` / `SUB_NUMBERED`.

**So this is a corpus-wide key-schema choice, not a parsing bug** — astroacharya's `@source`
citations resolve against these keys. Left for Rupali.

### The same question is a LIVE DEFECT in committed Caraka

Caraka's 8 `level3` divs are the **pādas** of Cikitsāsthāna adhyāyas 1 and 2 (Rasāyana,
Vājīkaraṇa), cited `Ca.6.1.1.1` = sthāna.adhyāya.pāda.verse. With `comps[-1]` taking the
verse component, **pāda 1 verse 1 and pāda 2 verse 1 are the same key**, so the four pādas
merge. Measured in the **committed** file:

| key | length |
|---|---:|
| `6.1.81` (Rasāyana) | **11,211 chars** |
| `6.2.53` (Vājīkaraṇa) | **6,264 chars** |
| median verse | **87 chars** |

Splitting them raises Caraka 9,256 → **9,525** with zero duplicates and keys `1.1`–`1.4`,
`2.1`–`2.4` — but lands on the identical depth-3 rejection. **Caraka is in the corpus today
with two adhyāyas' pādas merged**, and that is not fixable without the schema answer.


## Per-text caveats (moved out of `CLAUDE.md`, 2026-08-24)

These lived inline in [`CLAUDE.md`](../CLAUDE.md) and took that file 58 lines over its
180-line cap. A project `CLAUDE.md` is pointers and hard rules; per-text detail is this file.

**`bphs`** — one file since 2026-08-17 (was 11 chunks declaring 102 chapters for a 97-chapter
work). 4 mis-split chapters repaired, 5 shlokas recovered; ingests **3937 of 3937**.
Translation backlog closed 2026-08-22 — the last 5 (`12.11`, `53.20`, `61.55`, `66.43`,
`66.65`) are single-pāda fragments, a shape that occurs 13 other times in the text. **Ch 25
shloka 16 is absent from the digitisation and was not invented**; ch 60's parenthesised
duplicate is `"12अ"`, a variant reading.

**`muhurta_chintamani` — translation complete, numbering still wrong.** All 206 shlokas are
`"translated"` since 2026-08-22. Chapter-1 numbers still run 11–32, 1–7, 37–44: distinct, so
they ingest, but the sequence is wrong. `MC_REMAINING_RAW.json` does **not** resolve it —
checked 2026-08-22, it covers pages 53–480 with zero textual overlap with chapter 1. Fixing
it needs the chapter-1 pages of `muhurt_chintamani_002342_hr6.pdf` read against a canonical
edition.

**`aryabhatiya`** — 4 pādas / **121** shlokas, re-verified against the JSON 2026-09-02:
Gītikā 13, Gaṇita 33, Kālakriyā 25, Gola 50. **Edition digitised:** Clark, W. E. (ed. & tr.),
*The Āryabhaṭīya of Āryabhaṭa*, Chicago UP, 1930; cross-checked against Shukla, K. S. &
Sarma, K. V., INSA New Delhi, 1976. Composed 499 CE at Kusumapura, Āryabhaṭa aged 23.

**`panchasiddhantika`** — 18 chapters / **166** shlokas, re-verified 2026-09-02
(18·12·10·8·8·10·8·9·8·8·8·8·9·8·8·8·8·10). **Edition digitised:** Thibaut, G. & Dvivedī, S.,
*Pañcasiddhāntikā*, Benares 1889, repr. Chowkhamba Sanskrit Series vol. LXVIII, 3rd ed. 1997;
see also Neugebauer & Pingree, Copenhagen 1970–71. It is the sole surviving summary of five
earlier siddhāntas — Paitāmaha, Vāsiṣṭha, Romaka, Pauliśa, Saura — four of them otherwise
lost. Varāhamihira ranks Saura best, Romaka and Pauliśa equal behind it, and dismisses
Vāsiṣṭha and Paitāmaha. Epoch Śaka 427 = 505 CE.

Both entries were salvaged 2026-09-02 from per-text readme files before those were
drained; both READMEs also listed per-chapter files (`AB_001.json`, `PS_001.json` …) that the
one-file rule retired on 2026-08-18, and those lists were **not** carried forward.

**`apastamba_dharma_sutra`** — re-digitised from OCR 2026-09-02 (the 1898 Mysore edition
with Haradatta's Ujjvalā), replacing a 1,437-record off-schema file. **1,315 sūtras**,
citation `praśna.khaṇḍa.sūtra`. Externally checked: the parse independently yields 1.1
`अथातः…`, 1.2 `धर्मज्ञसमयः प्रमाणम्`, 1.3 `वेदाश्च` — the canonical opening, Āp.Dh.S.
1.1.1.1–3.

- **paṭala is deliberately not in the citation.** Only 4 paṭala colophons survive a strict
  pattern against 22 canonical; a looser pattern matches commentary prose that merely
  mentions paṭala, which is how an earlier count reached 20. Khaṇḍa numbers run continuously
  within a praśna, so `praśna.khaṇḍa.sūtra` is unique and can gain paṭala later from a
  reference edition **without renumbering anything**.
- **45 sūtras are ABSENT from the OCR across 29 khaṇḍas** (1,315 emitted + 45 absent =
  1,360 against the ~1,364 usually cited) — their `॥N॥` markers were lost, so
  the lines read as commentary. They are recorded, never invented; the parser prints each
  with its khaṇḍa and source line. Recovery was attempted and rejected: by position it fails
  (23 of 41 gap segments match the alternation, 18 do not), and by lemma-overlap it reaches
  83.5% raw / 96% gated — over 45 gaps that still puts commentary into a citable sūtra slot.
- **One sūtra was recovered, with its evidence in the code.** 1.1 sat unnumbered at source
  line 1158; the following line glosses its two opening words, and the next sūtra is
  independently numbered २. `RECOVERIES` in `apastamba.py` carries the justification.
- **1.9.14 was not absent — it was MERGED.** The OCR ran two sūtras onto one line,
  `अन्तश्शवम्॥१४॥ अन्तश्चाण्डालम्`, and the parser's end-of-line numeral regex swallowed 14
  into 15 and reported 14 missing. **Found by a translator reading the text, not by any
  count** — `GOTCHAS.md` G12, "a 'missing' record may be a MISLABELLED one, and counts cannot
  tell you." Exactly one such line exists in the text; the parser now splits them.
- **1.32.24 is genuinely corrupt.** `धर्मप्रह्लादन कुमालनाय रुदह्न मृर्त्युः` does not parse
  as Sanskrit. Its legible opening and closing are drafted and the corrupt middle is marked
  untranslatable in both languages rather than smoothed into a plausible sentence.
- **2.14.20 continues after a lunar day missing from the source itself**, and 2.6.11 lists
  seven Vedāṅgas where the canonical count is six. Both recorded, neither corrected.
- **Translation state: `drafted`, not `translated`.** All 1,315 carry `english_draft` and
  `hindi_draft`; the served `english`/`hindi` fields are empty on every one. Roughly 90
  sūtras were flagged by their translators as obscure or OCR-damaged and rendered literally
  rather than smoothed — that list is in the commit messages for the drafting batches and is
  the natural starting point for verification.

### Incipit audit COMPLETE — 33 texts, 71,110 shlokas, all GENUINE

Run 2026-09-02 after three fabricated Siddhānta texts were found. Every held text outside the
Jyotiṣa set was compared against its attested incipit, with mid- and end-of-text spot checks
because the `panchasiddhantika` pattern (genuine opening, fabricated remainder) defeats an
opening-only check.

| Set | Texts | Shlokas | Result |
|---|---:|---:|---|
| Vedic Saṃhitā | 5 | 22,686 | **all genuine** |
| Upaniṣad | 20 | 2,100 | **all genuine** |
| Upaveda | 8 | 45,324 | **all genuine** |

**Fabrication is confined to the three Siddhānta texts** from the 2026-07-17 hand-ingestion.
Everything fetched through the Wikisource, SARIT and sanskritdocuments pipelines is real. That
is the single most useful thing this audit establishes: **the pipelines are trustworthy and the
hand-ingestion was not.**

Two specific worries going in, both cleared:
- **G21, verse-only extraction.** Caraka and Suśruta are mixed verse and prose, and a
  digitisation reading only `<l>` would drop most of the text while validating cleanly.
  Checked: 288 and 203 passages over 400 characters respectively. **The prose is present.**
- **The seven Brāhmaṇa/Āraṇyaka-embedded Upaniṣads** could legitimately begin mid-work.
  None does; all open at their canonical beginning.

**`bhela_samhita` starts at 4.1 and that is CORRECT** — it survives in one damaged Tanjore
manuscript and adhyāyas 1–3 are lost in transmission, as §"Bhela Saṃhitā from SARIT" already
records. An attested transmission gap, not the `saravali` ordering defect. Do not "fix" it.

**Smaller findings:** `susruta_samhita` carries an extra `1.0` prefatory entry before 1.1.
`dhanurveda` is a faithful digitisation — byte-checked against its sanskritdocuments source —
but "Dhanurveda" is a genre label, and this is specifically a **Śārṅgadhara-tradition digest**
citing the *Vīracintāmaṇi*, distinct from the 17th-c. Vāsiṣṭha Dhanurveda-saṃhitā. Its
author/edition fields should record that rather than staying blank.

### Upaniṣad set — all 20 GENUINE, three separate defects

Audited 2026-09-02 against attested incipits, with mid/end spot checks on the four largest.
**No fabrication anywhere**: `isha` opens `ईशा वास्यमिदं सर्वं`, `chandogya`
`ओमित्येतदक्षरमुद्गीथमुपासीत`, `brihadaranyaka` `उषा वा अश्वस्य मेध्यस्य शिरः`, `maitri` the
Bṛhadratha–Śākāyanya frame. **None of the seven Brāhmaṇa/Āraṇyaka-embedded Upaniṣads starts
mid-work** — a specific worry going in, since they are chapters of larger works.

Three defects, none of them fabrication:

- **`brihadaranyaka_upanishad` — 127 of 437 shlokas (29%) carry English editorial apparatus
  INSIDE the Devanāgarī `text` field.** It is a sandhi-split study edition and the apparatus
  came with it: *"SF as marked below is Sandhi-free text to aid students"*, `काण्व पाठः । A
  मधु काण्ड[उपदेश काण्ड] अध्याय I ब्राह्मण i-vi`. This is a **mukhya** Upaniṣad and that text
  is served as scripture. The worst of the three.
- **`mundaka_upanishad` — mis-chaptered by one.** Chapter 1 holds a single shloka, the
  śānti-pāṭha; the real opening `ॐ ब्रह्मा देवानां प्रथमः संबभूव` is chapter 2 shloka 1, so
  every khaṇḍa number is offset. Distinct from the `saravali` pattern: it does not begin
  mid-work, it is mis-numbered.
- **`subala_upanishad` — shloka 1 is absent**, numbering starts at 2. The cosmogonic opening
  frame (`तदाहुः किं तदासीत्…`) is missing; the substantive content that follows is authentic.

**Why this matters for reading the Translated column:** all three defects sit in texts that are
otherwise genuine, so none would ever be caught by an incipit check alone — the apparatus
contamination in particular is invisible unless you look for Latin characters in a Devanāgarī
field.

### `taittiriya_samhita` — 49% of its verses are duplicates that all ingest

Found 2026-09-02 by the incipit audit. **The text is genuine** — TS 4.5 is the Śrī Rudram
Namakam verbatim, and the attested `इषे त्वोर्जे त्वा` opening is present. This is a
duplication defect, not the fabrication pattern.

**976 of 2,294 shlokas (42.5%) are exact duplicates of the shloka two positions earlier**, and
1,126 (49.1%) are exact duplicates of something. The pattern is A, B, A, B:

```
1.1.1  पूर्णर्षयोऽग्निना ये देवास्सूऱ्यो…
1.1.2  इद्यज्ञं प्र सुव नारिरानुष्टुभेन…
1.1.3  पूर्णर्षयोऽग्निना ये देवास्सूऱ्यो…   ← identical to 1.1.1
1.1.4  इद्यज्ञं प्र सुव नारिरानुष्टुभेन…   ← identical to 1.1.2
```

**They all ingest, and that is the load-bearing part.** There are **zero** duplicate
`(chapter, number)` keys, so `seed_texts.py`'s dedupe — which keys on exactly that pair — has
nothing to catch. G8 records that a duplicate key deletes data silently; this is its mirror
image: **distinct keys over identical text multiply data silently.** A citation to 1.1.3 and
one to 1.1.1 return the same verse, and both look valid.

**Consequences:** the text's true unique content is roughly **1,168 verses, not 2,294**, and
the corpus total of 93,481 is inflated by ~1,126. Any per-text count reasoning about
`taittiriya_samhita` is wrong by a factor of two.

**The other four Saṃhitās are clean** — Ṛgveda 0.7% incidental, Sāmaveda 0.0%, Śukla Yajurveda
0.6%, Atharvaveda 3.9%, and **none** shows the offset-2 signature (0.0%, 0.0%, 0.1%, 0.0%).
So this is one text's ingestion defect, not a pipeline-wide one.

### ⚠ THREE SIDDHĀNTA TEXTS ARE FABRICATED — verified 2026-09-02, quarantine before use

`aryabhatiya`, `surya_siddhanta` and `panchasiddhantika` — **559 shlokas, all marked
`translated`, all serving as citation surfaces** — do not contain the works they claim to.
Found while looking for OCR ground truth; the scan of Pañcasiddhāntikā and our held text
share no content at the same verse number.

**The evidence, per text:**

- **`aryabhatiya` 1.1** reads `हरिः तेषां पादानां प्रणम्य परमं स्मरेत् । ब्रह्मगुप्ततनय आर्यभटः
  सिद्धान्तमाह ॥` — *"Āryabhaṭa, **son of Brahmagupta**"*. Brahmagupta was born **c. 598 CE**
  and wrote in 628; the Āryabhaṭīya is **499 CE**, and Brahmagupta *studied* it as a later
  astronomer (verified against Wikipedia 2026-09-02). The claimed father was born 99 years
  after the son wrote his book. The real Gītikāpāda 1 opens `प्रणिपत्यैकमनेकं…` with a tribute
  to **Brahman**; ours opens with **Hari**.
- **`surya_siddhanta` 1.1–1.2** read `प्रणम्य शिरसा देवं गुरुं विद्याविनायकम्…` and
  `ब्रह्मा ब्रह्मगिरि ब्रह्ममयं…`. The real 1.2 is the famous
  `अल्पावशिष्टे तु कृते मयो नाम महासुरः` (verified 2026-09-02). Ours *mentions* `मयदैत्याय` —
  right topic, wrong words, and `ब्रह्मा ब्रह्मगिरि ब्रह्ममयं` is not grammatical Sanskrit.
- **`panchasiddhantika`** is genuine for **1.1–1.3 only**, then breaks into uniform two-line
  paraphrase (163 of 166 verses; median 48 chars, the shortest of any verse text held). 1.12
  writes revolutions as the digit string `४३२००००` where Sanskrit astronomical texts use
  *bhūtasaṃkhyā* word-numerals; **1.17 gives the epoch as Śaka 425 where this very file
  records Śaka 427**; 1.18 is a pseudo-colophon calling chapter 1 "the first *tantra* …
  abridged by Varāhamihira". Its 13.6 gives earth's circumference as 500 yojanas with
  diameter 200 — π ≈ 2.5.

**Why every existing check passed.** The metadata is correct. `aryabhatiya`'s structure is
4 pādas of 13/33/25/50 = 121, matching canon exactly — re-verified against the JSON on
2026-09-02, hours before this was found. The editions recorded above (Clark 1930; Thibaut &
Dvivedī) are real. Contiguity, duplicate-key and canonical-count checks all pass, **because
every one of them checks numbering and none checks the words.** This is `GOTCHAS.md` G6
arriving from an unwatched direction: the citation surface is intact and what sits behind it
is invented.

**There is no cheap corpus-wide detector, and that was measured rather than assumed.** A
digit-string probe flags `samaveda_samhita` at 60.8% and `manu_smriti` at 55.8% — legitimate
source formatting — while scoring both fabricated Siddhānta texts **0.0%**. Type-token ratio
does not separate them either (`aryabhatiya` 0.566 sits mid-pack). **Only comparison against
the known incipit distinguishes them.** Done for all 19 Jyotiṣa texts on 2026-09-02: the Hora
and Saṃhitā set is genuine — `bphs` opens with Maitreya approaching Parāśara, `brihat_samhita`
with `जयति जगतः प्रसूतिर्विश्वात्मा`, `shatpanchashika` correctly naming Pṛthuyaśas as
Varāhamihira's son — and `arch_jyotisham`/`yajusha_jyotisham` are genuine Vedāṅga Jyotiṣa.
**The three are confined to Siddhānta.**

**Provenance:** all three entered as per-chapter files on **2026-07-17** (`1cccca6`
"recategorize Hora into schools + ingest new texts", with `4258491`), and were consolidated to
one-JSON-per-text by `c08e08f` on 2026-08-18. STATE.md's 2026-08-12 line "Saravali, Surya
Siddhanta, Aryabhatiya, and Panchasiddhantika are now digitized" records that arrival.

**`saravali` has a different defect from the same ingestion window and is NOT fabricated.**
Its 1.1 is `न प्रपीता भवेत्कूपे…` — a real verse about Mars in the fourth house, i.e. the
digitisation begins mid-work. A flat 1,163-sūtra single chapter with no opening. Ordering, not
invention.

**Not defects — do not "fix" them into breakage:** `MinarajaYavanajataka` numbers variant
chapters `"24अ"` / `"63अ"` / `"63ब"`; `Jatakaparijatah` numbers half-shlokas `"N 1/2"`.

**The 71 dedupe losses, in full.** Was **2,800**: `brihat_samhita` was 2,729 of it and is now
**0**, its two files consolidated 2026-08-18. They were never two recensions — 2,574 of 2,711
shared keys differed only in **sandhi** (`प्रसूतिः विश्वात्मा` vs `प्रसूतिर्विश्वात्मा`), one
text digitised twice. Ingestion unchanged at 2,771. The remaining 71 are intra-chapter and
pre-date the converter's duplicate rejection.

**Āpastamba, checked against the canonical structure 2026-08-18.** It is
Praśna→Paṭala→Khaṇḍa→sūtra, so `1.1.1` is a *correct citation*; the data cannot be mapped
onto it — 219 bare-integer records and 15 literal `X.X.21` placeholders, the digitiser
recording "prefix unknown". **`apastamba_paribhasha_sutra` is equally broken, not a minor
sibling:** every integer 1–53 is reused as `number` 2–15 times, plus 7 empty-string records.

## Nārada Smṛti lands — and the same fix recovered 118 Caraka units (2026-08-24)

**Tier `uncitable`. 3 parts · 22 chapters · 931 verses — against 931 `<lg>` in the file.**
Zero duplicate keys, zero residual IAST. Lariviere/Ikari critical edition, © Richard W.
Lariviere and Yasuke Ikari and SARIT, CC BY-SA.

Structure, stated by the TEI: Mātṛkā (Prolegomena) 3, Vyavahārapadāni (Titles of Law) 17,
Pariśiṣṭam (Addenda) 2. **The addenda declare `n=19,20`, not 1,2** — positional numbering
would file them as chapters 1 and 2 (G24). Part 2 holds 17 titles where Nārada canonically
has 18: the 18th is absent from this recension and the addenda resume at 19. That is the
edition's own numbering and is **not** repaired.

### The two shapes that blocked it — and the weight was the opposite of first reported

| Shape | Lines | Verses | What it is |
|---|---:|---:|---|
| `15-16.001a` | **62** | **31** | a **merged chapter** |
| `01.124-1a` | 4 | 2 | a **sub-numbered verse** |

An earlier note had these reversed in emphasis. Measured: the merged chapter is the bulk.

**The merged chapter carries no collision risk, and that is measured rather than assumed.**
`<div n="15">` holds **62 merged-numbered labels and zero own-numbered ones**; its `<head>` is
*Vāgdaṇḍapāruṣye (Verbal and Physical Assault)* — title 15 (Vākpāruṣya, verbal) and 16
(Daṇḍapāruṣya, physical) combined into one chapter by this edition. The chapter number keeps
coming from the div; only the last component of the citation is ever the verse.

### One line was the whole blocker

`int(re.sub(r"[^\d]", "", comp))` renders `124-1` as **1241** — a plausible number, silently
wrong, colliding with nothing so nothing complained. Replaced by `verse_number()`, which
returns `int | str`; `norm_key()` already returned `int | str` and the validator's
`SUB_NUMBERED` already accepted `N-M`. The corpus has supported these keys since Mayamata's
`41-2`. A `verse_sort_key()` is required alongside it — `sorted()` raises `TypeError` on
`{1, "124-1"}`.

### It was never Nārada-only: 118 Caraka units were hidden the same way

Measured across every SARIT text before shipping: hyphen tolerance also matches **118 Caraka
lines** (`Ca.1.18.7-1`, `-2`, `-3` — sub-numbered *prose* units) and **1 Suśruta** verse
range (`1.15.26-27`). Aṣṭāṅgahṛdaya, Aṣṭāṅgasaṃgraha, Bhela and Manusmṛti: **+0**. So it is a
default rule, not a per-text opt-in.

**Where those 118 units actually were — corrected.** The first report said "merged into verse
7". They were appended to the **preceding cited verse**: `Ca.1.18.6` measured **1,419
characters** against a corpus median of 87, and is now **522**. Caraka's verses over 1,000
characters dropped **50 → 38**. Verse `18.7` was 118 characters throughout and never held
them — the `order[-1]` continuation branch attaches an unmatched line to whatever was cited
last, which is not always the verse the citation names.

**One source inconsistency, rejoined rather than corrected away.** Caraka writes the run as
`Ca.1.18.7.-1`, `Ca.1.18.7-2`, `Ca.1.18.7-3` — a stray dot on the first only. A component that
is *only* a sub-number is rejoined to the one before it. Without that, `-1` reduces to verse 1
and collides with the chapter's real verse 1, blocking the whole text on a duplicate key.

### Validator: `structure.levels` counts a sub-number as part of its component

`_components` now returns `(main, sub)` pairs, so `18.7` and `18.7-1` are both **depth 2** and
`18.7 < 18.7-1 < 18.8`. Reading `18.7-1` as three components would make a correct parse look
one level too deep. `DOTTED` widened to match. **Measured cost: +1 error**, in
`apastamba_paribhasha_sutra` — an already-failing off-schema text where the widened check
found one more real defect. Nothing was suppressed.

### Also fixed: the OUTER division now uses its declared `n`

The inner division was switched to declared numbering under G24; the outer was still
positional. Measured 2026-08-24: **every held text's outer divs are positional**, so this is a
no-op today — which is exactly the state G24 was written about, one level up. Confirmed a
no-op by an unchanged full dry-run.

## `fixability.py` — deciding manual vs code by measurement (2026-08-24)

Six texts have been blocked on **numbering** rather than on data, and the call was made by
feel each time. Once it was made badly: Manusmṛti got two sessions of accurate damage
analysis that was thrown away when the text was re-acquired whole in one pass.

`scripts/sanskrit-convert/fixability.py` scores a blocked text and recommends
**re-acquire / code / code-opt-in / manual**.

### What is derived, and what is not

`A` (affected units), `S` (distinct citation shapes) and `X` (sibling blast radius) are
**measured** from the source and the current parse. `R` (a clean edition exists elsewhere)
and `N` (the fix would renumber existing keys) are judgements no script can make, so they are
**declared** — and declaring them is the point at which someone has to have looked.

### The rule, in order

1. **`R` → re-acquire.** Replacing beats diagnosing; check for a clean source *before*
   characterising damage.
2. **`N` → never renumber** (G7). Use a string key or `structure.known_gaps`.
3. **`A/S ≥ 10` → code a rule.** If `X > 0` it must be a per-text **opt-in**.
4. **`A/S < 10` → manual**, via `SARIT_CORRECTIONS` / `SOURCE_CORRECTIONS`.

### It reproduces every decision already made — that is what makes it a metric

| Case | A | S | X | Rule says | What was done |
|---|--:|--:|--:|---|---|
| Mayamata adhyāya 21 marker | 1 | 1 | 0 | manual | manual |
| Caraka stray-dot sub-number | 1 | 1 | 0 | manual | manual |
| Nārada citation shapes | 33 | 2 | 0 | code | code |
| Aṣṭāṅgasaṃgraha Paribhāṣā | 119 | 1 | 0 | code | code |
| Bhela no-separator | 272 | 1 | 2 | code-opt-in | code-opt-in |
| Manusmṛti bracketed xref | 801 | 2 | 0 | code | code |
| Manusmṛti damaged numbering | — | — | — | re-acquire | re-acquire |

`--history` replays these on every run, and each is a test.

### The threshold is under-determined, and says so

**No case falls between 2 and 16**, so any threshold in that gap reproduces every decision
identically. `10` is the midpoint of an empty interval, not a discovered constant. Confirmed
by mutation: moving it to **20** breaks Nārada (16.5), moving it to **0.5** breaks Mayamata
and Caraka (1.0). The first case that lands in the gap is the one that should settle it.

### The prerequisite: "manual" had to become possible first

`apply_corrections()` is called from exactly one place — the wikitext/marker path — so
**SARIT texts had no manual-correction mechanism at all**, and every text acquired since
Aṣṭāṅgahṛdaya is SARIT. A metric that recommends "fix this by hand" is worthless if by-hand
is unimplemented. `SARIT_CORRECTIONS` is the citation-keyed sibling.

**Its loud half is `unfired_sarit_corrections`.** A page-and-index correction fails loudly by
landing on the wrong verse; a citation-keyed one just silently does nothing when the source
changes under it. Verified by mutation: a stale citation prints
`CORRECTION NEVER FIRED` *and* drops Caraka 9,643 → 9,642.

### The metric's first act was to overturn one of my own changes

The Phase-A rejoin heuristic for `Ca.1.18.7.-1` fires on **exactly one line in the whole
corpus** — A=1, S=1 → **manual**. It is now a `SARIT_CORRECTIONS` entry instead, and the
conversion is byte-identical.

### Two instrument errors inside the metric itself, both caught by using it

1. **`shape()` normalised digits but not the trailing Sanskrit word**, so
   `Ca.2.7.1athāta` and `Ca.2.7.6tasyemāni` counted as two shapes rather than one.
   S is the denominator, so over-counting shapes deflates `A/S` and flips code → manual.
   Caraka measured **S=12** before, **S=2** after.
2. **The digit placeholder was `N`, which is itself a letter**, so the letter-collapse ate its
   own placeholder: `Ca.2.7.1athāta` → `W.W.W`, which the citation-ish filter discarded. The
   tool reported **"nothing affected" for a text with 13 real unread citations** — a reader
   inventing an absence (`rule:discernment-checks` §6). Placeholder is now `#`.

### What it found immediately

**Caraka still has ~13 unread citation lines** in 3 shapes — `Ca.2.7.1athāta` (no separator)
and `Ca.2.7.7,(1)tato` (comma-parenthesis sub-number). Scored **A=6, S=3 → 2.0 → manual**.
Not actioned; recorded so the next session starts from a measurement rather than a hunch.

---

## Part 7 — Brāhmaṇa and Āraṇyaka (Youvan's scope), acquired 2026-08-25

Converted by this pipeline, emitted into `Tushar/Youvan/texts/`. One pipeline, one validator,
one sources repo; only the output root differs (`convert.py:YOUVAN_OWNED`).

### Both are `unit_mismatch`, and that is a decision

**What is citable for these two is the DIVISION count, not a verse total**, and both parses
match the citable figure exactly. No published anuvāka total was found for either.

| Text | Citable | Parsed | Verses (anuvākas) |
|---|---|---|---:|
| Taittirīya Brāhmaṇa | 28 prapāṭhakas, in 3 aṣṭakas (8 + 8 + 12) | **28**, in 4 sections | 1,832 |
| Taittirīya Āraṇyaka | 10 praśnas | **10** + a 2-praśna Ekāgnikāṇḍa | 638 |

**The Brāhmaṇa's fourth section is not a fourth aṣṭaka.** The source heads its divisions
`प्रथमाष्टके … प्रपाठकः N`, `द्वितीयाष्टके …`, `तृतीयाष्टके …` and then `काठके …` — and
Kāṭhaka's three are prapāṭhakas 10–12 of aṣṭaka 3, which is what makes the canonical 8+8+12
come out right. The corpus keeps four sections because that is the source's own division;
citations read `taittiriya_brahmana 1.1.80` = aṣṭaka.prapāṭhaka.anuvāka.

**The Āraṇyaka's Ekāgnikāṇḍa is kept as a second section rather than renumbered.** This
edition prints it after praśna 10 under its own heading with its own numbering, 1 and 2.
Folding it in as praśnas 11 and 12 would change the value of a key the source states
(`rule:safety-flag-needs-a-test`'s sibling, G7: never renumber). It is section 2.

### Three source facts the parse depends on

1. **The structure is in `<h2>` headings inside the content block, not in verse markers.**
   `parse_sanskritdocs_sectioned` reads the section from the heading's first word and the
   division number from its trailing numeral. Numbering by POSITION would give 1..28 where
   the citation says 1.1 .. 4.3, because prapāṭhakas restart at 1 in each section (G24).
2. **A pluta vowel is written `३` and can start a line.** `वेत्था ३ इति` — two in the
   Brāhmaṇa, one in the Āraṇyaka, all mid-division and all out of sequence. A verse number
   strictly increases; these do not, so the line is read as a continuation and merged into
   the previous verse. Nothing is dropped: 1,834 markers, 1,832 verses, and the body
   Devanagari count is within 178 characters of the source (colophon stripping).
3. **Each praśna of the Āraṇyaka closes with a repeated śānti-pāṭha numbered `०`.** Kept as
   `0-2`, the `SUB_NUMBERED` form already used for Mayamata's `41-2`, and ordered beside its
   twin because a chapter must not restart. **It is not always a copy of the opening** — in
   praśna 6 the closing block is 223 characters against the opening's 79 and carries a verse
   the opening does not, so merging it away on an assumed identity would have deleted text.

### `aranyaka.itx` is excluded, and the source says so itself

`sanskritdocuments.org/doc_veda/aranyaka.itx` is titled, in its own header,
`taittirIya AraNyaka 1 aruNaprashnaH` — praśna 1 of the text above, i.e. a **subset**.
It is also ITRANS/TeX, not Devanagari; a Devanagari-character count of it returns 0, which
is a fact about the encoding and not about the content. Not ingested.

### `goladhyaya` — partial by design, and the absences are enumerated

**241 verses of the 318 its own table of contents implies (76%).** Digitised 2026-09-02 by
`scripts/sanskrit-convert/goladhyaya.py` from Ānandāśrama Sanskrit Series vol. 122
(`8252.txt`), which interleaves three layers: the mūla, Bhāskara's own *Vāsanā*
auto-commentary, and Muniśvara's *Marīci* ṭīkā. Only the mūla was taken.

**Seven of the eight chapters end on exactly the verse number the table of contents predicts**
— ग्रहण 29, वलन 74, उदयास्त 24, शृङ्गोन्नति 6, ऋतुवर्णन 15, प्रश्न 63, त्रिप्रश्न 49. The
exception is यन्त्र, which ends at 57 against a predicted 58. That disagreement is recorded
rather than resolved.

**The shortfall is deliberate and is false-negative by choice.** Marīci quotes mūla verses
inside its own commentary — the Ṛtuvarṇana opening is quoted 700 lines early, inside the
Yantra chapter — so verses appearing inside a commentary block are skipped rather than
harvested. That costs real verses: `वलन` holds 45 of 74, `प्रश्न` 39 of 63. **For a citation
surface a missing verse is recoverable and a wrong one is not**, and this corpus already
carries three fabricated texts that passed every numbering check (G31).

**Per-chapter absences are printed by the converter on every run** — do not restate them here,
and do not fill one in from a second edition without recording which edition it came from.

Verified on write: all 241 verses appear **verbatim** in the source, none carries commentary
vocabulary or Latin characters, all end in a daṇḍa, and the text contributes **zero** duplicate
`(chapter, number)` keys, so every verse reaches Mongo (G8).

### `grahaganita` — the first half only, and its witness is weaker than `goladhyaya`'s

**272 verses across 9 sections**, digitised 2026-09-02 by
`scripts/sanskrit-convert/grahaganita.py` from Ānandāśrama Sanskrit Series vol. 110
(`7404.txt`).

**It is `(पूर्वार्धः)` — the first half.** The volume's own preface says
`ग्रहगणिताध्यायेऽस्मिन्नेकादशाधिकारा वर्तन्ते`, eleven adhikāras, of which this carries three:
मध्यम, स्पष्ट, त्रिप्रश्न. The *uttarārdha* is a separate Ānandāśrama number and is **not
held** — do not read the 272 as a complete Grahagaṇita.

**Nine sections, not three**, because मध्यमाधिकāra is subdivided into seven adhyāyas. The
volume states this itself (`सप्तभिरध्यायैः` in its closing colophon; the प्रत्यब्दशुद्धि
colophon calls that adhyāya `पञ्चमः`), so the spans are read off colophons rather than inferred.

**The validation is weaker than `goladhyaya`'s and that difference matters.** Golādhyāya is
checked against a table of contents giving every chapter's last verse — independent of the body.
**This volume has no such ToC**: its `अनुक्रमणिका` lists chapter names with no verse numbers. So
the bound is each section's own highest verse number, derived from the data it checks. It still
rejects commentary citing a verse from elsewhere, but it cannot catch a section mis-numbered
throughout. **Treat `grahaganita` as less corroborated than `goladhyaya`.**

**One finding left visible rather than repaired:** `ग्रहभगणमानाध्यायः` reports 14 verses against
a bound of 52, so 38 read as absent. A stray number is almost certainly inflating the bound.
Inventing a smaller one to tidy the output is the exact failure G31 records.

Verified on write: all 272 verses **verbatim** in the source, no commentary vocabulary, no Latin,
all terminated by a daṇḍa, all untranslated with empty served fields, and **zero** duplicate
`(chapter, number)` keys.

### `lilavati` — verses 135–272 only, and a correction to an earlier judgement

**117 verses of the 138 in its range**, digitised 2026-09-02 from Ānandāśrama 107 (`8244.txt`),
which is `उत्तरार्धरूपो द्वितीयो भागः` — the **second half only**, opening at `क्षेत्रव्यवहार`.
There is no first half in this volume.

**An earlier assessment the same day called Līlāvatī intractable, and it was wrong.** The
reasoning was that a mathematics treatise prints quantities in Devanāgarī between daṇḍas, so
verse numbers cannot be told from data. The measurement behind it was taken on the **Benares
scan's OCR** — 262 markers, 84 descents, 33% +1 steps — and that judged *the instrument*, not
the text. This clean file opens at verse **135**, where `क्षेत्रव्यवहार` falls in the work, and
closes at **272**, Līlāvatī's attested last verse.

**That closing 272 is the only external check available here** — no table of contents exists in
this volume — and it is worth more than it looks: the file's own final verse agreeing with the
attested total is corroboration from outside the file.

**Ordering was resolved by keeping the longest strictly-ascending reading**, not by tuning. Five
numbers were dropped as transposed or stray (`154, 164, 29, 1, 14` — the `१४` sits between 260
and 261), and every one reappears in the absence list, so nothing vanishes silently.

Verified on write: 117 verses **verbatim**, no gloss vocabulary, no Latin, all daṇḍa-terminated,
all untranslated with empty served fields, **zero** duplicate keys.

**Two further Līlāvatī witnesses are held as scans** and neither has been merged in: Benares
Sanskrit Series 153, and a 146-page volume reaching verse 249+. Merging editions without
recording which verse came from which is `rule:discernment-checks` §5 — do not.

### `bijaganita` — completes Siddhānta Śiromaṇi, and is the weakest of the four

**150 verses**, digitised 2026-09-02 from S.K. Abhyankar's bilingual edition (`3328.txt`). With
this, **all four parts of the Siddhānta Śiromaṇi are held**: Līlāvatī, Bījagaṇita, Grahagaṇita,
Golādhyāya.

**The file was twice mis-assessed, and both errors were in the same direction — dismissing a
usable source.**

1. *"83 verse markers."* It uses **both** daṇḍa forms; counting only `॥N॥` missed 106 of 189.
   That is **G32, on the file that motivated G32.**
2. *"Poor OCR."* The stray-Latin count was high because the edition is **bilingual** — Devanāgarī
   and Latin legitimately interleave. The Devanāgarī is clean: `गुण` 84 vs `गुग` 0, `वर्ग` 92 vs
   `वगे` 0.

On that basis Bījagaṇita was recorded as the one missing part while its source sat in the tree.

**The file has no newlines.** It is a single line, so every line-oriented converter returns zero
on it. The markers are the only boundaries, and the verse is the maximal Devanāgarī **suffix** of
each segment, the English translation preceding it.

**Rank the four by how well corroborated they are, because they are not equal:**

| | witness |
|---|---|
| `goladhyaya` | **strongest** — a ToC giving every chapter's last verse; 7 of 8 chapters land on it |
| `lilavati` | closes on **272**, Līlāvatī's attested last verse — corroboration from outside the file |
| `grahaganita` | section maxima, self-derived |
| `bijaganita` | **weakest** — bound 187 self-derived, no ToC, no attested total for this edition |

Verified on write: 150 verses **verbatim**, **no Latin** (the translation did not leak), no served
fields, zero duplicate keys. 37 absences of 187 recorded, and 7 numbers dropped as out-of-order.

### `surya_siddhanta` — DELETED 2026-09-02

**Removed from the corpus.** It was fabricated: 14 chapters, 272 shlokas, every one marked
`translated` with a non-empty English field, opening
`प्रणम्य शिरसा देवं गुरुं विद्याविनायकम्` where the attested 1.2 is
`अल्पावशिष्टे तु कृते मयो नाम महासुरः` — a line that appears **zero** times in the deleted text
and is present in the genuine 1925 scan.

**Why deletion rather than a fix.** `scripts/seed_texts.py` walks every corpus JSON and
`/texts/{text_id}` serves it, so the public API was returning 272 invented verses **and 272
invented English translations** under the name of a real work. That breaks the workspace hard
rule *"Computation is AI-assisted; meaning is not"* on the surface most likely to be quoted.
Nothing computed on it — `@source` is read-only (`app/masters/_source.py:77`), attaching
metadata and a docstring line — so removal costs nothing at runtime and `/texts` returns a 404
listing the available texts.

**Three `@source` decorators still name it** — `yearly_calendar.py:26,28`, `yearly_gochar.py:29`
— plus two provenance strings in `panchanga.py`'s tithi table. Those are now **dangling
citations, which is the correct state**: the claim "this calculation is justified by Sūrya
Siddhānta 1.1–10" is true of the real text; it simply cannot be resolved against a corpus that
no longer holds a forgery of it. Do not "fix" them by pointing at another text.

**The replacement is blocked on OCR quality, not availability** — the Asiatic Society of Bengal
1925 edition (ed. Sudhākara Dvivedī, *Sudhāvarṣiṇī*) is held and public domain; its reading is
not usable. Detail in STATE.

**`aryabhatiya` and `panchasiddhantika` are still held and still fabricated.** They are cited
nowhere under any spelling, so the exposure is the `/texts` surface alone — the same argument
applies to them and they have not been removed.

### `aryabhatiya` and `panchasiddhantika` — DELETED 2026-09-02

Removed alongside `surya_siddhanta`, on the same argument and by the same instruction. **With
these, all 559 fabricated shlokas G31 records are out of the corpus**: 121 + 166 + 272, every
one of which was marked `translated` and carried a machine-written English field.

- **`aryabhatiya`** opened `हरिः तेषां पादानां प्रणम्य … ब्रह्मगुप्ततनय आर्यभटः` — *"Āryabhaṭa
  son of Brahmagupta"*, naming a father born c. 598 CE for a book written in 499, and saluting
  Hari where the real Gītikāpāda 1 (`प्रणिपत्यैकमनेकं`) salutes Brahman.
- **`panchasiddhantika`** was genuine for 1.1–1.3 and paraphrase thereafter, stating the epoch as
  Śaka 425 where this file records 427.

**Neither was cited anywhere, under any spelling**, so unlike `surya_siddhanta` their exposure
was the `/texts` API alone and nothing dangles.

**A scan is held for `panchasiddhantika`** (`panch_siddhantika_040577_hr6.pdf`, 344pp) and it is
**two-column** — use `--psm 3`, not `--psm 6`, which merges the columns into one line. No source
of any kind is held for `aryabhatiya`.

**The seeder now walks 61 JSON files and none of them is fabricated.** Derive it, do not trust
this line:

```sh
python3 -c "
from pathlib import Path
f=[x for x in Path('.').rglob('*.json') if 'docs' not in x.parts]
print(len(f),'files;',any(n in str(x) for x in f for n in ('Aryabhatiya','Panchasiddhantika','SuryaSiddhanta')))"
```

### `surya_siddhanta` — REPLACED the same day it was deleted

**280 verses across 11 chapters**, from a clean Rashtriya Sanskrit Sansthan e-text (`1277.txt`,
405,426 Devanāgarī characters, 458 Latin) carrying Raṅganātha's `गूढार्थप्रकाशक` commentary.

**Authenticity was checked in both directions before conversion**, and the converter refuses to
run if the first fails: the attested `अल्पावशिष्टे तु कृते मयो नाम महासुरः` is present and
correctly spelled — `कृते`, where the 1925 scan's OCR gave `कते` — and the deleted forgery's
opening `प्रणम्य शिरसा देवं` appears **zero** times.

**Its witness is the strongest of any text in this corpus, and it is fully external.** Sūrya
Siddhānta's canonical chapter lengths are attested independently of this file, and **8 of 11
chapters land on their canonical last verse exactly**: मध्यम 70, त्रिप्रश्न 48, चन्द्रग्रहण 26,
सूर्यग्रहण 17, छेद्यक 24, उदयास्त 18, भूगोल 25, ज्योतिष 27. The three that do not — स्पष्ट
(68 of 69), पात (13 of 14), मान (6 of 13) — are recorded, not adjusted.

**Numbering: ASCII digits inside daṇḍas.** Verses are marked `।।2।।` and `||1||` — the daṇḍa is
sometimes U+0964 doubled and sometimes an ASCII pipe, and **the digits are ASCII, not
Devanāgarī**. A `[०-९]` probe scores this file **5** markers against the correct **813**. This is
G32 one level deeper: the daṇḍa form varies *and* the digit script does.

Verified on write: 280 verbatim, no Latin, no served fields, zero duplicate keys. 67 lines were
rejected for carrying a number above their chapter's canonical length.

**The three `@source` decorators that dangled after the deletion now resolve again** —
`yearly_calendar.py:26,28` and `yearly_gochar.py:29` cite Sūrya Siddhānta 1.1–10 and 2.66, and
chapters 1 and 2 are held. Chapter 2 verse 66 is present.
