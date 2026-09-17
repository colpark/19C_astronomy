import pandas as pd
REPO="/home/aid1/Documents/4_19C_astronomy/repo"
POSA=("SN ","SLSN","TDE","nova","LRN","LBV","ILRT","Ca-rich","Other","other")
def pool_E1():
    c=pd.read_csv(f"{REPO}/astronomy/agent1_supply_corpus/corpus.csv",dtype=str)
    def cls(t):
        t=str(t)
        if t.startswith(POSA): return "pos"
        if t.startswith(("CV","AGN")): return "neg"
        return "none"
    uc=c.assign(k=c["type"].map(cls)).groupby("object_cluster_1arcsec")["k"].first()
    p=pd.read_csv(f"{REPO}/astronomy/wave2/agent4_instrument/compositions/predictions/pred_E1_C.csv")
    p["cls"]=p["unit"].astype(str).map(uc)
    return p[p.cls.isin(["pos","neg"])]
