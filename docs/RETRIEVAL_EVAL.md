# Retrieval evaluation — 50 frozen pairs, and what tags already answer

**Curated. `scripts/retrieval_eval.py` scores it and never writes it.** Frozen 2026-09-15,
**before any arm was scored** — the same pre-registration discipline as
`docs/EMBEDDING_EVAL.md`, and for the same reason: a bar chosen after seeing the numbers is a
check that cannot fail.

## What this answers

`EMBEDDING_EVAL.md`'s **D2** is unreachable as written (it needs an instrument to reach 12 of 16;
neither did) and its baseline is stale. This file scores its replacement:

> **D2′ · Embeddings earn their existence iff they answer queries the TAG LAYER cannot.**

Three arms, same 50 pairs, scored identically:

| arm | mechanism | needs |
|---|---|---|
| **tags** | exact filter over `tags` — `graha:saturn` + `bhava:10` | nothing; the layer exists |
| **`$text`** | keyword match over `english` | nothing |
| **embeddings** | cosine over embedded English | an API key, ~$0.10 |

**The headline number is not which arm wins. It is how many of the 50 the TAG ARM already
answers** — that is the size of the gap, and it is what decides whether a vector store is needed
at all.

## Where the questions come from

**Not invented, and deliberately not drawn from `JyotishEntity.citations`** — that is the
hand-curated table this work exists to replace, so scoring against it would be circular.

They are written from measured demand, in the querent's language:

- **`marketing-intel/docs/keyword-demand-direction.md`** — the seven demand slices and their
  consult-intent ranking. Highest intent: personal-decision muhūrta, consultation, career (slice
  6, *"partial → kundli/dasha, 10th house"*), and slice 7's difficult planets.
- **the booking `life_area` enum** (`bookings.ts`): career · relationships · money · family ·
  health · muhurta.
- **the GSC classifier buckets** (`topic-from-query.ts`): Saturn · Rahu-Ketu · Lagna ·
  **Mahadasha** · Remedies · General.

**A finding that shapes the whole exercise: the three highest-demand popular terms do not exist
in the canon.** `sade sati`, `manglik` and `kaal sarp` each return **zero** English matches
across all 3,937 BPHS verses. The *concepts* are there — `57.42` states Saturn-to-Moon affliction
without naming it — but the words a querent types are modern. **Any arm that matches strings
fails those by construction, and a compositional arm (Saturn + Moon + position) might not.**
Rows 41–45 exist to measure exactly that.

## Scoring

For each pair the arm returns a ranked list. Recorded per arm:

- **hit@1** — the gold verse is first
- **hit@5** — the gold verse is in the top five
- **miss** — not in the top five

Gold verses were found by **reading the English and confirming against the Devanāgarī**, never by
tag lookup — choosing gold with the instrument under test is how a gold set becomes a mirror.

**A caveat that must not be smoothed:** one gold verse per question understates every arm. Many
questions have several defensible answers (`24.50`, `16.5` and `30.15` all speak to children), so
hit@5 is the honest headline and hit@1 is a lower bound. Where a second verse is clearly as good
it is listed in `also`, and an arm returning it counts as a hit.

## The pairs

