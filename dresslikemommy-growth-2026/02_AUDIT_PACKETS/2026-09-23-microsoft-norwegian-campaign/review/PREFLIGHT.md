# Independent Norwegian campaign preflight

Verdict: **PASS_WITH_GATES** for paused preparation. **NOT approval to activate or spend.** Confidence: H for extraction; M for linguistic assessment. Reviewer owned only this report; no browser, external, source, canonical, or Git writes.

Sources: supplied `Pasted text.txt`, all files in `../payload/`, parent current-session readback messages. Attachment SHA256: `260573045d7e5979ac4137612486e5bfabc9ec24f9c663da6366d130c32ec109`. Reviewed regenerated `campaign_payload.json` SHA256: `06050488a4e2bb20bcb7674460cdf03c8b649f6c575e47656881b904b3feb37f`.

## VERIFIED locally

Independent Python extraction compared attachment line ranges against every group's JSON, combined JSON, positive/negative paste files, campaign-negative paste files, callouts, sitelinks, associations, snippets, URLs, paths, and original suffixes. **Zero fidelity differences.**

| Supplied group | Positives | Group negatives |
|---|---:|---:|
| Kjoler til mor og datter | 17 | 8 Phrase |
| Matchende familieantrekk | 20 | 8 Exact |
| Skjorter og T-skjorter til familien | 18 | 9 Exact |
| Pysjamas til mor og datter | 17 | 0 |
| Skjorter til far og sønn | 15 | 10 Phrase |
| Antrekk til mor og datter | 16 | 13 Exact |
| Badetøy til mor og datter | 18 | 0 |
| Gensere og hettegensere til familien | 23 | 6 Phrase |

Totals: **144 positives (62 Exact/82 Phrase); 233 campaign negatives (138 Norwegian Phrase, 84 English Phrase, 11 provisional Exact); all 54 group negatives (30 Exact/24 Phrase)**. English negatives are intentional attachment content. Zero normalized same-scope duplicates or literal positive/negative conflicts; this is not Microsoft semantic matching verification.

All 120 headlines and 32 descriptions fit the attachment's declared 30/90 limits. Observed maxima: headlines 30, descriptions 90, paths 13/8, sitelinks 25/34/32, callouts 25, snippet values 24. Eight sitelinks, 32 associations, six callouts, eight snippets match the attachment.

## Gates and reconciled findings

1. **Country/name unresolved:** request says `NB | NB`; attachment explicitly says United States/`US | NB` (lines 5–9, 41). Effective name, country, target ID and suffix remain null. Resolve once before creating the separate target. Corrected payload explicitly excludes Polish-owned 506256099; never reuse it.
2. **Parent-verified baseline:** USD 10/day, Maximize Clicks, USD 0.20 cap; requested source similarity governs paused-copy preparation. Eight-versus-seven difference is reconciled: copy seven source groups and add supplied mother/daughter outfits group. These are parent readbacks, not independent native verification here.
3. **All conditional negatives retained:** attachment lines 207/457 condition routing on recipient groups being active and suitable. Keep all 54 in paused review; verify destinations before launch. The 11 campaign Exact rows are provisional assortment restrictions (lines 831–847), not broad category exclusions.
4. **Images:** attachment references 160 caption pairs but supplies zero actual pairs/320 fields (lines 978–992). Payload correctly invents none. Preserve actual source pictures; translate source captions only after image/caption readback. Do not alter assets shared with existing campaigns.
5. **Copy:** Bokmål is understandable and coherent; “mamma og meg”/“look” are stylistic choices, not critical errors. No unsupported delivery guarantee, discount, UV protection, or local-stock claim found. Specific garments, patterns, and adult/child combinations still require landing/product evidence. Parent reports eight routes render products but untranslated labels/promo key remain; launch readiness is unproven.
6. **Tracking/native closeout:** source US suffixes are evidence only. Resolve geography and inherited tagging before applying localized suffixes or empty templates. Obtain settled native campaign/group exports and compare exact tuples, including inherited negatives and shared assets. Preserve Paused; no activation authority follows from this review.

Next action: root obtains the country/name decision, then performs the authorized separate paused build and native reconciliation. Canonical continuity remains root-owned; use `ops/prompts/paid-growth-ai-army-continuation-prompt.md` for continuation.
