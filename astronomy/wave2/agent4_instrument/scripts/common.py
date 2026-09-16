"""Shared helpers. calibration only, contamination FAIL on this cohort.
PRE-I1: graph edge R1->I1 unmet, escalated."""
import hashlib, os, sys
W = "/home/aid1/Documents/4_19C_astronomy/repo/astronomy/wave2/agent4_instrument"
CORPUS = "/home/aid1/Documents/4_19C_astronomy/repo/astronomy/agent1_supply_corpus/corpus.csv"
CORPUS_SHA = "b059acf0656ed79fc743944b560aa3fd358096963067d96e144850403c3d8442"
FROZEN_SHA = "b2f72948de0b39682ff8bc01c3c3f13f931a0a96966ede90c50466a9d045427c"
BANNER = "calibration only, contamination FAIL on this cohort | PRE-I1: graph edge R1->I1 unmet, escalated"


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for ch in iter(lambda: f.read(1 << 20), b""):
            h.update(ch)
    return h.hexdigest()


def check_frozen():
    got = sha256(os.path.join(W, "compositions_FROZEN.md"))
    if got != FROZEN_SHA:
        sys.exit(f"compositions_FROZEN.md hash {got} != frozen {FROZEN_SHA}. Abort.")
    if sha256(CORPUS) != CORPUS_SHA:
        sys.exit("corpus.csv hash mismatch. Abort.")


POSA_PREFIX = ("SN ", "SLSN", "TDE", "nova", "LRN", "LBV", "ILRT", "Ca-rich", "Other", "other")


def label_class(t):
    t = str(t)
    if t == "-":
        return "unlabeled"
    if t.startswith("CV") or t.startswith("AGN"):
        return "neg"
    if t.startswith(POSA_PREFIX):
        return "posA"
    return "unmapped"


def night(mjd):
    import numpy as np
    return np.floor(np.asarray(mjd, dtype=float) - 0.8333).astype(int)
