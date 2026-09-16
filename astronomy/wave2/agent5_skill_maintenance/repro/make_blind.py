#!/usr/bin/env python3
"""Build a polarity-free cases_blind.csv (opaque ids, shuffled rows) and an id map for the holder.
Never prints polarity. Hashes the polarity column in a canonical form without writing it.
Canonical polarity column: UTF-8 bytes of "case_id,polarity\\n" followed by one "<case_id>,<polarity>\\n"
line per row, in cases.csv row order.
usage: make_blind.py <cases.csv> <prefix> <seed> <blind_out> <idmap_out>"""
import csv, hashlib, io, json, random, re, sys
src, prefix, seed, blind_out, map_out = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4], sys.argv[5]
raw = open(src, "rb").read()
rows = list(csv.DictReader(io.StringIO(raw.decode("utf-8"), newline="")))
pol = "case_id,polarity\n" + "".join(f"{r['case_id']},{r['polarity']}\n" for r in rows)
order = list(range(len(rows))); random.Random(seed).shuffle(order)
ids = {rows[i]["case_id"]: f"{prefix}-{j+1:02d}" for j, i in enumerate(order)}
with open(blind_out, "w", newline="") as fh:
    w = csv.writer(fh, lineterminator="\n"); w.writerow(["case_id", "stage", "sealed", "input"])
    for i in order: w.writerow([ids[rows[i]["case_id"]], rows[i]["stage"], rows[i]["sealed"], rows[i]["input"]])
with open(map_out, "w", newline="") as fh:
    w = csv.writer(fh, lineterminator="\n"); w.writerow(["blind_id", "case_id"])
    for i in order: w.writerow([ids[rows[i]["case_id"]], rows[i]["case_id"]])
blind = open(blind_out, "rb").read()
leak_words = re.compile(r"must[ _-]?(not[ _-]?)?fire|polarity", re.I)
print(json.dumps({
    "source": src, "source_sha256": hashlib.sha256(raw).hexdigest(), "rows": len(rows),
    "polarity_column_canonical_sha256": hashlib.sha256(pol.encode()).hexdigest(),
    "shuffle_seed": seed, "blind_file": blind_out, "blind_sha256": hashlib.sha256(blind).hexdigest(),
    "blind_header": blind.split(b"\n", 1)[0].decode(),
    "blind_inputs_matching_polarity_words": sum(bool(leak_words.search(r["input"])) for r in rows),
    "id_map_file": map_out, "id_map_sha256": hashlib.sha256(open(map_out, "rb").read()).hexdigest(),
}, indent=1))
