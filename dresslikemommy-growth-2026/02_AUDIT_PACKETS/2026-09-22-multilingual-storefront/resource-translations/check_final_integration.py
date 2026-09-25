"""Read-only integration checks. Writes only this lane's final review artifact."""
import collections
import hashlib
import html
import json
import re
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

R = Path(__file__).resolve().parent
B = R.parent
snapshots = {}

def read(path):
    path = Path(path)
    if not path.is_absolute():
        path = B / path
    raw = path.read_bytes()
    snapshots[str(path)] = hashlib.sha256(raw).hexdigest()
    return json.loads(raw)

def key(row):
    return (row['resourceId'], row['locale'], row['key'])

def h(value):
    return hashlib.sha256(value.encode()).hexdigest()

failures = []
checks = []

def check(name, condition, details=None):
    result = {'check': name, 'status': 'PASS' if condition else 'FAIL'}
    if details is not None:
        result['details'] = details
    checks.append(result)
    if not condition:
        failures.append(result)

candidate = read('content_release_candidate.json')
bound = read('content_release_bound.json')
fresh = read('content_before_apply.json')
rows = candidate['rows']
keys = [key(r) for r in rows]
cmap = {key(r): r for r in rows}
bkeys = [key(r) for r in bound['translations']]
bmap = {key(r): r for r in bound['translations']}
check('candidate_and_bound_counts813', len(rows) == len(bound['translations']) == bound['fields'] == 813)
check('candidate_bound_hash_binding', bound['candidateSHA256'] == snapshots[str(B/'content_release_candidate.json')])
check('no_duplicate_resource_locale_keys', len(keys) == len(set(keys)) and len(bkeys) == len(set(bkeys)))
check('candidate_bound_same_keyset', set(keys) == set(bkeys))
check('bound_values_equal_reviewed_candidate', all(bmap[k]['value'] == cmap[k]['value'] for k in set(keys) & set(bkeys)))

fresh_nodes = {}
node_conflicts = []
for page in fresh:
    for node in page['nodes']:
        k = (page['locale'], node['resourceId'])
        if k in fresh_nodes and fresh_nodes[k] != node:
            node_conflicts.append(k)
        fresh_nodes[k] = node
check('fresh_snapshot_no_conflicting_resource_nodes', not node_conflicts, node_conflicts)

guard_errors = []
refreshed = []
for r in rows:
    k = key(r)
    n = fresh_nodes.get((r['locale'], r['resourceId']))
    if n is None:
        guard_errors.append({'key': k, 'issue': 'missing fresh node'})
        continue
    sources = [x for x in n['translatableContent'] if x['key'] == r['key']]
    translations = [x for x in n['translations'] if x['key'] == r['key'] and x['locale'] == r['locale'] and x.get('market') is None]
    if len(sources) != 1 or len(translations) > 1:
        guard_errors.append({'key': k, 'issue': 'ambiguous fresh source/translation'})
        continue
    source = sources[0]
    before = r.get('before')
    before_value = before.get('value') if isinstance(before, dict) else before
    fresh_value = translations[0]['value'] if translations else None
    if r['source'] != source['value']:
        guard_errors.append({'key': k, 'issue': 'source text drift'})
    if before_value != fresh_value:
        guard_errors.append({'key': k, 'issue': 'before-value drift'})
    if isinstance(before, dict) and before.get('locale', r['locale']) != r['locale']:
        guard_errors.append({'key': k, 'issue': 'before locale mismatch'})
    if bmap[k]['translatableContentDigest'] != source['digest']:
        guard_errors.append({'key': k, 'issue': 'bound digest differs from fresh source'})
    if r['sourceDigest'] != source['digest']:
        refreshed.append(k)
