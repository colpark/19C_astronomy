"""Build tool_coverage_axis.json from run_log.jsonl (protocol section 8). Dispositions are derived mechanically:
UNDEMONSTRATED = PRECHECK record or no successful LOAD; PASS = >=1 valid alert run with status ok; FAIL otherwise.
Valid alert runs = alert runs after the tool's last successful LOAD (earlier runs under a failed or superseded load are
reported, not counted; GHOST runs voided by AM2 are excluded)."""
import collections, datetime, hashlib, json, pathlib

D = pathlib.Path(__file__).resolve().parent.parent
W1 = pathlib.Path("/home/aid1/Documents/4_19C_astronomy/repo/astronomy/agent4_tools_instrument")
BAND_HASH_TIME = "2026-09-16T18:51:26.922781Z"
PROTOCOL_FREEZE = "2026-09-16T20:52:25.088956Z"
runs = [json.loads(l) for l in open(D / "run_log.jsonl")]
inv = json.load(open(W1 / "tool_inventory_slot.json"))["value"]["tools"]
FM = {t["id"]: bool(t["fm_channel"]) for t in inv}
REMAP = {"ATAT": ["Fink_EarlySNIa_RF", "Fink_SLSN_RF"], "Astromer1": ["Fink_EarlySNIa_RF", "Fink_SLSN_RF"],
         "Astromer2": ["Fink_EarlySNIa_RF", "Fink_SLSN_RF"]}
COUNTERPART = {t["id"]: REMAP.get(t["id"], t["counterparts"]) for t in inv}
VOIDED = {("GHOST", "2026-09-16T21:04:18.552158Z"), ("GHOST", "2026-09-16T21:06:12.640199Z")}
STAGE_OVERRIDE = {  # disclosed: generic stage mapper labelled these 'infer'; traceback places the failure in the tool's input parsing
    "RAPID": ("parse", "Classify._do_error_checks: assert len(light_curve) == 10 (input validator)"),
    "Astromer1": ("parse", "ASTROMER load_numpy tf.data generator TypeError on the v11_1 row array (input pipeline)"),
    "Astromer2": ("parse", "src.data.loaders.load_numpy generator TypeError, expects float (None,3) (input pipeline)"),
    "SuperNNova": ("parse", "supernnova classify_lcs feature assembly KeyError ['MWEBV']: model cli_args require MWEBV, wrapper supplies none"),
}
TOOLS = [t["id"] for t in inv]
per = []
for tool in TOOLS:
    rs = [r for r in runs if r["tool"] == tool]
    pre = [r for r in rs if r["alert_id"] == "PRECHECK"]
    loads = [r for r in rs if r["alert_id"] == "LOAD"]
    ok_loads = [r for r in loads if r["status"] == "ok"]
    entry = {"tool": tool, "group": "FM/deep" if FM[tool] else "classical", "rubin_counterparts_after_remap": COUNTERPART[tool],
             "remapped": tool in REMAP, "n_log_lines": len(rs)}
    if pre:
        entry.update(disposition="UNDEMONSTRATED", reason=pre[-1]["error"], alerts_run=0, passes=0)
    elif not ok_loads:
        entry.update(disposition="UNDEMONSTRATED", reason="could not be loaded: " + (loads[-1]["error"] if loads else "no load record"),
                     alerts_run=0, passes=0)
    else:
        t_load = ok_loads[-1]["start_utc"]
        valid = [r for r in rs if r["alert_id"] not in ("LOAD", "PRECHECK") and r["start_utc"] > t_load and (tool, r["start_utc"]) not in VOIDED]
        superseded = [r for r in rs if r["alert_id"] not in ("LOAD", "PRECHECK") and r not in valid]
        passes = sum(1 for r in valid if r["status"] == "ok")
        entry.update(alerts_run=len(valid), passes=passes, superseded_or_voided_runs=len(superseded),
                     failed_load_attempts=[r["error"] for r in loads if r["status"] != "ok"])
        if passes:
            entry.update(disposition="PASS", pass_count=f"{passes}/{len(valid)}")
        else:
            stages = collections.Counter(r["status"] for r in valid)
            st, detail = STAGE_OVERRIDE.get(tool, (None, None))
            if st is None:
                s0 = stages.most_common(1)[0][0] if stages else "error:unknown"
                st = s0.split(":", 1)[1].split("(")[0]
            entry.update(disposition="FAIL", stage=st, logged_statuses=dict(stages),
                         error=next((r["error"] for r in valid if r.get("error")), "code default output on every alert (non-default rule not met)"),
                         stage_reclassified=detail)
    per.append(entry)

cnt = {g: collections.Counter() for g in ("FM/deep", "classical", "all")}
for e in per:
    cnt[e["group"]][e["disposition"]] += 1
    cnt["all"][e["disposition"]] += 1
counts = {g: {k: c.get(k, 0) for k in ("PASS", "FAIL", "UNDEMONSTRATED")} for g, c in cnt.items()}
passed = {e["tool"] for e in per if e["disposition"] == "PASS"}
fm_pass = [e["tool"] for e in per if e["group"] == "FM/deep" and e["disposition"] == "PASS"]
cp_ok = {t: [c for c in COUNTERPART[t] if c in passed] for t in fm_pass}
fm_accepts = [e["tool"] for e in per if e["group"] == "FM/deep" and (e["disposition"] == "PASS" or (e["disposition"] == "FAIL" and e.get("stage") in ("infer", "emit")))]
if fm_pass and all(cp_ok[t] for t in fm_pass):
    band = "PROCEED"