| # | slice | question | gold | also |
|---|---|---|---|---|
| 1 | career | what does the tenth lord in the fourth house give | `24.112` | |
| 2 | career | tenth lord with the ascendant lord and a strong Moon | `21.21` | |
| 3 | career | Saturn in the tenth with a debilitated planet | `21.16` | |
| 4 | career | which house shows profession | `7.39` | |
| 5 | career | bravery bringing wealth and victory | `47.31` | |
| 6 | money | second lord in its own sign or exalted | `13.10` | `24.16` |
| 7 | money | second lord in the eleventh, eleventh lord in the second | `13.4` | |
| 8 | money | what causes poverty from birth | `13.7` | |
| 9 | money | which yogas make a person poor | `42.1` | `37.12` |
| 10 | money | the yogas that make a person wealthy | `41.1` | |
| 11 | money | second lord in the fourth house | `24.16` | |
| 12 | money | loss of wealth through royal punishment | `13.8` | |
| 13 | relationships | seventh lord in the seventh house | `24.79` | |
| 14 | relationships | when does marriage happen with Venus exalted | `18.22` | |
| 15 | relationships | what makes the wife beautiful and virtuous | `30.15` | `33.47` |
| 16 | relationships | Sun in the seventh house and the wife | `18.7` | |
| 17 | relationships | Ketu in the seventh from Arudha | `29.24` | |
| 18 | family | tenth lord in the fourth and devotion to the mother | `24.112` | |
| 19 | family | which house shows the mother | `11.5` | |
| 20 | family | when does the father die early | `20.15` | `20.14` |
| 21 | family | father's death before the native's birth | `20.14` | |
| 22 | family | Sun afflicted between malefics and the father | `9.36` | |
| 23 | family | elder and younger siblings, which houses | `5.19` | |
| 24 | children | fifth lord in the second house | `24.50` | |
| 25 | children | fifth lord exalted with Jupiter exalted | `16.5` | |
| 26 | children | when do children live abroad | `16.18` | |
| 27 | children | Ketu in the third or eleventh and brothers | `30.36` | |
| 28 | health | what makes a person long-lived | `12.5` | `10.6` |
| 29 | health | when is leprosy indicated | `17.7` | `17.8` |
| 30 | health | white leprosy versus black leprosy | `17.8` | |
| 31 | health | ascendant lord combust or debilitated causing disease | `12.2` | |
| 32 | health | ascendant lord with malefics in the sixth eighth twelfth | `12.1` | |
| 33 | health | which house shows disease | `17.1` | |
| 34 | health | Saturn with Rahu and constant illness | `17.14` | |
| 35 | mahadasha | Venus antardaśā inside Venus mahādaśā | `60.1` | |
| 36 | mahadasha | gain of villages and land from the king in a daśā | `59.10` | |
| 37 | mahadasha | how are daśā and antardaśā results calculated | `51.3` | |
| 38 | remedies | what japa removes the doṣa of an afflicted Sun | `52.3` | |
| 39 | remedies | donating and building ponds during a good period | `56.42` | |
| 40 | remedies | untimely death and how to avert it | `52.72` | |
| 41 | **slice 7 — no canonical term** | sade sati — Saturn afflicting the Moon | `57.42` | |
| 42 | **slice 7 — no canonical term** | manglik — Mars in the seventh and marriage | `18.7` | |
| 43 | **slice 7 — no canonical term** | kaal sarp — all planets between Rahu and Ketu | — | |
| 44 | slice 7 | Rahu in the eighth house | `17.14` | |
| 45 | slice 7 | Ketu's results in a house | `29.24` | `30.36` |
| 46 | lagna | ascendant lord in a quadrant or trine | `12.5` | |
| 47 | lagna | what the ascendant shows | `11.5` | |
| 48 | general | what is a rāja yoga | `39.1` | `39.3` |
| 49 | general | what does a debilitated or combust planet give | `6.53` | `3.60` |
| 50 | general | Bhadra yoga and its results | `75.6` | |

**Row 43 has no gold and that is deliberate.** Kāla-sarpa is a modern construct; no BPHS verse
states it. An arm that confidently returns something for row 43 is **wrong**, and the scorer
counts a non-empty answer there as a **false positive**, not a miss. It is the one row that can
only be failed by over-answering.

## Result — run 2026-09-15

| arm | hit@1 | hit@5 | miss | false-positive on row 43 |
|---|---:|---:|---:|---:|
| **tags** | 2 | **11** | 38 | 1 |
| **`$text`** | 11 | **18** | 31 | 1 |
| **embed-en** — local `all-minilm` | **19** | **29** | 20 | 1 |
| **hybrid** — tag filter → embed rank | 14 | 26 | 23 | 1 |

**The embedding arm ran LOCALLY on 2026-09-15 — no API key, no cost.** `ollama` 0.34.0 was
already installed and serving; the model is `all-minilm`, 384d, **46 MB, English-only, and the
weakest option available**. A stronger model would raise these numbers, not change the ordering.

*(`bge-m3` was attempted first — 1024d and multilingual, which would have opened a Devanāgarī
arm the 2026-09-14 run could not run at all. Its 1.2 GB download died on a TLS timeout at 32 MB.
Worth retrying: the corpus is 83% untranslated, so an arm that reads the Sanskrit directly is
worth more than any English model.)*

**Harness validated both ways** (`rule:discernment-checks` §1). Oracle — each question replaced by
its own gold verse's English — **49 of 49 hit@1**. Negative control — a nonsense query — **0 of
49**. It can report a pass and it can report a floor.

### D2′ is answered: embeddings earn their existence, decisively

**29 against 11.** The weakest available local embedding model answers **29 of 49** where the tag
layer answers **11** and `$text` answers **18**. D2′ asked whether embeddings answer queries the
tag layer cannot; they answer more than twice as many.

### The hybrid LOST, which is the opposite of what was predicted

The plan stated *"the hybrid is the one the plan predicts wins"*, reasoning that a ranker facing
~332 tag-filtered candidates is doing an easier job than one facing 3,937. **It measured 26
against the plain embedding's 29.** The prediction was wrong and the reason is measurable:

