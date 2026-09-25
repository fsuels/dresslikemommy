import json,re,html,hashlib,importlib.util
from pathlib import Path
P=Path(__file__).resolve().parent
ROOT=P.parent
spec=importlib.util.spec_from_file_location('offline',ROOT.parent/'tooling/offline_translation.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
claims={r['resourceId']:r['claims'] for r in json.loads((ROOT.parent/'articles/source_claims_release_review.json').read_text())['articles']}
def build(locale):
 sources=json.loads((ROOT/f'{locale}_source_texts.json').read_text())
 if locale=='he': vals=json.loads((ROOT/'he_000.json').read_text())+json.loads((ROOT/'he_045.json').read_text())+(P/'he_095.txt').read_text().splitlines()
 else:
  vals=[]
  for f in sorted(P.glob('pl_[0-9][0-9][0-9].txt')): vals+=f.read_text().splitlines()
 assert len(vals)==len(sources),(locale,len(vals),len(sources))
 translations=dict(zip(sources,vals)); rows=[]
 for base in json.loads((ROOT/f'{locale}_baseline.json').read_text()):
  def sub(match):
   txt=match.group(); key=html.unescape(txt).strip()
   if not key:return txt
   assert key in translations,(locale,key)
   return txt[:len(txt)-len(txt.lstrip())]+html.escape(translations[key],quote=False)+txt[len(txt.rstrip()):]
  source=base['sourceValue'];target=re.sub(r'(?<=>)[^<]+(?=<)|^[^<]+(?=<)|(?<=>)[^<]+$',sub,source)
  row={**base,'source':source,'value':target,'translationMethod':'manual_text_node_translation_exact_template_reuse','releaseStatus':'HOLD_SOURCE_CLAIMS' if base['resourceId'] in claims else 'CANDIDATE_REQUIRES_INDEPENDENT_REVIEW','sourceClaimHolds':claims.get(base['resourceId'],[])}
  rows.append(row)
 baseline=[{**r,'source':r['sourceValue']} for r in json.loads((ROOT/f'{locale}_baseline.json').read_text())]
 report=m.verify_rows(rows,baseline)
 (P/f'{locale}_candidate.json').write_text(json.dumps({'status':'OFFLINE_CANDIDATES_ONLY','rows':rows},ensure_ascii=False,indent=2)+'\n')
 (P/f'{locale}_checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 (P/f'{locale}_first5_candidate.json').write_text(json.dumps({'status':'OFFLINE_CANDIDATES_ONLY','rows':rows[:5]},ensure_ascii=False,indent=2)+'\n')
 (P/f'{locale}_text_map.json').write_text(json.dumps(dict(zip(sources,vals)),ensure_ascii=False,indent=2)+'\n')
 print(locale,report['status'],len(rows),[(r['resourceId'],r['errors']) for r in report['rows'] if r['errors']])
if __name__=='__main__':
 import sys
 for locale in sys.argv[1:]:build(locale)
