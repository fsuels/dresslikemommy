from pathlib import Path
import json,re,html,hashlib,collections,importlib.util,copy
P=Path(__file__).parent;PACK=P.parents[2]
sha=lambda s:hashlib.sha256(s.encode()).hexdigest()
write=lambda n,d:(P/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
rows=json.loads((P/'template_body_worklist.json').read_text())['rows'];pairs=json.loads((P/'template_pairs.json').read_text());alts=json.loads((P/'alt_pairs_bound.json').read_text());altmanual=json.loads((P/'manual_alt.json').read_text())
lookup={(x['locale'],x['source'],x['target']):x for x in pairs};altlookup={(x['locale'],x['source'],x['target']):x for x in alts}
rules=collections.defaultdict(list);overrides={};ruleuses=collections.Counter()
for f in sorted(P.glob('body_rules_*.json')):
 d=json.loads(f.read_text());overrides.update(d.get('nodeOverrides',{}))
 for loc in ['ar','cs','da']:
  for k,(old,new)in enumerate(d.get(loc,[])):rules[loc].append((f.name+':'+loc+':'+str(k),old,new))
def transform(s,loc):
 for rule,old,new in rules[loc]:
  count=s.count(old)
  if count:ruleuses[rule]+=count;s=s.replace(old,new)
 return s
spec=importlib.util.spec_from_file_location('o',PACK/'tooling/offline_translation.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def seg(s):return[html.unescape(x).strip()for x in re.split(r'(<[^>]+>)',s)if x.strip()and not x.startswith('<')]
img=re.compile(r'<img\b[^>]*>');altprefix=re.compile(r'\balt="([^"]*)"');altfull=re.compile(r'\balt="(.*?)"(?=\s+(?:style|loading|width|height|data-[\w-]+)=|\s*/?>)',re.S)
class Attr(m.HTMLParser):
 def handle_starttag(self,t,a):self.a=a
checks=[];changes=[];altchanges=[];final=[]
for r0 in rows:
 r=copy.deepcopy(r0);source=r['sourceValue'];before=r['before']['value'];ss,tt=seg(source),seg(before);assert len(ss)==len(tt)
 translated=[]
 for s,t in zip(ss,tt):
  pair=lookup[(r['locale'],s,t)];new=overrides.get(str(pair['i']),t);new=transform(new,r['locale'])
  if s[:1].isupper() and new[:1].islower():new=new[0].upper()+new[1:]
  if '→'in s and'→'not in new:new+=' →'
  if t!=new:changes.append({'ledgerId':r['ledgerId'],'pairIndex':pair['i'],'source':s,'beforeText':t,'valueText':new})
  translated.append(new)
 tokens=re.split(r'(<[^>]+>)',source);at=0
 for i,token in enumerate(tokens):
  if token.strip()and not token.startswith('<'):
   lead=re.match(r'^\s*',token).group();trail=re.search(r'\s*$',token).group();tokens[i]=lead+html.escape(translated[at],quote=False)+trail;at+=1
 assert at==len(translated);value=''.join(tokens)
 sourceimgs=img.findall(source);beforeimgs=img.findall(before);n=0
 def targetimg(match):
  global n
  s=sourceimgs[n];t=beforeimgs[n];n+=1
  parser=Attr(convert_charrefs=True);parser.feed(s);bad=any(k not in{'src','alt','style','loading','width','height','data-mce-src','data-mce-style'}for k,v in parser.a)
  sm=altprefix.search(s)if bad else altfull.search(s);tm=altprefix.search(t)if bad else altfull.search(t)
  if not sm:return s
  assert tm
  st,bt=html.unescape(sm.group(1)),html.unescape(tm.group(1));ap=altlookup[(r['locale'],st,bt)];new=transform(altmanual.get(str(ap['i']),bt),r['locale'])
  if bt!=new:altchanges.append({'ledgerId':r['ledgerId'],'altPairIndex':ap['i'],'source':st,'beforeText':bt,'valueText':new})
  # Replace only the authoritative source alt value; keep every other source tag byte.
  m0=altprefix.search(s);return s[:m0.start(1)]+html.escape(new,quote=True)+s[m0.end(1):]
 value=img.sub(targetimg,value);assert n==len(sourceimgs)
 # Source image tags differ only in localized alt value. Substitute exact source tags
 # solely for checking markup invariant; visible content, links, facts remain candidate.
 n=0
 def sourceimg(match):
  global n
  out=sourceimgs[n];n+=1;return out
 normalized=img.sub(sourceimg,value)
 v=m.verify_text(source,normalized,r['locale']);assert not v['errors'],(r['ledgerId'],v)
 # Separately ensure replacing the candidate alt value by the source value gives
 # exactly its original image tag, including inherited malformed source attributes.
 for st,ct in zip(sourceimgs,img.findall(value)):
  s0=altprefix.search(st);c0=altprefix.search(ct)
  if s0:
   assert c0
   restored=ct[:c0.start(1)]+s0.group(1)+ct[c0.end(1):]
   assert restored==st,(r['ledgerId'],'non-alt-image-change')
  else:assert st==ct
 assert len(seg(value))==len(ss),(r['ledgerId'],'node-count')
 assert '50'not in ' '.join(seg(value))or'50'in ' '.join(ss),(r['ledgerId'],'stale-threshold')
 r.update({'source':source,'value':value,'sourceSHA256':sha(source),'valueSHA256':sha(value),'expectedBeforeValueSHA256':sha(before),'reason':'Reviewed complete source-target body and image descriptions; repair confirmed stale shipping text, omissions, mixed-language fragments, printed slogans and grammar. Preserve complete current English claims, source image tags except localized alt values, all links/numbers/layout. No source-English edits.','reviewStatus':'MANUALLY_AUTHORED_PENDING_ROOT_INDEPENDENT_REVIEW'})
 final.append(r);checks.append({'ledgerId':r['ledgerId'],'resourceId':r['resourceId'],'locale':r['locale'],'key':r['key'],'sourceDigest':r['sourceDigest'],'sourceSHA256':r['sourceSHA256'],'beforeSHA256':r['expectedBeforeValueSHA256'],'valueSHA256':r['valueSHA256'],'sourceVisibleNodeCount':len(ss),'candidateVisibleNodeCount':len(seg(value)),'nonAltSourceMarkupExact':True,'normalizedAltStructuralCheck':v,'sourceBeforeBound':True,'localizedAltValuesIndividuallyReviewed':True})
write('body_candidates.json',{'status':'63_COMPLETE_MANUAL_CORRECTIONS_PENDING_INDEPENDENT_REVIEW','rows':final})
write('body_checks.json',{'status':'PASS_EXPLICIT_LOCALIZED_ALT_EXCEPTION','checkedRows':len(final),'uniqueTextPairsReviewed':len(pairs),'uniqueAltPairsReviewed':len(alts),'rows':checks,'limits':'Localized alt attribute strings differ intentionally from English. All other source tag bytes preserved. Twelve inherited malformed source IMG tag occurrences remain identical apart from parsed alt value; source English is not altered. Full live freshness and application are root responsibilities.'})
write('body_changes.json',{'visibleNodeChanges':changes,'altChanges':altchanges,'ruleUses':dict(ruleuses),'unusedRules':[x[0]for loc,rr in rules.items()for x in rr if not ruleuses[x[0]]]})
print({'rows':len(final),'checks':'PASS','visibleChanges':len(changes),'altChanges':len(altchanges),'unusedRules':[x[0]for loc,rr in rules.items()for x in rr if not ruleuses[x[0]]]})
