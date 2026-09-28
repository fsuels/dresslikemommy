import json,re,sys,os
sys.path.insert(0,'../feed')
from gql import gql
src=json.load(open("source.json"))
APPLY="--apply" in sys.argv
locs=[a for a in sys.argv[1:] if not a.startswith("--")]
tags=lambda h: re.findall(r"<\s*(/?[a-zA-Z0-9]+)",h)
hrefs=lambda h: re.findall(r'href="([^"]+)"',h)
nums=lambda s: sorted(re.findall(r"\d+(?:[.,]\d+)?",re.sub(r'href="[^"]+"',"",s)))
report={}
for loc in locs:
    f=f"job_{loc}/out.json"
    if not os.path.exists(f): report[loc]="NO_OUTPUT"; continue
    try: out=json.load(open(f))
    except Exception as e: report[loc]=f"BAD_JSON {e}"; continue
    errs=[]
    for h,a in src.items():
        o=out.get(h) or {}
        for k,fv in a["fields"].items():
            if k=="handle": continue
            s=fv["value"]; t=o.get(k)
            if not t or not t.strip(): errs.append(f"{h}.{k} missing"); continue
            if tags(s)!=tags(t): errs.append(f"{h}.{k} tag sequence differs")
            if hrefs(s)!=hrefs(t): errs.append(f"{h}.{k} hrefs differ")
            ns,nt=nums(s),nums(t)
            if [n for n in ns if n not in nt]: errs.append(f"{h}.{k} numbers missing {sorted(set(n for n in ns if n not in nt))[:6]}")
            if t.strip()==s.strip() and k!="handle": errs.append(f"{h}.{k} untranslated")
            if k=="meta_description" and len(t)>170: errs.append(f"{h}.meta_description {len(t)} chars")
            if k=="title" and len(t)>80: errs.append(f"{h}.title {len(t)} chars")
    report[loc]=errs or "OK"
    if APPLY and not errs:
        res=[]
        for h,a in src.items():
            tr=[{"locale":loc,"key":k,"value":out[h][k],"translatableContentDigest":fv["digest"]} for k,fv in a["fields"].items() if k!="handle"]
            r=gql('''mutation($id:ID!,$t:[TranslationInput!]!){translationsRegister(resourceId:$id,translations:$t){translations{key locale} userErrors{field message}}}''',{"id":a["id"],"t":tr})["translationsRegister"]
            res.append((h,len(r["translations"] or []),r["userErrors"]))
        report[loc]={"registered":res}
print(json.dumps(report,ensure_ascii=False,indent=1))
json.dump(report,open("report_"+("apply" if APPLY else "check")+".json","a"),ensure_ascii=False); open("report_"+("apply" if APPLY else "check")+".json","a").write("\n")
