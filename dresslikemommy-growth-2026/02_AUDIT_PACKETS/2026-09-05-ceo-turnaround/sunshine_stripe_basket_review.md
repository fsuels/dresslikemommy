# Sunshine Stripe basket-ceiling review

Confidence: H for local arithmetic. **PASS after three precision corrections; conditional ceilings only, not launch readiness.** Reviewed 2026-09-06. I did not independently inspect UI, source/account identity, supplier stock, material/measurement evidence or a rendered buyer journey. Product IDs, variant labels and inputs agree across the supplied artifacts.

Procurement reconciles: Child 2 Years CNY22×2 plus Adult S/M/L CNY26×3 = **CNY122 goods, four purchased SKUs/five units**. Non-goods CNY3+86.72+0.22+32.50=122.44; provider total CNY244.44. Provider returns-number zero does not establish no customer returns.

All five scenarios use only those four purchased sizes and current individual prices: child $21.99, adult $24.99. Goods prices are historical inputs conditional on recurrence; they are not extended to the ten other current variants. Revenues sum individually selected tees, not a separately sold family bundle, bottoms or styling props.

Independent Decimal results:

| Scenario | Merchandise USD | Total/non-goods CNY ceilings | Required conversion at $0.15 CPC |
| --- | ---: | ---: | ---: |
| One Child 2 Years | 21.99 | 67.39 / 45.39 | 4.434% |
| One Adult S | 24.99 | 76.87 / 50.87 | 3.902% |
| Child 2 Years + Adult S | 46.98 | 146.09 / 98.09 | 2.076% |
| Child 2 Years + Adult S/M | 71.97 | 224.73 / 150.73 | 1.355% |
| Observed five tees | 118.95 | 370.34 / 248.34 | 0.820% |

For unknown disjoint USD expenses `E`, non-goods ceiling is `(0.70R − F − R/6.5 − E)/k − G`. Using `k=0.164265` includes funding handling once. `E=0` defines an upper envelope, not zero actual expenses; each $1 of E reduces capacity by approximately CNY6.08772. This historical funding factor is not an assigned settlement rate or future guarantee.

The four hypothetical fees are rounded half-up to cents before calculation: $0.94/$1.02/$1.66/$2.39. The 2.9%+$0.30 assumption is consistent with the sampled domestic allocations, not a verified future fee contract. The observed row uses the actual $4.13 allocation on $131.94 gross while excluding $12.99 priority revenue from merchandise.

Final corrections verified: provider ceilings floor to CNY0.01; required conversion percentages round upward to 0.001 percentage point; the pair is 2.076%, not a downward-rounded 2.075%. The observed row’s CNY125.90 headroom is explicitly conditional at E=0. JSON/CSV agree.

Thresholds count purchases per paid click and assume every conversion buys the listed basket; they are not all-session conversion rates. No future quote, shipping allocation, expected AOV, conversion forecast or approved CPA follows. Reusing the five-unit freight/services for smaller orders is unsupported. New quotes must confirm goods and non-goods costs; changed fees/rates/expenses change the ceilings. Meeting a ceiling is necessary, not sufficient. Retain buyer-path, purchase-capture, overlap, operating-account and exact authority gates.

SHA256 bindings:

- Offer: `d81646293a2693e028ac6b630ddcdfeacd40b9c56a4622af9d6f9377e77d53d3`
- Procurement: `e8bcb49a6b837d580f7a204bd6bff149774e5d01ec3d3b03b74cd318b5b6b4f0`
- Ceilings JSON: `0ca34b0a44935a345b29056e9becc8f7011ff36994bbb5fc1e2e620c75b3ed69`
- Ceilings CSV: `c8f9c717657125726a7e4f69fd631441a36a90629f0e3d1a4940012c6b33b762`
- Funding: `0a43d2c5d205e1503f903d2574e3b910426291ccda1661a73adfd15806eebf88`
- Payout fees: `1b1d642854e936ceb93fc14c01792b39156c6924aa39fd510147b8210e2e1b9d`
