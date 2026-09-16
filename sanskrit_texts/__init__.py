"""Typed model and Postgres store for the classical Sanskrit text corpus.

WHY THIS PACKAGE EXISTS. Before it, 28 Python files in this repo opened the corpus
independently — 15 of them calling `json.load` directly, four hardcoding the same BPHS
path, six re-implementing the same `chapters[] -> shlokas[]` loop. Nothing anywhere
declared what a shloka *is*: astroacharya's `texts_repo` functions are typed
`-> list[dict]`, and the only real schema was 16 runtime checks across 458 lines of
`astroacharya/scripts/validate_corpus.py`, which validate files and never the database.

THE PROBLEM THIS SOLVES IS NOT "NO ORM". It is that the function loading JSON into
MongoDB accidentally holds the editorial policy. `seed_texts.py`'s `_normalize_shloka`
copies 12 named keys and drops the rest, and that allowlist is the only thing keeping
draft translations off the public API (G50). A data-loading function is enforcing a
publishing rule, from another repository. So the job is separating **what the corpus
possesses from what it publishes** — which is why this package has two model layers:

    models.py   SQLAlchemy 2.0 declarative — what is STORED
    schema.py   Pydantic v2 — what LEAVES the building

They are deliberately different classes. SQLModel was rejected for exactly the property
that makes it attractive: it makes them one class, and one class is how a storage
concern became a publication policy in the first place.

WHAT IS DECLARED DATA, NOT CODE. Verse numbering is a per-text property and it lives in
each text's `structure` block (`levels`, `shloka_number_format`), never in this package.
The importer READS those declarations and never infers: the corpus holds 11 distinct
label shapes across depths 2-4, verse numbers are `int` on 45 texts and `str` on 17 with
4 texts mixing both, and no global rule round-trips. A parser competing with its own data
loses. Derive the current picture rather than trusting this docstring:

    python3 scripts/check_inventory.py

THREE THINGS NOT TO REINTRODUCE, each of which this corpus has already paid for:
  G8   ingest dedupe on (chapter, shloka) drops verses without erroring. Here the key is
       a UNIQUE constraint, so a collision fails the import instead of losing 70 verses.
  G12  a matching TOTAL over mislabelled records proves nothing. Reconcile field by field.
  G50  the publication gate is an allowlist, and an allowlist fails CLOSED. Never widen it
       to make a field "just show up"; add it deliberately, with a test.
"""

__all__ = ["__version__"]

__version__ = "0.1.0"
