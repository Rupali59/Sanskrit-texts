# Dharmashastra re-digitisation — scope and plan

Status: **partly closed 2026-08-24.** `manu_smriti` is done — and not by this plan.
Written 2026-08-22 as Lane D of a 4-lane parallel session; analysis-only, no corpus files
touched by this plan's author.

> ## Read this before executing any of the below
>
> **`manu_smriti` was not repaired. It was replaced.** On 2026-08-24 it was re-acquired
> whole from SARIT's `manusmrti.xml` (CC BY-SA 3.0) — 12 adhyāyas, 2,684 verses, on-schema,
> zero duplicate keys, 11 of 12 chapters matching Bühler's per-chapter counts exactly. The
> 12 off-schema `MS_*.json` files were deleted in the same change. It took one pass.
>
> Everything this document says about *how* Manusmriti's numbering is damaged is accurate
> and is now worthless. Two sessions went into characterising the damage, including a
> careful 2026-08-23 correction about which citation component cycles. None of it was used.
>
> **The lesson, and the first step for the two remaining texts: look for a clean source
> before characterising the damage.** A published critical edition in a machine-readable
> corpus is worth more than any amount of forensic work on a bad digitisation. SARIT was
> already surveyed in [`SOURCES.md`](../SOURCES.md) and already held Manusmriti while this plan was being
> written to repair it by hand.
>
> **What remains in scope — narrowed again 2026-09-02 to `apastamba_dharma_sutra` alone.**
> `apastamba_paribhasha_sutra` **left for Youvan**: it is not dharma. It is praśna 24–25 of
> the Āpastamba *Kalpasūtra* — the paribhāṣā governing the whole Kalpasūtra — its first sūtra
> is `यज्ञं व्याख्यास्यामः` ("we shall explain the sacrifice"), and its commentator
> Kapardisvāmin commented on the Kalpasūtra. Kalpa went to Youvan 2026-08-24. It now lives at
> `Tushar/Youvan/texts/Kalpa/Paribhasasutra/Apastamba/`, off-schema, with its defects
> documented there. **Step 2 below is therefore void** — do not re-parse it here.
>
> Its sibling stays: the Dharmasūtra opens `धर्मज्ञसमयः प्रमाणम्` and is genuine
> Dharmaśāstra. Both are praśnas of the same Kalpasūtra, so the split is **by genre, not by
> containing work** — the rule that keeps the Brāhmaṇa-embedded Upaniṣads with Vipin.
>
> **Source hunt: closed, and it found nothing.** SARIT has no Āpastamba (2026-08-24); GRETIL
> carries only Āpastamba's Śulba-, Gṛhya- and Śrautasūtra (2026-09-02). There is no clean
> machine-readable edition. The OCR is what there is.
>
> **⚠ This plan says "None of the 4,737 existing records carry any English or Hindi today."
> That is false.** Measured 2026-09-02: `ADS_001.json` is 1,437/1,437 and `APS_001.json` was
> 358/358 for both languages — unverified machine output in `english_translation` /
> `hindi_translation`. Those are not the served field names, so nothing publishes them; **a
> migration that renames them to `english`/`hindi` would publish 1,795 unverified machine
> translations.** Sample: `धर्मज्ञसमयः प्रमाणम्` → *"The knowledge of dharma is the proof of
> time"*, misreading *samaya* (agreed practice) as "time". Step 6 must be rewritten: the job
> is not "translation begins", it is "these drafts are quarantined or discarded".

