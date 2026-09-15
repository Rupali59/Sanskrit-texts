#!/usr/bin/env python3
"""
The embedding arms of docs/RETRIEVAL_EVAL.md, run against a LOCAL model.

WHY LOCAL, AND WHY IT IS NOT MERELY CHEAPER. docs/EMBEDDING_EVAL.md's protocol says:
"Pin the model version — the floor is not reproducible against a drifting model." A hosted
model can be updated underneath you and silently move the floor; a local weights file
cannot. Local satisfies a requirement the protocol already states, and incidentally costs
nothing and needs no key.

It also reopens an arm the 2026-09-14 run closed on availability grounds. That run recorded
"no major embedding model declares Sanskrit", so it embedded ENGLISH only. A multilingual
local model (bge-m3 and similar) embeds Devanagari directly — and the corpus is 83%
untranslated, so an arm that reads the Sanskrit is worth more than another English one.

WHAT THIS DOES NOT DO. It does NOT re-test BPHS's recorded -12.9%. That figure was measured
with text-embedding-3-large @3072, and the value of re-running it is that the Devanagari
never changed while the English did — a one-variable test. Swapping the model changes two
variables and answers nothing. That re-test still wants the paid API and is worth ~$0.10.

THREE ARMS, added beside the `tags` and `$text` already scored in retrieval_eval.py:

  embed-en    cosine over embedded ENGLISH — comparable in kind to the recorded run
  embed-sa    cosine over embedded DEVANAGARI — only possible with a multilingual model
  hybrid      tag filter FIRST, then embedding rank within the survivors

The hybrid is the one the plan predicts wins, and the prediction is specific: a tag query
matches a median of 332 verses, so the ranker faces ~332 candidates instead of 3,937. The
recorded AUC of 0.870 was measured on the harder, unfiltered problem.

CACHE lives OUTSIDE the repo by default (~/.cache/sanskrit-texts/). This repo's .gitignore
deliberately keeps it to JSON plus docs/; a vector cache is neither.

Exit codes (rule:discernment-checks §2):
  0  ran, scored
  2  could not run — ollama unreachable, model absent, corpus or eval doc missing
"""

import argparse
import json
import math
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import retrieval_eval as RE  # noqa: E402  — pairs, scoring, and the validated harness

OLLAMA = "http://127.0.0.1:11434"
CACHE = Path.home() / ".cache" / "sanskrit-texts"


