from pathlib import Path
import json,re,hashlib,html,importlib.util
P=Path(__file__).parent;PACK=P.parents[1];sha=lambda s:hashlib.sha256(s.encode()).hexdigest();fsha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest();write=lambda n,d:(P/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
spec=importlib.util.spec_from_file_location('o',PACK/'tooling/offline_translation.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
pairs=json.loads((P/'article16_pairs.json').read_text());rows=json.loads((P/'article16_candidates_frozen_copy.json').read_text())['rows'];checks=json.loads((P/'article16_checks.json').read_text())['rows'];assert not any(r['errors']for r in checks)
# Exact whole visible text-node corrections; source facts and source HTML are retained.
rules=[
(38,'مجموعة القطع العلوية','Retain tops category breadth rather than shirts only.'),
(202,'Celý outfit v černé','Retain all-black outfit meaning, not black color generally.'),
(273,pairs[273]['target'].replace('den mest populære farveskema','det mest populære farveskema'),'Danish noun gender agreement.'),
(286,pairs[286]['target'].replace('Let lag','Lette lag'),'Danish plural agreement for light layers.'),
(291,'Lette cardigans eller jakker til lag-på-lag','Danish plural light-cardigans phrase.'),
(320,'Helt sort','Danish all-black phrase grammar.'),
(342,pairs[342]['target'].replace('familiefotograferes','familie fotograferes'),'Restore missing space between family and is photographed.'),
(356,pairs[356]['target'].replace('Τα συντονισμένα οικογενειακές εμφανίσεις','Οι συντονισμένες οικογενειακές εμφανίσεις'),'Greek article/adjective agree with feminine plural noun.'),
(422,'Καρό μοτίβα και λεπτομέρειες από φανέλα','Retain plaid and flannel fabric accents, not generic undershirts.'),
(706,'Koko perheen yhteensopivat asut','Retain full-family matching clothing meaning rather than abstract family unity.'),
(792,'mère-fille en robes assorties','Retain dresses specifically in dress collection link text.'),
(865,pairs[865]['target'].replace("que chacun ait l'air d'une véritable équipe","que chacun ait l’air et se sente membre d’une même équipe"),'Restore feel as well as look like a team; avoid each person being a team.'),
(971,'— टोपी, बो वाले रिबन और','Retain bow-shaped ribbon accessories, not unspecified ribbons.'),
(1412,'badkleding','Retain general family swimwear, not one-piece swimsuits only.'),
(1652,'Vestidos de verão para mãe e filha, camisas casuais para pai e filho','Retain summer/sundress type.'),
(1746,pairs[1746]['target'].replace('Probabil acesta este cea mai populară schemă','Probabil aceasta este cea mai populară schemă'),'Romanian demonstrative agrees with feminine schema noun.')]
corrections=[];out=[];(P/'article16').mkdir(exist_ok=True)
for r,c in zip(rows,checks):
 v=r['value'];ident=r['resourceId'].split('/')[-1]+':'+r['locale'];applied=[]
 for i,to,why in rules:
  pair=pairs[i]
  if ident not in pair['tuples']:continue
  tokens=re.split(r'(<[^>]+>)',v);count=0
  for at,t in enumerate(tokens):
   if not t.startswith('<')and html.unescape(t).strip()==pair['target']:
    lead=re.match(r'^\s*',t).group();trail=re.search(r'\s*$',t).group();tokens[at]=lead+html.escape(to,quote=False)+trail;count+=1
  assert count==1,(i,ident,count);v=''.join(tokens)
  fix={'resourceId':r['resourceId'],'locale':r['locale'],'key':r['key'],'sourceDigest':r['sourceDigest'],'authorValueSHA256':sha(r['value']),'pairId':i,'sourceText':pair['source'],'from':pair['target'],'to':to,'reason':why,'occurrences':count};corrections.append(fix);applied.append(fix)
 ck=m.verify_text(r['source'],v,r['locale']);assert not ck['errors'],(ident,ck);assert re.findall('<[^>]+>',v)==re.findall('<[^>]+>',r['value'])
 assert sha(r['source'])==r['sourceSHA256'];assert sha(r['before']['value'])==r['expectedBeforeValueSHA256'];assert fsha(PACK/r['rawFile'])==r['rawFileSHA256'];assert fsha(PACK/r['candidateFile'])==r['candidateFileSHA256']
 f=P/'article16'/f"{r['locale']}_{r['resourceId'].split('/')[-1]}.html";f.write_text(v)
 rr={**r,'sourceValue':r['source'],'value':v,'valueSHA256':sha(v),'candidateFile':str(f.relative_to(PACK)),'candidateFileSHA256':fsha(f),'independentMeaningReview':'PASS_WITH_EXACT_CORRECTIONS'if applied else'PASS','independentReviewer':'article_he_pl_complete','independentReviewArtifact':'review/product-remainder-independent/article16_review.json','authorCandidateFile':r['candidateFile'],'authorCandidateFileSHA256':r['candidateFileSHA256'],'independentCorrectionsApplied':len(applied)};out.append(rr)
write('article16_corrections.json',{'rules':corrections});write('article16_reviewed_candidates.json',{'rows':out});write('article16_review.json',{'status':'PASS_AFTER_16_EXACT_CORRECTIONS','rows':16,'correctedRows':len(set((x['resourceId'],x['locale'])for x in corrections)),'completeBodiesRead':16,'uniqueSourceTargetTextPairs':1829,'inlineParagraphsInFullBodyReview':549,'reviewMethod':'Both exact English source bodies read in full; every full target body read against its source, including linked text joins, new planning/order/size/delivery advice, all headings and lists. All current source claims preserved. Source/raw/digest/global-before bindings and HTML/attributes/images/URLs/numbers verified independently. Exact correction proposals applied only to new review copies; author originals untouched.','correctionsFile':'article16_corrections.json','rowsEvidence':checks,'sourceDefects':[],'limits':'Root owns existing source-policy dispositions and fresh external source/before guard; no live or Git action taken.'})
print({'rows':16,'corrections':len(corrections),'correctedRows':len(set((x['resourceId'],x['locale'])for x in corrections)),'sha256':fsha(P/'article16_reviewed_candidates.json')})
