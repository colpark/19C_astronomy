#!/usr/bin/env python3
"""Append one line to order_of_operations.log:
<UTC ISO> | <step> | <message> | <path> sha256=<hex> ; ...
usage: oplog.py <step> <message> [paths...]   (run from agent5_integrity/, paths relative to repo root allowed)"""
import sys, hashlib, datetime, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
step, msg, paths = sys.argv[1], sys.argv[2], sys.argv[3:]
def res(p):
    return p if os.path.isabs(p) or os.path.exists(p) else os.path.join(ROOT, p)
hs = " ; ".join(f"{p} sha256={hashlib.sha256(open(res(p),'rb').read()).hexdigest()}" for p in paths)
line = f"{datetime.datetime.now(datetime.timezone.utc).isoformat().replace('+00:00','Z')} | {step} | {msg}" + (f" | {hs}" if hs else "")
open(os.path.join(os.path.dirname(__file__), "..", "order_of_operations.log"), "a").write(line + "\n")
print(line)
