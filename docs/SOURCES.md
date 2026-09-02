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
| `.wikitext` | Sanskrit Wikisource page source, byte-exact as fetched. **The largest tier** — most of the Veda, Upaniṣad and Upaveda corpus arrived this way. | **Yes** |
| `.md` | Proofread Devanagari transcription. **Canonical for the Sanskrit text**; the JSON is the derived form. | **Yes** |
| `.html` | Upstream proofread Devanagari page, byte-exact as fetched. Strip to `.md` before use. | Yes, via `.md` |
| `.xml` | SARIT TEI edition. Romanised — needs transliteration to Devanagari first; see §"The one blocker: script". | Yes, after transliteration |
| `.txt` | **Raw tier** — OCR output or an unprocessed dump. Unproofed. | **No.** Never directly. |
| `.pdf` | Scan. May have no text layer at all. | No |
| `.json` | Raw un-chunked extraction held for reference. | No |
| `.redirect` · `.DUPLICATE-OF-NNN` | **Fetch markers, not content.** A Wikisource page that redirected elsewhere, or one detected as a duplicate of another. Keep them: they are the evidence that a gap in a numbering sequence is deliberate rather than a dropped text ([`GOTCHAS.md`](../../propagation/state/sanskrit-texts/GOTCHAS.md) G12). | No |

The rule the `.txt` row encodes is [`GOTCHAS.md`](../../propagation/state/sanskrit-texts/GOTCHAS.md) G6: a `text_id` is a citation surface, so
unproofed text must not acquire one. `MuhurtaMartanda`'s OCR is the worked example.

## Attribution

Sanskrit Documents requires attribution to the site and to the volunteer encoder and
proofreader named in each file's own footer. Where a source carries such a credit it is
recorded in `Attribution`; `—` means the file carries none (typically a scan or an OCR
artifact we produced).

---

## Held sources

Generated 2026-08-23. `sha256` is the first 16 hex characters.

**Scope — read this before treating the table as complete.** It covers the **38 files held on
2026-08-23** and was never regenerated. The Vedic, Upaniṣad and Upaveda acquisition that
followed added ~146 more, and their provenance is recorded in the prose sections below
(§"Vedāṅga / Upaveda — where the data actually is", §SARIT), **not** in this table. So the
table is authoritative for the Jyotiṣa texts and silent about the corpus's other 81% by shloka
count. Derive what is actually on disk:

```sh
find ../sanskrit-texts-sources -type f \
  -not -name '.DS_Store' -not -name '*.bundle' -not -name '*.jpg' | wc -l
```

Extending it by hand is what let it rot; if it is regenerated, generate it.

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

### Not a source: `sanskrit-texts-prerewrite-e0613c4.bundle`

150 MB at the root of the sources tree — **41% of its total size** — and named in no document
until 2026-09-02. It is a `git bundle`: a backup of this repository taken before the
`e0613c4` history rewrite, parked in the sources tree because that tree is gitignored and
large files are tolerated there. It is **not** corpus provenance and must not be read as such.
It verifies clean and **records a complete history**, `refs/heads/main` at `e0613c4` — a commit the live repo no longer has, so this bundle is the only copy. Re-check before deleting:

```sh
git bundle verify ../sanskrit-texts-sources/sanskrit-texts-prerewrite-e0613c4.bundle
```

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
  `4609.txt` — **identified 2026-09-02: the `Āpastamba-ukta Śrāvaṇī`**, a *prayoga* (ritual
  handbook) for the Vedotsarjana/Upākarma rites in Āpastamba's school. It opens
  `॥अथापस्तंबोक्तश्रावणीप्रारंभः॥` and closes `॥इत्यापस्तंबोक्तश्रावणीसमाप्तः॥`, so it is a
  complete self-contained work, not a fragment. **It is Kalpa, and therefore Youvan's** — the
  genre test, not the containing tradition: 13 saṅkalpa resolves (`करिष्ये`), `उत्सर्जन` ×10,
  `उपाकर्म` ×4, `होम`, `आचम्य`, and **zero** dharma-determination markers (`निर्णय`,
  `मीमांसा`, `स्मृति`, `व्रत` all absent). It reasons about no dharma; it tells you what to do
  and in what order. Nothing moves on disk — the file stays here, as Youvan has no sources
  tier.


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


### The transliteration check — it is lossless, and the citations are the bonus

Measured on SARIT's actual text with `indic-transliteration`, round-tripping
IAST → Devanagari → IAST and comparing byte-for-byte:

