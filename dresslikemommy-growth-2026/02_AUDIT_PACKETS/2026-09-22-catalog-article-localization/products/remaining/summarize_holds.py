#!/usr/bin/env python3
import collections
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
manifest = json.loads((HERE / 'remaining_manifest.json').read_text())
held = [r for r in manifest['fieldLedger'] if r['status'] == 'PRECISE_SOURCE_OR_TABLE_HOLD']
groups = collections.defaultdict(list)
for row in held:
    groups[(row['resourceId'], row['key'], row['artifact'])].append(row['locale'])
actions = {
    'source_claim_holds.json': 'Align the English shipping/return promise with the current policy, then obtain fresh source digests and translate the corrected claim.',
    'meta_titles_source_holds.json': 'Resolve exact title/body/SEO garment or print contradiction before translating the SEO field.',
    'titles_000_067_held.json': 'Resolve bikini versus one-piece and unsupported Halloween print conflict from product evidence.',
    'titles_068_135_held.json': 'Resolve cotton/silk versus viscose/polyester composition conflict from seller evidence.',
    'body_source_holds.json': 'Resolve recorded material/claim/operator-copy conflict or obsolete chart in source_content_conflicts and body_source_holds before translation.',
    'body_construction_source_holds.json': 'Resolve one-piece versus two-piece swimsuit construction conflict.',
    'older_stale_table_holds.json': 'Normalize malformed translated HTML and reconcile duplicate charts without inventing or silently replacing measurement values.',
    'changed_source_chart_holds.json': 'Reconcile Sunshine/Raglan changed source tables with current options and seller measurements.',
    'ru_body_final_holds.json': 'Resolve exact per-field Russian source/table/markup hold, including stale Sunshine/Raglan charts despite no English prose gap.',
    'sv_body_final_holds.json': 'Resolve exact per-field Swedish measurement/source claim or legacy image variance; authored held drafts remain excluded.',
    'short_fields_review_holds.json': 'Resolve incorrect Red Heart Print SEO source for the red cardigan with gold heart buttons, then refresh source digest and translate.'
}
data = {
    'status': 'PRECISE_HOLDS_NO_SOURCE_OR_MEASUREMENT_CHANGES_APPLIED',
    'fields': len(held), 'distinctResources': len({r['resourceId'] for r in held}),
    'countsByKey': dict(collections.Counter(r['key'] for r in held)),
    'countsByArtifact': dict(collections.Counter(r['artifact'] for r in held)),
    'groups': [{'resourceId': rid, 'key': key, 'locales': sorted(locales), 'fields': len(locales),
                'evidence': artifact, 'evidenceSHA256': hashlib.sha256((HERE / artifact).read_bytes()).hexdigest(),
                'requiredResolution': actions[artifact]} for (rid, key, artifact), locales in sorted(groups.items())],
    'limits': ['Hold is specific to the field and source evidence; it does not hold unrelated qualified translations.',
               'No English source, product facts, measurements, policy promises or live fields changed by this lane.']
}
assert len(held) == 918
(HERE / 'remaining_hold_summary.json').write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
print({k: data[k] for k in ['fields', 'distinctResources', 'countsByKey']})
