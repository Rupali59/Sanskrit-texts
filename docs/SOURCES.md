# Source manifest

Every source file this corpus derives from, recorded so it is **re-fetchable and
verifiable without being stored in git**.

Sources live in `../../sanskrit-texts-sources/`, which is deliberately **not committed** —
it is ~310 MB, and Sanskrit Documents' terms discourage redistribution (see
[`../REFERENCES.md`](../REFERENCES.md)). This file is the tracked substitute: it records
what a source is, where it came from, and its checksum, so any of it can be re-acquired and
proven identical.

## How to use it

- **Verify what you hold:** `shasum -a 256 <file>` and compare the `sha256` column (first 16
  hex chars shown; that is ample to detect corruption or truncation).
- **A missing file is not a lost file** — refetch from `Upstream URL` and check the sum.
- **A checksum mismatch means the source moved under us.** Do not silently re-derive the
  JSON; find out what changed first. Upstream texts get re-proofread.

## Tiers — what a file's extension means

Recorded here because it existed only as scattered prose until 2026-08-23.

| Tier | Meaning | May become corpus JSON? |
|---|---|---|
| `.md` | Proofread Devanagari transcription. **Canonical for the Sanskrit text**; the JSON is the derived form. | **Yes** |
| `.html` | Upstream proofread Devanagari page, byte-exact as fetched. Strip to `.md` before use. | Yes, via `.md` |
| `.txt` | **Raw tier** — OCR output or an unprocessed dump. Unproofed. | **No.** Never directly. |
| `.pdf` | Scan. May have no text layer at all. | No |
| `.json` | Raw un-chunked extraction held for reference. | No |

The rule the `.txt` row encodes is `GOTCHAS.md` G6: a `text_id` is a citation surface, so
unproofed text must not acquire one. `MuhurtaMartanda`'s OCR is the worked example.

## Attribution

Sanskrit Documents requires attribution to the site and to the volunteer encoder and
proofreader named in each file's own footer. Where a source carries such a credit it is
recorded in `Attribution`; `—` means the file carries none (typically a scan or an OCR
artifact we produced).

---

## Held sources

Generated 2026-08-23. `sha256` is the first 16 hex characters.