| Text | Lines | Round-trip | Per-line citations |
|---|---:|---|---:|
| Carakasaṃhitā | 17,090 | **17,086 ok / 4 differ — 99.98%** | 9,268 (54%) |
| Suśrutasaṃhitā | 6,191 | **6,188 ok / 3 differ — 99.95%** | 3,130 (50%) |
| Aṣṭāṅgahṛdaya | 15,439 | 12,035 ok / 3,404 differ — 77% | 14,959 (**96%**) |

**Every residual failure is a citation label or a source typo, never lost Sanskrit.**
Caraka's 4 and Suśruta's 3 are exactly the lines carrying a stray capital in the source
(`hetuyuktijO`, `pitYn`). Aṣṭāṅgahṛdaya's 3,404 are lines with an **embedded trailing**
citation (`... || 5 || Ah.1.1.005v/ 1-5bv`), where only the capital `Ah` changes case —
the Sanskrit before it is identical. Citations are metadata and must be excluded from
transliteration anyway.

One normalisation is needed first: the sources mix **`ṁ` (dot above) and `ṃ` (dot below)**
for anusvāra. `ṁ` round-trips to a candrabindu; mapping it to `ṃ` beforehand resolves it.

**Two instrument errors on the way to this number, both worth recording.** A first pass
reported **45%** because it transliterated the citation prefix along with the text. A second
reported HK, SLP1 and Velthuis each round-tripping Aṣṭāṅgahṛdaya at **100%** — a false pass,
because a scheme that cannot read a character leaves it untouched and it round-trips
trivially. A 100% on an unreadable text is not a pass.

**And the citations are worth more than the script conversion.** `Ca.1.1.3ab` is
sthāna.adhyāya.verse.pāda, stated per line by the source. Aṣṭāṅgahṛdaya carries one on 96%
of its lines. That is the structure this corpus has spent the whole session inferring badly
from verse numbers — stated outright.


### The Brahmanand Tripāṭhī Aṣṭāṅga Hṛdaya PDF — not usable

`Ashtang_Hridayam_Brahmanand_Tripathi_अष्टांग_हृदय-1.pdf`, 387 pages, 51 MB. **Zero
characters extract from the entire document** — not a low count, zero. Every page is a pair
of JPEG images at ~144 ppi, Ghostscript-wrapped. It is a scan.

Checked the way G3 prescribes, because a byte count looks like success: `pdftotext | tr -d
'\f\n\t ' | wc -c` returns **0** across all 387 pages, and `pdfimages -list` shows each
page as `887×~1310 rgb jpeg` with no text object.

**Three independent blockers, any one of which is sufficient:**

1. **No text layer.** OCR would be required, and at ~144 ppi — well under the ~300 ppi
   Devanagari OCR wants — this is the same path already rejected for `MuhurtaMartanda`.
2. **It is a commentary edition.** Tripāṭhī's is the *Nirmalā* Hindi commentary, so the mūla
   is interleaved with commentary — the Caraka problem (G18), which no amount of OCR quality
   fixes.
3. **Copyright.** The Sanskrit mūla is public domain; Tripāṭhī's commentary and edition are a
   modern Chaukhamba work and are not.

**SARIT's Aṣṭāṅgahṛdaya is strictly better on every axis** — machine-readable, 96% of lines
carrying an explicit `Ah.1.1.005` citation, and CC BY-SA 3.0. Its only deficit is script,
and that is a lossless mapping rather than an OCR gamble.


## Four sources that were not what they looked like

**Sanskrit titles collide, and four apparent sources for this corpus turned out to be
different texts.** All four are NAME COLLISIONS — the pattern is [`GOTCHAS.md`](../../propagation/state/sanskrit-texts/GOTCHAS.md) G26; the
instances are here.

**Two failure modes live in this section and they are not the same thing.** A name collision
means the file you found is a different work. An unusable source means the right work in an
unreadable form. `MuhurtaMartanda` has *both*, which is why an earlier version of this
section listed its unreadable PDF as one of "the four" and left the actual `martanda`
collision unrecorded — while G26 counted it. Kept apart below.

`CLAUDE.md` said `GargaSamhita` and `MuhurtaMartanda` already had sources ready. Both claims
died on inspection 2026-08-23.

- **`GargaSamhita`'s `3003.txt` is the wrong Garga Saṃhitā.** Its colophon reads
  `अश्वमेधखण्डे ... अध्याय ५९` — the devotional Vaiṣṇava Purāṇa, not the Jyotiṣa work.
  Digitised, then **relocated to `Tushar/Youvan/texts/Stotra/KrishnaSahasranamaStotram/`**
  (127 shlokas) under the Jyotiṣa/Youvan ownership split. That directory has **no source
  waiting**; the Jyotiṣa text still needs sourcing.
