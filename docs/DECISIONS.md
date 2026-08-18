# sanskrit-texts — Decisions (append-only)

Project-scoped decisions. Workspace-wide decisions live in `../../docs/DECISIONS.md`.
Convention: `../../docs/STATE_MANAGEMENT.md`. Never edit past entries; supersede by appending.

## 2026-06-09: Adopt STATE.md / DECISIONS.md convention; subsume TODO.md
**What:** sanskrit-texts adopts the workspace state-management convention. STATE.md at repo root, DECISIONS.md under tracked `docs/`. The existing `TODO.md` digitization checklist (8 items, 5 completed + 3 pending) is copied into STATE.md Pending/Completed; `TODO.md` retained as historical with a frozen banner. Sixth and final sibling onboarded.
**Why:** This repo is a data corpus, not a code project — its "state" is the digitization + translation progress matrix. STATE.md gives that progress a uniform shape matching the four code-project siblings, so a workspace sweep over `*/STATE.md` returns coherent answers for both code and data repos.
**Refs:** workspace `docs/STATE_MANAGEMENT.md`; astroacharya commit `98f7bb3`; Astroclarity `60008c3`; Campaigner `f880cff`; VipinKaushik-mb `d652cec`.

## 2026-06-20: Uniform-schema normalization sweep across the corpus
**What:** Migrated every `.json` text file off the pre-normalization shape (`source`, `header`, `book`, `english_meaning`, `hindi_meaning`, `source_file`, `source_chunk`, `is_duplicate`) onto the uniform schema documented in `CLAUDE.md` (`text_id`, `title_sa`, `title_en`, `category`, `chapters[].shlokas[]` with `text` / `english` / `hindi` / `status`). Shloka `number` coerced from Devanagari strings (`"१"`) to integers, half-shlokas retained as strings (`"1/2"`). Sweep touched 331 Hora + 28 Samhita files.
**Why:** astroacharya's seed script iterates the uniform schema; the legacy fields broke `/texts` ingestion and inflated counts via duplicate (`is_duplicate`) entries. Single shape → uniform iteration, dedup by `(chapter, shloka)` key.
**Status:** Applied in the working tree; **not yet committed** as of this entry. The legacy fields must not be reintroduced (see `CLAUDE.md` → "Do not add back").
**Affects:** sanskrit-texts (consumed by astroacharya `/texts` seed)

## 2026-06-20: Corpus reaches 100% translation; new digitizations land
**What:** All 14 registered `text_id`s now report 100% English + Hindi translation. New since the last registry snapshot: `uttara_kalamrita` (324 shlokas, 9 chapters) graduated from README-stub to digitized text; `minaraja_yavana_jataka` extended with the Uttarakhanda (MS_040–071, ~1,887 shlokas) for 4027 total; `jataka_parijata` 1772→1947, `phaladeepika` →100%, `brihat_samhita` →5500, plus `bphs` 3867→3932. Counts are deduplicated-unique and authoritative; `CLAUDE.md` registry updated to match.
**Why:** Completes the translation-injection backlog tracked in the frozen `TODO.md` and `STATE.md` Pending.
**Status:** Reflected in `CLAUDE.md` and `STATE.md` (working tree); underlying JSON + new files **not yet committed**.
**Affects:** sanskrit-texts

## 2026-06-20: Catch up to workspace state + plans convention (6th sibling); un-ignore `docs/`
**What:** Adopted the missing pieces of the 2026-06-19 workspace sweep that bypassed this repo: added `docs/plans/README.md` (project-plan convention), and corrected `.gitignore` — the prior content was a malformed `docs/` ignore line that hid the tracked `docs/` tree (same defect Astroclarity fixed in its T13 follow-up). New `.gitignore` ignores `.DS_Store`, `__pycache__/`, `*.py[cod]`, and `.code-review-graph/`. Per-project hygiene hooks (T33) remain **not installed** here — deferred, infra-only.
**Why:** Keep all six siblings on one shape so a workspace sweep over `*/STATE.md` and `*/docs/plans/` returns coherent results. The malformed `.gitignore` contradicted `CLAUDE.md`'s claim that "`docs/` is tracked here."
**Affects:** sanskrit-texts

