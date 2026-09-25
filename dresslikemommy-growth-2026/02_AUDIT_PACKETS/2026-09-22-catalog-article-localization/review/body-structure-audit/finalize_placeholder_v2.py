import json,re,hashlib
from pathlib import Path
H=Path(__file__).resolve().parent;sha=lambda s:hashlib.sha256(s.encode()).hexdigest()
d=json.loads((H/'placeholder_candidates_v1.json').read_text());inv=json.loads((H/'effective_body_inventory.json').read_text())['rows'];r=next(x for x in inv if x['productIndex']==134 and x['locale']=='ro');old='perfect ca imagine și liniștit capricios.<strong>\n  <li>';new='perfect ca imagine și liniștit capricios.</li>\n  <li>';v=r['expectedEffectiveBeforeValue'];assert v.count(old)==1;quote=re.findall(r'<li>.*?</li>',r['source'],re.S)[2];assert quote.endswith('</li>');value=v.replace(old,new,1);row={k:r[k] for k in ['productIndex','resourceId','locale','key','source','sourceDigest','sourceSHA256','before','rawBefore','rawFile','rawFileSHA256','onlineStoreUrl']};row.update(value=value,valueSHA256=sha(value),expectedBeforeValueSHA256=sha(v),beforeValueSHA256=sha(v),requiresFreshLiveSourceAndBeforeGuard=True,originalSourceDispositionHold=False,patches=[{'before':old,'after':new,'reason':'Source-paired list-item closing li was mistranslated to opening strong; retain all prose exactly.','sourceExactQuote':quote,'sourceListItemOrdinal':2}],reviewStatus='AUTHOR_COMPLETE_PENDING_INDEPENDENT_REVIEW',reason='Source-backed malformed closing list tag only; no prose edit.');d['rows'].append(row)
assert len(d['rows'])==88 and len({(x['resourceId'],x['locale'],x['key']) for x in d['rows']})==88
for x in d['rows']:
 for p in x['patches']:assert p['sourceExactQuote'] in x['source']
 check=x['before']['value']
 for p in x['patches']:
  assert check.count(p['before'])==1;check=check.replace(p['before'],p['after'],1)
 assert check==x['value']
 assert re.findall(r'<table\b.*?</table>',x['before']['value'],re.S)==re.findall(r'<table\b.*?</table>',x['value'],re.S)
 assert not any(m[0] not in x['source'] for m in re.finditer(r'[A-Za-z0-9_]*(?:QZ|XTOKEN|QX|TOKEN)[A-Za-z0-9_]*',x['value']))
(H/'placeholder_candidates_v2.json').write_text(json.dumps({'status':'FINAL88_AUTHOR_COMPLETE_PENDING_INDEPENDENT_REVIEW','rows':d['rows']},ensure_ascii=False,indent=2)+'\n');print(json.dumps({'rows':88,'sha256':sha((H/'placeholder_candidates_v2.json').read_text())}))
