from pathlib import Path
import json,re,html,collections
P=Path(__file__).parent
rows=json.loads((P/'template_body_worklist.json').read_text())['rows'];pairs={}
ALT=re.compile(r'\balt="(.*?)"(?=\s+(?:style|loading|width|height|data-[\w-]+)=|\s*/?>)',re.S)
for r in rows:
 s=ALT.findall(r['sourceValue']);t=ALT.findall(r['before']['value']);assert len(s)==len(t),(r['ledgerId'],len(s),len(t))
 for ss,tt in zip(s,t):pairs.setdefault((r['locale'],html.unescape(ss),html.unescape(tt)),[]).append(r['ledgerId'])
out=[{'i':i,'locale':loc,'source':s,'target':t,'ledgerIds':ids}for i,((loc,s,t),ids)in enumerate(pairs.items())]
(P/'alt_pairs_full.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(len(out),collections.Counter(x['locale']for x in out))
for x in out[:112]:
 if '"'in x['source']or'"'in x['target']:print(x)
