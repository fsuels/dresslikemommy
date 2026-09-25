import collections
import hashlib
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
load = lambda path: json.loads(path.read_text())
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
plain = lambda value: re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', value))).strip()
dump = lambda name, value: (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
work_file = ROOT / 'review/product-remainder-review/source_disposition_worklist.json'
rows = load(work_file)['rows']
baseline_file = ROOT / 'products/remaining/baseline.json'
baseline = load(baseline_file)['rows']
source_by_field = {}
for row in baseline + rows:
    key = (row['resourceId'].rsplit('/', 1)[-1], row['key'])
    entry = {'resourceId': row['resourceId'], 'key': row['key'], 'sourceValue': row.get('sourceValue', row['source']), 'sourceDigest': row['sourceDigest']}
    if key in source_by_field:
        assert source_by_field[key] == entry
    source_by_field[key] = entry

groups = [
    ('policy', 527, 'Shipping and returns qualification', 'POLICY_SCOPE_CONFLICT_OR_OMITTED_QUALIFICATION',
     'The same source suffix says “Free shipping + 30-day returns.” on 129 products. The saved shipping policy limits included shipping to standard methods where available. Of these fields, 124 explicitly describe swimwear, which the saved refund policy excludes; 403 other fields do not establish a return-policy contradiction from category alone.',
     'Which shipping qualification and product-specific return eligibility should the public metadata state? General 30-day returns are supported for eligible items; do not replace that fact with a blanket prohibition.'),
    ('shirt_type', 115, 'T-shirt versus collared button-up', 'CONTRADICTORY_SAME_PRODUCT_FIELDS',
     'Product 7502178222177 SEO says “Family Matching T-Shirts - Blue Tropical Print | Dress Like Mommy”; its body says “Short-sleeve, button-front style” and “classic collar”. The same category conflict affects 20 products.',
     'Confirm the intended product category from the same-product seller evidence; update the erroneous SEO category consistently, including affected descriptions.'),
    ('seasonal_design', 8, 'Wrong seasonal design in SEO', 'CONTRADICTORY_SAME_PRODUCT_FIELDS',
     'Product 7230194942049 SEO says “Halloween Print” while its title identifies a battery-themed design. Product 7230424645729 says “Christmas Print” but identifies a rainbow/sunshine design. Two swim-short products 7510790733921 and 7510791159905 say Christmas but identify tropical-leaf and color-block designs.',
     'Confirm the actual design, then align English SEO titles and descriptions with the product evidence.'),
    ('heart_design', 2, 'Heart print versus heart buttons', 'CONTRADICTORY_SAME_PRODUCT_FIELDS',
     'Product 7241105670241 SEO says “Red Heart Print”; the body says “Gold heart-shaped buttons add a delightful, decorative touch.”',
     'Confirm red garment color and gold heart-button design; do not translate a printed-heart design unless the source evidence supports it.'),
    ('piece_count', 9, 'One-piece versus bikini/two-piece', 'CONTRADICTORY_SAME_PRODUCT_FIELDS',
     'Product 6719764463713 is called “Bikini” in its title and “one-piece” in its body. Product 7109292130401 says “Two-Piece Swimsuit” but also “Stylish one-piece design with elegant cut-out details”. The first product also has unsupported Halloween SEO and natural/organic-versus-synthetic copy.',
     'Confirm the construction and sold pieces for each product; neither translation nor a guessed category resolves the English contradiction.'),
    ('fiber_contradiction', 4, 'Cotton-silk versus viscose/polyester', 'CONTRADICTORY_MATERIAL_FACTS',
     'Product 7516369715297 says “White Cotton-Silk” and “Soft cotton-silk blend (viscose shell / polyester lining)”. Cotton, silk, viscose and polyester cannot be treated as synonyms.',
     'Confirm the actual shell and lining fiber content from a label or seller specification; do not invent percentages or choose one unsupported claim.'),
    ('organic_synthetic', 5, 'Natural/organic versus synthetic composition', 'CONTRADICTORY_MATERIAL_FACTS',
     'Product 6718945034337 calls the manufacturing materials “natural and organic materials” but specifies “82% Nylon, 18% Spandex”. Four products have this primary conflict; another is counted under piece count.',
     'Determine whether the synthetic composition is authoritative and whether any narrower organic claim has evidence. Generic positive style copy is not itself a hold.'),
    ('weight_units', 2, 'Inconsistent kilogram/pound chart', 'CONTRADICTORY_NUMERIC_FACTS',
     'Product 7227630649441 pairs “50 kg / 100 lbs and below” and “57.5 kg / 115 lbs and below”; the child rows use the same incorrect 2:1 ratio.',
     'Identify the authoritative weight column before recalculating its counterpart. Preserve neither pair as if it were a correct conversion.'),
    ('extrapolated_sizes', 2, 'Unpublished larger sizes and fit promise', 'UNVERIFIED_SIZE_GUIDANCE_AND_POLICY_PROMISE',
     'Product 7229128441953 says the factory publishes measurements through Child 9–10 Years, recommends the next size up for larger ranges, and says “we’re happy to swap or refund if the fit isn’t right” (source uses straight apostrophes).',
     'Confirm the larger-size measurements and available variants, plus the actual exchange/return terms for this product. No measurements should be fabricated.'),
    ('bundle_inclusion', 2, 'Unclear contents of one purchased set', 'CONTRADICTORY_SOLD_UNIT_FACTS',
     'Product 7497751986273 says “Each set includes a matching top and bottom for both mom and daughter.” It then says “Order one set for mom and one for your daughter”.',
     'Does one selection contain one wearer’s top and bottom, or both wearers’ pieces? Establish that before changing the English inclusion statement.'),
    ('operator_instruction', 2, 'SKU instruction exposed to customers', 'EXPOSED_INTERNAL_COPY',
     'Product 7502791671905 says “Sizing: Men + Boys (list each SKU by its age group)”.',
     'Remove the internal editing instruction after confirming customer-facing size labels. No garment fact needs to be invented.'),
    ('selector_draft', 16, 'Draft top/bottom/set selection explanation', 'EXPOSED_INTERNAL_COPY_AND_SOLD_UNIT_AMBIGUITY',
     'Product 7545279840353 says “this draft intentionally lists only the chart-backed top variants” although the source selector includes tops, bottoms and complete suits.',
     'Confirm the actual current sellable unit and variants. Remove workflow commentary while stating the verified inclusion clearly.'),
    ('derived_chart_draft', 20, 'Draft listing and derived measurements', 'EXPOSED_INTERNAL_COPY_AND_UNVERIFIED_MEASUREMENTS',
     'Product 7585867432033 says “This draft keeps the request precise” and “derived waist and hip values” where the source did not publish them.',
     'Confirm which measurements are seller-backed and which garments are sold. Remove draft instructions; do not silently present inferred chart values as measured facts.'),
    ('source_access_copy', 132, 'Vendor-access commentary and unknown composition', 'EXPOSED_INTERNAL_COPY_WITH_EXPLICIT_UNKNOWNS',
     'Eleven products expose source-gathering notes, for example product 7585867628641: “exact fiber content was not visible from the blocked vendor page.” Product 7536982163553 also calls its care line a “conservative inference”. These statements identify uncertainty, not proof that the visible garment description is false.',
     'Clean customer copy without inventing fiber or care facts. Confirm any precise material/care claim from seller evidence; preserve uncertainty where a fact remains unknown.'),
]
group_map = {row[0]: {'groupId': row[0], 'expectedFields': row[1], 'label': row[2], 'classification': row[3], 'exactExamplesAndAssessment': row[4], 'decisionOrUnknownFact': row[5]} for row in groups}
special = {
    '6719764463713': 'piece_count', '7109292130401': 'piece_count', '7516369715297': 'fiber_contradiction',
    '7227630649441': 'weight_units', '7229128441953': 'extrapolated_sizes', '7497751986273': 'bundle_inclusion',
    '7502791671905': 'operator_instruction', '7545279840353': 'selector_draft', '7585867432033': 'derived_chart_draft',
}
organic_ids = {'6718945034337', '6718948147297', '6719774720097', '6719792873569'}
season_ids = {'7230194942049', '7230424645729', '7510790733921', '7510791159905'}
access_ids = {'7536982163553', '7537007198305', '7537367384161', '7537978572897', '7545279217761', '7545373130849', '7546613530721', '7562834215009', '7585867628641', '7585980055649', '7585992048737'}

for row in rows:
    pid = row['resourceId'].rsplit('/', 1)[-1]
    key = row['key']
    if key == 'meta_description':
        group = 'policy'
        assert 'Free shipping + 30-day returns.' in row['sourceValue']
        row['policySubclassification'] = 'SWIMWEAR_EXPLICIT_REFUND_POLICY_CONFLICT' if re.search(r'bikini|swimsuit|swim trunks|tankini', row['sourceValue'], re.I) else 'STANDARD_SHIPPING_QUALIFICATION_AND_RETURN_ELIGIBILITY_CHECK'
    elif key == 'meta_title' and pid in season_ids:
        group = 'seasonal_design'
    elif key == 'meta_title' and pid == '7241105670241':
        group = 'heart_design'
    elif pid in special and (key != 'meta_title' or pid in {'6719764463713', '7109292130401'}):
        group = special[pid]
    elif key == 'meta_title':
        assert 'T-Shirts' in row['sourceValue']
        group = 'shirt_type'
    elif key == 'body_html' and pid in organic_ids:
        group = 'organic_synthetic'
    elif key == 'body_html' and pid in access_ids:
        group = 'source_access_copy'
    else:
        raise AssertionError((pid, key))
    row['independentSourceGroup'] = group
    row['sourceSHA256'] = hashlib.sha256(row['sourceValue'].encode()).hexdigest()
    row['beforeValueSHA256'] = hashlib.sha256(row['before']['value'].encode()).hexdigest() if row.get('before') else None

counts = collections.Counter(row['independentSourceGroup'] for row in rows)
assert len(rows) == len({(r['resourceId'], r['locale'], r['key']) for r in rows}) == 846
assert counts == {group[0]: group[1] for group in groups}, counts
for group in group_map.values():
    subset = [row for row in rows if row['independentSourceGroup'] == group['groupId']]
    group['fields'] = len(subset)
    group['products'] = len({row['resourceId'] for row in subset})
    group['locales'] = sorted({row['locale'] for row in subset})
    group['keys'] = dict(collections.Counter(row['key'] for row in subset))
    group['resourceIds'] = sorted({row['resourceId'] for row in subset})

# Evidence is exact English snapshot text, with HTML removed and whitespace normalized only.
examples = [
    ('shirt_type', '7502178222177', 'meta_title', 'Family Matching T-Shirts - Blue Tropical Print | Dress Like Mommy'),
    ('shirt_type', '7502178222177', 'body_html', 'Short-sleeve, button-front style'),
    ('shirt_type', '7502178222177', 'body_html', 'classic collar'),
    ('heart_design', '7241105670241', 'body_html', 'Gold heart-shaped buttons add a delightful, decorative touch.'),
    ('piece_count', '6719764463713', 'body_html', 'one-piece Matching Mommy And Me Hollow Out Bikini'),
    ('piece_count', '7109292130401', 'body_html', 'Stylish one-piece design with elegant cut-out details'),
    ('piece_count', '7109292130401', 'body_html', 'Chic Mother-Daughter Two-Piece Swimsuit'),
    ('fiber_contradiction', '7516369715297', 'body_html', 'Soft cotton-silk blend (viscose shell / polyester lining)'),
    ('organic_synthetic', '6718945034337', 'body_html', 'natural and organic materials'),
    ('organic_synthetic', '6718945034337', 'body_html', '82% Nylon, 18% Spandex'),
    ('weight_units', '7227630649441', 'body_html', '50 kg / 100 lbs and below'),
    ('weight_units', '7227630649441', 'body_html', '57.5 kg / 115 lbs and below'),
    ('extrapolated_sizes', '7229128441953', 'body_html', "we're happy to swap or refund if the fit isn't right"),
    ('bundle_inclusion', '7497751986273', 'body_html', 'Each set includes a matching top and bottom for both mom and daughter.'),
    ('bundle_inclusion', '7497751986273', 'body_html', 'Order one set for mom and one for your daughter'),
    ('operator_instruction', '7502791671905', 'body_html', 'Sizing: Men + Boys (list each SKU by its age group)'),
    ('selector_draft', '7545279840353', 'body_html', 'this draft intentionally lists only the chart-backed top variants'),
    ('derived_chart_draft', '7585867432033', 'body_html', 'This draft keeps the request precise'),
    ('derived_chart_draft', '7585867432033', 'body_html', 'derived waist and hip values'),
    ('source_access_copy', '7585867628641', 'body_html', 'exact fiber content was not visible from the blocked vendor page.'),
    ('source_access_copy', '7536982163553', 'body_html', 'conservative inference'),
]
evidence = []
for group, pid, key, exact in examples:
    source = source_by_field[(pid, key)]
    assert exact in plain(source['sourceValue']), (pid, key, exact)
    evidence.append({'groupId': group, **source, 'exactNormalizedPlainTextExcerpt': exact})
for pid in sorted(season_ids):
    for key in ['title', 'meta_title']:
        source = source_by_field[(pid, key)]
        evidence.append({'groupId': 'seasonal_design', **source, 'exactNormalizedPlainTextExcerpt': plain(source['sourceValue'])})
for pid in sorted(access_ids):
    source = source_by_field[(pid, 'body_html')]
    text = plain(source['sourceValue'])
    excerpt = next((m.group(0) for m in re.finditer(r'[^.!?]*(?:exact fiber|no exact fiber|fiber content|conservative inference)[^.!?]*[.!?]', text, re.I)), None)
    assert excerpt
    evidence.append({'groupId': 'source_access_copy', **source, 'exactNormalizedPlainTextExcerpt': excerpt.strip()})

policy_file = ROOT.parent / '2026-09-22-multilingual-storefront/content_before_apply.json'
policy_rows = load(policy_file)
policy_nodes = {r['resourceId']: r for lang in policy_rows for r in lang['nodes'] if 'ShopPolicy' in r['resourceId']}
policy_evidence = []
for pid, quotes in [
    ('29845782625', ['Standard shipping is included in product prices for countries and regions where a standard method is available. Checkout shows the exact method, delivery estimate, and any express upgrade before payment.']),
    ('14695685', ['You have 30 days from the date of delivery to request a return or exchange.', 'Swimwear and intimates (for hygiene reasons)', 'Items marked as "Final Sale"']),
]:
    rid = 'gid://shopify/ShopPolicy/' + pid
    content = next(row for row in policy_nodes[rid]['translatableContent'] if row['key'] == 'body')
    for quote in quotes:
        assert quote in plain(content['value'])
    policy_evidence.append({'resourceId': rid, 'sourceDigest': content['digest'], 'exactNormalizedPlainTextExcerpts': quotes})

policy_counts = dict(collections.Counter(row.get('policySubclassification') for row in rows if row['key'] == 'meta_description'))
shirt_ids = {r['resourceId'] for r in rows if r['independentSourceGroup'] == 'shirt_type'}
secondary = []
for row in rows:
    if row['key'] != 'meta_description':
        continue
    pid = row['resourceId'].rsplit('/', 1)[-1]
    reasons = []
    if row['resourceId'] in shirt_ids and 't-shirts' in row['sourceValue']:
        reasons.append('shirt_type')
    if pid in season_ids:
        reasons.append('seasonal_design')
    if pid == '7241105670241':
        reasons.append('heart_design')
    if pid in {'6719764463713', '7109292130401'}:
        reasons.append('piece_count_or_design')
    if reasons:
        row['secondarySourceIssues'] = reasons
        secondary.append({'resourceId': row['resourceId'], 'locale': row['locale'], 'key': row['key'], 'groups': reasons})

packet = {
    'status': 'SOURCE_DISPOSITION_REVIEW_PACKET_NO_SOURCE_EDITS_OR_NEW_APPROVAL_GATES',
    'scope': '846 exact unreleased product translation fields grouped by demonstrated source issue. These are fields, not 846 separate products.',
    'fields': 846, 'uniqueProducts': len({r['resourceId'] for r in rows}),
    'fieldCounts': dict(collections.Counter(r['key'] for r in rows)),
    'limitations': 'Offline September 22 snapshots, not fresh live evidence. Root must refresh the specific English source and policies before any source repair. No replacement English, fiber composition, measurements, sold-unit facts or return exceptions are invented here.',
    'notAGate': 'Existing flags alone are not an approval requirement. Ordinary style/marketing language is not held. Known English conflicts need factual disposition; exposed workflow text can be cleaned without fabricating unknown facts.',
    'inputFile': str(work_file.relative_to(ROOT)), 'inputSHA256': sha(work_file),
    'baselineFile': str(baseline_file.relative_to(ROOT)), 'baselineSHA256': sha(baseline_file),
    'policyEvidenceFile': str(policy_file), 'policyEvidenceFileSHA256': sha(policy_file),
    'policyEvidence': policy_evidence, 'policySubclassificationCounts': policy_counts,
    'secondaryMetadataIssueCounts': dict(collections.Counter(group for entry in secondary for group in entry['groups'])),
    'groups': list(group_map.values()), 'evidence': evidence, 'rows': rows,
}
dump('product_source_disposition846.json', packet)
lines = [
    '# Product source decisions: 846 remaining translation fields', '',
    f'The 846 fields concern {packet["uniqueProducts"]} products: 527 SEO descriptions, 129 SEO titles, 186 bodies and 4 titles. This is an evidence classification, not a blanket hold or a proposal to change unknown product facts.', '',
    'The saved policy supports a 30-day return window for eligible items, but explicitly excludes swimwear and intimates. Among the 527 SEO descriptions, 124 explicitly identify swimwear; the other 403 are not proven to violate returns policy merely by mentioning 30 days. All 527 omit the available-standard-method qualification on shipping. Source categories/design errors also occur in some of these descriptions and are recorded as secondary issues in the exact ledger.', '',
    '| Issue | Fields / products | Exact source example and fact to resolve |',
    '|---|---:|---|',
]
for group in group_map.values():
    prose = group['exactExamplesAndAssessment'] + ' **Decision:** ' + group['decisionOrUnknownFact']
    lines.append('| ' + group['label'] + ' | ' + str(group['fields']) + ' / ' + str(group['products']) + ' | ' + prose.replace('|', '\\|') + ' |')
lines.extend(['', 'Counts are mutually exclusive primary groups. Products can appear in more than one group, and the ledger retains secondary issues. A generic marketing flag is not a new permission gate. Where only internal sourcing commentary is exposed, cleanup can preserve the factual unknown instead of inventing fiber content, care instructions or measurements.', '',
              'Evidence: [exact 846-field ledger, source digests, before values, grouped examples and policy excerpts](product_source_disposition846.json). Product English and policy evidence are saved September 22 snapshots; root should refresh the relevant source before changing it. No external action, canonical-source edit or publication was performed by this review.', ''])
(HERE / 'PRODUCT_SOURCE_DECISIONS.md').write_text('\n'.join(lines))
print(json.dumps({'fields': len(rows), 'products': packet['uniqueProducts'], 'groups': counts, 'policy': policy_counts, 'secondary': packet['secondaryMetadataIssueCounts']}))