> ## Feasibility of re-parsing the Dharmasūtra from OCR — measured 2026-09-02, VERDICT: tractable
>
> Against `4617.txt` (9,642 lines; **use it, not `4605.txt`**, which is the same edition as a
> single-line 1.2 MB dump — the shape that made Manusmṛti unrecoverable).
>
> **The mūla/ṭīkā split is mechanical.** Sūtra lines end in a Devanāgarī numeral in daṇḍas
> (`॥५॥`); Haradatta's commentary lines end in a plain `॥`. They alternate, one per line,
> blank-separated. 1,313 lines match the sūtra pattern; 3,507 do not.
>
> **The structural spine is in the body, not just the table of contents** — explicit
> colophons: `इति प्रथमः खण्डः`, `व्याख्यायामुज्ज्वलायां प्रथमः पटलः`.
>
> | Level | Found in OCR | Canonical | Shortfall |
> |---|---:|---:|---:|
> | sūtras | 1,313 | ~1,364 | ~4% |
> | khaṇḍas | 59 | ~61 | 2 |
> | paṭalas | 20 | 22 | 2 |
>
> **The shortfall is uniform (~3–4%) across all three levels, which is OCR dropout, not
> missing structure — and it is self-detecting.** The 1,313 numerals form 63 runs that align
> with the khaṇḍa colophons; 29 of 63 are already exactly `1..N`, and the other 34 fail by
> *individually missing* numbers in otherwise contiguous runs (the run at line 1748 skips 18,
> 20 and 23; at 1879 skips 10; at 2336 skips 2). A gap in a contiguous run is repairable and
> its candidate line is adjacent. `4605.txt` is a second OCR pass of the same edition and is
> the cross-check for the gaps.
>
> So the contiguity guard step 5 demands is not just possible, it is the natural output shape.
> **What is NOT yet established:** which khaṇḍa belongs to which paṭala/praśna (the colophons
> give ordinals, and only one praśna marker was found in the body), and whether the 2 missing
> khaṇḍa colophons hide a run-merge. Both need checking before a parser is trusted.

## Diagnosis

Three texts remain off-schema — `sutras[]`/`shlokas[]` at the top level, no
`chapters[]` wrapper — and were deliberately **not** migrated onto the uniform
schema during the 2026-08-17/18 normalization waves:

| text_id | Files | Records | Location |
|---|---:|---:|---|
| `manu_smriti` | 12 | 2,942 | `Dharmashastra/ManuSmriti/chapters/MS_001.json` … `MS_012.json` |
| `apastamba_dharma_sutra` | 1 | 1,437 | `Dharmashastra/ApastambaDharmaSutra/chapters/ADS_001.json` |
| `apastamba_paribhasha_sutra` | 1 | 358 | `Dharmashastra/ApastambaParibhashaSutra/chapters/APS_001.json` |

Total: 14 files, 4,737 records. This confirms `CLAUDE.md` and
`propagation/state/sanskrit-texts/DECISIONS.md` (2026-08-18 entry
"ManuSmriti and Apastamba need re-digitisation, not renumbering").

**The version of the diagnosis this session initially held, and discarded:**
the task brief (derived from `CLAUDE.md`) states "Manusmriti's leading number
component runs 1–33." Measuring `MS_001.json` directly shows this is not what
the data does — the leading (first) integer of every dotted `number` field in
`MS_001` is **`1`** in 1,514 of 1,518 records (the other 4 are bare integers
or a stray `1.9.9`). What actually ranges up to ~33–34 and restarts
repeatedly is the *second* component — the traditional verse number within
whatever the digitiser considered "chapter 1" — and it restarts **87 times**
by a simple decrease-detection (close to, not exactly, the "89 fragmentary
cycles" already on record; the difference is definitional — how a restart is
counted at the bare-integer/dotted boundary, not a disagreement about the
data being fragmented). **The conclusion is unchanged — this file is still an
unrecoverable jumble of restart cycles — but "leading component runs 1–33" is
imprecise and should not be repeated verbatim.** It described the *verse*
component's range, not the *chapter* component, and a future re-reading of
`CLAUDE.md` should not build on the literal claim.

Everything else in the existing diagnosis was re-measured and **confirmed**:

