"""Module V property tests: patched queue.py (patch 01, scratch copy) and vendored power.py (unpatched).
Seeded: hypothesis derandomize=True (seed ledger: 'hypothesis derandomize'); random grid seed 20260917."""
import sys, os, math, csv, json, subprocess, tempfile, random, importlib.util
import pytest
from hypothesis import given, settings, strategies as st, HealthCheck
from scipy.stats import beta
HERE=os.path.dirname(os.path.abspath(__file__))
SCR=os.path.join(HERE,"scratch/fm-advantage-benchmark/scripts")
VEND=os.path.join(HERE,"../../../../fm-advantage-benchmark/scripts/power.py")
spec=importlib.util.spec_from_file_location("queue_patched",os.path.join(SCR,"queue.py")); Q=importlib.util.module_from_spec(spec); spec.loader.exec_module(Q)
PY=sys.executable
S=settings(derandomize=True,max_examples=300,deadline=None,suppress_health_check=list(HealthCheck))
kn=st.integers(1,10**6).flatmap(lambda n: st.tuples(st.integers(0,n),st.just(n)))
# ---------- queue.py (patched) ----------
@S
@given(kn)
def test_interval_contains_point(t):
    k,n=t; lo,hi=Q.clopper(k,n)
    assert 0.0<=lo<=k/n+1e-12 and k/n-1e-12<=hi<=1.0
@S
@given(st.integers(0,2000),st.integers(1,5000))
def test_monotone_in_n(k,dn):
    n=max(k,1)
    lo1,hi1=Q.clopper(k,n); lo2,hi2=Q.clopper(k,n+dn)
    assert hi2<=hi1+1e-12 and lo2<=lo1+1e-12
@S
@given(kn)
def test_agrees_with_scipy_beta_ppf(t):
    k,n=t; lo,hi=Q.clopper(k,n)
    slo=0.0 if k==0 else beta.ppf(0.025,k,n-k+1); shi=1.0 if k==n else beta.ppf(0.975,k+1,n-k)
    assert abs(lo-slo)<=1e-9+1e-7*slo and abs(hi-shi)<=1e-9+1e-7*shi
