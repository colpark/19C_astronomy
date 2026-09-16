#!/usr/bin/env python3
"""Find the smallest n at which the vendored queue.py Clopper-Pearson crashes.
Imports the UNMODIFIED queue.py from a path given on the command line.
Failure condition read from the code: ibeta divides by t, where t is the midpoint
sum over [0,1] of x^(a-1)(1-x)^(b-1)/steps, independent of m. So clopper(k,n)
raises iff t(k, n-k+1)==0 (k>0) or t(k+1, n-k)==0 (k<n)."""
import sys, importlib.util
spec = importlib.util.spec_from_file_location("q", sys.argv[1]); q = importlib.util.module_from_spec(spec); spec.loader.exec_module(q)
STEPS = 3000
def t(a, b):
    return sum(((i + .5) / STEPS) ** (a - 1) * (1 - (i + .5) / STEPS) ** (b - 1) for i in range(STEPS)) / STEPS
def fails_t(k, n):
    return (k > 0 and t(k, n - k + 1) == 0.0) or (k < n and t(k + 1, n - k) == 0.0)
def fails_real(k, n):
    try: q.clopper(k, n); return False
    except ZeroDivisionError: return True

# 1. global: first n where ANY k fails. a+b = n+1 in both calls; t is smallest near a=b,
#    so screen k within +-3 of n/2, then confirm exhaustively over all k at n_min-1 and n_min.
n = 1000
while not any(fails_t(k, n) for k in range(max(0, n//2-3), min(n, n//2+3)+1)): n += 1
print(f"screen: first n with a failing k near n/2 = {n}")
lo = n - 1
bad_prev = [k for k in range(0, lo + 1) if fails_t(k, lo)]
bad_here = [k for k in range(0, n + 1) if fails_t(k, n)]
print(f"exhaustive all k at n={lo}: failing k = {bad_prev}")
print(f"exhaustive all k at n={n}: failing k = {bad_here}")
for k in bad_here:
    print(f"  confirm via queue.clopper({k},{n}) raises ZeroDivisionError: {fails_real(k, n)}")
if bad_here:
    print(f"  control clopper({bad_here[0]},{lo}) raises: {fails_real(bad_here[0], lo)}")

# 2. fixed-yield families: smallest n where clopper(round(r*n), n) raises (linear scan, confirmed with the real function)
for label, r in (("astronomy yield 7154/11183", 7154/11183), ("source-record yield 1/6", 1/6), ("yield 0.05", 0.05)):
    n = 1000
    while not fails_t(round(r * n), n): n += 1
    k = round(r * n)
    print(f"{label}: smallest failing n = {n} (k={k}); clopper raises {fails_real(k, n)}; "
          f"n-1 (k={round(r*(n-1))}) raises {fails_real(round(r*(n-1)), n-1)}")