## 2026-06-20: T33 per-project hygiene hooks installed (supersedes prior "deferred")
**What:** Wired the T33 hooks — `.githooks/{pre-commit,post-commit}` (5-line dispatchers resolving the workspace via `~/.gstack/workspace-root`) + `scripts/install-hooks.sh` (sets `core.hooksPath=.githooks` per-clone). Registered `"sanskrit-texts" = "main"` in workspace `docs/CONTEXT-BUDGET.md [active_lines]`. Supersedes the "remain not installed — deferred, infra-only" note in the entry above.
**Why:** 6th-sibling parity. The hooks are type-agnostic (size-caps + state-shape check line counts / file presence, not build structure), so the no-build data corpus runs them identically to the Node/Python siblings. dep-audit skips this repo (no `package.json`).
**Affects:** sanskrit-texts, workspace

## 2026-06-20: Data-correctness audit — normalize stray status; drop dead `TRANSLATION_FLAGS.json` refs
**What:** Audit verified all 14 texts genuinely 100% translated (0 untranslated/partial, 0 empty `english`/`hindi`). Two fixes: (1) 350 shlokas in Jataka Parijata (JP_014/017/018) carried the non-canonical `"status": "completed"` → normalized to `"translated"` (schema allows only `translated`/`partial`/`untranslated`; content was already complete). (2) Removed the two `docs/TRANSLATION_FLAGS.json` references in `CLAUDE.md` (layout block + ⚑ footer) — the file was never tracked, has no consumer (astroacharya doesn't read it), and at 100% there is nothing to flag.
**Why:** Keep the `status` field machine-trustworthy for AstroAcharya's `/texts` ingestion, and stop docs pointing at a file that never existed.
**Affects:** sanskrit-texts

## 2026-06-20: Digitization-backlog scope call — Siddhanta in, SamudrikShastra out
**What:** Resolved the scope of the README-only stub texts. **In-scope (stay here, digitize when prioritized):** the 4 Hora stubs (Saravali, Sarvartha Chintamani, Prashna Marga, Jataka Tattvam) and the 5 **Siddhanta** texts (Surya Siddhanta, Aryabhatiya, Brahmasphuta Siddhanta, Siddhanta Shiromani, Panchasiddhantika) — Siddhanta (mathematical astronomy) is a Jyotish skandha and belongs in this corpus. **Out of scope:** `SamudrikShastra/` (Hastamuktavali, SamudrikaTilaka) → **Youvan Prakashan** under the Tantra/Mantra/Philosophy ownership split (2026-05-04); to be removed here and recreated under Youvan. **Flagged separately:** `ThreeHundredImportantCombinationsRaman` is a 20th-c. English work (raw OCR only, no Devanagari shlokas) — does not fit the uniform schema; pending an exclude-vs-keep-as-reference call.
**Why:** Make "what's next" explicit and prevent out-of-scope digitization. Siddhanta confirmed canonical to Jyotish; Samudrik (physiognomy/palmistry) sits with Youvan's tradition scope.
**Affects:** sanskrit-texts, Youvan

## 2026-06-20: Execute removals — SamudrikShastra + ThreeHundred out; `samudrika` category retired
**What:** `git rm`'d `SamudrikShastra/` (→ Youvan) and `Hora/ThreeHundredImportantCombinationsRaman/` (excluded — English OCR, non-schema). Dropped `SamudrikShastra/` from the `CLAUDE.md` layout and removed `"samudrika"` from the `category` enum (no file ever used it). README metadata for both is preserved in git history. **Youvan scaffold deferred:** `Tushar/Youvan` is a Next.js website with no text-corpus structure (nearest is `app/concepts/palmistry/`) and currently has uncommitted work — form + timing is a Youvan-side decision, not blocking this repo.
**Why:** Complete the scope call physically so the corpus contains only in-scope Jyotish texts. Avoided forcing a malformed scaffold into a dirty website repo.
**Affects:** sanskrit-texts, Youvan

## 2026-07-17: Corpus wiki + source-out-of-git policy + propagation flow
**What:** (1) Added a generated corpus **wiki** — `scripts/gen_inventory.py` walks the tree and
emits `docs/INVENTORY.md` (23 texts / 240 chapters, by category with links); `docs/README.md` is the
wiki front page. Generated, never hand-edited — rerun the script after adding a text. (2) **Source-out-of-git
policy:** canonical data is the per-chapter JSON; source scans (PDF, raw OCR `.txt`) are kept **local, not
committed** — they bloat git and aren't the canonical form (the 4 already-tracked PDFs are stripped in the
history-rewrite step; new ones gitignored). (3) **State-based propagation:** new root `.propagates.yml`
declares `docs/INVENTORY.md` → astroacharya `reference.md` + `DATA_GAPS.md` — a text-level change fires a
drift row so astroacharya's from-canon `@source` tracking never silently diverges from the corpus.
**Why:** The corpus grows continuously; a hand-maintained inventory would rot, and downstream astroacharya
canon had no automated signal when the corpus changed. Generate the catalog + declare one coarse
producer→consumer edge (INVENTORY, not per-chapter — that would flood the ledger).
**Affects:** sanskrit-texts, astroacharya

