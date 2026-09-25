import json,re,collections,hashlib,html
from pathlib import Path
from html.parser import HTMLParser
H=Path(__file__).resolve().parent
class Optional(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=False);self.stack=[];self.errors=[];self.optional=[];self.ignored=[]
 def handle_starttag(self,t,attrs):
  if t=='li' and 'li' in self.stack:
   ix=len(self.stack)-1-self.stack[::-1].index('li')
   if 'ul' not in self.stack[ix+1:] and 'ol' not in self.stack[ix+1:]:
    if self.stack[ix+1:] and self.stack[ix+1:]!=['p']:self.errors.append({'event':'li_start_with_unclosed_nonoptional_inline','open':self.stack[ix+1:]})
    self.optional.append('li_before_li');self.stack=self.stack[:ix]
  if t in 'address article aside blockquote details dialog dd div dl dt fieldset figcaption figure footer form h1 h2 h3 h4 h5 h6 header hgroup hr li main menu nav ol p pre section table ul'.split() and 'p' in self.stack:
   ix=len(self.stack)-1-self.stack[::-1].index('p');self.optional.append('p_before_block');self.stack=self.stack[:ix]
  if t not in 'area base br col embed hr img input link meta param source track wbr'.split():self.stack.append(t)
 def handle_endtag(self,t):
  if t in 'area base br col embed hr img input link meta param source track wbr'.split():return
  if t in ['ul','ol'] and self.stack and self.stack[-1]=='li':self.stack.pop();self.optional.append('li_before_parent_end')
  if self.stack and self.stack[-1]==t:self.stack.pop();return
  if t in ['ul','li'] and t not in self.stack:self.ignored.append('unmatched_'+t+'_end_ignored');return
  self.errors.append({'event':'mismatched_end','tag':t,'open':self.stack[-6:]})
  if t in self.stack:self.stack=self.stack[:len(self.stack)-1-self.stack[::-1].index(t)]
 def handle_startendtag(self,t,a):self.handle_starttag(t,a);self.handle_endtag(t)
 def finish(self):
  if self.stack==['p']:self.optional.append('p_at_end_of_parent');self.stack=[]
  if self.stack:self.errors.append({'event':'unclosed_nonoptional_elements','open':self.stack})
  if self.rawdata:self.errors.append({'event':'unconsumed_markup','text':self.rawdata})
def check(s):p=Optional();p.feed(s);p.close();p.finish();return {'errors':p.errors,'optional':p.optional,'ignored':p.ignored}
inv=json.loads((H/'effective_body_inventory.json').read_text())['rows'];idx={(r['productIndex'],r['locale']):r for r in inv};original=json.loads((H/'additional_parser_inventory.json').read_text())['findings'];repairs=json.loads((H/'placeholder_candidates_v2.json').read_text())['rows'];ov={(r['productIndex'],r['locale']):r for r in repairs};rows=[]
for f in original:
 r=idx[f['productIndex'],f['locale']];b=check(r['expectedEffectiveBeforeValue']);a=check(ov.get((r['productIndex'],r['locale']),{}).get('value',r['expectedEffectiveBeforeValue']))
 status='NONOPTIONAL_STRUCTURE_ISSUE' if b['errors'] else 'IGNORED_EXTRA_UL_END_AND_OPTIONAL_CLOSURE' if b['ignored'] else 'VALID_OPTIONAL_END_TAG_OMISSION'
 rows.append({'productIndex':r['productIndex'],'resourceId':r['resourceId'],'locale':r['locale'],'outdated':r['before']['outdated'],'classification':status,'before':b,'afterPlaceholderRepairs':a,'placeholderRepairAuthored':(r['productIndex'],r['locale']) in ov})
report={'scope':193,'method':'Bounded HTML5 optional-end-tag semantics for li before next li/parent end and p before block/end of parent; unmatched ul end ignored as in browser tree construction. This is not a complete HTML5 parser. Inline/heading mismatches remain explicit defects.','counts':dict(collections.Counter(r['classification'] for r in rows)),'afterPlaceholderRemainingNonoptionalRows':sum(bool(r['afterPlaceholderRepairs']['errors']) for r in rows),'rows':rows}
(H/'optional_closure_classification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='rows'}));print(json.dumps([r for r in rows if r['afterPlaceholderRepairs']['errors']],ensure_ascii=False))
