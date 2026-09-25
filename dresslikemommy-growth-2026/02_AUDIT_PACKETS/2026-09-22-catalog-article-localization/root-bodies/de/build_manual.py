"""Offline full-body assembly from exact manually translated text nodes."""
from pathlib import Path
from html.parser import HTMLParser
import json, hashlib, importlib.util
BASE = Path(__file__).resolve().parent
class Spans(HTMLParser):
    def __init__(self,s):
        super().__init__(convert_charrefs=False); self.s=s; self.spans=[]; self.lines=[0]
        self.lines += [i+1 for i,c in enumerate(s) if c=='\n']
        self.feed(s); self.close()
    def absolute_offset(self):
        line,col=self.getpos(); return self.lines[line-1]+col
    def handle_starttag(self,tag,attrs):
        if tag in {'script','style'}: raise ValueError('Raw block requires review')
        a=self.absolute_offset(); self.spans.append((a,a+len(self.get_starttag_text())))
    def handle_startendtag(self,tag,attrs): self.handle_starttag(tag,attrs)
    def handle_endtag(self,tag):
        a=self.absolute_offset(); self.spans.append((a,self.s.index('>',a)+1))
    def handle_comment(self,data):
        a=self.absolute_offset(); self.spans.append((a,self.s.index('-->',a)+3))
    def handle_decl(self,data):
        a=self.absolute_offset(); self.spans.append((a,self.s.index('>',a)+1))
def parts(s):
    out=[]; start=0
    for a,b in Spans(s).spans:
        if a>start: out.append((False,s[start:a]))
        out.append((True,s[a:b]));start=b
    if start<len(s):out.append((False,s[start:]))
    assert ''.join(x[1] for x in out)==s
    return out
rows=json.loads((BASE.parent/'de_baseline.json').read_text())
segments={};data=[]
for r in rows:
    for tag,t in parts(r['sourceValue']):
        t=t.strip()
        if tag or not t:continue
        if t not in segments:
            segments[t]=str(len(data)+1);data.append({'id':str(len(data)+1),'source':t,'resources':[]})
        rec=data[int(segments[t])-1]
        if r['resourceId'] not in rec['resources']:rec['resources'].append(r['resourceId'])
(BASE/'source_segments.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
translations={};conflicts=[]
for r in rows:
    f=BASE/(r['resourceId'].split('/')[-1]+'.html')
    if not f.exists():continue
    sp=[x[1].strip() for x in parts(r['sourceValue']) if not x[0] and x[1].strip()]
    tp=[x[1].strip() for x in parts(f.read_text()) if not x[0] and x[1].strip()]
    if len(sp)!=len(tp):continue  # Full HTML stays authoritative; do not infer fragment alignment.
    for s,t in zip(sp,tp):
        id=segments[s]
        if id in translations and translations[id]!=t:
            conflicts.append({'id':id,'source':s,'first':translations[id],'other':t})
        else:translations[id]=t
for f in sorted(BASE.glob('manual_nodes_*.json')):
    for id,t in json.loads(f.read_text()).items():
        if id in translations and translations[id]!=t:raise ValueError('Conflicting explicit node '+id)
        translations[id]=t
(BASE/'reuse_variant_review.json').write_text(json.dumps(conflicts,ensure_ascii=False,indent=2)+'\n')
claims={x['resourceId']:x['claims'] for x in json.loads((BASE.parent.parent/'articles/source_claims_release_review.json').read_text())['articles']}
spec=importlib.util.spec_from_file_location('offline',BASE.parent.parent/'tooling/offline_translation.py');offline=importlib.util.module_from_spec(spec);spec.loader.exec_module(offline)
overrides={'gid://shopify/Article/559471919201':{'316':'passende Outfits'}}
candidates=[];progress=[];checks=[]
for r in rows:
    f=BASE/(r['resourceId'].split('/')[-1]+'.html')
    if f.exists():value=f.read_text().rstrip('\n');missing=[]
    else:
        out=[];missing=[]
        for tag,t in parts(r['sourceValue']):
            s=t.strip()
            if tag or not s:out.append(t);continue
            id=segments[s]
            if id not in translations:missing.append(id);out.append(t);continue
            target=overrides.get(r['resourceId'],{}).get(id,translations[id])
            prefix=t[:len(t)-len(t.lstrip())]
            if target[:1] in ',.;:!?':prefix=''
            out.append(prefix+target+t[len(t.rstrip()):])
        value=''.join(out)
    progress.append({'resourceId':r['resourceId'],'complete':not missing,'missingSegmentIds':sorted(set(missing),key=int)})
    if missing:continue
    c={**r,'value':value,'sourceClaimReview':claims.get(r['resourceId'],[])};candidates.append(c)
    checks.append({'resourceId':r['resourceId'],**offline.verify_text(r['sourceValue'],value,'de')})
(BASE/'candidate_all_complete.json').write_text(json.dumps({'status':'MANUAL_DRAFTS_FOR_INDEPENDENT_REVIEW','rows':candidates},ensure_ascii=False,indent=2)+'\n')
(BASE/'verification.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
(BASE/'progress.json').write_text(json.dumps({'total':len(rows),'completed':len(candidates),'translatedNodes':len(translations),'totalNodes':len(data),'articles':progress},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'total':len(rows),'completed':len(candidates),'translatedNodes':len(translations),'totalNodes':len(data),'structuralFailures':sum(bool(x['errors']) for x in checks),'reuseVariants':len(conflicts)}))