| Path (under `sanskrit-texts-sources/`) | Tier | Size | sha256 | Upstream URL | Attribution |
|---|---|---:|---|---|---|
| `Dharmashastra/4605.txt` | .txt | 1.1 MB | `99c1fcf9a5a0e76c` | _unrecorded_ | — |
| `Dharmashastra/4607.txt` | .txt | 345 KB | `8339d002c024f5b1` | _unrecorded_ | — |
| `Dharmashastra/4609.txt` | .txt | 90 KB | `c4bbe40e18ba2da2` | _unrecorded_ | — |
| `Dharmashastra/4617.txt` | .txt | 1000 KB | `3041cb26648d3db9` | _unrecorded_ | — |
| `Dharmashastra/ManuSmriti/9048.txt` | .txt | 2.7 MB | `24f1585579005646` | _unrecorded_ | — |
| `Dharmashastra/ManuSmriti/manu_clean.txt` | .txt | 2.7 MB | `d7f52eaef22a977b` | _unrecorded_ | — |
| `Hora/Nadi/Bhrigusootram/bhrigustrotram.md` | .md | 67 KB | `33e60e77a5fca439` | _unrecorded_ | — |
| `Hora/Parashari/BrihatJataka/brihmajjataka.md` | .md | 162 KB | `a01f10125acf5d4a` | _unrecorded_ | — |
| `Hora/Parashari/BrihatParasharaHoraShastra/BrihatParasharaHoraShastra.md` | .md | 962 KB | `bb8a79a4fa04a8c8` | _unrecorded_ | — |
| `Hora/Parashari/Chamatkarchintamani/Chamatkarchintamani.md` | .md | 45 KB | `755cd71b10882348` | _unrecorded_ | — |
| `Hora/Parashari/Jatakaparijatah/jatakaparijatah.md` | .md | 676 KB | `651e5339fc01bd8d` | _unrecorded_ | — |
| `Hora/Parashari/Laghujatakam/Laghujatakam_By_Varahamihiracharya.md` | .md | 57 KB | `6f34f5307d1ced90` | _unrecorded_ | — |
| `Hora/Parashari/MinarajaYavanajataka/Minaraja_Shrivriddhayavanajataka_Purvakhanda.md` | .md | 680 KB | `ad410e29c737c37f` | _unrecorded_ | — |
| `Hora/Parashari/Phaladeepika/phaladeepika.md` | .md | 325 KB | `e8314fba229690d3` | _unrecorded_ | — |
| `Hora/Parashari/Saravali/saravaliofkalyan01kalyuoft.pdf` | .pdf | 16.5 MB | `3bfd4f7f717798f8` | _unrecorded_ | — |
| `Hora/Parashari/Shatpanchashika/Shatpanchashika.md` | .md | 19 KB | `f7a26d9b31de4978` | _unrecorded_ | — |
| `Hora/Parashari/UttaraKalamrita/raw_uttara_kalamrita.txt` | .txt | 1016 KB | `6552c2bba6333432` | _unrecorded_ | — |
| `Hora/Parashari/UttaraKalamrita/sections/sec1.txt` | .txt | 29 KB | `570f7dc8be125322` | _unrecorded_ | — |
| `Hora/Parashari/UttaraKalamrita/sections/sec2.txt` | .txt | 100 KB | `db1e48d71c1f83e4` | _unrecorded_ | — |
| `Hora/Parashari/UttaraKalamrita/sections/sec3.txt` | .txt | 45 KB | `e8f3dd2c4a58abe1` | _unrecorded_ | — |
| `Hora/Parashari/UttaraKalamrita/sections/sec4.txt` | .txt | 161 KB | `fbef2acc9d6e449a` | _unrecorded_ | — |
| `Hora/Parashari/UttaraKalamrita/sections/sec5.txt` | .txt | 190 KB | `3d6ea05e018b95e0` | _unrecorded_ | — |
| `Hora/Parashari/UttaraKalamrita/sections/sec6.txt` | .txt | 106 KB | `5ca2873f9fc02f3c` | _unrecorded_ | — |
| `Hora/Parashari/UttaraKalamrita/sections/sec7.txt` | .txt | 43 KB | `18126d10db04bc60` | _unrecorded_ | — |
| `Hora/Parashari/UttaraKalamrita/sections/sec8.txt` | .txt | 107 KB | `af0c1d3b164a6aa1` | _unrecorded_ | — |
| `Hora/Parashari/UttaraKalamrita/sections/sec9.txt` | .txt | 177 KB | `5132b4553958b283` | _unrecorded_ | — |
| `Hora/Parashari/VarahamihirDaivagnavallabh/Varahamihircharita_daivagya_vallabh.md` | .md | 87 KB | `00eb70a50536ac2b` | _unrecorded_ | — |
| `Muhurta/MuhurtaChintamani/MC_REMAINING_RAW.json` | .json | 313 KB | `0b574dfa23192322` | _unrecorded_ | — |
| `Muhurta/MuhurtaChintamani/muhurt_chintamani_002342_hr6.pdf` | .pdf | 35.8 MB | `1f6a56a104795c2e` | _unrecorded_ | — |
| `Muhurta/MuhurtaMartanda/1759902040.pdf` | .pdf | 4.8 MB | `a472456702c49cca` | _unrecorded_ | — |
| `Muhurta/MuhurtaMartanda/raw_muhurta_martanda_ocr.txt` | .txt | 842 KB | `9e069e7fc7163b4a` | _unrecorded_ | — |
| `Samhita/BrihatSamhita/Varahmihir_brihatsamhita.md` | .md | 882 KB | `176344af746f0d52` | _unrecorded_ | — |
| `Samhita/BrihatSamhita/Varahmihir_brihatsamhita2.md` | .md | 902 KB | `83f051c6a4e8c3ca` | _unrecorded_ | — |
| `Samhita/GargaSamhita/3003.txt` | .txt | 43 KB | `2df74209e0bdc377` | _unrecorded_ | — |
| `Siddhanta/Panchasiddhantika/panch_siddhantika_040577_hr6.pdf` | .pdf | 17.0 MB | `901c7020770ed2be` | _unrecorded_ | — |
| `Siddhanta/SuryaSiddhanta/1770115260.pdf` | .pdf | 86.3 MB | `e5333a829983abba` | _unrecorded_ | — |
| `Vedanga-Jyotisha/Rigveda/Aarchjyotisham/Aarchjyotisham.md` | .md | 9 KB | `db06d35fd7e3441b` | _unrecorded_ | — |
| `Vedanga-Jyotisha/Yajurveda/Yajushajyotisham/Yajushajyotisham.md` | .md | 12 KB | `c2a78453fe33ec0e` | _unrecorded_ | — |

