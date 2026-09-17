import sys, os, glob, datetime as dt
sys.path.insert(0, os.path.dirname(__file__)); from common import *
A=f"{REPO}/astronomy"
RL=f"{A}/wave3/agent4_tool_recount/run_log.jsonl"
rows=[json.loads(l) for l in open(RL)]
VOID={("GHOST","170609056632799366"),("GHOST","170609056632800306")}  # amendments.md AM2
def tally(rows, void=VOID):
    tools={}
    for r in rows: tools.setdefault(r["tool"],[]).append(r)
    disp={}; per={}
    for t,rs in tools.items():
        alerts=[r for r in rs if r["alert_id"] not in ("PRECHECK","LOAD")]
        valid=[r for r in alerts if (t,r["alert_id"]) not in void or "FileNotFound" not in (r["error"] or "")+(r.get("traceback_tail") or "")]
        loaded=any(r["alert_id"]=="LOAD" and r["status"]=="ok" for r in rs)
        passes=sum(1 for r in valid if r["status"]=="ok" and r["non_default"] is True)
        if not loaded and not alerts: d="UNDEMONSTRATED"
        elif passes>=1: d="PASS"
        elif loaded: d="FAIL"
        else: d="UNDEMONSTRATED"
        disp[t]=d; per[t]={"alerts_logged":len(alerts),"valid":len(valid),"passes":passes}
    from collections import Counter
    return dict(Counter(disp.values())), disp, per
c,disp,per=tally(rows)
alert_runs=sum(1 for r in rows if r["alert_id"] not in ("PRECHECK","LOAD"))
voided_check=[(r["tool"],r["alert_id"],r["status"],"FileNotFound" in (r["error"] or "")+(r.get("traceback_tail") or "")) for r in rows if (r["tool"],r["alert_id"]) in VOID]
# premises
flip=[dict(r,non_default=False) if r["tool"]=="CATS" else r for r in rows]; c_flip,_,_=tally(flip)
_,_,per_unvoid=tally(rows,void=set())
all_lines=len(rows)
inp={"run_log.jsonl":sha(RL),"recount_protocol_FROZEN.md":sha(f"{A}/wave3/agent4_tool_recount/recount_protocol_FROZEN.md"),"amendments.md":sha(f"{A}/wave3/agent4_tool_recount/amendments.md")}
seal("T01",{"counts":c,"n_tools":len(disp),"dispositions":disp},"own tally over run_log.jsonl: PASS if >=1 valid alert run status ok and non_default true; FAIL if LOAD ok and no pass; UNDEMONSTRATED if no successful load; GHOST alerts 1-2 voided per AM2 only when FileNotFound present",inp,
     {"premise":{"flip_CATS_non_default_false_counts":c_flip,"fires":c_flip!=c}})
seal("T02",{"CATS":per["CATS"],"GHOST":per["GHOST"],"voided_rows":voided_check},"as T01",inp,{"premise":{"unvoided_GHOST":per_unvoid["GHOST"],"fires":per_unvoid["GHOST"]!=per["GHOST"]}})
seal("T03",{"alert_runs":alert_runs,"all_log_lines":all_lines},"count run_log lines whose alert_id not in PRECHECK/LOAD",inp,{"premise":{"including_precheck_load":all_lines,"fires":all_lines!=alert_runs}})
# O02 precondition (b)
def P(s): return dt.datetime.fromisoformat(s.replace("Z","+00:00"))
band_line=[l for l in open(f"{A}/wave2/agent1_rubin_bands/order_of_operations.log") if "bands_FROZEN.md hashed" in l][0]
band_t=P(band_line.split(" | ")[0]); band_hash_in_log=band_line.split("bands_FROZEN.md sha256=")[1][:64]
prot_line=[l for l in open(f"{A}/wave3/agent4_tool_recount/order_of_operations.log") if "recount_protocol_FROZEN.md frozen" in l][0]
prot_t=P(prot_line.split(" | ")[0])
starts=[P(r["start_utc"]) for r in rows]; ends=[P(r["end_utc"]) for r in rows]
first=min(starts); last=max(ends)
all_after_band=all(s>band_t for s in starts); all_after_prot=all(s>prot_t for s in starts)
bands_now=sha(f"{A}/wave2/agent1_rubin_bands/bands_FROZEN.md")
mt=lambda p: dt.datetime.fromtimestamp(os.stat(p).st_mtime,dt.timezone.utc).isoformat()
d={"band_hash_utc":band_t.isoformat(),"band_hash_logged_equals_current_file":band_hash_in_log==bands_now,"protocol_frozen_utc":prot_t.isoformat(),
   "first_run_start_utc":first.isoformat(),"last_run_end_utc":last.isoformat(),"all_runs_after_band_hash":all_after_band,"all_runs_after_protocol_freeze":all_after_prot,
   "n_tools_with_disposition":len(disp),"all_25_dispositioned":len(disp)==25,"precondition_b_clears":all_after_band and all_after_prot and len(disp)==25,
   "mtime_bands_FROZEN":mt(f"{A}/wave2/agent1_rubin_bands/bands_FROZEN.md"),"mtime_recount_protocol":mt(f"{A}/wave3/agent4_tool_recount/recount_protocol_FROZEN.md"),
   "precheck_rows_timestamps_after_band":all(P(r["start_utc"])>band_t for r in rows if r["alert_id"]=="PRECHECK")}