## 2026-07-17: Recategorize Hora into schools (backfilled 2026-08-12)
**What:** Restructured the flat `Hora/<Text>/` layout into school-level subdirectories: `Hora/Parashari/` (BrihatJataka, BrihatParasharaHoraShastra, Chamatkarchintamani, Jatakaparijatah, JatakaTattvam, Laghujatakam, MinarajaYavanajataka, Phaladeepika, Saravali, SarvarthaChintamani, Shatpanchashika, UttaraKalamrita, VarahamihirDaivagnavallabh), `Hora/Nadi/` (Bhrigusootram), `Hora/Prashna/` (PrashnaMarga), `Hora/Jaimini/` (JaiminiSutras). ~194 file renames in commit `1cccca6`. Empty school branches not yet holding a digitized text (`Hora/Nadi/ChandraKalaNadi/`, `Hora/Jaimini/JaiminiSutras/`) were seeded with a `.placeholder` file so the school directory exists in git ahead of content. The same commit also ingested new digitized chapter stores and added the `Dharmashastra/` and `Muhurta/` category trees, and committed `scripts/digitize.py` + `scripts/translate.py`.
**Why:** The flat `Hora/<Text>/` list conflated distinct predictive traditions (Parashari natal astrology, Nadi, Prashna/horary, Jaimini) that classical Jyotish treats as separate schools with different methodological assumptions. Grouping by school makes the corpus tree reflect the actual textual tradition and gives new Nadi/Jaimini/Prashna acquisitions an obvious home instead of flattening everything under one Hora bucket.
**Consequence:** `CLAUDE.md`'s layout block and `text_id` registry still show the pre-restructure flat paths — every path in both tables is now wrong. Not fixed as part of this entry; tracked in `STATE.md` Pending.
**Affects:** sanskrit-texts

## 2026-08-10: Raw Dharmashastra source ingest ahead of chunking (backfilled 2026-08-12)
**What:** Committed four raw Dharmashastra source texts unprocessed — `Dharmashastra/4605.txt`, `4607.txt`, `4609.txt`, `4617.txt` (commit `7fbfae1`). None are yet chunked into per-chapter JSON under the uniform schema. The same commit re-tagged two `hora_acharya` targets in `.propagates.yml` to `kind: prose`.
**Why:** Follows the existing precedent set by `Dharmashastra/ManuSmriti/9048.txt` (also committed raw, ahead of its own chunking pass) — land the raw source text first so it's tracked and diffable, chunk into JSON on a later pass rather than blocking ingestion on immediate digitization.
**Status:** Raw `.txt` files committed; chunking into `chapters/*.json` not yet done.
**Affects:** sanskrit-texts

## 2026-08-17: Second normalization wave — 3 texts migrated, 3 stopped on numbering
**What:** Migrated `saravali` (1,163), `asvalayana_grhya_sutra` (394) and MuhurtaChintamani's `MC_001` (37) off the pre-normalization shape onto the uniform schema — content asserted byte-for-byte, only field names and structure changed. `saravali`'s stale `category: "hora"` corrected to `parashari` (the last file using the retired value). MC_001 has English but no Hindi, so its shlokas carry `status: "partial"`. Corpus 222 → 225 conformant files, 18,965 → 20,559 normalized shlokas.
**Deliberately NOT migrated:** `manu_smriti` (12 files), `apastamba_dharma_sutra`, `apastamba_paribhasha_sutra` — 14 files, 4,737 records over only 1,520 distinct keys. Their numbering collides with *distinct* content (`1.1.1` appears 24 times with 24 different sūtras; `MS_001` claims chapter 1 but spans 1–5; `MS_012` contains a chapter "13" of a 12-chapter work). Converting them would yield schema-valid files that `seed_texts.py` then silently truncates by two-thirds, because it deduplicates by `(chapter, shloka)` with later-file-wins.
**Why:** the blocker for those three is numbering, not schema. Repairing it needs the source text and is a scholarly act, not a mechanical one — and a conversion that *looks* ingestible while dropping 2/3 of the content is worse than the honest defect.
**Also:** `CLAUDE.md`'s `category` enum listed 4 values against the 8 the data uses, and its `text_id` registry had 11 of 17 directories pointing at paths dead since commit `1cccca6`. Both corrected from disk. The same stale path map lived in `../astroacharya/scripts/list_sources.py`.
**Affects:** sanskrit-texts, astroacharya (`/texts` ingestion, `scripts/list_sources.py`)

