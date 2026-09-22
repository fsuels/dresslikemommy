"""Bind reviewed translations to fresh source and before-state; no external writes."""
import hashlib
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main():
    candidate = json.loads((ROOT / 'content_release_candidate.json').read_text())
    fresh = json.loads((ROOT / 'content_before_apply.json').read_text())
    nodes = {(batch['locale'], n['resourceId']): n for batch in fresh for n in batch['nodes']}
    groups = defaultdict(list)
    bound = []
    refreshed = 0
    for row in candidate['rows']:
        node = nodes[(row['locale'], row['resourceId'])]
        source = next(c for c in node['translatableContent'] if c['key'] == row['key'])
        before = [c for c in node['translations'] if c['key'] == row['key']]
        assert len(before) <= 1, 'Duplicate returned locale key'
        before = before[0] if before else None
        assert source['value'] == row['source'], (row['locale'], row['key'], 'Source changed')
        assert (before or {}).get('value') == (row['before'] or {}).get('value'), (row['locale'], row['key'], 'Before value changed')
        if source['digest'] != row['sourceDigest']:
            assert row.get('sourceChangePending'), 'Unexpected source digest change'
            refreshed += 1
        item = {'locale': row['locale'], 'key': row['key'], 'value': row['value'],
                'translatableContentDigest': source['digest']}
        groups[row['resourceId']].append(item)
        bound.append({'resourceId': row['resourceId'], **item})
    out = ROOT / 'mutation_batches'
    out.mkdir(exist_ok=True)
    batches = []
    for rid, items in sorted(groups.items()):
        current = []
        for item in items:
            if current and (len(json.dumps(current, ensure_ascii=False)) + len(json.dumps(item, ensure_ascii=False)) > 30000 or len(current) == 100):
                batches.append({'resourceId': rid, 'translations': current})
                current = []
            current.append(item)
        if current:
            batches.append({'resourceId': rid, 'translations': current})
    manifest = []
    for i, batch in enumerate(batches):
        path = out / f'{i:03}.json'
        path.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + '\n')
        manifest.append({'path': str(path.relative_to(ROOT)), 'resourceId': batch['resourceId'],
                         'fields': len(batch['translations']), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
    release = {'status': 'FRESH_SOURCE_AND_BEFORE_GUARDS_PASS',
               'candidateSHA256': hashlib.sha256((ROOT / 'content_release_candidate.json').read_bytes()).hexdigest(),
               'fields': len(bound), 'sourceDigestsRefreshed': refreshed, 'batches': manifest,
               'translations': bound}
    (ROOT / 'content_release_bound.json').write_text(json.dumps(release, ensure_ascii=False, indent=2) + '\n')
    (ROOT / 'mutation_manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(json.dumps({'fields': len(bound), 'batches': len(batches), 'sourceDigestsRefreshed': refreshed}))


if __name__ == '__main__':
    main()
