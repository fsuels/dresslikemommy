"""Read-only comparison of the exact article release inputs and captured API states."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib, json, re, sys, unicodedata
from datetime import datetime, timezone

BASE = Path(__file__).resolve().parent
TARGET = 'gid://shopify/Article/559471886433'
LOCALES = ['ar','cs','da','de','el','es','fi','fr','he','hi','it','ja','ko','nl','no','pt-BR','ro']
PROTECTED = ['id','title','handle','summary','tags','templateSuffix','isPublished','publishedAt','createdAt','author','blog','image']

def read(name): return json.loads((BASE/name).read_text())
def data(name):
    obj = read(name)
    assert not obj.get('errors'), obj.get('errors')
    return obj['data']
def sha(s): return hashlib.sha256(s.encode()).hexdigest()
def file_sha(name): return hashlib.sha256((BASE/name).read_bytes()).hexdigest()
def timestamp(s): return datetime.fromisoformat(s.replace('Z','+00:00'))
def rows(obj):
    resource = obj['translatableResource']
    assert resource['resourceId'] == TARGET, 'Wrong global translation resource identity'
    pairs = [((r['locale'],r['key'],r['market']['id'] if r['market'] else None),r)
             for a,v in resource.items() if re.fullmatch(r'l\d+',a) for r in v]
    assert len(dict(pairs)) == len(pairs), 'Duplicate translation identity'
    return dict(pairs)

class Blocks(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True); self.blocks=[]; self.active=None; self.text=[]; self.tags=[]; self.links=[]; self.stack=[]; self.errors=[]
    def handle_starttag(self,t,attrs):
        self.tags.append(t); d=dict(attrs)
        if t=='a': self.links.append(d.get('href'))
        if t in ['h2','p','li']:
            if self.active: self.errors.append('nested block')
            self.active=t; self.text=[]
        if t not in ['br','hr','img','meta','link','input']: self.stack.append(t)
        if any(k.lower().startswith('on') for k,v in attrs) or t in ['script','iframe','form','style']: self.errors.append('active markup')
    def handle_data(self,s):
        if self.active: self.text.append(s)
    def handle_endtag(self,t):
        if t==self.active:
            self.blocks.append(unicodedata.normalize('NFC',re.sub(r'\s+',' ',''.join(self.text)).strip()));self.active=None
        if not self.stack or self.stack[-1]!=t:self.errors.append('unbalanced '+t)
        else:self.stack.pop()

def candidate_check():
    checks={}; en=(BASE/'gift-guide-candidate.html').read_text(); ep=Blocks();ep.feed(en)
    expected={}
    for locale in ['en']+LOCALES:
        path=BASE/'gift-guide-candidate.html' if locale=='en' else BASE/'locales'/locale/'candidate.html'
        s=path.read_text(); p=Blocks();p.feed(s); prefix='' if locale=='en' else '/'+('pt' if locale=='pt-BR' else locale)
        links=[prefix+x if x.startswith('/') else x for x in ep.links]
        checks[locale+'_balanced_safe_html']=not p.errors and not p.stack
        checks[locale+'_structure']=([t for t in p.tags if t!='div']==[t for t in ep.tags if t!='div'])
        checks[locale+'_eight_links']=p.links==links and len(p.links)==8
        checks[locale+'_six_headings']=p.tags.count('h2')==6
        if locale in ['ar','he']:checks[locale+'_rtl']='dir="rtl"' in s and 'lang="'+locale+'"' in s
        if locale!='en':
            author=read('locales/'+locale+'/AUTHOR_NOTES.json'); review=read('locales/'+locale+'/REVIEW.json')
            checks[locale+'_author_hashes']=author['source_sha256']==sha(en) and author['candidate_sha256']==sha(s) and author['before_sha256']==file_sha('locales/'+locale+'/before.html')
            checks[locale+'_independent_review']=review['status'] in ['PASS','PASS_WITH_LIMITS'] and review['reviewer']!=author['author'] and review['candidate_sha256']==sha(s) and review['source_sha256']==sha(en)
            checks[locale+'_review_input_bindings']=all(file_sha(k)==v for k,v in review['input_sha256'].items())
        expected[locale]={'file':str(path.relative_to(BASE)),'sha256':sha(s),'blocks_count':len(p.blocks),'normalized_blocks_sha256':sha('\n'.join(p.blocks)),'links':p.links}
    english=read('ENGLISH_RELEASE_SUPPLEMENT_REVIEW.json')
    checks['english_current_independent_review']=english['status'] in ['PASS','PASS_WITH_LIMITS'] and english['english_candidate_sha256']==sha(en) and english['reviewer']!='/root' and not english['blocking_findings']
    checks['english_review_input_bindings']=all(file_sha(k)==v for k,v in english['source_sha256'].items())
    return checks,expected

def verify(stage):
    assert stage in ['prewrite','after-english','after']
    checks={}; before=data('gift-guide-inventory.json');now=data(stage+'-inventory.json')
    oldt=rows(data('gift-guide-translations.json')); newt=rows(data(stage+'-translations.json'))
    oldm=data('gift-guide-market-translations.json');newm=data(stage+'-market-translations.json')
    en=(BASE/'gift-guide-candidate.html').read_text()
    checks['target']=before['article']['id']==now['article']['id']==TARGET
    checks['source_resource_identity']=before['translatableResource']['resourceId']==now['translatableResource']['resourceId']==TARGET
    checks['shop']=before['shop']==now['shop']
    checks['locale_inventory']=before['shopLocales']==now['shopLocales'] and len(now['shopLocales'])==21
    checks['market_inventory']=before['markets']==now['markets'] and not now['markets']['pageInfo']['hasNextPage']
    checks['six_empty_market_contexts']=oldm==newm and len(newm)==6 and all(v==[] for r in newm.values() for a,v in r.items() if a!='resourceId')
    checks['market_resource_identities']=all(r['resourceId']==TARGET for r in newm.values())
    for k in PROTECTED:checks['article_'+k]=before['article'][k]==now['article'][k]
    checks['english_body']=now['article']['body']==(before['article']['body'] if stage=='prewrite' else en)
    if stage=='prewrite':checks['article_timestamp_unchanged']=before['article']['updatedAt']==now['article']['updatedAt']
    oldsrc={r['key']:r for r in before['translatableResource']['translatableContent']}; newsrc={r['key']:r for r in now['translatableResource']['translatableContent']}
    checks['source_keys']=set(oldsrc)==set(newsrc) and len(newsrc)==5
    for k,v in oldsrc.items():
        if k=='body_html' and stage!='prewrite':checks['english_source_body']=newsrc[k]['value']==en and newsrc[k]['digest']==sha(en) and newsrc[k]['locale']=='en' and newsrc[k]['type']==v['type']
        else:checks['source_'+k]=newsrc[k]==v
    checks['translation_identities']=set(oldt)==set(newt) and len(newt)==53
    checks['seventeen_existing_bodies']={k[0] for k in oldt if k[1]=='body_html'}==set(LOCALES)
    for k,v in oldt.items():
        locale,key,market=k; n=newt.get(k,{})
        if key=='body_html' and stage=='after':
            checks['body_'+locale]=n.get('value')==(BASE/'locales'/locale/'candidate.html').read_text() and n.get('outdated') is False and n.get('market') is None
        elif key=='body_html' and stage=='after-english':
            allowed={'outdated','updatedAt'}
            checks['unmodified_body_translation_'+locale]={x:y for x,y in n.items() if x not in allowed}=={x:y for x,y in v.items() if x not in allowed}
            checks['body_flag_'+locale]=n.get('outdated') is True
            checks['body_timestamp_'+locale]=timestamp(v['updatedAt'])<=timestamp(n['updatedAt'])<=timestamp(read(stage+'-translations.json')['completed_at_utc'])
        else:checks['translation_'+locale+'_'+key]=n==v
    request=read('english-mutation-request.json')['variables']
    checks['english_exact_body_only_payload']=request=={'id':TARGET,'article':{'body':en}}
    checks['english_rollback']=read('english-rollback-request.json')['variables']=={'id':TARGET,'article':{'body':before['article']['body']}}
    return checks

def payload_check(bound=False):
    checks={}; name='translations-mutation-request.json' if bound else 'translations-mutation-template.json'
    request=read(name); variables=request['variables']; source=data('after-english-inventory.json') if bound else None
    digest=next(r['digest'] for r in source['translatableResource']['translatableContent'] if r['key']=='body_html') if bound else 'FRESH_BODY_DIGEST_REQUIRED_AFTER_ENGLISH_SAVE'
    checks['mutation_resource']=variables.get('id')==TARGET and set(variables)=={'id','translations'}
    rows_=variables['translations']; checks['exact_seventeen']=len(rows_)==17 and sorted(r['locale'] for r in rows_)==sorted(LOCALES)
    for r in rows_:
        locale=r['locale']; checks['payload_'+locale]=r=={'locale':locale,'key':'body_html','value':(BASE/'locales'/locale/'candidate.html').read_text(),'translatableContentDigest':digest}
    checks['query_exact']=request['query']==(BASE/'translation-mutation.graphql').read_text().strip()
    rollback=read('translations-rollback-template.json'); before=rows(data('gift-guide-translations.json'))
    checks['rollback_scope']=rollback['variables']['id']==TARGET and len(rollback['variables']['translations'])==17 and {r['locale'] for r in rollback['variables']['translations']}==set(LOCALES)
    for r in rollback['variables']['translations']:
        locale=r['locale']; checks['rollback_'+locale]=r=={'locale':locale,'key':'body_html','value':before[(locale,'body_html',None)]['value'],'translatableContentDigest':'FRESH_BODY_DIGEST_REQUIRED_AFTER_ENGLISH_RESTORE'}
    if bound:checks['source_digest_exact_current_candidate']=digest==file_sha('gift-guide-candidate.html') and source['article']['body']==(BASE/'gift-guide-candidate.html').read_text() and source['translatableResource']['resourceId']==TARGET
    return checks

if __name__=='__main__':
    stage=sys.argv[1]
    if stage=='candidates':
        checks,expected=candidate_check();(BASE/'EXPECTED_PUBLIC_CONTENT.json').write_text(json.dumps(expected,ensure_ascii=False,indent=2)+'\n')
    elif stage in ['payload-template','payload-bound']: checks=payload_check(stage=='payload-bound')
    else:checks=verify(stage)
    result={'stage':stage,'status':'PASS' if all(checks.values()) else 'FAILED','passed':sum(checks.values()),'total':len(checks),'checks':checks,'limitations':'Source/preservation and structural checks only; independent language/source review and actual public rendering remain separate.'}
    (BASE/('verification-'+stage+'.json')).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='checks'}));print('Failed:',[k for k,v in checks.items() if not v])
    sys.exit(0 if all(checks.values()) else 1)
