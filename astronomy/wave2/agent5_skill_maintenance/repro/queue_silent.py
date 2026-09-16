#!/usr/bin/env python3
"""Silent-error scan for the vendored clopper: where does its printed (3-decimal) interval
first differ from scipy.stats.beta.ppf, before any exception is raised?"""
import sys, importlib.util
from scipy.stats import beta
s = importlib.util.spec_from_file_location("o", sys.argv[1]); O = importlib.util.module_from_spec(s); s.loader.exec_module(O)
def sp(k, n): return (0.0 if k == 0 else beta.ppf(.025, k, n-k+1), 1.0 if k == n else beta.ppf(.975, k+1, n-k))
fmt = lambda x: (f"{x[0]:.3f}", f"{x[1]:.3f}")
first = None
for n in range(2, 1072):
    k = n // 2
    if fmt(O.clopper(k, n)) != fmt(sp(k, n)): first = n; break
print(f"k=n//2: first n whose printed interval differs from scipy = {first}; orig={fmt(O.clopper(first//2, first))} scipy={fmt(sp(first//2, first))}")
first = None
for n in (10**e for e in range(1, 7)):
    o, t = O.clopper(1, n), sp(1, n)
    print(f"k=1 n={n:>7}: orig hi={o[1]:.4g} scipy hi={t[1]:.4g} ratio={t[1]/o[1]:.3g}")
