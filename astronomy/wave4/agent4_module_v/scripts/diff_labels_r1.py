import sys,os,csv,json,re,collections
sys.path.insert(0,os.path.dirname(__file__))
import labels_lib_r1 as L
A=L.A
det={r["ZTFID"]:r for r in csv.DictReader(open(f"{A}/wave2/agent2_label_source/label_basis_per_object_detail.csv"))}
tb=json.load(open(f"{A}/wave3/agent2_measured_labels/out/track1_bound.json"))
newL=set(tb["new_L_ids"]); newX=set(tb["new_excl_ids"])
diff=collections.defaultdict(list)
for r in L.rows:
    z=r["ZTFID"]; cat,m,why=L.categorize(r)
    p=det[z]["category"].split(" ")[0]
    if z in newL: p="MODEL_ANNOTATION"
    if z in newX: p="MEASURED"
    if p!=cat: diff[(cat,why,p)].append((z,r["IAUID"],r["type"],det[z]["fetch_status"],det[z]["evidence"][:160]))
for k,v in diff.items(): print(k,len(v)); [print("   ",x) for x in v[:6]]
