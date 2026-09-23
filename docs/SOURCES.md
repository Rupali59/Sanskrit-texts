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
| `Dharmashastra/ApastambaDharmaSutra-MahadevaSastri1898-sd4605.txt` | .txt | 1.1 MB | `99c1fcf9a5a0e76c` | _unrecorded_ | — |
| `Dharmashastra/ApastambaParibhasaSutra-Kapardisvamin-Haradatta-sd4607.txt` | .txt | 345 KB | `8339d002c024f5b1` | _unrecorded_ | — |
| `Dharmashastra/ApastambaSravani-sd4609.txt` | .txt | 90 KB | `c4bbe40e18ba2da2` | _unrecorded_ | — |
| `Dharmashastra/ApastambaDharmaSutra-Haradatta-Ujjvala-sd4617.txt` | .txt | 1000 KB | `3041cb26648d3db9` | _unrecorded_ | — |
| `Dharmashastra/ManuSmriti/ManuSmriti-Kullukabhatta-VasudevaSarma-sd9048.txt` | .txt | 2.7 MB | `24f1585579005646` | _unrecorded_ | — |
| `Dharmashastra/ManuSmriti/manu_clean.txt` | .txt | 2.7 MB | `d7f52eaef22a977b` | _unrecorded_ | — |
| `Hora/Nadi/Bhrigusootram/BhriguSutram.md` | .md | 67 KB | `33e60e77a5fca439` | _unrecorded_ | — |
| `Hora/Parashari/BrihatJataka/brihmajjataka.md` | .md | 162 KB | `a01f10125acf5d4a` | _unrecorded_ | — |
| `Hora/Parashari/BrihatParasharaHoraShastra/BrihatParasharaHoraShastra.md` | .md | 962 KB | `bb8a79a4fa04a8c8` | _unrecorded_ | — |
| `Hora/Parashari/Chamatkarchintamani/Chamatkarchintamani.md` | .md | 45 KB | `755cd71b10882348` | _unrecorded_ | — |
| `Hora/Parashari/Jatakaparijatah/jatakaparijatah.md` | .md | 676 KB | `651e5339fc01bd8d` | _unrecorded_ | — |
| `Hora/Parashari/Laghujatakam/Laghujatakam_By_Varahamihiracharya.md` | .md | 57 KB | `6f34f5307d1ced90` | _unrecorded_ | — |
| `Hora/Parashari/MinarajaYavanajataka/Minaraja_Shrivriddhayavanajataka_Purvakhanda.md` | .md | 680 KB | `ad410e29c737c37f` | _unrecorded_ | — |
| `Hora/Parashari/Phaladeepika/phaladeepika.md` | .md | 325 KB | `e8314fba229690d3` | _unrecorded_ | — |
| `Hora/Parashari/Saravali/Saravali-Kalyanavarma-archiveorg.pdf` | .pdf | 16.5 MB | `3bfd4f7f717798f8` | _unrecorded_ | — |
| `Hora/Parashari/Shatpanchashika/Shatpanchashika.md` | .md | 19 KB | `f7a26d9b31de4978` | _unrecorded_ | — |
| `Hora/Parashari/UttaraKalamrita/UttaraKalamrita-raw.txt` | .txt | 1016 KB | `6552c2bba6333432` | _unrecorded_ | — |
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
| `Muhurta/MuhurtaMartanda/MuhurtaMartanda-Mohanarama-Martandavallabha-154pp.pdf` | .pdf | 4.8 MB | `a472456702c49cca` | _unrecorded_ | — |
| `Muhurta/MuhurtaMartanda/raw_muhurta_martanda_ocr.txt` | .txt | 842 KB | `9e069e7fc7163b4a` | _unrecorded_ | — |
| `Samhita/BrihatSamhita/Varahmihir_brihatsamhita.md` | .md | 882 KB | `176344af746f0d52` | _unrecorded_ | — |
| `Samhita/BrihatSamhita/Varahmihir_brihatsamhita2.md` | .md | 902 KB | `83f051c6a4e8c3ca` | _unrecorded_ | — |
| `Siddhanta/Panchasiddhantika/panch_siddhantika_040577_hr6.pdf` | .pdf | 17.0 MB | `901c7020770ed2be` | _unrecorded_ | — |
| `Siddhanta/SuryaSiddhanta/SuryaSiddhanta-SudhakaraDvivedi-BibliothecaIndica-345pp.pdf` | .pdf | 86.3 MB | `e5333a829983abba` | _unrecorded_ | — |
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

