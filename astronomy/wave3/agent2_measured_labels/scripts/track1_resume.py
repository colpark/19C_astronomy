#!/usr/bin/env python3
"""Track one (protocol sec 11): resume wave-2 E1 fetch (definitions_FROZEN.md 4f89ff67, sealed order 76300235) under the public archive
route. Reads wave-2 fetch_log.jsonl READ-ONLY for already-attempted objects; writes only under this directory. Cap: 1 h (AMW3-2, declared here before running)."""
import json, time, re, sys, hashlib, gzip, urllib.request, urllib.error, pathlib
D = pathlib.Path(__file__).resolve().parent.parent
W2 = D.parents[1] / "wave2/agent2_label_source"
seal = W2/"sealed_fileonly_placement.json"
assert hashlib.sha256(seal.read_bytes()).hexdigest() == "763002355b6129d9fe0a0eada86684e7dfb2e02bc9475554a8a57c9969c03eb0"
S = json.load(open(seal)); objs = {o["ZTFID"]: o for o in S["objects"]}
done = set(json.loads(l)["ZTFID"] for l in open(W2/"sources/tns_captures/fetch_log.jsonl"))
OUT = D/"out/track1_captures"; (OUT/"html").mkdir(parents=True, exist_ok=True); LOG = OUT/"fetch_log.jsonl"
if LOG.exists(): done |= set(json.loads(l)["ZTFID"] for l in open(LOG))
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k): return None
op = urllib.request.build_opener(NoRedirect)
def get(u):
    try:
        r = op.open(u, timeout=30); return r.status, dict(r.headers), r.read()
    except urllib.error.HTTPError as e: return e.code, dict(e.headers or {}), (e.read() if e.fp else b"")
    except Exception as e: return -1, {}, repr(e).encode()
t0 = time.time(); n = 0
with open(LOG, "a") as log:
    for item in S["fetch_order"]:
        z = item["ZTFID"]
        if z in done: continue
        if time.time() - t0 > 3600: print("cap", flush=True); break
        o = objs[z]; name = o["tns_name"]
        rec = dict(ZTFID=z, IAUID=o["IAUID"], tier=item["tier"], started=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), chain=[])
        if not name: rec["final"] = "no_name"; log.write(json.dumps(rec)+"\n"); continue
        url = f"https://web.archive.org/web/20260916id_/https://www.wis-tns.org/object/{name}"; tries = 0; final = None
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
            fn = OUT/"html"/f"{name}_{rec['capture_ts']}.html.gz"; fn.write_bytes(gzip.compress(body))
            rec["file"] = str(fn.relative_to(D)); rec["sha256_html"] = hashlib.sha256(body).hexdigest(); final = "ok"
        rec["final"] = final; log.write(json.dumps(rec)+"\n"); log.flush(); n += 1
print("done", n, flush=True)
