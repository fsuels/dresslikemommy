// Category bucketing for Merchant Center triage.
// Each bucket is a list of regexes tested (case-insensitive) against
// the union of: product.tags + product.product_type + product.title.
// A product can land in multiple buckets — that's intentional, since a
// "mommy and me pajama set" should show up in both PAJAMAS and FAMILY_MATCHING.
//
// Edit this file to fix tag drift; do not change the bucket KEYS without
// updating the GitHub Action's report routing.

export const BUCKETS = {
  MOMMY: [
    /\bmommy\b/i,
    /\bmom\b/i,
    /\bmother\b/i,
    /\bmommy[\s-]?and[\s-]?me\b/i,
  ],
  DADDY_ME: [
    /\bdaddy\b/i,
    /\bdad\b/i,
    /\bfather\b/i,
    /\bdaddy[\s-]?and[\s-]?me\b/i,
    /\bdaddy[\s-]?&[\s-]?me\b/i,
  ],
  FAMILY_MATCHING: [
    /\bfamily[\s-]?matching\b/i,
    /\bmatching[\s-]?family\b/i,
    /\bmatching[\s-]?set\b/i,
    /\bcoordinating\b/i,
  ],
  PAJAMAS: [
    /\bpajama/i,
    /\bpjs?\b/i,
    /\bsleepwear\b/i,
    /\bnightwear\b/i,
    /\bloungewear\b/i,
  ],
  SWIMSUITS: [
    /\bswim/i,
    /\bswimsuit\b/i,
    /\bbikini\b/i,
    /\bbathing[\s-]?suit\b/i,
    /\bone[\s-]?piece\b/i,
  ],
};

/**
 * Return all bucket keys that match a given product.
 * @param {{tags?: (string[]|string), product_type?: string, title?: string}} product
 * @returns {string[]}
 */
export function bucketsFor(product) {
  const tags = Array.isArray(product.tags)
    ? product.tags
    : typeof product.tags === 'string'
      ? product.tags.split(',').map((t) => t.trim())
      : [];
  const haystack = [
    ...tags,
    product.product_type || '',
    product.title || '',
  ]
    .filter(Boolean)
    .join(' | ');

  const hits = [];
  for (const [bucket, patterns] of Object.entries(BUCKETS)) {
    if (patterns.some((re) => re.test(haystack))) hits.push(bucket);
  }
  return hits.length ? hits : ['UNCATEGORIZED'];
}
