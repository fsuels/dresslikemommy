// Age-group derivation for Google Merchant Center.
//
// GMC values: newborn | infant | toddler | kids | adult
// GMC age brackets:
//   newborn:  0–3 months
//   infant:   3–12 months
//   toddler:  1–5 years
//   kids:     5–13 years
//   adult:    13+ years
//
// Inputs we look at, in order of trust:
//   1. variant.size (already classified by the option-name slot mapping)
//   2. variant.option1/2/3 (raw)
//   3. product.title / product.tags
//
// Output:
//   { value: <gmcValue|null>, confidence: 'high'|'medium'|'low'|'none', reason: <string> }
//
// "confidence: high" items are safe to push to the supplemental feed.
// "medium"/"low" should be reviewed before upload.

const MONTH_RE = /\b(\d+)\s*(?:month|mo|m)\b/i;
const YEAR_RE = /\b(\d+(?:\s*-\s*\d+)?)\s*(?:year|yr|y)s?\b/i;
const NEWBORN_RE = /\b(?:newborn|nb|preemie|0[\s-]?3\s*m)\b/i;
const ADULT_LITERAL_RE = /\b(?:adult|mother|mom|mommy|father|dad|daddy|men|women|man|woman)\b/i;
const KIDS_LITERAL_RE = /\b(?:kid|kids|child|children|youth|junior|girl|boy|teen)\b/i;
const TODDLER_LITERAL_RE = /\b(?:toddler)\b/i;
const INFANT_LITERAL_RE = /\b(?:infant|baby)\b/i;
const ADULT_LETTER_SIZE_RE = /\b(?:XX?S|XS|S|M|L|XL|2XL|3XL|4XL|5XL)\b/;

/**
 * Classify a single string (size value, title, etc.).
 * @param {string} s
 * @returns {{value: string|null, confidence: 'high'|'medium'|'low'|'none', reason: string} | null}
 */
function classifyOne(s) {
  if (!s) return null;
  const str = String(s).trim();
  if (!str) return null;

  // Newborn first — most specific.
  if (NEWBORN_RE.test(str)) return { value: 'newborn', confidence: 'high', reason: `matched newborn keyword in "${str}"` };

  // Explicit "Baby N Months" → infant or newborn.
  const m = str.match(MONTH_RE);
  if (m) {
    const months = Number(m[1]);
    if (months <= 3) return { value: 'newborn', confidence: 'high', reason: `${months}mo ≤ 3mo` };
    if (months <= 12) return { value: 'infant', confidence: 'high', reason: `${months}mo in (3,12]` };
    // 13mo+ falls through to year handling
  }

  // "Child N Years" / "Child N-N Years" → toddler/kids/adult by lower bound.
  const y = str.match(YEAR_RE);
  if (y) {
    const lower = Number(y[1].split(/\s*-\s*/)[0]);
    if (lower < 1) return { value: 'infant', confidence: 'high', reason: `<1yr` };
    if (lower < 5) return { value: 'toddler', confidence: 'high', reason: `${lower}yr in [1,5)` };
    if (lower < 13) return { value: 'kids', confidence: 'high', reason: `${lower}yr in [5,13)` };
    return { value: 'adult', confidence: 'high', reason: `${lower}yr ≥ 13yr` };
  }

  // Word-only signals.
  if (TODDLER_LITERAL_RE.test(str)) return { value: 'toddler', confidence: 'high', reason: 'matched toddler keyword' };
  if (INFANT_LITERAL_RE.test(str)) return { value: 'infant', confidence: 'medium', reason: 'matched infant/baby keyword' };
  if (KIDS_LITERAL_RE.test(str)) return { value: 'kids', confidence: 'medium', reason: 'matched kids keyword' };

  // Adult literals (Mother/Father/Adult) + adult letter sizes are high confidence
  // because the catalog's own size taxonomy uses them ("Adult S", "Mother 2XL", etc.).
  if (ADULT_LITERAL_RE.test(str)) {
    return { value: 'adult', confidence: 'high', reason: 'matched adult/mother/father keyword' };
  }

  // Bare letter-size like "S" or "2XL" — only trust if the whole string is just that
  // (we don't want to match the "S" inside "Sleepwear").
  if (ADULT_LETTER_SIZE_RE.test(str) && /^(?:XX?S|XS|S|M|L|XL|2XL|3XL|4XL|5XL)$/.test(str)) {
    return { value: 'adult', confidence: 'low', reason: 'standalone adult letter size' };
  }

  return null;
}

/**
 * Pick the most specific / highest-confidence classification across multiple signals.
 */
function combine(results) {
  // Drop nulls.
  const xs = results.filter(Boolean);
  if (xs.length === 0) return { value: null, confidence: 'none', reason: 'no age signal' };

  // Specificity ordering: newborn > infant > toddler > kids > adult.
  // We don't pick "most specific" blindly — we pick the highest-confidence;
  // ties broken by specificity rank.
  const rank = { newborn: 5, infant: 4, toddler: 3, kids: 2, adult: 1 };
  const conf = { high: 3, medium: 2, low: 1, none: 0 };
  xs.sort((a, b) => {
    const c = conf[b.confidence] - conf[a.confidence];
    if (c !== 0) return c;
    return rank[b.value] - rank[a.value];
  });
  return xs[0];
}

/**
 * Derive age_group for a single GMC item.
 *
 * Tiered fallback — variant size is authoritative because product-level tags
 * and titles can describe the WHOLE family-matching set (e.g. tags include
 * both "Mother S" and "Child 1-2yr" on every variant). Using product-level
 * signals when the variant's own size already classifies would misroute the
 * item.
 *
 *   tier 1 (highest):  variant size + raw option1/2/3
 *   tier 2 (fallback): product title + tags
 *
 * Within a tier we still use combine() to pick the strongest signal.
 *
 * @param {{size?: string, title?: string, tags?: string[], option1?: string, option2?: string, option3?: string}} item
 * @returns {{value: string|null, confidence: 'high'|'medium'|'low'|'none', reason: string}}
 */
export function deriveAgeGroup(item) {
  const variantSignals = [
    classifyOne(item.size),
    classifyOne(item.option1),
    classifyOne(item.option2),
    classifyOne(item.option3),
  ].filter(Boolean);

  if (variantSignals.length) return combine(variantSignals);

  const productSignals = [
    classifyOne(item.title),
    ...(Array.isArray(item.tags) ? item.tags.map(classifyOne) : []),
  ].filter(Boolean);

  return combine(productSignals);
}

// Exposed for tests.
export const _internal = { classifyOne, combine };
