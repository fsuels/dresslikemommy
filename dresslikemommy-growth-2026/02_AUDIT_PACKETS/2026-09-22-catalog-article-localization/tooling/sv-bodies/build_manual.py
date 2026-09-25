"""Exact manual text-node reuse. Standard library only, no API/provider calls."""
from html.parser import HTMLParser
from pathlib import Path
import hashlib,json,sys
BASE=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE.parent))
from offline_translation import verify_rows
class Spans(HTMLParser):
    def __init__(self,s):
        super().__init__(convert_charrefs=False);self.s=s;self.spans=[]
        self.lines=[0]
        for i,c in enumerate(s):
            if c=='\n':self.lines.append(i+1)
        self.feed(s);self.close()
    def absolute_offset(self):
        line,col=self.getpos();return self.lines[line-1]+col
    def handle_starttag(self,tag,attrs):
        if tag in {'script','style'}:raise ValueError('Manual raw block review required')
        a=self.absolute_offset();self.spans.append((a,a+len(self.get_starttag_text())))
    def handle_startendtag(self,tag,attrs):self.handle_starttag(tag,attrs)
    def handle_endtag(self,tag):
        a=self.absolute_offset();self.spans.append((a,self.s.index('>',a)+1))
    def handle_comment(self,data):
        a=self.absolute_offset();self.spans.append((a,self.s.index('-->',a)+3))
    def handle_decl(self,data):
        a=self.absolute_offset();self.spans.append((a,self.s.index('>',a)+1))
def parts(s):
    out=[];start=0
    for a,b in Spans(s).spans:
        if a>start:out.append((False,s[start:a]))
        out.append((True,s[a:b]));start=b
    if start<len(s):out.append((False,s[start:]))
    assert ''.join(p[1] for p in out)==s
    return out
rows=[r for p in sorted(BASE.glob('source_batch_*.json')) for r in json.loads(p.read_text())['rows']]
segments={};data=[]
for r in rows:
    for tag,text in parts(r['sourceValue']):
        if tag or not text.strip():continue
        text=text.strip()
        if text not in segments:
            segments[text]=str(len(data)+1);data.append({'id':str(len(data)+1),'source':text,'resources':[]})
        rec=data[int(segments[text])-1]
        if r['resourceId'] not in rec['resources']:rec['resources'].append(r['resourceId'])
(BASE/'source_segments.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
translations={}
for p in sorted(BASE.glob('manual_*.json')):
    for k,v in json.loads(p.read_text()).items():
        if k in translations and translations[k]!=v:raise ValueError('Conflicting manual translation '+k)
        translations[k]=v
candidates=[];progress=[]
for r in rows:
    missing=[];out=[]
    for tag,text in parts(r['sourceValue']):
        trimmed=text.strip()
        if tag or not trimmed:out.append(text);continue
        id=segments[trimmed]
        if id not in translations:missing.append(id);out.append(text);continue
        prefix=text[:len(text)-len(text.lstrip())];suffix=text[len(text.rstrip()):]
        # A translated clause may move its final word before an inline link.
        # Swedish punctuation then attaches directly to the preceding text.
        if translations[id][:1] in '.,:;!?':prefix=''
        out.append(prefix+translations[id]+suffix)
    progress.append({'resourceId':r['resourceId'],'missingSegmentIds':sorted(set(missing),key=int),'complete':not missing})
    if not missing:
        candidate={**r,'source':r['sourceValue'],'value':''.join(out),'reason':'Confirmed missing Swedish article body; manually translated from exact source with reviewed text-node reuse; independent meaning review required.'}
        candidate['valueSHA256']=hashlib.sha256(candidate['value'].encode()).hexdigest();candidates.append(candidate)
(BASE/'candidate.json').write_text(json.dumps({'rows':candidates},ensure_ascii=False,indent=2)+'\n')
report=verify_rows(candidates,[{**r,'source':r['sourceValue']} for r in rows])
(BASE/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
(BASE/'progress.json').write_text(json.dumps({'translatedSegments':len(translations),'totalSegments':len(data),'completedArticles':len(candidates),'totalArticles':len(rows),'articles':progress},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'segments':len(data),'translated':len(translations),'articlesComplete':len(candidates),'verification':report['status'],'failedRows':report['failedRows']}))