check('fresh_source_text_before_value_and_bound_digest_guards', not guard_errors, {'checkedFields': len(rows), 'errors': guard_errors, 'translationMatch': 'exact requested locale and key with market null; MAIN all-locale response filtered'})
faqid = 'gid://shopify/Page/161933381'
aboutid = 'gid://shopify/Page/161498117'
locales = set(r['locale'] for r in rows)
expected_refresh = {(resource, locale, 'body_html') for resource in (faqid, aboutid) for locale in locales}
check('exact40_updated_faq_about_digests', len(locales) == 20 and set(refreshed) == expected_refresh and bound['sourceDigestsRefreshed'] == 40,
      {'refreshedFields': len(refreshed), 'resources': [faqid, aboutid], 'locales': sorted(locales)})

batch_translations = []
batch_errors = []
for record in bound['batches']:
    payload = read(record['path'])
    if record['sha256'] != snapshots[str(B/record['path'])]:
        batch_errors.append({'path': record['path'], 'issue': 'hash mismatch'})
    if payload['resourceId'] != record['resourceId'] or len(payload['translations']) != record['fields']:
        batch_errors.append({'path': record['path'], 'issue': 'resource/count mismatch'})
    for t in payload['translations']:
        batch_translations.append(dict(t, resourceId=payload['resourceId']))
batch_keys = [key(r) for r in batch_translations]
check('41_mutation_batches_exact_bound_payload', len(bound['batches']) == 41 and len(batch_keys) == 813 and len(batch_keys) == len(set(batch_keys)) and set(batch_keys) == set(bkeys) and all(r == bmap[key(r)] for r in batch_translations) and not batch_errors,
      {'batches': len(bound['batches']), 'fields': len(batch_keys), 'errors': batch_errors})

alignment = read('resource-translations/final_faq_destination_customs_20.json')
faq_errors = []
for ar in alignment['rows']:
    row = cmap.get(key(ar))
    ps = re.findall(r'<p\b[^>]*>.*?</p>', row['value'], re.S) if row else []
    if len(ps) != 70:
        faq_errors.append({'locale': ar['locale'], 'issue': 'not70 paragraphs'})
        continue
    for p in ar['canonicalParagraphs']:
        if ps[p['paragraphIndexZeroBased']] != p['value']:
            faq_errors.append({'locale': ar['locale'], 'paragraphIndex': p['paragraphIndexZeroBased'], 'issue': 'canonical value mismatch'})
check('all20_faq_destination_and_customs_paragraphs_exact', len(alignment['rows']) == 20 and not faq_errors, {'paragraphs': 40, 'errors': faq_errors})

prefixes = {locale: ('pt' if locale == 'pt-BR' else locale) for locale in locales}
href_errors = []
internal_count = 0
pt_count = 0
preserved_service_hrefs = []
for r in rows:
    for raw in re.findall(r'\bhref=["\']([^"\']+)', r['value']):
        u = urlsplit(html.unescape(raw))
        internal = (u.hostname in ('dresslikemommy.com', 'www.dresslikemommy.com') or (not u.scheme and not u.netloc and u.path.startswith('/')))
        if not internal:
            continue
        internal_count += 1
        if u.path.startswith(('/account', '/checkout', '/cart', '/apps', '/cdn')):
            source_hrefs = re.findall(r'\bhref=["\']([^"\']+)', r['source'])
            if raw not in source_hrefs:
                href_errors.append({'key': key(r), 'href': raw, 'issue': 'service/authentication route changed from source'})
            preserved_service_hrefs.append({'key': key(r), 'href': raw})
            continue
        prefix = '/' + prefixes[r['locale']]
        if r['locale'] == 'pt-BR':
            pt_count += 1
        if u.path != prefix and not u.path.startswith(prefix + '/'):
            href_errors.append({'key': key(r), 'href': raw, 'expectedPrefix': prefix})
check('owned_content_hrefs_same_locale_including_pt_and_service_routes_preserved', not href_errors, {'internalHrefs': internal_count, 'ownedContentHrefs': internal_count - len(preserved_service_hrefs), 'portugueseHrefsUsingPt': pt_count, 'sourcePreservedServiceHrefs': preserved_service_hrefs, 'errors': href_errors})