- **Left the tree 2026-09-08, to Youvan** (`Tushar/text-sources/Kalpa/…`), both Kalpa —
  ritual procedure — and so Youvan's by the 2026-09-02 assignment. Tracked there as **YV-036**:
  `ApastambaParibhasaSutra-Kapardisvamin-Haradatta-sd4607.txt` (Bibliotheca Sanskrita No. 2;
  it fills an EMPTY stub already declared in Youvan's corpus) and `ApastambaSravani-sd4609.txt`
  (not held there at all). **The Āpastamba _Dharmasūtra_ editions `sd4605` and `sd4617` stay
  here** — a praśna of a Kalpasūtra, but its genre is dharma. Do not move them on the author.
- `Samhita/GargaSamhita/GargaSamhita-KrishnaSahasranamaStotra-VAISHNAVA-sd3003.txt` — **REMOVED 2026-09-08** (Youvan already holds it digitised as `krishna_sahasranama_stotram_garga`, 127 units). Was the **devotional Vaishnava** Garga Samhita, Ashvamedha
  Khanda ch. 59, not the Jyotish work. Digitised and relocated to
  `Tushar/Youvan/texts/Stotra/KrishnaSahasranamaStotram/`. See `DECISIONS.md` 2026-08-23.
- `Muhurta/MuhurtaMartanda/raw_muhurta_martanda_ocr.txt` — **produced here**, not fetched:
  `pdftoppm -r 300 -gray` then `tesseract -l san+hin --psm 6` over the sibling PDF.
  Substantively corrupt and a three-layer commentary edition; see its `README-OCR.md`.
- `Dharmashastra/{4605,4617}.txt` — Āpastamba-Dharmasūtra with Haradatta's Ujjvalā
  commentary (ed. Mahādeva Śāstri, Mysore 1898). `ApastambaParibhasaSutra-Kapardisvamin-Haradatta-sd4607.txt` — Āpastamba-Paribhāṣā-Sūtra.
  `ApastambaSravani-sd4609.txt` — **identified 2026-09-02: the `Āpastamba-ukta Śrāvaṇī`**, a *prayoga* (ritual
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

- **`GargaSamhita`'s `GargaSamhita-KrishnaSahasranamaStotra-VAISHNAVA-sd3003.txt` is the wrong Garga Saṃhitā.** Its colophon reads
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
> each recorded in its own section at the end of this file. **Also supplied, rights noted and
> held rather than refused: `PrasnaMarga`, `GargaHora`, `SarvarthaChintamani`, and a
> `Bijaganita`.** The cost estimate above was not wrong — the mūla/ṭīkā separation it names is
> still outstanding for all of them.
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

### Praśna Mārga — supplied 2026-09-02; rights RECORDED, not a rejection

`Panangadu_Nambudhiri_-_Prasna_Marga_(Part_I).pdf`, 745pp, 18 MB, no text layer. Priority #5
of the eleven. **Held. The rights position below is recorded for the review surface, not acted on** — per Rupali, 2026-09-02: acquire the data, note the terms, and let her judge publication.

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
Those describe `Muhurta/MuhurtaMartanda/MuhurtaMartanda-Mohanarama-Martandavallabha-154pp.pdf`, **154 pages of `tiff2pdf`-wrapped CCITT
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

### Garga Horā Śāstra — supplied 2026-09-02; rights RECORDED, not a rejection

`Garga Hora Shastra Pathak K.K..pdf`, 158pp, 6.5 MB, no text layer, **no digitiser stamp** (so
no CC-0 claim — unlike the eGangotri scans). Priority #9. **Held** at
`Hora/Parashari/GargaHora/raw/GargaHora-Pathak-Ranjan.pdf`; rights noted below.

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

**Already held, never OCR'd.** `Siddhanta/SuryaSiddhanta/SuryaSiddhanta-SudhakaraDvivedi-BibliothecaIndica-345pp.pdf`, 345pp, `no-text`
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

**The quality split is the finding, and it is provable on a single shared verse.** `SiddhantaShiromani-Grahaganitadhyaya-purvardha-Anandashrama110-sd7404.txt`
and `SiddhantaShiromani-Grahaganitadhyaya-purvardha-Anandashrama-sd1139.txt` both contain the maṅgala verse `॥६॥`:

| | text of `॥६॥` |
|---|---|
| `SiddhantaShiromani-Grahaganitadhyaya-purvardha-Anandashrama110-sd7404.txt` | `वेदस्य चक्षुः किल शास्त्रमेतत् प्रधानताऽङ्गेषु ततोऽस्य युक्ता। अङ्गैर्युतोऽन्यैः परिपूर्णमूर्तिश्चक्षुर्विहीनः पुरुषो न कश्चित्॥६॥` |
| `SiddhantaShiromani-Grahaganitadhyaya-purvardha-Anandashrama-sd1139.txt` | `पधानवाप्रवेन्यू वोऽश्य युक्ता। मुपवा चाइगष्षेप्रय ने नोच्यो। अझै तोम्पैः परिपूर्ण मानि-` |

Same verse, same work, one clean and one unusable. **Do not merge or cross-check these two as
if they were independent witnesses** — the second is OCR noise, not a variant reading.

| File | Devanāgarī | verse markers | stray Latin | Verdict | Part |
|---|---:|---:|---:|---|---|
| `SiddhantaShiromani-Grahaganitadhyaya-purvardha-Anandashrama110-sd7404.txt` | 426,311 | 935 | **0** | **CLEAN** | *Grahagaṇitādhyāya* — Ānandāśrama 110 |
| `SiddhantaShiromani-Goladhyaya-uttarardha-Anandashrama122-sd8252.txt` | 560,002 | 735 | **0** | **CLEAN** | *Golādhyāya* — Ānandāśrama 122, Vāsanābhāṣya + Marīci |
| `SiddhantaShiromani-Lilavati-uttarardha-Anandashrama107-sd8244.txt` | 220,262 | 364 | 1 | clean | *Līlāvatī* — Ānandāśrama 107, two commentaries |
| `SiddhantaShiromani-Ganitadhyaya-GirijaprasadDvivedi-hindi-sd1274.txt` | 532,141 | 550 | 34 | poor OCR | whole Siddhānta Śiromaṇi + Prabhā Hindi commentary |
| `SiddhantaShiromani-Grahaganitadhyaya-purvardha-Anandashrama-sd1139.txt` | 333,191 | 603 | 63 | poor OCR | *Grahagaṇita*, Vāsanābhāṣya + Śiromaṇiprakāśa |
| `SiddhantaShiromani-Bijaganita-Abhyankar-sd3328.txt` | 23,141 | 83 | 165 | **rejected** | *Bījagaṇita* + English, S.K. Abhyankar |

Five PDFs accompany them, all `no-text` scans, held under `raw/`: `1706778372` (Ānandāśrama 107,
Līlāvatī — the page witness for `SiddhantaShiromani-Lilavati-uttarardha-Anandashrama107-sd8244.txt`), `1706617850` (Ānandāśrama 122, Golādhyāya — witness
for `SiddhantaShiromani-Goladhyaya-uttarardha-Anandashrama122-sd8252.txt`), `1706607175` (175pp, Sanskrit + commentary, *kṣetravyavahāra* sections),
`1696318554` (53pp — **misidentified on first pass as "an errata table"**; it is a complete
**Līlāvatī, Benares Sanskrit Series No. 153**, edited by the pandits of the Benares Sanskrit
College under **G. Thibaut** — 19th century and unambiguously public domain. The first pass
sampled pages 1–5, hit an `अशुद्धम्` corrigenda leaf, and stopped. **Sampling the front of a
scan identifies its front matter, not the volume**), `1736590500` (Hindi tr. by Pandit Udai Narain
Singh of Madhurapur, Muzaffarpur). One carries a **new digitiser stamp variant** the classifier
had not seen — `Digitized By Siddhanta eGangotri Gyaan Kosha` — and note it does **not** say
CC-0, unlike the Dharmasindhu and Muhūrta Mārtaṇḍa stamps. Do not infer CC-0 from the word
eGangotri.

**Rights.** The Ānandāśrama Sanskrit Series files carry `शके १८५९` (1937 CE) and `शके १८७३`
(1951 CE), consistent with the series volume numbers; the mūla is 1150 CE and unambiguously
public domain. **The editorial apparatus's status is not established here and is not asserted** —
it is very likely clear, but nobody has checked, and this file has already recorded one
"public-domain work ≠ public-domain file" failure today (G26). **`SiddhantaShiromani-Bijaganita-Abhyankar-sd3328.txt` is Prof. S.K.
Abhyankar's modern edition and English translation for Bhaskaracharya Pratishthana Pune**, which
it calls its "maiden publication", carrying 1978/1980/1991. **Rights noted, not a bar — it is
staged**, and it is the corpus's only *Bījagaṇita*, the fourth part of Siddhānta Śiromaṇi.

**Still missing: a clean *Bījagaṇita*.** Three of four parts are covered; the algebra survives
only in the rejected Abhyankar file and inside the poor `SiddhantaShiromani-Ganitadhyaya-GirijaprasadDvivedi-hindi-sd1274.txt`.

**Upstream URLs are unrecorded** — the files arrived by numeric id (an archive.org / e-library
convention) rather than by link. Record them when known; §"Held sources" already carries four
Dharmaśāstra `.txt` files with `_unrecorded_` provenance and that gap has cost real time.

#### Structure of the three clean files — read this before writing a converter

Measured 2026-09-02. **They are commentary editions, and a naive extraction produces a corrupt
text.** Three findings, in the order they were got wrong and then right:

1. **Indentation does NOT mark verse.** Front matter indents quoted verses at three tabs, which
   looks like a clean signal. In the body it is the opposite: **705 of 707 verse-ending lines
   in `SiddhantaShiromani-Grahaganitadhyaya-purvardha-Anandashrama110-sd7404.txt` sit at zero tabs**, and three-tab lines almost never end a verse. Do not build
   on the tab.
2. **Verse numbers repeating is NOT duplication.** Collapsing the whole file gives "verse 1"
   eighteen times in `SiddhantaShiromani-Goladhyaya-uttarardha-Anandashrama122-sd8252.txt`, which reads exactly like the `taittiriya_samhita` defect. It is
   not: **numbering resets per chapter**, so those are eighteen different chapters' opening
   verses. **Segment by colophon before numbering anything**, or a correct text will be
   "deduplicated" into ruin.
3. **The commentary also ends in `॥N॥`**, so the terminator alone does not identify mūla. Marīci
   prose is introduced by `म०टी०—` and by the `अथ … आह—` formula, and cites the mūla by
   *pratīka* only (`उपजातिकयाऽऽह—भुजोऽक्षमेति`). Length separates the bulk but not cleanly:
   mūla runs ~40–75 characters, commentary is either very short (`स्पष्टार्थम्॥२॥`,
   `स्पष्टम्॥१॥२॥` — "the meaning is clear", covering a verse range) or long prose above ~120.

**These editions also carry Bhāskara's own *Vāsanā*** auto-commentary alongside the later Marīci
and Mitākṣara ṭīkās. That is three apparatus layers, one of them authorial — decide deliberately
what the corpus holds, rather than letting a regex decide.

**Authenticity is settled**, so the remaining work is purely structural:
`इति श्रीमहेश्वरोपाध्यायसुतभास्कराचार्यविरचिते सिद्धान्तशिरोमणिवासना` — Bhāskara II's standard
self-identification as son of Maheśvara Upādhyāya.

*Do not convert these on a percentage.* A candidate extraction scored 72–91% contiguous verse
numbering, and the corpus already carries three fabricated texts and two with doubled verses,
every one of which passed a numbering check. Follow `scripts/sanskrit-convert/apastamba.py`:
block on duplicate or misordered numbers **within a segmented chapter**, record absences rather
than invent them, and validate against an external witness before writing JSON.

### Sarvārtha Cintāmaṇi — supplied 2026-09-02; rights RECORDED, not a rejection

`SarvarthaChintamani-VyankateshSharma-Bhasin-sd1267.txt`, 1.0 MB. Priority #4. **Held** at `Hora/Parashari/SarvarthaChintamani/SarvarthaChintamani-VyankateshSharma-Bhasin-sd1267.txt`;
rights recorded below, not acted on.

> Sagar's *"Search-Light on Indian Astrology"* / Aryan Miscellany —
> **The Sarvarth Chintamani of Vyankatesh Sharma, translated into English by J.N. Bhasin**
> Ranjan Publications, 16 Ansari Road, Darya Ganj, New Delhi 110002

The publisher's note dates it: *"sadly over delayed due to the sudden demise of its renowned
author Sh. J.N. Bhasin"*, completed from his manuscript by **S.S. Sareen**. Bhasin died in 1993,
so this is a mid-1990s commercial translation from a publisher still trading — the same class as
the Raman, Pathak and Abhyankar editions rejected the same day. Latin characters outnumber
Devanāgarī 375,617 to 177,359.

**It IS the right text, and that was worth confirming** because `sarvartha` is one of G26's nine
collisions, having matched Pūjyapāda's Jain **Sarvārthasiddhi** on SARIT. Tested against both:
jyotiṣa markers are dense (`लग्न` 496, `दशा` 250, `ग्रह` 238, `राशि` 183, `भाव` 153) while every
distinctive Jain marker is **zero** — `अजीव`, `तत्त्वार्थ`, `आस्रव`, `संवर`, `निर्जरा`,
`पूज्यपाद`. (`जीव` at 145 is non-diagnostic; it is an ordinary word.) So the rejection is on
rights, not identity.

**It also produced G32**, which nearly cost a good source. A `॥` (U+0965) verse-marker probe
scores this file **0**, because it uses `।।` — two U+0964 single daṇḍas — throughout. Its real
count is **1,956**. A zero from that probe reads as "no verse structure" and is exactly the kind
of confident absence that gets acted on. The three Siddhānta Śiromaṇi files were re-checked and
are unaffected: they use U+0965 exclusively, so those counts stand.

**What would source this text:** a Devanāgarī edition of Veṅkaṭeśa Śarmā's original that is not a
modern translator's volume. Still absent from all seven surveyed channels.

## Rights are RECORDED, never a reason to discard a source

**Decided by Rupali, 2026-09-02, after the rule was broken four times in one session.**

> *"stop rejecting on the rights, note it. I told you that"*

**The standing instruction is: acquire the data, record the terms, and leave publication to the
review surface.** Rights govern what the corpus *serves* — which is already enforced
mechanically by the draft-field allowlist in astroacharya's `seed_texts.py` (see
`../CLAUDE.md` §"Uniform JSON schema") — and by G6, which keeps unproofed OCR in the raw tier.
Neither of those is a reason to refuse a file, and **the sources tree is not a publication.**

So for any supplied source, whatever its copyright page says:

1. **Stage it** under `sanskrit-texts-sources/`.
2. **Record the terms** — publisher, date, edition, and the exact wording of any reservation.
3. **Do not delete it, and do not decline to hold it.** Note the position and move on.

### Sources deleted in error, 2026-09-02 — needs re-supplying

Four supplied sources were treated as refusable on rights grounds; two were **deleted from
`~/Downloads` with `/bin/rm`**, which does not use the Trash. **Rupali re-supplied three of the
four the same day and they are now staged.**

| File | Text | Status |
|---|---|---|
| `SarvarthaChintamani-VyankateshSharma-Bhasin-sd1267.txt` | **Sarvārtha Cintāmaṇi** — J.N. Bhasin tr., Ranjan Publications | ✅ re-supplied → `Hora/Parashari/SarvarthaChintamani/SarvarthaChintamani-VyankateshSharma-Bhasin-sd1267.txt` |
| `SiddhantaShiromani-Bijaganita-Abhyankar-sd3328.txt` | **Bījagaṇita** — S.K. Abhyankar, Bhaskaracharya Pratishthana | ✅ re-supplied → `Siddhanta/SiddhantaShiromani/SiddhantaShiromani-Bijaganita-Abhyankar-sd3328.txt` |
| Garga Horā PDF | K.K. Pathak, Nishkaam Peeth | ✅ re-supplied → `Hora/Parashari/GargaHora/raw/GargaHora-Pathak-Ranjan.pdf` |
| **Praśna Mārga PDF** | B.V. Raman, Motilal Banarsidass | ⚠ **still outstanding — re-supply needed** |

All three re-supplied files were checksum-verified against the originals on staging. The
identification and structural work survived in the sections above throughout and did not need
redoing — only the data had been lost.

**Why it happened, stated so it does not recur.** Each refusal was individually argued and
looked careful — a copyright page quoted, a comparison drawn to the previous one. That is what
made it hard to notice they were four instances of overriding a decision that had already been
made by the person whose call it was. **A judgment the user has reserved is not yours to make
well.**

#### The other two clean files are PARTIAL volumes, and neither carries a verse-count witness

Measured 2026-09-02, after `goladhyaya` was digitised successfully from `SiddhantaShiromani-Goladhyaya-uttarardha-Anandashrama122-sd8252.txt`. **Do not
assume the Golādhyāya recipe transfers** — what made it safe was a property of that volume,
not of the series.

| File | Covers | Verse-count witness |
|---|---|---|
| `SiddhantaShiromani-Goladhyaya-uttarardha-Anandashrama122-sd8252.txt` — Golādhyāya | complete | **Yes** — a ToC giving every chapter's last verse. This is what made digitisation defensible |
| `SiddhantaShiromani-Lilavati-uttarardha-Anandashrama107-sd8244.txt` — Līlāvatī | **`उत्तरार्धरूपो द्वितीयो भागः`** — the SECOND half only, from `क्षेत्रव्यवहार` onward | **None** — the file opens on its title page and goes straight into the text |
| `SiddhantaShiromani-Grahaganitadhyaya-purvardha-Anandashrama110-sd7404.txt` — Grahagaṇita | **`(पूर्वार्धः)`** — the FIRST half. Its own preface says `ग्रहगणिताध्यायेऽस्मिन्नेकादशाधिकारा वर्तन्ते`, eleven adhikāras, of which this volume carries **three**: मध्यम, स्पष्ट, त्रिप्रश्न | **Partial** — the `अनुक्रमणिका` lists chapters but **no verse numbers** |

**So a Līlāvatī or Grahagaṇita digitisation has no independent check available**, and contiguity
alone is exactly the evidence G31 records as worthless: all three fabricated texts, and both
doubled ones, passed a numbering check. `goladhyaya`'s converter rejected verses numbered above
the ToC maximum — 7 of its 8 chapters land on the predicted last verse — and none of that is
possible here.

**Before digitising either, get a witness.** Options, in preference order: a complementary
volume (the Līlāvatī *pūrvārdha* and the Grahagaṇita *uttarārdha* are separate Ānandāśrama
numbers and would supply both the missing halves and, if they carry one, a ToC); a printed
edition's verse counts; or a second digitisation to diff against. Contiguity is not a witness.

#### The witness arrived: a second, independent Līlāvatī

**`SiddhantaShiromani-BenaresSanskritSeries-Thibaut-53pp.pdf` is the complementary volume the section above asks for**, and it was already
in the tree — supplied 2026-09-02 with the other ten files and filed as an errata leaf.

| | `SiddhantaShiromani-Lilavati-uttarardha-Anandashrama107-sd8244.txt` | `SiddhantaShiromani-BenaresSanskritSeries-Thibaut-53pp.pdf` |
|---|---|---|
| Edition | Ānandāśrama 107, Śaka 1859 = 1937 | **Benares Sanskrit Series 153**, ed. under G. Thibaut, 19th c. |
| Form | clean machine-readable Devanāgarī | scan, no text layer, 53pp |
| Covers | `उत्तरार्धरूपो द्वितीयो भागः` — second half, from `क्षेत्रव्यवहार` | **from `परिभाषा`** — its ToC runs `परिभाषा · संख्यास्थाननिर्णयः · सङ्कलितव्यवकलिते · गुणनप्रकारः · भागहारः · वर्गः · वर्गमूलम् · घनः · घनमूलम् · भागजातिः · … · त्रैराशिकम्` |

So between them the two halves are covered, **and they are independent editions of the same
text a century apart** — which is a stronger position than either alone. A verse present in
both, agreeing, is corroborated; a verse in only one is a finding.

**Do not merge them into one file without recording which edition each verse came from.**
`rule:discernment-checks` §5 — comparing unlike things is how this corpus produced two of its
worst numbers, and two editions of one work are exactly the case where the distinction stops
being obvious.

Thibaut also edited the Pañcasiddhāntikā whose edition `CANONICAL_COUNTS.md` records, so the
same hand is behind two of this corpus's witnesses.

##### …and why Līlāvatī is harder than Golādhyāya even with the witness in hand

**In a mathematics treatise the numerals are the CONTENT.** Golādhyāya is astronomy in verse,
so a Devanāgarī number between daṇḍas is almost always a verse number. Līlāvatī is arithmetic:
worked examples print quantities in the same script, between the same daṇḍas, on the same
lines. Measured on the Benares OCR — 262 markers, **84 descents, only 33% of steps are +1**,
range 1..196 where the work has ~272 verses. The Golādhyāya converter's core assumption does
not hold here.

So the Benares volume is a good **corroborating witness for text** — its OCR reads at 81–88%
word accuracy on probe words, against the Sūrya Siddhānta scan's 6–34% — but **not** a witness
for numbering. Getting Līlāvatī right needs a way to separate a verse number from a quantity,
and neither file supplies one on its own.

*The pairing is still the way in:* `SiddhantaShiromani-Lilavati-uttarardha-Anandashrama107-sd8244.txt` is clean text for the second half and can be read
for structure, while the Benares scan covers the first half and can corroborate wording. Neither
alone is enough, which is the honest position and is worth more than a plausible merge.

### Pañcasiddhāntikā — a SECOND edition, and it is wanted for its ordering

Supplied 2026-09-02 as `1736760325.pdf`, 422pp, 54 MB, `no-text` scan. Staged at
`Siddhanta/Panchasiddhantika/raw/Panchasiddhantika-Prakashika-Lahore-1930.pdf`.

| | `Panchasiddhantika-ThibautDvivedi-sd8801.txt` | this scan |
|---|---|---|
| Edition | **Thibaut & Sudhākara Dvivedī** — the edition `CANONICAL_COUNTS.md` names | **Pañcasiddhāntikā-prakāśikā**, Moti Lal Banarsi Dass / Punjab Sanskrit Book Depot, **Lahore 1930**, dedicated to F. Max Müller |
| Form | clean text, bilingual | scan, bilingual (Sanskrit body, English translation at the back) |
| Rights | — | *"All Rights Reserved"*, 1930. **Noted, not a bar** |

**Why a second edition is worth 422 pages of OCR.** `Panchasiddhantika-ThibautDvivedi-sd8801.txt` is genuine — all five siddhānta
names, and decisively the epoch **427 present / 425 absent** where the deleted forgery said 425
— but **it is not linear**: its 18 `CHAPTER` headings sit at offsets 498271–678463, which is the
English translation at the back of the book, and the Sanskrit colophons run out of order (6th
adhyāya @199821, 10th @214926, 4th @332344, 18th @497654). An offset table cannot segment it.
A second witness gives the adhyāya sequence independently.

Identified by sampling the **middle** (G34): p.200 carries `पञ्चसिद्धान्तिकाप्रकाशिका` with
mandaphala/kendra computation, and p.410 the English *"When Mars is retrograde in Pisces…"*.
The title page alone would have given only the imprint.

### Bṛhadāraṇyaka — a DEVANĀGARĪ edition, which is what both other sources lacked

Supplied 2026-09-02 as `1781600259.pdf`, **989pp**, 57 MB, `no-text` scan. Staged at
`Upanishad/shukla-yajurveda/Brihadaranyaka/raw/Brihadaranyaka-devanagari-989pp.pdf`.

**It answers both blockers recorded against this text on the same day:**

| | held `brinew-proofed.html` | GRETIL TEI | this scan |
|---|---|---|---|
| Script | Devanāgarī | **IAST only** — 0 Devanāgarī | **Devanāgarī** |
| `SF` contamination | **4,317 markers** | 0 | to be measured |
| Citation structure | none usable | 773 attribute-less `<div>`s | **running heads carry `3.1.6`, `3.1.8`, `6.4.5`** |

**The running heads are the witness.** Every page prints the canonical
**adhyāya.brāhmaṇa.mantra** reference — `[3.1.6`, `3.1.8]`, `6.4.5] BRHADARANYAKA UPANISAD 933` —
which is exactly the three-level structure the held text cannot express and the GRETIL markup
does not encode.

Bilingual: Devanāgarī mūla (`पृथिवी रसः, पृथिव्या आपः, अपामोषधयः … ॥ १ ॥`) with facing English,
`SECTION` headings, and Śaṅkara's commentary — from the translator's preface it is very likely
Swāmī Mādhavānanda's Advaita Ashrama edition.

Identified by sampling the **middle and end** (G34); the front matter is translator's preface and
would have said nothing about the structure.

**OCR'd 2026-09-02, and the reading FAILS the gate — measured 2026-09-04.** Both passes ran
(`BriDevanagari.san.txt`, `BriDevanagari.hin.txt`). The scan is genuine, correctly identified and
public-domain-shaped; the *reading* of it is not usable on a citation surface:

| measure | result |
|---|---|
| Devanāgarī chars, `san` pass | 471,649 — but only **94,863** on Devanāgarī-dominant lines. The rest is the edition's English half misread as Devanāgarī |
| word accuracy, mantra 1.1.1 | **27 of 53 words (51%)** appear verbatim in the held text |
| systematic substitution | ए→प — `पव` 53, `पवं` 43, `पष` 57 where `एव` / `एवं` / `एष` belong |
| `याज्ञवल्क्य` | correct **5** times against **12 distinct corrupt spellings** |
| `hin` pass | **worse** — the attested incipit `उषा वा अश्वस्य` does not occur in it at all |

`उषा वा अश्वस्य मेभ्यस्य शिरः । सू्ेश्वह्ु, धातः प्राणः…` against the true
`…मेध्यस्य शिरः । सूर्यश्चक्षुर्वातः प्राणो…`.

**Same shape as Sūrya Siddhānta, and the same answer: do not convert from it (G6).** The value of
this scan is unchanged for the purpose it was acquired for — its running heads are still the only
witness that prints the canonical `adhyāya.brāhmaṇa.mantra` citation, and it is a proofing
reference. It is the OCR, not the book, that is refused.

**A bilingual page is an OCR hazard in itself.** Four fifths of this file's apparent Devanāgarī is
Latin text the `san` pass hallucinated into Devanāgarī. Any character-count check on a bilingual
edition will read as healthy — measure the Devanāgarī-dominant *lines*, not the character total.

## Supplied 2026-09-04 — two scans, and only one of them is what the batch implied

Both arrived together, one named for the Muṇḍaka. **They are different works, and the unnamed
one is not an Upaniṣad at all.** Identified by content per G26 and G34 — sampling the middle and
end, never the front matter, which OCR'd blank on both.

### `TaittiriyaSamhita-Jangamwadi-eGangotri-981pp.pdf` — the Taittirīya Saṃhitā, accented

Supplied as `1784366669.pdf`, **981pp**, 94 MB, landscape two-page spreads, `no-text` tier.
Staged at `Veda/krishna-yajurveda/TaittiriyaSamhita/raw/`.

**Rights: CC-0** — the only text layer in the whole file is the digitiser's stamp, one line
repeated across 981 pages: *"CC-0. Jangamwadi Math Collection. Digitized by eGangotri"*. That is
56,896 characters of provenance and zero characters of text, which is why `classify.py` tiers it
`no-text` rather than `clean`.

**Identified at page 979, by colophon:** `इति तैत्तिरीयसंहितायाः सप्तमकाण्डः समाप्तः ॥ ७ ॥`, under
a running head reading `तैत्तिरीय … संहिता`. Page 950 carries `अम्बे अम्बाल्यम्बिके`, page 700 the
aśvamedha animal lists. The last leaves are an **anukramaṇī index** giving each pratīka with a
number — `इषे (१९५८३)`, `वायव्यं (११२६५)` — which is a citation witness in its own right.

**It is ACCENTED.** Udātta and anudātta marks throughout, so it is a svara witness, and svara
marks are precisely what OCR mangles. Any conversion has to be gated on that, not on word
accuracy alone.

**What it would answer, and what it would not.** The held `taittiriya_samhita` sits at **anuvāka**
granularity — 650 units over 7 kāṇḍas `[145, 75, 55, 82, 120, 66, 107]` — which was verified
2026-09-02 against researched anuvāka counts and is **not in doubt**. This edition is a
**mantra-level** printed witness with the traditional numbering, so what it offers is finer
granularity and an independent accented reading, not a correction to the 650.

**One real defect it could fix now:** the held unit `1.1.1` opens with the śānti-pāṭha and the
edition's own front matter — `ओं शान्तिः शान्तिः शान्तिः ॥ हरिः ओ(३)म् ॥ श्री … गुरुभ्यो नमः ॥
प्रथमकाण्डे प्रथमः प्रश्नः १ १` — and only then the true opening `इषे त्वोर्जे त्वा`. Unlike
Muṇḍaka's defect this is **not an off-by-one**: nothing is shifted, the apparatus is prepended
inside the unit. It is a text-field contamination, fixable from the held HTML alone.

### `Mundaka-GitaPress-Gorakhpur-136pp.pdf` — the named text, and it is the named text

**136pp**, 197 MB, `no-text` tier, from an archive.org derive (its sidecar's identifier is
`/var/tmp/autoclean/derive/mundaka-upanishad-gita-press-gorakhpur`). Staged at
`Upanishad/atharvaveda/Mundaka/raw/` with its page-number sidecar.

Identified at page 130: running head `१२० मुण्डकोपनिषद् [ मुण्डक ३`, over a two-column
**Sanskrit + Hindi** body — Śāṅkara-bhāṣya with facing Hindi (`यहाँ ब्रह्मविद्या समाप्त हुई है`).

**Muṇḍaka does not need it for structure.** It was re-parsed 2026-09-02 onto the canonical
9/13/10/11/10/11 = 64. So this is a **proofing** witness — and, more usefully, a **Hindi
translation** witness for a Vedic corpus that is 0% translated. It is a commentary edition, so the
mūla/bhāṣya split is the same problem Golādhyāya and Sūrya Siddhānta posed.

**Rights: not established.** The early leaves OCR blank, so the scan's own copyright page could
not be read; Gita Press editions are generally still in copyright. **Recorded, not a bar** — G33
and the standing instruction. Serving is gated mechanically by `seed_texts.py`'s allowlist, and
the sources tree is not a publication.

`Mundaka-GitaPress-Gorakhpur-page-numbers.json` is archive.org's leaf→printed-page OCR sidecar.
**Treat it as a hint, not an authority**: every entry in its opening run carries
`"confidence": 0`, and several read a page number as `"3"` or `"11"` where the leaf is unnumbered
front matter.

### The lesson worth keeping: a batch is not an identification

Two files arrived together, one named `Mundaka Upanishad - Gita Press Gorakhpur.pdf` and one
named `1784366669.pdf`. The obvious reading — a book and its companion — is wrong: the second is
a 981-page Saṃhitā from a different Veda in a different layer. G26 records nine sources that were
a different text than their **name** implied; this is the same failure with **adjacency** in place
of a name, and it is cheaper to fall for. Identify every file on its own content.

### Seen 2026-09-04 and NOT staged — `Mundaka_Upanishad_SP.pdf`

*Swami Paramārthananda's Lectures on Muṇḍakōpaniṣad*, 457pp, born-digital (Word 2007), tier
**`clean`** — 29,094 Devanāgarī characters, 0 PUA, mātrā ratio 0.440, so `pdftotext` would extract
it directly. It is the easiest file to read of anything supplied this week, and it is still not
corpus material.

**It is a modern teaching commentary, not an edition of the text**: 712,180 Latin characters
against those 29,094 Devanāgarī. What it contains is a contemporary teacher's lectures, in
English, quoting the mūla. This corpus holds mūla.

**Left in place, not staged and not deleted.** Recorded here so the next person who finds it does
not have to re-decide — and because the reason is a scope judgement rather than a defect, which is
the kind of thing that gets silently re-litigated. If it is ever wanted, it would be as a
*verification* reference for a human translator, never as a text or a translation source: the
publication gate takes verified human translation only, and this is a third-party work in
copyright besides.

## Supplied 2026-09-04 (second batch) — two of the four unsourced texts, both digitised same day

`JatakaTattva-Mahadeva-SubrahmanyaSastri-sd1223.txt` and `JaiminiSutra-Upadesa-VidyabhavanSeries57-sd1154.txt`, numeric filenames in the sanskritdocuments style. Identified by content
per G26/G34.

### `JaiminiSutra-Upadesa-VidyabhavanSeries57-sd1154.txt` — Jaimini Sūtra, and it is the cleanest source acquired all day

`महर्षि-जैमिनिप्रणीतं (उपदेशापरनामकं) जैमिनि-सूत्रम्`, *Vidyābhavan Prācyavidyā Granthamālā-57*,
with the **Tattvādarśa** commentary of Pt. Sītārāma Śarmā Maithila (Jyotiṣācārya Jhā). Staged at
`Hora/Jaimini/JaiminiSutras/raw/JaiminiSutra-Upadesa-VidyabhavanSeries57-sd1154.txt`.

**129,358 Devanāgarī characters and ZERO Latin** — a real digitisation, not OCR of a scan, so the
gate that blocked five texts earlier the same day does not apply at all. 410 markers of the
**doubled-single** form `।। N ।।`; a probe for `॥ N ॥` scores zero (G32).

**Partial by transmission, not by damage:** it carries exactly ONE adhyāya colophon, 127
characters from the end — `…जैमिनिसूत्रतिलके द्वितीयाध्यायः समाप्तः` — so it holds **adhyāyas 1–2
of the canonical 4**. Digitised the same day: 408 sūtras across 8 pādas.

### `JatakaTattva-Mahadeva-SubrahmanyaSastri-sd1223.txt` — Jātaka Tattva, bilingual, and its markers are not daṇḍas

`श्री महादेवकृतं जातकतत्त्वम्` — *Mahādeva's Jātaka Tatva, with an English Translation by
Panditabhushana V. Subrahmanya Sastri, B.A., Asst. Secretary to the Govt. of Mysore (Retd.)*.
Staged at `Hora/Parashari/JatakaTattvam/raw/JatakaTattva-Mahadeva-SubrahmanyaSastri-sd1223.txt`.

**97,821 Devanāgarī against 280,689 Latin** — English-dominant, with an English index at the end
that is apparatus and must not become text.

**The marker form is the finding.** Probes for `॥ N ॥` *and* `।। N ।।` both score **ZERO**. The
verse numbers print as Devanāgarī digits followed by a full stop — `२०८. सुतेशदृष्टेऽङ्गे…` —
**2,270 of them**. This is the same shape that made Garga Horā look markerless: *a text can look
unsegmentable and be densely numbered, and the probe is what is wrong.* Digitised the same day:
17 chapters, 2,277 sūtras.

**The English translation is a separate work in copyright and never reaches a served field** —
`english` is empty and `status` is `untranslated` throughout, asserted by a test that fails if a
single Latin character survives into any `text`.

## `brahmasphuta_siddhanta` — acquired 2026-09-04 as REFERENCE, deliberately not a corpus text

Fetched from **both** channels and staged at `Siddhanta/BrahmasphutaSiddhanta/raw/`:
`…-GRETIL-TEI.xml` plus `…-TITUS-part{1..5}-ch{12,18,19,20,21.17-23}.htm`.

**Correction to the entry above:** the TITUS path recorded there
(`texte/etcs/ind/aind/klskt/mathemat/brsphsd/`) serves a "not yet available" placeholder. The real
files are `brsph001.htm`–`brsph005.htm`, and the working host is **`titus.fkidg1.uni-frankfurt.de`**
— `titus.uni-frankfurt.de` 403s/404s directory listings.

**Correction to the markup assessment:** the GRETIL TEI has **zero `<div>` elements** — its own
boilerplate note claiming "unnumbered div elements are used to structure the text" is generic
template text that does not describe this file. Structure lives in `xml:id` on `<lg>` and `<l>`,
e.g. `BSS_18.42a`, so chapter/verse/pada are all machine-extractable from the id alone. Verified
independently: 0 divs, 214 `<lg>`, 645 `xml:id`s. **This is better than the Bṛhadāraṇyaka failure
mode, not the same as it.**

Contents confirmed against the canonical 24 chapters: 12 (66 verses), 18 (102), 19 (20), 20 (19),
21.17–23 (7) — **214 verses / 431 padas**, so "partial" is accurate. Script is IAST throughout.

**No `text_id`, no corpus JSON, by decision.** Rupali confirmed 2026-09-04 that this material is
for internal reference while building astroacharya's logic, not for publication. The
`sanskrit-texts` repo is public and its contents are served by astroacharya's `/texts` API, so the
gitignored sources tree is where reference-only material belongs and the licence question does not
arise there. Licences recorded verbatim: GRETIL **CC BY-NC-SA 4.0**; TITUS *"No parts of this
document may be republished in any form without prior permission by the copyright holder"*
(© TITUS Project, 8.12.2008).

## Supplied 2026-09-14 — eight items, one exact duplicate, one mislabelled zip that turns out to unblock a named gap

All seven from `~/Downloads`, plus two archive.org text fetches. `classify.py` plus
chars-per-page (`pdftotext` byte count / `pdfinfo` page count) run on every PDF.

### `saravaliofkalyan01kalyuoft.pdf` — NOT staged, byte-identical to the held copy

**MD5 `a893...42c1` matches exactly** the already-held
`Hora/Parashari/Saravali/Saravali-Kalyanavarma-archiveorg.pdf` — same 17,278,726 bytes, same
`pdfinfo` metadata (`Recoded by LuraDocument PDF v2.28`, `CreationDate` 2009-01-21) down to the
second. This is the same archive.org derive downloaded twice. Not staged; nothing to record
beyond this note.

### `PingreeVYJ.zip` → two files — **not Vedāṅga Jyotiṣa.** It is Pingree's Vṛddhayavanajātaka
of Mīnarāja, and it is the exact witness commit `5039783` (this morning) named as missing

The filename reads as "Vedanga Jyotisha" (VYJ); it is not. Both halves open with the same
title page: *Gaekwad's Oriental Series, Oriental Institute Baroda, no. 162/163,
"VṚDDHAYAVANAJĀTAKA OF MĪNARĀJA"*, ed. David Pingree, Professor of the History of
Mathematics, Brown University, 1976. Vol. II's foreword states explicitly: *"The present
volume contains chapters 40-71 of the text and the four appendices."*

`classify.py`: both tier `latin` (21,448 and 59,690 Roman letters respectively, 0 Devanāgarī —
an English critical apparatus around a romanised text, not a script problem). Chars-per-page:
Vol. I 453pp / 52,279 chars = **115/pp**; Vol. II 415pp / 122,007 chars = **293/pp**. Low
density, consistent with a scanned critical edition (introduction, apparatus, romanised verse)
rather than continuous prose.

Staged at `Hora/Parashari/MinarajaYavanajataka/raw/`:
- `MinarajaYavanajataka-Pingree-Vol1-GaekwadOrientalSeries162-Baroda1976-453pp.pdf`
- `MinarajaYavanajataka-Pingree-Vol2-Ch40-71-GaekwadOrientalSeries163-Baroda1976-415pp.pdf`

**Why this matters immediately:** commit `5039783` (`fix(corpus): minaraja_yavana_jataka is
two halves with different provenance`, landed the same day this batch arrived) declared that
the held text's chapters 40–71 (the Uttarakhaṇḍa, 1,887 śloka, 6% carrying detectable OCR
noise) have **NO SOURCE ANYWHERE** — added 2026-06-20 already translated, no source file
committed then or since — and named *"Pingree's edition of the Vrddhayavanajataka"* as *"the
obvious unconsulted witness"* that had not been consulted. Vol. II of this delivery is exactly
that witness, covering exactly that chapter range (40–71) plus four appendices. Vol. I (ch.
1–~39) is a second, independently-edited witness for the already-sourced Pūrvakhaṇḍa. Neither
is a proofread transcription — both are romanised critical-edition scans — so this unblocks
*verification against a witness*, not a ready-to-ingest source; someone still has to read Vol.
II against the 1,887 held śloka. Flagging this prominently because it directly answers a named
open item, not a general acquisition.

### Two Deva Keralam scans — IDENTITY UNVERIFIED, and the held `ChandraKalaNadi` row is already `REFUSED` for exactly this class of material

Both `no-text` per `classify.py` (0 extractable characters, `pdfimages` reports image
content) — chars-per-page is undefined/0 for both, so identity **cannot** be checked without
OCR. Recording them as supplied, not as Chandra Kala Nadi, per G26.

- `2015.489052.Deva-Keralam.pdf` — 268pp, archive.org id `2015.489052`. Staged at
  `Hora/Nadi/DevaKeralam/raw/DevaKeralam-archiveorg-2015.489052-268pp-IDENTITY-UNVERIFIED.pdf`.
- `Deva-Keralam-3-Chandrakala-Nadi-compressed.pdf` — 322pp, filename implies "book 3" of a
  multi-volume Deva Keralam set. Staged at
  `Hora/Nadi/DevaKeralam/raw/DevaKeralam-3-ChandraKalaNadi-compressed-322pp-IDENTITY-UNVERIFIED.pdf`.

**Neither is identical to what is already held.** The existing `raw/` in the same directory
carries `DevaKeralam-298pp.pdf` (298pp) and `ChandraKalaNadi-Book1-260pp.pdf` (260pp) — both
different page counts from the two supplied here, so these are not re-downloads of the same
scans.

**Read this alongside `INVENTORY.md`'s Acquisition status table before acting on these:** its
`ChandraKalaNadi` row is `REFUSED`, with the note *"Both supplied Deva Keralam scans were
refused on measured OCR quality. The last surviving stub directory."* — a plain reading of
that note is about the two files already in `raw/` (`DevaKeralam-298pp.pdf` and
`ChandraKalaNadi-Book1-260pp.pdf`), not these two. But it establishes that this exact
identity/quality problem has already been evaluated and refused once for this work. These two
new scans are additional/different material for what is functionally the same refused
acquisition target, not a fresh, unevaluated text. Did not touch `INVENTORY.md` — flagging
this cross-reference for whoever picks the OCR work up next.

### `2015.312156.Jataka-Parijata.pdf` — a second witness scan for the held `jataka_parijata`

682pp, archive.org id `2015.312156`, `no-text` per `classify.py` (0 chars, image content).
Chars-per-page undefined (0/682). Staged at
`Hora/Parashari/Jatakaparijatah/raw/JatakaParijata-archiveorg-2015.312156-682pp.pdf` — the
first file in that directory's `raw/`, which held only a `.md` until now.

`jataka_parijata` is already `HELD` (18 chapters / 1,947 units, 100%, sourced from
sanskritdocuments' `jAtakapArijAtaH` stem per the 2026-08-25 survey). This scan is a
**second, independent witness** — useful for cross-checking chapter/verse boundaries, not
needed to establish the text exists.

### Two English-only Garga Horā translations — TRANSLATION WITNESSES, explicitly NOT corpus sources

Same precedent as `ThreeHundredImportantCombinationsRaman` (excluded 2026-06-20, DECISIONS.md:
*"a 20th-c. English work (raw OCR only, no Devanagari shlokas) — does not fit the uniform
schema"*). Both score **0 Devanāgarī characters** — `classify.py` tiers both `latin`.

- `Sage_Gargacharya_-_Garga_Hora.pdf` — 95pp, 207,524 Roman letters, chars-per-page **2,920**
  (dense continuous English prose, not a low-density scan artifact). Identified from the title
  page: *"GARGA HORA by SAGE GARGACHARYA, Translated by R. SANTHANAM, Ranjan Publications, New
  Delhi, Edition 2014"*, foreword by B.V. Raman. Staged at
  `Hora/Parashari/GargaHora/raw/GargaHora-Santhanam-English-translation-RanjanPublications2014-95pp-TRANSLATION-WITNESS-NOT-SOURCE.pdf`.
- `Garga_Hora_by_Sage_Gargacarya.zip` → `garghora.htm` — 271 KB HTML, 232,408 characters after
  tag-stripping, IAST-diacritic English (`Sūrya`, `Candr`, `Mangal` …) — a **different**
  translation style from the Santhanam PDF (which uses plain English planet names), so likely a
  different translator; no translator credit found in the sampled front matter. Staged at
  `Hora/Parashari/GargaHora/raw/GargaHora-English-translation-witness-TRANSLATION-WITNESS-NOT-SOURCE.htm`.

**Why this might matter later:** the held `garga_hora` is `HELD` but incomplete — *"chapter 1
only of 3 / 84 units. Chapters 2–3 carry no printed verse numbers in either OCR pass"*. These
two English witnesses were not checked chapter-by-chapter against that gap in this pass; they
are recorded as witnesses for whoever takes that on, not confirmed to cover chapters 2–3.

### Two archive.org text fetches — not independently re-verified this pass

`mm.txt` (Muhurta Martanda, `in.ernet.dli.2015.307447`) and `pm.txt` (Prashna Marga) were
fetched to scratch per the brief's URLs but **not staged or further processed in this pass** —
out of scope for this batch, which covered the seven `~/Downloads` items. `MuhurtaMartanda`
already has raw material staged (`Muhurta/MuhurtaMartanda/raw/`); `PrashnaMarga` is
`UNSOURCED` per INVENTORY ("Supplied once and unusable; needs re-supply") — these two fetches
may be relevant to that gap but identification and staging is left to a dedicated pass.

### `PingreeVYJ2.pdf` — ADJUDICATED 2026-09-14, and it settles the Mīnarāja P0

Vol. II, 415pp. Its foreword states it *"contains chapters 40-71"* plus four appendices — an
**exact match for the unsourced range** of `minaraja_yavana_jataka`, so there was no ambiguity
about which witness applies. Chapter openings were located directly: ch.40 p.19 · ch.47 p.190 ·
ch.53 p.290 · ch.54 p.291 · ch.62 p.360 · ch.68 p.390.

**Pingree prints in DEVANĀGARĪ, not IAST.** The brief assumed IAST and was wrong. This is the
fact that made the adjudication cheap — the held `text` field compares directly, string for
string, against page renders with no transliteration layer.

**Usable only as page images.** `pdftotext` on the embedded layer is junk (as with Vol. I).
`tesseract -l script/Devanagari --psm 4` at 300dpi beat `-l san`, but the verdict rested on
**direct visual reading of the renders** — these are legible photo-offset reproductions, unlike
Vol. I's ruined layer, and eyeballing beat OCR noise for verse-by-verse comparison.

**Verdict: the Uttarakhaṇḍa is GENUINE.** Six chapters spanning the range agreed with the
witness; none contradicted. The defect is digitisation contamination — running headers, apparatus
sigla and the chapter heading bleeding into `text` ahead of the real verse. Full reasoning and
the worked 55.1 decode: `propagation/state/sanskrit-texts/STATE.md` §P2 Mīnarāja.

### `saravali00kalyuoft` — a SANSKRIT Sāravalī, found 2026-09-14, not yet staged

Found while testing whether the held `saravali01kalyuoft.pdf` had a sibling volume. **The
sibling is `00`, not `02`** — archive.org's multi-volume suffixes are not reliably sequential,
and its metadata API returns **HTTP 200 with an empty object** for an identifier that does not
exist, so the status code is not the existence test. `files: 0` is.

`language: san`, 19MB PDF, **932KB `_djvu.txt` text layer** — where `01` is Santhanam's English
translation at `no-text` tier, which is what forced Sāravalī into the OCR lane at all.

**Identity verified internally, per G26.** The colophons read
`इति कल्याणवर्मविरचितायां सारावल्यां … नाम प्रथमोऽध्यायः` — naming Kalyāṇavarma and the work,
not matched on a filename. Its chapter titles agree with the printed English ToC of the `01`
volume **6 for 6** (शास्त्रावतार / "Birth of Hora Sasthra"; होराशब्दार्थचिन्ता / "Meaning of
Hora"; होराराशिभेदो / "Rasi Description"; ग्रहयोनिभेदो / "Planetary Characters"; मिश्रकाध्यायः /
"Miscellaneous Matters"; कारकाध्यायः / "(Yoga) Karakas") — two independent witnesses in two
languages.

**2,368 verse markers · ~53 numbering resets**, consistent with the 55 chapters the `01` volume
states in print. Held `saravali` is 1,163 verses in one flat chapter.

**OCR damage is systematic and recoverable, which G55 says the ratios cannot tell you.** Its
profile is 100% Devanāgarī / 0 ASCII — identical to the REFUSED Praśna Mārga — but the damage is
a font-confusion set (`ल→ठ/ट`, `र्य→थ`): `प्रियाठापम्` ← प्रियालापम्, `कुटीनं` ← कुलीनं,
`कठहूप्रिय` ← कलहप्रिय. Words are damaged, not destroyed, and **the colophons are clean**.

**OPEN, and not to be resolved by assertion:** under damage-tolerant skeleton matching only
**5 of 40** held verses were located in this source, and the meter difference expected did not
appear (92 vs 93 Devanāgarī chars/verse — indistinguishable). That is consistent with partial
overlap *or* with a 12-character exact window being too strict for per-character damage. **The
instrument is not yet good enough to say which**, and no status change follows from it.

## Shlokam — `shlokam.org` — added 2026-09-23, recorded not ingested

Added at Rupali's request after it came up while searching for the Jaimini commentaries.
**Nothing has been taken from it**, and the two reasons are independent — either alone is
enough, and neither is about quality.

**What it offers.** Per verse: Devanāgarī with verse numbers, IAST, English translation,
word-by-word grammatical breakdown, and running commentary — for Māṇḍūkya that is **Śaṅkara's
Bhāṣya with Ānandagiri's Ṭīkā**. Multi-script display from Assamese to Urdu. Free, ad-free,
audio in places. Coverage is the devotional-Vedāntic core: Gītā, Bhāgavatam, Upaniṣads,
stotras — not jyotiṣa, so it is no help with the three Jaimini works that prompted the look.

**Reason 1 — it is commentary, and this corpus holds none, by decision.** **G6**: a `text_id`
is a citation surface, mūla only. That is not an oversight to be corrected by a good source —
Abhyankar's own Sanskrit commentary was deliberately **not** captured from an edition already
in hand, and `prashna_marga` was assessed specifically on whether its markers numbered the mūla
or the commentary. Taking Śaṅkara's Bhāṣya from here would be the first commentary in the
corpus and a reversal of G6, not an acquisition.

**Reason 2 — no licence.** Terms unestablished after checking the homepage, `/about/` (404),
`/info/about`, a text page and WHOIS. Full record and the verbatim self-description:
`LICENSES.md` §5. Default is all-rights-reserved.

**A quality signal worth recording separately, because it is the shape this corpus has already
paid for.** The site states of its non-English translations, in its own words:

> "Die deutsche Übersetzung wurde von Software erzeugt" — *the German translation was
> generated by software*

The same notice appears for French, Spanish and others. It is candid, and it is exactly the
class the 2026-09-16/17 campaign moved **67,820 served values** out of `english`/`hindi` for.
Its *English* is not claimed to be machine-generated — but a site that machine-generates one
translation layer and names no source edition for any of them is one whose English needs the
same scrutiny before it could be served.

**Where it could legitimately be useful,** if either reason is ever lifted: as a **second
witness for proofreading Devanāgarī** we already hold — the use `CANONICAL_COUNTS.md`
§"The second witness earns its keep" describes. That reads a source without redistributing it,
so the licence question does not arise, and it does not touch G6 because no commentary enters
the corpus. Māṇḍūkya itself needs nothing: **12 verses against canonical 12, authority `firm`**
(Deussen vol.2 pp.605–637).

## Supplied 2026-09-23 — six PDFs, three of them the Jaimini commentaries

Rupali supplied six files after the Jaimini search recorded all three commentaries as
`UNSOURCED`. **Three are the wanted works, one is a reference acquisition, two are not what
their names suggest.** Every identification below is from the file itself, not its filename —
which mattered, because the filenames misled twice.

| file | what it actually is | verdict |
|---|---|---|
| `Jaimini Sutra with Vyakhya - Neelkanth _882_Gha_Alm_5_Shlf_1…pdf` | **Nīlakaṇṭha's Subodhinī**, Jammu MS 882-घ | **wanted** |
| `Jaimini Sutra Vritti Subodhini of Sarveshvarananda…pdf` | **Nīlakaṇṭha's Subodhinī**, printed 1947, adhyāya 3 | **wanted** |
| `130369490-Kalpa-lataa-in-Astrology.pdf` | **Somanātha's Jyotiṣa Kalpalatā**, stabaka 1 | **wanted** |
| `2015.202757.Jyotihsastra_text.pdf` | **David Pingree, _Jyotiḥśāstra_** | **reference** |
| `ved_vedang_gp_22.pdf` | Hindi essay `वेदोंमें ज्योतिष`, Kalyāṇ Veda-kathāṅka pp.198–199 | no |
| `51-31-Pradip.Mandal.pdf` | Pāṇinian grammar paper on kāraka-vibhakti | no |

### ~~The two witnesses are complementary~~ — WRONG, corrected the same day

**They are not the same work.** Written above, committed, and reported to Rupali before anyone
opened a body page of the printed volume.

- **Jammu MS 882-घ — genuine.** Catalogue label states **Subject: ज्योतिषम्**, author
  `नीलकंठः`, commentary `सुबोधिनी व्याख्या`. ṭīkā only `द्वितीयाध्यायपर्यंत` — to adhyāya 2.
  Image-only; 207 extractable characters across three pages, all of it the CC-0 watermark.
- **Bombay 1947 printed edition — Jaimini's PŪRVA MĪMĀṂSĀ SŪTRA.** Ritual exegesis, not
  astrology. Moved to `_out-of-scope/`, which carries both checks: a body page reading
  `सामिधेनी` / `उपवीत` / `पूर्वपक्षे सिद्धान्तमाह` / `दर्शपूर्णमास याग`, and a vocabulary count
  over 62 OCR pages — Mīmāṃsā **390**, jyotiṣa **110**, with the jyotiṣa figure itself inflated
  by `ज्योतिष` ×38 which is near-certainly **ज्योतिष्टोम**, the archetypal Mīmāṃsā sacrifice.

So the claim "adhyāyas 1–3 between them" is void; **only adhyāyas 1–2 are sourced, from one
manuscript.**

**Three readings of this one title in one day, and the middle one was the confident one.**
First: "the archive.org Subodhinī is Sarveśvarānanda's, not Nīlakaṇṭha's — do not acquire."
Then, from the title page: "wrong — Sarveśvarānanda is the *translator*; this IS the Subodhinī."
Then, from a body page: "wrong again — it is the Subodhinī on the **Mīmāṃsā** Sūtras."

The original instinct was right and the reasoning behind it was wrong, which is the worst
combination, because correcting the reasoning looked like progress. **A title page names the
work; only the body says what the work is about.** Jaimini is famously the author of the Pūrva
Mīmāṃsā Sūtras — a title carrying his name is *more* likely to be that than the jyotiṣa one.

### Two filename traps, and I fell into the second one

**`इति हि ब्राह्मणम्` was not the last of these.** Sanskrit sources collide on titles (G26) and,
it turns out, on **roles**:

1. **`51-31-Pradip.Mandal.pdf`** is a *kāraka* paper — but Pāṇini's kārakas, not Jaimini's. It
   cites `कर्तृकरणयोस्तृतीया` (Aṣṭādhyāyī 2.3.18). The collision is on a technical **term**, one
   level below a title.
2. **`Subodhini of Sarveshvarananda`** — I read "of X" as authorship and recorded in
   `INVENTORY.md` that the archive.org copy is *"Sarveśvarānanda's, not Nīlakaṇṭha's — do not
   acquire it as this row."* The title page says `अनुवादकः` (**translator**) for Sarveśvarānanda
   and `संशोधकः` (**editor**) for Revārāma Śarmā. **The commentary is the Subodhinī, and the
   Subodhinī is Nīlakaṇṭha's** — which the Jammu wrapper independently states
   (`सुबोधिनी व्याख्या · कर्ता नीलकंठः`).

   So a warning meant to prevent acquiring the wrong text was itself telling the reader to skip
   the right one. **A library title names contributors in several roles, and only the script
   says which.** Open the title page.

### Pingree's `Jyotiḥśāstra` — acquired as REFERENCE, not as a corpus text

`archive.org/details/in.ernet.dli.2015.202757`, 154pp, `Author: David Pingree`. This is the
standard bibliographic survey of Sanskrit astral literature, and it is the right instrument for
exactly the questions this corpus keeps asking by web search — which recensions exist, which
commentaries, what survives. Its OCR is unusable (`s'-frrx") ’■■ A`), so it is for a human to
read, not a pipeline to parse. Same posture as `brahmasphuta_siddhanta` §"acquired as REFERENCE,
deliberately not a corpus text".

### Where the files are — staged 2026-09-23

Moved out of `~/Downloads` into the sources tree, renamed so the filename states what the file
IS rather than where it came from (both filename traps above were caused by trusting a name):

```
Hora/Jaimini/JaiminiSubodhini/raw/
    JaiminiSubodhini-JammuMS882gha-RaghunathaTemple-46folios.pdf          96M
    JaiminiSubodhini-adhyaya3-Bombay1947-hindi-tr-Sarveshvarananda.pdf   160M
Hora/Jaimini/JyotishaKalpalata/raw/
    JyotishaKalpalata-stabaka1-Saptarishis.pdf                           2.0M
_reference/
    Pingree-Jyotihsastra-HIL-VI4-DLI2015.202757.pdf                       24M
```

`_reference/` is new: a place for works that inform acquisition decisions without ever becoming
corpus texts. Pingree is the first occupant.

**The sources tree is not a git repo** — it is gitignored by design, so this section is the only
record that the move happened. The two non-sources (the Kalyāṇ essay, the Pāṇini paper) were
left in `~/Downloads`.

**Six more PDFs sat in `~/Downloads`. Checked 2026-09-23: all six are BYTE-IDENTICAL to
sources already staged.** They are re-downloads, not acquisitions. **Deleted from `~/Downloads` the
same day, 156 MB, each one gated on its staged counterpart being present and hash-matching at
the moment of deletion** — the staged copy under `sanskrit-texts-sources/` is now the only one.

```sh
for pair in …; do md5 -q "$dl" ; md5 -q "$staged"; done   # 6 of 6 matched
```

| in Downloads | already staged as |
|---|---|
| `2015.312156.Jataka-Parijata.pdf` | `Hora/Parashari/Jatakaparijatah/raw/JatakaParijata-archiveorg-2015.312156-682pp.pdf` |
| `2015.489052.Deva-Keralam.pdf` | `Hora/Nadi/DevaKeralam/raw/DevaKeralam-archiveorg-2015.489052-268pp-IDENTITY-UNVERIFIED.pdf` |
| `Deva-Keralam-3-Chandrakala-Nadi-compressed.pdf` | `…/DevaKeralam-3-ChandraKalaNadi-compressed-322pp-IDENTITY-UNVERIFIED.pdf` |
| `Garga Hora Shastra Pathak K.K..pdf` | `Hora/Parashari/GargaHora/raw/GargaHora-Pathak-Ranjan.pdf` |
| `Sage_Gargacharya_-_Garga_Hora.pdf` | `…/GargaHora-Santhanam-English-translation-…-TRANSLATION-WITNESS-NOT-SOURCE.pdf` |
| `saravaliofkalyan01kalyuoft.pdf` | `Hora/Parashari/Saravali/Saravali-Kalyanavarma-archiveorg.pdf` |

**This is what the naming convention is for, and it paid out immediately.** I was about to
report `Sage_Gargacharya_-_Garga_Hora.pdf` as a possible second witness that might unblock
`garga_hora`'s missing chapters 2–3 — until the staged copy turned out to be the same file,
already carrying the verdict in its own name: `TRANSLATION-WITNESS-NOT-SOURCE`. Re-run
independently, `scripts/sanskrit-pdf/classify.py` agrees: tier `latin`, **207,524 Roman letters
and zero Devanāgarī**. Somebody had already done this identification and written it where the
next person would trip over it.

**And the real gaps these would have addressed are unchanged, because the sources were never
the blocker:** `garga_hora` holds chapter 1 of 3 because chapters 2–3 carry **no printed verse
numbers at all** in the Pathak edition — confirmed absent in the source across two independent
OCR passes, not lost in processing. A third pass over the same bytes cannot fix that.

`classify.py` on the other five: all `no-text` — image scans, 0 characters after stripping page
separators, `pdfimages` reporting image content. G3's exact signature, and the reason a byte
count of "5 characters for 5 pages" is one form-feed per page rather than a text layer.
