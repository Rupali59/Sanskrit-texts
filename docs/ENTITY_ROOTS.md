# Entity roots — the nouns of jyotiṣa śāstra

**Curated. `scripts/entity_roots.py` reads this file and measures it; it never writes it.**
Same split as `docs/INVENTORY.md` ↔ `check_inventory.py` and `docs/RELATION_MARKERS.md`.

Step 1 of the feature-extraction plan. Relations came first and are in
`docs/RELATION_MARKERS.md`; the reason for that order is recorded in `DECISIONS.md`
2026-09-14 — a relation is what makes a verse a proposition, and relations are an order of
magnitude cheaper.

**Harvested from the corpus, not authored from a lexicon.** The direction is load-bearing:
`astroacharya` builds *from* this corpus, so defining the corpus's vocabulary by what a
downstream consumer happens to model would invert the dependency. The bhāva names below came
out of the text itself — every stem preceding a lord-suffix (`X-ेश`, `X-ाधिप`) is a bhāva or
rāśi name by construction, which is how `रन्ध्र`, `दार`, `द्यून` and `मारक` were found.

Measured 2026-09-14 over BPHS's 3,937 verses. Regenerate: `python3 scripts/entity_roots.py`.

## Coverage

| entity | verses | % | roots |
|---|---:|---:|---:|
| GRAHA | 1328 | 33.7% | 34 |
| BHAVA | 1187 | 30.1% | 28 |
| DASHA | 537 | 13.6% | 8 |
| YOGA | 369 | 9.4% | 6 |
| RASHI | 285 | 7.2% | 12 |
| VARGA | 178 | 4.5% | 11 |
| **any entity** | **2749** | **69.8%** | **99** |

With the 53 relational markers, **94.5% of BPHS verses carry at least one feature**, and
**62.5% carry both an entity and a relation** — which is the number that matters, because that
is the share of the book stating a proposition the feature layer can represent.

## Roots

| entity | roots |
|---|---|
| GRAHA · sun | `सूर्य` `रवि` `भास्कर` `भानु` |
| GRAHA · moon | `चन्द्र` `शशि` `विधु` `इन्दु` `सोम` `हिमांशु` |
| GRAHA · mars | `कुज` `भौम` `मङ्गल` `अङ्गारक` `रुधिर` |
| GRAHA · mercury | `बुध` |
| GRAHA · jupiter | `जीव` `बृहस्पति` `देवेज्य` `गुरु` |
| GRAHA · venus | `शुक्र` `भृगु` `भार्गव` |
| GRAHA · saturn | `शनि` `मन्द` `सूर्यज` `अर्कज` `छायासुत` |
| GRAHA · rahu | `राहु` `राहो` `स्वर्भानु` |
| GRAHA · ketu | `केतु` `केतो` `शिखि` |
| BHAVA | `लग्न` `धन` `सहज` `भ्रातृ` `सुख` `वाहन` `मातृ` `सुत` `पुत्र` `पञ्चम` `षष्ठ` `रिपु` `अरि` `दार` `द्यून` `जाया` `सप्तम` `रन्ध्र` `अष्टम` `भाग्य` `धर्म` `पितृ` `कर्म` `राज्य` `लाभ` `व्यय` `मारक` `भाव` |
| RASHI | `मेष` `वृष` `मिथुन` `कर्क` `सिंह` `कन्या` `तुला` `वृश्चिक` `धनु` `मकर` `कुम्भ` `मीन` |
| VARGA | `अंश` `वर्ग` `होरा` `द्रेष्काण` `नवांश` `सप्तांश` `दशांश` `षष्ट्यंश` `त्रिंशांश` `द्वादशांश` `दृकाण` |
| DASHA | `दशा` `दाय` `विंशोत्तर` `अष्टोत्तर` `कालचक्र` `योगिनी` `प्रत्यन्तर` `अन्तर्गत` |
| YOGA | `योग` `राजयोग` `धनयोग` `नाभस` `दोष` `अरिष्ट` |

**`दाय` is the surprise, at 183 verses.** `दायेश` — "lord of the daśā portion" — is the single
most frequent lord-compound after `लग्न`, and no hand-written daśā list would have included it.
It is the clearest evidence for harvesting rather than authoring.

## BHAVA is counted STRICTLY, and the loose count is twice as large