# Compare approved policy text exactly, tolerating only the documented href localization.
# Re-reading source candidate artifacts detects accidental integration transformations;
# independent repair artifacts additionally pin the reviewed Swedish/Polish policy outputs.
def strip_internal_prefixes(value):
    def replace(m):
        raw = html.unescape(m.group(2))
        u = urlsplit(raw)
        if not (u.hostname in ('dresslikemommy.com', 'www.dresslikemommy.com') or (not u.scheme and not u.netloc and u.path.startswith('/'))):
            return m.group(0)
        path = u.path or '/'
        parts = path.split('/')
        if len(parts) > 1 and parts[1] in set(prefixes.values()) | {'en'}:
            path = '/' + '/'.join(parts[2:])
        normalized = urlunsplit(('', '', path, u.query, u.fragment))
        return m.group(1) + normalized + m.group(3)
    return re.sub(r'(\bhref=["\'])([^"\']+)(["\'])', replace, value)

artifacts = {}
artifact_rows = {}
input_drift = []
for path, digest in candidate['inputs'].items():
    data = read(path)
    artifacts[path] = data
    if snapshots[str(B/path)] != digest:
        input_drift.append(path)
    if 'plans' in data:
        flat = [dict(r, resourceId=p['resourceId'], locale=p['locale']) for p in data['plans'] for r in p['rows']]
    else:
        flat = data.get('rows', [])
    artifact_rows[path] = {key(r): r for r in flat if all(x in r for x in ('resourceId', 'locale', 'key'))}
check('candidate_input_hashes_unchanged', not input_drift, input_drift)
policy_errors = []
policy_count = 0
preserved_count = 0
for r in rows:
    if '/ShopPolicy/' not in r['resourceId']:
        continue
    policy_count += 1
    path = r['candidateArtifact']
    if path.endswith('/preserved_internal_root_links.json'):
        expected = r['before']['value']
        preserved_count += 1
    else:
        original = artifact_rows[path].get(key(r))
        if original is None:
            policy_errors.append({'key': key(r), 'issue': 'no reviewed input row'})
            continue
        expected = original['value']
    if strip_internal_prefixes(r['value']) != strip_internal_prefixes(expected):
        policy_errors.append({'key': key(r), 'issue': 'policy text changed beyond href normalization'})
check('reviewed_policy_conditions_exclusions_unchanged_during_integration', not policy_errors,
      {'policyBodies': policy_count, 'existingGoodBodiesHrefOnly': preserved_count, 'errors': policy_errors, 'method': 'exact body comparison against reviewed input artifacts, neutralizing only same-origin href locale prefixes'})

supp = read('resource-translations/supplemental_exact_repairs.json')
sv = supp['swedishRefundReplacement']
review = read('resource-translations/independent_help_review_repairs.json')
pl = next(r for r in review['rows'] if r['resourceId'] == 'gid://shopify/ShopPolicy/14695685' and r['locale'] == 'pl')
check('reviewed_swedish_and_polish_refund_fixes_integrated', all(strip_internal_prefixes(cmap[key(r)]['value']) == strip_internal_prefixes(r['proposedValue']) for r in (sv, pl)))

tracking = artifacts['help-translations/tracking_widget_language.json']
track_errors = []
tracking_id = 'gid://shopify/Page/18847760481'
tracking_keys = {key(r) for r in rows if r['resourceId'] == tracking_id and r['key'] == 'body_html'}
documented_codes = tracking['documentation']['mapping']
def mask_allowed_strings(value):
    value, button_count = re.subn(r'(<input\b[^>]*\btype="button"[^>]*\bvalue=")[^"]*(")', r'\1[BUTTON]\2', value)
    value, alert_count = re.subn(r'(alert\(")[^"]*("\))', r'\1[ALERT]\2', value)
    value, lang_count = re.subn(r'(YQ_Lang:\s*")[^"]*(")', r'\1[LANG]\2', value)
    return value, (button_count, alert_count, lang_count)
