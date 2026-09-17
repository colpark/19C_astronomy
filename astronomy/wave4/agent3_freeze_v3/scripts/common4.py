"""Wave-4 helpers: reuses the wave-3 canonical-hash method verbatim (imported, not copied)."""
import os, sys, datetime
W3S = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "wave3", "agent3_manifest_freeze", "scripts"))
sys.path.insert(0, W3S)
from common import canonical_bytes, canonical_sha, manifest_hash, rp, sha, load, ref, now, dump, HASH_METHOD, W2, W3, W2SHA, W3SHA, BANDS, BANDS_SHA, REPO  # noqa
OUT = "astronomy/wave4/agent3_freeze_v3"
W3OUT = "astronomy/wave3/agent3_manifest_freeze"
W4 = "astronomy/wave4/PANEL_BRIEF_WAVE4.md"
W4SHA = "8f10181154219048bed3e8fa973c35d71d3a038cc98323fde76f509363511b58"
V = "astronomy/wave4/agent4_module_v"
def log(step, text, paths=()):
    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    hs = [f"{p} sha256={sha(p)}" for p in paths]
    line = f"{ts} | {step} | {text}" + (" | " + "; ".join(hs) if hs else "")
    open(rp(f"{OUT}/order_of_operations.log"), "a").write(line + "\n"); print(line)
if __name__ == "__main__":
    log(sys.argv[1], sys.argv[2], sys.argv[3:])
