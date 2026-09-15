# Phala categories — the result side of a shloka

**Curated closed set. `scripts/apply_phala.py` validates against it and refuses anything not
listed here.** A closed vocabulary is the point: an open-ended labeller drifts across 3,937
verses and produces a hundred near-synonyms that no query can use.

## Why this layer is read, not matched

Every other vocabulary in this repo is matched by script, because jyotiṣa's *condition* side has
productive morphology — whatever precedes `-ेश` is a bhāva name, and 54 relational markers cover
74.3% of BPHS.

**The result side has no such handle.** Measured 2026-09-15: adjacency to a result verb
(`भवेत्` `स्यात्` `जायते` `लभते`) covers only 761 of 3,937 verses, and the adjacent tokens are
dominated by function words — `च` 50, `वा` 37, `तु` 31 — and bare subject nouns (`नरः` 25,
`जनः`). There is nothing to anchor a matcher to.

So this layer is assigned by **reading the verse**, and the categories below exist to keep that
reading consistent.

## The publication gate — why this lands in `tags_draft`

**Machine-assigned phala tags are a semantic claim, and the workspace hard rule is
*"Computation is AI-assisted; meaning is not."*** A regex tag saying "this verse contains
`धनेशे`" is computation. A read tag saying "this verse predicts wealth" is closer to meaning,
and `tags` **is** inside `_normalize_shloka`'s 12-key allowlist, so it reaches the public API.

Therefore: **read tags are written to `tags_draft`, which is NOT in that allowlist and
structurally cannot reach the API** — exactly as `english_draft` works for translations.
Verification promotes into `tags`. No new mechanism, and G50 is untouched.

## The categories

Eighteen. Chosen from the aligned English's own frequency (`wealth` 422, `happiness` 278,
`loss` 257, `fear` 188, `children` 151, `wife` 151 …) and then checked against the Devanāgarī
of a sample.

| tag | covers | Devanāgarī seen |
|---|---|---|
| `phala:wealth` | wealth, gain, prosperity, treasure | `धनलाभ` `वैभव` `धनधान्य` |
| `phala:loss` | loss, poverty, destruction of assets | `हानि` `नाश` `दारिद्र्य` |
| `phala:happiness` | happiness, comfort, ease | `सुख` `सौख्य` |
| `phala:sorrow` | grief, mental pain, anxiety | `दुःख` `शोक` `मनस्ताप` `मनोरुजा` |
| `phala:disease` | illness, fever, wounds, bodily affliction | `रोग` `ज्वर` `व्रण` `पीडा` `कास` `श्वास` |
| `phala:death` | death, mortality, killing | `मरण` `मृत्यु` `अपमृत्यु` |
| `phala:longevity` | lifespan, long or short life | `आयुस्` `दीर्घायु` `अल्पायु` |
| `phala:children` | sons, offspring, progeny | `पुत्र` `सुत` `सन्तान` |
| `phala:marriage` | wife, marriage, spouse | `विवाह` `कलत्र` `दार` `नारी` `भार्या` |
| `phala:family` | parents, siblings, relatives, separation from them | `पितृ` `मातृ` `भ्रातृ` `वियोग` `बन्धु` |
| `phala:enemies` | enemies, quarrel, hatred, litigation | `शत्रु` `कलह` `द्वेष` `विवाद` |
| `phala:danger` | fear, thieves, weapons, fire, imprisonment | `भय` `चोर` `शस्त्र` `अग्नि` `बन्धन` |
| `phala:honour` | status, royal favour, fame, respect | `सम्मान` `राजप्रसाद` `कीर्ति` `मान` |
| `phala:learning` | education, wisdom, scholarship, eloquence | `विद्या` `पण्डित` `विद्वत्` `वाग्मी` |
| `phala:religion` | dharma, donation, pilgrimage, temples, remedies | `धर्म` `दान` `देवालय` `जप` `तीर्थ` |
| `phala:travel` | journeys, foreign residence, exile | `गमन` `प्रवास` `विदेश` `देशत्याग` |
| `phala:profession` | work, business, office, service | `व्यवसाय` `कर्म` `सेवा` |
| `phala:property` | house, land, vehicles, cattle | `गृह` `भूमि` `वाहन` `गो` `महिषी` |

**`phala:character` is deliberately absent.** Verses describing the native's temperament
(`क्रोधी` "irritable", `सुशीलो` "well-behaved") are a *description*, not a predicted result, and
folding them in would make the category mean two things.

## Assignment rules

1. **Read the Devanāgarī. The English is a hint, never the source.** Measured on a 14-verse
   sample: **at least 6 carried English that does not translate the adjacent Sanskrit** —
   `17.10` is fever and surgical wounds with English reading "victorious over enemies";
   `57.26` is royal favour with English reading "multiple sorrows"; `20.19` states the father's
   death with English about lucky children. Tagging from the English propagates those errors.
2. **Assign only what the verse states as a result.** A verse that is purely a condition
   (`लग्नेशे धनगे` with no consequent) gets no phala tag.
3. **Multiple categories are normal.** One verse routinely predicts wealth, sons and honour.
4. **Emit nothing rather than guess.** An empty list is a true statement; an invented tag is not.
5. **Record the alignment verdict alongside** — see below.

## The alignment verdict — this pass is also a verification pass

Because the reading compares Devanāgarī against English, it produces something no existing check
can: **whether the translation matches the verse.** Every assignment carries one of:

| verdict | meaning |
|---|---|
| `aligned` | the English translates the adjacent Devanāgarī |
| `mismatch` | the English describes something the Sanskrit does not say |
| `stub` | the English is a generated template (`"Further results regarding … in verse N."`) |
| `absent` | no English present |

**This addresses G31 directly.** Every numbering and schema check in this repo passes on
fluent English attached to unrelated Sanskrit; reading the two together is the only thing that
catches it. The 2026-09-14 session found `16.5` and `15.12` this way by hand, and estimated
Devanāgarī↔English agreement at ~82% corpus-wide — a rate nothing has since localised.
