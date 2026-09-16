#!/usr/bin/env python3
"""Re-score the wave-1 astronomy replay from verdicts keyed by opaque_id.

Steps, in order:
 1. hash the verdict file and print the hash before anything is joined;
 2. verify the id map, the vendored replay.py and the astronomy cases.csv against pinned sha256;
 3. validate verdict keys (all opaque, none unknown; missing ones are passed through as NO VERDICT);
 4. translate opaque_id -> case_id through the local map;
 5. build a temporary layout <tmp>/scripts/replay.py + <tmp>/cases/cases.csv (RULINGS_SEALED.csv is
    copied only with --with-rulings, i.e. by the holder) and call the UNCHANGED replay.py score
    for the development, sealed and all sets;
 6. parse the tallies and report polarity accuracy, unearned (validator-only) count, and the delta
    against wave 1 (20 of 20 polarity, 2 unearned: astronomy/replay/RESULT.md).

Full replay.py output (per-case lines include polarity) is written to --outdir, never to stdout.

usage: rescore.py --verdicts V.json [--map M.csv] [--outdir DIR] [--with-rulings]
exit: 0 scored; 2 input/integrity error
"""
import argparse, csv, hashlib, json, os, re, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
PIN = {
    "map": ("astronomy/wave3/agent5_integrity/holder_handover/id_map_astronomy_replay.csv",
            "be5cb3142a0bc9fcce481fd0b913e5d6e4c27b4c6b5d3cf6c5eacd040d943971"),
    "replay": ("fm-advantage-benchmark/scripts/replay.py",
               "d63459c3b9b377480f0fdba7f612a1f156b94eec121d41259303cc23f14b0ce6"),
    "cases": ("astronomy/replay/cases/cases.csv",
              "60782b6b097dd505ed7242c7fb84b7c16323f4204c7d6fb6c4615954c4b6ca74"),
    "rulings": ("astronomy/replay/cases/RULINGS_SEALED.csv",
                "6041714a30b9143ef6ea74edd3ed35dca86c51317d42a56d2b5204f559f2e2fc"),
}
WAVE1 = {"polarity_ok": 20, "n": 20, "must_fire_ok": 14, "must_fire_n": 14,
         "must_not_fire_ok": 6, "must_not_fire_n": 6, "unearned": 2,
         "source": "astronomy/replay/RESULT.md; astronomy/replay/evaluator/score_all.txt"}
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()

def die(msg):
    print(f"ERROR: {msg}", file=sys.stderr); sys.exit(2)

def pinned(key, override=None):
    rel, want = PIN[key]
    p = override or os.path.join(ROOT, rel)
    got = sha(p)
    if got != want: die(f"{key} sha256 {got} != pinned {want} ({p})")
    return p

