# Drained from `propagation/state/sanskrit-texts/STATE.md` — 2026-09-30

The 2026-09-24 session block, verbatim and complete, moved here to make room for current state
inside the 200-line cap. Precedent: `STATE_2026-09-14-drain.md`.

**Treat every count in it as of its date.** Two were already stale when this was drained:
`98,435 shlokas` is now 98,444 (nine OCR-merged brahmasphuta verses split apart, G71), and the
2026-09-17 translation-backlog figures predate two translation runs. The live residue stays in
`STATE.md` under "2026-09-24 → 09-30 · what is still true".

---

### 2026-09-24 · Sanskrit-side repairs, and `garga_hora` chapters 2-3 rebuilt

**Repairs (narrative compressed 2026-09-30 — full account: `git log -p -- STATE.md`).**
`latin-in-source` 79 → 18 corpus-wide and served `sanskrit-echo` 52 → 0, via four parallel lanes
on the Upaniṣad scraper chrome. `sanskrit_texts/translation_status.py` was written here and is
what surfaced all of it: it derives a verse's real state from what its fields hold rather than
from `status`, across ten defect classes. **G68** (tesseract cannot read a handwritten MS) and
**G69** (a segmentation matching the COUNT can still be cut in the wrong places) recorded.

**`garga_hora` is 3 chapters / 378 verses**, was chapter-1-only at 84. Chapters 2-3 were rebuilt
from our own `-l san` OCR after an Antigravity pass carrying Latin substitutions was reverted.
**The edition prints no verse numbers in chapters 2-3** — confirmed six ways, including by reading
page 40 of the scan — so numbering there is positional and `uncitable`, validated 73/84 against
chapter 1's known verses; chapter 1 keeps its marker-derived 84, because the edition's own numbers
beat inference. Method and rejected alternatives: `docs/SOURCES.md`.

**Left deliberately, and still true:** 18 `latin-in-source` verses documented as not-to-be-fixed
(`LOST PAGE` markers, variant apparatus carrying two readings, OCR with no clean source), and
`garga_hora` v83's reading. *(The third item here — "545 verses holding both a served translation
and a different unconsumed draft" — is CLOSED: re-measured 2026-09-30 it is **0**.)*

>>> **Corpus status, 2026-09-17.** Derive every number here rather than trusting it:
`python3 scripts/check_inventory.py` (texts, shlokas, registry drift),
`python3 scripts/translation_backlog.py` (outstanding work), `python -m sanskrit_texts.checks`
(confidence levels). Previous version of this block: `git log -p -- STATE.md`.

**The texts.** 66 texts in the tree, 66 imported, **98,435 shlokas**, registry matches the corpus.
*(This line read **98,142** until 2026-09-30 while the paragraph above it said 98,435 was correct —
one file asserting two verse counts. Derive it: `python3 scripts/check_inventory.py`.)*
**G62's four exclusions are CLOSED (2026-09-23)** and `EXCLUDED_TEXTS` is empty — an exclusion is a
hazard sitting in the tree, not a resolution, so the right end is that the text leaves.
`deva_keralam` and `dharmasindhu` are quarantined at `.quarantine/` (kept, acquisition rows back to
`REFUSED`); `taittiriya_brahmana` and `taittiriya_aranyaka` went to Youvan at
`Tushar/texts/_incoming/vk-2026-09-23/` as a second witness, on scope. **Every served English and Hindi value that was not a translation has
been moved to a draft field**: 67,820 template/echo values (`9ce801e`), 334 short-verse and echo
residues (`d203008`), 76 more the checker surfaced (`f3f7c6c`: 72 Sūrya Siddhānta Hindi values that
were English, 2 Minarāja `...`). Served failures left: 7 Minarāja gap verses + 1 Bhṛgu that echo
the Sanskrit (a human call), and Sūrya Siddhānta 2.22, a sine table flagged as a false positive.
**Text-level `status` is derived from the verses** and a test enforces it (17 texts were stamped
`translated` falsely). **The corpus is NFC** and a test pins it.

**Citations follow the editions (G64).** Six SARIT texts relabelled or split: Nārada ch.20 flat per
Lariviere, Aṣṭāṅgasaṅgraha Paribhāṣā as `Paribh.N`, Manu `M87`/`M207–209`, and **348 edition verses**
that had been concatenated into neighbours are now their own units. This resolved the "160
mixed-depth verses" without the printed editions. Per-text detail: `docs/CANONICAL_COUNTS.md`
§"The SARIT relabel of 2026-09-17". The converter now refuses a label collision.

**Translation work (derived 2026-09-17).** 2,791 verses empty or one-language, plus **67,228 English
drafts that fail the checker** (template/echo — translate from scratch, do not "verify"), and **1,692
plausible drafts** that are the real verify queue. Split and rules: `docs/TRANSLATION_BACKLOG.md`.

**The store.** Postgres on 5433 — **a Homebrew `postgresql@18` cluster since 2026-09-30, not Docker**
(data dir `/opt/homebrew/var/sanskrit-texts-pg`, LaunchAgent `com.rupali.sanskrit-texts-postgres`).
Migrations `0001`–`0003`; **98,365 verses** (98,435 less the 70 G8 duplicate labels), **210,097
annotations**, **all `draft`, 0 approved** (by design: `approved` needs a named human and a
confidence level). `corpus_api` sees 0 translation values; base tables refuse it (42501).
Fidelity round trip **66/66, order-sensitive** (G66 fixed the exporter). Suite 140 passed with
`CORPUS_REQUIRE_DB=1`; converter suite 386 passed (2 failures predate this work).