for r in tracking['rows']:
    release = cmap.get(key(r))
    if release is None or release['value'] != r['value']:
        track_errors.append({'locale': r['locale'], 'issue': 'release differs from reviewed tracking value'})
        continue
    expected_lang = documented_codes.get(r['locale'], 'en')
    actual_lang = re.findall(r'YQ_Lang:\s*"([^"]*)"', release['value'])
    if actual_lang != [expected_lang] or r['desiredYQLang'] != expected_lang:
        track_errors.append({'locale': r['locale'], 'issue': 'undocumented widget code'})
    if r['baseValuePath'].endswith('content_before_apply.json'):
        n = fresh_nodes[(r['locale'], tracking_id)]
        base = next(x['value'] for x in n['translations'] if x['locale'] == r['locale'] and x['key'] == 'body_html' and x.get('market') is None)
    else:
        path = 'help-translations/' + Path(r['baseValuePath']).name
        base = artifact_rows[path][key(r)]['value']
    if h(base) != r['baseValueSHA256']:
        track_errors.append({'locale': r['locale'], 'issue': 'base value hash mismatch'})
    m1, counts1 = mask_allowed_strings(base)
    m2, counts2 = mask_allowed_strings(release['value'])
    if m1 != m2 or counts1 != (1, 1, 1) or counts2 != (1, 1, 1):
        track_errors.append({'locale': r['locale'], 'issue': 'change outside button, alert, language strings'})
    if 'value="TRACK"' in release['value'] or 'alert("Enter your number.")' in release['value']:
        track_errors.append({'locale': r['locale'], 'issue': 'English visible control remains'})
check('tracking20_rows_only_documented_codes_and_three_string_locations', len(tracking_keys) == 20 and {key(r) for r in tracking['rows']} == tracking_keys and not track_errors,
      {'rows': len(tracking_keys), 'documentedLocalizedCodes': 17, 'unknownNativeLocalesRetainEn': ['ar', 'he', 'hi'], 'errors': track_errors})

changed_during_review = [path for path, sha in snapshots.items() if hashlib.sha256(Path(path).read_bytes()).hexdigest() != sha]
check('review_inputs_stable_during_check', not changed_during_review, changed_during_review)

report = {
    'status': 'PASS' if not failures else 'FAIL',
    'scope': 'Independent local integration check; broad translation semantics reviewed earlier and not repeated. No candidate edits, no external calls or live writes.',
    'candidateSha256': snapshots[str(B/'content_release_candidate.json')],
    'boundSha256': snapshots[str(B/'content_release_bound.json')],
    'freshBeforeSnapshotSha256': snapshots[str(B/'content_before_apply.json')],
    'checks': checks,
    'failures': failures,
    'notes': [
        'PASS applies only to these exact file hashes. Any final homepage correction requires regeneration/rebinding and rerunning this checker.',
        'Before guard compares exact existing value at locale/key/market:null; outdated metadata can change when the authorized English source is updated.',
        'Candidate contains old digests for exactly40 FAQ/About rows; bound payload uses fresh post-source-update digests in every case.',
        'Same-locale href correctness is a static destination check, not proof each rendered destination has been browser-verified.',
        'Parent confirmed intentional builder exceptions for account/checkout/cart/apps/cdn routes. All15 present account hrefs retain the exact English-source endpoint. Account/login flow was not tested and no authentication was attempted.',
        'Widget native language support remains unknown for ar/he/hi; only visible page controls are localized there and documented fallback en is retained.',
    ],
    'evidenceFilesSha256': snapshots,
}
(R/'final_integration_review.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
print(json.dumps({'status': report['status'], 'checks': len(checks), 'failures': failures, 'candidateSHA256': report['candidateSha256'], 'artifactSHA256': hashlib.sha256((R/'final_integration_review.json').read_bytes()).hexdigest()}, ensure_ascii=False))
