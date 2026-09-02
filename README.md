# Sanskrit Texts Repository

An open-source corpus of classical Sanskrit texts, digitized and structured for programmatic
access. One JSON file per text, on a single uniform schema, consumed by
[AstroAcharya](https://github.com/Rupali59/astroacharya)'s from-canon compute.

**Maintained by:** Tathya Dev

---

## What is here

```
Veda/              Saṃhitā layer — the five primary Saṃhitās
Upanishad/         Upaniṣad layer, filed under its Veda
Upaveda/           Āyurveda · Dhanurveda · Sthāpatyaveda
Vedanga-Jyotisha/  Oldest Jyotiṣa stratum (Lagadha) — Rigveda + Yajurveda recensions
Hora/              Natal astrology — Parashari · Nadi · Prashna · Jaimini
Siddhanta/         Mathematical astronomy
Samhita/           Encyclopedic / mundane astrology
Muhurta/           Electional astrology
Dharmashastra/     Codes of conduct, and the Nibandha festival-determination digests
docs/              INVENTORY.md (the registry) · SOURCES.md · CANONICAL_COUNTS.md · …
```

The top level carries **two classification systems**: `Veda/` and `Upanishad/` are the Vedic
*layer* scheme, while `Hora/`, `Siddhanta/`, `Samhita/` and `Muhurta/` are the four Jyotiṣa
*skandhas*. `Samhita` means different things in each — see [`CLAUDE.md`](./CLAUDE.md) §Layout.

**Scope:** Jyotiṣa, plus everything that is not Tantra, Mantra, Brāhmaṇa, Āraṇyaka, Śikṣā or
Kalpa — those belong to Youvan Prakashan. See the workspace `CLAUDE.md` §"Content / texts
ownership" for the split and why it is drawn by *layer*, not by containing work.

---

## What the corpus holds

**[`docs/INVENTORY.md`](./docs/INVENTORY.md) is the registry** — every text's `text_id`, path,
chapter and shloka counts, translation state and count-authority tier. It is the one place
holdings are stated; this file deliberately does not repeat them, because the per-text list
that used to live here described the tree as it was in July 2026 for six weeks after it
stopped being true.

Derive the totals rather than trusting any prose:

```sh
python3 -c "import json,glob;print(sum(len(c['shlokas']) for p in glob.glob('**/*.json',recursive=True) if not p.startswith('docs/') for c in (json.load(open(p)).get('chapters') or [])))"
```

The Jyotiṣa texts are fully translated; the Vedic and Upaveda texts are held untranslated.
Per-text state is in the registry.

---

## JSON schema

One schema, no exceptions — `text_id`, `title_sa`, `title_en`, `category`, and a `chapters[]`
array of `shlokas[]`. It is specified once, in [`CLAUDE.md`](./CLAUDE.md) §"Uniform JSON
schema", together with the fields that must **not** come back (`source`, `header`, `book`,
`english_meaning`, `hindi_meaning`).

Machine-drafted translations live in `english_draft` / `hindi_draft` and are **never** served:
AstroAcharya's seeder copies an allowlist of fields, so a draft cannot reach the public
surface. Verification promotes a draft into `english` / `hindi`.

---

## Sources

Source files are **not in this repository**. They live beside it in
`../sanskrit-texts-sources/`, mirroring the same tree — Wikisource `.wikitext`, SARIT `.xml`,
`.html`, transcriptions, OCR `.txt` and scans. `.gitignore` enforces the separation: this repo
is the translation layer, `.json` and nothing else.

[`docs/SOURCES.md`](./docs/SOURCES.md) records provenance;
[`docs/LICENSES.md`](./docs/LICENSES.md) records each upstream's terms and what we owe it.
**Sanskrit Documents is not open-licensed** — read [`docs/LICENSES.md`](./docs/LICENSES.md)
before redistributing.

Upstreams, in preference order and with the reason for each:
[`REFERENCES.md`](./REFERENCES.md).

- GRETIL — https://gretil.sub.uni-goettingen.de/
- Sanskrit Wikisource — the answer for most of the Vedic corpus
- SARIT — https://sarit.indology.info/
- Sanskrit Documents — https://sanskritdocuments.org/sanskrit/jyotisha/
- Internet Archive — https://archive.org/
- WisdomLib — https://www.wisdomlib.org/
