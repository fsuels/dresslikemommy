import { SourceError } from './collector.js';

function requireValue(value, code) { if (!value) throw new SourceError(code); }
const nonempty = value => typeof value === 'string' && value.trim().length > 0;

export function readEligibilityHolds(spec) {
  if (spec === undefined) return { parents: new Map(), source: null, scope: null };
  requireValue(spec?.schemaVersion === 1 && spec.scope === 'all_markets_and_locales', 'invalid_eligibility_hold_scope');
  requireValue(nonempty(spec.source?.path) && /^[a-f0-9]{64}$/.test(spec.source?.sha256 || ''), 'eligibility_hold_source_missing');
  requireValue(Array.isArray(spec.holds), 'eligibility_hold_list_missing');
  const parents = new Map();
  for (const hold of spec.holds) {
    requireValue(typeof hold?.product_id === 'string' && /^gid:\/\/shopify\/Product\/\d+$/.test(hold.product_id) &&
      !parents.has(hold.product_id), 'invalid_or_duplicate_held_parent');
    requireValue(nonempty(hold.reason) && nonempty(hold.release_condition) && Array.isArray(hold.evidence) &&
      hold.evidence.length > 0 && hold.evidence.every(nonempty), 'eligibility_hold_evidence_missing');
    parents.set(hold.product_id, hold);
  }
  return { parents, source: { ...spec.source }, scope: spec.scope };
}

export function summarizeEligibilityHolds(policy, products, exclusions) {
  const configuredParentIds = [...policy.parents.keys()];
  const sourceIds = new Set(products.map(product => product.id));
  const sourceParentIds = configuredParentIds.filter(id => sourceIds.has(id));
  const heldRows = exclusions.filter(item => item.code === 'reviewed_parent_eligibility_hold');
  const removedRowsByParent = {};
  for (const row of heldRows) removedRowsByParent[row.productId] = (removedRowsByParent[row.productId] || 0) + row.variants;
  return {
    scope: policy.scope, source: policy.source,
    configuredParentIds, sourceParentIds,
    // An archived/deleted held parent may be absent from a complete source. Keep
    // its hold so reactivation cannot silently put the product back in a feed.
    sourceAbsentParentIds: configuredParentIds.filter(id => !sourceIds.has(id)),
    removedAvailableRows: heldRows.reduce((total, row) => total + row.variants, 0),
    removedRowsByParent,
    sourceHeldParentsWithoutRemovedRows: sourceParentIds.filter(id => !removedRowsByParent[id]),
  };
}