- **`Muhurta Martanda` → Bhoja's `Rājamārtaṇḍa`.** SARIT carries `bhoja-rajamartanda.xml`;
  the substring `martanda` matched. It is a **commentary on the Yoga-sūtras**, not Nārāyaṇa
  Daivajña's muhūrta manual. *(This row was missing from this file until 2026-08-25 although
  G26 counted it — see the note above.)*

And from the 2026-08-25 survey:

- **`Sarvartha Cintamani` → Pūjyapāda's `Sarvārthasiddhi`.** SARIT carries
  `pujyapada-sarvarthasiddhi.xml`; the substring `sarvartha` matched. It is a **Jain**
  philosophical commentary on the Tattvārthasūtra, not Veṅkaṭeśa's Horā text.
- **`Siddhanta Siromani` → the Vīraśaiva `Siddhānta Śikhāmaṇi`, and this one is the trap.**
  Wikisource's `सिद्धान्तशिरोमणिः तत्त्वप्रदीपिकासहितः` is **1,238,304 bytes** where every
  other candidate in the survey was a 327–465 byte stub. Size read as proof. Content settled
  it: **zero** occurrences of Bhāskara II's structural markers — `गोलाध्याय`, `ग्रहगणित`,
  `लीलावती`, `बीजगणित`, `मध्यमाधिकार` — against **967** `लिङ्ग`, **643** `स्थल`, **174**
  `शिवयोगि`, **103** `रेणुक`, **85** `वीरशैव`. Its own second verse names it
  `सिद्धान्तशिखामणि`. Also note `भास्कर` appears 11 times in it, so even an author-name probe
  would have passed.

**Marked by the same instrument error each time.** All four were found by substring match on
a transliterated name — `garga`, `martanda`, `sarvartha`, `shiromani`. A name is a search key,
never evidence. Confirm with the structural markers the target text *must* contain, and with
the colophon.

### Separately — an unusable source, not a collision

**`MuhurtaMartanda`'s PDF has no text layer.** 154 pages of `tiff2pdf`-wrapped CCITT bitmaps;
`pdftotext` returns 154 bytes — one form-feed per page, zero characters (G3). It is a scan,
and additionally a *commentary edition* (mūla + Sanskrit ṭīkā + Hindi bhāṣā-ṭīkā interleaved),
so even clean OCR would not yield mūla shlokas without separating three text layers.

This is the **right work in an unreadable form**, which is a different problem from the four
above and does not count toward them.

## Source survey — all 11 undigitised texts, 2026-08-25

**Nine of the eleven had never been surveyed.** This file previously mentioned only Garga
Saṃhitā and Muhūrta Mārtaṇḍa; the rest were listed as pending on no evidence either way.

**Result: none of the eleven has a machine-readable source in any channel this pipeline
uses.** They are blocked on **sourcing**, not on parsing.

| Channel | Query | Result |
|---|---|---|
| sanskritdocuments | `GET /sanskrit/jyotisha/`, links under `/doc_z_misc_sociology_astrology/` | **0 of 11** — and see below |
| SARIT | `GET api.github.com/repos/sarit/SARIT-corpus/contents/`, 85 `.xml` | **0 of 11** (2 false positives) |
| Wikisource (sa) | `action=query&list=search` per title | stubs only, 327–465 bytes (1 false positive) |
| archive.org | the 104 `archive.org/details/` links on the jyotiṣa index | **0 of 11** name any |

### sanskritdocuments' jyotiṣa corpus is EXHAUSTED — and that is a milestone

Its index carries **50 document links → 25 stems → 13 distinct texts** (a `.pdf` and a
`.itx` per stem; BPHS alone is 11 stems, `par0110`…`par9197`). **All 13 are already held**,
and no stem fails to map:

| stem | `text_id` | | stem | `text_id` |
|---|---|---|---|---|
| `aarchajyotiSha` | `arch_jyotisham` | | `bRRihatsaMhitA`, `varbrhs` | `brihat_samhita` |
| `chamatkarachintamani` | `chamatkar_chintamani` | | `bhrigusUtram` | `bhrigu_sutram` |
| `jAtakapArijAtaH` | `jataka_parijata` | | `vriddhayavanajataka1` | `minaraja_yavana_jataka` |
| `daivaGYavallabha` | `varahamihir_daivagnavallabh` | | `yaajuShajyotiSha` | `yajusha_jyotisham` |
| `phaladIpika` | `phaladeepika` | | `laghujAtaka` | `laghu_jatakam` |
| `brihajjAtakam` | `brihat_jataka` | | `ShaTpanchAshikA` | `shatpanchashika` |
| `par0110`…`par9197`, `horaashaastraEng34-45` | `bphs` | | | |

