# Vedic corpus — śākhā map

Transcribed 2026-08-23 from `Vipin Kaushik/sanskrit-texts-sources/new_ved_tree.jpg`.

Each Veda branches into four layers: **संहिता** (mantra), **ब्राह्मण** (ritual prose),
**आरण्यक** (forest texts), **उपनिषद्** (philosophy). The names below are śākhā
(recension) and text names as the tree gives them.

**Status column:** `—` means not held anywhere in this ecosystem. Verified 2026-08-23 by
filename search across `~/Documents/GitHub`: **zero** of these texts exist on disk.

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

**This corpus.** Per the ownership split as revised 2026-08-23: **Youvan Prakashan holds
Tantra and Mantra; Vipin holds Jyotish and everything else.** Philosophy moved to Vipin,
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

None of these are held. Freely available for all of them:

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
