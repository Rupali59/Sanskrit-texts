# Wrong-text audit, 2026-10-03

**Served English that does not translate its verse was found in 16 texts (3,237 verses) by reading a sample, and
every verse in a confirmed run was unserved** (moved to `english_draft`/`hindi_draft`, status
`drafted`). A gap is safer than a confident mistranslation reaching AstroAcharya. Re-translation is
the follow-up, one text at a time, draft → review → promote.

## Method, and what it can and cannot see

- **Sample:** 63 texts, ~20 verses each (1,200 total), stratified by chapter, seed `20261003`.
  Each sampled verse read Sanskrit beside English and judged OK / PARTIAL / WRONG-TEXT / FILLER.
- **Bounding:** every WRONG-TEXT or FILLER hit was followed outward verse by verse until the
  English re-aligned. Run bounds below are read, not inferred — except where marked.
- **Verified by a second route:** 13 verses drawn from the six largest runs were re-read
  independently; all 13 confirmed wrong.
- **Blind spot:** a text that sampled clean is clean *in the sample*. ~20 verses cannot rule out a
  short run elsewhere. Only reading finds this class (G73); no detector has calibrated.

## Unserved (the runs)

Derive the current state, never trust these counts: the commit that applied them names the spec,
and `python3 scripts/check_inventory.py` gives each text's translated %.

| text | runs unserved | verses |
|---|---|---:|
| phaladeepika **(re-translated 2026-10-04, d58bc59)** | 1.1–3, 2.8–21, 3.2–6, 3.8–20, ch 4–5, 6.10–end, 7.2–end, 8.3–13.25, 14.10–20.62, 21.2–10, 22.1–6, 22.8–9, 23.1–10, 24.1–5, 24.34–35, 25.1–5, 25.18–29 | 565 |
| manu_smriti | 1.79–84, 1.107–119, 2.63–248, 3.16–end, 7.87, 7.207–209 | 480 |
| panchasiddhantika | ch 1 (duplicates ch 2), 4.12–end, ch 5–18 whole (ch 18 filler is interleaved, so taken whole) | 336 |
| jataka_parijata | 4.26–105, 6.16–101, 12.81–149 | 236 |
| grahaganita | 8.4–end, 9.6–end (9.25–99 interleaved filler, taken whole) | 154 |
| garga_hora | 2.5–59, 2.63–end | 139 |
| varahamihir_daivagnavallabh | 12.2–15.43 (end of text) | 99 |
| chandogya_upanishad | 2.9.2–8, 2.11.1–2.13.2, 4.17.2–9, 5.1.13–15, 5.3.3–5.4.2, 5.8.2–5.9.2, 5.10.7–5.24.4 | 71 |
| brihadaranyaka_upanishad | 6.1.8–6.5.4 (end) | 68 |
| brihat_samhita | 87 whole, 88.1–12 | 59 |
| susruta_samhita | 3.7.4–3.8.2, 4.37.82–84, 5.4.35–5.5.1, 1.45.133–146 | 51 |
| nirnayasindhu | all 32 served units (page summaries, not translations) | 32 |
| narada_smriti | 2.12.99–2.13.9 | 28 |
| jaiminiya_upadesa_sutra | 4.1.22–39 (each English renders the next sūtra) | 18 |
| kaushitaki_upanishad | 1.2–7 (shifted), 3 whole (summaries) | 15 |
| jataka_tattva | every verse of ch 2–10 read: 2.1–2, 2.51–61, 3.56–346 (five aligned 5-verse islands kept), 4.6–25, 5.6–20, 6.6–144 in five blocks, 7.6–219 in six blocks, 8.6–20, 8.26–38, 9.6–98, 10.6–157 in five blocks, 16.6–7. The invention runs on a fixed cycle — aligned islands at regular intervals, a generator's signature. 10.91–148 is a SHIFT (each English is the verse 9 later), so the Sanskrit of 10.91–99 has no English at all: re-align, don't just re-translate. Ch 1, 11–15, 17 sampled 1 in 4, clean | 886 |

**Over-inclusion is deliberate.** Where filler interleaves with real translation (grahaganita ch 9,
panchasiddhantika ch 18) the whole stretch was taken: a correct verse moved to drafts costs one
re-review; a wrong verse left served keeps reaching AstroAcharya.

## Not unserved — partial or boundary defects, English is incomplete rather than wrong

- **taittiriya_upanishad:** systemic. Sanskrit verses are cut mid-anuvāka, English follows whole
  passages, so each verse carries the previous tail and drops its own; the kośa descriptions
  (prāṇamaya…ānandamaya) and the Bhṛgu "पुनरेव वरुणं… स तपोऽतप्यत" refrain are untranslated.
  Needs re-segmentation of the English, not unserving.
- **lilavati** ~1.177–1.212 summary band (right topic, compressed).
- **astanga_sangraha** 1.3 weak, 3.91–3.97 filler/shift, 5.Paribh.89 meaning reversed.
- **aitareya** 4.1–4.3, **kena** 3.1/3.2 boundary; **paingala** 1.1, 1.2, 2.1 condensed;
  **kaushitaki** 4.18/4.19 truncated; **brihadaranyaka** 2.6.2–3, 4.6.2–3 lineages condensed.
- **brihat_samhita:** a "house"→"Bhava" find-replace damaged 139 verses across 35 chapters — a
  word-level fix, not an unserve.
- Isolated: bijaganita 1.166 filler, 1.186 (58 → 62); brahmasphuta 2.6 numerals; mahanarayana 50.1;
  surya_siddhanta 2.17; sarvasara 1.1; maitri 8.34 summary; susruta 6.39.194 "without boiling";
  one dropped half-verse each in astanga_hridaya 6.8.6, bhrigu_sutram 5.7, subala 1.11,
  brihat_jataka 1.17, sarvartha, goladhyaya; jaiminiya 4.4.10 adds a clause; jataka_parijata 6.8.
- **Sanskrit, not English:** maitri ch 7 duplicates ch 8.1–8; jaiminiya 1.3.13, 3.4.15, 3.4.23,
  4.3.69 OCR unreadable.

## Clean in the sample

rigveda, samaveda, atharvaveda, shukla_yajurveda, taittiriya_samhita, saravali, dhanurveda,
muhurta_chintamani, atmabodha, caraka, laghu_jatakam, apastamba, kaivalya, katha, isha, mandukya,
mundaka, prashna, shvetashvatara, jabala, arch_jyotisham, yajusha_jyotisham, minaraja,
jaimini_sutra, aryabhatiya, shatpanchashika, mayamata, manasara, uttara_kalamrita.
