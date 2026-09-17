import sys, os, re, gzip, csv, html as H, collections
sys.path.insert(0, os.path.dirname(__file__)); from common import *
A=f"{REPO}/astronomy"
RAW=f"{A}/data/raw/ztf_bts_all_2026-09-16.csv"; assert sha(RAW)=="61415979b75f96bcf2532439109b35f923c5fa1aadfacc5d6013235187ebe570"
DEF=f"{A}/wave2/agent2_label_source/definitions_FROZEN.md"; assert sha(DEF)=="4f89ff6718a14ad4e45a6d33d6bde848448ba6a66d895bd970330efe397b37cf"
LOGS=[(f"{A}/wave2/agent2_label_source/sources/tns_captures","w2"),(f"{A}/wave3/agent2_measured_labels/out/track1_captures","w3")]
E2NAMES={"2021ijb","2023tyk","2023vcz","2023uxa","2023uti","2023vcx","2023uty","2023vtp","2023vpd","2023vip","2023vwz","2023wts","2023xms","2023xhc","2023xkq"}
def cells(tr):
    return {m.group(1):H.unescape(re.sub(r"<[^>]+>"," ",m.group(2))).replace("\xa0"," ") for m in re.finditer(r'<td[^>]*class="cell-([a-z_A-Z]+)[^"]*"[^>]*>(.*?)</td>',tr,flags=re.S)}
def section(s,idname):
    i=s.find(f'id="{idname}"')
    if i<0: return None
    ends=[e for e in (s.find("</fieldset>",i),s.find("</details>",i)) if e>0]
    return s[i:min(ends)] if ends else s[i:]
def parse_page(path, name):
    s=gzip.open(path,"rt",errors="replace").read()
    t=re.search(r"<title>(.*?)</title>",s,flags=re.S); title=t.group(1) if t else ""
    title_ok= name in title.replace(" ","")
    cs=section(s,"class-fieldset")
    reps=[]
    if cs:
        tb=cs[cs.find("<tbody"):] if "<tbody" in cs else ""
        for tr in re.findall(r"<tr\b.*?</tr>",tb,flags=re.S):
            c=cells(tr)
            if "time_received" in c: reps.append(c)
    sp=section(s,"spectra-fieldset"); specs=[]
    if sp:
        tb=sp[sp.find("<tbody"):] if "<tbody" in sp else ""
        for tr in re.findall(r"<tr\b.*?</tr>",tb,flags=re.S):
            c=cells(tr)
            if "obsdate" in c: specs.append(c)
    return dict(valid=bool(title_ok and cs is not None),title_ok=title_ok,has_class=cs is not None,reports=reps,spectra=specs)
def norm(x):
    x=re.sub(r"\s+"," ",x.strip().lower())
    if x.endswith("-like"): x=x[:-5]
    return x.strip()
PAIRS={("sn ii","sn iip"),("sn ii","sn iil"),("sn iip","sn ii"),("sn ib/c","sn ibc")}
def match(bts,tns):
    b,t=norm(bts),norm(tns)
    return b==t or t.startswith(b+"-") or (b,t) in PAIRS
def model_of(classifier):
    c=classifier.lower()
    if "sniascore" in c: return "SNIascore"
    if "ccsnscore" in c: return "CCSNscore"
    if re.search(r"\b(bot|robot|automatic|automated|auto)\b",c): return "other-automated"
    return None
# evidence by tns name
ev={}; stat=collections.Counter()
for d,tag in LOGS:
    for l in open(f"{d}/fetch_log.jsonl"):
        r=json.loads(l); name=re.sub(r"^(SN|AT|TDE|FRB)\s*","",r["IAUID"]).strip()
        stat[(tag,r["final"])]+=1
        if r["final"]!="ok" or not r.get("file"): 
            ev.setdefault(name,{"src":tag,"final":r["final"]}); continue
        fp=f"{d}/html/{os.path.basename(r['file'])}"
        if not os.path.exists(fp): ev[name]={"src":tag,"final":"missing_file"}; stat[(tag,"missing_file")]+=1; continue
        if sha_gz_ok:=True: pass
        p=parse_page(fp,name); p.update(src=tag,final="ok",capture=r.get("capture_ts"))
        if name in ev and ev[name].get("final")=="ok" and ev[name]["capture"]>=p["capture"]: continue
        ev[name]=p
