import json,sys,time
sys.path.insert(0,'.')
from gql import gql
pl=[r for r in json.load(open("plan.json")) if not (r["age_before"] and r["set_age"])]
mf=[]
for r in pl:
    if r["set_age"]: mf.append({"ownerId":r["variant"],"namespace":"mm-google-shopping","key":"age_group","type":"single_line_text_field","value":r["age_after"]})
    if r["set_gender"]: mf.append({"ownerId":r["variant"],"namespace":"mm-google-shopping","key":"gender","type":"single_line_text_field","value":r["gender_after"]})
print("metafields",len(mf))
M='''mutation($m:[MetafieldsSetInput!]!){metafieldsSet(metafields:$m){metafields{id} userErrors{field message code}}}'''
errs=[];ok=0
for i in range(0,len(mf),25):
    b=mf[i:i+25]
    r=gql(M,{"m":b})["metafieldsSet"]
    if r["userErrors"]: errs.append({"batch":i,"errors":r["userErrors"]})
    ok+=len(r["metafields"] or [])
    time.sleep(0.25)
json.dump({"planned":len(mf),"written":ok,"errors":errs},open("apply_receipt.json","w"),indent=1)
print("written",ok,"error batches",len(errs))
