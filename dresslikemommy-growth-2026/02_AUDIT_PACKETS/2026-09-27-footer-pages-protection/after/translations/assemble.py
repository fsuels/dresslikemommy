"""Assemble tr/<locale>/<resource>__<field>.txt files into tr/<locale>.json. Usage: python3 assemble.py <locale>"""
import json,sys,os,glob
here=os.path.dirname(os.path.abspath(__file__))
loc=sys.argv[1]; out={}
for p in sorted(glob.glob(os.path.join(here,loc,'*__*.txt'))):
    k,f=os.path.basename(p)[:-4].split('__')
    out.setdefault(k,{})[f]=open(p,encoding='utf-8').read().strip()+('\n' if f=='body' else '')
json.dump(out,open(os.path.join(here,f'{loc}.json'),'w'),ensure_ascii=False,indent=1)
print(loc,len(out),'resources')