> **The tag filter's recall is 71%.** Of 45 gold verses, the filter *excludes* **13** outright —
> and the ranker can never recover a verse the filter removed.

Examples of the filter throwing away the answer: *"which house shows profession"* → `bhava:10`,
*"which house shows the mother"* → `bhava:4`, *"Sun in the seventh house and the wife"* →
`{bhava:7, graha:sun}`. Each is a *reasonable* tag set that simply does not match how the gold
verse is tagged.

**The general rule this measures: a filter placed before a ranker imposes its own recall as a
hard ceiling.** 71% recall caps the hybrid at 71% no matter how good the ranker is. Precision
bought at the cost of recall is a bad trade in front of a ranker that was already handling the
unfiltered problem.

**This does not make the tag layer useless** — it makes it the wrong instrument *for this job*.
It remains exact, auditable, and the right thing for a structured filter a user asks for
explicitly (`graha:saturn` + `bhava:10`). It is not a pre-filter for free-text retrieval.

### What the earlier reasoning got right and wrong

**The tag layer answers 11 of 49 (22%).** So the gap is **large**, and on that reading embeddings
are amply justified.

**But `$text` beats tags, 18 to 11** — and the reason is the finding:

> **A tag query matches a MEDIAN of 332 verses** (max 1,620, min 49). The gold verse has to be
> ranked above ~332 equally-tagged others, and tags carry no signal to do it with.

**Tags are a filter, not a ranker.** They cut 3,937 candidates to ~332 — a 12× reduction, which
is real — and then stop. `$text` wins because English keywords carry the *specific* content
("leprosy", "poverty", "beautiful wife") that tags deliberately abstract away into `bhava:6`,
`bhava:2`, `bhava:7`.

**This does not contradict the 97.32% within-chapter separation. It corrects what that number
meant.** Separating two verses is *discrimination*; finding one among 3,937 is *retrieval*. The
tag layer is excellent at the first and weak at the second, and conflating them is what made
"tags might replace embeddings" look plausible.

### What this implies for the store

**Tags and embeddings are complementary, not competing.** The measured shape is:

| stage | instrument | evidence |
|---|---|---|
| **filter** | tags | 3,937 → ~332, exact and auditable |
| **rank** | embedding | AUC **0.870** on within-chapter pairs (`EMBEDDING_EVAL.md`) |

An embedding asked to rank 332 tag-filtered candidates is doing a far easier job than one asked
to rank 3,937 — and 0.870 was measured on the *harder* version. **The hybrid is the arm worth
running next**, and it is cheap because the filter is already built.

> **THAT PREDICTION WAS RUN AND IS FALSE. Hybrid 26, plain embedding 29.** The paragraph above is
> left standing because it was the stated reasoning and it was wrong for a reason worth keeping:
> it counted what a filter *gives* the ranker and never counted what it *takes away*. The tag
> filter's recall is **71%**, so it discards 13 of 45 gold verses before the ranker sees them. A
> filter in front of a ranker imposes its own recall as a hard ceiling.

**Revised shape, measured rather than reasoned:**

| use | instrument |
|---|---|
| free-text retrieval | **the embedding alone** — 29/49, no filter in front of it |
| an explicit structured query a user asks for (`graha:saturn` + `bhava:10`) | **tags** — exact and auditable, and the user has accepted the recall trade by asking for it |
| telling two verses apart once retrieved | **tags** — 97.32% of within-chapter pairs |

### The trap row worked, and both arms failed it

Row 43 (kāla-sarpa, no valid answer) drew a confident non-empty response from **both** arms.
Neither can say "this concept is not in this text", and a citation layer that invents a verse for
a modern construct is worse than one that returns nothing. **Any shipped surface needs an
explicit floor below which it answers nothing** — which is what `astro-studio`'s
`grounding.py` already does with its measured `FLOOR = 0.55`.

### Honest limits of this number

- **One gold verse per question understates every arm.** Several questions have multiple
  defensible answers; `also` captures some but not all. **hit@5 is the headline, hit@1 a lower
  bound.**
- **The `$text` arm is a stand-in**, keyword overlap rather than Mongo's `$text` with its
  stemming and scoring. A real `$text` would likely do better, which strengthens rather than
  weakens the conclusion.
- **The English→tag bridge is written once and generally** (see the script's header), never per
  question. 46 of 50 questions produce at least one tag from it; 4 produce none and are scored as
  "no answer", not silently dropped.
- **Both arms are BPHS-only.** Nothing here generalises to the other 65 texts.
