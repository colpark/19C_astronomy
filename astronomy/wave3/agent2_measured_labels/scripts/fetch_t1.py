#!/usr/bin/env python3
"""Protocol sec 6: T1 Internet Archive captures of www.wis-tns.org/object/<name> for E (tier A then tier B), cap 4 h from first request.
Default python-urllib UA, no credentials, 1.0 s spacing, 60 s wait on 429/503 (3 retries), 30 s timeout. Resumable."""
import json, time, re, sys, hashlib, gzip, calendar, urllib.request, urllib.error, pathlib
D = pathlib.Path(__file__).resolve().parent.parent
E = json.load(open(D/"sealed/enumeration_E_SEALED.json"))
assert hashlib.sha256((D/"sealed/enumeration_E_SEALED.json").read_bytes()).hexdigest() == (D/"sealed/enumeration_E_SEALED.sha256").read_text().split()[0]
order = [("A", x["name"]) for x in E["tierA"]] + [("B", x["name"]) for x in E["tierB"]]
CAP = D/"out/tns_captures_w3"; (CAP/"html").mkdir(parents=True, exist_ok=True)
LOG = CAP/"fetch_log.jsonl"
done = set(); first = None
if LOG.exists():
    for l in open(LOG):
        r = json.loads(l); done.add(r["name"]); first = first or r["started"]
t0 = calendar.timegm(time.strptime(first, "%Y-%m-%dT%H:%M:%SZ")) if first else time.time()
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k): return None
op = urllib.request.build_opener(NoRedirect)
def get(u):
    try:
        r = op.open(u, timeout=30); return r.status, dict(r.headers), r.read()
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers or {}), (e.read() if e.fp else b"")
    except Exception as e:
        return -1, {}, repr(e).encode()
n = 0
with open(LOG, "a") as log:
    for tier, name in order:
        if name in done: continue
        if time.time() - t0 > 4*3600: print("time cap reached", flush=True); break
        rec = dict(name=name, tier=tier, started=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), chain=[])
        url = f"https://web.archive.org/web/20260916id_/https://www.wis-tns.org/object/{name}"
        tries = 0; final = None
        while final is None:
            u = url; hops = 0
            while True:
                st, hd, body = get(u); rec["chain"].append([u, st]); time.sleep(1.0)
                if st in (301, 302, 307, 308) and hops < 5:
                    loc = hd.get("Location") or hd.get("location")
                    if not loc: break
                    u = loc if loc.startswith("http") else "https://web.archive.org" + loc; hops += 1; continue
                break
            if st in (429, 503) or st == -1:
                tries += 1
                if tries > 3: final = "failed_retries"; break
                time.sleep(60 if st in (429, 503) else 10); continue
            if st != 200: final = "http_error"; break
            m = re.search(r"/web/(\d{14})id_/", u); rec["capture_ts"] = m.group(1) if m else None
            fn = CAP/"html"/f"{name}_{rec['capture_ts']}.html.gz"; fn.write_bytes(gzip.compress(body))
            rec["file"] = str(fn.relative_to(D)); rec["sha256"] = hashlib.sha256(body).hexdigest(); final = "ok"
        rec["final"] = final; log.write(json.dumps(rec) + "\n"); log.flush(); n += 1
        if n % 50 == 0: print(n, name, final, round(time.time()-t0), flush=True)
print("done", n, flush=True)
