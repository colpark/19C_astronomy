import sys,os,csv,json,re,collections
sys.path.insert(0,os.path.dirname(__file__))
import labels_lib as L
A=L.A
det={r["ZTFID"]:r for r in csv.DictReader(open(f"{A}/wave2/agent2_label_source/label_basis_per_object_detail.csv"))}
tb=json.load(open(f"{A}/wave3/agent2_measured_labels/out/track1_bound.json"))
newL=set(tb["new_L_ids"]); newX=set(tb["new_excl_ids"])
print({k:v for k,v in tb.items() if not k.endswith("_ids")})
mine={}
for r in L.rows:
    mine[r["ZTFID"]]=L.categorize(r)
pc=collections.Counter(); ex=collections.defaultdict(list)
for z,(cat,m,why) in mine.items():
    pcat=det[z]["category"] if z in det else "ABSENT"
    pc[(cat,pcat)]+=1
    if not pcat.startswith(cat): ex[(cat,pcat)].append(z)
for k,v in pc.items(): print(k,v)
for k,v in ex.items(): print(k,len(v),v[:6])
json.dump({str(k):v for k,v in ex.items()},open(f"{L.VD}/data_cache/label_diff_w2.json","w"),indent=1)