Re-derive it by mapping every stem under `/doc_z_misc_sociology_astrology/` to a held
`text_id` and asserting **both** empty sets: stems that map to nothing, and mapped ids that
are not held. Measured 2026-08-25: 25 stems, 13 ids, **0 unmapped, 0 unheld**.

**Count stems and texts separately.** "25 texts" is wrong and was written that way first —
the stem count flatters the corpus by 12, because a chunked text contributes one stem per
chunk.

### Second survey, 2026-09-02 — the three channels the first one named as untried

The 2026-08-25 survey closed four channels and named three it had not tried: GRETIL,
Muktabodha, the Vedic Heritage Portal. All three are now surveyed, plus the Digital Corpus
of Sanskrit and a partial look at TITUS.

**Result: 1 of the 11 exists as machine-readable text, and it is partial and
licence-blocked.** The other ten are absent from every channel checked.

| Channel | Method | Result |
|---|---|---|
| **GRETIL** | full index + update history grepped across transliteration schemes; TEI header opened on every candidate | **1 of 11** — Brāhmasphuṭasiddhānta |
| **Muktabodha** (public e-text library) | its two public 499-entry title-link lists, fetched directly | **0 of 11** |
| **Vedic Heritage Portal** | the site's own `?s=` search, per title | **0 of 11** |
| **Digital Corpus of Sanskrit** | its enumerated text list (~285 titles) | **0 of 11** |
| **TITUS** | single index pass — **not exhaustive** | 1 found; other ten **UNVERIFIED**, not absent |

**Two Muktabodha sub-collections are UNSURVEYED, not empty.** Its Gokarna Vedic collection is
login-gated and its IFP catalog needs individual scholarly registration; neither was accessed.
Both are manuscript images (DjVu/PDF) under CC BY-NC-ND, so a hit in either would be
scan-only. Recorded as unsurveyed because "not looked at" and "not there" are different facts.

**The absences are structural, which is what makes them a closure rather than a failed
search.** GRETIL's Nibandha section holds two texts total and its Jyotiṣa section twelve, all
siddhānta/gaṇita — it has no Muhūrta, Praśna, Jātaka or Nāḍī literature at all. Muktabodha's
own category breakdown is Śaiva/Tantric/Pāñcarātra/Śrīvidyā/Yoga with no Jyotiṣa or
Dharmaśāstra category. The Vedic Heritage Portal covers the Vedic canon by design and stops
before post-Vedic Jyotiṣa. None of the three is worth returning to for this list.

### `brahmasphuta_siddhanta` — available, partial, and licence-blocked

The one find, from **two** channels carrying what is evidently one digitisation — both cite
S. Dvivedin's Benares 1902 edition, digitised by Takao Hayashi 1993.

| | GRETIL | TITUS |
|---|---|---|
| URL | `gretil/corpustei/sa_brahmagupta-brAhmasphuTasiddhAnta.xml` | `texte/etcs/ind/aind/klskt/mathemat/brsphsd/` |
| Format | TEI XML + HTML + plain text | HTML, UTF-8 |
| Licence | **CC BY-NC-SA 4.0** | **"No parts of this document may be republished in any form without prior permission by the copyright holder"** (© TITUS Project, 8.12.2008) |

**Three blockers, and the licence is the one that decides it:**

1. **It is not the whole text.** Chapters 12, 18, 19, 20 and stanzas 17–23 of 21 only — the
   mathematical chapters — of a 24-chapter work. Verified in GRETIL's own TEI header.
2. **It is transliterated, not Devanāgarī.** The body opens `parikarma-viṃśatim yas
   saṅkalita-ādyām pṛthak vijānāti`. This is the same script blocker recorded above against
   SARIT, and needs the same transliteration step.
3. **Both licences conflict with what this corpus does.** TITUS forbids republication without
   permission outright, and republication is precisely the act — this repo is public and the
   text is served through AstroAcharya's `/texts` API. GRETIL's CC BY-NC-SA 4.0 permits that
   only **non-commercially**, and AstroAcharya is the funnel for a paid consultation practice.
   See [`LICENSES.md`](LICENSES.md) §"The NonCommercial question".

**So it is not acquirable on today's terms**, and the blocker is legal rather than technical.
The route that would open it is asking TITUS or the rights holder directly — a human act, not
a pipeline one.

### What this means for the eleven

There is no more Jyotiṣa to take from the channels in use. Acquiring any of the eleven needs
either a **new channel** (muktabodha, the Vedic Heritage Portal, GRETIL under a licence review)
or **OCR of scans** — and Muhūrta Mārtaṇḍa already showed what that costs: 154 pages of
`tiff2pdf`-wrapped CCITT bitmaps, `pdftotext` returning 154 bytes, and a commentary edition
needing mūla, Sanskrit ṭīkā and Hindi bhāṣā-ṭīkā separated. **Both were declined 2026-08-25**;
the eleven are recorded as unsourceable rather than pending.

