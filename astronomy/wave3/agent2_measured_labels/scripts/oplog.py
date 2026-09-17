#!/usr/bin/env python3
"""Append one line to order_of_operations.log: UTC timestamp | step | event | optional file sha256.
usage: oplog.py STEP "event text" [file ...]"""
import sys, hashlib, datetime, pathlib
D = pathlib.Path(__file__).resolve().parent.parent
step, ev, files = sys.argv[1], sys.argv[2], sys.argv[3:]
ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
hs = "; ".join(f"{f} sha256={hashlib.sha256(pathlib.Path(f).read_bytes()).hexdigest()}" for f in files)
line = f"{ts} | {step} | {ev}" + (f" | {hs}" if hs else "")
with open(D / "order_of_operations.log", "a") as fh: fh.write(line + "\n")
print(line)