def embed(texts, model, batch=64):
    """Embed via the local ollama server. Returns a list of vectors, or None on failure."""
    out = []
    for i in range(0, len(texts), batch):
        chunk = [t if t.strip() else " " for t in texts[i:i + batch]]
        body = json.dumps({"model": model, "input": chunk}).encode()
        req = urllib.request.Request(f"{OLLAMA}/api/embed", data=body,
                                     headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                d = json.loads(r.read())
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            print(f"could not run: ollama unreachable at {OLLAMA} ({e})", file=sys.stderr)
            return None
        if "embeddings" not in d:
            print(f"could not run: {str(d)[:160]}", file=sys.stderr)
            return None
        out.extend(d["embeddings"])
        print(f"\r  embedding {min(i+batch, len(texts)):>5}/{len(texts)}", end="", file=sys.stderr)
    print(file=sys.stderr)
    return out


def unit(v):
    n = math.sqrt(sum(x * x for x in v))
    return [x / n for x in v] if n else v


def cosine(a, b):
    return sum(x * y for x, y in zip(a, b))


def load_or_build(model, field, verses, refresh=False):
    """{ref: unit-vector} for one field, cached on disk keyed by model+field."""
    CACHE.mkdir(parents=True, exist_ok=True)
    f = CACHE / f"bphs.{model.replace(':', '_').replace('/', '_')}.{field}.json"
    if f.exists() and not refresh:
        return {k: v for k, v in json.loads(f.read_text()).items()}
    refs = [r for r, _ in verses]
    texts = [(s.get(field) or "") for _, s in verses]
    vecs = embed(texts, model)
    if vecs is None:
        return None
    got = {r: unit(v) for r, v in zip(refs, vecs)}
    f.write_text(json.dumps(got))
    print(f"  cached -> {f}", file=sys.stderr)
    return got


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--model", default="bge-m3", help="an ollama EMBEDDING model")
    ap.add_argument("--refresh", action="store_true", help="rebuild the cache")
    ap.add_argument("--sa", action="store_true", help="also run the Devanagari arm")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    pairs = RE.parse_pairs(RE.DOC)
    if pairs is None:
        return 2
    try:
        doc = json.loads(RE.BPHS.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        print(f"could not run: {e}", file=sys.stderr)
        return 2
    verses = [(f"{c['number']}.{s['number']}", s)
              for c in doc["chapters"] for s in c["shlokas"]]

    en = load_or_build(args.model, "english", verses, args.refresh)
    if en is None:
        return 2
    sa = load_or_build(args.model, "text", verses, args.refresh) if args.sa else None

    qv = embed([p["q"] for p in pairs], args.model)
    if qv is None:
        return 2
    qvec = {p["n"]: unit(v) for p, v in zip(pairs, qv)}

    def rank_embed(space):
        def arm(v, p):
            q = qvec[p["n"]]
            return [r for _, r in sorted(((-cosine(q, space[r]), r) for r, _ in v))]
        return arm

    def rank_hybrid(space):
        """Tag filter FIRST, then embedding rank inside the survivors. Falls back to the
        full space when the bridge yields no tags — an empty filter must not mean an empty
        answer, which would be a silent zero rather than an attributable one."""
        def arm(v, p):
            keep = RE.rank_tags(v, RE.tags_for(p["q"]))
            pool = keep if keep else [r for r, _ in v]
            q = qvec[p["n"]]
            return [r for _, r in sorted(((-cosine(q, space[r]), r) for r in pool))]
        return arm

    arms = {"embed-en": rank_embed(en), "hybrid": rank_hybrid(en)}
    if sa:
        arms["embed-sa"] = rank_embed(sa)

    n = len(pairs)
    traps = sum(1 for p in pairs if not p["gold"])
    print(f"  model: {args.model} · {n} pairs, {n-traps} scorable, {traps} trap")
    print()
    print(f"  {'arm':<10}{'hit@1':>7}{'hit@5':>7}{'miss':>7}{'false-pos':>11}")
    print("  " + "-" * 42)
    for name in ("tags", "$text"):
        fn = (lambda v, p: RE.rank_tags(v, RE.tags_for(p["q"]))) if name == "tags" \
            else (lambda v, p: RE.rank_text(v, p["q"]))
        r = RE.score(pairs, verses, fn)
        print(f"  {name:<10}{r['at1']:>7}{r['at5']:>7}{r['miss']:>7}{r['fp']:>11}")
    res = {}
    for name, fn in arms.items():
        r = RE.score(pairs, verses, fn)
        res[name] = r
        print(f"  {name:<10}{r['at1']:>7}{r['at5']:>7}{r['miss']:>7}{r['fp']:>11}")
    print("  " + "-" * 42)

    # The harness must prove it can fire, exactly as the lexical and embedding arms did.
    oracle = RE.score(pairs, verses, lambda v, p: RE.rank_text(
        v, (dict(v)[p["gold"][0]].get("english") or "")) if p["gold"] else [])
    neg = RE.score(pairs, verses, lambda v, p: RE.rank_text(v, "quick brown fox lazy dog"))
    print(f"  harness: oracle {oracle['at1']}/{n-traps} hit@1 · "
          f"negative control {neg['at5']}/{n-traps} hit@5")

    if args.verbose:
        for name, r in res.items():
            print(f"\n  --- {name}")
            for num, v, top in r["rows"]:
                p = next(x for x in pairs if x["n"] == num)
                print(f"    {num:>3} {v:<18}{top:<9}{p['q'][:52]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