> **Superseded in part, 2026-09-02.** Rupali supplied CC-0 eGangotri scans and the OCR route
> declined above was taken. **Acquired: `Dharmasindhu`, `Nirṇayasindhu`, `MuhurtaMartanda`** —
> each recorded in its own section at the end of this file. **Rejected on copyright, so still
> unsourced: `PrasnaMarga`** (the B.V. Raman edition). The cost estimate above was not wrong —
> the mūla/ṭīkā separation it names is still outstanding for all three.
>
> **Do not restate a remaining-count here**; this note carried "nine" for one hour before
> Muhūrta Mārtaṇḍa arrived and made it eight. The acquired list above is the fact; subtract it
> from the eleven in §"Source survey" when you need the number.
> `brahmasphuta_siddhanta`'s blocker remains licence, not availability.


## Dharmasindhu and Nirṇayasindhu — acquired by scan, OCR'd 2026-09-02

Priorities #1 and #2 of the eleven, both supplied by Rupali as PDFs after every online channel
returned ABSENT for them (§"Source survey", §"Second survey"). **These are the first two of the
eleven to be acquired at all.**

| | Dharmasindhu | Nirṇayasindhu |
|---|---|---|
| Edition | Kāśīnātha Upādhyāya, with Mihir Chandra's Hindi **Bhāṣā Ṭīkā** — Khemraj | Hindi edition |
| Pages | 738 | 1,024 |
| Text layer | **none** — the only extractable characters are a per-page eGangotri watermark | none |
| Licence | **CC-0** (eGangotri watermark) — the first non-NonCommercial upstream this corpus has found; see `LICENSES.md` §"The NonCommercial question" | as above |
| Landed at | `../sanskrit-texts-sources/Dharmashastra/Dharmasindhu/DharmaSindhu.{san,hin}.txt` | `.../NirnayaSindhu/NirnayaSindhu.{san,hin}.txt` |

**Identified from content, not from the filename** — G26 now has nine instances, and
`MuhurtaMartanda` and `GargaSamhita` both died on inspection after looking right by name. The
Dharmasindhu scan carries `धर्मसिन्धु` in its running head (OCR: `धमेसिन्धु`) and its body is
kāla-nirṇaya throughout — tithi/lagna **gaṇḍānta**, the śānti prescribed for a birth in each
half, vessel-and-image **varuṇa-pūjana** with 108 āhutis. That is the right subject *and* the
right genre, which is the test the fabricated Siddhānta texts failed.

**They are OCR, so they stay in the raw `.txt` tier — G6.** Neither has a `text_id`, and
neither may acquire one without proofing or an explicit decision from Rupali to qualify that
rule. The accuracy measurement that bounds any such decision is in
`scripts/sanskrit-pdf/README.md` §ocr: **use the `hin` output, not `san`** — the `san` model
renders `और` zero times in 738 pages.

**Still to do before either is usable:** separating Kāśīnātha's Sanskrit *mūla* from the Hindi
Bhāṣā Ṭīkā. The discriminator is **lexical, not structural** — unlike Āpastamba, where mūla and
commentary were both Sanskrit and split on a numeral. Build the Hindi marker list against
measured output: a narrow list under-detected Hindi badly in the first Nirṇayasindhu pass and
classified a plainly-Hindi line as Sanskrit.

**The ṭīkā is an asset, not only an obstacle.** Hindi is one of the corpus's two target
languages, and a human Hindi rendering outranks any machine draft.

### Praśna Mārga — a scan was supplied 2026-09-02 and REJECTED on copyright

`Panangadu_Nambudhiri_-_Prasna_Marga_(Part_I).pdf`, 745pp, 18 MB, no text layer. Priority #5
of the eleven. **Not ingested, and the reason is not fixable by better tooling.**

Its own front matter settles it:

> First Edition: Bangalore, 1980 · Second Edition: Delhi, 1991
> **© Copyright Dr. B.V. Raman, 1991 · All rights reserved**
> ISBN 81-208-0914-9 · **Motilal Banarsidass Publishers Pvt. Ltd.**

Title page: *"Praśna Mārga — English Translation with Original Text in Devanagari and Notes by
Bangalore Venkata Raman"*. The filename names the traditional author (a Nambūdiri of Panangadu,
Kerala, 16th–17th c.) and **the PDF metadata names the real one**: `Prasna Marga I - B.V.
RAMAN.djvu`. B.V. Raman died in 1998, so the edition is in copyright for decades yet and the
publisher is still trading.

