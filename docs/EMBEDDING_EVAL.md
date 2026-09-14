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

**BOTH ARMS RUN 2026-09-14. Lexical D1 = 2 of 16. Embedding D1 = 5 of 16, and 3 of those 5 are
single-chapter texts — 2 of 13 among texts with real chapter structure. Both FAIL the ≥12 bar.**

**Verdict: embedding-based triage does not work on this corpus, and a different model will not
fix it** — the failure is structural, not marginal. Per **D4** this falsifies *triage* and says
nothing about *retrieval*, where the measured AUC of 0.870 is encouraging and a different bar
applies.

**Goal 3 stays OPEN**, and the reason is worth being exact about: the *measurement* it asks for
is now done and recorded — that half is discharged. What is not done is the other half, "the
model **serving retrieval** was chosen on evidence". Nothing serves retrieval yet. **The
measurement having a negative answer is a result, not a failure to measure.**

### Lexical baseline — D1: **2 of 16. FAIL** (bar: ≥12 of 16)

Instrument: Devanāgarī → IAST (`indic-transliteration` 2.3.82, python3.9), NFKD-normalised with
combining marks stripped, **Dice coefficient over character 3-grams** against lowercased English.
The Sanskrit side is held fixed across true and null pairs, so verse-length effects cancel.

**The N1 null is exhaustive — all 2,410,736 within-chapter pairs, no sampling.** An earlier
sampled version returned 1/16 and 2/16 on different seeds; the two sub-50-verse texts flip on
sampling noise, which is why the deciding statistic enumerates.

| | result |
|---|---|
| **D1 (N1, within-chapter)** | **2 of 16 — FAIL.** Passes: `muhurta_chintamani` (206 verses), `yajusha_jyotisham` (45 verses, margin 0.1262 vs 0.1260 — too thin to lean on) |
| N2 (within-text) | 1 of 16 |
| N3 (global) | 4 of 16 |
| Mean AUC | **≈ 0.64** — real signal, about a coin weighted 64/36 |
| Median true > median null | **15 of 16** texts |
| Robustness | Jaccard/3-gram **1/16**; Dice/4-gram **4/16**. Not an artefact of the measure |

**Harness validated** (`rule:discernment-checks` §1 — the code path must be able to report a
pass). The identical script with the Sanskrit side replaced by the English itself — an oracle
whose true pair scores exactly 1.0 — returns **15 of 16, PASS**. It can report a pass. It did not
here.

**Population:** 16,882 → **16,668** surviving after exclusions (157 shared-English, 74 under-40,
13 marker strings — the marker class is a strict subset of the length class, so it adds nothing);
6 further unscorable (`text` has zero 3-grams) reported as unscorable, never as a zero; 1
N1-ineligible (sole verse in its chapter).

*The protocol predicted 11 markers, the run measured 13. Reconciled: 11 is the subset that are
**also** shared-English duplicates, while the "5 distinct strings" was over the full 13 — the two
halves of that row came from two different populations, the same per-string-vs-per-verse split
already flagged for 97 vs 157. Surviving n is 16,668 under either reading.*

### What this decides, and what it does not

**D2's cheap exit does NOT fire.** The lexical baseline is not a free triage tool, so the corpus
does not get its triage instrument for nothing — and **D2 stays unanswered**, because it compares
embeddings *to* this baseline and there is no embedding arm yet.

**Per D4, stated explicitly: this falsifies lexical TRIAGE and nothing about retrieval**, in
either direction, and says nothing about embeddings.

**Why the signal that exists is the wrong signal:** N1 p95 > N3 p95 in most texts — within-chapter
confusion is *harder* than global. Where character overlap works at all it is matching retained
Sanskrit technical terms and proper nouns carried untranslated into the English, and those are
exactly the tokens held constant across a chapter. It cannot do the operational job by
construction.

**The per-text N1 95th percentiles are now the measured floors an embedding arm must beat.** D3's
triage floor is read off the embedding arm's N1 distribution, never off this one.

### Blocking defect found by this arm — fix before any further arm runs

**`phaladeepika`: 178 of 851 translated verses (20.9%) carry a template stub, not a translation.**
`Chapter 21, Shloka 11 - Description of the subtle effects of planetary sub-sub-periods…`,
incrementing only the verse number. All `status: translated`, all over 40 characters, none an
exact-duplicate string — **so every one survives all three of this protocol's exclusions.**

**Consequence — CORRECTED 2026-09-14 by the embedding arm.** This originally read *"`phaladeepika`
cannot pass D1 for ANY instrument… the effective denominator is 15, not 16."* **That is a property
of the LEXICAL instrument, not of the corpus.** Under Dice-3-gram the 178 stubs score ≈1.0 against
each other, putting the oracle p95 at 1.0000; under cosine they score **0.95–0.985**, because an
embedding does not treat two near-identical strings as identical. The embedding oracle returns
**16 of 16**, and `phaladeepika`'s oracle p95 there is **0.9638**. **Do not carry "denominator 15"
forward unqualified.** The 178 stubs still do real damage — `phaladeepika` has the worst AUC
(0.672) and the worst margin (−29.6%) of any text in the embedding arm — but they bar it from
passing only under a character-overlap measure.