**`_unrecorded_` is a real gap, not a placeholder to ignore.** These files predate this
manifest and their upstream URLs were never written down. They are recoverable by searching
the named upstreams, but nobody has done it. Every source added from 2026-08-23 onward must
land with its URL filled in at fetch time — that is the whole point of the mechanism, and a
manifest whose provenance column is empty is a checksum list, not a manifest.

## Known provenance, recorded elsewhere

- `Samhita/GargaSamhita/3003.txt` — the **devotional Vaishnava** Garga Samhita, Ashvamedha
  Khanda ch. 59, not the Jyotish work. Digitised and relocated to
  `Tushar/Youvan/texts/Stotra/KrishnaSahasranamaStotram/`. See `DECISIONS.md` 2026-08-23.
- `Muhurta/MuhurtaMartanda/raw_muhurta_martanda_ocr.txt` — **produced here**, not fetched:
  `pdftoppm -r 300 -gray` then `tesseract -l san+hin --psm 6` over the sibling PDF.
  Substantively corrupt and a three-layer commentary edition; see its `README-OCR.md`.
- `Dharmashastra/{4605,4617}.txt` — Āpastamba-Dharmasūtra with Haradatta's Ujjvalā
  commentary (ed. Mahādeva Śāstri, Mysore 1898). `4607.txt` — Āpastamba-Paribhāṣā-Sūtra.
  `4609.txt` — **unidentified**; a Śrāvaṇī/Upākarma ritual manual fitting no text directory.


## Vedāṅga / Upaveda — where the data actually is (surveyed 2026-08-24)

Surveyed before fetching, because the plan's assumed source was wrong. **Sanskrit Wikisource
is the answer for almost all of it**, not sanskritdocuments and not GRETIL.

### Vipin's texts

| Text | Axis | Source | Devanagari | Shape | Status |
|---|---|---|---|---|---|
| **Dhanurveda** | Dhanurveda | sanskritdocuments `doc_veda/dhanurveda.html` | 18,399 | `double` + single-daṇḍa close | **ready** — 227 verses, contiguous |
| **Caraka Saṃhitā** | Āyurveda | Wikisource, 15 pages | 546,580 | `single_pair`/`double`/`bare` | **BLOCKED** — the markers number the *commentary*; see CANONICAL_COUNTS.md |
| **Suśruta Saṃhitā** | Āyurveda | Wikisource, 18 pages | 52,188 per sthāna page | **bare numerals** | needs a `bare` grammar |
| **Mānasāra** | Sthāpatyaveda | Wikisource, 1 page | **408,048** | **bare numerals** | needs a `bare` grammar |
| **Mayamata** | Sthāpatyaveda | Wikisource, 9 pages | 7,220 per page | **bare numerals** | needs a `bare` grammar |
| Aṣṭādhyāyī | Vyākaraṇa | Wikisource, 30 pages | 13,360 per adhyāya | sūtra | blocked on the sūtra schema |

### Youvan's texts, noted so nobody re-searches for them

Pāṇinīya Śikṣā (sanskritdocuments `pANinIyashikShA.html`, and Wikisource with khaṇḍa
subpages) · Nāṭyaśāstra (sanskritdocuments `natya01`–`natya37`, 37 chapters).

### The seventh marker grammar: bare numerals, no daṇḍa at all

