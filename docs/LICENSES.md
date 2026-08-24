# Upstream licences and attribution

Every source this corpus draws from, its terms, and what we owe it. Recorded verbatim
where the wording matters — a paraphrased licence is not a licence.

Verified 2026-08-23.

---

## 1 · Sanskrit Wikisource — `sa.wikisource.org`

**Licence: Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0).**
<https://creativecommons.org/licenses/by-sa/4.0/>

Confirmed from the wiki's own API rather than a page footer:

```
GET https://sa.wikisource.org/w/api.php?action=query&meta=siteinfo&siprop=rightsinfo
→ "Creative Commons Attribution-Share Alike 4.0"
```

**This is a genuinely open licence** and the only open one among our upstreams. Reuse,
redistribution and commercial use are all permitted.

**What we owe it — two obligations, and the second one has teeth:**

1. **Attribution (BY).** Credit Sanskrit Wikisource and link the licence. Per text, record
   the page title, the permanent revision id (`oldid`), and the fetch date, so the exact
   revision used is identifiable. Wikisource pages change.
2. **ShareAlike (SA) — this propagates.** A derivative of BY-SA material must itself be
   released under BY-SA. **Any JSON in this corpus derived from a Wikisource text carries
   that obligation onward.** It does not infect texts sourced elsewhere, but it does mean
   the corpus cannot be relicensed to something more restrictive for those files.

> **DECIDED 2026-08-23: ShareAlike accepted.** Wikisource- and DharmicData-derived texts
> carry BY-SA / ODbL onward. The consequence to remember: those files cannot later be
> relicensed to anything more restrictive, and anyone redistributing them inherits the same
> obligation. Texts sourced elsewhere are unaffected.

---

## 1b · DharmicData (GitHub) — `github.com/bhavykhatri/DharmicData`

**Licence: Open Database License (ODbL).** Verified by fetching the repo's `LICENSE.txt`
(25 KB, full ODbL text). Share, modify and use are permitted.

**Provenance:** the repo's own README cites **vedicheritage.gov.in** (Govt. of India) as the
source for its Rigveda, Yajurveda and Atharvaveda. It is a **third-party republication**,
not a primary edition — which is why the Wikisource copies are kept as independent
witnesses rather than deleted.

**What we owe it — and note the second one, again:**

1. **Attribution.** Repo, and the **pinned commit sha** (the equivalent of a Wikisource
   `oldid` — a branch moves, so a path alone makes a checksum unreproducible). Recorded as
   `bhavykhatri/DharmicData @ <sha>, ODbL — from vedicheritage.gov.in`.
2. **ShareAlike.** ODbL is share-alike, like CC BY-SA. Derived JSON carries the obligation
   onward. **Accepted 2026-08-23.**

**Not everything in it is Sanskrit.** `Samaveda/Samaveda.json` is Ralph T. H. Griffith's
1895 **English translation** (`"language": "English"`, 0 Devanagari characters) — caught by
the acquisition check on first fetch. It is a *translation* source, potentially useful for
the `english` field, and must never be filed as a corpus source.

---

## 2 · Sanskrit Documents — `sanskritdocuments.org`

**Licence: none. Permission-based use, with attribution.** Not Creative Commons, not
public domain.

Verbatim, from the per-file footer (e.g. `doc_upanishhat/atharvashikha.html`):

> "The file is not to be copied or reposted for promotion of any website or individuals or
> for commercial purpose without permission."

Verbatim, from the FAQ at <https://sanskritdocuments.org/faq/>:

> "You cannot use any contents from sanskritdocuments.org if you intend to promote your own
> web-site, commercial or not, to get more traffic for your site and or to attract viewers
> for gains from advertisements…"

> "We rely on the conscience of individuals who are using the contents of the site."

Permitted: **"personal studies, to learn, and to teach"**, with attribution to the site and
to the volunteer encoders and proofreaders, without altering references, claiming ownership,
or breaking the chain back to the source.

