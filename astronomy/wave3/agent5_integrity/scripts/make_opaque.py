#!/usr/bin/env python3
"""Implements OPAQUE_ID_RULE.md. Never prints polarity. Run from agent5_integrity/."""
import csv, hashlib, io, json, os, random, sys
sys.path.insert(0, os.path.dirname(__file__))
from idcheck import checks
R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
BRIEF = os.path.join(R, "astronomy/wave3/PANEL_BRIEF_WAVE3.md")
B = hashlib.sha256(open(BRIEF, "rb").read()).hexdigest()
assert B == open(os.path.join(R, "astronomy/wave3/BRIEF_SHA256")).read().split()[0], "brief hash mismatch"
PERM = int(hashlib.sha256(f"{B}:permtest".encode()).hexdigest(), 16)
SUITES = [("fm-advantage-benchmark", "fm-advantage-benchmark/cases/cases.csv"),
          ("astronomy_replay", "astronomy/replay/cases/cases.csv")]
W2_POL = {"fm-advantage-benchmark": "d0f89b30a42678f53dd122d642708659f1174de86c4f1cfb58779287988a853d",
          "astronomy_replay": "ff84a2407103db595ecde1cae6c36f989941f2925a43d20b7b1cc618e28af35f"}
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
issued, log = set(), {"brief_sha256": B, "rule_file_sha256": sha("OPAQUE_ID_RULE.md"), "suites": {}}
for suite, rel in SUITES:
    src = os.path.join(R, rel); raw = open(src, "rb").read()
    cases = list(csv.DictReader(io.StringIO(raw.decode("utf-8"), newline="")))
    cb = {c["case_id"]: c for c in cases}; oi = {c["case_id"]: i for i, c in enumerate(cases)}
    n = len(cases); attempts = []
    for t in range(20):
        seed = int(hashlib.sha256(f"{B}:{suite}:{t}".encode()).hexdigest(), 16)
        rng = random.Random(seed); order = rng.sample(range(n), n); ids = {}; local = set()
        for i in order:
            while True:
                x = f"{rng.getrandbits(40):010x}"
                if x not in issued and x not in local: break
            local.add(x); ids[x] = cases[i]["case_id"]
        out = sorted(ids)
        res = checks(out, cb, ids, oi, suite, PERM)
        ps = [v for k, v in res.items() if k.startswith("p_")]
        ok = min(ps) >= 0.05 and not res["ids_are_row_counters"] and not res["first_char_groups_all_single_polarity"]
        attempts.append({"attempt": t, "seed_derivation": f'int(sha256("{B}:{suite}:{t}").hexdigest(),16)', "checks": res, "accepted": ok})
        if ok: break
    else:
        raise SystemExit(f"{suite}: no attempt passed; stop and report")
    issued |= set(ids)
    d = f"suites/{suite}"; os.makedirs(d, exist_ok=True)
    with open(f"{d}/cases_opaque.csv", "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n"); w.writerow(["opaque_id", "stage", "sealed", "input"])
        for o in out: c = cb[ids[o]]; w.writerow([o, c["stage"], c["sealed"], c["input"]])
    with open(f"holder_handover/id_map_{suite}.csv", "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n"); w.writerow(["opaque_id", "case_id"])
        for o in out: w.writerow([o, ids[o]])
    pol = "case_id,polarity\n" + "".join(f"{c['case_id']},{c['polarity']}\n" for c in cases)
    open(f"holder_handover/polarity_{suite}.csv", "w", newline="").write(pol)
    if suite == "astronomy_replay":
        with open("evaluator/blind_inputs_opaque.csv", "w", newline="") as fh:
            w = csv.writer(fh, lineterminator="\n"); w.writerow(["opaque_id", "stage", "input"])
            for o in out: c = cb[ids[o]]; w.writerow([o, c["stage"], c["input"]])
    log["suites"][suite] = {"source": rel, "source_sha256": sha(src), "rows": n, "attempts": attempts,
        "cases_opaque": f"{d}/cases_opaque.csv", "cases_opaque_sha256": sha(f"{d}/cases_opaque.csv"),
        "id_map": f"holder_handover/id_map_{suite}.csv", "id_map_sha256": sha(f"holder_handover/id_map_{suite}.csv"),
        "polarity_file": f"holder_handover/polarity_{suite}.csv", "polarity_sha256": sha(f"holder_handover/polarity_{suite}.csv"),
        "polarity_sha256_matches_wave2_canonical": sha(f"holder_handover/polarity_{suite}.csv") == W2_POL[suite]}
    if suite == "astronomy_replay":
        log["suites"][suite]["evaluator_file"] = "evaluator/blind_inputs_opaque.csv"
        log["suites"][suite]["evaluator_file_sha256"] = sha("evaluator/blind_inputs_opaque.csv")
open("logs/generation.json", "w").write(json.dumps(log, indent=1) + "\n")
print(json.dumps(log, indent=1))