@pytest.mark.parametrize("n",[1,2,1071,1072,1073,10**4,10**5,10**6])
def test_no_crash_large_n(n):
    for k in (0,1,n//2,n-1,n):
        if 0<=k<=n: lo,hi=Q.clopper(k,n); assert math.isfinite(lo) and math.isfinite(hi)
def test_queue_refuses_non_nesting_counts():
    r=subprocess.run([PY,os.path.join(SCR,"queue.py"),"--counted","5","--passed","3","--survivors","4","--target","10"],capture_output=True,text=True)
    assert r.returncode!=0 and "nest" in (r.stderr+r.stdout)
def test_unpatched_queue_crashes_at_1072_control():
    # must-fire control: the vendored unpatched beta_inv raised ZeroDivisionError from n=1072 (patch 01 cause)
    spec=importlib.util.spec_from_file_location("queue_vendored",os.path.join(HERE,"../../../../fm-advantage-benchmark/scripts/queue.py")); V=importlib.util.module_from_spec(spec); spec.loader.exec_module(V)
    with pytest.raises(ZeroDivisionError): V.clopper(536,1072)
# ---------- power.py (vendored, unpatched) ----------
Z=1.9600+0.8416
def cols_with_sd(n,sd,rng):
    z=[rng.gauss(0,1) for _ in range(n)]; m=sum(z)/n; s=math.sqrt(sum((x-m)**2 for x in z)/(n-1))
    d=[sd*(x-m)/s for x in z]; a=[rng.random() for _ in range(n)]; b=[x-y for x,y in zip(a,d)]
    return a,b
def run_power(a,b,delta,extra=None):
    fd,p=tempfile.mkstemp(suffix=".csv"); os.close(fd)
    with open(p,"w",newline="") as fh:
        w=csv.writer(fh); w.writerow(["a","b"]); w.writerows(zip(a,b))
    r=subprocess.run([PY,VEND,"--scores",p,"--col-a","a","--col-b","b","--k","8","--candidates-per-item","46.41","--delta",str(delta)]+(extra or []),capture_output=True,text=True)
    os.unlink(p)
    out=r.stdout[:r.stdout.rfind("}")+1]
    return r.returncode,(json.loads(out) if out else None),r
GRID=random.Random(20260917)
@pytest.mark.parametrize("i",range(12))
def test_mde_scales_inverse_sqrt_n(i):
    sd=GRID.uniform(0.01,0.8); n=GRID.randint(10,400); rng=random.Random(1000+i)
    _,r1,_=run_power(*cols_with_sd(n,sd,rng),0.05); _,r4,_=run_power(*cols_with_sd(4*n,sd,rng),0.05)
    # amended after run 1: power.py rounds mde to 6 dp, so compare on the absolute scale with a rounding allowance
    assert abs(r1["mde"]-Z*sd/math.sqrt(n))<=2e-6 and abs(r4["mde"]-r1["mde"]/2)<=1.5e-6
@pytest.mark.parametrize("i",range(12))
def test_nmin_consistent_with_mde(i):
    sd=GRID.uniform(0.02,0.8); n=GRID.randint(20,300); delta=GRID.choice([0.018,0.05,0.1]); rng=random.Random(2000+i)
    _,r,_=run_power(*cols_with_sd(n,sd,rng),delta)
    nm=r["n_min"]; s=r["sigma_d"]
    assert Z*s/math.sqrt(nm)<=delta*(1+1e-5) and (nm==1 or Z*s/math.sqrt(nm-1)>delta*(1-1e-5))
def test_mde_decreases_with_n_one_seed():
    rng=random.Random(7); ms=[run_power(*cols_with_sd(n,0.3,rng),0.05)[1]["mde"] for n in (25,100,400,1600)]
    assert all(x>y for x,y in zip(ms,ms[1:]))
def test_power_refuses_empty_file():
    fd,p=tempfile.mkstemp(suffix=".csv"); os.close(fd); open(p,"w").write("a,b\n")
    r=subprocess.run([PY,VEND,"--scores",p,"--col-a","a","--col-b","b","--k","8","--candidates-per-item","46","--delta","0.05"],capture_output=True,text=True); os.unlink(p)
    assert r.returncode!=0 and "empty" in r.stderr
def test_power_refuses_missing_column():
    fd,p=tempfile.mkstemp(suffix=".csv"); os.close(fd); open(p,"w").write("a,b\n1,2\n3,4\n")
    r=subprocess.run([PY,VEND,"--scores",p,"--col-a","a","--col-b","c","--k","8","--candidates-per-item","46","--delta","0.05"],capture_output=True,text=True); os.unlink(p)
    assert r.returncode!=0 and "not in" in r.stderr
def test_power_refuses_mismatched_columns_blank_cell():
    fd,p=tempfile.mkstemp(suffix=".csv"); os.close(fd); open(p,"w").write("a,b\n1,2\n3,\n5,6\n")
    r=subprocess.run([PY,VEND,"--scores",p,"--col-a","a","--col-b","b","--k","8","--candidates-per-item","46","--delta","0.05"],capture_output=True,text=True); os.unlink(p)
    assert r.returncode!=0 and "Missing is not zero" in r.stderr
def test_power_refuses_single_unit():
    fd,p=tempfile.mkstemp(suffix=".csv"); os.close(fd); open(p,"w").write("a,b\n1,2\n")
    r=subprocess.run([PY,VEND,"--scores",p,"--col-a","a","--col-b","b","--k","8","--candidates-per-item","46","--delta","0.05"],capture_output=True,text=True); os.unlink(p)
    assert r.returncode!=0 and "two units" in r.stderr
def test_power_ragged_row_is_refused_not_silently_paired():
    # mismatched column lengths are only expressible as a short row; csv.DictReader fills None, power.py calls .strip() on None
    fd,p=tempfile.mkstemp(suffix=".csv"); os.close(fd); open(p,"w").write("a,b\n1,2\n3\n5,6\n")
    r=subprocess.run([PY,VEND,"--scores",p,"--col-a","a","--col-b","b","--k","8","--candidates-per-item","46","--delta","0.05"],capture_output=True,text=True); os.unlink(p)
    assert r.returncode!=0 and "Traceback" not in r.stderr, r.stderr[-300:]
def test_power_large_n_no_crash():
    rng=random.Random(11); n=10**6
    a=[rng.random() for _ in range(n)]; b=[rng.random() for _ in range(n)]
    code,r,_=run_power(a,b,0.05); assert r is not None and math.isfinite(r["mde"]) and code in (0,2)
