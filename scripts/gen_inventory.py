#!/usr/bin/env python3
"""Generate docs/INVENTORY.md — the corpus wiki catalog.

Walks the shloka-store tree and emits a grouped, linked inventory of every text.
GENERATED FILE — do not hand-edit docs/INVENTORY.md; run:

    python scripts/gen_inventory.py

The corpus is the PRODUCER; astroacharya's from-canon compute is the CONSUMER
(see .propagates.yml). Regenerate + commit whenever inventory changes, so the
propagation watcher flags downstream canon that may need reconciling.
"""
from __future__ import annotations
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
CATEGORIES = [
    ("Hora", "Horā — horoscopy (jātaka, praśna, nāḍī)"),
    ("Siddhanta", "Siddhānta — mathematical astronomy"),
    ("Muhurta", "Muhūrta — electional timing"),
    ("Samhita", "Saṃhitā — mundane / omens"),
    ("Dharmashastra", "Dharmaśāstra — ritual law / calendar"),
    ("Vedanga-Jyotisha", "Vedāṅga Jyotiṣa — the earliest calendar canon"),
    ("Kalpa", "Kalpa — ritual sūtra (gṛhya)"),
]
SKIP = {".git", "node_modules", "docs", "scripts", ".claude", ".kiro"}


def find_texts(cat: str):
    """A text = a dir holding .json shloka stores, either directly (BPHS,
    BrihatSamhita, Vedanga) or under a chapters/ subdir (most texts)."""
    catdir = ROOT / cat
    if not catdir.is_dir():
        return []
    # Resolve each json file to its text dir (parent, or parent-of-chapters/).
    tdirs = {}
    for jf in catdir.rglob("*.json"):
        tdir = jf.parent.parent if jf.parent.name == "chapters" else jf.parent
        tdirs.setdefault(tdir, None)
    texts = []
    for tdir in tdirs:
        chdir = tdir / "chapters"
        if chdir.is_dir() and any(chdir.glob("*.json")):
            n = len(list(chdir.glob("*.json")))
        else:
            n = len(list(tdir.glob("*.json")))
        rel = tdir.relative_to(ROOT)
        parts = rel.parts  # ("Hora","Parashari","BrihatJataka")
        school = "/".join(parts[1:-1]) or "—"
        readme = (tdir / "README.md").exists()
        sources = sorted({
            p.suffix.lstrip(".").lower()
            for p in tdir.glob("*")
            if p.suffix.lower() in (".pdf", ".txt")
        })
        texts.append({
            "name": parts[-1], "rel": rel.as_posix(), "school": school,
            "chapters": n, "readme": readme, "sources": sources,
        })
    return sorted(texts, key=lambda t: (t["school"], t["name"]))


def main():
    rows_by_cat, n_texts, n_ch = {}, 0, 0
    for cat, _ in CATEGORIES:
        texts = find_texts(cat)
        rows_by_cat[cat] = texts
        n_texts += len(texts)
        n_ch += sum(t["chapters"] for t in texts)

    out = []
    out.append("# Corpus inventory — sanskrit-texts wiki\n")
    out.append("> **GENERATED** by `scripts/gen_inventory.py` — do not hand-edit. "
               "Run `python scripts/gen_inventory.py` after adding a text, then commit.\n")
    out.append("From-canon Sanskrit shloka stores. Each text is chunked into per-chapter "
               "JSON under `chapters/`. This is the **producer**; astroacharya's from-canon "
               "compute is the **consumer** — see [`../.propagates.yml`](../.propagates.yml) "
               "and [propagation flow](#state-based-propagation-flow).\n")
    out.append(f"**Totals:** {n_texts} texts · {n_ch} chapter files · "
               f"{sum(1 for c in rows_by_cat if rows_by_cat[c])} live categories.\n")

    for cat, label in CATEGORIES:
        texts = rows_by_cat[cat]
        out.append(f"## {cat} — {label}\n")
        if not texts:
            out.append("_(no ingested texts yet)_\n")
            continue
        out.append("| Text | School | Chapters | Docs | Source held |")
        out.append("|------|--------|---------:|------|-------------|")
        for t in texts:
            rd = f"[README](../{t['rel']}/README.md)" if t["readme"] else "—"
            src = ", ".join(t["sources"]) if t["sources"] else "—"
            out.append(f"| [`{t['name']}`](../{t['rel']}) | {t['school']} | "
                       f"{t['chapters']} | {rd} | {src} |")
        out.append("")

    out.append("## State-based propagation flow\n")
    out.append("The corpus is upstream of astroacharya's from-canon primitives "
               "(each cites `@source((\"<Text>\", chapter, [shlokas]))`, per "
               "`MASTER_DECISIONS D17`). Adding or renaming a text can change what the "
               "compute can cite.\n")
    out.append("```")
    out.append("add / re-chunk a text  →  python scripts/gen_inventory.py  →  INVENTORY.md changes")
    out.append("                                                              ↓ (commit)")
    out.append("        propagation watcher (.propagates.yml)  →  drift row against astroacharya")
    out.append("                                                   reference.md / DATA_GAPS.md")
    out.append("```")
    out.append("Edges are declared in [`../.propagates.yml`](../.propagates.yml). Source scans "
               "(PDF / raw OCR `.txt`) are kept **local, not committed** — the canonical data is "
               "the per-chapter JSON.\n")

    (ROOT / "docs" / "INVENTORY.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"wrote docs/INVENTORY.md — {n_texts} texts, {n_ch} chapters")


if __name__ == "__main__":
    main()
