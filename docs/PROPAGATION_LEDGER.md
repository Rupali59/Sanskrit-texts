# Propagation Ledger — sanskrit-texts

**Empty, and expected to stay that way.** This repo became a ledger-owning propagate
workspace on 2026-08-17 so its propagation rows would commit alongside the change that
caused them, instead of landing in the workspace ledger a level up that this repo does not
track. The sibling `PROPAGATION_LEDGER.jsonl` is the authoritative store and is currently
0 bytes.

**Nothing writes v1 drift rows any more.** The launchd watcher that used to was retired
2026-08-14 (`~/.claude/skills/propagate/docs/DECISIONS.md`). Drift is now *derived from
content on demand* rather than remembered, so an empty ledger here is the correct state,
not a missing one.

**For current state, derive it — do not read this file:**

```bash
node ~/.claude/skills/propagate/cli.mjs reconcile      # edge state, derived from content
node ~/.claude/skills/propagate/cli.mjs graph --node <file>   # one file's couplings
```

**This file is hand-written and must not be regenerated.** `renderMarkdown` still emits
"Watcher healthy" and "Watcher writes drift rows; `/propagate drain` marks them done" —
both false since 2026-08-14, filed as propagate **N31**. Running it here would replace this
text with those claims. The two `ManavDaehi` ledgers carry the same hand-written warning
for the same reason.