**What we owe it:**

- **Per-text attribution is mandatory, naming the individual encoder and proofreader** from
  that file's own footer (e.g. *"Transliterated and proofread by Sunder Hattangadi"*), not
  just the site. Recorded in each text's `README.md` and in `SOURCES.md`.
- The attribution chain must remain traceable back to sanskritdocuments.org.

**The unresolved part, stated plainly.** This repository is public and its data is served
through AstroAcharya's `/texts` API. Redistributing derived texts here is arguably the
"reposting" the footer names, and would be squarely commercial if AstroAcharya is ever
monetised. The underlying Sanskrit is public domain; these terms attach to the
**transcription**, which is the volunteers' work.

Contact for written permission: **`sanskrit@cheerful.com`**. Asking converts "conscience"
into a documented yes and costs one paragraph.

`docs/legal/sanskritdocuments-permission.md` should hold that correspondence when it exists.

---

## 3 · GRETIL — `gretil.sub.uni-goettingen.de`

**Licence: not granted. Reference use only, terms inherited per file.**

> "THIS TEXT FILE IS FOR REFERENCE PURPOSES ONLY! COPYRIGHT AND TERMS OF USAGE AS FOR
> SOURCE FILE."

Each GRETIL file inherits the terms of whatever edition it was keyed from, which are stated
in that file's own header and vary per text. **There is no blanket GRETIL permission**, so
a GRETIL text cannot be treated as reusable without reading its individual header.

Also note GRETIL's Vedic files are frequently **IAST Roman, not Devanagari**.

---

## 4 · Digital Library of India mirror — `dli.sanskritdictionary.com`

Governed by the DLI copyright policy. Holdings are **scanned page images** of printed
editions; the scans' status depends on the edition's age and publisher.

Not used as a text source — see `REFERENCES.md` for why (OCR tier, commentary editions).

---

## Attribution recorded per text

`docs/SOURCES.md` carries an `Attribution` column. For a text to enter the corpus it must
have that column filled with something real:

| Upstream | What goes in the column |
|---|---|
| Wikisource | page title + `oldid` revision id + "CC BY-SA 4.0" |
| Sanskrit Documents | the encoder/proofreader named in the file's own footer |
| DharmicData (GitHub) | repo + pinned commit sha + "ODbL" + the upstream it cites |
| GRETIL | the printed edition named in the file header, plus its stated terms |

`—` is only acceptable for a file we produced ourselves (our own OCR, our own extraction).
An empty attribution on an upstream file is a defect, not a formatting gap.


## Mixed-licence files — added 2026-08-24, needs a call before redistribution

Two corpus files are no longer single-licence. Both are ODbL from DharmicData except for a
small number of verses supplied from Sanskrit Wikisource under **CC BY-SA 4.0**, because
the ODbL source was wrong or empty there:

| File | ODbL | CC BY-SA 4.0 | Wikisource oldid |
|---|---|---|---|
| `Samhita/rigveda/ShakalaSamhita` | 10,449 verses | **21** (8.67) | 299570 |
| `Samhita/atharvaveda/ShaunakaSamhita` | 6,088 verses | **3** (20.3) | 323600 |

The provenance is declared in each file's `structure.secondary_sources`, so it travels with
the data rather than living only here. Rationale for each: `CANONICAL_COUNTS.md`
§"The second witness earns its keep".

**Both licences are share-alike, which is why this was acceptable to do — and it is still
not the same licence.** ODbL and CC BY-SA 4.0 impose their share-alike obligations by
different mechanisms, and combining them in one distributed file is a question this repo has
not answered. Recorded as an open decision, not treated as resolved. Options if it becomes a
problem: keep the Wikisource verses in a sibling file with its own licence header, or
re-source those 24 verses from a public-domain edition (Aufrecht for the Rigveda, Whitney
for the Atharvaveda).
