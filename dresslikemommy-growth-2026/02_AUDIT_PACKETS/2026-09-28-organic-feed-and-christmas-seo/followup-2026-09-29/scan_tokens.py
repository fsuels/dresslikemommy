import sys,json,re
sys.path.insert(0,'.')
from gql import gql
locs=['ar','cs','da','de','el','es','fi','fr','he','hi','it','ja','ko','nl','no','pl','pt-BR','ro','ru','sv']
types=sys.argv[1].split(",")
pat=re.compile(r"__DLM|DLMTOK|__TOK|\{\{\s*\d|\[\[\d")
hits=[]
for rt in types:
    for l in locs:
        c=None
        while True:
            d=gql('''query($c:String,$l:String!,$t:TranslatableResourceType!){translatableResources(first:200,after:$c,resourceType:$t){pageInfo{hasNextPage endCursor} nodes{resourceId translations(locale:$l){key value outdated}}}}''',{"c":c,"l":l,"t":rt})["translatableResources"]
            for n in d["nodes"]:
                for t in n["translations"]:
                    if t["value"] and pat.search(t["value"]): hits.append({"type":rt,"id":n["resourceId"],"locale":l,"key":t["key"],"snippet":t["value"][max(0,pat.search(t["value"]).start()-40):pat.search(t["value"]).start()+30]})
            if not d["pageInfo"]["hasNextPage"]: break
            c=d["pageInfo"]["endCursor"]
    print(rt,"done, hits so far",len(hits),flush=True)
json.dump(hits,open(f"token_hits_{'_'.join(types)}.json","w"),ensure_ascii=False,indent=1)
