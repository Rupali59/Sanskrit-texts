# AGENTS.md

**Read [`CLAUDE.md`](./CLAUDE.md).** It is the guidance for this repository and this file
does not duplicate it.

## Why this file is a pointer

Until 2026-09-02 it held 38 lines of generic `code-review-graph` boilerplate — byte-identical
to the gitignored `.cursorrules` and `.windsurfrules` — with no sanskrit-texts content at all.
Two of its claims were wrong here:

- It said *"ALWAYS use the code-review-graph MCP tools BEFORE using Grep/Glob/Read."*
  `CLAUDE.md` §"Code exploration" says the opposite for this repo: it is a **JSON data
  corpus**, so callers/impact/tests tools do not apply to the data — use Grep, Read, or the
  Explore agent.
- It said *"the graph auto-updates on file changes (via hooks)."* It does not. A git
  **pre-commit** hook rebuilds it, so the graph always lags uncommitted work — which is
  precisely the work you are asking it about. Verify with `code-review-graph status` before
  trusting it; `rule:tool-priority` is canonical.

Keeping a second file that answered the same questions differently is how the two drifted.
