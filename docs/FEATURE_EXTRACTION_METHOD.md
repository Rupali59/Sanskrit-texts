# Feature extraction over a Sanskrit text — the method

**How to build a feature layer over a text in this corpus.** Written 2026-09-14/15 after
doing it once, end to end, on BPHS. Everything here is either a measured number from that
run or a trap that run walked into.

**Read this before starting on a second text.** The BPHS layer took a day and roughly half
of that was re-deriving things this file now states.

---

## 0 · The rule that is not negotiable

**Vocabulary comes from the text. A lexicon proposes candidates; only the corpus accepts
them.**

`astroacharya` builds *from* this corpus, so defining the corpus's vocabulary by what a
downstream consumer models inverts the dependency and makes any term the consumer does not
happen to model invisible in its own source.

This applies to *every* external list, including good ones:

| source | proposed | corpus verdict |
|---|---|---|
| `docs/BPHS_Master_Lexicon.md` (in-repo, hand-curated) | `कवि` for Venus | 22 verses of `कविर्वाग्मी` "poet" — **rejected** |
| same | `छायासुत` for Saturn | **0 occurrences** — the text says `छायासूनु` |
| `astroacharya/seeds/bhavas.json` | `तनु` for the 1st house | **0 occurrences in ch12, its own chapter** — the text says `लग्न` |

A lexicon is still worth consulting — the same Master Lexicon supplied six roots the harvest
missed. Consult it **after** harvesting, as a source of candidates, never as the authority.

---

## 1 · Triage — is this text a candidate at all? (minutes)

Before any curation, answer three questions with one script each. **A "no" here saves a day.**

```sh
python3 scripts/term_ledger.py --text <text_id>      # what vocabulary does it even have?
python3 scripts/relation_markers.py --text <text_id> # do the existing markers fire?
```

| check | BPHS | what a bad answer looks like |
|---|---|---|
| relational markers fire | **74.3%** of verses | under ~30% — the text is not stating conditions |
| the text has an internal ordering to validate against | ch12–23 are the 12 bhāvas in order | none — you will have no oracle (see §6) |
| the entity type you want is actually present | nakṣatras: **0.5%**, 8 of 27 absent | this is a **finding**, not a gap to fill |

**The nakṣatra result is the model for a clean "no".** BPHS names any of the 27 in 20 of 3,937
verses; `मूल`'s 47 apparent hits are `मूलत्रिकोणे`, a dignity marker. Building a nakṣatra list
from BPHS would have validated against 20 verses and shipped `मूल`/`हस्त` as confident false
positives. **Record the absence and go to a different text.**

---

## 2 · Relations before entities — always, and the ratio is why

**Do relations first.** One graha takes ~857 surface forms; **54 relational markers cover
74.3% of BPHS**. Relations are an order of magnitude cheaper *and* carry more meaning —
`(Mars, 4th)` is two nouns, `(Mars, स्थित, 4th)` is a claim.

The nine concepts, which are jyotiṣa-general and should transfer to any phala text:

```
POSITION  LORDSHIP  CONJUNCTION  POLARITY  MODALITY
DIGNITY   HOUSE_GROUP  STATE  ASPECT
```

**HOUSE_GROUP is the one people leave out.** 7.7% of verses speak of *kendras* and *trikoṇas*
as groups, so *"Jupiter in a kendra"* has no representation in a `(graha, bhāva)` coordinate
model at all.

Start from `docs/RELATION_MARKERS.md` — it is a curated list, not a BPHS-specific one, and is
the right first guess for any Hora text.

---

## 3 · Harvest entities from the text's own morphology

**Do not author a list. Find the construction that yields names.**

In jyotiṣa the construction is the lord-suffix: *whatever precedes `-ेश` / `-ाधिप` / `-ाधीश` /
`-नाथ` is a bhāva or rāśi name, by construction.*

```sh
# the harvest that produced the bhava vocabulary
python3 - <<'EOF'
import json,re,collections
# ... tokenise, then for each token find a lord-suffix and count what precedes it
EOF
```

That harvest produced `रन्ध्र` (8th), `दार` (7th), `द्यून` (7th), `मारक`, and above all
**`दाय` at 183 verses** — `दायेश`, "lord of the daśā portion", the most frequent lord-compound
after `लग्न` and on no hand-written list anywhere.

