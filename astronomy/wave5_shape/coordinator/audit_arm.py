import json,re,sys,hashlib
path=sys.argv[1]
hosts=r"alerce|fink|irsa|ipac|lasair|antares|wis-tns|\btns\b|arxiv|adsabs|simbad|\bned\b|https?://|curl |wget |requests\.|urllib"
paths=r"grader_private|grade\.py|data_cache|selection/|floor/|/r1/|tool_cards|ztf_bts_all|amendments\.md|order_of_operations"
tools_used={}; hits=[]; first=True; prompt_hash=None
for line in open(path,errors="replace"):
    line=line.strip()
    if not line: continue
    try: rec=json.loads(line)
    except: continue
    msg=rec.get("message",{}) or {}
    if first and rec.get("type")=="user" and isinstance(msg.get("content"),str):
        prompt_hash=hashlib.sha256(msg["content"].encode()).hexdigest(); first=False; continue
    content=msg.get("content")
    if not isinstance(content,list): continue
    for blk in content:
        if not isinstance(blk,dict): continue
        if blk.get("type")=="tool_use":
            name=blk.get("name"); tools_used[name]=tools_used.get(name,0)+1
            txt=json.dumps(blk.get("input",{}))
            for pat,lab in ((hosts,"HOST/NET"),(paths,"FORBIDDEN PATH")):
                for m in re.finditer(pat,txt,re.I):
                    s=max(0,m.start()-60); hits.append((lab,name,txt[s:m.end()+60].replace("\\n"," ")))
print("emitted prompt sha256:",prompt_hash)
print("tool calls:",tools_used,"total",sum(tools_used.values()))
print("hits in tool inputs:",len(hits))
for h in hits[:12]: print(" -",h[0],h[1],"|",h[2][:150])
