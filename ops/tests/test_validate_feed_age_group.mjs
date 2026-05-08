import assert from 'node:assert/strict';

import { deriveAgeGroup } from '../../scripts/validateFeed/ageGroup.js';

const cases = [
  ['Child 4T / Pink', 'toddler', 'high'],
  ['Child 5-6T / Pink', 'kids', 'high'],
  ['Child 10-12T / Pink', 'kids', 'high'],
  ['Baby 0-3 Months / Stripes', 'newborn', 'high'],
  ['Baby 0-6 Months / Stripes', 'infant', 'high'],
  ['Baby 6-12 Months / Stripes', 'infant', 'high'],
  ['Baby 12-18 Months / Stripes', 'toddler', 'high'],
  ['Mother XL / Blue', 'adult', 'high'],
];

for (const [size, expectedValue, expectedConfidence] of cases) {
  const actual = deriveAgeGroup({ size, option1: size });
  assert.equal(actual.value, expectedValue, `${size} value`);
  assert.equal(actual.confidence, expectedConfidence, `${size} confidence`);
}

