import json,re,html,hashlib,collections
from pathlib import Path
H=Path(__file__).resolve().parent;B=H.parents[1];sha=lambda x:hashlib.sha256(x.encode()).hexdigest()
inv=json.loads((H/'effective_body_inventory.json').read_text())['rows'];idx={(r['productIndex'],r['locale']):r for r in inv};findings=json.loads((H/'expanded_placeholder_inventory.json').read_text())['rows'];holds=json.loads((B/'review/article-title-independent/product_source_disposition846.json').read_text())['rows'];heldkeys={(r['resourceId'],r['locale'],r['key']) for r in holds}
manual={
(153,'cs'):'<li>\n<strong>Design:</strong> Vyberte si <em>šaty pro maminku</em> nebo <em>šaty pro dívku</em> ve vrstveném střihu s ramínky, nastavitelným zavazováním a elastickým pasem pod prsy; zvolte <em>košili pro tatínka</em> nebo <em>košili pro chlapce</em> ve volném střihu s krátkými rukávy, zapínáním na knoflíky a rozhalenkovým límcem.</li>',
(153,'el'):'<li>\n<strong>Σχεδίαση:</strong> Επιλέξτε <em>φόρεμα για τη μαμά</em> ή <em>φόρεμα για κορίτσι</em> σε γραμμή με διαδοχικές στρώσεις, λεπτές τιράντες, ρυθμιζόμενα δεσίματα και ελαστική μέση κάτω από το στήθος· επιλέξτε <em>πουκάμισο για τον μπαμπά</em> ή <em>πουκάμισο για αγόρι</em> σε χαλαρή γραμμή, με κοντά μανίκια, κουμπιά μπροστά και ανοιχτό γιακά.</li>',
(153,'fi'):'<li>\n<strong>Malli:</strong> Valitse <em>äidin mekko</em> tai <em>tytön mekko</em>, jossa on kerrostettu olkainmalli, säädettävät solmittavat nauhat ja joustava empirevyötärö; valitse <em>isän paita</em> tai <em>pojan paita</em>, jos haluat rennon, lyhythihaisen napitettavan paidan, jossa on avoin kaulus.</li>',
(154,'cs'):'<li>\n<strong>Design:</strong> Vyberte si <em>šaty pro maminku</em> nebo <em>šaty pro dívku</em> v maxi délce, bez rukávů, s hlubším kulatým výstřihem a duhovými pruhy; zvolte <em>tričko pro tatínka</em> nebo <em>tričko pro chlapce</em> s krátkým rukávem, kulatým výstřihem ke krku a hravým duhovým logem.</li>',
(154,'el'):'<li>\n<strong>Σχεδίαση:</strong> Επιλέξτε <em>φόρεμα για τη μαμά</em> ή <em>φόρεμα για κορίτσι</em> σε αμάνικο μάξι σχέδιο με βαθιά στρογγυλή λαιμόκοψη και ρίγες στα χρώματα του ουράνιου τόξου· επιλέξτε <em>μπλουζάκι για τον μπαμπά</em> ή <em>μπλουζάκι για αγόρι</em> με κοντά μανίκια, κλειστή στρογγυλή λαιμόκοψη και παιχνιδιάρικο λογότυπο ουράνιου τόξου.</li>',
(154,'fi'):'<li>\n<strong>Malli:</strong> Valitse <em>äidin mekko</em> tai <em>tytön mekko</em> hihattomana maksimekkona, jossa on avara pyöreä pääntie ja sateenkaariraidat; valitse <em>isän paita</em> tai <em>pojan paita</em> lyhythihaisena T-paitana, jossa on pyöreä pääntie ja leikkisä sateenkaarilogo.</li>',
}
# Opening li order is preserved in these source/target prose lists even when a closing boundary is corrupted.
def item_spans(s):
 starts=list(re.finditer(r'<li\b[^>]*>',s));out=[]
 for i,m in enumerate(starts):
  nextstart=starts[i+1].start() if i+1<len(starts) else len(s);close=re.search(r'</li\s*>',s[m.end():nextstart]);end=m.end()+close.end() if close else nextstart
  out.append((m.start(),end,s[m.start():end]))
 return out
