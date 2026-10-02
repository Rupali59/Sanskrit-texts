# Handover 4 to Antigravity — translate 959 verses, verified against online sources (2026-10-02)

**Run every command from the repo root:**
`cd "$HOME/Documents/GitHub/Vipin Kaushik/sanskrit-texts"`.

**Read the rules first.** They are §"The rules" and §"Before handing back" of
[`2026-10-02-antigravity-handover.md`](./2026-10-02-antigravity-handover.md), plus the rules specific
to `bphs` in [`2026-10-02-antigravity-handover-3.md`](./2026-10-02-antigravity-handover-3.md). Both
still apply. This file replaces handover 3's worklist.

## Why this handover exists: handover 3 did not produce translations

Of the 890 `bphs` drafts handover 3 returned, **852 were one of six template labels** with the
chapter and verse number slotted in:

> *"In Chapter 72 verse 11 of Ashtakavarga: The verse defines the precise bindu counts, reduction
> rules (Trikona/Ekadhipatya shodhana), or multipliers for planetary strength."*

That is not a translation. It describes no verse, and the topic was often wrong too: chapter 87 is
a remedy for births on Kṛṣṇa Caturdaśī, and it was labelled "ancestral curses". Five more were
wrong translations: 4.15 carried another verse's meaning, 7.18 and 7.19 misassigned the vimśopaka
values, 27.9 added the Sun to a rule about the Moon, Mars and Saturn, and 27.15 read सुराः (33) as
50. Thirty-three were good, and they are kept. All 857 others were reset to their earlier drafts.

**A label is worse than leaving a verse blank.** It reads like a summary and passes every
uniqueness check, because the numbers make each string different. Leave a verse blank if you
cannot translate it, and say so in your report.

## The task

Translate every verse on the worklist: English into `english_draft`, Hindi into `hindi_draft`.
The old draft in those fields is **wrong**; replace it and do not reuse it. Translate from the
verse's own `text`.

Derive the worklist — do not trust the count above:

```sh
python3 - <<'PY'
import json, pathlib, sys
TEXTS = {
    "bphs": "Hora/Parashari/BrihatParasharaHoraShastra/BrihatParasharaHoraShastra.json",
    "chamatkar_chintamani": "Hora/Parashari/Chamatkarchintamani/Chamatkarchintamani.json",
}
# Reviewed and good, or model-written and awaiting review: NOT yours to touch.
SKIP = {("bphs", 7, "17"), ("bphs", 36, "1"), ("bphs", 36, "4"), ("bphs", 39, "41")}
SKIP |= {("bphs", 15, str(n)) for n in range(5, 15)} | {("bphs", 16, str(n)) for n in range(1, 21)}
rows = []
for tid, path in TEXTS.items():
    d = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
    for c in d["chapters"]:
        for s in c["shlokas"]:
            k = (tid, c["number"], str(s["number"]))
            if k in SKIP:
                continue
            if not (s.get("english") or "").strip() and (s.get("english_draft") or "").strip():
                rows.append(k)
if len(rows) < 900:
    sys.exit(f"only {len(rows)} verses found -- the scan has gone blind, it has not found nothing")
for tid, ch, n in rows:
    print(f"{tid}\t{ch}\t{n}")
print(f"{len(rows)} verses", file=sys.stderr)
PY
```

Expected today: **959** (894 `bphs`, 65 `chamatkar_chintamani`).

## Verify every verse against online sources

Before writing each translation, check it against at least one published source online, and record
which one you used.

- **The Sanskrit.** Compare our `text` with an online edition, e.g. sanskritdocuments.org
  (Jyotiṣa section) or archive.org scans of the printed editions. If the online reading differs
  from ours in a way that changes the meaning, **do not edit `text`**. List the verse with both
  readings in your report.
- **The meaning.** Check your reading against a published English or Hindi translation of the
  same verse; for BPHS, for example, the Santhanam or G. C. Sharma translation. Use it to catch a
  misread number, planet or house. **Do not copy its wording**: those translations are under
  copyright, and ours must be your own translation of our `text`.
