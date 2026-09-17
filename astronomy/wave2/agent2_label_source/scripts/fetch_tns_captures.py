#!/usr/bin/env python3
"""E1 evidence: fetch latest Internet Archive capture (<= 2026-09-16) of www.wis-tns.org/object/<name>
for each labeled object, in the sealed fetch order (definitions_FROZEN.md section 8).
No credentials, default python-urllib User-Agent, no access-control bypass.
Saves gzipped page + parsed tables; logs every HTTP status chain. Resumable."""
import gzip, json, re, sys, time, html, hashlib, urllib.request, urllib.error
from pathlib import Path
from common import *

check_hashes()
SEAL = HERE / "sealed_fileonly_placement.json"
SEAL_SHA = (HERE / "sealed_fileonly_placement.sha256").read_text().split()[0]
if sha256(SEAL) != SEAL_SHA:
    sys.exit("ABORT: seal hash mismatch")
seal = json.load(open(SEAL))
objs = {o["ZTFID"]: o for o in seal["objects"]}
order = seal["fetch_order"]
HTML = CAPDIR / "html"; HTML.mkdir(parents=True, exist_ok=True)
LOG = CAPDIR / "fetch_log.jsonl"
PARSED = CAPDIR / "parsed.jsonl"
CAP_SECONDS = 5 * 3600
limit = int(sys.argv[1]) if len(sys.argv) > 1 else None

done = set()
if LOG.exists():
    for line in open(LOG):
        rec = json.loads(line)
        if rec.get("final") in ("ok", "invalid", "no_name", "http_error", "failed_retries"):
            done.add(rec["ZTFID"])


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


opener = urllib.request.build_opener(NoRedirect)


def get(url):
    try:
        r = opener.open(url, timeout=30)
        return r.status, dict(r.headers), r.read()
    except urllib.error.HTTPError as e:
        body = e.read() if e.fp else b""
        return e.code, dict(e.headers or {}), body
    except Exception as e:
        return -1, {}, repr(e).encode()


from tns_parse import parse


import calendar
first_start = None
if LOG.exists():
    for line in open(LOG):
        first_start = json.loads(line)["started"]; break
t0 = calendar.timegm(time.strptime(first_start, "%Y-%m-%dT%H:%M:%SZ")) if first_start else time.time()  # 5 h cap counts from the first fetch ever made
n = 0
with open(LOG, "a") as log, open(PARSED, "a") as parsed:
    for item in order:
        z = item["ZTFID"]
        if z in done:
            continue
        if limit is not None and n >= limit:
            break
        if time.time() - t0 > CAP_SECONDS:
            print("time cap reached"); break
        o = objs[z]
        name = o["tns_name"]
        rec = dict(ZTFID=z, IAUID=o["IAUID"], tier=item["tier"], started=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), chain=[])
        n += 1
        if not name:
            rec["final"] = "no_name"; log.write(json.dumps(rec) + "\n"); log.flush(); continue
        url = f"https://web.archive.org/web/20260916id_/https://www.wis-tns.org/object/{name}"
        tries = 0
        final = None
        while final is None:
            hops = 0
            u = url
            while True:
                st, hd, body = get(u)
                rec["chain"].append([u, st])
                time.sleep(1.0)  # declared minimum
                if st in (301, 302, 307, 308) and hops < 5:
                    loc = hd.get("Location") or hd.get("location")
                    if not loc:
                        break
                    u = loc if loc.startswith("http") else "https://web.archive.org" + loc
                    hops += 1
                    continue
                break
            if st in (429, 503) or st == -1:
                tries += 1
                if tries > 3:
                    final = "failed_retries"; break
                time.sleep(60 if st in (429, 503) else 10); continue  # 60 s declared for 429/503; connection errors not covered by the declaration
            if st != 200:
                final = "http_error"; break
            m = re.search(r"/web/(\d{14})id_/", u)
            rec["capture_ts"] = m.group(1) if m else None
            txt = body.decode("utf-8", errors="replace")
            fn = HTML / f"{name}_{rec['capture_ts']}.html.gz"
            fn.write_bytes(gzip.compress(body))
            rec["file"] = str(fn.relative_to(HERE)); rec["sha256_html"] = hashlib.sha256(body).hexdigest()
            p = parse(txt, name)
            final = "ok" if p["valid"] else "invalid"
            parsed.write(json.dumps(dict(ZTFID=z, IAUID=o["IAUID"], tns_name=name, capture_ts=rec["capture_ts"],
                                         sha256_html=rec["sha256_html"], **p)) + "\n"); parsed.flush()
        rec["final"] = final
        log.write(json.dumps(rec) + "\n"); log.flush()
        if n % 50 == 0:
            print(n, z, final, round(time.time() - t0), flush=True)
print("done", n, round(time.time() - t0))
