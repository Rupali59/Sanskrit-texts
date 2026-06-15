# sanskrit-texts — State

Last updated: 2026-06-15

Convention: `../docs/STATE_MANAGEMENT.md` (adopted 2026-06-09).
Decisions: [`docs/DECISIONS.md`](./docs/DECISIONS.md) (project `docs/` is tracked).
Supersedes: `TODO.md` (digitization checklist subsumed below; file retained as historical).

## Now (in flight)

- Local uncommitted state: `.DS_Store` (deleted/modified) + `.gitignore` edit. Unrelated to this state-system adoption; left untouched.
- Branch `main` is 1 commit ahead of `origin/main` (`e929691` docs CLAUDE.md update).

## Active initiatives

- **Translation injection wave** — inject English + Hindi translations into the remaining Jyotisha texts. Schema established with Aarchjyotisham (`11d936a`).

## Pending (by priority)

### P1 — Digitization (from TODO.md)

- **Uttarakhanda of Minaraja Shrivriddhayavanajataka** — find + digitize. Purvakhanda is complete.

### P2 — Translation injection (from TODO.md)

- None pending. All targeted translation injections completed.

### Possibly migrated from workspace `../TODOS.md`

- _None directly owned._ TM-068 (vendor-derived JSON deprecation sweep) mentions `SANSKRIT_TEXTS_PATH` but the work is astroacharya-side. TM-041 (Jyotish texts migration from Youvan into AstroAcharya) treats this repo as the destination — see workspace TODOS TM-041 for the producer side.

## Completed (from TODO.md)

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
