import json,re,html,hashlib,copy
from pathlib import Path
from prose_completion11_manual import TAILS
from prose_completion11_prefixes import PREFIXES,HEADINGS
H=Path(__file__).resolve().parent;B=H.parents[1];sha=lambda x:hashlib.sha256(x.encode()).hexdigest()
baseline=B/'review/size-label-repair/placeholder-review/placeholder88_reviewed.json';bsha=hashlib.sha256(baseline.read_bytes()).hexdigest();base=json.loads(baseline.read_text())['rows'];idx={(x['productIndex'],x['locale']):x for x in base}
def split_items(s):
 block=re.search(r'<ul\b[^>]*>(.*?)</ul>',s,re.S)[1];starts=list(re.finditer(r'<li\b[^>]*>',block));out=[]
 for i,m in enumerate(starts):
  end=starts[i+1].start() if i+1<len(starts) else len(block);t=block[m.start():end];close=t.find('</li>');out.append(t[:close+5] if close>=0 else t.rstrip()+'</li>')
 return out
rows=[];ledger=[]
for (j,l),values in TAILS.items():
 r=idx[j,l];src=r['source'];before=r['value'];st=list(re.finditer(r'<table\b.*?</table>',src,re.S));tt=re.findall(r'<table\b.*?</table>',before,re.S);assert len(st)==len(tt)==2
 sourceTail=src[st[-1].end():];pieces=re.split(r'(<[^>]+>)',sourceTail);nodes=[(i,p) for i,p in enumerate(pieces) if not p.startswith('<') and p.strip()];assert len(nodes)==len(values)==14
 tailchanges=[]
 for (i,p),v in zip(nodes,values):pieces[i]=html.escape(v,quote=False);tailchanges.append({'source':p,'value':v})
 tail=''.join(pieces);olditems=split_items(before);sourceitems=split_items(src);assert len(olditems)==len(sourceitems)==6;newitems=olditems[:];changes=[]
 for ordinal,(label,body) in PREFIXES[j,l].items():
  new='<li>\n<strong>'+html.escape(label,quote=False)+'</strong> '+body+'</li>'
  # Inline emphasis is manually retained for source role names; otherwise escape literal & only.
  new=new.replace(' & ',' &amp; ');newitems[ordinal]=new
  reason=('Current source wording/qualifiers missing or mistranslated; translate full exact clause. Fabric, role/garment, care and size facts remain English-source bound.')
  if ordinal==4 and j==176:reason='Restore like-colors and low tumble-dry options; remove obsolete care-inference sentence absent current English.'
  if ordinal==0 and j==196:reason='Restore woven-look qualification; do not assert woven construction; retain unconfirmed fiber-content qualification.'
  changes.append({'ordinal':ordinal,'source':sourceitems[ordinal],'before':olditems[ordinal],'after':new,'reason':reason})
 if l=='el':
  if j in [166,171,176]:heads=['Πίνακας μεγεθών — Φόρεμα (μαμά και κορίτσι)','Πίνακας μεγεθών — '+('Πουκάμισο και σορτς' if j==166 else 'Πουκάμισο')+' (μπαμπάς και αγόρι)']
  else:heads=['Πίνακας μεγεθών — Φόρεμα','Πίνακας μεγεθών — Πουκάμισο']
 else:heads=HEADINGS[l]
 value='<ul>\n'+'\n'.join(newitems)+'\n</ul>\n'+'\n'.join('<h3>'+html.escape(head,quote=False)+'</h3>\n'+table for head,table in zip(heads,tt))+tail
 assert re.findall(r'<table\b.*?</table>',value,re.S)==tt
 kept=[i for i in range(6) if i not in PREFIXES[j,l]]
 for i in kept:assert olditems[i] in value
 out={k:r[k] for k in ['productIndex','resourceId','locale','key','source','sourceDigest','sourceSHA256','rawBefore','rawFile','rawFileSHA256','onlineStoreUrl']}
 out.update(sourceValue=src,before=None,expectedEffectiveBeforeValue=before,expectedEffectiveBeforeValueSHA256=sha(before),expectedBeforeValueSHA256=sha(before),beforeValueSHA256=sha(before),value=value,valueSHA256=sha(value),requiresFreshEffectiveBeforeObject=True,requiresFreshLiveSourceAndBeforeGuard=True,reviewStatus='AUTHOR_COMPLETE_PENDING_INDEPENDENT_FULL_MEANING_REVIEW',plannedBeforeDependencies=[{'file':str(baseline.relative_to(B)),'sha256':bsha,'includes':'reviewed headers v2 and placeholder88; source11 has no structural375/size156 overlap'}],reason='Complete evidenced missing source prose and correct stale/garbled source clauses; exact reviewed table HTML is retained. Does not edit English source.',proseChanges=changes,retainedFirstListItemOrdinals=kept,localizedChartHeadings=heads,sourceMissingTail=sourceTail,localizedTail=tail,tailTextNodePairs=tailchanges)
 rows.append(out);ledger.append({'productIndex':j,'locale':l,'resourceId':r['resourceId'],'sourceDigest':r['sourceDigest'],'plannedBeforeSHA256':sha(before),'afterSHA256':sha(value),'replacedFirstListItemOrdinals':sorted(PREFIXES[j,l]),'retainedFirstListItemOrdinals':kept,'prefixChanges':changes,'tailTextNodePairs':tailchanges,'layoutRepair':'Remove duplicate/English orphan chart headings, extra list closing tags and fallback-marker comments; keep both real tables byte-exact in English source order. Complete current source tail follows final table.','existingEarlierParagraphDisposition':'P166 EL and P191 EL old paragraphs were abridged/mistranslated; P178 EL polished appearance was rendered as shiny. Each is superseded by faithful complete source paragraph at current-source position. Other rows had no such paragraph.'})
assert len(rows)==11 and len({(r['resourceId'],r['locale']) for r in rows})==11
(H/'prose_completion11_candidates_v1.json').write_text(json.dumps({'rows':rows},ensure_ascii=False,indent=2)+'\n');(H/'prose_completion11_delta_ledger.json').write_text(json.dumps({'rows':ledger},ensure_ascii=False,indent=2)+'\n');print(json.dumps({'rows':11,'sha256':sha((H/'prose_completion11_candidates_v1.json').read_text()),'baselineSHA256':bsha,'newTailNodes':sum(len(r['tailTextNodePairs']) for r in rows),'replacedFirstListClauses':sum(len(r['proseChanges']) for r in rows),'retainedFirstListClauses':sum(len(r['retainedFirstListItemOrdinals']) for r in rows)}))