Suśruta, Mānasāra and Mayamata carry **zero daṇḍas of any kind**. Their Wikisource
transcriptions terminate each verse with a bare numeral before a `<br>` — Devanagari in
Mānasāra and Suśruta (`…नमामि १`), **ASCII** in Mayamata (`…यथाक्रमम् 1`). All five existing
grammars find 0 markers, which reads as "empty text" and is why this needed checking rather
than assuming.

A bare numeral is far weaker evidence than a daṇḍa-delimited one, so it was tested rather
than trusted. Taking any numeral that terminates a segment:

| Text | Numerals | In ascending runs of ≥5 | Restarts at 1 | Implied chapters |
|---|---:|---:|---:|---|
| Mānasāra | 5,169 | **100%** | 69 | **70** — matches the canonical 70 adhyāyas exactly |
| Suśruta Uttaratantra 1–20 | 635 | 96% | 19 | **20** — matches the page's own range |
| Mayamata 1–5 | 91 | **100%** | 4 | **5** — matches the page's own range |

**The restart count is the validation.** If these numerals were incidental — quantities,
dates — they would not form ascending runs covering ~100% of occurrences, and the restarts
would not land exactly on the chapter counts the page titles declare. Mānasāra recovering
the canonical 70 from the data alone is the strongest single signal.

### Absent everywhere checked

**Aṣṭāṅgahṛdaya**, **Samarāṅgaṇa Sūtradhāra**, and **Nirukta as a standalone text**
(Wikisource's 87 "nirukta" hits are all mentions inside other works). GRETIL has Nirukta and
Caraka but in **IAST Roman under no granted licence**, so they serve as count witnesses only.
**Vedic Heritage Portal (vedicheritage.gov.in) mentions Nirukta and is the outstanding lead.**
SARIT returned 502 and Muktabodha's host did not resolve on the day — both worth retrying
rather than writing off.


## SARIT — the answer for Caraka and Suśruta, with one blocker (surveyed 2026-08-24)

`sarit.indology.info`, corpus at `github.com/sarit/SARIT-corpus`. It returned 502 on the
first attempt and was worth retrying — it is up, and it holds what nothing else did.

| Text | Structure in the TEI | Canonical | Commentary hits | Script |
|---|---|---|---:|---|
| **Carakasaṃhitā** | `level1` × 8 (sthānas), **`level2` × 120** | **120 adhyāyas** ✓ | 9 | IAST |
| **Suśrutasaṃhitā** | `sthāna` × 6, **`adhyāyaḥ` × 186** | **186 adhyāyas** ✓ | 11 | IAST |
| **Aṣṭāṅgahṛdayasaṃhitā** | 7,726 `<lg>`, 15,439 `<l>` | — | — | IAST |

**The structure is exact.** Caraka's 120 adhyāyas across 8 sthānas and Suśruta's 186 across
6 are the canonical figures, marked up explicitly rather than inferred. Compare what
Wikisource gave: Caraka's Cikitsāsthāna a redirect and its markers numbering the commentary;
Suśruta 4,296 of 8,338 verses with mislabelled page ranges.

**And it is essentially mūla-only** — 9 and 11 commentary-name hits, against **166** in
Wikisource's Caraka.

**Licence: CC BY-SA 3.0 Unported**, stated in each file's `<availability>`. Usable, and
share-alike like the Wikisource material already in the corpus — though 3.0 against
4.0 is a wrinkle for the licence question `LICENSES.md` already carries open.

### The one blocker: script

**Zero Devanagari.** Caraka carries 210,782 IAST diacritics, Suśruta 173,762,
Aṣṭāṅgahṛdaya 145,913. The whole corpus is Devanagari.

**This is not the GRETIL situation.** GRETIL failed on script *and* licence, and its texts
were partial. SARIT is complete, correctly structured, and licensed — it fails on script
alone, and **IAST → Devanagari is a deterministic, reversible character mapping**, not OCR
and not interpretation. It round-trips, so a conversion is verifiable rather than trusted.

**That is a decision, not an implementation detail**, and it is open: the corpus is
currently 100% Devanagari-sourced, and accepting machine transliteration changes its
provenance model. Recorded here rather than assumed either way.
