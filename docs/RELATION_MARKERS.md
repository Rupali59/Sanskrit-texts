# Relational markers — the predicate vocabulary of jyotiṣa śāstra

**Curated. `scripts/relation_markers.py` reads this file and measures it; it never writes it.**
Same split as `docs/INVENTORY.md` ↔ `check_inventory.py`.

## Why these come before entity names

An entity model alone cannot represent a verse. `(Mars, 4th)` is two nouns; `(Mars, स्थित, 4th)`
is a claim. And the relational vocabulary is **an order of magnitude cheaper to capture**: one
graha takes ~857 surface forms, while **54 markers cover 74.3% of BPHS's 3,937 verses**.

Measured 2026-09-14 over BPHS. Regenerate with
`python3 scripts/relation_markers.py --text bphs`.

## Coverage

| concept | verses | % | markers |
|---|---:|---:|---|
| POSITION | 1638 | 41.6% | `स्थित` `स्थ` `गत` `गे` `संस्थ` `वर्ती` `आश्रित` |
| LORDSHIP | 938 | 23.8% | `ेश` `ाधिप` `ाधीश` `नाथ` `पति` `ेश्वर` |
| CONJUNCTION | 846 | 21.5% | `युत` `युक्त` `संयुत` `सहित` `समन्वित` `सम्बन्ध` |
| POLARITY | 763 | 19.4% | `शुभ` `पाप` `सौम्य` `क्रूर` |
| MODALITY | 610 | 15.5% | `यदि` `चेत्` `तदा` `स्यात्` `भवेत्` |
| DIGNITY | 488 | 12.4% | `स्वोच्च` `उच्च` `नीच` `तुङ्ग` `स्वक्षेत्र` `स्वगृह` `मूलत्रिकोण` `मित्र` `शत्रु` |
| HOUSE_GROUP | 302 | 7.7% | `केन्द्र` `त्रिकोण` `उपचय` `अपोक्लिम` `पणफर` `दुःस्थान` |
| STATE | 262 | 6.7% | `अस्त` `बल` `निर्बल` `बली` `दीप्त` `मुदित` |
| ASPECT | 264 | 6.7% | `दृष्ट` `पश्य` `वीक्ष` `निरीक्ष` `अवलोक` |
| **any marker** | **2927** | **74.3%** | **54 markers** |

**`HOUSE_GROUP` is why a `(graha, bhāva)` model is insufficient.** 7.7% of verses speak of
*kendras* (1/4/7/10) and *trikoṇas* (1/5/9) as groups — *"Jupiter in a kendra"* has no
representation in a coordinate model at all.

## REJECTED markers, and why — the load-bearing half of this file

Each was measured, inspected in the surface string, and dropped. **An inflated 86.7% became an
honest 73.5% by removing three.**

| rejected | looked like | actually matches |
|---|---|---|
| **`प्`** | the `-प` lord suffix (`लग्नप`) | **1,887 tokens, 1,132 distinct, essentially none lordship**: `विप्र` (brahmin, 81), `प्रजायते` (is born, 44), `सप्तमे` (seventh, 41), `प्रोक्तं`. The lord suffix is **word-final `प`**, never `प्` anywhere |
| **`सम`** | DIGNITY (neutral/equal) | `सम्प्रवक्ष्यामि` ("I shall explain"), `समाचरेत्`, `राजसम्मानं`. The dignity sense is swamped |
| **`मन्द`** | POLARITY (slow, dull) | **It is Saturn.** `मन्दे` 42, `मन्दस्यान्तर्गते` 8, `मन्दारौ`, `मन्दसंयुक्ते`. Belongs in the entity list, not here |

## The matra lesson — `ेश`, never `ईश`

**`ईश` matches 5 verses. `ेश` matches 742.** After a consonant the lord suffix is written with the
e-matra, so `लग्नेशे` contains no `ईश` at all. Same for `ाधिप` (179) versus `अधिप` (**0**).

This is not a tuning detail — it is a **20× undercount** that would have looked like "lordship is
rare in BPHS". Any marker beginning with an independent vowel needs its matra form checked against
real text before it is trusted.

**Precision of `ेश` is 83.2%, NOT "close to perfect" — corrected 2026-09-14, same day it was
written.** The original claim came from reading the ten most frequent forms, every one of them a
genuine bhāva-lord:

```
लग्नेशे 59 · भाग्येशे 28 · धनेशे 26 · लाभेशे 26 · व्ययेशे 26
सुतेशे 22 · कर्मेशे 22 · रन्ध्रेशे 21 · सुखेशे 19 · दारेशे 19
```