candidates=[];held=[];evidence=[]
for f in findings:
 r=idx[f['productIndex'],f['locale']];j,l=r['productIndex'],r['locale'];before=r['expectedEffectiveBeforeValue'];source=r['source'];changes=[];v=before;sourceitems=item_spans(source)
 if f['outdated']:
  held.append({**f,'reason':'OUTDATED_TRUE_PARTIAL_MARKUP_PATCH_WOULD_FALSELY_REFRESH_CONTENT','originalSourceDispositionHold':(r['resourceId'],l,'body_html') in heldkeys});continue
 def apply(old,new,reason,sourcequote,extra=None):
  global v
  assert old in v and sourcequote in source,(j,l,reason,old[:100]);assert v.count(old)==1,(j,l,old[:40]);v=v.replace(old,new,1);changes.append({'before':old,'after':new,'reason':reason,'sourceExactQuote':sourcequote,**(extra or {})})
 if (j,l) in manual:
  spans=item_spans(v);start=spans[3][0];end=spans[4][0];old=v[start:end];new=manual[j,l]+ '\n';sq=sourceitems[3][2]
  apply(old,new,'Restore source design list item whose mask corruption also dropped or garbled garment details; manually translated full exact item.',sq)
 if (j,l)==(182,'de'):
  items=item_spans(v);bad=next(t for t in items if 'QZXTOKEN00289Q' in t[2]);si=next(t[2] for t in sourceitems if 'Ruffle-trim neckline' in t[2]);old=bad[2];new='<li>\n<strong>Ausschnitt mit Rüschenbesatz:</strong> Weiche Rüschen auf der Vorderseite und ein eckiger Ausschnitt sorgen bei Mama und Kind für eine hübsche, schicke Optik.</li>\n';apply(old,new,'Restore missing source-backed neckline clause and close strong/list item.',si)
 if j in [132,133,147] and l=='fi':
  token=next(m['token'] for m in f['matches'] if 'Q028' in m['token'] or '00307' in m['token']);apply(token,'</h3><ul>','Restore exact source heading/list boundary masked as a token.','</h3><ul>')
 if (j,l)==(145,'el'):
  apply('QZXTOKEN0030','</p><p>','Restore source paragraph break masked as a token.','penguin.</p><p>Wear it')
  p=v.find('</p><p>');pos=v.find('<li>',p);old=v[pos-60:pos+4];assert old.endswith('\n<li>')
  apply(old,old[:-5]+'</p><h3>Βασικά χαρακτηριστικά:</h3><ul>\n<li>','Restore omitted source paragraph close, localized key-features heading and list opening.','</p><h3>Key Features:</h3><ul>')
 # Handle all remaining known corrupt spans, preserving native-word prefixes exactly.
 ms=list(re.finditer(r'[A-Za-z0-9_]*(?:QZ|XTOKEN|QX|TOKEN)[A-Za-z0-9_]*',v))
 for m in reversed(ms):
  token=m[0]
  if token in source:continue
  if not any(x.isdigit() for x in token) and 'TOKEN' not in token:continue
  if j==163 and l in ['da','he','no','sv']:
   prefix={'da':'rmer','he':'','no':'ermer','sv':'rmar'}[l];assert token.startswith(prefix);old=token+'.';new=prefix+'.</li>';ordinal=len(re.findall(r'<li\b',v[:m.start()]))-1;sq=sourceitems[ordinal][2];apply(old,new,'Restore closing list tag from corrupted mask while retaining native sleeves word and sentence punctuation.',sq,{'sourceListItemOrdinal':ordinal});continue
  ordinal=len(re.findall(r'<li\b',v[:m.start()]))-1;assert ordinal>=0
  # Remaining corruption occurs precisely at a source item's closing boundary, immediately before next li.
  assert re.match(r'\s*<li\b',v[m.end():]),(j,l,token,v[m.end():m.end()+50])
  sourceCount=len(re.findall(r'<li\b',source));targetCount=len(re.findall(r'<li\b',v))
  if sourceCount+1==targetCount and re.match(r'<p><strong>Fabric:',source): ordinal-=1
  elif sourceCount!=targetCount:
   sourceFirst=re.search(r'<ul\b[^>]*>(.*?)</ul>',source,re.S);targetFirst=re.search(r'<ul\b[^>]*>(.*?)</ul>',v,re.S);assert sourceFirst and targetFirst and m.start()<targetFirst.end() and len(re.findall(r'<li\b',sourceFirst[1]))==len(re.findall(r'<li\b',targetFirst[1])),(j,l,'first-list-count')
  sq=sourceitems[ordinal][2];assert sq.rstrip().endswith('</li>')
  beforetags=re.findall(r'<[^>]+>',v[:m.start()]);assert beforetags[-1] in ['</strong>','</em>'],(j,l,token,beforetags[-1])
  old=v[max(0,m.start()-50):m.end()+10]; new=old[:m.start()-max(0,m.start()-50)]+'</li>'+old[m.end()-max(0,m.start()-50):]; apply(old,new,'Restore source closing li at same list-item ordinal; token is not product prose.',sq,{'sourceListItemOrdinal':ordinal,'sourceFollowingListItem':sourceitems[ordinal+1][2] if ordinal+1<len(sourceitems) else None})
 # No URL/image, table-cell/header or actual numeric measurements changed. Removed token digits are excluded explicitly.
 assert re.findall(r'<table\b.*?</table>',before,re.S)==re.findall(r'<table\b.*?</table>',v,re.S)
 assert re.findall(r'https?://[^\s<>"\']+',before)==re.findall(r'https?://[^\s<>"\']+',v)
 assert v!=before
 row={k:r[k] for k in ['productIndex','resourceId','locale','key','source','sourceDigest','sourceSHA256','before','rawBefore','rawFile','rawFileSHA256','onlineStoreUrl']}
 row.update(value=v,valueSHA256=sha(v),expectedBeforeValueSHA256=sha(before),beforeValueSHA256=sha(before),requiresFreshLiveSourceAndBeforeGuard=True,originalSourceDispositionHold=(r['resourceId'],l,'body_html') in heldkeys,patches=changes,reviewStatus='AUTHOR_COMPLETE_PENDING_INDEPENDENT_REVIEW',reason='Exact source-backed malformed token restoration; measurements, tables and URLs preserved. Does not alter English facts or clear separate source issue holds.')
 candidates.append(row);evidence.append({'productIndex':j,'locale':l,'resourceId':r['resourceId'],'sourceDigest':r['sourceDigest'],'changes':changes})
assert len(candidates)==87 and len(held)==6
(H/'placeholder_candidates_v1.json').write_text(json.dumps({'rows':candidates},ensure_ascii=False,indent=2)+'\n');(H/'placeholder_evidence_v1.json').write_text(json.dumps({'rows':evidence},ensure_ascii=False,indent=2)+'\n');(H/'placeholder_held_v1.json').write_text(json.dumps({'rows':held},ensure_ascii=False,indent=2)+'\n')
report={'status':'AUTHOR_PASS_PENDING_INDEPENDENT_REVIEW','rows':len(candidates),'heldOutdatedRows':len(held),'changes':sum(len(r['patches']) for r in candidates),'sourceHoldOverlapCurrentRows':sum(r['originalSourceDispositionHold'] for r in candidates),'sourceHoldOverlapOutdatedRows':sum(r['originalSourceDispositionHold'] for r in held),'tableHTMLExactAll87':True,'URLsExactAll87':True,'candidateSHA256':sha((H/'placeholder_candidates_v1.json').read_text())};(H/'placeholder_checks_v1.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report))
