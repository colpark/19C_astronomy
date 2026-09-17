import sys,os,json,glob,shutil
sys.path.insert(0,os.path.dirname(__file__)); from common import *
D=f"{VD}/data_cache"
cats=json.load(open(f"{D}/inv_cats_verdicts.json")); ctrl=json.load(open(f"{D}/inv_cats_control.json"))
gh=json.load(open(f"{D}/inv_ghost_verdicts.json")) if os.path.exists(f"{D}/inv_ghost_verdicts.json") else None
runs=[json.loads(l) for l in open(f"{VD}/invariance_runs.jsonl")]
fetch=json.load(open(f"{D}/alert_fetch_summary.json"))
w3=json.load(open(f"{REPO}/astronomy/wave3/agent4_tool_recount/out/alert_content_summary.json"))["alerts"]
w3h={a["oid"]:a["sources_raw_sha256"] for a in w3}
strip=lambda v:{o:{k:x[k] for k in ("arms","bitwise_equal","max_abs_diff_vs_alone","shape_equal","verdict","hashes")} for o,x in v.items() if isinstance(x,dict)}
def tool_verdict(v):
    vs=[x["verdict"] for x in v.values() if isinstance(x,dict)]
    if not vs: return "UNDEMONSTRATED"
    if "NOT_INVARIANT" in vs: return "NOT_INVARIANT"
    if all(x=="INVARIANT" for x in vs): return "INVARIANT"
    return "INVARIANT_WITHIN_FLOAT_TOL"
out={"charter_rule":"V_CHARTER.md §5 invariance: bitwise = INVARIANT; <=1e-6 abs = INVARIANT_WITHIN_FLOAT_TOL; else NOT_INVARIANT",
 "comparator_controls":json.load(open(f"{D}/inv_controls.json")),
 "alert_content":{"path":"Fink /api/v1/sources r: columns via copied safe_fetch.py (label-stripping)","fetched":[dict(f,matches_wave3_raw_sha256=(f["raw_sha256"]==w3h.get(f["oid"]))) for f in fetch],
                  "retention":"sanitized rows deleted after runs; only hashes kept"},
 "CATS":{"verdict":tool_verdict(cats),"per_alert":strip(cats),"repeat_alone_control":ctrl,
         "reading":"not bitwise invariant: batch composition changes the padded input tensor shape and outputs by <=1.19e-7 (float32 ulp scale); repeated alone runs are bitwise identical, so the difference is composition-induced, not run noise; argmax class unchanged"},
 "GHOST":{"run1_hash_equality_per_alert":{o:{"bitwise_equal":x["bitwise_equal"],"hashes":x["hashes"]} for o,x in gh.items() if isinstance(x,dict)},
          "run1_defect":"run-1 comparator masked NaN-vs-value differences (max(0,nan)=0), so its INVARIANT_WITHIN_FLOAT_TOL labels for 372829 and 373061 are void; only hash equality from run 1 is kept",
          "control2":json.load(open(f"{D}/inv_ghost_control2.json")),"verdict":"INVARIANT_WITHIN_FLOAT_TOL","reading":"alert 849114 bitwise identical alone and in both batches. For 372829 and 373061 a repeat alone run is bitwise identical (no network or run noise), and in batch every output column is equal under NaN-aware comparison (0 differing columns, max diff 0), but the JSON serialisation hash differs. Equal values with a different serialisation imply a type representation change (e.g. pandas int to float upcasting when batch rows are combined); the exact column type change was not captured, because outputs are not retained. Scores are value-identical; the serialised records are not bitwise identical","output_columns":gh.get("_columns")},
 "alert_runs":{"used_by_module_V":sum(r["alert_runs"] for r in runs),"cap":90,"wave3_prior":160,"rule_D_total_after":160+sum(r["alert_runs"] for r in runs)},
 "run_log":"invariance_runs.jsonl"}
json.dump(out,open(f"{VD}/invariance.json","w"),indent=1,default=str)
shutil.rmtree(f"{D}/alerts",ignore_errors=True)
for p in glob.glob(f"{D}/ghost/inv_*"): shutil.rmtree(p,ignore_errors=True)
oplog("invariance.json built; alert content and GHOST per-run outputs deleted (hashes retained)",f"{VD}/invariance.json",f"{VD}/invariance_runs.jsonl")
print(json.dumps({k:out[k]["verdict"] for k in ("CATS","GHOST")}),out["alert_runs"],[f["matches_wave3_raw_sha256"] for f in out["alert_content"]["fetched"]])
print(json.dumps(out["GHOST"]["per_alert"],indent=0)[:3000] if out["GHOST"]["per_alert"] else "")
