# sanskrit-texts — docs (the wiki)

From-canon Sanskrit shloka corpus. **One JSON file per text** (standardised 2026-08-18),
consumed by **astroacharya**'s from-canon compute — each primitive cites
`@source(("<text_id>", chapter, [shlokas]))`.

## The docs

| Doc | What |
|-----|------|
| [`INVENTORY.md`](INVENTORY.md) | **The registry** — every text's `text_id`, path, chapter/shloka counts, translation state, count-authority tier. |
| [`CANONICAL_COUNTS.md`](CANONICAL_COUNTS.md) | The evidence behind the counts — marker grammars, tier definitions, canonical totals, per-text caveats. |
| [`SOURCES.md`](SOURCES.md) | Source manifest — where each source came from, its tier and attribution. |
| [`LICENSES.md`](LICENSES.md) | Upstream licence terms and what each obliges. **Sanskrit Documents is not open-licensed.** |
| [`VEDIC_CORPUS.md`](VEDIC_CORPUS.md) | The śākhā map — 51 Vedic texts by Veda × layer, and the Vipin/Youvan ownership split. |
| [`BPHS_Master_Lexicon.md`](BPHS_Master_Lexicon.md) | Curated BPHS term lexicon, with glosses and synonyms. |
| [`BPHS_Only_Terminology.md`](BPHS_Only_Terminology.md) | BPHS term set without glosses. |
| [`DECISIONS.md`](DECISIONS.md) | Pointer — the log lives at `propagation/state/sanskrit-texts/DECISIONS.md`. |
| [`plans/`](plans/) · [`plans/README.md`](plans/README.md) | Digitization / ingestion plans, and the convention for filing them. |

### The store, and the translation pipeline

Added 2026-09-23. **These thirteen existed and this table did not list them**, while
`../CLAUDE.md` asserted that this file "indexes every other doc" — so over half the tree was
invisible from the one page meant to orient a reader to it. Seven had no inbound reference from
anywhere in the repo at all.

| Doc | What |
|-----|------|
| [`DATABASE.md`](DATABASE.md) | The Postgres store — schema, importer, exporter, the publication gate, what is excluded. |
| [`TRANSLATION_CONTRACT.md`](TRANSLATION_CONTRACT.md) | **Normative.** What a translation must be, and what must never be written into a served field. |
| [`TRANSLATION_BACKLOG.md`](TRANSLATION_BACKLOG.md) | The outstanding work, split into three jobs that must not be handed out as one. Counts derived by `scripts/translation_backlog.py`. |
| [`TRANSLATION_AUDIT.md`](TRANSLATION_AUDIT.md) | **Generated** by `scripts/translation_audit.py` — per-text defect table. Regenerate, never hand-edit. |
| [`SPOT_CHECK.md`](SPOT_CHECK.md) | **Generated** by `scripts/spot_check.py` — sampled verses for human review. |
| [`TERM_LEDGER.md`](TERM_LEDGER.md) | Term-by-term rendering decisions, so one Sanskrit term is not translated four ways. |
| [`ENTITY_ROOTS.md`](ENTITY_ROOTS.md) | Entity root forms used by `scripts/entity_roots.py`. |
| [`RELATION_MARKERS.md`](RELATION_MARKERS.md) | The anchored marker grammar (`=योगे`, `=तुङ्गे`) behind `scripts/relation_markers.py`. |
| [`FEATURE_EXTRACTION_METHOD.md`](FEATURE_EXTRACTION_METHOD.md) | How `scripts/tag_features.py` derives features, and what it refuses. |
| [`PHALA_CATEGORIES.md`](PHALA_CATEGORIES.md) | The phala category set applied by `scripts/apply_phala.py`. |
| [`EMBEDDING_EVAL.md`](EMBEDDING_EVAL.md) | Embedding evaluation method and results. |
| [`RETRIEVAL_EVAL.md`](RETRIEVAL_EVAL.md) | Retrieval evaluation — **frozen 2026-09-15, BPHS only**; it says so itself and does not generalise. |
| [`AUDIT-2026-09-23.md`](AUDIT-2026-09-23.md) | Audit of the 80 non-corpus files — what was fixed, what is still open, each with the command that reproduces it. |
| [`archive/`](archive/) | Drained state and superseded records, kept verbatim with their own dated headers. |

Repo orientation: [`../README.md`](../README.md) + [`../CLAUDE.md`](../CLAUDE.md).
Hazards that have already cost time:
[`GOTCHAS.md`](../../propagation/state/sanskrit-texts/GOTCHAS.md).

## Adding a text (the workflow)

```
1. acquire the source        →  ../sanskrit-texts-sources/<Category>/…/<Text>/   (never committed here)
2. convert                   →  <Category>/<School?>/<Text>/<Text>.json          (ONE file, whole text)
3. record provenance         →  docs/SOURCES.md
4. add the row by hand       →  docs/INVENTORY.md, and correct the Totals line
5. commit                    →  the INVENTORY.md change fires propagation (below)
```

`INVENTORY.md` is **hand-maintained** — the generator was retired 2026-08-17. It summarises the
tree, so the tree wins when they disagree; the verification one-liner is in its header.

## State-based propagation

The corpus is the **producer**; astroacharya is the **consumer**. Edges are declared in
[`../.propagates.yml`](../.propagates.yml): when `docs/INVENTORY.md` changes (a text added,
renamed, or re-scoped), propagation fires a drift row against astroacharya's canon trackers —
`app/masters/hora_acharya/reference.md` and `DATA_GAPS.md` — so what the compute can `@source`
never silently diverges from what the corpus holds. Flow diagram:
[`INVENTORY.md §State-based propagation flow`](INVENTORY.md#state-based-propagation-flow).

## Source-of-truth / policy

- **Canonical data = the per-text JSON.** That is what is committed and what astroacharya reads.
- **Sources are kept out of git** — they live in `../sanskrit-texts-sources/` (~369 MB) and are
  not the canonical form. `.gitignore` enforces it.
- **Machine drafts never publish.** They live in `english_draft` / `hindi_draft`; astroacharya's
  seeder copies an allowlist that excludes them, so the unsafe path is unreachable rather than
  merely discouraged. Verification promotes a draft into `english` / `hindi`.
