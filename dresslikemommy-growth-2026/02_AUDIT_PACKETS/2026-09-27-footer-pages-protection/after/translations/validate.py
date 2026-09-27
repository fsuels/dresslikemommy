"""Validate tr/<locale>.json against tr/source_en.json: same keys, same HTML tag/attribute skeleton. Usage: python3 validate.py <locale>"""
import json,sys,re,os
from html.parser import HTMLParser
here=os.path.dirname(os.path.abspath(__file__))
class Sk(HTMLParser):
    def __init__(s): super().__init__(); s.out=[]
    def handle_starttag(s,t,a): s.out.append((t,tuple((k,v) for k,v in a if k not in ('placeholder',))))
    def handle_endtag(s,t): s.out.append(('/'+t,))
def sk(h): p=Sk(); p.feed(h); return p.out
src=json.load(open(os.path.join(here,'source_en.json')))
bad=0
for loc in sys.argv[1:]:
    t=json.load(open(os.path.join(here,f'{loc}.json')))
    for k,e in src.items():
        if k not in t: print(loc,'MISSING resource',k); bad+=1; continue
        for f,v in e.items():
            tv=t[k].get(f)
            if not tv: print(loc,'MISSING field',k,f); bad+=1; continue
            if f=='body':
                a,b=sk(v),sk(tv)
                if a!=b:
                    i=next((i for i,(x,y) in enumerate(zip(a,b)) if x!=y),min(len(a),len(b)))
                    print(loc,'HTML skeleton differs',k,'at',i,a[i:i+2],b[i:i+2]); bad+=1
                for must in ['info@dresslikemommy.com','FKG Trading LLC']:
                    if v.count(must)!=tv.count(must): print(loc,'token count differs',k,must); bad+=1
                if tv.strip()==v.strip(): print(loc,'UNTRANSLATED',k); bad+=1
    print(loc,'OK' if not bad else f'{bad} problems')
sys.exit(1 if bad else 0)