**A bhāva name and its phala are the same word in jyotiṣa** — the 2nd house *is* dhana. So
`धनं लभते` ("obtains wealth") and `धनेशे` ("the 2nd lord") share a root while saying different
kinds of thing.

| counted as | verses | % |
|---|---:|---:|
| loose — the root anywhere | 2494 | 63.3% |
| **strict — the root carries a lord-suffix, a locative `-े`, or a position marker** | **1187** | **30.1%** |

The 1,307-verse gap is verses where the word is the **result**, not the house. The table above
reports strict. Reporting loose would have doubled BHAVA and pushed "any entity" from 69.8% to
84.5% — a number that is true of *bhāva vocabulary* and false of *bhāva discussion*
(`rule:discernment-checks` §5: state what the measurement is over).

## NAKSHATRA cannot be built from this text — and that is a finding, not a gap in the list

**20 of 3,937 verses — 0.5% — name any of the 27.** Eight occur **zero** times: `भरणी`,
`मृगशिर`, `आर्द्रा`, `पुनर्वसु`, `स्वाती`, `अनुराधा`, `धनिष्ठा`, `शतभिष`. The two chapters
whose titles mention nakṣatras (ch48 `विशेषनक्षत्रदशाफल`, ch89 `एक नक्षत्र जातशान्ति`)
contribute none — they discuss nakṣatra-daśā and śānti without naming individual asterisms.

Worse, the apparent hits are almost all false: `हस्त` scores 12 on `ग्रहस्तिष्ठेत्`
(graha+tiṣṭhet), `श्रवण` on `पुराणश्रवणादिकम्` ("listening to Purāṇas"), `चित्रा` on
`विचित्राम्बर` ("variegated garments"), and `मूल`'s 47 are overwhelmingly `मूलत्रिकोणे` — the
DIGNITY marker from `RELATION_MARKERS.md`, not the asterism.

**So a nakṣatra root list must come from a different text** — a muhūrta or jātaka work that
enumerates them. Building one from BPHS would produce a list validated against 20 verses, and
`मूल`/`हस्त` would ship as confident false positives.

## REJECTED roots — the negative list, and the load-bearing half of this file

Each was measured, its surface forms inspected, and dropped. **This is the list the plan
called for**, and every entry on it was predicted as a hazard before being confirmed as one.

| rejected | for | actually matches |
|---|---|---|
| **`ज्ञ`** | Mercury | **535 tokens, overwhelmingly not Mercury**: `ज्ञेयं` (58), `ज्ञेया` (36), `विज्ञेया` (15) — "should be known". The single worst candidate in the corpus |
| **`तम`** | Rāhu | **470 tokens**: `द्विजोत्तम` (58), `द्विजसत्तम` (49), and **`सप्तमे` (41) — "in the seventh"**. A superlative suffix, not darkness |
| **`सित`** | Venus | `कुत्सितान्नं` "bad food". The plan's predicted trap, confirmed |
| **`अर्क`** | Sun | 11 tokens and it collides with `अर्कज`/`अर्कि` — **Saturn**. `अर्कज` is kept for Saturn; bare `अर्क` is not kept for the Sun |
| **`वक्र`** | Mars | In BPHS it means **retrograde**, plus `वक्रमूर्धजः` "curly-haired". 17 tokens, mostly not Mars |
| **`हरि`** | Leo | `हरियोगः`, `हरिणांको`, `हरिश्चन्द्रो` — 8 tokens, almost none the rāśi |
| **`अज`** | Aries | 3 tokens, one of them `अज्ञानेन` "through ignorance" |
| **`कुलीर`** | Cancer | 6 tokens, 3 genuine; `शष्कुलीरहितौ` is a bad split. Too thin to be worth the risk |
| **`क्ल`** | — | Harvest artefact: `क्ल`+`ेश` = **`क्लेश` "affliction"**, 20 tokens |
| **`विद`** · **`स्वद`** | — | Harvest artefacts: **`विदेशगमनं` "going abroad" (17)**, `स्वदेशे` "in one's own country" |
| **`धर`** · **`सेन`** | — | `धराधिप` "king", `सेनाधीश` "army commander" — real compounds, but phala, not entities |
| **`मूल`** · **`हस्त`** · **`श्रवण`** | nakṣatras | See above — `मूलत्रिकोण`, `ग्रहस्तिष्ठेत्`, `पुराणश्रवण` |

## Exclusions — a root minus the words that merely contain it

