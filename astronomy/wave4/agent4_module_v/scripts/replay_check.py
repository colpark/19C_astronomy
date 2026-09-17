import sys,os,json
sys.path.insert(0,os.path.dirname(__file__))
src=open(os.path.join(os.path.dirname(__file__),"compare.py")).read().split("recs=[]")[0]
exec(src)   # imports cmp_num only (no records built)
cases=[("V-01","must_fire",cmp_num("O_merged",1938669,1937669,"int")),
       ("V-02","must_not_fire",cmp_num("sigma_d",0.08977815630613491,0.0897781114170792,"float_stat")),
       ("V-03","must_fire",cmp_num("P_lower_tail",6.6e-146,5.199601375735901e-146,"log10p")),
       ("V-04","must_not_fire",cmp_num("ci95[1]",0.6221,0.6242,"ci"))]
out=[]
for cid,pol,r in cases:
    fired = r["verdict"]=="DISCREPANCY"
    out.append({"case_id":cid,"polarity":pol,"verdict":r["verdict"],"fired":fired,"pass": fired==(pol=="must_fire"),"comparison":r})
json.dump(out,open(os.path.join(VD,"replay_check_results.json"),"w"),indent=1,default=str)
for o in out: print(o["case_id"],o["polarity"],o["verdict"],"PASS" if o["pass"] else "FAIL")
print("verdict function ARMED" if all(o["pass"] for o in out) else "NOT ARMED")
