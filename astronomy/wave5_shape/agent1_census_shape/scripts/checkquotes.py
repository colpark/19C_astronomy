import json,sys,re
# usage: checkquotes.py notes.json ; checks every "quote" appears (whitespace-collapsed) within the cited layout line range (+-3 lines)
base="/home/aid1/Documents/4_19C_astronomy/repo/astronomy/wave5_shape/agent1_census_shape/sources/"
bad=0;tot=0
def norm(s): return re.sub(r"\s+"," ",s).strip()
for path in sys.argv[1:]:
    o=json.load(open(path)); sid=o["seed_id"]
    lines=open(base+sid+".layout.txt").read().replace("\f","").split("\n")
    items=[]
    for k in ("branches","conclusions_depth","facts_for_shape","item_template_evidence"):
        items+= [(k,x) for x in o.get(k,[])]
    for ep in o.get("episodes",[]):
        items+= [("chain",x) for x in ep.get("chain",[]) if x.get("quote")]
    for k,x in items:
        q=x.get("quote"); loc=x.get("locator","")
        m=re.search(r"L(\d+)(?:-(\d+))?",loc)
        if not q or not m: print("MISSING quote/locator",path,k,x.get("id")); bad+=1; continue
        tot+=1
        a=int(m.group(1)); b=int(m.group(2) or a)
        seg=[norm(l) for l in lines[max(0,a-4):b+3]]
        # allow a quote to be matched inside a single line or across the full joined segment
        if not any(norm(q) in s for s in seg) and norm(q) not in " ".join(seg):
            print("NOTFOUND",path,k,x.get("id"),loc,repr(q)); bad+=1
print(f"checked {tot} quotes, {bad} failures")
sys.exit(1 if bad else 0)
