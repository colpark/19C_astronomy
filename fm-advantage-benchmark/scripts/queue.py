#!/usr/bin/env python3
"""Derive the queue size from observed yield. Never assume it.

The source record's end-to-end yield was 1 of 6, whose exact 95% interval runs
from 0.004 to 0.641. That licenses a queue anywhere from 2 to unbounded, so a
queue planned from six candidates is planned against noise. Re-derive after
every batch. Counting is free.

Three escapes, printed explicitly:
  ESCAPE target   survivor count reached S
  ESCAPE supply   optimistic yield on remaining supply cannot reach S
  PROVISIONAL     spread too wide to commit paid-tier effort

Usage
-----
    python queue.py --counted 40 --passed 13 --survivors 7 --target 10 --remaining 200
"""
import argparse, math

def beta_inv(p, a, b, steps=3000):
    def ibeta(m):
        s = sum(((i + .5) * m / steps) ** (a - 1) * (1 - (i + .5) * m / steps) ** (b - 1)
                for i in range(steps)) * m / steps
        t = sum(((i + .5) / steps) ** (a - 1) * (1 - (i + .5) / steps) ** (b - 1)
                for i in range(steps)) / steps
        return s / t
    lo, hi = 0.0, 1.0
    for _ in range(60):
        m = (lo + hi) / 2
        lo, hi = (m, hi) if ibeta(m) < p else (lo, m)
    return (lo + hi) / 2

def clopper(k, n, alpha=0.05):
    return (0.0 if k == 0 else beta_inv(alpha / 2, k, n - k + 1),
            1.0 if k == n else beta_inv(1 - alpha / 2, k + 1, n - k))

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--counted", type=int, required=True)
    p.add_argument("--passed", type=int, required=True)
    p.add_argument("--survivors", type=int, required=True)
    p.add_argument("--target", type=int, required=True)
    p.add_argument("--remaining", type=int, default=None)
    p.add_argument("--spread-limit", type=float, default=10.0)
    a = p.parse_args()

    if not (a.survivors <= a.passed <= a.counted):
        raise SystemExit("counts must nest: survivors <= passed <= counted")

    lo, hi = clopper(a.survivors, a.counted)
    point = a.survivors / a.counted
    print(f"observed      {a.survivors}/{a.counted} = {point:.3f}")
    print(f"95% interval  [{lo:.3f}, {hi:.3f}]")

    need = a.target - a.survivors
    if need <= 0:
        print(f"\nESCAPE target. S={a.target} reached. Stop enumerating.")
        return 0
    if point == 0:
        print(f"\nPROVISIONAL. Zero survivors so far, no point estimate exists.")
        print(f"Optimistic queue for {need}: {math.ceil(need / hi)}. Count that many, then re-derive.")
        return 1

    q_opt, q_pt = math.ceil(need / hi), math.ceil(need / point)
    q_pess = math.ceil(need / lo) if lo > 0 else None
    print(f"\nqueue for {need} more survivor(s)")
    print(f"  optimistic    {q_opt}")
    print(f"  point         {q_pt}")
    print(f"  pessimistic   {q_pess if q_pess else 'unbounded, zero yield not excluded'}")

    if a.remaining is not None:
        best = a.remaining * hi
        print(f"\nsupply remaining {a.remaining}, optimistic yield {best:.1f}")
        if best < need:
            print(f"ESCAPE supply. Even optimistically the pool cannot reach S={a.target}.")
            print("Close the domain and write the finding.")
            return 3

    spread = (q_pess / q_pt) if q_pess else float("inf")
    if spread > a.spread_limit:
        s = f"{spread:.0f}x" if q_pess else "unbounded"
        print(f"\nPROVISIONAL. Pessimistic queue is {s} the point estimate.")
        print(f"Enumerate {q_pt} against the point estimate, then re-derive.")
        print("Do not commit paid-tier effort on this number.")
        return 1
    print(f"\nLICENSED. Spread {spread:.1f}x. Plan against the point estimate.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