**The split that matters.** The Devanāgarī *stanzas* are public domain — the work is 16th–17th
century. Raman's translation, notes, and this edition's arrangement are **not**. Sampling p.121
shows them interleaved stanza-by-stanza (`॥११५॥` followed by `Stanza 115.—Watch the questioner
as to how he stands…`), with whole pages of Raman's own commentary between.

**So a mūla-only extraction is the one defensible route, and it is still not worth taking:**

- OCR would capture the copyrighted translation wholesale; separating it is the *same* problem
  as Dharmasindhu's ṭīkā split, but with legal stakes rather than merely editorial ones.
- The Devanāgarī OCR off this scan is **poor** — p.121 yields
  `दोषाय atuaed हि तख यतिः सिरा तख`, mixing Latin garbage into the stanza.
- There is **no second witness to proof it against**. That is precisely why Praśna Mārga is on
  the unsourced list; a lone bad OCR of a copyrighted edition is the worst of both.
- It is **Part I only** — chapters I–XVI of 32.

**This corpus is public and feeds a paid practice's API.** `LICENSES.md` §"The NonCommercial
question" records that tension as unresolved for *NonCommercial* sources; "all rights reserved"
is strictly worse and is not arguable. Contrast eGangotri (§above), which is CC-0 and dissolves
the question entirely.

**What would actually source this text:** a Devanāgarī witness that is not a modern translator's
edition. Praśna Mārga remains ABSENT from sanskritdocuments, SARIT, Wikisource and archive.org's
jyotiṣa index. **Do not re-acquire the Raman edition** — this entry exists so the next person
recognises it before spending 745 pages of OCR on it.

### Muhūrta Mārtaṇḍa — a SECOND scan, CC-0 and usable, 2026-09-02

**This supersedes every "no usable source" claim about this text in this file** — §"Two sources
that were not what they looked like", §"Absent everywhere checked", and the cost estimate in
§"What this means for the eleven" that cites it as the worked example of why OCR was declined.
Those describe `Muhurta/MuhurtaMartanda/1759902040.pdf`, **154 pages of `tiff2pdf`-wrapped CCITT
bitmaps**, and remain true of that file. A different and better scan now exists beside it.

| | |
|---|---|
| File | `Muhurta/MuhurtaMartanda/raw/MuhurtaMartanda-chaukhamba-eGangotri.pdf` |
| Pages | 188 · 126 MB · no text layer |
| Licence | **CC-0** — `CC-0. Mumukshu Bhawan Varanasi Collection. Digitized by eGangotri` |
| Edition | ed. **Kapileśvara Śāstrī** (Maithil paṇḍita, Jñānodaya Sanskrit Mahāvidyālaya, Patna), with the *sānvaya Mārtaṇḍaprakāśikā* Sanskrit commentary |
| Publisher | Chaukhamba Sanskrit Sansthan, Varanasi · Kāśī Sanskrit Granthamālā 146 |
| Printing | third edition, **Vikrama Saṃvat 2039 = 1982 CE**, ₹12 |

**Identified from the title page, not the filename** — `martanda` is one of the nine G26
collisions, having previously matched Bhoja's **Rājamārtaṇḍa**, a Yoga-sūtra commentary. The
title page reads `श्रीनारायणदैवज्ञविरचितः मुहूर्तमार्तण्डः` — *composed by Nārāyaṇa Daivajña* — which
is the target author for the 1571 muhūrta manual, and is decisively not Bhoja.

**On rights, and the contrast with Praśna Mārga two sections above.** Both were supplied the
same day; one is rejected and this one is not, so the distinction should be explicit. The Raman
Praśna Mārga carries `© Copyright Dr. B.V. Raman, 1991 · All rights reserved` from a publisher
still trading, over a translation by a man who died in 1998. This carries **no rights
reservation in its front matter**, its apparatus is a Sanskrit commentary rather than a modern
translation, and the digitiser asserts CC-0. The *mūla* is 1571 and public domain either way.
**The 1982 printing is a printing, not necessarily the commentary's date** — Kāśī Sanskrit
Granthamālā 146 places the first edition considerably earlier. Not researched further, because
nothing here turns on it; if the commentary is ever to be published rather than used as
apparatus, it should be.

**Why this text is wanted** (`INVENTORY.md:268`): it is the independent cross-check on the
muhūrta windows now that Muhūrta Cintāmaṇi is held — and **where two manuals diverge, as the
durmuhūrta weekday positions do, the divergence is what to surface for Vipin, not something to
resolve silently.** A second witness is the entire point, so this must not be reconciled against
Cintāmaṇi during digitisation.

OCR to `MuhurtaMartanda.{san,hin}.txt`, raw tier, G6. Note the prior
`raw_muhurta_martanda_ocr.txt` (842 KB) came off the **CCITT scan** and is not the same artifact.

