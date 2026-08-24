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