Applied per token, never per verse, for the reason given in `RELATION_MARKERS.md` §Exclusions.

| root | excluded | why |
|---|---|---|
| `धन` | `बन्धन` | "bondage" — `ब+न्+धन` |
| `भाग्य` | `सौभाग्य` | "good fortune", not the 9th house |
| `मकर` | `कर्म` `आराम` | `धर्मकर्मरहितो`, `नीचकर्मकरो`, `आरामकरणे` — 6 of 24 raw hits |
| `सिंह` | `सिंहासन` | the lion **throne** — a phala, 8 of 66 |
| `वृश्चिक` | `सर्पवृश्चिक` | literal scorpions, in a fear-of-snakes phala |
| `मेष` | `युग्मेष` `विषमेष` `समेष` | "even/odd" — the plan predicted this; it is real but only 3% |
| `गुरु` | `देवतागुरु` `गुरुदार` | the teacher, and the teacher's wife |
| `भानु` | `भानुनन्दन` `भानुज` `भानुसुत` | "son of the Sun" = **Saturn** |
| `सोम` | `सोमसुत` `सौम्य` | "son of the Moon" = **Mercury** |
| `भौम` | `सार्वभौम` | "emperor" |
| `मन्द` | `मन्दिर` `मन्दाकिन` | temple, and the Ganges |
| `केतु` | `केतुमाल` | a region name |
| `अरि` | `अरिष्ट` `चारि` | `अरिष्ट` is its own YOGA root |
| `धर्म` | `अधर्म` | the negation is not the 9th house |
| `योग` | `योगिनी` | `योगिनी` is a **daśā** system and is already a DASHA root — counting it as a yoga double-counts one concept under two types |

**The `X-सुत`/`X-ज` pattern is the sharpest of these: a graha's name inside a patronymic names
a DIFFERENT graha.** `भानुज` and `सूर्यज` are Saturn; `सोमसुत` is Mercury. A root list without
these exclusions attributes Saturn's verses to the Sun.

## Open, and stated rather than hidden

- **`दोष` is 82 verses but 45 of them are `तद्दोषपरिहारार्थं`** — "for the removal of that
  defect", a remedial formula. Kept in YOGA because it is genuinely dosha-related, but it is
  one phrase, not 82 independent mentions.
- **`अंश` at 7 verses is far too low** for a corpus that discusses vargas constantly; the
  varga vocabulary is mostly *compounded* (`नवांशके`, `त्रिंशांशके`, `मीनांशे`), so the bare
  root under-counts and the per-varga roots carry the weight.
- **A lead worth following: ch61 labels its grahas inline where ch52–60 do not.**
  `प्रत्यन्तर` yields 26 graha-bearing compounds across 8 grahas — `कुजप्रत्यन्तरे` (7),
  `बुधप्रत्यन्तरे` (4), `चन्द्रप्रत्यन्तरे` (3). That is an *evidence-bearing* daśā label,
  unlike the positional inference that failed for ch52–60 (`DECISIONS.md` 2026-09-14). ch62
  (`सूक्ष्मान्तर्दशा`) has exactly one and is not tractable this way.
- **No precision figure is claimed per root.** Precision was estimated by inspecting surface
  forms, which is how every rejection above was made — but an honest per-root precision needs
  a human reading a stratified sample, and the corpus has no oracle that can stand in for one.
  The last thing that claimed to be one measured agreement conditional on agreement.

## Chains — and the first non-circular oracle this project has had

A chain is entity → relation → entity: `लग्नेशे चतुर्थे`, "the lagna-lord in the 4th". It is
what a *proposition* looks like in this corpus, and it is the thing the feature layer exists to
capture.

| | verses | % |
|---|---:|---:|
| ≥2 entities | 1164 | 29.6% |
| **≥2 entities AND a relation — a chain** | **867** | **22.0%** |

**The structural finding: the chain is a COMPOUND, not a phrase.** 1,467 tokens carry an entity
and a relation *in the same word* — `लग्नेशे` is BHAVA+LORDSHIP in one token, `धनेशे` in
another. Sandhi fuses the relation onto its argument. **So word-level matching already captures
chains, and no syntactic parse is needed** — which is why this is affordable at all, and why the
segmenter the earlier plan wanted was never on the critical path.

Most common shapes, first three links:

