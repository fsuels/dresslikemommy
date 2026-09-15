# Navy French hip-label follow-up

This is a separate local candidate based on the French body **after the pending 42-field repair**, not a current live-body observation. The frozen parent proposal remains unchanged.

Exactly two replacements, one in column 8 of `size-chart` and one in column 8 of `size-chart-cardigan`:

`<th>Hip (cm/po)</th>` → `<th>Hanches (cm/po)</th>`

`Hanches` is the natural French label for the hip region in a clothing size chart. It does not infer that a value is a circumference; `tour de hanches` would add that interpretation and is intentionally not used. The existing `cm/po` units remain exact. No numerical conversion occurs.

Local validation passed: 240 data cells unchanged byte-for-byte, 18 other headers unchanged, identical HTML tag/attribute order and chart geometry, identical numeric sequence, exact inverse recovery of the prior body, and every byte outside the two labels unchanged. Parent proposal immutability was checked.

Before candidate body SHA-256: `d53c181559e9ac10fcf8d2a1b1f9afee9be3b6f062ef60a69aa44f5b5c807b89`

After candidate body SHA-256: `d9289e4ea7c86b903d9cf5e36cd6aac74d9d65153e97c998c797b484d654b595`

Proposal SHA-256: `bfb1be4aad96a16c9ae13774ba7c988e207062c9391ba46b55d9189031cc8c9c`

Builder SHA-256: `28d1969e874e2d8a4e3262897f5bdb2f26b149ec18032644ba79c959e5344b0a`

Root must first verify completion of the 42-field repair, then freshly read the actual global French body and current English source digest. The actual French body must match the bound after-42 candidate. Any drift requires review before registration. No digest is invented here, and no live mutation was attempted.
