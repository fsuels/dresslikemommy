import json,re,hashlib,collections,difflib,html
from pathlib import Path
H=Path(__file__).resolve().parent
sha=lambda s:hashlib.sha256(s.encode()).hexdigest()
a=json.loads((H/'effective_body_inventory.json').read_text())['rows']
mappings={
'ar':{'ديف':'div','لي':'li','معرف':'table','الرأس':'thead','تر':'tr','الجسم':'tbody','الجدول':'table','ح3':'h3'},
'it':{'testa':'thead','corpo':'tbody','tcorpo':'tbody','tabella':'table','immagine':'img'},
'ja':{'リ':'li','頭':'thead','本体':'tbody','テーブル':'table','オル':'ol'},
'nl':{'thoofd':'thead','tlichaam':'tbody','tabel':'table'},
'pl':{'głowa':'thead','ciało':'tbody','tabela':'table'},
'hi':{'ली':'li','तालिका':'table','सिर':'thead'},
'ko':{'리':'li','테이블':'table','머리':'thead','몸':'tbody'},
'ru':{'дел':'div','ул':'ul','ли':'li','голова':'thead','тр':'tr','тело':'tbody','тд':'td','таблица':'table'},
'pt-BR':{'corpo':'tbody','tabela':'table'}}
pat=re.compile(r'<\s*(/?)\s*([^\s<>/]+)(?:\s[^<>]*?)?\s*/?>')
void=set('area base br col embed hr img input link meta param source track wbr'.split())
def tokens(s):
 return [('' if not m[1] else '/')+m[2].lower() for m in pat.finditer(re.sub(r'<!--.*?-->','',s,flags=re.S)) if m[2][0].isalpha()]
def balance(s):
 seq=tokens(s);counts=collections.Counter();stack=[];issues=[]
 for t in seq:
  tag=t.lstrip('/')
  if tag in void:continue
  if t[0]!='/':counts[tag]+=1;stack.append(tag)
  else:
   counts[tag]-=1
   if stack and stack[-1]==tag:stack.pop()
   elif tag in stack:
    at=len(stack)-1-stack[::-1].index(tag);issues.append({'closing':tag,'interveningOpen':stack[at+1:]});stack=stack[:at]
   else:issues.append({'closing':tag,'withoutOpen':True})
 return {'unbalancedCounts':{k:v for k,v in counts.items() if v},'nestingIssueCount':len(issues),'unclosedStack':stack,'issues':issues}
