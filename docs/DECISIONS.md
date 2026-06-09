# sanskrit-texts — Decisions (append-only)

Project-scoped decisions. Workspace-wide decisions live in `../../docs/DECISIONS.md`.
Convention: `../../docs/STATE_MANAGEMENT.md`. Never edit past entries; supersede by appending.

## 2026-06-09: Adopt STATE.md / DECISIONS.md convention; subsume TODO.md
**What:** sanskrit-texts adopts the workspace state-management convention. STATE.md at repo root, DECISIONS.md under tracked `docs/`. The existing `TODO.md` digitization checklist (8 items, 5 completed + 3 pending) is copied into STATE.md Pending/Completed; `TODO.md` retained as historical with a frozen banner. Sixth and final sibling onboarded.
**Why:** This repo is a data corpus, not a code project — its "state" is the digitization + translation progress matrix. STATE.md gives that progress a uniform shape matching the four code-project siblings, so a workspace sweep over `*/STATE.md` returns coherent answers for both code and data repos.
**Refs:** workspace `docs/STATE_MANAGEMENT.md`; astroacharya commit `98f7bb3`; Astroclarity `60008c3`; Campaigner `f880cff`; VipinKaushik-mb `d652cec`.