**It also produces garbage, and that is fine** — `क्ल` (from `क्लेश` "affliction"), `विद` (from
`विदेशगमनं` "going abroad"), `धर` and `सेन` (from `धराधिप` "king", `सेनाधीश` "army commander").
Inspecting and rejecting those is §4, and it is the cheap part.

**Find the equivalent construction for the text you are on.** A dharma text will have a
different one; a tantra text another. The method is "locate a productive affix and read what
attaches to it", not "use the lord-suffix".

---

## 4 · The negative list is the load-bearing half — budget for it

**Never add a root without inspecting what it matches in the surface string.** This is the
single rule that separates a working layer from a plausible one, and it cannot be automated.

Print the top surface forms per candidate and read them:

```sh
# for each candidate root: total tokens, and the most frequent forms
```

Measured rejections from BPHS, every one of which looked like a fine root:

| rejected | intended | what it actually is |
|---|---|---|
| `ज्ञ` | Mercury | **535 tokens** of `ज्ञेयं` / `विज्ञेया` "should be known" |
| `तम` | Rāhu | **470 tokens** — `द्विजोत्तम`, and **`सप्तमे` "in the seventh"** |
| `प्` | lordship | 1,132 distinct forms, ~none lordship — `विप्र`, `प्रजायते`, `सप्तमे` |
| `सित` | Venus | `कुत्सितान्नं` "bad food" |
| `वक्र` | Mars | "retrograde", and `वक्रमूर्धजः` "curly-haired" |
| `कवि` | Venus | "poet" — *proposed by a hand-curated lexicon* |

**Chapter TITLES are their own trap surface, and a short root fires on them hard.** Found
2026-09-15 while checking whether the oracle transfers — three false positives in one pass:

| title | matched | actually |
|---|---|---|
| `अष्टमोऽध्यायः` | `अष्टम` → 8th house | **"chapter eight"** — the ordinal, not a bhāva |
| `बल-साधन खण्ड` | `धन` → 2nd house | **`साधन`** "means / accomplishment" contains `धन` |
| `आयुर्दायाध्यायः` | `आय` → 11th house | **`आयुर्दाय`** "longevity allotment" contains `आय` |

Titles are short, so a single false match dominates; and they are exactly what a positional
oracle reads. **Run the negative list over titles separately from verses.**

### Two mechanisms, doing different jobs

**Longest-match** solves collisions where one root contains another. Prefer it — it needs no
list. `सोमसुत` (Mercury) beats `सोम` (Moon); `सूर्यज`/`भानुज` (Saturn) beat `सूर्य`/`भानु`.

**Exclusions** handle only what longest-match cannot: `देश` is not a longer form of `ेश`, it
merely contains it.

**Exclusions must support anchoring, and this is not optional.** A substring exclusion
over-matches exactly the way the marker it corrects did: excluding `योग` from `गे` also kills
`लग्नगे` (contains `नग`) and `भाग्यगे` (contains `भाग`). Write `=योगे` for an exact-token test.

### The patronymic trap, which is jyotiṣa-wide

**A graha's name inside a patronymic names a DIFFERENT graha.** `भानुज` and `सूर्यज` are
**Saturn**; `सोमसुत` is **Mercury**. A root list without this files Saturn's verses under the
Sun. Longest-match handles it *provided the patronymic is itself a root* — if it is only an
exclusion, the token gets tagged as nothing at all.

### The matra trap

**`ईश` matches 5 verses; `ेश` matches 742.** After a consonant the suffix carries the e-matra,
so `लग्नेशे` contains no `ईश`. Same for `अधिप` (0) versus `ाधिप` (179).

**Any root beginning with an independent vowel needs its matra form checked against real text
before it is trusted.** A 20× undercount reads as "this feature is rare in this text".

### The homonym trap — a name and its significance are the same word

