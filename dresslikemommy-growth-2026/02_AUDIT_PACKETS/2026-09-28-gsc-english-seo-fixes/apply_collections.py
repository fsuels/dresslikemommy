"""Apply collection/product SEO changes from plan.py. Writes receipts.json."""
import json, sys
sys.path.insert(0, "/private/tmp/claude-501/-Users-fsuels-Projects-dresslikemommy/4297430a-559f-4c33-8ff6-032d877466c9/scratchpad")
from gql import gql
import plan

R = {"collections": {}, "thanksgiving": {}, "products": {}}
def ue(res, key):
    errs = res[key]["userErrors"]
    if errs: raise SystemExit(f"{key}: {errs}")
    return res[key]

# 1. Admin SEO for existing collections (theme renders EN copy; admin keeps sources consistent).
for h, c in plan.COLLECTIONS.items():
    if h == "mommy-and-me" or "--skip-step1" in sys.argv:
        continue  # theme already forces the target title/meta; no change
    col = gql('query($h:String!){collectionByHandle(handle:$h){id seo{title description} descriptionHtml}}', {"h": h})["collectionByHandle"]
    R["collections"][h] = {"id": col["id"], "before": col}
    out = ue(gql('mutation($i:CollectionInput!){collectionUpdate(input:$i){collection{id seo{title description}} userErrors{field message}}}',
        {"i": {"id": col["id"], "seo": {"title": c["seo_title"], "description": c["seo_description"]}, "descriptionHtml": c["body"]}}), "collectionUpdate")
    R["collections"][h]["after"] = out["collection"]

# 2. Thanksgiving collection.
t = plan.THANKSGIVING
exist = gql('query($h:String!){collectionByHandle(handle:$h){id}}', {"h": t["handle"]})["collectionByHandle"]
assert exist is None, "thanksgiving collection already exists"
ids = []
for h in t["members"]:
    p = gql('query($h:String!){productByHandle(handle:$h){id status}}', {"h": h})["productByHandle"]
    assert p and p["status"] == "ACTIVE", h
    ids.append(p["id"])
col = ue(gql('mutation($i:CollectionInput!){collectionCreate(input:$i){collection{id handle} userErrors{field message}}}',
    {"i": {"title": t["title"], "handle": t["handle"], "descriptionHtml": t["body"], "sortOrder": "MANUAL",
           "seo": {"title": t["seo_title"], "description": t["seo_description"]}, "products": ids}}), "collectionCreate")["collection"]
R["thanksgiving"]["collection"] = col
pubs = gql('{publications(first:20){nodes{id name}}}')["publications"]["nodes"]
os_pub = [p["id"] for p in pubs if p["name"] == "Online Store"]
ue(gql('mutation($id:ID!,$in:[PublicationInput!]!){publishablePublish(id:$id,input:$in){userErrors{field message}}}',
    {"id": col["id"], "in": [{"publicationId": os_pub[0]}]}), "publishablePublish")
R["thanksgiving"]["published_to"] = os_pub

# 3. Product SEO title.
for h, title in plan.PRODUCT_SEO_TITLES.items():
    p = gql('query($h:String!){productByHandle(handle:$h){id seo{title description}}}', {"h": h})["productByHandle"]
    R["products"][h] = {"id": p["id"], "before": p["seo"]}
    out = ue(gql('mutation($p:ProductUpdateInput!){productUpdate(product:$p){product{seo{title description}} userErrors{field message}}}',
        {"p": {"id": p["id"], "seo": {"title": title, "description": p["seo"]["description"]}}}), "productUpdate")
    R["products"][h]["after"] = out["product"]["seo"]

json.dump(R, open("receipts_collections.json", "w"), indent=1)
print(json.dumps({k: (list(v) if isinstance(v, dict) else v) for k, v in R.items()}))