### Garga Horā Śāstra — supplied 2026-09-02 and REJECTED on copyright

`Garga Hora Shastra Pathak K.K..pdf`, 158pp, 6.5 MB, no text layer, **no digitiser stamp** (so
no CC-0 claim — unlike the eGangotri scans). Priority #9. **Not ingested.**

> GARGA HORA SHASTRA — **By K.K. Pathak** · Nishkaam Peeth Prakashan
> (Publication Division of *The Times of Astrology*) · First Edition: **1999**
> **© Rajeshwari Shanker Associates. All rights reserved. No part of this book may be used or
> reproduced in any manner whatsoever without written permission from the publisher** except
> in the case of brief quotations embodied in critical essays and reviews.
> ISBN 81-87528-11-7

**It does contain the Devanāgarī mūla — record that correctly, because the first reading of
this file got it wrong.** The contents page lists *"House-Wise Effects of Moon / Mars / …"*,
which reads like a modern English handbook with no source text, and the foreword calls the book
*"a unique commentary on & elucidation over the principles enshrined in … classics like Garga
Hora"*. Both suggested there was nothing to extract. **A content page disproves it**: p.42 runs
śloka, then Hindi, then English, per verse —

> `द्रव्यपतिः लग्नगतः कृपणं व्यवसायिनं सुकर्माणम् ।`
> `धनिनं श्रीपतिविदितं करोति नरमतुलभोगयुतम् ॥`

So the rejection rests on **rights alone**, and the ground it does *not* rest on is worth
naming: rejecting it as "not a source text" would have been the right answer for the wrong
reason, and would have mis-recorded what the file is for whoever finds it next.

**Why it is nonetheless a firmer no than the Raman Praśna Mārga.** That edition asserts
`© 1991, all rights reserved`; this asserts **1999** plus an explicit prohibition on
reproduction *in any manner whatsoever*. Same entanglement — public-domain mūla inside a
copyrighted modern apparatus, here Hindi **and** English — with a later date and a stronger
clause. `LICENSES.md` §"The NonCommercial question" governs; this is not NonCommercial, it is
all-rights-reserved.

**What it does settle, and this is worth having.** The **jyotiṣa** Garga Horā is a real text
that exists in print with a substantial Devanāgarī mūla, and it is **not** the devotional
`गर्गसंहिता` that G26's first collision matched (the Vaiṣṇava Purāṇa, assigned to Youvan
2026-08-23 as nāma-mantra). Those are two different works and only the horā is Vipin's. What to
look for is a Devanāgarī witness that is not a modern translator's edition — a pre-1964 printing
or a manuscript transcription. **Do not re-acquire the Pathak edition.**

### Sūrya Siddhānta — the replacement for a fabricated text, OCR'd 2026-09-02

**Already held, never OCR'd.** `Siddhanta/SuryaSiddhanta/1770115260.pdf`, 345pp, `no-text`
tier — in this tree the whole time the corpus was serving a **fabricated** `surya_siddhanta`
under three live astroacharya citations. It went un-OCR'd because the OCR lane was unmeasured
and OCR of commentary editions had been declined; both of those changed on 2026-09-02.

| | |
|---|---|
| Edition | *Sūryasiddhānta*, ed. with the **Sudhāvarṣiṇī** commentary by Mahāmahopādhyāya **Sudhākara Dvivedī** |
| Published | Asiatic Society of Bengal, Calcutta, **1925** (Baptist Mission Press) |
| First edition | Bibliotheca Indica Nos. 1187 (1909) and 1296 (1911) |
| Rights | **Public domain** — editor died **1922**, per the prefatory note; publication 1909–1925 |
| OCR | `SuryaSiddhanta.{san,hin}.txt` — 311,251 / 320,147 Devanāgarī characters |

**Identified from content, both directions.** The attested incipit
`अल्पावशिष्टे तु कृते मयो नाम महासुरः` is present at `SuryaSiddhanta.san.txt:330`; the held
corpus text's opening `प्रणम्य शिरसा देवं` appears **zero times in 345 pages**. The second check
is the valuable one — it re-confirms the fabrication using a physical witness and full-text
search, where the original finding rested on incipit reasoning alone.

Structure is mūla interleaved with the Sanskrit ṭīkā (`सुधावर्षिणी टीका` in the running head), so
separation follows **Āpastamba's** pattern — both layers Sanskrit, split on the daṇḍa-plus-numeral
terminator — not Dharmasindhu's lexical Hindi/Sanskrit discriminator. Raw tier until that parser
exists, per G6.

### Siddhānta Śiromaṇi — 11 files supplied 2026-09-02; three are CLEAN, and that changes the route