In jyotiṣa the 2nd house *is* dhana, so `धनं लभते` ("obtains wealth") and `धनेशे` ("the 2nd
lord") share a root. Counting loosely doubles the number:

| | verses | % |
|---|---:|---:|
| loose — root anywhere | 2494 | 63.3% |
| **strict — root + lord-suffix, locative, or position marker** | **1246** | **31.6%** |

**Report strict.** Loose is true of *vocabulary* and false of *discussion*. And note the
strict test must accept the locative on the **compound**, not just the root — `धनगे` is
`धन`+`ग`+`े`, and checking only the character after the root missed 128 tokens.

---

## 5 · The matcher

**Maximal munch, left to right, longest root at each position, advance past it.**

Per-token "pick the longest root" is wrong: **24 BPHS tokens name more than one entity** —
`चन्द्रसूर्यग्रहे` is Moon *and* Sun, `शनिचन्द्रबुधा` is Saturn *and* Moon *and* Mercury.

**The matcher must import the curated docs' parsers, never copy the lists.** Three copies of a
vocabulary is how a rule ends up with four mutually exclusive versions of itself.

### Two rules for writing tags into the corpus

1. **Own your tags and regenerate them; never merge.** A merging tagger is not idempotent —
   a root removed from the doc leaves its output in the corpus forever, so the corpus becomes
   the union of every vocabulary ever applied. Preserve only what *another writer* owns.
   **Assert it: a second `--apply` must be a byte-level no-op.** (**G52**)
2. **Compare the KEY SET, not its size.** A pass that drops one verse and adds another
   survives a length check. (**G8**'s mirror)

### Where tags go, and the constraint nobody expects

`tags` is a flat list of strings, it is inside `_normalize_shloka`'s **12-key allowlist**, and
it is sparse-indexed in Mongo. That makes it correct for **filtering** and insufficient for
**meaning**:

> 38 `(lord_of, in_house)` pairs occur together with their reverse. `सुतेशे भाग्यगे`
> (lord of 5 in 9) and `भाग्येशो … सुतेशो` (lord of 9 in 5) produce the **same set**.
> 21% of tagged verses share their tag set with another verse.

**Encode the binding inside the tag string** — `chain:lord5_pos9` — and it ships without
touching the allowlist that is also the publication gate (**G50**). Honest result: 271 chains,
collisions 21% → 19%. **Correct where it fires; it fires on 7% of tagged verses.** A general
solution needs token-anchored spans and therefore a two-repo allowlist change — a decision to
take deliberately, not as a side effect.

---

## 6 · Validation — three layers, and only one needs a human

### Layer 1 · automatic, continuous, free

**These caught every defect in the BPHS run. None required a person.**

| check | what it catches | BPHS |
|---|---|---|
| doc↔corpus drift gate | a stated number the corpus no longer supports | caught a missing `योगिनी` exclusion |
| a root firing **zero** times | a claim that cannot fail | caught `छायासुत` |
| **collision rate** | tags that do not identify a verse | 21% — exposed the `X-गे` gap |
| idempotency (sha256 on a second `--apply`) | a merging, non-regenerating writer | caught G52 |
| trigger reachability (`--selftest`) | a documented hazard that cannot fire | caught G52's own trigger |

### Layer 2 · the internal oracle — find one, and check it is not circular

**BPHS ch12–23 treat the twelve bhāvas in order, so ch12+k is the (k+1)th house.** That number
is *external to the extraction* — nothing about a Devanāgarī compound knows its chapter — so
"is the most-named lord in chapter N the lord of chapter N's own house?" is a real test.
**10 of 12 raw; 12 of 12 excluding the lagna-lord as the universal reference (post-hoc, and
declared as post-hoc).**

**Two oracles in this project were circular and both reported ~100%:**

- an English-agreement rate that was `P(overlap | BOTH sides already agree)`, over 22.4% of the
  corpus, **excluding exactly the verses a tagger gets wrong**
- a "100% Vimśottarī agreement" whose labels were *assigned* by walking Vimśottarī order

**The test for circularity: name the fact the oracle uses, and check the extraction cannot see
it.** If the extraction could have known it, the oracle measures itself.

**This particular oracle is BPHS-ONLY — do not plan around having one.** Measured 2026-09-15:
**no other text in the corpus runs twelve consecutive bhāva chapters.** `phaladeepika` and
`brihat_jataka` organise by topic across 28 chapters; `uttara_kalamrita` by khaṇḍa;
`saravali` is a **single chapter** and so has no positional structure at all. The nearest
equivalent elsewhere is `jataka_parijata` ch13 `पञ्चमषष्ठभावफल`, which covers *two* houses in
one chapter.

So for a new text, **find its own internal ordering or accept that layer 2 is missing.**
Candidate substitutes, in descending strength:

1. **an internal ordering the text asserts itself** — chapter sequence, a declared enumeration
2. **cross-text agreement** — the same doctrine tagged alike in two texts by different authors;
   external to either text's extraction, so non-circular
3. **nothing** — say so. Layers 1 and 3 alone are a weaker but honest position

### Layer 3 · the human pass, once — then it is a regression suite forever

`scripts/spot_check.py` — stratified, deterministic, verdict column curated and surviving
regeneration; `--score` reports precision. **`unsure` is reported separately and folded into
neither numerator nor denominator**, because folding it invents a verdict the reviewer withheld.

**Split it or it stops measuring.** Tune the vocabulary against ~2/3; hold ~1/3 back and touch
it once. Tuning against the whole set rebuilds the circular oracle by hand.

---

## 7 · What generalises, and what does not

| | |
|---|---|
| **General to any text** | the method: triage → relations → harvest → negative list → matcher → three-layer validation. The traps in §4. The two write rules in §5 |
| **General to jyotiṣa** | the nine relational concepts; the patronymic trap; the homonym trap |
| **BPHS-specific and UNPROVEN elsewhere** | the 99 entity roots, every coverage number, and the chapter-position oracle |

### The relational markers DO generalise — measured 2026-09-15

Marker coverage per text, one `relation_markers.py --text <id>` each:

| jātaka genre | | | other genres | |
|---|---:|---|---|---:|
| `jataka_parijata` | **87.5%** | | `brihat_samhita` | 54.9% |
| `uttara_kalamrita` | 87.3% | | `surya_siddhanta` | 54.3% |
| `sarvartha_chintamani` | 86.7% | | `bhrigu_sutram` | 51.9% |
| `brihat_jataka` | 84.1% | | | |
| `saravali` | 82.8% | | | |
| `phaladeepika` | 82.6% | | | |
| `minaraja_yavana_jataka` | 79.9% | | | |
| `laghu_jatakam` | 79.1% | | | |
| `jataka_tattva` | 77.2% | | | |
| **`bphs`** | **74.3%** | | | |

**The nine relational concepts are general to the jātaka genre**, and the drop to ~52–55% lands
exactly on the genre boundary — Saṃhitā (encyclopedic), Siddhānta (mathematical astronomy) and
Nāḍī are stating different kinds of thing and need their own marker sets.

**BPHS scores LOWEST of the jātaka texts**, because its ch1–11 are cosmological rather than
phala. A text that is purely phala scores higher. Do not read BPHS's number as a ceiling.

**The ENTITY roots are untested elsewhere.** Only the markers have been measured across texts;
treat every number in `ENTITY_ROOTS.md` as a BPHS measurement until someone runs the same sweep
for entities.

---

## 8 · The half that is not built

**A shloka is CONDITION → RESULT, and only the condition side exists.**

The phala vocabulary — `धनं` wealth, `सुखी` happy, `रोग` disease — was treated throughout as
*noise to exclude*. It is the payload. **The 1,307-verse loose/strict gap in §4 is precisely
the predicate layer, already quantified and discarded.**

`धनं लभते` is not a failed `bhava:2`. It is a true `phala:wealth`. Building that vocabulary
uses the same harvest, the same exclusion machinery and the same validation — and it is what
turns the corpus from something you filter into something you can ask a question of.

---

## 9 · Cost, measured

| phase | effort | dominated by |
|---|---|---|
| triage | minutes | running two scripts |
| relations | ~2 h | already done once; reuse `RELATION_MARKERS.md` |
| harvest | ~1 h | finding the productive affix |
| **negative list** | **the bulk** | **a human reading surface forms — irreducible** |
| matcher | ~2 h | mostly written; reuse `tag_features.py` |
| validation instruments | ~2 h | mostly written; reuse |
| the human spot check | ~4 h | a Sanskrit reader, once per text |

**The negative list and the spot check are the only parts that do not transfer.** Everything
else in this repo is already written and takes a `--text` argument.
