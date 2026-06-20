# sanskrit-texts — State

Last updated: 2026-06-20

Convention: `../docs/STATE_MANAGEMENT.md` (adopted 2026-06-09).
Decisions: [`docs/DECISIONS.md`](./docs/DECISIONS.md) (project `docs/` is tracked).
Plans: [`docs/plans/README.md`](./docs/plans/README.md) (adopted 2026-06-20, 6th sibling).
Supersedes: `TODO.md` (digitization checklist subsumed below; file retained as historical).

## Recently shipped (2026-06-20)

The full corpus + catch-up work is committed and pushed (`main` @ `e23cbe2`). Five commits:

- `f2034e2` `refactor:` schema normalization (137 modified) + per-chapter→chunk consolidation (165 deletions, 2 `.md` renames)
- `3792b90` `feat:` new digitizations — Uttara Kalamrita + Minaraja Uttarakhanda (35 files) → all 14 texts 100%
- `b13cd88` `chore(state):` docs/state convention catch-up (`.gitignore` un-ignore `docs/`, `docs/plans/README.md`, registry → 100%)
- `da480bd` `chore(hooks):` T33 per-project hygiene hooks (6th-sibling parity) + `scripts/install-hooks.sh`
- `e23cbe2` `docs(decisions):` record T33 install

Throwaway processing scripts + temp artifacts were deleted; raw OCR intermediates + tool-local config are now gitignored (kept on disk). See `docs/DECISIONS.md` 2026-06-20 (3 entries).

## Now (in flight)

- None.

## Active initiatives

- None.

## Known signal

- `size-caps` (hygiene daemon) reports **`CLAUDE.md` at 164/180 lines (yellow, 91%)** — warn-only, goes red at 180. Trim on next edit (MCP/code-review-graph section + layout block are the fattest). Not urgent.

## Pending (by priority)

### P1 — Digitization backlog (README-only stubs, not yet digitized)

Scope candidates, not committed work — confirm intent before starting. Each is currently a `README.md` stub (or raw text) awaiting a digitized + translated `.json` under the uniform schema.

- **Hora:** Saravali, SarvarthaChintamani, PrashnaMarga, JatakaTattvam
- **Hora (raw text on disk, not yet JSON):** ThreeHundredImportantCombinationsRaman (`Three-Hundred-Important-Combinations.txt`)
- **Siddhanta:** Aryabhatiya, BrahmasphutaSiddhanta, Panchasiddhantika, SiddhantaShiromani, SuryaSiddhanta
- **SamudrikShastra:** Hastamuktavali, SamudrikaTilaka

Note: per parent workspace decision (2026-05-04), AstroAcharya owns all Jyotish source texts; Tantra/Mantra/Philosophy belong to Youvan Prakashan. Confirm a candidate is in-scope for this corpus before digitizing.

### P2 — Translation injection (from TODO.md)

- None pending. All targeted translation injections completed.

### Possibly migrated from workspace `../TODOS.md`

- _None directly owned._ TM-068 (vendor-derived JSON deprecation sweep) mentions `SANSKRIT_TEXTS_PATH` but the work is astroacharya-side. TM-041 (Jyotish texts migration from Youvan into AstroAcharya) treats this repo as the destination — see workspace TODOS TM-041 for the producer side.

## Completed

- ✅ **All 14 texts at 100% translation** — full registry in `CLAUDE.md`. Shipped 2026-06-20 (`3792b90`).
- ✅ **Uniform-schema normalization sweep** — 137 modified + 165 consolidated files onto the `CLAUDE.md` schema; counts deduplicated by `(chapter, shloka)` (`f2034e2`). See `docs/DECISIONS.md` 2026-06-20.
- ✅ **Caught up to workspace conventions** — `docs/plans/README.md`, `.gitignore` un-ignore of `docs/`, and **T33 per-project hygiene hooks** (`b13cd88`, `da480bd`); registered in workspace `docs/CONTEXT-BUDGET.md [active_lines]`.
- ✅ Digitize and translate Kalidasa's *Uttara Kalamrita* (324 shlokas across 9 chapters) into English and Hindi, bringing the entire text to 100% translated.
- ✅ Translate the Uttarakhanda section (Chapters 40–71) of Minaraja Shrivriddhayavanajataka (1,887 shlokas across 34 JSON files) into English and Hindi, bringing the entire Minaraja text to 100% translated.
- ✅ Digitize the Uttarakhanda section (Chapters 40–71) of Minaraja Shrivriddhayavanajataka (Volume II, Baroda 1976), adding 1,887 shlokas across 34 JSON files.
- ✅ Completed all remaining 270 untranslated shlokas for Brihat Samhita (chapters 93–106) in `Varahmihir_brihatsamhita.json` and all 1026 untranslated shlokas in `Varahmihir_brihatsamhita2.json`, bringing both files to 100% translated.
- ✅ Completed all remaining 152 untranslated shlokas for Jataka Parijata (chapters JP_014, JP_017), bringing it to 100% translated.
- ✅ Completed all remaining 10 untranslated shlokas for Minaraja Shrivriddhayavanajataka (chapters MS_014, MS_015, MS_024अ), bringing it to 100% translated.
- ✅ Completed all remaining 63 untranslated shlokas for Phaladeepika (chapters 24, 26, 27, 28), bringing it to 100% translated.
- ✅ Completed all remaining 49 untranslated shlokas across Chapters 84, 86, 87, 88, 89, and 90 in `BPHS8190.json`, bringing the entire file (Chapters 81–90) to 100% translated.
- ✅ Digitize Phaladeepika (chapters + shlokas JSON).
- ✅ Digitize Shatpanchashika (chapters + shlokas JSON).
- ✅ Digitize Shivasvarodayah (chapters + shlokas JSON).
- ✅ English + Hindi translations for all Aarchjyotisham shlokas (`11d936a`).
- ✅ Reorganize texts into canonical Jyotisha categories (`dbba4f2`).

## Linked plans

- [`REFERENCES.md`](./REFERENCES.md) — source-of-truth proofreading references.
- [`AGENTS.md`](./AGENTS.md) — agent-facing context.
- [`docs/BPHS_Master_Lexicon.md`](./docs/BPHS_Master_Lexicon.md) — BPHS terminology.
- [`docs/BPHS_Only_Terminology.md`](./docs/BPHS_Only_Terminology.md) — BPHS-exclusive terminology.

### Related gstack ledgers (scratch / memory — not plans)

- `~/.gstack/projects/Rupali59-sanskrit-texts/` (if present) — designs / reviews / learnings.
