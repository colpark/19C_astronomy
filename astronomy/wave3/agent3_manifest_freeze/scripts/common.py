"""Shared helpers for the wave-3 agent-3 manifest freezes.

HASH METHOD (recorded in every manifest under hash_method):
  1. Load the manifest as a Python object.
  2. Set obj["frozen_hash"] = "".
  3. canonical = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
  4. frozen_hash = sha256(canonical).hexdigest()
The on-disk file is pretty-printed (indent=1); the pretty printing is not hashed.
Verify with: python scripts/verify_hash.py <manifest.json>
"""
import hashlib, json, os, datetime

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))

HASH_METHOD = ("sha256 over json.dumps(manifest with frozen_hash set to \"\", sort_keys=True, "
               "separators=(',', ':'), ensure_ascii=False) encoded UTF-8; file on disk is indent=1 "
               "pretty print, which is not hashed; verify with scripts/verify_hash.py")


def canonical_bytes(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def canonical_sha(obj):
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()


def manifest_hash(m):
    c = json.loads(json.dumps(m))
    c["frozen_hash"] = ""
    return canonical_sha(c)


def rp(path):
    return path if os.path.isabs(path) else os.path.join(REPO, path)


def sha(path):
    return hashlib.sha256(open(rp(path), "rb").read()).hexdigest()


def load(path):
    return json.load(open(rp(path)))


def ref(path, locator=None):
    d = {"path": path, "sha256": sha(path)}
    if locator:
        d["locator"] = locator
    return d


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def dump(obj, path):
    with open(rp(path), "w") as f:
        json.dump(obj, f, indent=1, ensure_ascii=False)
        f.write("\n")


W2 = "astronomy/wave2/PANEL_BRIEF_WAVE2.md"
W3 = "astronomy/wave3/PANEL_BRIEF_WAVE3.md"
W2SHA = "31a36617f0c6ae4179bb95ec134a6db7717ae7073f52f48b4272dde6a7a0f4eb"
W3SHA = "a618d9114ec7c937cf6115a67be188a16a69856949bde33bf6fa9c8e8981c4b6"
BANDS = "astronomy/wave2/agent1_rubin_bands/bands_FROZEN.md"
BANDS_SHA = "8825ef8048b733b66e12f31ce16e67270de171f52f20f40ca8f21e5780e500d2"
OUT = "astronomy/wave3/agent3_manifest_freeze"
