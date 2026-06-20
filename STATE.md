# sanskrit-texts — State

Last updated: 2026-06-20

Convention: `../docs/STATE_MANAGEMENT.md` (adopted 2026-06-09).
Decisions: [`docs/DECISIONS.md`](./docs/DECISIONS.md) (project `docs/` is tracked).
Plans: [`docs/plans/README.md`](./docs/plans/README.md) (adopted 2026-06-20, 6th sibling).
Supersedes: `TODO.md` (digitization checklist subsumed below; file retained as historical).

## ⚠️ Uncommitted working tree (as of 2026-06-20)

The corpus is **complete in the working tree but largely uncommitted.** HEAD (`0f2b00c`) still carries the pre-normalization schema. Pending commit:

- **Schema-normalization sweep** — 331 Hora + 28 Samhita JSON files migrated to the uniform schema (legacy `source`/`header`/`english_meaning` → `text_id`/`english`/`status`). See `docs/DECISIONS.md` 2026-06-20.
- **New digitizations (untracked)** — Uttara Kalamrita (`uttara_kalamrita.json`) + Minaraja Uttarakhanda (`MS_040`–`MS_071`).
- **`.gitignore` fix + `docs/plans/README.md` + `CLAUDE.md` registry → 100%** (this catch-up).
- **Cleanup needed before commit:** untracked throwaway processing scripts (`Samhita/BrihatSamhita/update_shlokas*.py`, `template.py`) and temp artifacts (`temp_untranslated*.json`, `ch47_*.json`) must NOT be committed — see `CLAUDE.md` → "Do not commit processing scripts". The new `.gitignore` ignores `*.py[cod]`/`__pycache__/` but not the loose `.py`/`temp_*.json` themselves; remove or ignore them before staging.

## Now (in flight)

- **Commit the corpus** — stage the normalization sweep + new digitizations; exclude throwaway scripts/temp files. Recommended split: (1) schema normalization, (2) new digitizations, (3) docs/state catch-up.

## Active initiatives

- None.

## Pending (by priority)

### P1 — Digitization (from TODO.md)

- None pending.

### P2 — Translation injection (from TODO.md)

- None pending. All targeted translation injections completed.

### Possibly migrated from workspace `../TODOS.md`

- _None directly owned._ TM-068 (vendor-derived JSON deprecation sweep) mentions `SANSKRIT_TEXTS_PATH` but the work is astroacharya-side. TM-041 (Jyotish texts migration from Youvan into AstroAcharya) treats this repo as the destination — see workspace TODOS TM-041 for the producer side.

## Completed

- ✅ **All 14 texts at 100% translation** — full registry in `CLAUDE.md`. Milestone reached in working tree 2026-06-20 (commit pending).
- ✅ **Uniform-schema normalization sweep** — 331 Hora + 28 Samhita files migrated off legacy fields onto the `CLAUDE.md` schema; counts deduplicated by `(chapter, shloka)`. See `docs/DECISIONS.md` 2026-06-20.
- ✅ **Caught up to workspace plans convention** — added `docs/plans/README.md`; fixed malformed `.gitignore` that was hiding the tracked `docs/` tree (mirrors Astroclarity T13).
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
