# sanskrit-texts — State

Last updated: 2026-06-09

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

- **Inject English + Hindi translations for Minaraja Shrivriddhayavanajataka.**
- **Inject English + Hindi translations for Phaladeepika.**

### Possibly migrated from workspace `../TODOS.md`

- _None directly owned._ TM-068 (vendor-derived JSON deprecation sweep) mentions `SANSKRIT_TEXTS_PATH` but the work is astroacharya-side. TM-041 (Jyotish texts migration from Youvan into AstroAcharya) treats this repo as the destination — see workspace TODOS TM-041 for the producer side.

## Completed (from TODO.md)

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
