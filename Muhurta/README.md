# Muhurta — मुहूर्त (Electional Astrology)

The Muhurta skandha covers the selection of auspicious time for actions — the
choosing of a favourable moment (lagna, tithi, nakshatra, yoga, karana, and the
day-segment windows) for an undertaking. Classically muhurta is treated as a
branch of the Samhita/Hora tradition but is substantial enough, and distinct
enough in subject matter, to stand on its own here.

Muhurta is the textual basis for the AstroAcharya muhurta engine
(`astroacharya/app/masters/hora_acharya/calculations/muhurta/`): Choghadiya, the
30-muhurta enumeration, Durmuhurta weekday tables, Dishaashool, Abhijit/Brahma
windows. As of the audit that created this folder, **none of those windows have a
muhurta-manual source in this corpus** — they cite Muhurta Chintamani /
Dharmasindhu, neither of which is digitized here yet. Only the BPHS upagrahas
(Gulika/Kala/Mrityu/Yamaghantaka/Ardhaprahara, BPHS 3.66–70) are corpus-verifiable.

---

## Texts in this collection

| Folder | Title | Author | Period | Status |
|--------|-------|--------|--------|--------|
| `MuhurtaChintamani` | मुहूर्तचिन्तामणि | Rama Daivajna | 1600 CE | **Not yet digitized** |
| `MuhurtaMartanda` | मुहूर्तमार्तण्ड | Narayana Daivajna | 1571 CE | **Not yet digitized** |

---

## Ingestion note

To match the loader, each text should land as chapter/shloka JSON in the same
shape as the other texts in this corpus:

```json
{
  "text_id": "muhurta_chintamani",
  "title_sa": "मुहूर्तचिन्तामणि",
  "title_en": "Muhurta Chintamani",
  "category": "muhurta",
  "chapters": [
    { "number": 1, "title": "…", "shlokas": [ { "number": 1, "text": "…" } ] }
  ]
}
```

---

## References

- Sanskrit Documents — Jyotisha section: https://sanskritdocuments.org/sanskrit/jyotisha/
- Muhurta Chintamani (with Piyusha-dhara commentary) — Internet Archive / Chowkhamba editions