def parse(out):
    r = {}
    for pol in ("must_fire", "must_not_fire"):
        m = re.search(rf"^{pol}\s+(\d+) of (\d+)(?:, (\d+) undemonstrated)?", out, re.M)
        r[pol] = {"ok": int(m.group(1)), "n": int(m.group(2)), "undemonstrated": int(m.group(3) or 0)} if m else {"ok": 0, "n": 0, "undemonstrated": 0}
    m = re.search(r"^validator-only (\d+):", out, re.M)
    r["unearned"] = int(m.group(1)) if m else 0
    return r

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--verdicts", required=True)
    ap.add_argument("--map")
    ap.add_argument("--outdir", default=None)
    ap.add_argument("--with-rulings", action="store_true", help="holder only: annotate failures from RULINGS_SEALED.csv")
    a = ap.parse_args()

    vhash = sha(a.verdicts)
    print(f"verdict file sha256 {vhash}  ({a.verdicts})  recorded before join")
    mp = pinned("map", a.map); rp = pinned("replay"); cp = pinned("cases")
    idmap = {r["opaque_id"]: r["case_id"] for r in csv.DictReader(open(mp, newline=""))}
    try:
        v = json.load(open(a.verdicts))
    except Exception as e:
        die(f"verdict file is not JSON: {e}")
    if not isinstance(v, dict): die("verdict file must be an object keyed by opaque_id")
    orig_ids = set(idmap.values())
    leaked = sorted(k for k in v if k in orig_ids)
    if leaked: die(f"{len(leaked)} verdict key(s) are original case ids, not opaque ids; the evaluator saw non-blind ids")
    unknown = sorted(k for k in v if k not in idmap)
    if unknown: die(f"{len(unknown)} verdict key(s) not in the id map: {unknown[:5]}")
    bad = sorted(k for k, x in v.items() if not isinstance(x, dict) or not isinstance(x.get("fired"), bool) or x.get("via") not in ("stage", "validator"))
    if bad: die(f"{len(bad)} verdict(s) malformed (need fired: bool and via: stage|validator): {bad[:5]}")
    missing = sorted(set(idmap) - set(v))
    translated = {idmap[k]: x for k, x in v.items()}

    tmp = tempfile.mkdtemp(prefix="rescore_")
    try:
        os.makedirs(os.path.join(tmp, "scripts")); os.makedirs(os.path.join(tmp, "cases"))
        shutil.copyfile(rp, os.path.join(tmp, "scripts", "replay.py"))
        shutil.copyfile(cp, os.path.join(tmp, "cases", "cases.csv"))
        if a.with_rulings:
            shutil.copyfile(pinned("rulings"), os.path.join(tmp, "cases", "RULINGS_SEALED.csv"))
        vt = os.path.join(tmp, "verdicts_translated.json")
        open(vt, "w").write(json.dumps(translated, indent=1, sort_keys=True) + "\n")
        results, outputs = {}, {}
        for s in ("development", "sealed", "all"):
            p = subprocess.run([sys.executable, os.path.join(tmp, "scripts", "replay.py"), "score", "--verdicts", vt, "--set", s],
                               capture_output=True, text=True)
            if "no cases match" in p.stdout + p.stderr: die(f"replay.py found no cases for set {s}")
            outputs[s] = p.stdout; results[s] = parse(p.stdout); results[s]["replay_exit"] = p.returncode
        translated_hash = sha(vt)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    al = results["all"]
    n = al["must_fire"]["n"] + al["must_not_fire"]["n"]
    ok = al["must_fire"]["ok"] + al["must_not_fire"]["ok"]
    summary = {
        "verdict_file": a.verdicts, "verdict_sha256": vhash, "translated_verdicts_sha256": translated_hash,
        "id_map_sha256": sha(mp), "replay_py_sha256": sha(rp), "cases_sha256": sha(cp),
        "rulings_used": a.with_rulings, "verdicts_received": len(v), "missing_verdicts": len(missing),
        "sets": results,
        "polarity_accuracy": {"ok": ok, "n": n, "rate": round(ok / n, 4) if n else None},
        "unearned": al["unearned"],
        "wave1_baseline": WAVE1,
        "delta_vs_wave1": {"polarity_ok": ok - WAVE1["polarity_ok"],
                           "must_fire_ok": al["must_fire"]["ok"] - WAVE1["must_fire_ok"],
                           "must_not_fire_ok": al["must_not_fire"]["ok"] - WAVE1["must_not_fire_ok"],
                           "unearned": al["unearned"] - WAVE1["unearned"]},
        "reading": ("The delta is the measured issue-09 inflation only if the evaluator differs from wave 1 in nothing "
                    "but the ids; a fresh evaluator is a new sample, so the delta also carries run-to-run variance."),
    }
    if a.outdir:
        os.makedirs(a.outdir, exist_ok=True)
        for s, o in outputs.items(): open(os.path.join(a.outdir, f"score_{s}.txt"), "w").write(o)
        open(os.path.join(a.outdir, "rescore_summary.json"), "w").write(json.dumps(summary, indent=1) + "\n")
    print(f"polarity accuracy {ok} of {n}  (must_fire {al['must_fire']['ok']} of {al['must_fire']['n']}, "
          f"must_not_fire {al['must_not_fire']['ok']} of {al['must_not_fire']['n']}, missing {len(missing)})")
    print(f"unearned (validator-only) {al['unearned']}")
    d = summary["delta_vs_wave1"]
    print(f"delta vs wave 1 (20 of 20, 2 unearned): polarity {d['polarity_ok']:+d}, unearned {d['unearned']:+d}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
