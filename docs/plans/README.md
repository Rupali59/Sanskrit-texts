# sanskrit-texts plans

Per workspace convention (`~/Documents/GitHub/Vipin Kaushik/docs/plans/README.md`), project-specific plans live in this directory.

**Layout (2026-06-20):** lives at `docs/plans/`. Adopted on 2026-06-20 when sanskrit-texts caught up to the workspace state-management + plans convention (the 6th sibling did not receive it during the 2026-06-19 sweep). Same pattern as Astroclarity's T13 follow-up: `docs/` was previously gitignored, so `docs/`-tracked files only became visible after the `.gitignore` un-ignore landed.

## What goes here

Plans driving sanskrit-texts-specific work — new text digitizations (next stubs: Saravali, SarvarthaChintamani, PrashnaMarga, JatakaTattvam, Siddhanta + SamudrikShastra), schema-normalization sweeps, proofreading passes against `REFERENCES.md`, translation-injection batches.

## What does NOT go here

- Cross-cutting plans spanning sanskrit-texts + sibling repos (e.g. the `/texts` API contract consumed by astroacharya) → workspace `docs/plans/`
- Session-scratch / brainstorming → `~/.claude/plans/`
- gstack review artifacts → `~/.gstack/projects/Rupali59-sanskrit-texts/` (user-local; never committed)

## Provenance

When a plan is promoted from `~/.claude/plans/` to this directory, add a one-line HTML comment at the top:

```markdown
<!-- Promoted YYYY-MM-DD from ~/.claude/plans/<original-name>.md -->
```
