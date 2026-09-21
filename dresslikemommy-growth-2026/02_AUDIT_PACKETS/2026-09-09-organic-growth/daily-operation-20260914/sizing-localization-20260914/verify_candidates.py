"""Release-local, read-only candidate checks; no store writes or publication authority."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib, json, sys

BASE = Path(__file__).resolve().parent
SOURCE = 'c1c3ca1fa58097d25857d12fb361f82ac60ae7d45f5545a717ca9a6ab04aea88'
BLOCKS = {'p','h2','th','td','li'}

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

class Html(HTMLParser):
    def __init__(self, s):
        super().__init__(convert_charrefs=True)
        self.elements, self.stack, self.blocks, self.errors = [], [], [], []
        self.feed(s); self.close()
        if self.stack: self.errors.append('unclosed tags')
    def handle_starttag(self, tag, attrs):
        n={'tag':tag,'attrs':dict(attrs),'text':''}
        self.elements.append(n); self.stack.append(n)
        if tag in BLOCKS: self.blocks.append(n)
    def handle_endtag(self, tag):
        if not self.stack or self.stack[-1]['tag'] != tag: self.errors.append('mismatched '+tag)
        elif self.stack: self.stack.pop()
    def handle_data(self, s):
        for n in self.stack: n['text'] += s

def report():
    inventory=json.loads((BASE/'LOCALE_INVENTORY.json').read_text())
    routes=json.loads((BASE/'ROUTES.json').read_text())
    original=Html((BASE/'english-before.html').read_text())
    source=Html((BASE/'english-final.html').read_text())
    assert sha(BASE/'english-final.html') == SOURCE
    unchanged=[i for i,(a,b) in enumerate(zip(original.blocks,source.blocks)) if a['text']==b['text']]
    rows=[]
    for row in inventory['existing_bodies']:
        lc=row['locale']; d=BASE/'locales'/lc
        if not (d/'candidate.html').exists():
            rows.append({'locale':lc,'status':'MISSING'}); continue
        before=Html((d/'before.html').read_text()); candidate=Html((d/'candidate.html').read_text())
        notes=json.loads((d/'AUTHOR_NOTES.json').read_text())
        ce=candidate.elements[1:] if lc in ('ar','he') else candidate.elements
        checks={
            'before_hash':sha(d/'before.html')==row['before_sha256'],
            'author_before_hash':notes['before_sha256']==sha(d/'before.html'),
            'author_candidate_hash':notes['candidate_sha256']==sha(d/'candidate.html'),
            'author_source_hash':(notes['source_sha256'].get('english-final.html') if isinstance(notes['source_sha256'],dict) else notes['source_sha256'])==SOURCE,
            'balanced_html':not candidate.errors,
            'same_element_sequence':[e['tag'] for e in ce]==[e['tag'] for e in source.elements],
            'same_31_blocks':len(candidate.blocks)==len(source.blocks)==31,
            'nine_unchanged_blocks':len(unchanged)==9 and all(candidate.blocks[i]['text']==before.blocks[i]['text'] for i in unchanged),
            'four_localized_links':[e['attrs'].get('href') for e in ce if e['tag']=='a']==[routes[lc][k] for k in ['shopping','contact','shopping','contact']],
            'table_and_12_cell_styles':all(a['attrs'].get('style')==b['attrs'].get('style') for a,b in zip(ce,source.elements) if b['tag'] in {'table','th','td'}),
            'only_expected_attributes':all(a['attrs']==(dict(b['attrs'],href=routes[lc]['shopping'] if 'collections' in b['attrs']['href'] else routes[lc]['contact']) if b['tag']=='a' else b['attrs']) for a,b in zip(ce,source.elements)),
            'rtl_wrapper_correct':lc not in ('ar','he') or candidate.elements[0]==dict(tag='div',attrs={'dir':'rtl','lang':lc,'style':'text-align: right;'},text=candidate.elements[0]['text']),
        }
        review=None
        if (d/'REVIEW.json').exists():
            review=json.loads((d/'REVIEW.json').read_text())
            expected_reviewer=('/root/sizing_locales_c' if lc in ['de','fr','es','it','pt-BR','nl'] else '/root/daily_operation_review' if lc in ['cs','da','fi','no','pl','ro'] else '/root/sizing_locales_b')
            review_source=review.get('source_sha256')
            review_source=review_source.get('english-final.html') if isinstance(review_source,dict) else review_source
            checks.update(review_hash=review.get('candidate_sha256')==sha(d/'candidate.html'),review_source=review_source==SOURCE,review_pass=review.get('status',review.get('verdict')) in ['PASS','PASS_WITH_LIMITS'],reviewer_independent=bool(review.get('reviewer')) and review.get('reviewer')!=notes.get('author') and review.get('reviewer')==expected_reviewer)
        else: checks['review_present']=False
        rows.append({'locale':lc,'candidate_sha256':sha(d/'candidate.html'),'author':notes.get('author'),'reviewer':review.get('reviewer') if review else None,'checks':checks,'status':'PASS' if all(checks.values()) else 'HOLD'})
    return {'source_sha256':SOURCE,'rows':rows,'status':'PASS' if len(rows)==18 and all(r['status']=='PASS' for r in rows) else 'HOLD','checks_passed':sum(sum(r.get('checks',{}).values()) for r in rows),'checks_total':sum(len(r.get('checks',{})) for r in rows),'limit':'Static structure, scope and hash verification; separate language review and live after-state required.'}

if __name__=='__main__':
    result=report()
    (BASE/'candidate-verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'checks_passed':result['checks_passed'],'checks_total':result['checks_total'],'holds':[{'locale':r['locale'],'failed':[k for k,v in r.get('checks',{}).items() if not v]} for r in result['rows'] if r['status']!='PASS']}))
    sys.exit(0 if result['status']=='PASS' else 1)
