#!/usr/bin/env python3
"""Rule C fetcher. GET/POST a URL, record status and headers, drop label-bearing keys BEFORE anything
is written or printed. Raw bytes are never stored; only their sha256 and the dropped key names.
usage: safe_fetch.py OUTNAME METHOD URL [json_body]"""
import sys, json, hashlib, re, datetime, pathlib, requests
D = pathlib.Path(__file__).resolve().parent.parent
LABEL = re.compile(r"(class|prob|label|tns|type|score|rank|classifier|tag|xm_|simbad|otype|cataloged|clf_|sherlock|annotation|features?)", re.I)
def strip(o, dropped):
    if isinstance(o, dict):
        out = {}
        for k, v in o.items():
            if LABEL.search(str(k)): dropped.add(str(k)); continue
            out[k] = strip(v, dropped)
        return out
    if isinstance(o, list): return [strip(x, dropped) for x in o]
    return o
def fetch(name, method, url, body=None, timeout=300):
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
    try:
        r = requests.request(method, url, json=body, timeout=timeout)
    except Exception as e:
        rec = dict(name=name, time_utc=ts, method=method, url=url, body=body, status=None, error=repr(e))
        (D / "out/raw" / f"{name}.meta.json").write_text(json.dumps(rec, indent=1)); return rec, None
    dropped = set()
    try:
        data = strip(r.json(), dropped); kind = "json"
    except Exception:
        txt = r.text
        data = None if LABEL.search(txt[:0]) else txt[:2000]; kind = "text(first 2000 chars)"
    rec = dict(name=name, time_utc=ts, method=method, url=url, body=body, status=r.status_code,
               headers={k: v for k, v in r.headers.items() if k.lower() in ("content-type", "date", "server", "content-length", "www-authenticate")},
               raw_sha256=hashlib.sha256(r.content).hexdigest(), raw_bytes=len(r.content), kind=kind, dropped_keys=sorted(dropped))
    (D / "out/raw" / f"{name}.meta.json").write_text(json.dumps(rec, indent=1))
    (D / "out/raw" / f"{name}.sanitized.json").write_text(json.dumps(data))
    return rec, data
if __name__ == "__main__":
    name, method, url = sys.argv[1:4]
    body = json.loads(sys.argv[4]) if len(sys.argv) > 4 else None
    rec, data = fetch(name, method, url, body)
    print(json.dumps(rec, indent=1)); print(json.dumps(data)[:1500])
