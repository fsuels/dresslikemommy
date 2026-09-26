"""Build proposed shopper-copy fixes (NO Shopify writes). Reuses the 2026-09-26 dry-run 'Chart-backed sizing' rewrite verbatim."""
import json, re, html, csv, hashlib
from patterns import COMPILED
P = {p['id'].split('/')[-1]: p for p in json.load(open('products_en.json'))}
F = json.load(open('flags.json'))

# (rule_id, category, regex, replacement or fn, review_flag)
BUL = re.compile(r'<strong>Chart-backed sizing:</strong>\s*(.*?)\s+rows are transcribed from the (?:supplied|published)[^<.]*charts?\.', re.S)
def chart_backed(m):  # identical to dry-run fix_desc.py rewrite()
    counts = m.group(1).replace(' rows', ' sizes').replace('rows,', 'sizes,')
    return f'<strong>Family size range:</strong> {counts} sizes; see the size chart for measurements.'
AP = r"(?:'|’|&#39;|&rsquo;)"
RULES = [
 ("R01_chart_backed_bullet", BUL, chart_backed, None),
 ("R02_care_not_supplied", re.compile(r"Follow the sewn-in garment label; an exact care method is not supplied\."), "Follow the care instructions on the sewn-in garment label.", None),
 ("R03_fiber_not_supplied", re.compile(r"Soft flannel one-piece; exact fiber content is not supplied\."), "Soft flannel one-piece.", None),
 ("R04_fiber_not_specified", re.compile(r"(Soft(?:-finished| knit)? fabric) with 95% polyester; the remaining fiber is not specified\."), r"\1, 95% polyester.", None),
 ("R05_makers_age_labels", re.compile(r"\b([Cc])hild sizes follow the maker" + AP + r"s age labels"), r"\1hild sizes are labeled by age", None),
 ("R06_not_part_of_listing", re.compile(r"\b(is|are) not part of this listing\."), r"\1 not included with your order.", None),
 ("R07_asian_factory_fit", re.compile(r"follows Asian factory fit"), "follows Asian sizing", None),
 ("R08_factory_publishes", re.compile(r"the factory publishes measurements through"), "the size chart lists measurements through", None),
 ("R09_largest_published_row", re.compile(r"from the largest published row"), "from the largest size in the chart", None),
 ("R10_source_residue", re.compile(r"with matching shorts measurements on the source"), "with matching shorts", "REVIEW: original sentence is truncated operator residue; confirm shorts are pictured, not sold"),
 ("R11_vendor_label_header", re.compile(r"<th>Vendor Label</th>"), "<th>Tag Size</th>", "REVIEW: size-table header change; re-run localized size-chart repair/audit for this handle"),
 ("R12_no_weight_guidance", re.compile(r"no (weight(?: or height)?) guidance is published"), r"the chart gives no \1 guidance", None),
 ("R13_no_hip_published", re.compile(r"No hip measurement is published\."), "The chart has no hip measurement.", None),
 ("R14_published_in_inches", re.compile(r"Body measurements are published in inches"), "Body measurements are shown in inches", None),
 ("R15_no_child_hip", re.compile(r"and no child hip is published"), "and the chart has no child hip measurement", None),
 ("R16_size_variant_jargon", re.compile(r"\(choose each size variant\)"), "(choose a size for each person)", None),
 ("R17_size_slash_variant", re.compile(r"\(select each size/variant separately for a matching set\)"), "(select each person" + "’" + "s size separately for a matching set)", None),
 ("R18_sku_jargon", re.compile(r"\(list each SKU by its age group\)"), "(choose each size by age group)", None),
 # DRAFT-only drafting residue
 ("D01_chart_backed_variants", re.compile(r"<strong>Chart-backed variants:</strong> Every listed garment and size comes from the attached source chart\."), "<strong>Size chart:</strong> Every garment and size offered has its own row in the size chart.", None),
 ("D02_fiber_not_confirmed", re.compile(r"A lightweight woven-look dress and matching shorts are shown; exact fiber composition is not confirmed\."), "A lightweight woven-look dress and matching shorts.", None),
 ("D03_supplied_family_image", re.compile(r", as shown in the supplied family image\."), ", as shown in the photos.", None),
 ("D04_attached_chart_publishes", re.compile(r"The attached chart publishes dedicated dress rows plus short length and hip measurements for boys and men; shirt measurements from the combined source table are intentionally not listed\."), "The size chart shows dress measurements plus shorts length and hip measurements for boys and men; shirt measurements are not listed.", None),
 ("D05_source_sweatshirt_chart", re.compile(r"Seven child rows and seven adult rows come directly from the source sweatshirt chart\."), "Seven child sizes and seven adult sizes; see the size chart for measurements.", None),
 ("D06_single_garment_scope", re.compile(r"<strong>Single-garment scope:</strong> Each selected variant includes one sweatshirt;"), "<strong>One sweatshirt per selection:</strong> Each selection includes one sweatshirt;", None),
 ("D07_chart_backed_size", re.compile(r"choose each person" + AP + r"s chart-backed size"), "choose each person’s size", None),
 ("D08_backed_by_source_chart", re.compile(r", all backed by the attached source chart\."), ".", None),
 ("D09_source_chart_publishes", re.compile(r"The source chart publishes garment length"), "The size chart shows garment length", None),
 ("D10_variant_maps_to_row", re.compile(r"Every available variant maps to one row in the attached size chart\."), "Every available size has its own row in the size chart.", None),
 ("D11_supplied_image_fiber", re.compile(r"Lightweight-looking pleated fabric shown in the supplied image; exact fiber content is not supplied\."), "Lightweight-looking pleated fabric.", None),
]
def text_hits(h):
    t=' '.join(html.unescape(re.sub(r'<[^>]+>',' ',h or '')).split())
    return sorted({k for k,rx in COMPILED if rx.search(t)})