**Also: 18 `minaraja` verses have a `text` field containing no Devanāgarī at all** (runs of
`..........`). **The exclusions clean the English side only** — they need a Devanāgarī-side rule
and a near-duplicate (not exact-string) rule.

### Embedding arm — `text-embedding-3-large`, run 2026-09-14

**Pinned:** `text-embedding-3-large`, **3072 dimensions**, OpenAI `/v1/embeddings`, no dimension
reduction. L2-normalised once; cosine. Both sides verbatim — no preprocessing — so verse-length
effects are held as the lexical arm held them.

**Cost: $0.349.** 33,308 unique strings, 174 batched requests, 2,685,497 tokens. Cached per
batch; a retry re-spends nothing.

**Read from `git archive HEAD`, not the working tree** — a translation job had left 7 files
unreadable there. All 66 parsed from HEAD. Population reproduces the lexical arm exactly:
**16,668** surviving (157 / 13 / 74 excluded), 16 texts, **0 unscorable**.

**N1 exhaustive: 2,411,676 pairs** — 940 more than the lexical arm, reconciled: that arm dropped
6 verses it could not 3-gram (5 `minaraja` verses whose `text` is `..........`), removing their
chapters' pairs. Embeddings score those.

> ## D1 — **5 of 16. FAIL** (bar ≥12)
>
> **And 3 of the 5 passes are SINGLE-CHAPTER texts** — `saravali` (1 ch), `yajusha_jyotisham`
> (1 ch), `arch_jyotisham` (1 ch) — where the within-chapter null is degenerate and collapses
> into the global one. **Among the 13 texts with real chapter structure: 2 of 13**
> (`brihat_samhita`, 106 chapters; `bhrigu_sutram`, 8). Verified independently. **The headline 5
> is flattered by corpus structure.**

| | embedding | lexical |
|---|---|---|
| D1 | **5 of 16** (2 of 13 multi-chapter) | 2 of 16 |
| Mean AUC vs N1 | **0.870** | 0.673 |
| Median true > median null | **16 of 16** | 15 of 16 |
| N2 | 8 of 13 evaluable (3 not computable — single chapter) | 1 of 16 |
| N3 | 11 of 16 | 4 of 16 |

**The two largest texts fail worst.** `minaraja` (4,012) −15.1% and `bphs` (3,816) −12.9% —
together 47% of the population. A triage queue that systematically under-ranks those two is worse
than no queue, which is what the ≥12 bar exists to catch.

**Harness validated three ways** (`rule:discernment-checks` §1): oracle (Devanāgarī replaced by
the English itself) **16 of 16 PASS**; negative control (English deranged within chapter, two
seeds) **0 of 16** both times; real arm 5 of 16. It can report a pass and it can report a floor.

**D2 cannot be satisfied as written.** It requires beating lexical "in at least the same 12
texts"; neither instrument reaches 12, so the clause is unreachable. Scale-free, the embedding
beats lexical in **13 of 16** — but **the pass-sets are not nested**: the embedding *loses*
`muhurta_chintamani`, which lexical passes. Better nearly everywhere, and still not containing
the baseline.

**D3 — there is no single corpus-wide floor.** The per-text N1 p95 ranges **0.2996–0.4125**, a
spread of 0.11. Any triage threshold would have to be per text. That is itself a result.

**Mismatch logged, not resolved.** An independent lexical re-run during this arm measured **3 of
16** against the committed **2 of 16**, diverging on `arch_jyotisham` (0.1008 vs p95 0.0889 — not
a thin margin), reproduced by a second implementation. Attributed to normalisation detail between
two implementations. **The committed 2 of 16 stands as the pre-registered baseline of record.**

### Verdict — embedding triage does not work here, and a different model will not fix it

**Per D4: this falsifies embedding-based TRIAGE and nothing about retrieval**, in either
direction.

The signal is real and large — AUC 0.870 means a true pair beats a random within-chapter false
pair about 8.4 times in 10. **It fails anyway, and structurally rather than marginally.** D1 asks
the *median* true pair to clear the *95th percentile* of the null, which needs something near AUC
0.98. The distributions overlap because **a chapter is 40 verses on one topic in one translator's
register, so a wrong pairing inside it is genuinely similar text.** The model is right that those
verses resemble each other. D1 is asking it to be wrong about that.

**What remains open is retrieval**, where AUC 0.87 is encouraging and a different bar applies.

**Order of work:** fix the 178 stubs → extend the exclusions to the Devanāgarī side and to
near-duplicates → then run the embedding arms against the table above.
