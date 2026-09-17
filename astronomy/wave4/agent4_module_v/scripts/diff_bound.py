import sys,os,csv,json,re,collections
sys.path.insert(0,os.path.dirname(__file__))
import labels_lib_r1 as L
A=L.A
KEY=os.environ.get("KEY","iau")
det={r["ZTFID"]:r for r in csv.DictReader(open(f"{A}/wave2/agent2_label_source/label_basis_per_object_detail.csv"))}
# ZTFID keyed evidence: evidence only applies to the ZTFID fetched
fetched={}
for d,tag in L.LOGS:
    for l in open(f"{d}/fetch_log.jsonl"):
        r=json.loads(l); fetched[r["ZTFID"]]=tag
def cat(r, sources):
    name=re.sub(r"^(SN|AT|TDE|FRB)\s*","",r["IAUID"]).strip()
    if KEY=="ztfid" and r["ZTFID"] not in fetched:
        if L.FIX_E2 and name in L.E2NAMES and r["type"]=="SN Ia": return ("MODEL_ANNOTATION","SNIascore","E2_only")
        return ("UNRESOLVED",None,"not_fetched_this_ztfid")
    e=L.ev.get(name)
    if e and e.get("src") not in sources:
        if L.FIX_E2 and name in L.E2NAMES and r["type"]=="SN Ia": return ("MODEL_ANNOTATION","SNIascore","E2_only")
        return ("UNRESOLVED",None,"src_excluded")
    return L.categorize(r)
def bound(sources):
    cats=collections.Counter(); P=0; Lset=set(); ex={"E1":set(),"E4":set(),"E5":set()}; allx=set()
    for r in L.rows:
        c,m,why=cat(r,sources); cats[c]+=1
        if r["type"]!="SN Ia": continue
        P+=1; z=r["ZTFID"]
        if c=="MODEL_ANNOTATION" and m=="SNIascore": Lset.add(z)
        contra= c in ("MEASURED","PHOTOMETRIC_ONLY") or (c=="MODEL_ANNOTATION" and m!="SNIascore")
        if contra: ex["E1"].add(z)
        if z in L.e4: ex["E4"].add(z)
        try:
            if float(r["peakt"])<1259.5: ex["E5"].add(z)
        except: pass
    allx=ex["E1"]|ex["E4"]|ex["E5"]
    return dict(cats=dict(cats),P=P,L=len(Lset),U=P-len(allx),U_noE5=P-len(ex["E1"]|ex["E4"]),nE1=len(ex["E1"]),nE4=len(ex["E4"]),nE5=len(ex["E5"])),ex
w2,ex2=bound(("w2",)); w23,ex23=bound(("w2","w3"))
print("KEY",KEY,"w2only",w2); print("w2+w3",w23)
# compare E4/E5 flags with producer detail
pE4={z for z,d in det.items() if d["type"]=="SN Ia" and d["E4"]=="True"} if "type" in next(iter(det.values())) else {z for z,d in det.items() if d["class"]=="SN Ia" and d["E4"]=="True"}
pE5={z for z,d in det.items() if d["class"]=="SN Ia" and d["E5"]=="True"}
print("E4 mine",len(ex2["E4"]),"producer",len(pE4),"mine-prod",len(ex2["E4"]-pE4),"prod-mine",len(pE4-ex2["E4"]), list(pE4-ex2["E4"])[:5], list(ex2["E4"]-pE4)[:5])
print("E5 mine",len(ex2["E5"]),"producer",len(pE5),len(ex2["E5"]-pE5),len(pE5-ex2["E5"]))
# producer's wave2 U from detail: P minus objects with (E1 contradiction category) or E4 or E5
pE1={z for z,d in det.items() if d["class"]=="SN Ia" and (d["category"].startswith("MEASURED") or d["category"].startswith("PHOTOMETRIC") or (d["category"].startswith("MODEL") and d["model"]!="SNIascore"))}
P=sum(1 for d in det.values() if d["class"]=="SN Ia")
print("producer-detail-implied wave2 U:",P-len(pE1|pE4|pE5),"P",P,"E1",len(pE1),"E4",len(pE4),"E5",len(pE5))
tb=json.load(open(f"{A}/wave3/agent2_measured_labels/out/track1_bound.json")); newX=set(tb["new_excl_ids"])
print("w3 new exclusions already excluded by E4/E5 (producer rule says 'not already excluded'):",len(newX&(pE4|pE5)), "of",len(newX))
print("my w3 E1 exclusions new vs w2:",len(ex23["E1"]-ex2["E1"]),"of which not in E4|E5:",len((ex23["E1"]-ex2["E1"])-(ex2["E4"]|ex2["E5"])))
