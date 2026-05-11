# Sanskrit Texts Repository

An open-source collection of classical Sanskrit texts, digitized and structured for programmatic access. Organized by the canonical branches of the Jyotish tradition and related shastra.

**Maintained by:** Tathya Dev / Youvan Prakashan

---

## Structure

```
texts/
├── Vedanga-Jyotisha/    Oldest stratum — Vedic ritual astronomy (Lagadha)
│   ├── Rigveda/         Archa/Rik recension — 36 verses        [digitized]
│   ├── Yajurveda/       Yajusha recension — 43 verses          [digitized]
│   ├── Samaveda/        Lost — no extant manuscript
│   └── Atharvaveda/     Lost — no extant manuscript
│
├── Hora/                Natal astrology — birth chart interpretation
│   ├── BrihatParasharaHoraShastra/    [digitized — chapters split]
│   ├── BrihatJataka/                  [digitized]
│   ├── Laghujatakam/                  [digitized]
│   ├── Bhrigusootram/                 [digitized]
│   ├── Jatakaparijatah/               [digitized]
│   ├── MinarajaYavanajataka/          [digitized]
│   ├── Phaladeepika/                  [digitized]
│   ├── Shatpanchashika/               [digitized]
│   ├── Chamatkarchintamani/           [digitized]
│   ├── VarahamihirDaivagnavallabh/    [digitized]
│   ├── Saravali/                      [reference — not yet digitized]
│   ├── SarvarthaChintamani/           [reference — not yet digitized]
│   ├── UttaraKalamrita/               [reference — not yet digitized]
│   ├── PrashnaMarga/                  [reference — not yet digitized]
│   └── JatakaTattvam/                 [reference — not yet digitized]
│
├── Samhita/             Encyclopedic / mundane astrology
│   ├── BrihatSamhita/                 [digitized — raw]
│   └── GargaSamhita/                  [reference — not yet digitized]
│
├── Siddhanta/           Mathematical astronomy
│   ├── SuryaSiddhanta/                [reference — not yet digitized]
│   ├── Aryabhatiya/                   [reference — not yet digitized]
│   ├── BrahmasphutaSiddhanta/         [reference — not yet digitized]
│   ├── SiddhantaShiromani/            [reference — not yet digitized]
│   └── Panchasiddhantika/             [reference — not yet digitized]
│
├── Tantra/              Related esoteric traditions
│   ├── Shivasvarodayah/               [digitized]
│   ├── KularnavaTantra/               [reference — not yet digitized]
│   ├── TripuraRahasya/                [reference — not yet digitized]
│   └── VijnanaBhairavaTantra/         [reference — not yet digitized]
│
└── SamudrikShastra/     Palmistry and body reading — in progress
    ├── SamudrikaTilaka/               [reference — not yet digitized]
    └── Hastamuktavali/                [reference — not yet digitized]
```

Each branch has a `README.md` with canonical text list, authors, periods, and digitization status. Placeholder folders contain a README with source references for acquisition.

---

## JSON Schema

Digitized texts follow one of two schemas:

**Schema A** (most texts):
```json
{
  "source": "filename.md",
  "header": "Sanskrit title",
  "chapters": [
    {
      "number": 1,
      "title": "chapter title",
      "shlokas": [
        { "number": 1, "text": "...", "english_meaning": "...", "hindi_meaning": "..." }
      ]
    }
  ]
}
```

**Schema B** (Phaladeepika-style):
```json
{ "book": "TextName", "chapters": [ ... ] }
```

**BPHS** is split by chapter range: `BPHS0110.json` = chapters 1–10, `BPHS1120.json` = chapters 11–20, etc.

Some texts have a `chapters/` subdirectory with one JSON per chapter.

---

## External sources

- GRETIL: https://gretil.sub.uni-goettingen.de/
- Sanskrit Documents: https://sanskritdocuments.org/sanskrit/jyotisha/
- Internet Archive: https://archive.org/search?query=jyotish+sanskrit
- WisdomLib: https://www.wisdomlib.org/
- BORI Manuscripts (Pune): http://bori.ac.in/
