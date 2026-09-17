#!/usr/bin/env python3
"""Addition C seal: file-only / paper-only placement (E2-E6) of every labeled object, and the
bound these rules give, written and hashed BEFORE any archived TNS page is read per object.
Implements definitions_FROZEN.md sections 5, 6, 7, 9."""
import json
import numpy as np
import pandas as pd
from common import *

check_hashes()
raw, ext = load()
assert len(raw) == 11217
ext = ext[["ZTFID", "discID", "discdate", "type"]].rename(columns={"type": "type_ext"})
d = raw.merge(ext, on="ZTFID", how="left", validate="1:1")
assert (d.type == d.type_ext).all()
lab = d[d.type != "-"].copy()
assert len(lab) == 7843
lab["peakt_f"] = lab.peakt.astype(float)
lab["disc"] = pd.to_datetime(lab.discdate.str[:10], errors="coerce")
cap = parse_explorer_capture(CAP2021)
lab["cap2021_type"] = lab.ZTFID.map(cap)
lab["tns_name"] = lab.IAUID.map(iau_to_tns)

rows = []
for r in lab.itertuples():
    ev = []
    plain = r.type == "SN Ia"
    e2 = plain and r.IAUID in E2_NAMED
    e3 = not plain
    e4 = plain and r.cap2021_type == "SN Ia"
    e5 = plain and r.peakt_f < E5_CUT
    e6 = (not pd.isna(r.disc)) and r.disc >= pd.Timestamp("2021-04-15")
    if e2: ev.append("E2:" + E2_NAMED[r.IAUID])
    if e3: ev.append("E3:type '%s' not emittable by SNIascore" % r.type)
    if e4: ev.append("E4:SN Ia in BTS explorer capture 2021-01-28T12:53:21")
    if e5: ev.append("E5:peakt %.2f < %.1f" % (r.peakt_f, E5_CUT))
    if e6: ev.append("E6:discovered %s >= 2021-04-15" % r.disc.date())
    cc_possible = r.type in CC_CLASSES and (not pd.isna(r.disc)) and r.disc >= CCSN_DISC_CUT
    rows.append(dict(ZTFID=r.ZTFID, IAUID=r.IAUID, tns_name=r.tns_name, type=r.type, peakt=r.peakt_f,
                     discdate=None if pd.isna(r.disc) else str(r.disc.date()),
                     E2=e2, E3=e3, E4=e4, E5=e5, E6=e6, ccsn_possible_by_date=bool(cc_possible),
                     fileonly_category="MODEL_ANNOTATION" if e2 else "UNRESOLVED",
                     fileonly_strength="MODERATE" if e2 else "",
                     evidence=" | ".join(ev)))
t = pd.DataFrame(rows)
P = t[t.type == "SN Ia"]
L = int(P.E2.sum())
U = int((~(P.E4 | P.E5)).sum())
U_noE5 = int((~P.E4).sum())
# fetch order (section 8)
rng = np.random.default_rng(20260916)
tier1 = t[(t.type == "SN Ia") & ~t.E5]
tier2 = t[(t.type == "SN Ia") & t.E5]
tier3 = t[t.type != "SN Ia"]
order = []
for tier, df in [(1, tier1), (2, tier2), (3, tier3)]:
    ids = df.ZTFID.to_numpy()[rng.permutation(len(df))]
    order += [dict(tier=tier, ZTFID=z) for z in ids]
seal = dict(
    sealed_at="2026-09-16, before any per-object archived TNS page read",
    definitions_sha256=DEFS_SHA,
    raw_sha256=RAW_SHA, extra_sha256=EXTRA_SHA, capture2021_sha256=CAP2021_SHA,
    capture2021_rows_parsed=len(cap), capture2021_note="Internet Archive stored copy truncated at 1,048,576 bytes; rows present parsed",
    labeled=len(t), plain_SN_Ia=len(P),
    E2_named_in_file_as_SN_Ia=L,
    E2_names_not_plain_SN_Ia_in_file={n: (lab[lab.IAUID == n].type.tolist() or ["absent"]) for n in E2_NAMED if n not in set(P.IAUID)},
    E4_excluded=int(P.E4.sum()), E5_excluded=int(P.E5.sum()), E4_and_E5=int((P.E4 & P.E5).sum()),
    predicted_bound_fileonly=dict(lower=L, upper=min(U, WAVE1_UPPER), upper_raw=U, upper_noE5_sensitivity=U_noE5),
    ccsn_possible_by_date=int(t.ccsn_possible_by_date.sum()),
    fetch_order_counts=dict(tier1=len(tier1), tier2=len(tier2), tier3=len(tier3)),
    placement_counts=t.fileonly_category.value_counts().to_dict(),
)
out = HERE / "sealed_fileonly_placement.json"
json.dump(dict(summary=seal, fetch_order=order, objects=t.to_dict("records")), open(out, "w"), indent=0, default=str)
(HERE / "sealed_fileonly_placement.sha256").write_text(f"{sha256(out)}  sealed_fileonly_placement.json\n")
print(json.dumps(seal, indent=1, default=str))
print("sha256", sha256(out))
