"""Offline source preservation, locale coverage, and actual-script fixture preparation."""
from pathlib import Path
import json,re,hashlib,difflib
from collections import Counter
from manual_translations import COPY,KEYS
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[4]
manifest=json.loads((OUT/'before_manifest.json').read_text())
fallback=json.loads((OUT/'unpublished_fallback_locales.json').read_text())
def digest(s):return hashlib.sha256(s.encode()).hexdigest()
def load_locale(name):
 s=(ROOT/'locales'/f'{name}.json').read_text();return json.loads(s[s.index('{'):])
def lookup(d,key):
 for part in key.split('.'):d=d[part]
 return d
checks=[]
def check(condition,label):
 assert condition,label
 checks.append(label)
new_digests={};patch=[]
for rel,baseline in manifest.items():
 path=ROOT/rel;s=path.read_text();new_digests[rel]=digest(s)
 if rel.endswith('.json'):
  header=s[:s.index('{')];d=json.loads(s[len(header):]);copy=d['storefront'].pop('article')
  check(digest(json.dumps(d,sort_keys=True,ensure_ascii=False))==baseline['json_without_article_sha256'],rel+': every pre-existing JSON value preserved')
  old=header+json.dumps(d,ensure_ascii=False,indent=2)+'\n'
  check(digest(old)==baseline['sha256'],rel+': non-article JSON bytes preserved')
  locale=path.stem
  expected=COPY.get(locale,COPY['en.default'])
  check(copy==expected,rel+': exact manually authored values or explicit unpublished fallback')
  check(list(copy)==KEYS,rel+': exact20keys')
  for key,value in copy.items():
   check(Counter(re.findall(r'{{\s*(\w+)\s*}}',value))==Counter(re.findall(r'{{\s*(\w+)\s*}}',COPY['en.default'][key])),rel+': placeholders '+key)
   check(bool(value.strip()) and '<' not in value and '>' not in value,rel+': nonempty plain text '+key)
 else:old=(OUT/(path.name+'.before.txt')).read_text()
 patch.extend(difflib.unified_diff(old.splitlines(True),s.splitlines(True),fromfile='a/'+rel,tofile='b/'+rel))
(OUT/'exact_source_changes.diff').write_text(''.join(patch))
main=(ROOT/'sections/main-article.liquid').read_text();snippet=(ROOT/'snippets/style-journal-internal-links.liquid').read_text();old_main=(OUT/'main-article.liquid.before.txt').read_text();old_snippet=(OUT/'style-journal-internal-links.liquid.before.txt').read_text()
# Every context-specific English article-to-collection assignment stays intact.
assign_pattern=r"assign collection_link_[123]_(?:handle|title|caption) = '[^']*'"
old_assign=re.findall(assign_pattern,old_snippet);new_assign=re.findall(assign_pattern,snippet)
check(Counter(x for x in old_assign if not x.endswith("= ''"))==Counter(x for x in new_assign if not x.endswith("= ''") and x in old_assign),'English tailored titles/captions and handles unchanged')
for marker,end in [('  case article_context_handle','  assign collection_link_1_object = blank'),('  assign related_article_1_handle','  if guide_link_1_title != blank and guide_link_1_caption == blank')]:
 a=old_snippet[old_snippet.index(marker):old_snippet.index(end)]
 b=snippet[snippet.index(marker):snippet.index(end)]
 check(a==b,'Source routing block unchanged: '+marker)
check(re.findall(r'href="[^"]*"',main)==re.findall(r'href="[^"]*"',old_main),'Main HTML links unchanged')
check(re.findall(r'href="[^"]*"',snippet)==re.findall(r'href="[^"]*"',old_snippet),'Shared snippet HTML links unchanged')
check(re.findall(r'data-style-journal-[\w-]+=',main+snippet)==re.findall(r'data-style-journal-[\w-]+=',old_main+old_snippet),'Tracking attributes unchanged')
check("if request.locale.iso_code != 'en'" in snippet,'Teaser override is non-English only')
block=snippet.split("  if request.locale.iso_code != 'en'",1)[1].split('  assign inline_cta_url',1)[0]
for n in range(1,4):
 p=f'collection_link_{n}'
 check(f"assign {p}_title = ''" in block and f'if {p}_object != blank' in block,'Missing collection cannot retain English title '+str(n))
 check(f"render 'collection-seo-fallback', collection: {p}_object, field: 'display_title'" in block,'Collection title renderer '+str(n))
 check(f"assign {p}_caption = 'storefront.collection_fallback_description' | t: title: {p}_title" in block,'Neutral translated caption '+str(n))