The head is clean and the **tail is not**: `देश` ("country") and `क्लेश` ("affliction") both
contain the suffix. **125 of the 742 `ेश` verses — 16.8% — match nothing but those**:
`विदेशगमनं` "going abroad" (16), `विदेशे` (6), `देशे` (5), `क्लेशकरं` (5), `देशत्यागो` (5),
`स्वदेशे` (4). Inspecting the head of a distribution and generalising to the whole of it is the
same error as trusting the first ten rows of any ranked list — the exclusions below fix it, and
LORDSHIP drops from 1,043 verses to 938.

**It does still yield bhāva vocabulary for free** — `रन्ध्र` (8th), `दार` (7th), `भाग्य` (9th),
`सुत` (5th) — classical names the chapter titles do not all use.

## Exclusions — a marker minus the words that merely contain it

The script reads this table. A verse counts for a marker only if some token contains the marker
**and** contains none of its exclusions.

| marker | excluded | why |
|---|---|---|
| `ेश` | `देश` `क्लेश` | "country" and "affliction", not lordship — 16.8% of raw `ेश` hits |
| `बल` | `बलि` | `बलि` is an offering / the demon Bali, not strength — 17 verses |
| `गे` | `=योगे` `=तुङ्गे` `=मृगे` `=भागे` `=मार्गे` `=रोगे` `=त्यागे` `=भङ्गे` | `X-गे` is "gone to X", the commonest positional form (`लग्नगे` 19, `लाभगे` 33, `धनगे`, `पञ्चमगे`). These are words whose OWN stem ends in ग. **Anchored (`=`) on purpose:** a substring exclusion for `योग` also kills `लग्नगे` (contains `नग`) and `भाग्यगे` (contains `भाग`) — the exclusion over-matching exactly as the marker did |

**Exclusion is per-token, never per-verse.** A verse reading *"the lagna-lord causes travel to a
foreign country"* contains both `लग्नेशे` and `विदेशगमनं`; it is a true LORDSHIP hit and must stay
one. Dropping the whole verse because one token is excluded would trade a false positive for a
false negative and report the trade as an improvement.

## Known imprecision, stated rather than hidden

- **`गत` and `स्थ` are substrings of much else.** `गत`'s frequent matches include `सूक्ष्मगते`,
  `प्राणगते` and — usefully — `X-स्यान्तर्गते`, the formula that opens each antardaśā run. That
  last is a *feature*: it marks the daśā construction.
- **`बल` collides with `बल` in compounds meaning "strength of"** and with `निर्बल` (weak), which
  is listed separately and would double-count if both fire.
- **`पाप` (malefic) and `चाप` (bow / Sagittarius) both end in `-आप`** — a word-final `-प` rule
  catches `पापे` (23) and `चापे` (20) as false lordship. This is why bare `-प` is not in the set.
- **These markers are morphological, not semantic.** `दृष्ट` says an aspect is asserted; it does
  not say *by whom* or *upon what*. Pairing marker to arguments is the reading layer, not this one.

## What to do when the ledger surfaces a new one

`स्वोच्चे` (80 occurrences, "in its own exaltation") was **not** in the original 31 and was found
by `docs/TERM_LEDGER.md` on its first run. That is the intended loop: the ledger records what the
matcher did not recognise, a human reads the high-count entries, and real markers land here.

Add the marker, re-run `scripts/relation_markers.py`, and record the coverage delta in this file.
**Never add a marker without inspecting what it matches in the surface string** — three of the
first sixty failed exactly that test.

## The roots file is derived, and `.gitignore` keeps it that way

`scripts/known/relation_markers.txt` is **generated, untracked, and must be regenerated
before the ledger run that consumes it** — `.gitignore:32` is `*.txt`, which is the rule
keeping this repo to `.json` plus `docs/` prose. A fresh clone has this table and the script
but not the file, so the ledger loop is two commands, never one:

```sh
python3 scripts/relation_markers.py --roots > scripts/known/relation_markers.txt
python3 scripts/term_ledger.py --text bphs --known scripts/known/relation_markers.txt
```

Stating it because the alternative was worse: `docs/TERM_LEDGER.md`'s own regenerate line
names that path, and a path that exists on the author's disk and in no clone is the failure
mode `rule:delegation-criteria` §5 describes — the reader blames the tooling rather than
their own position. Measured effect of the second command: **3,076 unrecognised terms → 2,466**.