- Apastamba Dharma Sutra: 219 records with zero dots in `number` (of which
  171 are plain integers and 48 use hyphens like `"1-1-1"` — still not a
  Praśna.Paṭala.Khaṇḍa.Sūtra citation, so "bare/malformed" as a category is
  accurate even though "integer" undercounts the true 219). Exactly **15**
  records literally contain the placeholder text `X.X.21` / `X.X.22`
  (`X.X.21.18`, `X.X.21.21`, `X.X.22.1`…`X.X.22.13`) — the digitiser's own
  "prefix unknown" marker, confirmed byte-for-byte. 16 records (not the
  recorded 13) start with a bare `..` — `..10.4` through `..10.16` (13
  records) plus `..11.1` through `..11.3` (3 more) — so the prior count of 13
  looks like it captured only the first malformed run and missed the second.
  Minor, does not change the verdict.
- Apastamba Paribhasha Sutra was **not previously measured in detail** and
  turns out to have the *same* pathology as the Dharma Sutra, not a milder
  one: of 358 records, the integer `1` is used as the `number` **15 times**,
  `2` **12 times**, and so on — every value 1–53 repeats between 2 and 15
  times, with **7 records carrying an empty string** as `number`. This is a
  khaṇḍa-relative numbering that lost its parent citation, structurally the
  same defect as the Dharma Sutra's bare integers. **New finding: all three
  texts, not two, need full re-digitisation** — Paribhasha Sutra was
  previously an afterthought in the write-up and should be treated as equally
  broken.
- Canonical structures, checked against `propagation/state/sanskrit-texts/DECISIONS.md`
  (2026-08-18 entry) rather than from memory: Manusmriti is 12 adhyāyas,
  ~2,684 verses; Apastamba Dharmasūtra is Praśna → Paṭala → Khaṇḍa → sūtra, so
  a citation like `1.1.1` (three components) is *correct form*, and this
  repo's records mixing 1, 2, 3 and 4-dot depths in the same file
  (`{0: 219, 1: 238, 2: 578, 3: 402}` dot-count histogram measured directly)
  confirm the citation depth was applied inconsistently during OCR/parsing,
  not that the source itself is inconsistent.

## Task 1 — the four unfiled source files

`../sanskrit-texts-sources/Dharmashastra/{4605,4607,4609,4617}.txt`, read in full
(head/tail/preface text), with confidence:

| File | Size | Identification | Confidence |
|---|---|---|---|
| `4605.txt` | 1.19MB, 0 newlines (single line) | **Āpastamba-Dharmasūtra with Haradatta's Ujjvalā commentary**, ed. A. Mahādeva Śāstri, Government Oriental Library Series, Mysore 1898. Title page, preface, and manuscript list (telugu/grantha/nāgarī sources) are word-for-word identical to `4617.txt`. Ends in a पदानुक्रमणी (word index). | **High.** Title block and preface text match verbatim. |
| `4617.txt` | 1.02MB, 9,642 lines (formatted) | The **same edition** as `4605.txt` — same title, same "Bibliotheca Sanskrita" series line, same nine-manuscript list (Telugu/Grantha/Nāgarī), same editor. Appears to be a cleaner/differently-formatted OCR pass of the same physical scan, not a different volume. | **High** that it is the same work as 4605; **medium** on "same OCR pass vs. a second independent scan" — not disambiguated further (see Open Questions). |
| `4607.txt` | 353KB, 1,503 lines | **Āpastamba-Paribhāṣā-Sūtra**, with the commentaries of Kapardisvāmin and Haradattāchārya. Title page reads literally "आपस्तम्बपरिभाषासूत्रम् … THE APASTAMBA–PARIBHÁSHÁ–SUTRA WITH THE COMMENTARIES OF KAPARDISVA'MIN AND HARADATTA'CHA'RYA." | **High.** Exact title-string match to the existing `ApastambaParibhashaSutra` text_id. |
| `4609.txt` | 92KB, 0 newlines (single line, heavily garbled OCR — no spaces between words) | Opens `अथापस्तंबोक्तश्रावणीप्रारंभः` — "here begins the Śrāvaṇī [rite] as taught according to Āpastamba." This is a **ritual prayoga manual** (upākarma/śrāvaṇī ceremony instructions — gaṇapati-pūjā, saṃkalpa, mṛttikā-snāna, etc.), not a dharmaśāstra treatise. It does not read as part of the Dharmasūtra, the Paribhāṣā-Sūtra, or either undigitised stub (`Dharmasindhu`, `NirnayaSindhu` — those are general digest/customs compendia, not single-rite prayoga texts). | **Unidentified as to a target text directory.** What it *is* (a Śrāvaṇī prayoga in the Āpastamba tradition) is reasonably clear from the opening line; where in this corpus's layout it belongs is not — it does not fit any of the three known Dharmashastra texts and I found no textual link (title, colophon) to `Dharmasindhu` or `NirnayaSindhu` specifically. Flagging as its own open question rather than forcing a placement. |

