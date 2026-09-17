#!/usr/bin/env python3
"""Protocol sec 7: reachable fractions f19, f185 from sample R rows (difference-flux peak, S/N>=5)."""
import json, math, pathlib, collections
from scipy.stats import beta
D = pathlib.Path(__file__).resolve().parent.parent
oids = json.load(open(D/"sealed/lookup_list_SEALED.json"))["sample_R"]["oids"]
peak = {}; nrows = 0; batches = []
for l in open(D/"out/reach_rows.jsonl"):
    b = json.loads(l); batches.append((b["batch"], b["status"], b["n_rows"]))
    for r in b["rows"] or []:
        nrows += 1
        f, e = r.get("r:psfFlux"), r.get("r:psfFluxErr")
        oid = str(r.get("r:diaObjectId"))
        if f is None or e is None or f <= 0 or e <= 0 or f / e < 5: continue
        m = 31.4 - 2.5 * math.log10(f)
        peak[oid] = min(peak.get(oid, 99), m)
def cp(k, n):
    lo = beta.ppf(0.025, k, n - k + 1) if k > 0 else 0.0
    hi = beta.ppf(0.975, k + 1, n - k) if k < n else 1.0
    return [round(float(lo), 6), round(float(hi), 6)]
n = len(oids); with_rows = sum(1 for o in oids if o in peak)
k19 = sum(1 for o in oids if peak.get(o, 99) <= 19.0); k185 = sum(1 for o in oids if peak.get(o, 99) <= 18.5)
O = 1937669
res = dict(sample_n=n, oids_with_SN5_detection=with_rows, rows=nrows, batches=batches,
  f19=dict(k=k19, n=n, point=k19/n, cp95=cp(k19, n)), f185=dict(k=k185, n=n, point=k185/n, cp95=cp(k185, n)),
  peak_mag_quantiles={q: sorted(peak.values())[int(q*(len(peak)-1))] for q in (0.0, 0.01, 0.05, 0.1, 0.5, 0.9)} if peak else None,
  A_per_night={nn: dict(point=k19/n*O/nn, cp95_hi=cp(k19, n)[1]*O/nn, cp95_lo=cp(k19, n)[0]*O/nn) for nn in (10, 9)},
  A185_per_night={nn: dict(point=k185/n*O/nn, cp95_hi=cp(k185, n)[1]*O/nn) for nn in (10, 9)},
  denominator_note="oids without any S/N>=5 positive difference-flux row count as not reachable (peak unknown -> fainter than S/N 5); disclosed")
json.dump(res, open(D/"out/reachability.json", "w"), indent=1); print(json.dumps(res, indent=1)[:2500])