planted=[dict(rows[0],start_utc="2026-09-16T18:00:00Z")]+rows[1:]
seal("O02",d,"own parse of run_log start/end vs band-hash log line and protocol-freeze log line; mtimes as secondary",dict(inp,**{"w2a1_oplog":sha(f"{A}/wave2/agent1_rubin_bands/order_of_operations.log"),"w3a4_oplog":sha(f"{A}/wave3/agent4_tool_recount/order_of_operations.log")}),
     {"premise":{"planted_early_run_detected": not all(P(r["start_utc"])>band_t for r in planted)}})
# O01 ruling-1 ordering
b3=f"{A}/wave3/PANEL_BRIEF_WAVE3.md"; pc=f"{A}/wave2/agent4_instrument/power_calibration.json"; pd5=f"{A}/wave3/agent4_tool_recount/power_calibration_delta005.json"
step1=[l for l in open(f"{A}/wave3/agent4_tool_recount/order_of_operations.log") if " | 1 | " in l][0]
step1_t=P(step1.split(" | ")[0]); step1_hash=step1.split("power_calibration_delta005.json sha256=")[1][:64]
brief_verif=[]
for f in glob.glob(f"{A}/wave3/*/order_of_operations.log"):
    l=open(f).readline(); brief_verif.append((os.path.relpath(f,A),l.split(" | ")[0],"a618d9114ec7c937" in l))
earliest_brief_verif=min(P(t) for _,t,ok in brief_verif if ok)
power_outputs=sorted(glob.glob(f"{A}/wave2/agent4_instrument/data_cache/power/*"))
earliest_power_mtime=min(os.stat(p).st_mtime for p in power_outputs+[pc])
t_brief=dt.datetime.fromtimestamp(os.stat(b3).st_mtime,dt.timezone.utc); t_pc=dt.datetime.fromtimestamp(os.stat(pc).st_mtime,dt.timezone.utc)
t_earliest_power=dt.datetime.fromtimestamp(earliest_power_mtime,dt.timezone.utc)
brief_text_has_override="0.018 becomes 0.05" in open(b3).read()
d={"wave3_brief_mtime_utc":t_brief.isoformat(),"wave3_brief_sha256_now":sha(b3),"wave3_brief_contains_override_text":brief_text_has_override,
   "earliest_self_logged_brief_hash_verification_utc":earliest_brief_verif.isoformat(),"brief_verifications":brief_verif,
   "power_calibration_json_mtime_utc":t_pc.isoformat(),"earliest_wave2_power_output_mtime_utc":t_earliest_power.isoformat(),
   "w3a4_step1_log_utc":step1_t.isoformat(),"w3a4_step1_logged_hash_equals_current_delta005_file":step1_hash==sha(pd5),
   "delta005_file_mtime_utc":dt.datetime.fromtimestamp(os.stat(pd5).st_mtime,dt.timezone.utc).isoformat(),
   "order_override_lt_first_MDE_mtime":t_brief<t_earliest_power, "order_first_MDE_lt_resolvability":t_pc<step1_t,
   "order_holds_in_UTC":t_brief<t_earliest_power<=t_pc<step1_t,
   "gap_override_to_first_power_output_min":(t_earliest_power-t_brief).total_seconds()/60,
   "cannot_establish_without_git":["commit times 32229e3 15:14:03-0500 and f898294 15:46 -0500 (quoted in preamble, not independently read)",
       "whether an earlier, overwritten version of power_calibration.json or any MDE print existed before 20:14Z (mtime is last-modification only)",
       "clock integrity: all mtimes and logs are self-reported on one host"]}
planted_rev=not (t_pc<t_brief)  # swapping brief and power times must break the order
seal("O01",d,"file mtimes (os.stat, UTC), first lines of wave-3 order_of_operations logs, hash of delta005 file vs step-1 log line",{"brief":sha(b3),"power_calibration.json":sha(pc),"delta005":sha(pd5)},
     {"premise":{"swap_brief_and_power_times_breaks_order":planted_rev}})
print(json.dumps({"T":c,"per":{k:per[k] for k in ("CATS","GHOST")},"runs":alert_runs},indent=0))
