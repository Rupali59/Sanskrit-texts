# The corpus database

A modelled Postgres store for the corpus, with a **structural publication gate**: unreviewed
text is not filtered out at read time, it is absent from what a consumer can reach.

`make setup` then `make hello`. Everything below explains why it is shaped this way.

## Getting started

```sh
make setup     # deps, the container on 5433, the schema, and the test database
make hello     # one small text, dry run, nothing written
make import    # the whole corpus
make test
```

`make help` lists the rest. **Derive every number below rather than trusting it** —
`make hello` and `scripts/check_inventory.py` are the authorities, and a count in a document
rots faster than anything else in it.

## The two DSNs, and why there are two

```
CORPUS_OWNER_DSN   migrations and the importer. The application must NEVER hold this.
CORPUS_API_DSN     the consumer. SELECT on the published views, nothing else.
```

A table **owner can re-grant past any REVOKE** and is not subject to RLS unless it is FORCEd,
so a gate built on GRANT is worth nothing if the application connects as owner. `compose`
creates only the owner; the migration creates `corpus_api` and grants it SELECT on two views.
`corpus_owner` is additionally a **superuser** (compose makes `POSTGRES_USER` one), which is
the sharpest form of the same point: the gate is the *view definition plus the grant*, and it
protects consumers, never the owner.

Copy `.env.example` to `.env`. Nothing in it is a deployment credential — the database binds
`127.0.0.1:5433` and holds a public-domain corpus.

## Schema

```
category ──< text ──< section ──< verse ──< annotation ──< annotation_revision
              │        │ (self-FK,          │ kind: translation | tag        (append-only,
              │        │  ragged tree)      │ state: the lifecycle below      enforced by a
              │        └─ depth/level_name  │ position: array order           trigger)
              ├──< text_facet               │ source_field: which JSON key
              └── part_of (self-FK)         └─ lang
```

**`verse.number_label` is the literal printed label; `verse.position` is an integer used only
for ordering.** Nothing ever parses a label to sort. Eleven label shapes occur, including half
shlokas (`27 1/2`), Devanagari suffixes (`12अ`), hyphen sub-numbers (`1.12-3`) and digit
strings that look like ints and are not.

**`section` is a ragged tree.** `structure.levels` declares the MAXIMUM depth, not a uniform
one: Caraka's Cikitsāsthāna subdivides adhyāyas 1–2 into pādas and leaves the other 28 alone,
so a label with fewer components means that branch is not subdivided. A check that assumed
uniform depth accused ~20% of the corpus before the check turned out to be wrong.

**`text_facet` is the directory's middle level** — `(bphs, school, Parashari)`. Five kinds;
52 of 66 texts carry one. The 14 that do not are the four Siddhānta Śiromaṇi parts (joined by
`text.part_of` instead) and 10 genuinely standalone works.

Two columns exist purely so the export can reproduce the source and are easy to mistake for
noise: **`verse.number_is_str`** (32 labels are digit strings typed `str`, and 4 texts mix
both types, so it cannot live on `text`) and **`annotation.source_field`** (a served value and
its draft both land as `state='draft'` with identical `(kind, lang)`, so nothing else tells
them apart).

**`text.status`** (migration `0002`) is the third. 28 of 66 files carry a text-level `status`
and the rest do not, so NULL means "no such key" and the exporter needs the column to know
which files to emit it for. It is a summary of the verses, and on the day it landed it was
false on 17 texts — stamped `translated` over Manusmṛti's 0 of 2,684. Its definition is
`reader.derive_text_status`, and `tests/test_reader.py` fails naming any text whose stored
value disagrees with its verses. **The importer stores it as the file has it and never
corrects it**: an importer that fixed data would hide exactly the disagreement the test exists
to report.

## The editorial lifecycle

```
draft ──> in_review ──> approved
  ^            │            │
  └── needs_revision        └──> superseded
```

**Everything imports as `draft`. Nothing is `approved`, because nothing has a named reviewer.**
An earlier design mapped the corpus's `status` field onto publication state — that would have
written 55,942 rows asserting a review nobody performed, derived from a field the corpus uses
as an **arrival date**. Measured: 69,813 verses carry both translations while `status` reads
`untranslated`. It was withdrawn before it ran; `verse.status` keeps the arrival fact and
makes no claim about review.

`published_verse` joins annotations on `state='approved'`, so a draft is **absent from the
view**, not filtered out of it.

## Promoting

```sh
python -m sanskrit_texts.promote --to approved --text bphs --author "Vipin Kaushik" \
    --kind translation --lang en --dry-run
```

`approved` **requires `--author`** and `--method human`; a matcher may propose, never approve.
Every promotion writes an `annotation_revision` naming the human and the method, and that
table is append-only in the database — a `BEFORE UPDATE OR DELETE` trigger raises — so the
record cannot be tidied away.

**This path exists deliberately, rather than forbidding bulk promotion.** Withholding
already-curated content with no sanctioned route to publish it is what creates the pressure
toward a bulk `UPDATE … SET state='approved'` that nothing can distinguish from legitimate
use. An audited bulk path is the defense.

Approving a verse that holds two candidates (a served value and its draft) is **refused, not
resolved** — the partial unique index permits one approved value per `(verse, kind, lang)`,
and choosing between them is a review decision, not something a flag should make.

## Export

```sh
python -m sanskrit_texts.export --mode fidelity --all --out /tmp/rt   # the cutover gate
python -m sanskrit_texts.export --mode citable  --all --out dist/     # the dataset release
```

**One `--mode`, no default.** `fidelity` carries everything including drafts and exists to
prove the import lost nothing; `citable` carries approved annotations only. They cannot both
be one artifact: the committed corpus contains thousands of draft values, so "reproduces the
corpus" and "contains no draft bytes" are contradictory requirements.

After cutover the exporter WRITES the tracked JSON, so its serialization is a contract:
`json.dumps(doc, ensure_ascii=False, indent=2) + "\n"`, insertion key order, never
`sort_keys`. `sanskrit_texts.export.serialize` is the single definition.

## What is deliberately excluded

`sanskrit_texts/exclusions.py` names four texts the importer skips, with the reason inline.
Three contain no genuine digitised text. `check_inventory.py` deliberately does not read that
list — its drift row is the standing record that they are here and unresolved.

## Known and tracked

- **70 verses** violate `uq_verse_label_in_section` — the duplicates the Mongo seeder drops
  silently today. The importer names every one and **refuses to commit** unless
  `--allow-partial` says the loss is accepted. Data to fix, never a constraint to relax.
- **Unicode normalisation is undecided.** 4 texts are not NFC. The importer normalises
  nothing, so the round trip is sound either way — but a byte-level assertion cannot be added
  until that decision lands.
- The gate suite **skips itself** without a database, which reads as a pass. `CORPUS_REQUIRE_DB=1`
  turns that into a failure; CI must set it.