- **If no source can be found for a verse**, translate it anyway, and mark it `no source found` in
  the report.
- **If our verse numbering doesn't match the source's**, match on content, never on number. That
  is rule 1 of the first handover, and it matters most here.

Your report must list, per text, the sources you used, and every verse where the source disagreed
with our Sanskrit or with your first reading.

## Self-check — must pass before you hand back

Run this after writing. It must print `OK`. If it fails, fix the verses it names, do not edit the
check.

```sh
python3 - <<'PY'
import json, pathlib, re, sys, collections
TEXTS = {
    "bphs": "Hora/Parashari/BrihatParasharaHoraShastra/BrihatParasharaHoraShastra.json",
    "chamatkar_chintamani": "Hora/Parashari/Chamatkarchintamani/Chamatkarchintamani.json",
}
LABEL = re.compile(r"\b(in chapter \d|verse \d+\s*:|chapter \d+ verse|describes the (specific )?(fruits|results)|"
                   r"maharshi parashara (describes|declares)|principles of|this verse (defines|describes))", re.I)
# Planet names are blanked too: chamatkar_chintamani's defect was one sentence with the planet swapped.
PLANET = re.compile(r"\b(Sun|Moon|Mars|Mercury|Jupiter|Venus|Saturn|Rahu|Ketu|Surya|Chandra|Mangala|"
                    r"Kuja|Budha|Guru|Shukra|Shani)\b", re.I)
SKIP = {("bphs", 7, "17"), ("bphs", 36, "1"), ("bphs", 36, "4"), ("bphs", 39, "41")}
SKIP |= {("bphs", 15, str(n)) for n in range(5, 15)} | {("bphs", 16, str(n)) for n in range(1, 21)}
bad, skel, n = [], collections.defaultdict(list), 0
for tid, path in TEXTS.items():
    d = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
    for c in d["chapters"]:
        for s in c["shlokas"]:
            en, hi = s.get("english_draft") or "", s.get("hindi_draft") or ""
            if (tid, c["number"], str(s["number"])) in SKIP:
                continue
            if (s.get("english") or "").strip() or not en.strip():
                continue
            n += 1
            k = f"{tid} {c['number']}.{s['number']}"
            if LABEL.search(en):
                bad.append(f"{k}: label, not a translation")
            if not re.search("[ऀ-ॿ]", hi):
                bad.append(f"{k}: hindi_draft has no Devanagari")
            skel[PLANET.sub("P", re.sub(r"[0-9]+", "N", en))].append(k)
if n < 900:
    sys.exit(f"only {n} drafts scanned -- the check has gone blind")
for e, ks in skel.items():
    if len(ks) > 1:
        bad.append(f"{len(ks)} drafts share one wording with only numbers or planets changed: {ks[:5]}")
print("\n".join(bad) if bad else "OK", f"({n} drafts scanned)")
sys.exit(1 if bad else 0)
PY
```

If two verses' **Sanskrit** genuinely differs only in a planet or a number (some daśā and
aṣṭakavarga verses are formulaic), identical English is correct. Leave it, and list the pair in
your report with both Sanskrit lines quoted. Never reword a translation just to make the check pass.

Passing the self-check is necessary, not sufficient: it catches labels, not wrong translations.
The verses are read against their Sanskrit before anything is promoted.

## Specific to `chamatkar_chintamani`

Each verse states the results of one planet in one house, numbered 1–12 within the planet's
chapter (5 Mercury, 6 Jupiter, 7 Venus, 8 Saturn, 9 Rahu, 10 Ketu). The old drafts were copies of
other planets' verses with the name swapped. **Never take wording from another verse of this
text**: the Sun, Moon and Mars chapters are served and correct, and copying them is the defect
being repaired. The text is in Bhujaṅgaprayāta and often rhetorical ("what use is X if…"); keep
the rhetorical form rather than flattening it into a list.

Promotion is not yours to do. Write drafts, run the self-check, and hand back with the report.
