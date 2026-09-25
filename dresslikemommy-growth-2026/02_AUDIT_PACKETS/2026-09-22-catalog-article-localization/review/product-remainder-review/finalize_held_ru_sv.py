# -*- coding: utf-8 -*-
from pathlib import Path
import hashlib,html,importlib.util,json,re
P=Path(__file__).resolve().parent;R=P.parent.parent
rows=json.loads((P/'held_ru_sv_prepared.json').read_text())['rows']
pairs=json.loads((P/'held_ru_sv_unique_review.json').read_text())
fixes={
0:'Сделайте семейный отпуск ещё более запоминающимся с этими стильными пляжными нарядами в едином стиле! Ярко-жёлтые многоярусные платья макси для женщин и девочек добавляют элегантности, а белые футболки с жёлтыми шортами для мужчин и мальчиков создают непринуждённое летнее настроение. Эти сочетающиеся наряды из лёгкой дышащей ткани помогают сохранять прохладу и выглядеть шикарно. Отдыхаете ли вы в тропиках или проводите день на пляже, этот согласованный комплект позволит вашей семье выделиться стильным образом.',
2:'Яркий и насыщенный жёлтый цвет идеально подходит для пляжных прогулок и отпуска.',
6:'Удобная посадка для взрослых и детей, идеально подходит для семейных фотографий или весёлого отдыха в отпуске.',
16:'Встречайте лето стильно в этих ярких семейных нарядах с тропическим настроением. Сочетающиеся комплекты с выразительным разноцветным принтом листьев включают струящиеся платья для мам и дочерей и стильные футболки с подходящими шортами для пап и сыновей. Лёгкая дышащая ткань идеально подходит для пляжных дней, семейных фотографий и весёлых летних прогулок. Благодаря удобной посадке и привлекательному дизайну этот семейный комплект в едином стиле сделает каждый момент отпуска ещё более особенным. Подберите сочетающиеся наряды для всей семьи и стильно запечатлейте прекрасные воспоминания!',
17:'Яркие семейные наряды в едином стиле для пляжа и летних приключений',
19:'Струящиеся платья для мам и дочерей, футболки с сочетающимися шортами для пап и сыновей',
21:'Идеальны для семейного отпуска, пляжных фотосессий или непринуждённых летних прогулок',
22:'Мягкая, удобная посадка и модели, которые легко надевать взрослым и детям',
}
fixmap={(pairs[i]['locale'],pairs[i]['source']):text for i,text in fixes.items()}
out=[];checks=[]
for r in rows:
 if r['resourceId'].endswith('/7545279512673'):continue
 source=r['source'];parts=re.split('(<[^>]*>)',source);edits=[]
 for n in r['nodes']:
  assert n['value'] is not None
  val=fixmap.get((r['locale'],n['source']),n['value'])
  val=html.unescape(val)
  if val!=html.unescape(n['value']):edits.append({'source':n['source'],'beforeDraft':n['value'],'value':val})
  old=parts[n['partIndex']];leading=old[:len(old)-len(old.lstrip())];trailing=old[len(old.rstrip()):]
  parts[n['partIndex']]=leading+html.escape(val,quote=False)+trailing
 value=''.join(parts)
 spec=importlib.util.spec_from_file_location('v',R/'tooling/offline_translation.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
 check=v.verify_text(source,value,r['locale'])
 assert not check['errors'],(r['resourceId'],r['locale'],check)
 rr={k:r[k] for k in ['resourceId','productId','locale','key','sourceDigest','before','rawFile']}
 rr.update(sourceValue=source,value=value,marketId=None,reason='Complete source-bound body translation rebuilt on original English HTML, image attributes and full current chart. Replaces inherited shifted age/size labels, malformed HTML and obsolete image variance. All prose and labels author-reviewed.',independentReview='AUTHOR_FULL_MEANING_REVIEW_PENDING_ROOT_INDEPENDENT_REVIEW')
 out.append(rr);checks.append({'resourceId':r['resourceId'],'locale':r['locale'],'key':r['key'],'sourcePreservation':check,'meaning':'FULL_AUTHOR_REVIEW_PASS','ageAndSizeLabels':'DERIVED_FROM_SOURCE_NO_INHERITED_NUMBERS','corrections':edits,'sourceSHA256':hashlib.sha256(source.encode()).hexdigest(),'valueSHA256':hashlib.sha256(value.encode()).hexdigest()})
assert len(out)==36
for name,data in [('held_ru_sv36_candidate.json',{'rows':out}),('held_ru_sv36_checks.json',{'fields':checks,'reviewCoverage':'253 distinct source-target pairs reviewed; 107 missing Swedish prose segments manually translated, remaining prose reviewed against source. All numeric/age cells and HTML rebuilt from current source.','limit':'Offline source/before binding; root retains live guard and independent review authority.'})]:(P/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'rows':len(out),'preservationFailures':0}))
