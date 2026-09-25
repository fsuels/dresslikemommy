"""Preserve current Russian; replace exact manually translated English spans only."""
from pathlib import Path
from html.parser import HTMLParser
import re,json,hashlib,importlib.util,collections
P=Path(__file__).resolve().parent
ROOT=P.parents[2]
class Spans(HTMLParser):
    def __init__(self,s):
        super().__init__(convert_charrefs=False);self.s=s;self.spans=[];self.lines=[0]+[i+1 for i,c in enumerate(s) if c=='\n'];self.feed(s);self.close()
    def pos(self):
        l,c=self.getpos();return self.lines[l-1]+c
    def handle_starttag(self,t,a):
        x=self.pos();self.spans.append((x,x+len(self.get_starttag_text())))
    def handle_startendtag(self,t,a):self.handle_starttag(t,a)
    def handle_endtag(self,t):
        x=self.pos();self.spans.append((x,self.s.index('>',x)+1))
    def handle_comment(self,d):
        x=self.pos();self.spans.append((x,self.s.index('-->',x)+3))
    def handle_decl(self,d):
        x=self.pos();self.spans.append((x,self.s.index('>',x)+1))
def parts(s):
    out=[];last=0
    for a,b in Spans(s).spans:
        assert a>=last,'Inherited malformed/overlapping tags'
        if a>last:out.append((False,s[last:a]))
        out.append((True,s[a:b]));last=b
    if last<len(s):out.append((False,s[last:]))
    assert ''.join(t for _,t in out)==s
    return out
segments=json.loads((P/'english_segments.json').read_text());lookup={x['sourceSpan']:x['id'] for x in segments};manual={}
for f in sorted(P.glob('manual_*.json')):
    for k,v in json.loads(f.read_text()).items():
        assert k not in manual or manual[k]==v,'conflicting node'
        manual[k]=v
invariants={}
for s in segments:
    v=s['sourceSpan']
    v=re.sub(r'(?<![A-Za-z])(?:cm|in|inch|inches|kg|lbs|lb|mm|XXXL|XXL|XL|XS|S|M|L|T|Y|F)(?![A-Za-z])','',v)
    if not re.search('[A-Za-z]',v):invariants[s['id']]=s['sourceSpan']
spec=importlib.util.spec_from_file_location('off',ROOT/'tooling/offline_translation.py');off=importlib.util.module_from_spec(spec);spec.loader.exec_module(off)
rows=json.loads((P/'composition_baseline.json').read_text())['rows'];done=[];progress=[];checks=[];inverses=[]
for r in rows:
    if r['resourceId'].split('/')[-1] in {'7545279512673','7545279840353','7670724329569','7670744842337'}:
        progress.append({'resourceId':r['resourceId'],'missingSegmentIds':[],'complete':False,'disposition':'NO_ENGLISH_PROSE_GAP_NAMED_LABELS_PRESERVED'})
        continue
    missing=[];out=[];patches=[]
    for tag,t in parts(r['compositionValue']):
        text=t.strip();id=lookup.get(text)
        if tag or not id:out.append(t);continue
        value=manual.get(id,invariants.get(id))
        if value is None:missing.append(id);out.append(t);continue
        out.append(t[:len(t)-len(t.lstrip())]+value+t[len(t.rstrip()):])
        if value!=text:patches.append({'segmentId':id,'before':text,'value':value})
    progress.append({'resourceId':r['resourceId'],'missingSegmentIds':sorted(set(missing),key=int),'complete':not missing})
    if missing:continue
    value=''.join(out);a,b=off.Shape(r['compositionValue']),off.Shape(value)
    errors=[]
    if a.events!=b.events:errors.append('NEW_html_structure_or_attributes_changed')
    if re.findall(r'\d+(?:[.,]\d+)*',''.join(a.text))!=re.findall(r'\d+(?:[.,]\d+)*',''.join(b.text)):errors.append('NEW_numeric_lexemes_changed')
    if collections.Counter(off.URL.findall(r['compositionValue']))!=collections.Counter(off.URL.findall(value)):errors.append('NEW_urls_or_emails_changed')
    assert not errors,(r['resourceId'],errors)
    sourcecheck=off.verify_text(r['source'],value,'ru')
    c={k:v for k,v in r.items() if k!='compositionValue'}
    c.update({'value':value,'reason':'Remaining verified English spans translated manually; existing Russian preserved.','manualTextNodePatches':patches,'status':'INDEPENDENT_REVIEW_REQUIRED' if not sourcecheck['errors'] else 'INHERITED_SOURCE_MISMATCH_REVIEW_REQUIRED','sourceComparisonFindings':sourcecheck['errors'],'valueSHA256':hashlib.sha256(value.encode()).hexdigest()});done.append(c)
    checks.append({'resourceId':r['resourceId'],'newMutationErrors':errors,'sourceComparison':sourcecheck,'inheritedFindings':r['inheritedStructuralFindings']})
    inverses.append({'resourceId':r['resourceId'],'locale':'ru','key':'body_html','before':r['before'],'value':r['before']['value'] if r['before'] else None,'sourceDigest':r['sourceDigest']})
(P/'candidates_complete.json').write_text(json.dumps({'status':'OFFLINE_MANUAL_CANDIDATES_NOT_APPLIED','rows':done},ensure_ascii=False,indent=2)+'\n')
(P/'inverses_complete.json').write_text(json.dumps({'rows':inverses},ensure_ascii=False,indent=2)+'\n')
(P/'checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
(P/'technical_invariants.json').write_text(json.dumps(invariants,ensure_ascii=False,indent=2)+'\n')
(P/'progress.json').write_text(json.dumps({'inspectedRows':118,'boundRowsPresentIn514RowBaseline':118,'statisticalNamedLabelRowsIncluded':2,'compositionRows':116,'malformedBlocked':2,'noEnglishProseGap':4,'completed':len(done),'manualNodes':len(manual),'invariantNodes':len(invariants),'totalNodes':len(segments),'rows':progress},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'complete':len(done),'newErrors':0,'inheritedSourceMismatchCandidates':sum(bool(x['sourceComparison']['errors']) for x in checks),'manualNodes':len(manual),'invariants':len(invariants)}))