elif not fm_accepts:
    band = "CLOSE"
else:
    band = "ESCALATE"
alert_times = [r["start_utc"] for r in runs]
w1_sha = hashlib.sha256(open(W1 / "tool_coverage_axis.json", "rb").read()).hexdigest()
now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
precond_b = all(t > BAND_HASH_TIME for t in alert_times) and len(per) == 25 and all(e.get("disposition") for e in per)
axis = {
    "id": "axis-tool_coverage-astronomy-rubin-recount-2026-09-16",
    "axis": "tool_coverage",
    "stage": "P3 recount after band hash (wave 3, rule D)",
    "supersedes": {"path": "astronomy/agent4_tools_instrument/tool_coverage_axis.json", "sha256": w1_sha,
                   "note": "wave-1 counts were structural (no tool executed); this recount is functional under the frozen protocol"},
    "recount_timestamps": {"band_hash_utc": BAND_HASH_TIME, "protocol_frozen_utc": PROTOCOL_FREEZE,
                           "first_run_utc": min(alert_times), "last_run_utc": max(r["end_utc"] for r in runs), "record_built_utc": now,
                           "all_runs_after_band_hash": all(t > BAND_HASH_TIME for t in alert_times)},
    "protocol": {"path": "recount_protocol_FROZEN.md", "sha256": hashlib.sha256(open(D / "recount_protocol_FROZEN.md", "rb").read()).hexdigest(),
                 "amendments": ["AM1 dedupe candidate oids (before any fetch or run)", "AM2 GHOST pruned model re-fetched; 2 runs voided"]},
    "alert_sample": {"sealed_ids": "sealed/alert_ids_SEALED_v2.json",
                     "sha256": hashlib.sha256(open(D / "sealed/alert_ids_SEALED_v2.json", "rb").read()).hexdigest(),
                     "n_alerts": 10, "diaSources_per_alert": "1-3", "sky": "all within ~0.9 deg of ra 223.6, dec -40.0"},
    "packet_format_qualifier": "No public endpoint served lsst v11_1 Avro packets (Fink /api/v1/sources output-format=avro -> HTTP 400 'Output format avro is not supported. Choose among json, csv, votable, or parquet'). Every run used public Fink LSST API JSON rows carrying lsst v11_1 field names (r: columns), values unchanged. No tool was run on v11_1 Avro packets.",
    "value": {"counts_by_group_and_disposition": counts, "per_tool": per,
              "fm_deep_passing": fm_pass, "fm_deep_accepting_v11_1_input_past_parse": fm_accepts, "classical_counterparts_passing_for_each_fm_pass": cp_ok,
              "alert_runs_logged": sum(1 for r in runs if r["alert_id"] not in ("LOAD", "PRECHECK")),
              "rule_D_cap": "250 alert runs (25 x 10)"},
    "band_reading": {"band_source": "astronomy/wave2/agent1_rubin_bands/bands_FROZEN.md sha256 8825ef80…00d2 §tool_coverage",
                     "reading": band,
                     "why": "PROCEED needs >=1 FM/deep PASS and >=1 classical counterpart PASS per such channel: CATS passes but both its Rubin counterparts (Fink_EarlySNIa_RF, Fink_SLSN_RF) FAIL at emit on these 1-3-point alerts. CLOSE needs no FM/deep channel to accept v11.1 inputs: CATS accepted them. Hence ESCALATE.",
                     "note": "stated for P4; not ruled here"},
    "p4_precondition_b": {"clears": precond_b,
                          "basis": "every run timestamp is after the band hash (18:51:26Z) and all 25 tools carry a PASS, FAIL or UNDEMONSTRATED disposition; zero or low passes are still a number"},
    "referent": "number of the 25 inventory tools that complete parse, infer and emit with non-default output on at least one of 10 sealed real Rubin cohort alerts, by group and disposition",
    "source": "scripts/build_axis.py over run_log.jsonl (sha256 recorded in order_of_operations.log); runners scripts/run_fink_tools.py and scripts/run_other_tools.py; protocol recount_protocol_FROZEN.md",
    "population": "25 tool channels x up to 10 alerts (10 distinct diaObjectIds first detected at MJD 61222.04-61222.06, sealed before any run); 158 alert runs logged",
    "adjudicator": "classical channels under the same pass criterion on the same 10 alerts; wave-1 structural count (0/25 verified on Rubin) as the superseded value",
    "falsifier": "a rerun of the runners on the sealed ids that changes any disposition, or a public v11_1 Avro endpoint on which a FAIL-at-parse tool's own parser succeeds, would show the count is wrong",
    "definition_widened": False,
    "completeness": "All 25 wave-1 tools carry a disposition from logged runs or prechecks after the band hash. Not covered: v11_1 Avro packets (not served); cutouts and forced photometry (not fetched per protocol S4); I4 construct validity and I5 certification for the two PASS tools; any alert beyond the 10 sealed ids.",
}
json.dump(axis, open(D / "tool_coverage_axis.json", "w"), indent=1)
print(json.dumps(counts), band, "precondition_b", precond_b)
for e in per:
    print(e["tool"], e["group"], e["disposition"], e.get("pass_count") or e.get("stage") or "", (e.get("reason") or "")[:60])