def snippet(h, s, e, pad=0):
    return ' '.join(html.unescape(re.sub(r'<[^>]+>',' ',h[s:e])).split())
dry = {r['id']: r['new'] for r in json.load(open('/private/tmp/claude-501/-Users-fsuels-Projects-dresslikemommy/3686ed1c-4587-446d-9c90-3c1276c7c210/scratchpad/desc_fix_dry.json'))}
out=[]; rows=[]; dry_mismatch=[]
for r in F:
    if r['status']=='ARCHIVED': continue
    p=P[r['id']]; before=p['descriptionHtml']; after=before; changes=[]; reviews=[]
    for rid, rx, rep, rev in RULES:
        for m in list(rx.finditer(after))[::-1]:
            new = rep(m) if callable(rep) else m.expand(rep)
            changes.append({'rule':rid,'before_html':m.group(0),'after_html':new,
                            'before_text':snippet(after,m.start(),m.end()),'after_text':' '.join(html.unescape(re.sub(r'<[^>]+>',' ',new)).split())})
            if rid=='R01_chart_backed_bullet' and r['id'] in dry and dry[r['id']]!=new: dry_mismatch.append(r['id'])
            after = after[:m.start()] + new + after[m.end():]
            if rev: reviews.append(rev)
    residual = text_hits(after)
    rec={'product_id':r['id'],'gid':p['id'],'handle':p['handle'],'status':p['status'],'title':p['title'],
         'before_updatedAt':p['updatedAt'],'before_sha256':hashlib.sha256(before.encode()).hexdigest(),
         'after_sha256':hashlib.sha256(after.encode()).hexdigest(),'categories_before':text_hits(before),
         'residual_categories_after':residual,'review_notes':reviews,
         'in_2026_09_26_dry_run':r['id'] in dry,'changes':changes,'before_html':before,'after_html':after,
         'fix_status':'READY' if not residual and not reviews else ('NEEDS_REVIEW' if not residual else 'RESIDUAL')}
    out.append(rec)
    for c in changes:
        rows.append([r['id'],p['handle'],p['status'],c['rule'],c['before_text'],c['after_text'],rec['fix_status'],'; '.join(reviews)])
print('products',len(out),'changes',sum(len(o['changes']) for o in out))
from collections import Counter
print(Counter(o['fix_status'] for o in out), Counter(o['status'] for o in out))
print('residual',[(o['handle'],o['residual_categories_after']) for o in out if o['residual_categories_after']])
print('dry-run ids covered',sum(o['in_2026_09_26_dry_run'] for o in out),'/',len(dry),'mismatch',dry_mismatch)
print(Counter(c['rule'] for o in out for c in o['changes']))
json.dump(out,open('copy_fixes_full.json','w'),indent=1,ensure_ascii=False)
with open('copy_fixes.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['product_id','handle','status','rule','before_snippet','after_snippet','fix_status','review_note']); w.writerows(rows)
