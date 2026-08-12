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