## 2026-08-17: BPHS consolidated to one file; 4 mis-split chapters repaired
**What:** `BrihatParasharaHoraShastra/` was 11 JSON + 11 `.md` chunks; every sibling text keeps one of each. Now `BrihatParasharaHoraShastra.json` + `.md`. The chunks declared **102 chapters for a 97-chapter work**: the digitiser split 4 chapters mid-way and wrote each continuation as a *new* chapter, numbering it with the shloka at the split point and titling it with that shloka's verse text. Five chapter numbers (11, 20, 43, 55, 65) existed twice and 65 shlokas were discarded at ingest. Strays reattached to chapters 12, 53, 61 and 66 (×2), and the 5 missing shlokas restored from the stray titles as Sanskrit-only, `status: "untranslated"`.
**Why it is safe:** verified for all 5 before editing — `stray.number == precedingBlock.lastShloka + 1` and `stray.firstShloka == precedingBlock.lastShloka + 2`, a gap of exactly one every time. **Every affected chapter came out contiguous 1..N**, which is the proof; the merge refused to write while any chapter was non-contiguous.
**Left honest, surfaced by that guard:** ch 25 shloka 16 is genuinely absent from the digitisation (1–15, 17–87) and was not invented; ch 60 carried two shlokas numbered 12, the second parenthesised — a variant reading (पाठभेद), now `"12अ"` per the corpus's Devanagari-suffix convention, and the only parenthesised record in all of BPHS.
**Result:** 97 chapters, 3,937 shlokas; `bphs` ingests 3937 of 3937 (was 3867 of 3932). 92 of 97 chapters complete in both languages — the entire BPHS translation backlog is the 5 restored shlokas (12.11, 53.20, 61.55, 66.43, 66.65).
**Also:** `scripts/gen_inventory.py` counted `*.json` while labelling the column "Chapters" — invisibly wrong while most texts were one file per chapter, plainly wrong when BPHS reported 1 chapter for 97. It now counts real `chapters[]` entries; all 23 rows verified against the data (590 chapters, previously reported as 240 "chapter files").
**Affects:** sanskrit-texts, astroacharya (`/texts` ingestion)

## 2026-08-17: Two corpus-wide defects recorded, not fixed
**What:** (1) **`brihat_samhita` ships two recensions of the same work.** `Varahmihir_brihatsamhita.json` (105 chapters) and `Varahmihir_brihatsamhita2.json` (106, adds ch 38) both number chapters 1–106; 2,711 of 2,750 keys collide and 2,575 of those hold *different* text. 2,729 shlokas are discarded at ingest. File 2 is the fuller recension (longer translations, avg English 193 vs 173) and is already the one kept — but only because `seed_texts.py:96` sorts filenames and later wins. (2) **~506 disordered shloka numbers** remain across 25 chapters, beyond the 11 repaired where neighbours forced the answer.
**Why not fixed:** (1) is an editorial call — drop file 1 as superseded, or give it its own `text_id` to preserve the variant readings. (2) needs the source text; a heuristic that repairs 2.5% is not a repair, and inventing shloka numbers is worse than the defect.
**Status:** open. Corpus ingestion is 17,764 of 20,564 present shlokas.
**Affects:** sanskrit-texts, astroacharya

