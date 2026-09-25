import json,re,runpy,hashlib,collections
from pathlib import Path
H=Path(__file__).resolve().parent
M=runpy.run_path(str(H/'mapping_draft.py'));groups=json.loads((H/'semantic_groups.json').read_text())['rows'];pairs=json.loads((H/'source_bound_pairs.json').read_text())['rows'];raw=json.loads((H.parent/'body-structure-audit/effective_body_inventory.json').read_text())['rows'];rawmap={(r['resourceId'],r['locale']):r for r in raw}
rows=[];coverage=[];exceptions=[]
def reason(g):
 s,t=g['sourceStem'],g['targetStem']
 if re.search(r'\b(short|pant)\b',s) and 'waist' not in s:return 'Restore garment shorts/pants and the explicit source length qualifier; target used the adjective short or mixed English.'
 if s in ['bust','chest/bust','hip','hips','waist','shoulder','upper bust','underbust','leg opening'] and g['semanticIndex'] in M['CONTEXT_REVIEW']:return 'Preserve the generic source dimension; remove target-only circumference/width method or restore the named body area.'
 if 'flat/stretch' in s:return 'Preserve the two source measurement states: laid flat and stretched; target described elastic material or omitted flat position.'
 if 'height' in s:return 'Use human-height wording only for a source column whose person size/measurement context proves stature; retain exact qualifiers and units.'
 if s=='chest width':return 'Source explicitly says chest width; current target circumference is a different measurement.'
 if s=='skirt length':return 'Source column is skirt length; target incorrectly says sleeve or skirt.'
 if s=='size':return 'Use the garment-size noun rather than generic physical size.'
 if g['semanticIndex']==1373:return 'Source Body Length is the T-shirt body length; separate Recommended Height column proves this is garment length.'
 if 'weight' in s:return 'Preserve source weight recommendation or body-weight meaning in clothing-size context.'
 return 'Correct the evidenced typo, missing word, mixed English, or incorrect garment/body-part meaning while retaining the complete source label.'
for g in groups:
 i=g['semanticIndex'];status='REVIEWED_RETAIN_MEANING'
 if i in M['CORRECTIONS']:
  new=M['CORRECTIONS'][i]
  for pi in g['pairIndexes']:
   p=pairs[pi];match=re.search(r'\s*[（(][^()（）]*[)）]\s*$',p['targetHeader']);suffix=match.group(0) if match else ''
   after=new+suffix
   if after==p['targetHeader']:continue
   uses=[];ret=[]
   for u in p['uses']:
    if i in M['PERSON_HEIGHT_CONTEXT_ONLY'] and u['productIndex'] in M['GARMENT_HEIGHT_PRODUCTS']:
     ret.append(u);exceptions.append({**u,'disposition':'RETAIN_GARMENT_HEIGHT','reason':'English Height column contains father shorts 50–53 cm and child shorts 28–33 cm; separate Height Range is human stature.'})
    else:uses.append(u)
   if uses:rows.append({'mappingIndex':len(rows),'semanticIndex':i,'pairIndex':pi,'locale':p['locale'],'sourceHeader':p['sourceHeader'],'beforeHeader':p['targetHeader'],'afterHeader':after,'preservedSuffix':suffix,'reason':reason(g),'uses':uses,'currentCount':sum(not x['effectiveOutdated'] for x in uses),'outdatedCount':sum(x['effectiveOutdated'] for x in uses)})
  status='PROPOSED_SOURCE_BOUND_CORRECTION'
 elif i in [588,981,1391,1476,1758,1853]:status='RETAIN_CONTEXTUAL_COAT_LENGTH_SOURCE_IS_SHIRT'
 elif i in [1827,1917]:status='RETAIN_US_QUALIFIER_PRESENT_IN_FULL_HEADER'
 coverage.append({**g,'disposition':status})
result={'scope':'Full manual semantic read of all 1926 compact groups and exact source/target suffix variants over 4760 effective product bodies. Final occurrence application is current-only, subject to later overlays and independent review.','counts':{'languagesRead':len(M['READ_LOCALES']),'semanticGroupsRead':len(groups),'exactPairsCovered':len(pairs),'mappingRows':len(rows),'currentProposedOccurrences':sum(x['currentCount'] for x in rows),'outdatedProposedOccurrences':sum(x['outdatedCount'] for x in rows)},'rows':rows}
for name,obj in [('mapping_dictionary_v1.json',result),('semantic_coverage1926.json',{'rows':coverage}),('context_retained_occurrences.json',{'rows':exceptions})]:(H/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
(H/'mapping_dictionary_v1.tsv').write_text('map\tgroup\tlocale\tsource\tbefore\tafter\tcurrent\toutdated\n'+''.join(f"{x['mappingIndex']}\t{x['semanticIndex']}\t{x['locale']}\t{x['sourceHeader']}\t{x['beforeHeader']}\t{x['afterHeader']}\t{x['currentCount']}\t{x['outdatedCount']}\n" for x in rows))
print(result['counts']);print(hashlib.sha256((H/'mapping_dictionary_v1.json').read_bytes()).hexdigest())
