from pathlib import Path
from collections import Counter
import hashlib
import json

P = Path(__file__).resolve().parent
R = P.parent.parent
S = R / 'products/remaining'
def read(p): return json.loads(p.read_text())
def key(r): return (r['resourceId'], r['locale'], r['key'])
def write(name, data): (P/name).write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n')
baseline = {key(r): r for r in read(S/'baseline.json')['rows']}
release_files = [R/'review/qualified_product_release_index.json', R/'review/root_product_release_rows.json', R/'review/german_title_correction_proposals.json']
released = {key(r) for f in release_files for r in read(f)['rows']}
held = read(R/'review/held_product_ledger.json')['existingSourceAndChartHolds']
retained = read(S/'no_change_outdated_metadata.json')['rows']
correctable, source_holds = [], []
for row in held:
    assert key(row) not in released, key(row)
    evidence_file = R/row['evidenceFile']
    evidence = next(r for r in read(evidence_file)['rows'] if key(r)==key(row))
    repairable = False
    why = 'Source contradiction, factual ambiguity, shipping/return promise or exposed internal source copy requires root source disposition.'
    artifact = row['artifact']
    if artifact == 'body_source_holds.json':
        repairable = all('Current source has no size table' in s for s in evidence['reasons'])
        if repairable: why = 'Reconstruct source body without obsolete translated-only size table.'
    elif artifact == 'older_stale_table_holds.json':
        repairable = True
        why = 'Reconstruct complete source HTML and single source chart; replace malformed translated HTML or duplicate charts.'
    elif artifact in ['ru_body_final_holds.json', 'sv_body_final_holds.json']:
        pid = row['resourceId'].rsplit('/',1)[-1]
        repairable = pid not in ['7227630649441','7229128441953','7497751986273','7502791671905','7545279840353']
        if repairable: why = 'Reconstruct source HTML, images and complete chart with current source numbers and age labels; inherited translation variance is repairable.'
    elif artifact == 'changed_source_chart_holds.json':
        repairable = row['resourceId'].endswith('/7545279512673')
        if repairable: why = 'Translate complete current Sunshine source with its current chart and product-facing text; replace outdated translation facts.'
    b = baseline[key(row)]
    assert b['sourceDigest'] == evidence['sourceDigest']
    target = correctable if repairable else source_holds
    target.append({**b, 'sourceValue': b['source'], 'priorHoldArtifact': artifact, 'remainderDisposition': 'TRANSLATION_ONLY_REPAIRABLE' if repairable else 'ROOT_SOURCE_DISPOSITION', 'dispositionReason': why, 'priorEvidence': str(evidence_file.relative_to(R))})

retained_rows=[]
for r in retained:
    assert key(r) not in released
    b=baseline[key(r)]
    assert b['before'] and b['before']['outdated'] and b['sourceDigest']==r['sourceDigest']
    retained_rows.append({**b,'sourceValue':b['source'],'priorNoChangeArtifact':r['artifact']})

write('translation_only_held_worklist.json',{'rows':correctable})
write('source_disposition_worklist.json',{'rows':source_holds})
write('retained96_worklist.json',{'rows':retained_rows})
counts={
    'originalHeld':len(held),'translationOnlyRepairable':len(correctable),'sourceDisposition':len(source_holds),
    'repairableByLocale':dict(Counter(r['locale'] for r in correctable)),
    'repairableByArtifact':dict(Counter(r['priorHoldArtifact'] for r in correctable)),
    'sourceDispositionByKey':dict(Counter(r['key'] for r in source_holds)),
    'retainedOutdated':len(retained_rows),'retainedByKey':dict(Counter(r['key'] for r in retained_rows)),
    'alreadyQualifiedExcluded':len(released),'overlapQualified':0,
}
write('inventory.json',{'counts':counts,'sourceFreshness':'Bound to supplied read-only baseline; root performs live digest/before guards.','inputs':{str(f.relative_to(R)):hashlib.sha256(f.read_bytes()).hexdigest() for f in [S/'baseline.json',S/'no_change_outdated_metadata.json',R/'review/held_product_ledger.json',*release_files]}})
print(json.dumps(counts))
