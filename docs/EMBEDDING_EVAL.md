# Embedding evaluation — protocol

**Pre-registered 2026-09-14. Nothing has been run.** The decision rule below was written
before any number was seen, and that ordering is the point: at n=16,882 any separation is
statistically significant, so a threshold chosen after looking at the data is a check that
cannot fail (`rule:discernment-checks` §1).

Answers goal 3 in `../../propagation/state/workspace/GOALS.md` — *"the embedding model was
measured on THIS corpus, not assumed."* That goal's `Derived by:` reads the `## Result`
section at the bottom of this file. **It is empty until the run happens, and an empty result
must read as "not yet measured", never as a pass.**

## The question

Not "can a model retrieve Sanskrit." **Can a model place a verse nearer its own English
translation than nearer a different verse's translation** — on this corpus, with these
translators.

That is a far weaker property than semantic search, and it is the one that matters first,
because it is what would make the corpus's real problem tractable: **1,315 machine drafts exist
today and the verification queue has no ordering.** A working alignment score turns an unbounded
queue into a triaged one, and it is the same instrument that would have caught `minaraja`, where
fluent, term-for-term-correct English sat on top of OCR apparatus garbage and no monolingual
check could see it.

## Why the obvious design is worthless

Four defects, all raised in review before anything ran.

**1 · A global shuffle measures the wrong thing.** No text exceeds 23.9% of the translated
population and the top five hold 82%, so a globally-shuffled "false" pair is usually a verse
against *another work's translator*. That measures register and house style, not alignment. The
confusion that matters operationally is **within a chapter**, where adjacent verses share
vocabulary, subject and translator — and within-chapter discrimination is exactly what triage
depends on.

**2 · The positive class is contaminated.** Measured 2026-09-14 over all 16,882 translated
verses with non-empty English:

| | count |
|---|---:|
| verses whose English string is shared with another verse | **157** (60 distinct strings, so 97 are extra copies) |
| verses whose English is an ellipsis / missing-verse marker | **11** (5 distinct strings) |
| verses with English under 40 characters | **74** (minimum: **3 characters**) |

These sit in the true-pair distribution and widen precisely the left tail a naive reading would
interpret as "the instrument works on most verses."

**3 · The kill criterion cannot be evaluated as stated.** "Look at the bottom 200 and check the
known-contaminated `minaraja` verses are concentrated there" — `minaraja` is **23.9%** of the
population, so a *null* instrument puts ~48 of any bottom 200 there. With no labelled
contamination set, every outcome is explicable.

**4 · The largest block is confounded in the favourable direction.** `minaraja`'s uttarakhaṇḍa
arrived already fully translated with no source file committed and no recorded authorship. If
that English was machine-produced from the same Devanāgarī, it will align *better* than a human
translation does — for a reason unrelated to model capability. A high pooled mean would then be
a fact about provenance.

## Protocol

### Population

Start from the 16,882 translated verses with non-empty English. **Exclude** the 157 shared-English
verses, the 11 marker verses, and the 74 under 40 characters — reporting the excluded count, not
silently dropping them. Report the surviving n.

### Three nulls, reported separately

| null | how the false pair is drawn | what it measures |
|---|---|---|
| **N1 within-chapter** | a different verse's English **from the same chapter** | the operational case — this is the one that decides triage |
| **N2 within-text** | a different chapter, same text | same translator, different subject |
| **N3 global** | any other verse | register and house style. **The weakest, and the one a naive design would use alone** |

**Report per text, never pooled.** A pooled distribution over 16 texts and 16 translators is a
mixture of 16 distributions reported as one (`rule:discernment-checks` §5).

### Mandatory control: a lexical baseline on the same pairs

Character n-gram overlap between the IAST transliteration of `text` and the English —
`indic-transliteration` is already a dependency in `../scripts/sanskrit-convert/`. **If lexical
overlap separates as well as the embedding does, the embedding added nothing.** This is the same
test applied to the retrieval layer later, and it is the one result that can end the direction on
day one for about a dollar.

### Arms

At least: one multilingual embedding model, one Sanskrit-capable candidate, the lexical baseline.
**Pin the model version** — the floor is not reproducible against a drifting model, and
`grounding.py`'s `FLOOR = 0.55` is only meaningful because its 0.41–0.51 noise band was measured
against a fixed one.

## Decision rule — written before any number

**D1 · The instrument is usable for triage** iff, against **N1 (within-chapter)**, the median
true-pair score exceeds the **95th percentile** of the null in **at least 12 of the 16 texts**.
Fewer than 12 means it works on some translators and not others, which for a triage queue is
worse than not having it — it would silently under-rank whole texts.

**D2 · Embeddings earn their existence** iff they beat the lexical baseline on D1's metric in at
least the same 12 texts. If lexical passes D1 and the embedding does not beat it, **ship the
lexical instrument and stop** — the corpus gets its triage tool and the vector direction is
answered "not needed yet", which is a successful outcome, not a failure.

**D3 · The floor is measured, never chosen.** Whatever threshold the triage tool uses is the
N1 95th percentile, recorded here beside the distribution it came from.

**D4 · Failing D1 does not falsify retrieval**, only triage. Say so explicitly rather than
over-reading it — the two need different model properties, and conflating them is how one null
result kills a direction it did not test.

## Result

**Not yet measured.** No arm has been run. This section must name the model and dimension, the
measured N1 floor, the null distribution it clears, the per-text pass count out of 16, and the
lexical baseline's score — or it is not a result.
