#!/usr/bin/env python3
"""Append one line to order_of_operations.log: UTC | step | text | path sha256=... ."""
import sys, hashlib, datetime, os
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()
def log(step, text, paths=()):
    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    hs = []
    for p in paths:
        ap = p if os.path.isabs(p) else os.path.join(REPO, p)
        hs.append(f"{p} sha256={sha(ap)}")
    line = f"{ts} | {step} | {text}" + (" | " + "; ".join(hs) if hs else "")
    with open(os.path.join(HERE, "order_of_operations.log"), "a") as f:
        f.write(line + "\n")
    print(line)
if __name__ == "__main__":
    log(sys.argv[1], sys.argv[2], sys.argv[3:])
