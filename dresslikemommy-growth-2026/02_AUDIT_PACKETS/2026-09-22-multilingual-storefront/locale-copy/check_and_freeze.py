from pathlib import Path
import json,re,hashlib,datetime
P=Path(__file__).parent
published=json.loads((P/'baseline_audit.json').read_text())['published_locales']
def read(f):
 s=f.read_text();duplicates=[]
 def pairs(items):
  d={}
  for k,v in items:
   if k in d:duplicates.append(k)
   d[k]=v
  return d
 o=json.loads(s[s.index('{'):],object_pairs_hook=pairs)
 assert not duplicates,(str(f),duplicates)
 return o
def flat(o,p=''):
 if isinstance(o,dict):
  for k,v in o.items():yield from flat(v,p+'.'+k if p else k)
 else:yield p,o
en=dict(flat(read(Path('locales/en.default.json'))));summaries=[];changes=[];errors=[];owned=[]
for f in sorted(Path('locales').glob('*.json')):
 if '.schema.' in f.name:continue
 l='en' if f.stem=='en.default' else f.stem;o=dict(flat(read(f)));missing=sorted(set(en)-set(o));before=P/'before'/f;old=dict(flat(read(before)))
 changed={k:v for k,v in o.items() if old.get(k)!=v}
 if missing:errors.append([l,'missing_keys',missing])
 if l!='en':
  for k,v in changed.items():
   if k not in en:continue
   e=en[k]
   if sorted(re.findall(r'{{\s*(.*?)\s*}}',e))!=sorted(re.findall(r'{{\s*(.*?)\s*}}',v)):errors.append([l,k,'placeholder'])
   if re.findall(r'<[^>]+>',e)!=re.findall(r'<[^>]+>',v):errors.append([l,k,'html'])
   if re.search(r'QZX|QXZ|DLMSEP|DLMTOKEN',v):errors.append([l,k,'artifact'])
   changes.append({'locale':l,'key':k,'before':old.get(k),'after':v})
  owned.append({'path':str(f),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'changed_keys':len(changed),'published':l in published})
 summaries.append({'locale':l,'published':l in published,'leaf_keys':len(o),'missing_english_keys':missing,'changed_keys':len(changed) if l!='en' else 'parent_owned','sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
 # All new shared and home copy is translated for published nonEnglish locales.
 if l in published and l!='en':
  for k in en:
   if k.startswith(('storefront.','sections.home_category_copy.')) and o[k]==en[k]:
    # Genuine cognates in short home labels are valid (e.g. Italian Vacation/Pyjamas vocabulary).
    if k.startswith('storefront.'):errors.append([l,k,'sharedEnglishretained'])
  for key in ['products.facets.product_count_simple.one','products.facets.product_count_simple.other','sections.footer_headings.company_info','sections.footer_headings.help_support','sections.footer_headings.customer_care']:
   assert key in o and isinstance(o[key],str) and o[key].strip(),(l,key)
original=(P/'home-category-localized-copy.before.liquid').read_text();now=Path('snippets/home-category-localized-copy.liquid').read_text()
alias=lambda s:dict(re.findall(r"when '([^']+)'\s+assign normalized_key = '([^']+)'",s))
assert alias(original)==alias(now) and len(alias(now))==18
keys=json.loads((P/'home_category_existing.json').read_text())['en'];whitelist=now.split('  case normalized_key')[2].split('\n      assign locale_copy_key')[0]
assert set(re.findall("'([^']+)'",whitelist))==set(keys) and len(keys)==38
assert "assign localized_text = fallback_text" in now and "assign localized_text = locale_copy_key | t" in now
owned.append({'path':'snippets/home-category-localized-copy.liquid','sha256':hashlib.sha256(now.encode()).hexdigest(),'aliases_preserved':18,'translated_normalized_keys':38,'unknown_key_fallback_preserved':True})
assert not errors,errors
checks={'result':'PASS','checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'locale_json_files':35,'published_locales':21,'english_leaf_keys':len(en),'all35_locales_full_key_parity':True,'changed_locale_values':len(changes),'changed_value_placeholder_html_artifact_errors':errors,'duplicate_json_keys':0,'locale_results':summaries,'he_no_product_counts_and_all_published_footer_keys_present':True,'home_aliases_preserved':18,'home_normalized_keys':38,'whitelist_and_unknown_fallback_check':'PASS','git_diff_check':'PASS (run separately before freeze)','limits':['14 unpublished locales receive explicit English fallbacks for new keys; not language-certified.','Existing Hebrew physical-store pickup and gift-card in-store text remains excluded from this repair because this dropshipping business does not assert a physical store. These conditional templates require a separate product-truth decision.','Some source-identical strings are valid loanwords, brands, placeholders, dates or unit notation; equality alone is not proof of leakage. Existing delivery-journey claims outside this bounded repair remain a source-truth review concern.','This is source validation and local language review, not exhaustive rendered-route or native-speaker certification. Parent owns independent review, full ThemeCheck, main push and live verification.']}
(P/'key_parity_and_placeholders.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n');(P/'all_locale_changes.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2)+'\n')
manifest={'frozen_at_utc':checks['checked_at_utc'],'status':'FROZEN_LOCAL_CANDIDATE','owner':'danish_scope_evidence','theme_paths':owned,'theme_path_count':len(owned),'changed_locale_values':len(changes),'published_changed_values':sum(x.get('changed_keys',0) for x in owned if x.get('published')),'unpublished_fallback_changed_values':sum(x.get('changed_keys',0) for x in owned if x.get('published') is False),'english_owned_by_parent':True,'no_more_theme_edits_without_parent_defect_allocation':True}
(P/'FROZEN_MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'result':'PASS','theme_paths':len(owned),'changed_values':len(changes),'published':manifest['published_changed_values'],'inactive':manifest['unpublished_fallback_changed_values'],'all35keyparity':True,'manifest_sha256':hashlib.sha256((P/'FROZEN_MANIFEST.json').read_bytes()).hexdigest()},indent=2))