Priority #8, and the one G26's `shiromani` collision burned. **Three of the four parts are now
sourced as machine-readable Devanāgarī**, so this text does not need the OCR lane at all.

**Identification, by G26's own prescribed test.** That entry records the Vīraśaiva *Siddhānta
Śikhāmaṇi* passing a title probe *and* an author-name probe (`भास्कर` appears 11 times in it),
and names the structural markers as the only thing that separated them. Run against all six
text files: **`शिवयोगि` = 0 and `शिखामणि` = 0 in every one**, while Bhāskara II's markers are
abundant. These are the real thing. (`लिङ्ग`/`स्थल` counts are non-diagnostic here — they are
ordinary Sanskrit words; G26 records the Vīraśaiva text at 967 and 643, two orders of magnitude
above anything seen here.)

**The quality split is the finding, and it is provable on a single shared verse.** `7404.txt`
and `1139.txt` both contain the maṅgala verse `॥६॥`:

| | text of `॥६॥` |
|---|---|
| `7404.txt` | `वेदस्य चक्षुः किल शास्त्रमेतत् प्रधानताऽङ्गेषु ततोऽस्य युक्ता। अङ्गैर्युतोऽन्यैः परिपूर्णमूर्तिश्चक्षुर्विहीनः पुरुषो न कश्चित्॥६॥` |
| `1139.txt` | `पधानवाप्रवेन्यू वोऽश्य युक्ता। मुपवा चाइगष्षेप्रय ने नोच्यो। अझै तोम्पैः परिपूर्ण मानि-` |

Same verse, same work, one clean and one unusable. **Do not merge or cross-check these two as
if they were independent witnesses** — the second is OCR noise, not a variant reading.

| File | Devanāgarī | verse markers | stray Latin | Verdict | Part |
|---|---:|---:|---:|---|---|
| `7404.txt` | 426,311 | 935 | **0** | **CLEAN** | *Grahagaṇitādhyāya* — Ānandāśrama 110 |
| `8252.txt` | 560,002 | 735 | **0** | **CLEAN** | *Golādhyāya* — Ānandāśrama 122, Vāsanābhāṣya + Marīci |
| `8244.txt` | 220,262 | 364 | 1 | clean | *Līlāvatī* — Ānandāśrama 107, two commentaries |
| `1274.txt` | 532,141 | 550 | 34 | poor OCR | whole Siddhānta Śiromaṇi + Prabhā Hindi commentary |
| `1139.txt` | 333,191 | 603 | 63 | poor OCR | *Grahagaṇita*, Vāsanābhāṣya + Śiromaṇiprakāśa |
| `3328.txt` | 23,141 | 83 | 165 | **rejected** | *Bījagaṇita* + English, S.K. Abhyankar |

Five PDFs accompany them, all `no-text` scans, held under `raw/`: `1706778372` (Ānandāśrama 107,
Līlāvatī — the page witness for `8244.txt`), `1706617850` (Ānandāśrama 122, Golādhyāya — witness
for `8252.txt`), `1706607175` (175pp, Sanskrit + commentary, *kṣetravyavahāra* sections),
`1696318554` (53pp, opens on an errata table), `1736590500` (Hindi tr. by Pandit Udai Narain
Singh of Madhurapur, Muzaffarpur). One carries a **new digitiser stamp variant** the classifier
had not seen — `Digitized By Siddhanta eGangotri Gyaan Kosha` — and note it does **not** say
CC-0, unlike the Dharmasindhu and Muhūrta Mārtaṇḍa stamps. Do not infer CC-0 from the word
eGangotri.

**Rights.** The Ānandāśrama Sanskrit Series files carry `शके १८५९` (1937 CE) and `शके १८७३`
(1951 CE), consistent with the series volume numbers; the mūla is 1150 CE and unambiguously
public domain. **The editorial apparatus's status is not established here and is not asserted** —
it is very likely clear, but nobody has checked, and this file has already recorded one
"public-domain work ≠ public-domain file" failure today (G26). **`3328.txt` is NOT staged**: it
is Prof. S.K. Abhyankar's modern edition and English translation for Bhaskaracharya Pratishthana
Pune, which it calls its "maiden publication", carrying 1978/1980/1991 — the same category as
the rejected Raman and Pathak editions.

**Still missing: a clean *Bījagaṇita*.** Three of four parts are covered; the algebra survives
only in the rejected Abhyankar file and inside the poor `1274.txt`.

**Upstream URLs are unrecorded** — the files arrived by numeric id (an archive.org / e-library
convention) rather than by link. Record them when known; §"Held sources" already carries four
Dharmaśāstra `.txt` files with `_unrecorded_` provenance and that gap has cost real time.