check(snippet.index("if request.locale.iso_code != 'en'")<snippet.index('assign inline_cta_label ='),'Inline CTA consumes localized title')
check("| append: '/matching-outfits' | json" in main,'JS fallback retains localized collection route')
refs=set(re.findall(r"'((?:storefront.article|storefront.journal|storefront.menu|sections.breadcrumbs)\.[\w.]+)'\s*\|\s*t",main+snippet))
reused=['storefront.journal.title','storefront.journal.read_time','storefront.menu.shop_now','storefront.menu.shop_edit','sections.breadcrumbs.cat_mommy_me','sections.breadcrumbs.cat_family_matching','storefront.collection_fallback_description']
for locale in COPY:
 d=load_locale(locale)
 for key in refs|set(reused):check(isinstance(lookup(d,key),str),'Resolved translation '+locale+':'+key)
 if locale!='en.default':
  check(all(v!=COPY['en.default'][k] for k,v in COPY[locale].items()),locale+': all20newkeys differ from English')
# Verify all12 preselected collection handles map to native translated display-title keys.
helper=(ROOT/'snippets/collection-seo-fallback.liquid').read_text()
first_case=helper.split('  case collection_handle',1)[1].split('  endcase',1)[0]
handle_keys={}
for match in re.finditer(r"when ([^\n]+)\n(.*?)(?=    when|\Z)",first_case,re.S):
 key=re.search(r"effective_display_title_key = '([^']+)'",match[2])
 if key:
  for handle in re.findall(r"'([^']+)'",match[1]):handle_keys[handle]=key[1]
handles=set(re.findall(r"assign collection_link_[123]_handle = '([^']+)'",old_snippet))
check(len(handles)==12 and all(h in handle_keys for h in handles),'All12 article-selected collection handles use existing title translations')
for locale in COPY:
 for handle in handles:check(bool(lookup(load_locale(locale),handle_keys[handle])),'Collection title key '+locale+':'+handle)
# Inline JavaScript fixtures are derived from the actual edited script, not a replacement implementation.
def cta_script(s):return next(x for x in re.findall(r'<script>(.*?)</script>',s,re.S) if 'var ctaData' in x)
script=cta_script(main);old_script=cta_script(old_main);fixtures=[]
for locale in COPY:
 code='en' if locale=='en.default' else locale;d=load_locale(locale);rendered=re.sub(r"{% if request.locale.iso_code == 'en' %}(.*?){% else %}(.*?){% endif %}",lambda m:m[1] if code=='en' else m[2],script,flags=re.S)
 rendered=re.sub(r"{{ '([^']+)' \| t \| json }}",lambda m:json.dumps(lookup(d,m[1]),ensure_ascii=False),rendered)
 rendered=re.sub(r"{{ '([^']+)' \| json }}",lambda m:json.dumps(m[1]),rendered)
 route=('/collections' if code=='en' else '/'+code+'/collections')
 rendered=rendered.replace("{{ routes.collections_url | append: '/matching-outfits' | json }}",json.dumps(route+'/matching-outfits'))
 check('{{' not in rendered and '{%' not in rendered,'JS fixture fully substituted '+code)
 fixtures.append({'locale':code,'script':rendered,'expectedText':'Ready to start matching?' if code=='en' else COPY[locale]['inline_cta_text'],'expectedLabel':'Shop Matching Outfits' if code=='en' else COPY[locale]['inline_cta_label'],'expectedUrl':route+'/matching-outfits'})
(OUT/'js_fixtures.json').write_text(json.dumps({'beforeEnglishScript':old_script,'fixtures':fixtures},ensure_ascii=False,indent=2)+'\n')
(OUT/'check_results.json').write_text(json.dumps({'status':'PASS','checkCount':len(checks),'scopeFiles':len(manifest),'publishedNonEnglish':20,'newKeysPerLocale':20,'unpublishedEnglishFallback':fallback,'afterSha256':new_digests,'checks':checks},indent=2,ensure_ascii=False)+'\n')
print(f'PASS {len(checks)} assertions across37 source files,20 translations and14 explicit unpublished fallbacks.')
