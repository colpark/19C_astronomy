#!/usr/bin/env python3
"""AMW4-1 transport retry: re-probe archived WISeREP pages whose first probe ended in a connection error (-1). Up to 3 attempts."""
import json, time, urllib.request, urllib.error, pathlib, gzip, hashlib
D = pathlib.Path(__file__).resolve().parent.parent
class NR(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k): return None
op = urllib.request.build_opener(NR)
def get(u):
    try: r = op.open(u, timeout=45); return r.status, dict(r.headers), r.read()
    except urllib.error.HTTPError as e: return e.code, dict(e.headers or {}), (e.read() if e.fp else b"")
    except Exception as e: return -1, {}, repr(e).encode()
P = D/"out/wiserep_archive_probe.json"; prev = json.load(open(P))
for rec in prev:
    if rec["final_status"] != -1: continue
    for attempt in range(3):
        chain = []; u = f"https://web.archive.org/web/20260916id_/https://www.wiserep.org/object/{rec['name']}"; body = b""
        for hop in range(5):
            st, hd, body = get(u); chain.append([u, st]); time.sleep(2)
            loc = hd.get("Location") or hd.get("location")
            if st in (301, 302) and loc: u = loc if loc.startswith("http") else "https://web.archive.org" + loc; continue
            break
        rec.setdefault("retries", []).append(dict(attempt=attempt + 1, chain=chain, utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())))
        if chain[-1][1] != -1:
            rec["final_status"] = chain[-1][1]
            if chain[-1][1] == 200:
                while body[:2] == b"\x1f\x8b": body = gzip.decompress(body)
                (D/"sources/wiserep"/f"object_{rec['name']}.html").write_bytes(body); rec["sha256"] = hashlib.sha256(body).hexdigest()
            break
        time.sleep(10)
    print(rec["name"], rec["final_status"], flush=True)
json.dump(prev, open(P, "w"), indent=1)
