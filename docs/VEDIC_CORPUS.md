# Vedic corpus — śākhā map

Transcribed 2026-08-23 from `Vipin Kaushik/sanskrit-texts-sources/new_ved_tree.jpg`.

Each Veda branches into four layers: **संहिता** (mantra), **ब्राह्मण** (ritual prose),
**आरण्यक** (forest texts), **उपनिषद्** (philosophy). The names below are śākhā
(recension) and text names as the tree gives them.

**Status column:** `—` means not held. **Superseded 2026-08-24** — this read "**zero** of
these texts exist on disk", which was true for about one day. Derive what is held, never
restate it; `docs/INVENTORY.md` is the registry, and the command is in `CLAUDE.md`.

### What is held, as of 2026-08-24

| Layer | Held | Of | Note |
|---|---:|---:|---|
| **संहिता** | **5** | 13 | The **primary recension of every Veda**, plus both Yajurveda branches: Śākala (RV), Taittirīya (KYV), Mādhyandina (ŚYV), Kauthuma (SV), Śaunaka (AV) |
| **उपनिषद्** | **24** | 17+ | **All 13 mukhya**, plus 11 minor |
| **ब्राह्मण** | — | 16 | **Youvan's, from 2026-08-24** — not this corpus |
| **आरण्यक** | — | 5 | **Youvan's, from 2026-08-24** — not this corpus |

**The eight Saṃhitās not held are alternate śākhās, not missing Vedas:** Bāṣkala (RV) ·
Maitrāyaṇī, Kāṭhaka, Kapiṣṭhala (KYV) · Kāṇva (ŚYV) · Rāṇāyanīya, Jaiminīya (SV) ·
Paippalāda (AV). Several survive only in fragments or single manuscripts; Kapiṣṭhala in
particular is not fully extant. Do not read "5 of 13" as 38% of the Saṃhitā layer — the
mantra text of all four Vedas is present.

**Brāhmaṇa and Āraṇyaka now belong to Youvan** (2026-08-24), so they are not this corpus's
backlog at all. They were already excluded here by decision rather than omission — ritual
prose with four nesting levels against a converter built for numbered verse — and the
ownership change makes that permanent rather than deferred. **Nothing moved on disk: zero
of the 21 were held**, so this reassigned a scope, not files. The rows above read `—`, not
`0`, because "not ours" and "ours and absent" are different facts.

### The line is drawn by LAYER, and getting that wrong costs four mukhya Upaniṣads

**Seven of the 24 Upaniṣads held here are textually chapters of a Brāhmaṇa or Āraṇyaka.**
They stay. Reading the split by *containing work* instead of by *layer* would hand Youvan
1,497 verses including four principal Upaniṣads:

| Upaniṣad | Held | Sits inside |
|---|---:|---|
| Bṛhadāraṇyaka | 437 verses | Śatapatha Brāhmaṇa 14 (Mādhyandina) |
| Chāndogya | 627 | Chāndogya Brāhmaṇa 3–10 |
| Mahānārāyaṇa | 263 | Taittirīya Āraṇyaka 10 |
| Taittirīya Up. | 51 | Taittirīya Āraṇyaka 7–9 |
| Kauṣītaki | 51 | Kauṣītaki Āraṇyaka 3–6 |
| Kena | 35 | Jaiminīya Upaniṣad Brāhmaṇa 4.18–21 |
| Aitareya | 33 | Aitareya Āraṇyaka 2.4–6 |

Say "the Upaniṣad layer is ours"; never "anything not in an Āraṇyaka is ours." The second
phrasing is wrong for seven texts and reads as correct.

**Two known gaps inside what is held**, both declared in the data rather than papered over:
RV 1.65 (two interleaved numbering systems — a scholarly call) and AV 20.13 (absent from
both witnesses; see `CANONICAL_COUNTS.md`). Everything else is contiguous.

---

## ऋग्वेद · Rigveda

| Layer | Texts | Status |
|---|---|---|
| संहिता | शाकल · बाष्कल | — |
| ब्राह्मण | ऐतरेय · कौषीतकी · शांखायन | — |
| आरण्यक | ऐतरेय | — |
| उपनिषद् | ऐतरेय · बाष्कल · कौषीतकी | — |

## यजुर्वेद · Yajurveda

Splits into **कृष्ण** (Krishna/Black) and **शुक्ल** (Shukla/White) before branching.

