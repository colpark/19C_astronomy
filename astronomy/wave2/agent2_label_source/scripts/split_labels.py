#!/usr/bin/env python3
"""Per-object label basis and SNIascore / CCSNscore bounds (definitions_FROZEN.md sections 2-7).
Reads the sealed file-only placement and the archived TNS captures (re-parsed from the saved gz pages)."""
import gzip, json, collections, sys
import pandas as pd
from common import *
from tns_parse import parse

check_hashes()
SEAL = HERE / "sealed_fileonly_placement.json"
assert sha256(SEAL) == (HERE / "sealed_fileonly_placement.sha256").read_text().split()[0], "seal hash mismatch"
seal = json.load(open(SEAL))
objs = pd.DataFrame(seal["objects"])
LOG = CAPDIR / "fetch_log.jsonl"
fetch = {}
if LOG.exists():
    for line in open(LOG):
        r = json.loads(line)
        fetch[r["ZTFID"]] = r  # last record wins

status_counts = collections.Counter()
mismatch_pairs = collections.Counter()
rows = []
sniascore_reports = []
syncatto = []
for o in objs.itertuples():
    f = fetch.get(o.ZTFID)
    fstat = f["final"] if f else "not_attempted"
    status_counts[fstat] += 1
    cat, strength, ev, e1_detail = "UNRESOLVED", "", [], {}
    model = ""
    if fstat in ("ok", "invalid"):
        # AMENDMENT A1 (parser bug fix): some captures were served gzip-encoded, so the stored copy is gzip-in-gzip;
        # the fetch-time parser marked them 'invalid'. Decompress until the payload is not gzip, then re-parse.
        body = gzip.decompress((HERE / f["file"]).read_bytes())
        while body[:2] == b"\x1f\x8b":
            body = gzip.decompress(body)
        page = body.decode("utf-8", errors="replace")
        p = parse(page, o.tns_name)
        cap = f["capture_ts"]
        if not p["valid"]:
            ev.append(f"E1 invalid capture {cap}")
        elif not p["reports"]:
            ev.append(f"E1 capture {cap}: no classification report on page")
        else:
            reps = sorted(p["reports"], key=lambda r: r["time"] or "")
            last = reps[-1]
            for r in reps:
                if automated_marker(r["classifier"]) == "SNIascore":
                    sniascore_reports.append(dict(ZTFID=o.ZTFID, time=r["time"], classification=r["classification"], bts_type=o.type, is_latest=r is last))
                if "syncatto" in (r["classifier"] or "").lower() and r is last:
                    syncatto.append(o.ZTFID)
            e1_detail = dict(capture=cap, report_id=last["id"], time=last["time"], classifier=last["classifier"], sender=last["sender"],
                             group=last["group"], tns_class=last["classification"], n_reports=len(reps), n_spectra=len(p["spectra"]))
            if not class_match(o.type, last["classification"]):
                mismatch_pairs[(o.type, last["classification"])] += 1
                ev.append(f"E1 capture {cap}: latest report {last['id']} '{last['classification']}' does not match BTS '{o.type}'")
            else:
                mk = automated_marker(last["classifier"])
                spec_before = [s for s in p["spectra"] if (s["obsdate"] or "9999") <= (last["time"] or "")]
                remark_phot = bool(re.search(r"photometr|light ?curve", last["remarks"] or "", re.I))
                base = f"E1 wis-tns.org/object/{o.tns_name} capture {cap}: report {last['id']} {last['time']} by '{last['classifier']}' (sender {last['sender']}, group {last['group']}) = '{last['classification']}'"
                if mk:
                    cat, strength, model = "MODEL_ANNOTATION", "STRONG", mk
                    ev.append(base + f"; automated marker {mk}")
                elif not spec_before:
                    cat = "PHOTOMETRIC_ONLY"
                    strength = "STRONG" if remark_phot else "MODERATE"
                    ev.append(base + f"; no public spectrum with obs-date <= report time ({len(p['spectra'])} spectra listed)" + ("; remarks state photometric basis" if remark_phot else ""))
                else:
                    cat, strength = "MEASURED", "STRONG"
                    ev.append(base + f"; human classifier; {len(spec_before)} public spectrum/spectra on or before report")
    else:
        ev.append(f"E1 not available: fetch {fstat}")
    # E2 (moderate) applies only when E1 did not place
    if o.E2:
        if cat == "UNRESOLVED":
            cat, strength, model = "MODEL_ANNOTATION", "MODERATE", "SNIascore"
        ev.append(o.evidence.split(" | ")[[i for i, s in enumerate(o.evidence.split(" | ")) if s.startswith("E2")][0]])
    for tag in ("E3", "E4", "E5", "E6"):
        for s in (o.evidence or "").split(" | "):
            if s.startswith(tag):
                ev.append(s)
    rows.append(dict(ZTFID=o.ZTFID, IAUID=o.IAUID, **{"class": o.type}, category=cat if cat != "UNRESOLVED" else "UNRESOLVED (UNDEMONSTRATED)",
                     model=model, strength=strength, evidence=" || ".join(ev), fetch_status=fstat,
                     E2=o.E2, E3=o.E3, E4=o.E4, E5=o.E5, E6=o.E6, discdate=o.discdate, peakt=o.peakt,
                     e1_group=e1_detail.get("group", ""), e1_classifier=e1_detail.get("classifier", ""),
                     e1_report_time=e1_detail.get("time", ""), e1_capture=e1_detail.get("capture", ""),
                     syncatto_classifier=o.ZTFID in syncatto))
