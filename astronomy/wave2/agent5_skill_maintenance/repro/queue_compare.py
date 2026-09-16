#!/usr/bin/env python3
"""Compare vendored clopper (orig), patched clopper (fixed) and scipy.stats.beta.ppf."""
import sys, importlib.util
from scipy.stats import beta
def load(p, name):
    s = importlib.util.spec_from_file_location(name, p); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
O = load(sys.argv[1], "orig"); F = load(sys.argv[2], "fixed")
def sp(k, n, alpha=0.05):
    return (0.0 if k == 0 else float(beta.ppf(alpha/2, k, n-k+1)), 1.0 if k == n else float(beta.ppf(1-alpha/2, k+1, n-k)))
grid = [(k, n) for n in (1, 2, 3, 5, 6, 10, 20, 40, 50, 100, 200, 250, 500, 1000, 1071) for k in sorted({0, 1, 2, n//6, n//3, n//2, n-1, n}) if 0 <= k <= n]
mo = mf = mof = 0.0; worst = None; rounded_diff = []
for k, n in grid:
    o, f, s = O.clopper(k, n), F.clopper(k, n), sp(k, n)
    eo = max(abs(o[0]-s[0]), abs(o[1]-s[1])); ef = max(abs(f[0]-s[0]), abs(f[1]-s[1])); eof = max(abs(o[0]-f[0]), abs(o[1]-f[1]))
    if eo > mo: mo, worst = eo, (k, n, o, s)
    mf = max(mf, ef); mof = max(mof, eof)
    if (f"{o[0]:.3f}", f"{o[1]:.3f}") != (f"{f[0]:.3f}", f"{f[1]:.3f}"): rounded_diff.append((k, n, o, f))
print(f"small-n grid: {len(grid)} (k,n) pairs, n <= 1071")
print(f"  max |orig - scipy|  = {mo:.2e}  worst at k={worst[0]}, n={worst[1]}: orig={worst[2]}, scipy={worst[3]}")
print(f"  max |fixed - scipy| = {mf:.2e}")
print(f"  max |orig - fixed|  = {mof:.2e}")
print(f"  pairs whose printed 3-decimal interval differs orig vs fixed: {len(rounded_diff)}")
for r in rounded_diff: print("   ", r)
print("large n, fixed vs scipy (orig raises or is not evaluated):")
for k, n in ((520, 1072), (727, 1136), (7154, 11183), (9, 250), (1, 30), (1, 100000), (1, 10**6), (50000, 100000), (5*10**5, 10**6), (10**6, 10**6), (0, 10**6)):
    f, s = F.clopper(k, n), sp(k, n)
    try: o = O.clopper(k, n); os_ = f"({o[0]:.6g}, {o[1]:.6g})"
    except ZeroDivisionError: os_ = "ZeroDivisionError"
    print(f"  k={k:>7} n={n:>8}  orig={os_:<26} fixed=({f[0]:.6g}, {f[1]:.6g})  scipy=({s[0]:.6g}, {s[1]:.6g})  max|fixed-scipy|={max(abs(f[0]-s[0]), abs(f[1]-s[1])):.1e}")
