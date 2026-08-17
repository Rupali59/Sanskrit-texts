# Corpus inventory — sanskrit-texts wiki

> **GENERATED** by `scripts/gen_inventory.py` — do not hand-edit. Run `python scripts/gen_inventory.py` after adding a text, then commit.

From-canon Sanskrit shloka stores. Each text is chunked into per-chapter JSON under `chapters/`. This is the **producer**; astroacharya's from-canon compute is the **consumer** — see [`../.propagates.yml`](../.propagates.yml) and [propagation flow](#state-based-propagation-flow).

**Totals:** 23 texts · 240 chapter files · 7 live categories.

## Hora — Horā — horoscopy (jātaka, praśna, nāḍī)

| Text | School | Chapters | Docs | Source held |
|------|--------|---------:|------|-------------|
| [`Bhrigusootram`](../Hora/Nadi/Bhrigusootram) | Nadi | 8 | — | — |
| [`BrihatJataka`](../Hora/Parashari/BrihatJataka) | Parashari | 28 | — | — |
| [`BrihatParasharaHoraShastra`](../Hora/Parashari/BrihatParasharaHoraShastra) | Parashari | 11 | — | — |
| [`Chamatkarchintamani`](../Hora/Parashari/Chamatkarchintamani) | Parashari | 10 | — | — |
| [`Jatakaparijatah`](../Hora/Parashari/Jatakaparijatah) | Parashari | 18 | — | — |
| [`Laghujatakam`](../Hora/Parashari/Laghujatakam) | Parashari | 16 | — | — |
| [`MinarajaYavanajataka`](../Hora/Parashari/MinarajaYavanajataka) | Parashari | 74 | — | — |
| [`Phaladeepika`](../Hora/Parashari/Phaladeepika) | Parashari | 1 | — | — |
| [`Saravali`](../Hora/Parashari/Saravali) | Parashari | 1 | [README](../Hora/Parashari/Saravali/README.md) | pdf |
| [`Shatpanchashika`](../Hora/Parashari/Shatpanchashika) | Parashari | 1 | — | — |
| [`UttaraKalamrita`](../Hora/Parashari/UttaraKalamrita) | Parashari | 1 | [README](../Hora/Parashari/UttaraKalamrita/README.md) | txt |
| [`VarahamihirDaivagnavallabh`](../Hora/Parashari/VarahamihirDaivagnavallabh) | Parashari | 1 | — | — |

## Siddhanta — Siddhānta — mathematical astronomy

| Text | School | Chapters | Docs | Source held |
|------|--------|---------:|------|-------------|
| [`Aryabhatiya`](../Siddhanta/Aryabhatiya) | — | 4 | [README](../Siddhanta/Aryabhatiya/README.md) | — |
| [`Panchasiddhantika`](../Siddhanta/Panchasiddhantika) | — | 18 | [README](../Siddhanta/Panchasiddhantika/README.md) | — |
| [`SuryaSiddhanta`](../Siddhanta/SuryaSiddhanta) | — | 14 | [README](../Siddhanta/SuryaSiddhanta/README.md) | — |

## Muhurta — Muhūrta — electional timing

| Text | School | Chapters | Docs | Source held |
|------|--------|---------:|------|-------------|
| [`MuhurtaChintamani`](../Muhurta/MuhurtaChintamani) | — | 15 | [README](../Muhurta/MuhurtaChintamani/README.md) | — |

## Samhita — Saṃhitā — mundane / omens

| Text | School | Chapters | Docs | Source held |
|------|--------|---------:|------|-------------|
| [`BrihatSamhita`](../Samhita/BrihatSamhita) | — | 2 | — | — |

## Dharmashastra — Dharmaśāstra — ritual law / calendar

| Text | School | Chapters | Docs | Source held |
|------|--------|---------:|------|-------------|
| [`ApastambaDharmaSutra`](../Dharmashastra/ApastambaDharmaSutra) | — | 1 | — | — |
| [`ApastambaParibhashaSutra`](../Dharmashastra/ApastambaParibhashaSutra) | — | 1 | — | — |
| [`ManuSmriti`](../Dharmashastra/ManuSmriti) | — | 12 | [README](../Dharmashastra/ManuSmriti/README.md) | txt |

## Vedanga-Jyotisha — Vedāṅga Jyotiṣa — the earliest calendar canon

| Text | School | Chapters | Docs | Source held |
|------|--------|---------:|------|-------------|
| [`Aarchjyotisham`](../Vedanga-Jyotisha/Rigveda/Aarchjyotisham) | Rigveda | 1 | — | — |
| [`Yajushajyotisham`](../Vedanga-Jyotisha/Yajurveda/Yajushajyotisham) | Yajurveda | 1 | — | — |

## Kalpa — Kalpa — ritual sūtra (gṛhya)

| Text | School | Chapters | Docs | Source held |
|------|--------|---------:|------|-------------|
| [`Asvalayana`](../Kalpa/Grhyasutra/Asvalayana) | Grhyasutra | 1 | — | — |

## State-based propagation flow

The corpus is upstream of astroacharya's from-canon primitives (each cites `@source(("<Text>", chapter, [shlokas]))`, per `MASTER_DECISIONS D17`). Adding or renaming a text can change what the compute can cite.

```
add / re-chunk a text  →  python scripts/gen_inventory.py  →  INVENTORY.md changes
                                                              ↓ (commit)
        propagation watcher (.propagates.yml)  →  drift row against astroacharya
                                                   reference.md / DATA_GAPS.md
```
Edges are declared in [`../.propagates.yml`](../.propagates.yml). Source scans (PDF / raw OCR `.txt`) are kept **local, not committed** — the canonical data is the per-chapter JSON.

