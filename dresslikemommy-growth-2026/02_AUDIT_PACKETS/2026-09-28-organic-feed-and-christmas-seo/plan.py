import json,re
from collections import Counter
d=json.load(open("variants_before.json"))
def size_of(v):
    for o in v["selectedOptions"]:
        if o["name"].lower()=="size": return o["value"].strip()
    return None
def age(s):
    t=s.lower()
    if re.search(r"\b(mother|father|adult|mom|dad|women|men)\b",t) or re.fullmatch(r"(xxs|xs|s|m|l|xl|xxl|2xl|3xl|4xl|5xl)",t) or "adult" in t: return "adult"
    m=re.search(r"(\d+)\s*(?:-\s*(\d+))?\s*months?",t)
    if m:
        hi=int(m.group(2) or m.group(1))
        return "newborn" if hi<=3 else ("infant" if hi<=12 else "toddler")
    m=re.search(r"(\d+)\s*cm",t)
    if m:
        cm=int(m.group(1)); return "infant" if cm<=80 else ("toddler" if cm<=110 else "kids")
    m=re.search(r"(\d+)\s*(?:-\s*(\d+))?\s*(?:years?|y\b|t\b)",t) or re.search(r"(\d+)\s*-\s*(\d+)t\b",t) or re.search(r"\b(\d+)t\b",t)
    if m:
        hi=int(m.group(2) or m.group(1)) if m.lastindex and m.lastindex>=2 and m.group(2) else int(m.group(1))
        return "toddler" if hi<=5 else "kids"
    return None
def gender(s):
    t=s.lower()
    if re.search(r"\bmother\b|\bgirl\b",t): return "female"
    if re.search(r"\bfather\b|\bboy\b",t): return "male"
    return None
plan=[];unknown=Counter();chg=Counter()
for p in d:
    for v in p["variants"]["nodes"]:
        s=size_of(v)
        if not s: unknown[("NOSIZE",p["handle"],v["title"])]+=1; continue
        a=age(s)
        if not a: unknown[s]+=1; continue
        cur=(v["ag"] or {}).get("value")
        g=gender(s); curg=(v["ge"] or {}).get("value")
        row={"product":p["id"],"handle":p["handle"],"variant":v["id"],"size":s,"age_before":cur,"age_after":a,"gender_before":curg,"gender_after":g}
        need_a = cur!=a; need_g = bool(g) and curg!=g
        if need_a or need_g:
            row["set_age"]=need_a; row["set_gender"]=need_g; plan.append(row)
            chg[(cur,a)]+=need_a
json.dump(plan,open("plan.json","w"),indent=0)
print("plan rows",len(plan),"age sets",sum(r["set_age"] for r in plan),"gender sets",sum(r["set_gender"] for r in plan))
print("age transitions",chg.most_common())
print("unknown",unknown.most_common(40))