t = pd.DataFrame(rows)
t[["ZTFID", "class", "category", "evidence", "strength"]].to_csv(HERE / "label_basis_per_object.csv", index=False)
t.to_csv(HERE / "label_basis_per_object_detail.csv", index=False)

# ---- bounds
P = t[t["class"] == "SN Ia"]
is_sn = (P.category == "MODEL_ANNOTATION") & (P.model == "SNIascore")
L_strong = int((is_sn & (P.strength == "STRONG")).sum())
L = int(is_sn.sum())
e1_excl = P.category.isin(["MEASURED", "PHOTOMETRIC_ONLY"]) | ((P.category == "MODEL_ANNOTATION") & (P.model != "SNIascore"))
U_raw = int((~(e1_excl | P.E4 | P.E5)).sum())
U_noE5 = int((~(e1_excl | P.E4)).sum())
bound = dict(lower=max(L, 0), upper=min(U_raw, WAVE1_UPPER), lower_strong_only=L_strong, upper_raw=U_raw,
             upper_noE5_sensitivity_not_slot_value=U_noE5, wave1=[0, WAVE1_UPPER],
             excluded_by=dict(E1=int(e1_excl.sum()), E4=int(P.E4.sum()), E5=int(P.E5.sum()), E1_only_not_E4_E5=int((e1_excl & ~P.E4 & ~P.E5).sum())),
             within_upper_E1_status=P[~(e1_excl | P.E4 | P.E5)].fetch_status.value_counts().to_dict(),
             within_upper_unresolved=int((~(e1_excl | P.E4 | P.E5) & ~is_sn).sum()))
C = t[t["class"].isin(CC_CLASSES)]
cc_model = (C.category == "MODEL_ANNOTATION") & (C.model == "CCSNscore")
cc_excl = C.category.isin(["MEASURED", "PHOTOMETRIC_ONLY"]) | ((C.category == "MODEL_ANNOTATION") & (C.model != "CCSNscore"))
cc_date = pd.to_datetime(C.discdate, errors="coerce") >= CCSN_DISC_CUT
cc_bound = dict(population=len(C), lower=int(cc_model.sum()), upper=int((cc_date & ~cc_excl).sum()) if True else None,
                upper_before_E1=int(cc_date.sum()),
                note="upper counts CC-class objects discovered >= 2025-02-09 not excluded by E1; start date of CCSNscore TNS reporting UNDEMONSTRATED; any CCSNscore report found with discovery < 2025-02-09 would falsify the date margin",
                ccsnscore_reports_found_discovered_before_cut=int((cc_model & ~cc_date).sum()))
sn_times = sorted(r["time"] for r in sniascore_reports)
by_year = collections.Counter(r["time"][:4] for r in sniascore_reports if r["is_latest"])
summary = dict(
    definitions_sha256=DEFS_SHA, seal_sha256=sha256(SEAL),
    population_labeled=len(t),
    fetch_status=dict(status_counts),
    category_counts=t.category.value_counts().to_dict(),
    category_by_strength=t.groupby(["category", "strength"]).size().rename("n").reset_index().to_dict("records"),
    model_annotation_by_model=t[t.category == "MODEL_ANNOTATION"].groupby(["model", "strength"]).size().rename("n").reset_index().to_dict("records"),
    photometric_only_by_class=t[t.category == "PHOTOMETRIC_ONLY"]["class"].value_counts().to_dict(),
    measured_by_group=t[t.category == "MEASURED"].e1_group.value_counts().head(15).to_dict(),
    sniascore_bound=bound, ccsnscore_bound=cc_bound,
    sniascore_reports_seen=dict(n=len(sniascore_reports), earliest=sn_times[0] if sn_times else None, latest=sn_times[-1] if sn_times else None,
                                latest_report_is_sniascore_by_year=dict(sorted(by_year.items())),
                                sniascore_report_not_SN_Ia=[r for r in sniascore_reports if r["classification"] != "SN Ia"][:20],
                                sniascore_report_before_2021_04_15=[r for r in sniascore_reports if r["time"] < "2021-04-15"][:20],
                                sniascore_earlier_report_superseded=sum(1 for r in sniascore_reports if not r["is_latest"])),
    class_mismatch_pairs_top=[dict(bts=a, tns=b, n=n) for (a, b), n in mismatch_pairs.most_common(40)],
    class_mismatch_total=sum(mismatch_pairs.values()),
    syncatto_latest_classifier_measured=int(t[t.syncatto_classifier & (t.category == "MEASURED")].shape[0]),
    e2_contradicted_by_e1=t[t.E2 & (t.category != "MODEL_ANNOTATION")][["ZTFID", "category", "e1_classifier"]].to_dict("records"),
)
json.dump(summary, open(HERE / "split_summary.json", "w"), indent=1, default=str)
print(json.dumps(summary, indent=1, default=str))
