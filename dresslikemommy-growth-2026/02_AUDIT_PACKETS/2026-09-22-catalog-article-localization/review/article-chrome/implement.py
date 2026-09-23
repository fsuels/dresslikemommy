from pathlib import Path
import json,hashlib
from manual_translations import COPY
ROOT=Path(__file__).resolve().parents[5]
OUT=Path(__file__).resolve().parent
before=json.loads((OUT/'before_manifest.json').read_text())
for rel,record in before.items():
 assert hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==record['sha256'],f'Changed since scoped baseline: {rel}'
def exact(s,old,new,n=1):
 assert s.count(old)==n,(old,s.count(old),n)
 return s.replace(old,new)
def t(key):return "{{ 'storefront.article."+key+"' | t }}"
p=ROOT/'sections/main-article.liquid';s=p.read_text()
s=exact(s,"assign journal_label = 'Style Journal'","assign journal_label = 'storefront.journal.title' | t")
s=exact(s,'aria-label="breadcrumbs"','aria-label="'+t('breadcrumbs_label')+'"')
s=exact(s,'>Family Fashion Editor<','>'+t('author_credential')+'<')
s=exact(s,' }} min read</span>'," }} {{ 'storefront.journal.read_time' | t }}</span>")
s=exact(s,'aria-label="Table of contents"','aria-label="'+t('contents_aria_label')+'"')
s=exact(s,'>In this article<','>'+t('contents_label')+'<')
s=exact(s,"|| 'Ready to start matching?';","|| {% if request.locale.iso_code == 'en' %}{{ 'Ready to start matching?' | json }}{% else %}{{ 'storefront.article.inline_cta_text' | t | json }}{% endif %};")
s=exact(s,"|| 'Shop Matching Outfits';","|| {% if request.locale.iso_code == 'en' %}{{ 'Shop Matching Outfits' | json }}{% else %}{{ 'storefront.article.inline_cta_label' | t | json }}{% endif %};")
s=exact(s,"|| '/collections/matching-outfits';","|| {{ routes.collections_url | append: '/matching-outfits' | json }};")
s=exact(s,'Shop now <span',"{{ 'storefront.menu.shop_now' | t }} <span")
s=exact(s,'>Shop the edit<',">{{ 'storefront.menu.shop_edit' | t }}<")
for key in ['recommended_products','written_by','author_bio','shop_look','compare_title','compare_body','continue_reading']:
 s=exact(s,'>'+COPY['en.default'][key]+'<','>'+t(key)+'<')
s=exact(s,'>Mommy &amp; Me<',">{% if request.locale.iso_code == 'en' %}Mommy &amp; Me{% else %}{{ 'sections.breadcrumbs.cat_mommy_me' | t }}{% endif %}<")
s=exact(s,'>Family Matching<',">{{ 'sections.breadcrumbs.cat_family_matching' | t }}<")
s=exact(s,'>More from {{ journal_label }}<',">{{ 'storefront.article.more_from' | t: journal: journal_label }}<")
p.write_text(s)
p=ROOT/'snippets/style-journal-internal-links.liquid';s=p.read_text()
s=exact(s,"  assign journal_blog = blogs['news']","  assign journal_blog = blogs['news']\n  assign journal_label = 'storefront.journal.title' | t")
# Keep English branch-specific title/caption assignments byte-for-byte. Override only non-English output.
block="  if request.locale.iso_code != 'en'\n"
for n in range(1,4):
 prefix=f'collection_link_{n}'
 block+=f"    assign {prefix}_title = ''\n    assign {prefix}_caption = ''\n    if {prefix}_object != blank\n      capture {prefix}_title\n        render 'collection-seo-fallback', collection: {prefix}_object, field: 'display_title'\n      endcapture\n      assign {prefix}_title = {prefix}_title | strip\n      assign {prefix}_caption = 'storefront.collection_fallback_description' | t: title: {prefix}_title\n    endif\n"
block+="  endif\n\n"
s=exact(s,"  assign inline_cta_url = collection_link_1_url | default: collections_root",block+"  assign inline_cta_url = collection_link_1_url | default: collections_root")
s=exact(s,"  assign inline_cta_label = collection_link_1_title | default: 'Shop matching collections'","  assign inline_cta_fallback_label = 'storefront.article.inline_cta_label' | t\n  assign inline_cta_label = collection_link_1_title | default: inline_cta_fallback_label")
s=exact(s,"  assign inline_cta_text = 'Ready to shop the looks from this guide?'","  assign inline_cta_text = 'storefront.article.inline_cta_text' | t")
for n in range(1,4):
 old=f"    capture guide_link_{n}_caption\n      echo 'Read '\n      echo guide_link_{n}_title\n      echo ' before you shop.'\n    endcapture\n    assign guide_link_{n}_caption = guide_link_{n}_caption | strip"
 new=f"    assign guide_link_{n}_caption = 'storefront.article.guide_caption' | t: title: guide_link_{n}_title"
 s=exact(s,old,new)
for key in ['shop_collection','shop_collections','build_look','continue_reading','read_before_shop','view_all_guides']:
 s=exact(s,'>'+COPY['en.default'][key]+'<','>'+t(key)+'<')
s=exact(s,'>More from Style Journal<',">{{ 'storefront.article.more_from' | t: journal: journal_label }}<")
s=exact(s,'>Style Journal<','>{{ journal_label }}<')
p.write_text(s)
for code,copy in COPY.items():
 p=ROOT/'locales'/f'{code}.json';s=p.read_text();header=s[:s.index('{')];data=json.loads(s[len(header):]);data['storefront']['article']=copy
 p.write_text(header+json.dumps(data,ensure_ascii=False,indent=2)+'\n')
(OUT/'manual_translations.json').write_text(json.dumps(COPY,ensure_ascii=False,indent=2)+'\n')
print('Changed exactly23 source files;20 article keys x21 language dictionaries.')