**Practical read:** `4605.txt` and `4617.txt` are two representations of the
Apastamba Dharma Sutra source (same edition the corpus's own
`ApastambaDharmaSutra` text_id is presumably meant to be), and are candidate
re-digitisation source material alongside whatever the `ApastambaDharmaSutra`
README currently cites. `4607.txt` is very likely the actual clean source for
`apastamba_paribhasha_sutra`. `4609.txt` needs a human call before it is
placed anywhere — see Open Questions.

## Task 2 — per-text scope, canonical target, and recoverability verdict

### `manu_smriti`

- **Current shape:** 12 files (`MS_001.json`…`MS_012.json`), 2,942 records
  total (confirmed). Field names: `text_id`, `title_sa`, `title_en`,
  `category`, `chapter_number`, `shlokas[]` where each record is
  `{number, sanskrit, english_translation, hindi_translation}` (no `status`
  field at all — a further schema gap beyond the missing `chapters[]`
  wrapper).
- **Numbering, measured directly:** `MS_001.json` (labelled `chapter_number: 1`)
  holds 1,518 records. Of these, 1,514 use a two-part `number` like `"1.34"`
  where the leading component is always `1` (i.e. the file *is* internally
  consistent about being "chapter/adhyāya 1" — the earlier "leading component
  runs 1–33" phrasing was wrong, see Diagnosis above); the second component
  is the traditional verse number and it restarts from 1 roughly 87 times
  across the file, meaning `MS_001` alone contains at minimum ~87 fragments
  each independently numbered `1.1, 1.2, 1.3…` before jumping back down.
  `MS_002`…`MS_011` are internally consistent the same way (each file's
  leading component matches its own filename number). `MS_012` is the one
  exception on record — it contains both leading component `12` and `13`
  (i.e. it holds a stray "chapter 13" inside a nominally 12-chapter file),
  which is consistent with the standing note that Manusmriti canonically has
  12 adhyāyas.
- **Canonical target:** 12 adhyāyas, ~2,684 verses total (ch 1 ≈ 119, ch 2 ≈
  249, per the 2026-08-18 decision entry, itself sourced from Wikipedia /
  Wisdomlib — not independently re-verified by this session, flagged as an
  open question below).
- **Sources on disk:** `../sanskrit-texts-sources/Dharmashastra/ManuSmriti/9048.txt`
  and `manu_clean.txt`, both confirmed **byte-similar duplicates of the same
  1909 Nirnaya Sagar edition** (identical opening title block: `मनुस्मृतिः
  श्रीमत्कुल्लूकभट्टविरचितया श्लोकानामकारादिकोशेन च समेता`), both a single
  line (0 newlines), 2.8–2.86MB. Front matter and Kullūka's commentary
  included, unseparated from the root verses.
- **Verdict: needs re-parsing from source, not transformation of the existing
  JSON.** The existing 2,942 records cannot be reordered into 2,684 correctly
  numbered verses — the digitiser's `chapter_number`-per-file grouping is
  usable as a rough chapter boundary (11 of 12 files are internally
  consistent about which adhyāya they claim to be), but the verse-level
  numbering inside each file is not a permutation of 1..N, it is dozens of
  short repeating fragments. Recovering it means walking the 1909 edition's
  actual verse boundaries (likely via its own printed numbering, which the
  single-line OCR dump does not preserve as structure) and re-associating
  each fragment's Sanskrit/English/Hindi with a real verse number. This is
  the same "digitisation project, not a patch" call the 2026-08-18 decision
  already made; nothing found here weakens it.

### `apastamba_dharma_sutra`

- **Current shape:** 1 file (`ADS_001.json`), 1,437 records, fields
  `text_id`, `title_sa`, `title_en`, `category`, `chapter_number`,
  `chapter_title_sa`, `chapter_title_en`, `sutras[]` (`number`, `sanskrit`,
  `english_translation`, `hindi_translation`).
- **Numbering, measured directly:** dot-count histogram over `number`:
  0 dots → 219, 1 dot → 238, 2 dots → 578, 3 dots → 402. Canonical form is
  4 components (Praśna.Paṭala.Khaṇḍa.Sūtra, i.e. 3 dots) — only 402 of 1,437
  records (28%) are even shaped correctly, independent of whether their
  *values* are right. Confirmed the two named pathologies exactly as
  recorded: **15** records literally read `X.X.21.*` / `X.X.22.*` (the
  digitiser's explicit "unknown prefix" marker) and a run of **16** records
  (not 13) start with a bare `..` (`..10.4`…`..10.16`, then `..11.1`…`..11.3`
  — likely two malformed runs where the prior count only caught one).
- **Canonical target:** Praśna → Paṭala → Khaṇḍa → sūtra hierarchy — a
  4-component citation like `1.1.1.14` is the *correct* form, not an error,
  which the 578 3-dot and 402 (mislabelled 2-dot, i.e. missing one level)
  records partially already reflect.
- **Sources:** `../sanskrit-texts-sources/Dharmashastra/4605.txt` and
  `4617.txt` — both now identified (Task 1) as the same 1898 Mysore
  Government Oriental Library edition with Haradatta's Ujjvalā commentary,
  the presumable intended source for this exact text.
- **Verdict: needs re-parsing from source.** The existing JSON mixes citation
  depths inconsistently (0 through 3 dots for what should uniformly be a
  4-component citation) and carries explicit "unknown" placeholders from a
  prior digitisation attempt — there is no purely mechanical way to recover
  the missing Paṭala/Khaṇḍa levels for the 219+238+578 under-specified
  records from the numbers alone; it requires re-reading the source edition's
  own citation markers.

### `apastamba_paribhasha_sutra`

- **Current shape:** 1 file (`APS_001.json`), 358 records, same field shape
  as the Dharma Sutra.
- **Numbering, measured directly — NOT previously characterised in this
  detail.** All values are bare integers or empty strings (no dotted
  citations at all): the integer `1` is reused as `number` **15 times**, `2`
  **12 times**, `3` **12 times**, decreasing roughly monotonically down to
  single digits by the 40s, and **7 records have `number == ""`**. Range
  covers 1–53 with no gap, but every value in that range repeats.
- **Canonical target:** not independently re-derived by this session (no
  citation-structure reference was checked the way Manusmriti/Dharma Sutra
  were) — flagged as an open question. Given the shared authorship and genre
  with the Dharma Sutra, a Paṭala/Khaṇḍa-style hierarchy is plausible but
  unconfirmed.
- **Sources:** `../sanskrit-texts-sources/Dharmashastra/4607.txt` — identified
  in Task 1 with high confidence as the clean source (title page reads
  "आपस्तम्बपरिभाषासूत्रम्" / "THE APASTAMBA–PARIBHÁSHÁ–SUTRA").
- **Verdict: needs re-parsing from source.** The repeated bare integers mean
  the current `number` field has lost whatever grouping (likely khaṇḍa)
  distinguished the 15 different sūtras all currently labelled `"1"`. This
  text was treated as a smaller, lower-priority sibling of the Dharma Sutra
  in the existing write-ups; the numbers say it needs the same treatment,
  not a lighter one.

## Ordered steps

1. **Human decision on `4609.txt`** (Task 1) before any Dharmashastra source
   work proceeds on it — it may be out of scope for this corpus entirely (a
   liturgical prayoga rather than a jyotiṣa-adjacent dharmaśāstra text); see
   Open Questions.
2. **Re-parse `apastamba_paribhasha_sutra` first.** Smallest text (358
   records, 1 source file, `4607.txt` already confidently identified), and
   it is the one whose canonical structure is least understood — doing it
   first surfaces that unknown early, before committing to a shared
   Praśna/Paṭala/Khaṇḍa parser design across all three texts.
3. **Re-parse `apastamba_dharma_sutra`** using the citation depth already
   half-present in the data (402 records already carry 3-dot citations) as a
   partial check against the freshly-parsed source, then `4605.txt`/`4617.txt`
   as primary source, cross-checking the two OCR passes against each other
   where they diverge.
4. **Re-parse `manu_smriti` last** — largest (2,942 records across 12 files,
   87+ internal restart cycles in `MS_001` alone) and its source
   (`manu_clean.txt`/`9048.txt`) is a single-line 2.8MB dump with
   unseparated front matter and Kullūka's commentary, the most source-side
   cleanup of the three.
5. **After each text is re-parsed:** validate with the same kind of
   contiguity guard already used for the BPHS consolidation (2026-08-17
   decision) — refuse to write unless the resulting verse sequence per
   chapter is contiguous 1..N (or a documented, cited exception, the same way
   BPHS's `12अ` variant reading was handled) — before migrating onto the
   uniform `chapters[]` schema.
6. **Only then** does translation begin — it is a separate, downstream job,
   explicitly blocked on re-digitisation landing. None of the 4,737 existing
   records carry any English or Hindi today, so there is no existing
   translation work to preserve or migrate; a fresh translation pass follows
   the corpus's normal workflow (`CLAUDE.md` → Translation workflow) once
   each text has real verse numbers.

## Hazards, in the order to address them

1. **Duplicate/near-duplicate sources look independent and aren't.**
   `4605.txt` and `4617.txt` are the same edition; treating them as two
   independent witnesses to cross-check against each other is only valid to
   the extent their OCR errors are uncorrelated, which has not been verified.
   Check before relying on "two sources agree" as a correctness signal.
2. **Single-line OCR dumps hide structure that the original page layout had.**
   Both Manusmriti sources and 4605.txt have zero newlines; whatever chapter/
   verse boundary markers existed on the printed page did not survive OCR as
   line breaks. Re-parsing needs to key on in-text Devanagari numeral markers
   (`॥ १२॥`-style, per this repo's own convention for `.md` sources) or
   equivalent, not on line structure.
3. **A small clean sample is not evidence the whole file is clean** — this is
   the exact failure already recorded for Apastamba's first 30 records
   (2026-08-18 decision, and `rule:discernment-checks` §4 more generally).
   Any acceptance check for the re-digitised output must run over the full
   record set, not a prefix.
4. **The macOS case-insensitivity near-miss from the 2026-08-18 consolidation**
   (`Phaladeepika.json` / `phaladeepika.json` landing on one inode) applies
   here too if any intermediate filenames differ only by case. Capture a
   baseline (record counts, a content hash) before any bulk write, the same
   discipline that caught it last time.
5. **`docs/INVENTORY.md` and the `CLAUDE.md` registry currently show these
   three texts as un-ingestible / off-schema.** Once re-digitised, both need
   updating in the same commit as the corpus change (per the hand-maintained
   convention adopted 2026-08-17), not as a follow-up.
6. **This plan's own "leading component runs 1–33" correction** (see
   Diagnosis) should be carried into [`CLAUDE.md`](../../CLAUDE.md) / [`DECISIONS.md`](../DECISIONS.md) the next time
   either is touched for this text, so the imprecise phrasing does not get
   copied forward into a future session's starting assumptions.

## What is already known / done

- The off-schema/needs-re-digitisation conclusion for `manu_smriti` and both
  Apastamba texts was reached 2026-08-18 and is **confirmed**, not
  overturned, by this session's direct measurement — with the corrections
  above (the "1–33" phrasing, the 13-vs-16 malformed-run count, and
  `apastamba_paribhasha_sutra` turning out equally broken rather than a minor
  sibling issue).
- Two of the four raw `Dharmashastra/{4605,4607,4609,4617}.txt` files are now
  identified with high confidence (`4605`/`4617` → Apastamba Dharma Sutra
  source, `4607` → Apastamba Paribhasha Sutra source) — this closes part of
  the "await chunking" item open since `7fbfae1` (2026-08-10).
- No corpus JSON, README, `STATE.md`, `DECISIONS.md`, or `CLAUDE.md` was
  modified by this plan. This file is the only new artifact.

## Open questions needing a human decision

1. **What is `4609.txt`, and does it belong in this corpus at all?** It reads
   as an Āpastamba-tradition Śrāvaṇī/Upākarma prayoga (a ritual how-to, not a
   dharmaśāstra treatise or a jyotiṣa text). Candidates: (a) out of scope,
   archive or move elsewhere; (b) a genuinely relevant ancillary text that
   needs its own new text directory rather than folding into any existing
   one; (c) supporting material for one of the two undigitised stubs
   (`Dharmasindhu`, `NirnayaSindhu`) — no textual evidence found linking it to
   either, so this would be a placement guess, not a finding.
2. **Are `4605.txt` and `4617.txt` two OCR passes of one physical scan, or
   scans of two distinct exemplars of the same 1898 print run?** Not
   disambiguated — matters for whether cross-checking them against each
   other during re-parsing is a meaningful error-catch or circular.
3. **Manusmriti's canonical per-chapter verse counts** (ch 1 ≈ 119, ch 2 ≈
   249, ~2,684 total) were carried forward from the 2026-08-18 decision entry,
   which cites Wikipedia and Wisdomlib. Worth a second, corpus-quality source
   check (e.g. a critical edition's stated verse count) before those numbers
   become the acceptance target for the re-parse.
4. **Apastamba Paribhasha Sutra's canonical citation structure** was never
   established (unlike Manusmriti and the Dharma Sutra) — needs a scholarly
   reference before step 2 of the ordered steps can define what a "correct"
   re-parsed record looks like.
5. **Priority relative to the rest of the corpus's open work** — this is a
   from-scratch digitisation project for three texts (4,737 records' worth of
   re-parsing plus translation afterward), not a bounded bugfix. Worth an
   explicit call on whether it is worth doing now versus the other pending
   items in `STATE.md` (the ~506 disordered BPHS-adjacent shloka numbers, the
   13 undigitised stub texts, etc).

## Translation is downstream and blocked

None of the 4,737 existing records in any of the three texts carry English or
Hindi translation content (0 of 2,942 Manusmriti records, 0 of 1,437 Dharma
Sutra records, 0 of 358 Paribhasha Sutra records — this session did not
re-verify the "0 EN, 0 HI" figure record-by-record but it is consistent with
every sample read during this analysis). Translation cannot meaningfully
start until each text has real, source-verified verse numbers — translating
against the current fragmented numbering would produce translations keyed to
citations that will not survive re-digitisation.