| Layer | कृष्ण | शुक्ल | Status |
|---|---|---|---|
| संहिता | तैत्तिरीय · मैत्रायणी · काठक · कपिष्ठल | माध्यंदिन · काण्व | — |
| ब्राह्मण | तैत्तिरीय | शतपथ (मा.) · शतपथ (का.) | — |
| आरण्यक | तैत्तिरीय · मैत्रायणी | बृहदारण्यक (मा.) · बृहदारण्यक (का.) | — |
| उपनिषद् | तैत्तिरीय · महानारायण · मैत्री · कठ · श्वेताश्वतर | बृहदारण्यक · ईशावास्य · शिवसंकल्प | — |

## सामवेद · Samaveda

| Layer | Texts | Status |
|---|---|---|
| संहिता | कौथुम · राणायणी · जैमिनी | — |
| ब्राह्मण | तंड्यमहाब्राह्मण (पंचविंश) · षड्विंश · वंश · सामविधान · आर्षेय · मंत्र · दैवत · संहितोपनिषद् · जैमिनीय (तलवकार) | — |
| उपनिषद् | केन · छांदोग्य | — |

## अथर्ववेद · Atharvaveda

| Layer | Texts | Status |
|---|---|---|
| संहिता | शौनक · पिप्पलाद | — |
| ब्राह्मण | गोपथ | — |
| उपनिषद् | प्रश्न · मुण्डक · माण्डूक्य · अथर्वशिखा वगैरे · "बावन्न उपनिषद" (52 Upaniṣads) | — |

---

## The other two axes — Vedāṅga and Upaveda

**The four layers are not the only division, and conflating them is the mistake this section
exists to stop.** Three axes, orthogonal:

| Axis | What it is | Relation to a Veda |
|---|---|---|
| **Layer** (4) | Saṃhitā · Brāhmaṇa · Āraṇyaka · Upaniṣad | *strata within* each Veda |
| **Vedāṅga** (6) | Śikṣā · Kalpa · Vyākaraṇa · Nirukta · Chandas · Jyotiṣa | *limbs attached to* the Vedas, serving all four |
| **Upaveda** (4) | Āyurveda · Dhanurveda · Gāndharvaveda · Sthāpatyaveda | *applied* knowledge, one traditionally per Veda |

**Puruṣārtha — dharma, artha, kāma, mokṣa — is on none of these axes.** It is the four aims
of human life, from Dharmaśāstra and Vedānta. It is not a textual division of anything and
must not become a directory. Recorded because it was proposed as one, 2026-08-24.

### Vedāṅga — ownership and what is held

| Vedāṅga | Subject | Owner | Held |
|---|---|---|---|
| Śikṣā | phonetics, recitation | **Youvan** | — |
| Kalpa | ritual procedure | **Youvan** | moved there 2026-08-24 (`asvalayana_grhya_sutra`, 394 verses) |
| Vyākaraṇa | grammar (Aṣṭādhyāyī) | Vipin | — · **sūtra shape, blocked** |
| Nirukta | etymology | Vipin | — |
| Chandas | metre (Piṅgala) | Vipin | — · **sūtra shape, blocked** |
| **Jyotiṣa** | ritual timing | Vipin | **held** — `Vedanga-Jyotisha/`, Ārca 36 + Yājuṣa 45 |

**This corrects a claim that stood here until 2026-08-24:** that Vedāṅga Jyotiṣa was *"the
one genuine overlap already in this repo."* It was not the only one — `Kalpa/` was a Vedāṅga
too, sitting as an unrelated top-level directory with nothing recording that they share an
axis. Two of six were held and the file said one.

### Upaveda — ownership

| Upaveda | Subject | Owner |
|---|---|---|
| Āyurveda | medicine | Vipin |
| Dhanurveda | archery, warfare | Vipin |
| **Gāndharvaveda** | music, dance (Sāmavedic chant, Nāṭyaśāstra) | **Youvan** — ritual performance |
| Sthāpatyaveda | architecture, Vāstuśāstra | Vipin |

**Sthāpatyaveda is not blocked by the Vāstu refusal.** Vāstu was refused *as a service* on
2026-07-15 ("a ritual isn't a repair"). That is about selling a consultation; holding the
canonical text is a different act, exactly as holding Dharmaśāstra is not offering ritual
law. Stated here so it is not re-litigated by the next person who greps for "vastu".

**Nothing on either axis is acquired yet beyond Jyotiṣa.** Acquisition splits by **text
shape, not by axis**: the converter finds numbered verse terminators, and Vyākaraṇa, Chandas
and Kalpa are *sūtra* — the same shape as the 14 off-schema Dharmaśāstra files. See
`plans/2026-08-22-dharmashastra-redigitisation.md`; solve it once there.

## The Rigveda's own divisions — two parallel schemes

A Rigvedic citation exists in **two** numbering systems, and they do not convert to one
another by arithmetic:

| Scheme | Levels | Used by |
|---|---|---|
| **Maṇḍala** | maṇḍala (10) → anuvāka → sūkta → ṛc | **our data** — `chapters[]` are the 10 maṇḍalas |
| Aṣṭaka | aṣṭaka (8) → adhyāya (64) → varga → ṛc | recitational; common in older printed editions |

Only the maṇḍala scheme is implemented. Adding aṣṭaka means dual keys on 10,470 verses, so
it is documented and deliberately not built. **A citation from a printed edition may be in
aṣṭaka form** — check before assuming a lookup failure is a missing verse.

## Counts

| | Saṃhitā | Brāhmaṇa | Āraṇyaka | Upaniṣad | Total |
|---|---|---|---|---|---|
| Rigveda | 2 | 3 | 1 | 3 | 9 |
| Yajurveda | 6 | 3 | 4 | 8 | 21 |
| Samaveda | 3 | 9 | 0 | 2 | 14 |
| Atharvaveda | 2 | 1 | 0 | 4 | 7 |
| **Total** | **13** | **16** | **5** | **17** | **51** |

The Atharvaveda's Upaniṣad cell is not a clean count — the tree gives three named texts
plus "अथर्वशिखा वगैरे" (etc.) plus the traditional **52 Upaniṣads** attributed to the
Atharvaveda. Treat 17 as a floor for Upaniṣads, not a total. Traditional enumerations run
to 108 Upaniṣads overall, of which 10–13 are the *mukhya* (principal) ones.

## Where this belongs

**Saṃhitā and Upaniṣad: this corpus. Brāhmaṇa and Āraṇyaka: Youvan, from 2026-08-24.**

Per the ownership split as revised 2026-08-23 and narrowed again 2026-08-24: **Youvan
Prakashan holds Tantra, Mantra, Brāhmaṇa and Āraṇyaka; Vipin holds Jyotish and everything
else.** Philosophy moved to Vipin,
so the Āraṇyakas and Upaniṣads land here, and the Saṃhitās and Brāhmaṇas with them.

This file was first written into `Tushar/Youvan/texts/` on 2026-08-23 under the previous
three-way split (Youvan = Tantra/Mantra/**Philosophy**) and moved here the same day when
that split was narrowed. Recorded because the reasoning inverted, not just the location.

**What stays at Youvan:** the Krishna Sahasranama Stotram relocated here on 2026-08-23.
A sahasranama is nāma-mantra — Mantra scope — so the relocation still holds under the
revised split. It was decided on devotional-vs-Jyotish grounds, which the revision does
not touch.

**Note the boundary this file does not cross.** `sanskrit-texts` was Jyotish-only until
this revision, and two prior calls enforced that: the 2026-06-20 SamudrikShastra removal
and the 2026-08-23 GargaSamhita relocation. Both remain correct — SamudrikShastra is
physiognomy and the Garga text is devotional. **But "out of scope here" no longer implies
"belongs at Youvan."** Only Tantra and Mantra do.

**The one genuine overlap already sits in this repo** and should stay there: the
**Vedāṅga Jyotiṣa**, Lagadha's ritual-timing manual, in its Ārca (Rigveda, 36 verses) and
Yājuṣa (Yajurveda, 45 objects / 43 numbered) recensions. It is a Vedāṅga — a limb attached
to the Vedas — not a layer of the tree above, and its subject is astronomical calculation.
The Sāmaveda and Atharvaveda recensions of it are **lost**, with no extant manuscript.

## Sourcing

**Do not restate what is held here** — `docs/INVENTORY.md` is the registry and the derivation command is in `CLAUDE.md`. This line read *"None of these are held"* until 2026-08-24; it was measured on 2026-08-23 and falsified the next day, the third stale count in this one file. Sources, freely available for all of them:

- **GRETIL** — gretil.sub.uni-goettingen.de (machine-readable, best transcription quality)
- **sanskritdocuments.org** — this ecosystem's existing proofreading source of truth
  (`sanskrit-texts/REFERENCES.md`)
- **Vedic Heritage Portal** — vedicheritage.gov.in (recitation audio, śākhā metadata)

Smallest useful first step is the **mukhya Upaniṣads** — roughly a dozen short texts,
already well-transcribed, and the highest-value layer for Youvan's philosophy scope. The
Saṃhitās are an order of magnitude larger (Rigveda alone is ~10,600 verses).

## Before digitising any of this

No directories have been created for these texts. Doing so would materialise ~51 empty
stubs — and `sanskrit-texts` already carries the cost of that pattern: 13 README-only
directories that `docs/INVENTORY.md` cannot see by construction, two of which
(`Samaveda`, `Atharvaveda`) describe **lost** texts and are not backlog at all.

Create a directory when a source is in hand, not before.
