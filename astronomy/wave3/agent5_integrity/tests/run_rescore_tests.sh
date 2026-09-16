#!/usr/bin/env bash
# Dummy-verdict tests for scripts/rescore.py. Run from agent5_integrity/. Writes holder_handover/rescore_test_out/.
set -u
# Test artifacts go under the gitignored holder_handover/: wave1_as_opaque.json is a polarity key
# for the opaque ids (wave 1 scored 20 of 20) and tampered_map.csv carries id-map rows.
T=holder_handover/rescore_test_out; rm -rf $T; mkdir -p $T
python3 - <<'PY'
import csv, json, hashlib
ids = [r["opaque_id"] for r in csv.DictReader(open("evaluator/blind_inputs_opaque.csv"))]
h = lambda s: hashlib.sha256(s.encode()).digest()
json.dump({i: {"fired": h(i)[0] % 2 == 0, "ruling": "dummy", "via": "validator" if h(i)[1] % 5 == 0 else "stage"} for i in ids},
          open("holder_handover/rescore_test_out/dummy_opaque.json", "w"), indent=1)
inv = {r["case_id"]: r["opaque_id"] for r in csv.DictReader(open("holder_handover/id_map_astronomy_replay.csv"))}
w1 = json.load(open("../../replay/evaluator/verdicts.json"))
json.dump({inv[k]: v for k, v in w1.items()}, open("holder_handover/rescore_test_out/wave1_as_opaque.json", "w"), indent=1)
m = {inv[k]: v for k, v in w1.items()}; m.pop(sorted(m)[0]); json.dump(m, open("holder_handover/rescore_test_out/missing_one.json", "w"), indent=1)
json.dump(w1, open("holder_handover/rescore_test_out/original_ids.json", "w"), indent=1)
d = json.load(open("holder_handover/rescore_test_out/dummy_opaque.json")); d["ffffffffff"] = {"fired": True, "via": "stage"}; json.dump(d, open("holder_handover/rescore_test_out/unknown_id.json", "w"))
d = json.load(open("holder_handover/rescore_test_out/dummy_opaque.json")); k = sorted(d)[0]; d[k]["fired"] = "yes"; json.dump(d, open("holder_handover/rescore_test_out/malformed.json", "w"))
rows = open("holder_handover/id_map_astronomy_replay.csv").read().splitlines(); a, b = rows[1].split(","), rows[2].split(",")
rows[1], rows[2] = f"{a[0]},{b[1]}", f"{b[0]},{a[1]}"; open("holder_handover/rescore_test_out/tampered_map.csv", "w").write("\n".join(rows) + "\n")
PY
run() { name=$1; shift; echo "### $name"; echo "\$ python3 scripts/rescore.py $*"; python3 scripts/rescore.py "$@" 2>&1 | sed "s#$(pwd)/##g"; echo "[exit=${PIPESTATUS[0]}]"; echo; }
run "T1 dummy verdicts (fired from sha256(opaque_id), no polarity used): must score, tallies sum to 14 and 6" --verdicts $T/dummy_opaque.json --outdir $T/t1
run "T2 wave-1 verdicts re-keyed to opaque ids: must reproduce 20 of 20, 2 unearned, delta 0" --verdicts $T/wave1_as_opaque.json --outdir $T/t2
run "T3 one verdict missing: must report 19 of 20 and 1 missing, not crash" --verdicts $T/missing_one.json --outdir $T/t3
run "T4 verdicts keyed by original case ids: must refuse (exit 2)" --verdicts $T/original_ids.json
run "T5 unknown opaque id: must refuse (exit 2)" --verdicts $T/unknown_id.json
run "T6 malformed fired value: must refuse (exit 2)" --verdicts $T/malformed.json
run "T7 tampered id map (two rows swapped): must refuse on hash (exit 2)" --verdicts $T/dummy_opaque.json --map $T/tampered_map.csv
echo "### T8 stdout never carries per-case polarity lines"
echo "\$ grep -cE '(must_fire|must_not_fire) +(ok|FAIL)' tests/rescore_tests.log (stdout of T1-T7)"
