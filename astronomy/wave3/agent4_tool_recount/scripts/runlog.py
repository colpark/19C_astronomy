"""Rule D run logger. Each run: timestamps, tool, alert id, callable text, status, error, output sha256, non_default.
Outputs are hashed then discarded; values are never written or printed."""
import datetime, hashlib, json, pathlib, traceback

D = pathlib.Path(__file__).resolve().parent.parent
LOG = D / "run_log.jsonl"
ALERT_DIR = D / "out" / "raw"
BAND_HASH_TIME = "2026-09-16T18:51:26.922781Z"


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def _ser(o):
    try:
        import numpy as np
        if isinstance(o, np.ndarray):
            return o.tolist()
        if isinstance(o, (np.floating, np.integer)):
            return o.item()
    except Exception:
        pass
    try:
        import pandas as pd
        if isinstance(o, (pd.Series, pd.DataFrame)):
            return o.to_json()
    except Exception:
        pass
    return repr(o)


def run(tool, alert_id, command, fn, non_default_rule, stage_of_error=None):
    """fn() -> output. non_default_rule(output) -> bool. stage_of_error(exc) -> 'parse'|'infer'|'emit'|'load'."""
    t0 = now()
    rec = {"tool": tool, "alert_id": alert_id, "command": command, "start_utc": t0}
    try:
        out = fn()
        blob = json.dumps(out, default=_ser, sort_keys=True).encode()
        rec["output_sha256"] = hashlib.sha256(blob).hexdigest()
        nd = bool(non_default_rule(out))
        rec["non_default"] = nd
        rec["status"] = "ok" if nd else "error:emit(default output)"
        rec["error"] = None
        del out, blob
    except Exception as e:  # noqa
        st = stage_of_error(e) if stage_of_error else "unknown"
        rec["status"] = f"error:{st}"
        rec["error"] = (type(e).__name__ + ": " + str(e))[:500]
        rec["traceback_tail"] = traceback.format_exc()[-500:]
        rec["output_sha256"] = None
        rec["non_default"] = False
    rec["end_utc"] = now()
    rec["after_band_hash"] = rec["start_utc"] > BAND_HASH_TIME
    with open(LOG, "a") as fh:
        fh.write(json.dumps(rec) + "\n")
    print(json.dumps({k: rec[k] for k in ("tool", "alert_id", "status", "non_default")}), (rec.get("error") or "")[:160])
    return rec


def log_precheck(tool, command, status, error):
    rec = {"tool": tool, "alert_id": "PRECHECK", "command": command, "start_utc": now(), "status": status,
           "error": error, "output_sha256": None, "non_default": False}
    rec["end_utc"] = rec["start_utc"]
    rec["after_band_hash"] = rec["start_utc"] > BAND_HASH_TIME
    with open(LOG, "a") as fh:
        fh.write(json.dumps(rec) + "\n")
    print(json.dumps(rec)[:300])


def load_alerts():
    ids = json.load(open(D / "sealed" / "alert_ids_SEALED_v2.json"))["accepted_ids"]
    out = []
    for oid in ids:
        rows = json.load(open(ALERT_DIR / f"s4_sources_{oid}.sanitized.json"))
        rows = sorted(rows, key=lambda r: r["r:midpointMjdTai"])
        out.append((oid, rows))
    return out
