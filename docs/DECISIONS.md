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
