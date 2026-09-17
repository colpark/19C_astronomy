#!/usr/bin/env python3
"""Protocol secs 1-5: census of 2026 classification reports from T1 captures; P per month splits (a), (b), (c)."""
import json, gzip, re, pathlib, collections, hashlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from tns_parse_w3 import parse, decompress_all, marker, program
D = pathlib.Path(__file__).resolve().parent.parent
assert hashlib.sha256((D/"census_protocol_FROZEN.md").read_bytes()).hexdigest() == "9fac85524f28b5e3874a0d43a2c089915d20814b7996c18a0c77cc230b3c95fb"
E = json.load(open(D/"sealed/enumeration_E_SEALED.json"))
tierA = {x["name"]: x for x in E["tierA"]}
MONTHS = [f"2026-{m:02d}" for m in range(1, 10)]
log = [json.loads(l) for l in open(D/"out/tns_captures_w3/fetch_log.jsonl")]
last = {}
for r in log: last[r["name"]] = r
status = collections.Counter(r["final"] for r in last.values())
status_by_tier = collections.Counter((r["tier"], r["final"]) for r in last.values())
http_codes = collections.Counter(s for r in log for u, s in r["chain"])
units = {}          # (object, program) -> earliest report
objects_first = {}  # object -> earliest report (any program)
invalid, no_reports, capture_ts = 0, 0, []
per_object = []
for name, r in last.items():
    if r["final"] != "ok": continue
    b = decompress_all(gzip.decompress((D/r["file"]).read_bytes()))
    p = parse(b.decode("utf-8", errors="replace"), name)
    if not p["valid"]: invalid += 1; continue
    capture_ts.append(r["capture_ts"])
    if not p["reports"]: no_reports += 1
    lsst_ids = [re.sub(r"\D", "", x) for x in p["internal_names"] if x.startswith("LSST")]
    for rep in sorted(p["reports"], key=lambda x: x["time"] or ""):
        prog = program(rep); mk = marker(rep["classifier"])
        spec_cell = rep.get("spectra_count_cell")
        spectro = (spec_cell not in (None, "", "0")) or any((s.get("group") == rep.get("group")) and (s.get("obsdate") or "9") <= (rep.get("time") or "") for s in p["spectra"])
        u = dict(object=name, program=prog, time=rep["time"], month=(rep["time"] or "")[:7], classification=rep["classification"],
                 classifier=rep["classifier"], sender=rep["sender"], marker=mk, spectroscopic=bool(spectro), capture=r["capture_ts"],
                 cohort=tierA.get(name, {}).get("cohort"), lsst_internal_ids=lsst_ids, tier=r["tier"])
        units.setdefault((name, prog), u)
        objects_first.setdefault(name, u)
        per_object.append(u)
def month_table(sel):
    c = collections.Counter(u["month"] for u in sel)
    return {m: c.get(m, 0) for m in MONTHS}
U = [u for u in units.values() if u["month"] in MONTHS]
O = [u for u in objects_first.values() if u["month"] in MONTHS]
a_spec = [u for u in U if u["spectroscopic"]]; a_nonspec = [u for u in U if not u["spectroscopic"]]
b_incl = [u for u in a_spec if u["marker"] in (None, "SUSPECT-AUTOMATED")]
b_excl = [u for u in a_spec if u["marker"] is None]
c_all = [u for u in U if u["cohort"]]
c_b_incl = [u for u in c_all if u["spectroscopic"] and u["marker"] in (None, "SUSPECT-AUTOMATED")]
c_b_excl = [u for u in c_all if u["spectroscopic"] and u["marker"] is None]
programs = collections.defaultdict(lambda: {m: 0 for m in MONTHS})
prog_auto = collections.defaultdict(collections.Counter)
for u in a_spec:
    programs[u["program"]][u["month"]] += 1; prog_auto[u["program"]][u["marker"] or "human"] += 1
res = dict(
    protocol_sha256="9fac85524f28b5e3874a0d43a2c089915d20814b7996c18a0c77cc230b3c95fb",
    fetch=dict(objects_in_E=len(E["tierA"]) + len(E["tierB"]), attempted=len(last), status=dict(status), status_by_tier={f"{k[0]}:{k[1]}": v for k, v in status_by_tier.items()},
               http_codes_all_requests={str(k): v for k, v in http_codes.items()}, valid_captures_with_reports=len(capture_ts) - no_reports, captures_without_reports=no_reports, invalid=invalid,
               capture_ts_range=[min(capture_ts), max(capture_ts)] if capture_ts else None),
    units_dedup_object_program=len(U),
    a_all_units_per_month=dict(spectroscopic=month_table(a_spec), non_spectroscopic_or_unknown=month_table(a_nonspec)),
    P_objects_first_classified_per_month=month_table(O),
    b_nonbot_measured_per_month=dict(b_incl_syncatto_as_human=month_table(b_incl), b_excl_syncatto_as_automated=month_table(b_excl)),
    c_cohort_per_month=dict(all=month_table(c_all), b_incl=month_table(c_b_incl), b_excl=month_table(c_b_excl)),
    c_cohort_units=c_all,
    programs_spectroscopic_per_month={k: v for k, v in sorted(programs.items(), key=lambda kv: -sum(kv[1].values()))},
    programs_automation_mix={k: dict(v) for k, v in prog_auto.items()},
    status_note="all counts are LOWER BOUNDS from archived captures (reports after a capture are unseen; objects whose capture 404/403 contribute nothing); no month is exact because T2 has no 2026 month breakdown",
)
json.dump(res, open(D/"out/census_counts.json", "w"), indent=1, default=str)
json.dump(per_object, open(D/"out/census_reports_all.json", "w"), indent=0, default=str)
print(json.dumps({k: v for k, v in res.items() if k not in ("c_cohort_units",)}, indent=1, default=str)[:5000])