```
 47  BHAVA+LORD → BHAVA+POSITION              the canonical jyotisa statement
 26  BHAVA+LORD → BHAVA+POSITION → BHAVA+LORD
 26  BHAVA+LORD → BHAVA+POSITION → CONJ
 22  GRAHA+POSITION → GRAHA → GROUP
 15  GRAHA+POSITION → GRAHA → DIGNITY
```

**213 concrete `lord(X) in Y` propositions extract across 152 distinct pairs** — e.g.
`lord(पुत्र) in लग्न` ×8, `lord(व्यय) in लग्न` ×6, `lord(धन) in लाभ` ×5.

### The validation, and why it is not circular

BPHS ch12–23 treat the twelve bhāvas in order, so **ch12+k is the (k+1)th house**. That number
is *external to the extraction* — nothing about a Devanāgarī compound knows which chapter it
sits in. So asking "is the most-named lord in chapter N the lord of chapter N's own house?" is a
real test, unlike the two circular oracles this project has already discarded (`DECISIONS.md`
2026-09-14 ×2).

| | result |
|---|---|
| raw | **10 of 12 chapters** |
| excluding the lagna-lord as the universal reference | **12 of 12** |

```
12->1  13->2  14->3  15->4  16->5  17->6  18->7  19->8  20->9  21->10  22->11  23->12
```

**The lagna-lord exclusion was added AFTER seeing the two misses, and that is stated rather than
hidden.** In ch17 (6th) and ch19 (8th) the lagna-lord outranks the chapter's own lord, because
the lagna is the reference point every chapter measures from — a property of the text, not an
extraction error. It is one rule, principled, and applied uniformly; but a post-hoc rule that
takes 10/12 to 12/12 is a weaker claim than one fixed in advance, and **10 of 12 is the figure
to quote if only one is quoted.**

This is the closest thing to a gold standard the corpus has yielded. It does not measure
per-root precision — it measures whether the *chain extraction* recovers a structure the text's
own organisation independently asserts. Those are different claims (`rule:discernment-checks`
§5), and only the second is supported here.

## Cross-checked against astroacharya — as a validator, never as a source

The direction stays fixed: `astroacharya` builds **from** this corpus, so its `seeds/` cannot
define the corpus's vocabulary. But two lists built independently disagreeing **is** evidence,
and this one produced three findings — two about this list, one about astroacharya's.

astroacharya carries exactly **one name per entity** (`nameHi`), no synonyms.

| | astroacharya | this list | ratio |
|---|---:|---:|---:|
| GRAHA — names/roots | 9 | 34 | |
| GRAHA — BPHS verses matched | 797 | **1341** | **1.7×** |
| RASHI — names/roots | 12 | 12 | |
| RASHI — BPHS verses matched | 292 | 304 | 1.0× |

**The synonym tail is worth 544 graha verses — 40% more of the book — and it is worth nothing
at all for rāśis.** Rāśi names are stable single words (`मेष`, `कर्क`), so a one-name list loses
nothing; graha names are not, so it loses two fifths. That asymmetry is why "add synonyms"
is the right effort for grahas and wasted effort for rāśis.

### `मंगल` vs `मङ्गल` — one name, and it is a real join defect

astroacharya writes `मंगल` with **ANUSVARA**; BPHS writes `मङ्गल` with **NGA + VIRAMA**. They
are different strings. In BPHS the anusvāra form appears in **2** verses and the conjunct form
in **15**, so any join between astroacharya's entity names and this corpus on the Devanāgarī
string silently under-matches Mars by ~87%.

**Checked systematically across all 60 graha / rāśi / nakṣatra / bhāva names: `मंगल` is the only
one affected.** It is a single defect, not a class — stated that way rather than generalised
into an encoding-normalisation project the evidence does not support.

### astroacharya's 1st-house name is the one BPHS does not use

`seeds/bhavas.json` calls the 1st house **`तनु भाव`**. In BPHS, `तनु` occurs **0 times in
ch12 — the 1st-house chapter** — and its 34 corpus-wide hits are overwhelmingly `मध्यतनुर्`
("middling body") and `वृत्ततनुर्` ("round body"): phala describing the physique, not the
house. BPHS says **`लग्न`**, 498 verses, 9 of them in ch12.

`तनु` is a correct classical name and is not wrong in astroacharya. It is simply the wrong
**key** for reaching this corpus, which is exactly the kind of thing only a cross-check
surfaces — neither list is defective on its own terms.