## 2026-08-17: Retire `scripts/gen_inventory.py`; `docs/INVENTORY.md` becomes hand-maintained
**What:** Deleted the generator. `docs/INVENTORY.md` is now maintained by hand, updated in the same commit as the corpus change it describes. Its header carries a one-line `node -e …` check that counts chapters straight from the JSON, and states that **the tree wins when the two disagree**. `docs/README.md`, `.propagates.yml` and `STATE.md` repointed; the two earlier DECISIONS entries that describe the generator are left untouched, per append-only.
**Why:** Rupali's call — a script whose entire job was writing one document earned less than it cost.
**Recorded against it, for whoever revisits this:** in the same session, the *hand-maintained* `text_id` registry in `CLAUDE.md` had 11 of 17 directories pointing at paths dead since `1cccca6`, while the generated INVENTORY was accurate; and the generator is what surfaced the chapter-count mislabelling. The mitigation for that risk is the verification one-liner, not the script.
**Found on the way out:** the generator was over-counting by one. It fell back to `else 1` for any JSON without a `chapters` list, which counted `Muhurta/MuhurtaChintamani/chapters/MC_REMAINING_RAW.json` — 320KB of raw `info`/`segments`, not a chapter. **Totals corrected 590 → 589.**
**Affects:** sanskrit-texts

## 2026-08-17: Remove the remaining processing scripts and `TODO.md`
**What:** Deleted `scripts/digitize.py`, `scripts/translate.py` and `TODO.md`, plus `scripts/__pycache__/` and 9 stray `.DS_Store` files. `scripts/` now holds only `install-hooks.sh`, which wires the T33 hygiene githooks and is not a processing script.
**Why (scripts):** `CLAUDE.md` has said since 2026-06-20 — *"Do not commit processing scripts (batch\*.py, inject\*.py etc.) to this repo — they were throwaway tools and have been removed. Future translation patches should directly update JSON."* Both landed anyway in `1cccca6`, and `STATE.md` had been carrying them as a known violation ever since. This closes it, on the same argument that retired `gen_inventory.py`: this is a data repository, and a corpus change should be a change to the corpus.
**Why (`TODO.md`):** **this supersedes the 2026-06-09 decision above**, which kept it "as historical with a frozen banner". Its 8 items (5 completed, 3 pending) have been fully absorbed into `STATE.md`, and the `### P2 — Translation injection (from TODO.md)` heading was the last thing still pointing at it. Git history keeps the file.
**Kept deliberately:** `scripts/install-hooks.sh`; every editor/agent config (`.claude/`, `.cursor/`, `.kiro/`, `.mcp.json`, …); and `Hora/Parashari/Saravali/saravaliofkalyan01kalyuoft.pdf` — a 17MB source scan held locally and gitignored under the source-out-of-git policy, **not** clutter.
**Affects:** sanskrit-texts

## 2026-08-18: One format — sources in `../sanskrit-texts-sources/`, translations here
**What:** (1) Moved every source file out of this repo — 14 Devanagari `.md` transcriptions, 17 raw OCR `.txt` (all of them *committed*, against the policy), and `MC_REMAINING_RAW.json` (raw extraction living as `.json`, which the extension-based sweep missed). Deleted Saravali's 17MB PDF as a byte-identical duplicate of the copy already in sources. (2) Consolidated 221 per-chapter files into 15 single-text files, so every digitised text is now `<Category>/<School?>/<Text>/<Text>.json`. `.gitignore` gained a repo-wide `*.txt` beside the existing `*.pdf`, and its two dead rules (pre-`1cccca6` `Hora/UttaraKalamrita/` paths, matching nothing for weeks) were removed.
**Why:** the repo was mixing three things — translations, raw sources, and metadata — and the JSON itself had two incompatible layouts (8 texts direct, 15 under `chapters/`). That split is why `list_sources.py` has to search both locations and why the registry had to spell out which convention each text followed. One question, one answer.
**Data unchanged, and proved so:** chapters 589 → 589, shlokas 25,301 → 25,301, ingestible 17,764 → 17,764, per-text losses byte-identical. Files 230 → 35.
**Four texts deliberately not consolidated:** `BrihatSamhita` (105 duplicate chapter numbers — the two files are separate *recensions*; merging would conflate two works, not tidy one), and `ManuSmriti` + both Apastamba sutras (still `sutras[]`-shaped, blocked on numbering rather than format).
**Reversed a decision from the plan:** `Jatakaparijatah` (55), `Laghujatakam` (14) and `MinarajaYavanajataka` (1) were to be left split for carrying duplicate keys. On inspection that was wrong — the seeder dedupes by `(chapter, shloka)` across *all* files of a `text_id`, so layout changes nothing about their visibility. They were consolidated with the counts reported instead.
**Near miss worth keeping:** macOS is case-insensitive. Writing `Phaladeepika.json` landed on the same inode as `phaladeepika.json`, and unlinking the "source" afterwards deleted what had just been written — 851 shlokas, 28 chapters. Caught **only** by the invariant baseline captured before starting; restored from git and verified by reading the content back rather than trusting `checkout`. The merge now writes to a temp name, removes sources, renames, and re-reads to assert the shloka count survived. **Capture the baseline before a bulk move; the guard is worth more than the script.**
**Affects:** sanskrit-texts, astroacharya (unaffected in fact — `TEXT_ID_TO_PATH` points at text *directories*, which did not move; 10/10 resolve, suite 1001 passed)

