# sanskrit-texts — docs (the wiki)

From-canon Sanskrit shloka corpus. Texts are digitized, chunked into per-chapter JSON,
and consumed by **astroacharya**'s from-canon compute (each primitive cites
`@source(("<Text>", chapter, [shlokas]))`, per `MASTER_DECISIONS D17`).

## Start here

| Doc | What |
|-----|------|
| [`INVENTORY.md`](INVENTORY.md) | **The catalog** — every text by category, with chapter counts + links (generated). |
| [`BPHS_Master_Lexicon.md`](BPHS_Master_Lexicon.md) | Canonical BPHS term lexicon. |
| [`BPHS_Only_Terminology.md`](BPHS_Only_Terminology.md) | BPHS-only terminology set. |
| [`DECISIONS.md`](DECISIONS.md) | Append-only corpus decisions (schema, categorization, policy). |
| [`plans/`](plans/) | Digitization / ingestion plans. |

Per-text detail lives in each text's own `README.md` (linked from `INVENTORY.md`).
Repo orientation: [`../README.md`](../README.md) + [`../CLAUDE.md`](../CLAUDE.md).

## Adding inventory (the workflow)

The corpus grows continuously. Keep the wiki + propagation in sync with one step:

```
1. digitize + chunk the text  →  <Category>/<School?>/<Text>/chapters/*.json (+ README.md)
2. python scripts/gen_inventory.py        # regenerates docs/INVENTORY.md
3. commit                                 # INVENTORY.md change fires propagation (below)
```

`INVENTORY.md` is **generated — never hand-edit it**; edit the tree + rerun the script.

## State-based propagation

The corpus is the **producer**; astroacharya is the **consumer**. Edges are declared in
[`../.propagates.yml`](../.propagates.yml): when `docs/INVENTORY.md` changes (a text added,
renamed, or re-chunked), the workspace propagation watcher fires a drift row against
astroacharya's canon trackers (`reference.md`, `DATA_GAPS.md`) — so what the compute can
`@source` never silently diverges from what the corpus actually holds. Full flow diagram in
[`INVENTORY.md §State-based propagation flow`](INVENTORY.md#state-based-propagation-flow).

## Source-of-truth / policy

- **Canonical data = the per-chapter JSON.** That's what's committed and what astroacharya reads.
- **Source scans (PDF, raw OCR `.txt`) are kept local, not committed** — they bloat git and aren't
  the canonical form. (Decision logged in `DECISIONS.md`.)
