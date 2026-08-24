# References & Sources

The texts in this repository are sourced, compiled, and verified from digitized resources.
This file names the upstreams, their terms, and which one to prefer for what.

## Upstreams

**Full terms and what each one obliges us to: [`docs/LICENSES.md`](./docs/LICENSES.md).**
Do not restate licence text anywhere else.

| Source | Use for | Format | Licence |
|---|---|---|---|
| [Sanskrit Wikisource](https://sa.wikisource.org/) | **Vedic Saṃhitās.** The only openly-licensed upstream | Devanagari wikitext via API | **CC BY-SA 4.0** ✅ |
| [Sanskrit Documents](https://sanskritdocuments.org/) | **Jyotiṣa; Upaniṣads.** Best proofreading quality | Devanagari `.html`, ITRANS `.itx`, `.pdf` | Permission-based, attribution required |
| [GRETIL](https://gretil.sub.uni-goettingen.de/) | Cross-check only | TEI-XML, HTML; often **IAST Roman, not Devanagari** | None granted — per-file, reference only |
| [Vedic Heritage Portal](https://vedicheritage.gov.in/) | śākhā metadata, recitation audio | audio, metadata | Govt. of India |
| [DLI mirror](https://dli.sanskritdictionary.com/) | **Last resort only** | Scanned page images | DLI copyright policy |

## Saṃhitā sources — resolved 2026-08-23

Four of the five Saṃhitā targets had no acceptable source under a Devanagari-only,
proofread-tier rule. **Sanskrit Wikisource resolves the two hard ones**, and does it under
an open licence:

| Saṃhitā | Source | Script | Accents | Note |
|---|---|---|---|---|
| **Rigveda** Śākala | sanskritdocuments `r01`–`r10` | Devanagari | **accented only** | No unaccented Devanagari Rigveda exists upstream. `RVMDF1-9` / `RVMDF2-10` are also accented and are **UTF-16**, not UTF-8. |
| **Sāmaveda** Kauthuma | sanskritdocuments `sv-kauthuma.html` | Devanagari | **unaccented** ✅ | Complete — 539 KB, 157,404 Devanagari chars, ends in the site footer. An earlier report of upstream truncation was **its own fetch truncating**, not the file. |
| **Kṛṣṇa YV** Taittirīya | sanskritdocuments `taittirIyasamhitA.html` | Devanagari | accented | `taitsamhita1.html` is kāṇḍa 1 only — do not mistake it for the whole. |
| **Śukla YV** Vājasaneyi | **Sanskrit Wikisource** `शुक्लयजुर्वेदः/अध्यायः ०१…४०` | Devanagari | partial | Complete, 40 adhyāyas. Adhyāya 40 is the Īśāvāsya Upaniṣad, as it should be — a free consistency check. **Absent from sanskritdocuments; GRETIL's own index says "Restricted download / proprietary format from TITUS. Converted file(s) not available at present."** |
| **Atharvaveda** Śaunaka | **Sanskrit Wikisource** `अथर्ववेदः/…` | Devanagari | — | GRETIL has it only as **IAST Roman** (`avs___u.htm` unaccented, `avs_acu.htm` accented). MIU's Vedic Reserve PDF has a text layer but in a **legacy 8-bit font encoding** — 0 Devanagari, 380k Latin, `p[qm;idtOcSy i]∑up(` — unusable without the font's mapping table. |

**On the accent decision.** Nissvara was chosen, but no unaccented Rigveda or Taittirīya
Saṃhitā exists upstream. Those are fetched accented and stripped locally. Stripping is
deterministic and **reversible only because the accented source is kept and checksummed**
in `docs/SOURCES.md` — the exact codepoints removed (U+0951, U+0952, U+1CD0–U+1CFF,
U+A8E0–U+A8F1) must be logged per text, or we have silently minted a new recension behind a
`text_id` claiming to be Śākala.

Section index used for Jyotiṣa proofreading:
[sanskritdocuments.org/sanskrit/jyotisha](https://sanskritdocuments.org/sanskrit/jyotisha/).
Vedic material: [`doc_veda/`](https://sanskritdocuments.org/sanskrit/veda/) and
[`doc_upanishhat/`](https://sanskritdocuments.org/doc_upanishhat/).

## ⚠ Sanskrit Documents is not open-licensed

Verified 2026-08-23. Quoted from a per-file footer and the site FAQ:

> "The file is not to be copied or reposted for promotion of any website or individuals or
> for commercial purpose without permission."

> "You cannot use any contents from sanskritdocuments.org if you intend to promote your own
> web-site, commercial or not, to get more traffic for your site and or to attract viewers
> for gains from advertisements…"

> "We rely on the conscience of individuals who are using the contents of the site."

Permitted for "personal studies, to learn, and to teach", **with attribution** to the site
and to the volunteer encoders and proofreaders, and without breaking the chain back to the
source. It is **not** Creative Commons and **not** public domain.

The underlying Sanskrit is public domain; these terms attach to the **transcription**.
Since this repository is public and its data is served through AstroAcharya's `/texts` API,
redistribution here is a live question, not a settled one. Contact for permission:
`sanskrit@cheerful.com`.

**Attribution is therefore not optional.** Each text sourced from Sanskrit Documents records
its encoder/proofreader — taken from that file's own footer — in the text's `README.md` and
in the source manifest.

## Why not DLI, in general

`dli.sanskritdictionary.com` mirrors the Digital Library of India (551,427 books, 31TB) as
**scanned page images**; its search is Tesseract OCR over those scans. Devanagari OCR fails
into well-formed *wrong* characters, so it passes every script-purity check while being
substantively incorrect, and DLI holdings are frequently commentary editions where mūla and
ṭīkā interleave. Measured cost of learning this: see `GOTCHAS.md` G3–G5.

Use DLI only for a text available nowhere else, and only as raw tier — never as corpus JSON
without a proofreading pass.

## Choosing a file at Sanskrit Documents

- **Take the `.html`.** It carries literal Devanagari codepoints. **Do not take `.itx`** as
  the text carrier — ITRANS→Devanagari is a lossy, ambiguous conversion this repo would own
  forever. `.itx` is useful as a *second witness* (it carries an encoder/proofreader header)
  for verse-count cross-checks.
- **Stems are not derivable from titles.** Verified: `doc_upanishhat/isha.html` → 404;
  `iisha.html` → 200. Scrape the index; never construct a URL.
- **Accents.** Filename hints exist (`sasvarA`, `saswara`, `accent` for accented;
  `niHsvaraH` for explicitly unaccented; bare stem *usually* unaccented) but the rule is
  unreliable — the Rigveda files `r01`–`r10` carry no suffix and are fully accented. Decide
  by scanning for accent codepoints (U+0951, U+0952, U+1CD0–U+1CFF, U+A8E0–U+A8F1), not by
  filename.

## Source manifest

Fetched sources live in `../sanskrit-texts-sources/` and are **deliberately not committed**
— too large, and their licence discourages redistribution. What *is* committed is
[`docs/SOURCES.md`](./docs/SOURCES.md): per text, the upstream URL, checksum, fetch date and
attribution, so every source is re-fetchable and verifiable without being stored here.