## 2026-08-18: BrihatSamhita consolidated — and it was never two recensions
**What:** `Samhita/BrihatSamhita/` is now one file, `BrihatSamhita.json` — 106 contiguous chapters, 2,771 shlokas, 0 duplicate keys, 100% translated. Built as the **union of the two files with `Varahmihir_brihatsamhita2.json` winning on shared keys**, which is precisely what `seed_texts.py:92-94` already computed (sorted filenames, later wins). Ingestion was therefore **unchanged at 2,771**; what changed is that the corpus no longer carries the collision. File 1's **21 unique keys are preserved** by the union.
**Correcting the earlier record:** the 2026-08-17 entries called these "two recensions of the same work" and said merging would conflate two texts, needing an editorial decision. **That was wrong.** Of 2,711 shared keys, 2,574 differ only in sandhi and word-splitting — `जगतः प्रसूतिः विश्वात्मा` vs `जगतः प्रसूतिर्विश्वात्मा`, `ग्रन्थविस्तरस्यार्थम्` vs `ग्रन्थविस्तरस्य अर्थम्` — 66 differ in translation only, and 71 are identical. It is one text digitised twice under different orthographic conventions. File 2 was better on every axis measured: 106 chapters to 105 (it alone has ch 38), 39 keys file 1 lacks, 0 internal duplicates against file 1's 18, and richer English (avg 193 vs 173 chars).
**Effect on the corpus-wide collision:** **2,800 → 71.** All that remains is intra-chapter and pre-existing: `jataka_parijata` 55, `laghu_jatakam` 14, `minaraja_yavana_jataka` 1, `yajusha_jyotisham` 1.
**Affects:** sanskrit-texts, astroacharya (ingestion unchanged; suite 1001 passed)

## 2026-08-18: ManuSmriti and Apastamba need re-digitisation, not renumbering
**What:** Checked the two remaining off-schema texts against their canonical structures and concluded the numbering **cannot be recovered from the JSON**. `STATE.md` P1 restated accordingly — "blocked on numbering" understated it.
**Canonical structures:** Manusmriti is 12 adhyāyas, ~2,684 verses (ch 1 = 119, ch 2 = 249). The Apastamba Dharmasūtra is part of the Kalpasūtra and runs Praśna → Paṭala → Khaṇḍa → sūtra, with khaṇḍas typically holding ~4 sūtras — so **`1.1.1` is a correct citation, not a broken number**, which was the opposite of the working assumption.
**Why the data cannot reach them:** Manusmriti's leading component runs **1–33** for a 12-chapter work, "chapter 1" holds 1,516 records against a canonical 119, and `MS_001` alone contains **89 fragmentary cycles** with gaps (`1.14 → 1.18`). Apastamba's 1,437 records carry 219 bare integers, 13 malformed `..10`, and 15 of the literal placeholder **`X.X.21`/`X.X.22`** — the digitiser itself recording "prefix unknown".
**Method note worth keeping:** the first 30 Apastamba records form a clean `1.1.1…1.1.14` cycle, and on that basis the numbering looked merely truncated and mechanically reconstructible. Across the full file it is not. **A 30-record sample gave a confident wrong answer about a 1,437-record file** — the same shape as `rule:discernment-checks` §4.
**Sources held:** `../sanskrit-texts-sources/Dharmashastra/{4605,4607,4609,4617}.txt` and `ManuSmriti/{manu_clean,9048}.txt`. `manu_clean.txt` is a 2.8MB scanned book on a **single line** — the 1909 Nirnaya Sagar edition with front matter and Kullūka's commentary — so re-digitisation is a project, not a patch.
**References:** en.wikipedia.org/wiki/Manusmriti · en.wikipedia.org/wiki/Apastamba_Dharmasutra · wisdomlib.org/hinduism/book/apastamba-dharma-sutra
**Affects:** sanskrit-texts
