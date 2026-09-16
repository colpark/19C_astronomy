#!/usr/bin/env python3
"""Issue-09 checks for a blind replay file. Reads polarity programmatically; prints only
aggregate statistics and p-values, never a per-case polarity.

library use: checks(rows_in_output_order, idcol, cases_by_id, idmap, original_index, suite, perm_seed)
cli:  idcheck.py <blind.csv> <idcol> <map.csv> <map_blind_col> <cases.csv> <suite> <perm_seed_int>
"""
import csv, re, sys, random
from collections import defaultdict

def author(case_id):
    if re.match(r"AST0\d$", case_id): return "agent1"
    for pre, a in (("AST-P2-", "agent2"), ("AST3-", "agent3"), ("AST4-", "agent4"), ("AST5-", "agent5"), ("ASTC-", "coordinator")):
        if case_id.startswith(pre): return a
    return None

def ranks(xs):
    return list(range(len(xs)))

def mean_rank_gap(labels):
    a = [i for i, l in enumerate(labels) if l == "must_fire"]; b = [i for i, l in enumerate(labels) if l != "must_fire"]
    return abs(sum(a) / len(a) - sum(b) / len(b)) if a and b else 0.0

def spearman_abs(x):  # x = original index per output position; positions are 0..n-1
    n = len(x)
    r = sorted(range(n), key=lambda i: x[i]); rk = [0] * n
    for pos, i in enumerate(r): rk[i] = pos
    d2 = sum((rk[i] - i) ** 2 for i in range(n))
    return abs(1 - 6 * d2 / (n * (n * n - 1)))

def kw_h(groups):
    n = len(groups); by = defaultdict(list)
    for i, g in enumerate(groups): by[g].append(i + 1)
    return 12 / (n * (n + 1)) * sum(len(v) * (sum(v) / len(v)) ** 2 for v in by.values()) - 3 * (n + 1)

def perm_p(stat, seq, rng, n_perm=20000):
    obs = stat(seq); cnt = 0; s = list(seq)
    for _ in range(n_perm):
        rng.shuffle(s)
        if stat(s) >= obs - 1e-12: cnt += 1
    return (cnt + 1) / (n_perm + 1)

def checks(out_ids, cases_by_id, idmap, original_index, suite, perm_seed):
    rng = random.Random(perm_seed)
    orig = [idmap[o] for o in out_ids]
    pol = [cases_by_id[c]["polarity"] for c in orig]
    res = {"n": len(out_ids)}
    pref = {re.match(r"[^0-9]*", o).group(0) for o in out_ids}
    res["distinct_non_digit_prefixes"] = len(pref)
    res["ids_share_one_alpha_prefix"] = len({re.match(r"[A-Za-z_-]*", o).group(0) for o in out_ids}) == 1 and bool(re.match(r"[A-Za-z]", out_ids[0]))
    nums = [re.findall(r"\d+", o) for o in out_ids]
    res["ids_are_row_counters"] = all(n and int(n[-1]) == i + 1 for i, n in enumerate(nums))
    res["ids_sorted_equals_row_order"] = list(out_ids) == sorted(out_ids)
    res["p_polarity_vs_position"] = round(perm_p(mean_rank_gap, pol, rng), 4)
    res["p_original_index_vs_position"] = round(perm_p(spearman_abs, [original_index[c] for c in orig], rng), 4)
    if suite == "astronomy_replay":
        res["p_author_vs_position"] = round(perm_p(kw_h, [author(c) for c in orig], rng), 4)
    # id-channel check: does any leading id character class separate polarity perfectly?
    by = defaultdict(set)
    for o, p in zip(out_ids, pol): by[o[0]].add(p)
    res["first_char_groups_all_single_polarity"] = all(len(v) == 1 for v in by.values()) and len(by) < len(out_ids) / 2
    return res

if __name__ == "__main__":
    blind, idcol, mapf, mapcol, casesf, suite, seed = sys.argv[1:8]
    rows = list(csv.DictReader(open(blind, newline="")))
    cases = list(csv.DictReader(open(casesf, newline="")))
    cb = {c["case_id"]: c for c in cases}; oi = {c["case_id"]: i for i, c in enumerate(cases)}
    idmap = {r[mapcol]: r["case_id"] for r in csv.DictReader(open(mapf, newline=""))}
    import json
    print(json.dumps(checks([r[idcol] for r in rows], cb, idmap, oi, suite, int(seed)), indent=1))
