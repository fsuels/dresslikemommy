"""Build a public, reviewable Shopify translation release; never writes externally."""
import copy
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent
LOCALES = set('ar cs da de el en es fi fr he hi it ja ko nl no pl pt ro ru sv'.split())


def read(name):
    return json.loads((ROOT / name).read_text())


def localized_href(href, locale):
    prefix = '/pt' if locale == 'pt-BR' else '/' + locale
    parsed = urlsplit(href)
    if parsed.netloc and parsed.netloc not in ('dresslikemommy.com', 'www.dresslikemommy.com'):
        return href
    if parsed.scheme and parsed.scheme not in ('http', 'https'):
        return href
    if not parsed.netloc and not href.startswith('/'):
        return href
    path = parsed.path or '/'
    if path.split('/')[1] in LOCALES:
        return href
    if path.startswith(('/account', '/checkout', '/cart', '/apps', '/cdn')):
        return href
    path = path.replace('/pages/shipping-and-delivery', '/policies/shipping-policy')
    result = prefix + ('' if path == '/' else path)
    if parsed.query:
        result += '?' + parsed.query
    if parsed.fragment:
        result += '#' + parsed.fragment
    return result


def localize_links(value, locale):
    return re.sub(r'(href\s*=\s*)([\"\'])(.*?)\2', lambda m: m[1] + m[2] + localized_href(m[3], locale) + m[2], value, flags=re.I)


def main():
    rows = []
    inputs = ['resource-translations/candidate_17_locales.json',
              'resource-translations/he_manual.json', 'resource-translations/ko_manual.json',
              'help-translations/pl_manual.json', 'help-translations/ru_manual.json',
              'help-translations/sv_manual.json', 'help-translations/shipping_manual.json',
              'help-translations/faq_corrections_group_a.json',
              'help-translations/faq_corrections_group_b.json',
              'help-translations/faq_corrections_group_c.json']
    for filename in inputs:
        data = read(filename)
        candidate_rows = [r for p in data['plans'] for r in p['rows']] if 'plans' in data else data['rows']
        for row in candidate_rows:
            row = copy.deepcopy(row)
            row['candidateArtifact'] = filename
            rows.append(row)
    assert len(read('help-translations/pl_manual.json')['rows']) == 4, 'Polish return page pending'
    by_key = {(r['resourceId'], r['locale'], r['key']): r for r in rows}
    assert len(by_key) == len(rows), 'Duplicate candidate translation key'
    tracking_file = 'help-translations/tracking_widget_language.json'
    inputs.append(tracking_file)
    for tracking in read(tracking_file)['rows']:
        key = (tracking['resourceId'], tracking['locale'], tracking['key'])
        if key in by_key:
            assert by_key[key]['before'] == tracking['before']
            rows.remove(by_key[key])
        row = copy.deepcopy(tracking)
        row['candidateArtifact'] = tracking_file
        rows.append(row)
        by_key[key] = row
    for link in read('resource-translations/preserved_internal_root_links.json')['links']:
        key = (link['resourceId'], link['locale'], link['key'])
        if key not in by_key:
            row = copy.deepcopy(link)
            row['value'] = row['before']['value']
            row['reason'] = 'Preserve translated policy wording; retain locale in owned internal links.'
            row['candidateArtifact'] = 'resource-translations/preserved_internal_root_links.json'
            rows.append(row)
            by_key[key] = row
    for row in rows:
        original = row['value']
        row['value'] = localize_links(original, row['locale'])
        row['internalLinksLocalized'] = original != row['value']
        assert row['value'].strip(), 'Empty translated value'
        assert 'assassinshoodies.com' not in row['value'], 'Foreign storefront link'
        assert 'mail%20to:' not in row['value'], 'Invalid email link'
    rows.sort(key=lambda r: (r['resourceId'], r['locale'], r['key']))
    output = {'status': 'REVIEWED_CANDIDATE_REQUIRES_FRESH_SOURCE_DIGEST_AND_BEFORE_GUARD',
              'themeId': 'gid://shopify/OnlineStoreTheme/133290917985',
              'rows': rows,
              'inputs': {f: hashlib.sha256((ROOT / f).read_bytes()).hexdigest() for f in inputs},
              'counts': {'fields': len(rows), 'resources': len({r['resourceId'] for r in rows}),
                         'locales': len({r['locale'] for r in rows}),
                         'linkLocalizedFields': sum(r['internalLinksLocalized'] for r in rows)}}
    (ROOT / 'content_release_candidate.json').write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(output['counts']))


if __name__ == '__main__':
    main()
