#!/usr/bin/env python3
"""calendar_model_FROZEN.md sec 7: archived WISeREP object pages for the sealed lookup list (post-seal). Default UA, >=1 s spacing."""
import json, time, hashlib, urllib.request, urllib.error, pathlib, re, gzip
D = pathlib.Path(__file__).resolve().parent.parent
L = json.load(open(D/"sealed/wiserep_lookup_SEALED.json"))
assert hashlib.sha256((D/"sealed/wiserep_lookup_SEALED.json").read_bytes()).hexdigest() == (D/"sealed/wiserep_lookup_SEALED.sha256").read_text().split()[0]
class NR(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k): return None
op = urllib.request.build_opener(NR)
def get(u):
    try: r = op.open(u, timeout=30); return r.status, dict(r.headers), r.read()
    except urllib.error.HTTPError as e: return e.code, dict(e.headers or {}), (e.read() if e.fp else b"")
    except Exception as e: return -1, {}, repr(e).encode()
out = []
for group in ("typed_cohort", "untyped_cohort_sample", "positive_controls_noncohort"):
    for name in L[group]:
        chain = []; u = f"https://web.archive.org/web/20260916id_/https://www.wiserep.org/object/{name}"; body = b""
        for hop in range(5):
            st, hd, body = get(u); chain.append([u, st]); time.sleep(1.2)
            if st in (301, 302) and (hd.get("Location") or hd.get("location")):
                loc = hd.get("Location") or hd.get("location"); u = loc if loc.startswith("http") else "https://web.archive.org" + loc; continue
            break
        while body[:2] == b"\x1f\x8b": body = gzip.decompress(body)
        title = re.search(rb"<title>(.*?)</title>", body, re.S)
        rec = dict(group=group, name=name, chain=chain, final_status=chain[-1][1], bytes=len(body), sha256=hashlib.sha256(body).hexdigest(),
                   title=title.group(1).decode(errors="replace").strip() if title else None, utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
        if chain[-1][1] == 200:
            (D/"sources/wiserep"/f"object_{name}.html").write_bytes(body)
        out.append(rec); print(group, name, [s for _, s in chain], rec["title"], flush=True)
json.dump(out, open(D/"out/wiserep_archive_probe.json", "w"), indent=1)
