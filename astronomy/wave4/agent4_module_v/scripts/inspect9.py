import sys,os,csv,json,re
sys.path.insert(0,os.path.dirname(__file__))
import labels_lib as L
det={r["ZTFID"]:r for r in csv.DictReader(open(f"{L.A}/wave2/agent2_label_source/label_basis_per_object_detail.csv"))}
ids=['ZTF21abhzboh','ZTF23aasopeh','ZTF18acaezsx','ZTF23aawwcuu','ZTF18aafdigb','ZTF23abjzkqu','ZTF23ablpfnb','ZTF23abnydbs','ZTF18aaeqjmc']
byz={r["ZTFID"]:r for r in L.rows}
for z in ids:
    r=byz[z]; name=re.sub(r"^(SN|AT|TDE|FRB)\s*","",r["IAUID"]).strip(); e=L.ev.get(name)
    print(z,r["IAUID"],repr(r["type"]),L.categorize(r))
    if e and e.get("final")=="ok": print("  valid",e["valid"],"title_ok",e["title_ok"],"has_class",e["has_class"],"n_reports",len(e["reports"]),[ (c.get("time_received"),c.get("type"),c.get("classifier_name","")[:50]) for c in e["reports"]][:3])
    else: print("  ev",e)
    d=det[z]; print("  producer:",d["category"],d["model"],d["evidence"][:200],d["fetch_status"],d["e1_classifier"][:60],d["e1_report_time"],d["e1_capture"])
# wave3 measured: find the missing one
tb=json.load(open(f"{L.A}/wave3/agent2_measured_labels/out/track1_bound.json"))
newX=set(tb["new_excl_ids"]); 
mineM={r["ZTFID"] for r in L.rows if L.categorize(r)[0]=="MEASURED" and L.ev.get(re.sub(r"^(SN|AT|TDE|FRB)\s*","",r["IAUID"]).strip(),{}).get("src")=="w3"}
print("w3 excl not in mine MEASURED:",[(z,L.categorize(byz[z]),byz[z]["type"]) for z in newX-mineM][:5]); print("mine not in newX:",list(mineM-newX)[:5])
