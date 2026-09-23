"""`make clean-db` must refuse a non-local store, and must not drop the dev corpus unasked.

Found by audit 2026-09-23. `clean-db` runs `alembic downgrade base` -- which drops every
table -- against `OWNER_DSN`, whose default is the DEVELOPMENT database `sanskrit_texts`.
It had no host check, no port check and no confirmation; its `## (local only)` help text
was a label, not an enforced property.

The asymmetry is what made it worth fixing: `tests/conftest.py` carried an elaborate guard
protecting the test fixture FROM the dev corpus (G59), while nothing protected the dev
corpus from the Makefile.

Per `rule:safety-flag-needs-a-test` these construct the inputs that must be refused rather
than asserting the guard exists, and `test_the_local_dev_store_is_permitted` is the control
without which a guard that refused everything would pass every other test here.
"""

from __future__ import annotations

import pytest

from sanskrit_texts import dsn_guard

LOCAL = "postgresql+psycopg://corpus_owner:pw@127.0.0.1:5433/sanskrit_texts"


@pytest.mark.parametrize("dsn,why", [
    ("postgresql+psycopg://u:p@db.example.com:5433/sanskrit_texts", "remote hostname"),
    ("postgresql+psycopg://u:p@10.0.0.7:5433/sanskrit_texts", "remote IP"),
    ("postgresql+psycopg://u:p@127.0.0.1:5432/sanskrit_texts", "wrong port — 5432 is AuroraV3"),
    ("postgresql+psycopg://u:p@localhost:6543/sanskrit_texts", "pooler port"),
])
def test_a_non_local_store_is_refused(dsn: str, why: str) -> None:
    with pytest.raises(RuntimeError) as e:
        dsn_guard.assert_local_store(dsn, "drop every table in")
    # The message must say what was about to happen, not merely that something was refused
    # (rule:discernment-checks §2 — absence, and refusal, must be attributable).
    assert "drop every table in" in str(e.value), f"refusal for {why} does not name the action"


def test_the_local_dev_store_is_permitted() -> None:
    """The control. A guard that refused everything would satisfy every test above."""
    dsn_guard.assert_local_store(LOCAL, "drop every table in")


def test_the_cli_refuses_a_remote_store_without_asking_anything() -> None:
    """Exit 2 on a remote DSN — before any prompt, so it cannot be confirmed past."""
    rc = dsn_guard._main(["--dsn", "postgresql+psycopg://u:p@db.example.com:5433/corpus"])
    assert rc == 2


def test_the_cli_refuses_local_when_nobody_can_confirm(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Local is necessary and NOT sufficient: the dev corpus is local, and losing it is the hazard.

    With stdin not a terminal (CI, a pipe, a hook) there is nobody to ask, so the answer is
    no rather than yes-by-default.
    """
    monkeypatch.delenv("CORPUS_ALLOW_DESTROY", raising=False)
    monkeypatch.setattr("sys.stdin.isatty", lambda: False)
    assert dsn_guard._main(["--dsn", LOCAL]) == 2


def test_the_explicit_override_is_honoured(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CORPUS_ALLOW_DESTROY", "1")
    assert dsn_guard._main(["--dsn", LOCAL]) == 0


def test_the_override_does_NOT_rescue_a_remote_store(monkeypatch: pytest.MonkeyPatch) -> None:
    """The override says "I mean it", not "skip the locality check".

    Otherwise one environment variable set once in a shell profile would disarm the whole
    guard for every future invocation, which is the shape G59's first fix got wrong.
    """
    monkeypatch.setenv("CORPUS_ALLOW_DESTROY", "1")
    rc = dsn_guard._main(["--dsn", "postgresql+psycopg://u:p@db.example.com:5433/corpus"])
    assert rc == 2