**Decided (DECISIONS 2026-09-17):** T5 in full (NFC, DB-resident `structure`, backup = JSON in git +
pg_dump, Rupali owns the review queue — **no date set**), and T6 confidence markers.

**T5.4 DISCHARGED 2026-09-30** (`477c7af`): `make backup` dumps the database **and the globals** —
`corpus_api` lives in the cluster, not the database, so a database-only dump restores a corpus whose
gate has no grantee — then restores into a scratch DB and compares. Run, not merely written: 39 MB
dump, all eight counts matched, gate held in the restored DB. It was still listed as Open when the
store died on 2026-09-29 with no dump; nothing irreplaceable was lost, but only because zero
annotations were approved.

**Open:** confidence phases B (Sanskrit source) and C
(structure/counts) · structure-editing CLI · split-out units whose parent's translation may cover
their text · checker tuning (numeric-only English) ·
the astroacharya cutover (§4). **Discharged 2026-09-23:** the 4 excluded texts and the translation
agent's untracked leftovers — reports deleted (G67), `AGENTS.md` pre-authorisation block reverted,
one-shot extractor handed to Youvan with the texts it produced. **Hazards paid this session:** G65 (a converter test fixture wiped
1,227 translations, twice) and G66 (order-blind round-trip test).

**Audit of the non-corpus files, 2026-09-23** — the 80 tracked files that are not corpus JSON.
Full report with a reproducing command per finding:
[`docs/AUDIT-2026-09-23.md`](../../../sanskrit-texts/docs/AUDIT-2026-09-23.md). 21 findings; 9
fixed in the same pass (two silent-loss paths — the importer swallowing unreadable files, and
`make clean-db` dropping the dev database unguarded — plus four false doc claims and the docs
index). **SC-001 CLOSED 2026-09-23 — converter fixed, both texts repaired.** Root cause: the Kaivalya
source writes verses 21 and 23 as `॥ N` without the closing daṇḍa the other verses carry, so the
converter merged each forward (G23, inconsistent within one file). Nothing was missing; the split
needed no external text and is byte-identical in verse content. Kaivalya is now 2 khaṇḍas of
19 + 5 and moved to `Upanishad/atharvaveda/` — its own colophon reads `इत्यथर्ववेदीया`. Kauṣītaki
is 4 adhyāyas of 6/15/9/20. The structural ratchet is empty. **Still open, not SC-001:** Kauṣītaki
ch2's English translates adhyāya 3; Kaivalya 22 and 24 are untranslated. **(superseded below)** Kauṣītaki now matches canonical 4 adhyāyas chapter for chapter; its
residual is an English/Sanskrit misalignment in ch2, separate from SC-001. Kaivalya holds
canonical 20, 21, 23 **mislabelled** 20, 22, 24 — G12, and my first two reports of it said
"21 and 23 missing", read off the labels and wrong. Absent are 22 and 24. It also sits under
`krishna-yajurveda/` while its 19+5 shape is the **Atharva** recension. Three calls for Rupali:
relabel, source the two absent verses, decide the recension. Old text follows.

**(superseded)** `convert.py` now folds a colophon-only chunk
back into the chapter it closes, with a detector in `structure_checks.py` reported by
`check_inventory.py` and ratcheted by a test. The two live instances are **not mechanically
repairable** — `kaushitaki_upanishad`'s stray record carries a real translation of 2.1 against a
colophon Sanskrit (the English column is offset against the Sanskrit across the boundary), and
`kaivalya_upanishad` ch2 is separately missing verses 21 and 23. A human reading an edition owns
them; everything mechanical is done. **Still open, highest first:** those two repairs · `schema.py` is described by two docstrings and does not
exist · the `EXCLUDED_TEXTS` guard has never been proven to fire · `CORPUS_REQUIRE_DB`'s
fail-vs-skip path is untested · the schema-drift check cannot see a type change.

**Fixing SC-001's kaushitaki instance closes a question `CANONICAL_COUNTS.md` records as open** —
its §"The +3 discrepancies, and a hypothesis that failed" cannot explain Kauśītaki's excess;
merging the stray colophon verse back gives exactly the cited 50 verses in 4 chapters. Muṇḍaka's
+1 is a different cause and must not be folded in.

**One propagation edge stays red, deliberately.** `CLAUDE.md → sanskrit-texts/CLAUDE.md`
(`c0e01c6d`, DIVERGED) is **BLOCKED by 11 upstream edges** in `astroacharya/`, `persona/profile.yaml`,
`docs/constitution/` and `VipinKaushik-mb/` — none of which concerns this project (G20: the ordering
guard is graph-scoped while `reconcile` is workspace-scoped). Clearing it means draining the workspace
fix order root-to-leaf, which is separate work. **It was NOT deferred**, on purpose: deferring moves an
edge off the worklist without the work being done, which is the exact shape G62 cost a week. It stays
in `needs attention`, where it belongs. `propagate graph` prints the order.
