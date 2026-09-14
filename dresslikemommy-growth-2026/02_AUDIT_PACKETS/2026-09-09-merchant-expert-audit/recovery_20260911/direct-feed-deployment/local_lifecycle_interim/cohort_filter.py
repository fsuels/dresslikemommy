"""Pure, byte-preserving containment of reviewed parent-level eligibility holds.

No network, credentials, source mutation, scheduler or publication code.
"""
import copy
import hashlib
import json
import re


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(body):
    return hashlib.sha256(body).hexdigest()


def apply_holds(body, manifest, diagnostics, hold_bytes, previous_ids, protected_ids=(), source_parent_ids=None):
    holds = json.loads(hold_bytes)
    require(holds.get('schemaVersion') == 1 and manifest['market']['key'] in holds.get('markets', []), 'hold_scope_mismatch')
    entries = holds.get('holds')
    require(isinstance(entries, list), 'hold_list_missing')
    ids = [item.get('product_id') for item in entries]
    require(len(set(ids)) == len(ids) and all(isinstance(i, str) and re.fullmatch(r'gid://shopify/Product/\d+', i) for i in ids), 'invalid_or_duplicate_held_parent')
    require(all(item.get('reason') and item.get('release_condition') and item.get('evidence') for item in entries), 'hold_evidence_missing')
    held = set(ids)
    require(isinstance(source_parent_ids, (list, tuple))
            and len(source_parent_ids) == manifest['sourceParents']
            and len(set(source_parent_ids)) == len(source_parent_ids)
            and all(isinstance(i, str) and re.fullmatch(r'gid://shopify/Product/\d+', i) for i in source_parent_ids),
            'complete_source_parent_ids_required')
    known_parents = set(source_parent_ids)
    require(held <= known_parents, 'unknown_held_parent')
    country = manifest['market']['country']
    require(manifest['sha256'] == sha(body) and manifest['bytes'] == len(body), 'input_hash_mismatch')
    require(manifest['objectEtag'] == manifest['expectedMd5'] == hashlib.md5(body).hexdigest(), 'input_md5_mismatch')
    lines = body.splitlines(keepends=True)
    row_ids = manifest['rowIds']
    require(len(lines) == len(row_ids) + 1 and len(row_ids) == manifest['rows'] and len(set(row_ids)) == len(row_ids), 'input_rows_not_single_line_unique_tsv')
    kept_lines, kept_ids, removed_rows = [lines[0]], [], []
    parent_counts, removed_counts = {}, {}
    for line, offer in zip(lines[1:], row_ids):
        require(line.split(b'\t', 1)[0].decode() == offer, 'input_line_id_mismatch')
        match = re.fullmatch(r'shopify_' + re.escape(country) + r'_(\d+)_(\d+)', offer)
        require(bool(match), 'input_offer_country_mismatch')
        parent = 'gid://shopify/Product/' + match[1]
        require(parent in known_parents, 'offer_parent_not_in_complete_source')
        if parent in held:
            removed_rows.append({'id': offer, 'productId': parent,
                                 'variantId': 'gid://shopify/ProductVariant/' + match[2],
                                 'code': 'reviewed_parent_eligibility_hold', 'variants': 1})
            removed_counts[parent] = removed_counts.get(parent, 0) + 1
        else:
            kept_lines.append(line); kept_ids.append(offer)
            parent_counts[parent] = parent_counts.get(parent, 0) + 1
    require(kept_ids and set(protected_ids) <= set(kept_ids), 'empty_cohort_or_protected_offer_lost')
    require(len(previous_ids) == len(set(previous_ids)), 'previous_ids_duplicate')
    result = b''.join(kept_lines)
    new = copy.deepcopy(manifest)
    digest = sha(result); md5 = hashlib.md5(result).hexdigest()
    new.update(sha256=digest, expectedMd5=md5, objectEtag=md5,
               objectKey='merchant/' + manifest['market']['key'] + '/' + digest + '.tsv',
               bytes=len(result), rows=len(kept_ids), rowIds=kept_ids)
    report = copy.deepcopy(diagnostics)
    previous = set(previous_ids); current = set(kept_ids)
    report['rows'] = len(kept_ids)
    report['lifecycle'] = {'added': sorted(current - previous), 'removed': sorted(previous - current),
                           'retained': sorted(previous & current), 'previousIdsProvided': True}
    report['exclusions'] = report.get('exclusions', []) + removed_rows
    exception_parents = {item['productId'] for item in report.get('returnCohorts', [])
                         if item.get('classification') == 'verified_policy_exception'}
    exception_removed = sum(item['productId'] in exception_parents for item in removed_rows)
    require(report.get('exceptionRows', 0) >= exception_removed, 'exception_count_conflict')
    report['exceptionRows'] = report.get('exceptionRows', 0) - exception_removed
    report['returnCohorts'] = [item for item in report.get('returnCohorts', []) if item['productId'] not in held]
    report['eligibilityHolds'] = {
        'hold_spec_sha256': sha(hold_bytes), 'input_feed_sha256': sha(body),
        'held_parent_ids': sorted(held), 'removed_available_rows': len(removed_rows),
        'removed_rows_by_parent': removed_counts, 'kept_rows': len(kept_ids),
        'known_held_parents_without_available_rows': sorted(held - removed_counts.keys()),
        'kept_parents': len(parent_counts), 'retained_lines_byte_identical': True,
        'protected_ids': list(protected_ids),
        'scope': 'Merchant eligibility only; Shopify product status/options/stock/content are unchanged. Source snapshot/counts/timestamps remain the original complete read.'}
    return result, new, report