rows=[r for r in csv.DictReader(open(RAW)) if r["type"].strip()!="-"]
def categorize(r, precedence="marker_first", spec_rule="table"):
    name=re.sub(r"^(SN|AT|TDE|FRB)\s*","",r["IAUID"]).strip()
    e=ev.get(name)
    if not e or e.get("final")!="ok" or not e["valid"]: return "UNRESOLVED",None,"no_valid_E1"
    if not e["reports"]: return "UNRESOLVED",None,"no_reports"
    R=max(e["reports"],key=lambda c:c["time_received"].strip())
    if not match(r["type"],R.get("type","")): return "UNRESOLVED",None,"mismatch"
    m=model_of(R.get("classifier_name",""))
    tr=R["time_received"].strip()[:19]
    if spec_rule=="table": has_spec=any(c["obsdate"].strip()[:19]<=tr for c in e["spectra"] if c["obsdate"].strip())
    else:
        cnt=re.sub(r"\D","",R.get("spectra","")); has_spec=(int(cnt)>0 if cnt else False) or any(c["obsdate"].strip()[:19]<=tr and c.get("source_group_name","").strip()==R.get("source_group_name","").strip() for c in e["spectra"])
    if precedence=="marker_first":
        if m: return "MODEL_ANNOTATION",m,"marker"
        return ("MEASURED",None,"human+spectrum") if has_spec else ("PHOTOMETRIC_ONLY",None,"human,no spectrum<=report")
    else:
        if not has_spec: return "PHOTOMETRIC_ONLY",m,"no spectrum<=report"
        return ("MODEL_ANNOTATION",m,"marker") if m else ("MEASURED",None,"human+spectrum")
# E4 explorer capture pre-2021-04-15
E4P=f"{A}/wave2/agent2_label_source/sources/bts_explorer_captures/wayback_bts_explorer_20210128125321.html"
s=open(E4P,errors="replace").read(); e4=set()
for tr in re.findall(r"<tr\b.*?</tr>",s,flags=re.S):
    c=[H.unescape(re.sub(r"<[^>]+>","",x)).replace("\xa0"," ").strip() for x in re.findall(r"<td\b.*?</td>",tr,flags=re.S)]
    if len(c)>=15 and re.fullmatch(r"ZTF\d{2}[a-z]{7}",c[0]) and c[11]=="SN Ia": e4.add(c[0])
def compute(precedence="marker_first", spec_rule="table", sources=("w2","w3"), key="iau"):
    cats=collections.Counter(); reasons=collections.Counter(); L_strong=set(); L=set(); excl=set(); excl_noE5=set(); P=[]
    for r in rows:
        name=re.sub(r"^(SN|AT|TDE|FRB)\s*","",r["IAUID"]).strip()
        e=ev.get(name)
        if e and e.get("src") not in sources: cat,m,why="UNRESOLVED",None,"source_excluded"
        else: cat,m,why=categorize(r,precedence,spec_rule)
        cats[cat]+=1; reasons[why]+=1
        if r["type"]=="SN Ia":
            P.append(r["ZTFID"])
            if cat=="MODEL_ANNOTATION" and m=="SNIascore": L_strong.add(r["ZTFID"]); L.add(r["ZTFID"])
            contradiction = cat in ("MEASURED","PHOTOMETRIC_ONLY") or (cat=="MODEL_ANNOTATION" and m!="SNIascore")
            if name in E2NAMES and not contradiction: L.add(r["ZTFID"])
            x=contradiction or r["ZTFID"] in e4
            try: e5=float(r["peakt"])<1259.5
            except: e5=False
            if x or e5: excl.add(r["ZTFID"])
            if x: excl_noE5.add(r["ZTFID"])
    U=len(P)-len(excl); UnoE5=len(P)-len(excl_noE5)
    return dict(population=len(rows),categories=dict(cats),reasons=dict(reasons),P_plain_SN_Ia=len(P),L_strong=len(L_strong),L=len(L),U=U,U_noE5=UnoE5,
                bound_wave2_rule=[max(len(L),0),min(U,3131)],bound_wave3_rule=[max(803,len(L)),min(2247,U)],E4_objects=len(e4))