rows=[];held=[];rulecounts=collections.Counter();allproof=[]
for r in a:
 if not r.get('targetOnlyUnknownTags'):continue
 if r['overlayApplied'] or r['before']['outdated'] is not False:held.append({'resourceId':r['resourceId'],'locale':r['locale'],'reason':'Outdated or unverifiable current object'});continue
 before=r['expectedEffectiveBeforeValue'];src=r['source'];replacements=[];sourceTokens=tokens(src)
 unknown={t['name'] for t in r['targetOnlyUnknownTags']}
 def fix(m):
  old=m[2].lower()
  if old not in unknown:return m[0]
  if re.fullmatch(r'thcolspan=["\'][56]["\']',old):
   target='th';new=m[0].replace(m[2],m[2][:2]+' '+m[2][2:],1);kind='MALFORMED_TH_ATTRIBUTE_BOUNDARY_WHITESPACE_ONLY'
  else:
   target=mappings[r['locale']][old];new=m[0][:m.start(2)-m.start()]+target+m[0][m.end(2)-m.start():];kind='TRANSLATED_ELEMENT_NAME_ONLY'
  tok=('/' if m[1] else '')+target
  assert tok in sourceTokens,(r['productIndex'],r['locale'],tok,'not observed in exact source')
  # Every attribute byte remains intact for ordinary replacements. The th fix adds exactly one boundary space.
  if kind=='TRANSLATED_ELEMENT_NAME_ONLY':
   assert m[0][m.end(2)-m.start():]==new[(m.start(2)-m.start())+len(target):]
   if r['locale']=='ar' and old=='معرف':
    assert re.search(r'<table\s+id=',src);new=re.sub(r'(?<=table)\s+الجدول(?=\s*=)', ' id',new);kind='TRANSLATED_TABLE_AND_SOURCE_BACKED_ID_NAME'
   if r['locale']=='hi' and old=='तालिका' and not m[1]:
    assert re.search(r'<table\s+id=',src);new=re.sub(r'(?<=table)\s+आईडी(?=\s*=)', ' id',new);kind='TRANSLATED_TABLE_AND_SOURCE_BACKED_ID_NAME'
  else:assert new.replace('th colspan','thcolspan')==m[0]
  replacements.append({'oldLiteral':m[0],'newLiteral':new,'oldName':old,'newName':target,'kind':kind,'beforePosition':m.start(),'sourceToken':tok,'sourceTokenObserved':True,'attributesPreserved':True});rulecounts[(r['locale'],old,target)]+=1
  return new
 tagValue=pat.sub(fix,before);value=tagValue
 prose=[]
 if r['productIndex']==5 and r['locale']=='ja':
  for old,new in [('調節可能なネクタイ:', '調節可能な首の結びひも:'),('調節可能なネクタイで','調節可能な首の結びひもで'),('ホルターネックの調節可能なネクタイにより','ホルターネックの調節可能な結びひもにより')]:
   assert value.count(old)==1;value=value.replace(old,new,1);prose.append({'before':old,'after':new,'count':1,'sourceEvidence':'Adjustable Neck Tie / The adjustable neck tie of the halter top ensures a custom fit','reason':'Swimsuit neck fastening tie, not a formal necktie; explicitly requested root scope.'})
 assert len(replacements)==len(r['targetOnlyUnknownTags'])
 assert re.sub(r'<[^>]*>','',before)==re.sub(r'<[^>]*>','',tagValue)
 expectedText=re.sub(r'<[^>]*>','',before)
 for change in prose:expectedText=expectedText.replace(change['before'],change['after'],1)
 assert expectedText==re.sub(r'<[^>]*>','',value)
 assert re.findall(r'=\s*([\"\'])(.*?)\1',before)==re.findall(r'=\s*([\"\'])(.*?)\1',value)
 assert re.findall(r'\d+(?:[.,]\d+)?',before)==re.findall(r'\d+(?:[.,]\d+)?',value)
 assert re.findall(r'https?://[^\s<>\"\']+',before)==re.findall(r'https?://[^\s<>\"\']+',value)
 assert all(t['name'] not in unknown for t in [{'name':x.lstrip('/')} for x in tokens(value)])
 # Show exact source alignment independently of inherited extra tables or other pre-existing differences.
 afterTokens=tokens(value);alignment={};sm=difflib.SequenceMatcher(None,sourceTokens,afterTokens,autojunk=False)
 for block in sm.get_matching_blocks():
  for off in range(block.size):alignment[block.b+off]=block.a+off
 beforeTokens=tokens(before);assert len(beforeTokens)==len(afterTokens)
 repairTokenIndices=[i for i,(x,y) in enumerate(zip(beforeTokens,afterTokens)) if x!=y]
 for rep,i in zip(replacements,repairTokenIndices):
  assert rep['sourceToken']==afterTokens[i];rep['targetTokenIndex']=i;rep['alignedSourceTokenIndex']=alignment.get(i);rep['sourceSequenceAlignment']='EXACT_ALIGNED_TOKEN' if i in alignment else 'SOURCE_TOKEN_AND_LOCAL_TABLE_OR_LIST_CONTEXT_REQUIRES_REVIEW'
 beforeBal=balance(before);afterBal=balance(value)
 c={k:r[k] for k in ['productIndex','resourceId','locale','key','source','sourceDigest','sourceSHA256','before','rawBefore','rawFile','rawFileSHA256','onlineStoreUrl']}
 c.update(value=value,valueSHA256=sha(value),beforeValueSHA256=sha(before),expectedBeforeValueSHA256=sha(before),reviewStatus='AUTHOR_PENDING_INDEPENDENT_STRUCTURAL_REVIEW',requiresFreshLiveSourceAndBeforeGuard=True,reason='Repair proven translated HTML element names / source-backed ID attribute names / missing th boundary space. All prose, cells, numbers, URLs and attribute VALUES preserved, except separately recorded root-requested Japanese P5 necktie correction.',replacements=replacements,proseExceptions=prose,tagOnlyValueSHA256=sha(tagValue),checks={'beforeOutdatedFalse':True,'tagOnlyVisibleTextExact':True,'finalVisibleTextExactExceptExplicitJapaneseP5ThreePhrases':True,'numericSequenceExact':True,'urlsExact':True,'attributeValuesExact':True,'attributeNamesExactExceptSourceBackedTranslatedId':True,'allTargetOnlyUnknownTagsRemoved':True,'beforeBalancedness':beforeBal,'afterBalancedness':afterBal,'afterExactSourceElementSequence':sourceTokens==afterTokens,'sourceAndCurrentOtherStructuralDifferencesPreserved':True},translatedIdAttributeNamesRestored=bool(r['locale'] in ['ar','hi']))
 rows.append(c)
(H/'tag_candidates_v1.json').write_text(json.dumps({'status':'CURRENT_FALSE_TRANSLATED_TAG_ONLY_PENDING_INDEPENDENT_REVIEW','rows':rows},ensure_ascii=False,indent=2)+'\n')
(H/'tag_held_ledger.json').write_text(json.dumps({'rows':held},ensure_ascii=False,indent=2)+'\n')
summary={'status':'AUTHOR_STRUCTURAL_CHECKS_PASS_PENDING_INDEPENDENT_REVIEW','rows':len(rows),'heldOutdated':len(held),'occurrences':sum(len(r['replacements']) for r in rows),'all374BeforeOutdatedFalse':True,'visibleTextNumericURLAttributeParity':len(rows),'exactAlignedSourceTokens':sum(p['sourceSequenceAlignment']=='EXACT_ALIGNED_TOKEN' for r in rows for p in r['replacements']),'sourceTokensRequiringContextReview':sum(p['sourceSequenceAlignment']!='EXACT_ALIGNED_TOKEN' for r in rows for p in r['replacements']),'beforeUnbalancedCountRows':sum(bool(r['checks']['beforeBalancedness']['unbalancedCounts']) for r in rows),'afterUnbalancedCountRows':sum(bool(r['checks']['afterBalancedness']['unbalancedCounts']) for r in rows),'afterNestingIssueRows':sum(bool(r['checks']['afterBalancedness']['nestingIssueCount'] or r['checks']['afterBalancedness']['unclosedStack']) for r in rows),'afterExactSourceSequenceRows':sum(r['checks']['afterExactSourceElementSequence'] for r in rows),'rules':[dict(locale=k[0],old=k[1],new=k[2],occurrences=v) for k,v in sorted(rulecounts.items())],'candidateSHA256':sha((H/'tag_candidates_v1.json').read_text()),'limits':['Exact source element sequence can differ because legacy target retains duplicate fallback table; do not delete tables.','Arabic/Hindi ID attribute names restored from exact English table context; existing translated ID VALUES retained to avoid duplicate IDs.','Remaining valid-HTML source/current structural differences are preserved, not claimed fixed.']}
(H/'tag_checks.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in summary.items() if k!='rules'},ensure_ascii=False))
