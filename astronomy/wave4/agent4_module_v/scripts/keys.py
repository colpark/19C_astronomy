import json,sys
def walk(o,p="",d=0):
    if d>6: return
    if isinstance(o,dict):
        for k,v in o.items(): walk(v,f"{p}.{k}",d+1)
    elif isinstance(o,list):
        print(f"{p}[] len={len(o)}")
        if o: walk(o[0],p+"[0]",d+1)
    else: print(f"{p} :{type(o).__name__}")
for f in sys.argv[1:]:
    print("==",f); walk(json.load(open(f)))
