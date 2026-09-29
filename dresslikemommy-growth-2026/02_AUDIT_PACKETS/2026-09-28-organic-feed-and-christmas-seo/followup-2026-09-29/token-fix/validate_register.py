import json,re,sys,os
sys.path.insert(0,'../feed')
from gql import gql
APPLY="--apply" in sys.argv
items={str(i["n"]):i for i in json.load(open("items.json"))}
tags=lambda h: re.findall(r"<\s*(/?[a-zA-Z0-9]+)",h)
res={"ok":0,"bad":[],"registered":0,"errors":[]}
for l in ["ar","pl","ko","ja","nl","hi"]:
    f=f"job_{l}/out.json"
    if not os.path.exists(f): res["bad"].append((l,"NO_OUTPUT")); continue
    out=json.load(open(f))
    want={n for n,i in items.items() if i["locale"]==l}
    if set(out)!=want: res["bad"].append((l,"keyset",len(set(out)^want))); continue
    for n,v in out.items():
        i=items[n]; e=[]
        if not v or not v.strip(): e.append("empty")
        if re.search(r"DLMTOK|__TOK",v): e.append("token")
        if "<" in i["en"] and tags(i["en"])!=tags(v): e.append("tags")
        for m in re.findall(r'[\w.+-]+@[\w-]+\.[\w.]+|https?://[^\s"<>]+|dresslikemommy\.com',i["en"]):
            if m not in v: e.append("lost:"+m)
        if e: res["bad"].append((l,n,i["type"],e)); continue
        res["ok"]+=1
        if APPLY:
            r=gql('''mutation($id:ID!,$t:[TranslationInput!]!){translationsRegister(resourceId:$id,translations:$t){userErrors{field message}}}''',{"id":i["id"],"t":[{"locale":l,"key":i["key"],"value":v,"translatableContentDigest":i["digest"]}]})["translationsRegister"]["userErrors"]
            if r: res["errors"].append((n,r))
            else: res["registered"]+=1
print(json.dumps(res,ensure_ascii=False)[:3000])
