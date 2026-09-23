"""Refuse a destructive operation against anything but the local corpus store.

WHY THIS IS A MODULE AND NOT A COPY IN EACH CALLER. On 2026-09-16 the TRUNCATE fixture in
`tests/conftest.py` grew a host/port/`_test`-suffix guard (G59). `make clean-db` did not
grow anything: it runs `alembic downgrade base`, which drops every table, against
`OWNER_DSN` -- whose default is the DEVELOPMENT database `sanskrit_texts`, not a `_test`
one -- with no host check, no port check, and no confirmation. Its `## (local only)` help
text was a label, not an enforced property.

So the repo held an elaborate guard protecting the test fixture from the dev corpus, and
nothing at all protecting the dev corpus from the Makefile. Found by audit 2026-09-23.

**The two callers need DIFFERENT policies, and that is the point of splitting the check:**

| caller | host+port | database |
|---|---|---|
| `tests/conftest.py` TRUNCATE | local only | must end `_test` -- the dev corpus is on the same host and port, and a test run must never empty it |
| `make clean-db` | local only | `sanskrit_texts` IS the intended target, so no suffix rule -- but a human must say so |

`assert_local_store` is the half they share. Each caller adds its own second clause, which
is what `rule:safety-flag-needs-a-test` means by scoping a guard to the threat you have
rather than the one you imagined: G59's first fix checked host and port, felt sufficient,
and was not.
"""

from __future__ import annotations

import argparse
import os
import sys
import urllib.parse

# `""` covers a DSN with no host at all (a unix socket), which is local by construction.
LOCAL_HOSTS = {"127.0.0.1", "localhost", "::1", ""}
EXPECTED_PORT = 5433  # ports.yml allocates this to Vipin Kaushik/sanskrit-texts/postgres


def split(dsn: str) -> tuple[str, int | None, str]:
    """`(host, port, database)` from a SQLAlchemy/libpq URL, lowercased host."""
    parsed = urllib.parse.urlsplit(dsn)
    return (parsed.hostname or "").lower(), parsed.port, (parsed.path or "").lstrip("/")


def assert_local_store(dsn: str, action: str) -> None:
    """Raise unless `dsn` names a store on the local host and the allocated port.

    `action` appears in the message, so the refusal says what was about to happen rather
    than only that something was refused.
    """
    host, port, database = split(dsn)
    if host not in LOCAL_HOSTS or port != EXPECTED_PORT:
        raise RuntimeError(
            f"refusing to {action} a non-local corpus store: host={host!r} port={port!r} "
            f"database={database!r}. Only {sorted(LOCAL_HOSTS - {''})} on port "
            f"{EXPECTED_PORT} is the local corpus store."
        )


def _main(argv: list[str] | None = None) -> int:
    """Preflight for `make clean-db`, which drops every table via `alembic downgrade base`.

    Deliberately NOT a `--dry-run`-style flag on the destructive command itself. The
    corollary in `rule:safety-flag-needs-a-test` is that you never run a command to find
    out what it would do; this runs BEFORE the destructive command and writes nothing, so
    there is no unsafe path for it to guard the wrong side of.
    """
    ap = argparse.ArgumentParser(description=_main.__doc__)
    ap.add_argument("--dsn", required=True)
    ap.add_argument("--action", default="drop every table in")
    args = ap.parse_args(argv)

    try:
        assert_local_store(args.dsn, args.action)
    except RuntimeError as e:
        print(f"REFUSED: {e}", file=sys.stderr)
        return 2

    _, _, database = split(args.dsn)
    # Local is necessary and not sufficient: the dev corpus is local, and losing it is the
    # whole hazard. Require a human, unless a caller has said in advance that it is fine.
    if os.environ.get("CORPUS_ALLOW_DESTROY", "").strip() in ("1", "true", "yes"):
        print(f"CORPUS_ALLOW_DESTROY set — proceeding to {args.action} {database!r}.")
        return 0
    if not sys.stdin.isatty():
        print(
            f"REFUSED: about to {args.action} {database!r}, but stdin is not a terminal so "
            "nobody can confirm. Set CORPUS_ALLOW_DESTROY=1 to mean it in a script.",
            file=sys.stderr,
        )
        return 2

    print(f"About to {args.action} the database {database!r} on {EXPECTED_PORT}.")
    print("Every table is dropped. The corpus JSON in git is unharmed and `make import`")
    print("rebuilds it -- but any APPROVED review rows are not in git and do not come back.")
    try:
        answer = input(f"Type the database name to confirm [{database}]: ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\nREFUSED: no confirmation.", file=sys.stderr)
        return 2
    if answer != database:
        print(f"REFUSED: got {answer!r}, expected {database!r}.", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
