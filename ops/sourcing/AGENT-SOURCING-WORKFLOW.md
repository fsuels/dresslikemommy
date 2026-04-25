# Dress Like Mommy Sourcing Workflow

Use this when the goal is to find new 1688 products for the store before Shopify listing work.

## Mental Model

The workflow is:

1. Search 1688 through a logged-in browser session.
2. Collect visible product cards into `candidates.json`.
3. Score candidates into `Gold`, `Test`, or `Reject`.
4. Review candidates in the local sourcing dashboard.
5. Persist operator decisions in `ops/sourcing/state/decisions.json`.
6. Open kept products and verify detail-page evidence.
7. Save proof in the dashboard: size chart, vendor image path, generated image path, dropship support, dispatch speed, supplier proof, and notes.
8. Create a draft package.
9. Run the draft-agent prompt to create a Shopify DRAFT product with images.
10. Review the Shopify draft, then publish only when the operator asks.

## Store Categories

Configured in `ops/sourcing/sourcing-categories.json`:

- `mommy-and-me`
- `daddy-and-me`
- `family-matching`
- `couples`
- `maternity`

Each category has its own listing mode and 1688 search queries. Future runs should write `run.json` with a `category_id` so the dashboard can group candidates correctly.

## Launch The App

Preferred:

```text
/Users/fsuels/Applications/Dress Like Mommy Sourcing.app
```

Backup double-click launcher:

```text
ops/sourcing/Open Dress Like Mommy Sourcing.command
```

Manual command:

```bash
python3 ops/scripts/1688_sourcing_dashboard.py --open
```

Dashboard URL:

```text
http://127.0.0.1:8766/
```

## Plain-Language Dashboard Labels

- `Stored Cards`: all raw 1688 cards saved locally across runs.
- `Buyer Shortlist`: fresh, category-fit leads that are worth opening first.
- `Saved`: products the operator chose with Save/Keep.
- `Ready for Draft`: saved products with required proof fields filled in.
- `Rejected`: remembered rejects that should not be researched again unless restored.
- `Best Leads`: internal `Gold` verdict.
- `Unverified Leads`: internal `Test` verdict; promising, but missing supplier/detail-page proof.

The dashboard has a `Find Qualified Leads` button. It first checks the helper Chrome tab through `/api/browser-status`; if 1688 is showing login, CAPTCHA, `Captcha Interception`, `_____tmd_____`, or a punish URL, the dashboard must show that blocker and avoid creating a fake empty run. Once the browser is clear, it starts the CDP collector from the browser UI, rotates configured category keywords, skips already-seen offer IDs, and stops once it has at least 3 `Gold`/`Test` candidates. If 1688 requires login or CAPTCHA, use `Open 1688 Login/Search`, let the user complete that browser step, then click `Find Qualified Leads` again.

`Open 1688 Login/Search` should reuse one helper tab through CDP when possible. Do not create many repeated 1688 search tabs.

Freshness rules:

- In 2026, visible 2020-2024 year signals should be rejected for the active sourcing queue.
- A search-stage product should need visible 2025/2026 or Chinese new-style evidence before it becomes `Test` / `Unverified Leads`.
- A search-stage product should also need a newer 1688 offer ID. Current `MIN_FRESH_OFFER_ID` is `850000000000`, because old 1688 products can be edited with a fresh-looking title.
- If search-card sales have no stated time window, treat them as a popularity clue only and confirm sales/availability on the detail page.
- If 1688 redirects to `Captcha Interception` or a `_____tmd_____` punish URL, stop and recover the browser session; do not treat zero cards as a successful search.

## Fill A Category With Fresh Candidates

Preferred: use `Find Qualified Leads` inside the dashboard.

Manual fallback: use a logged-in Chrome/1688 session. The current browser-assisted collector expects Chrome DevTools Protocol on port `9333`.

One category:

```bash
python3 ops/scripts/1688_sourcing_cdp_collect.py --category family-matching --limit 24
```

Tuned target mode:

```bash
python3 ops/scripts/1688_sourcing_cdp_collect.py --category mommy-and-me --limit 48 --query-index -1 --target-reviewable 3
```

All categories:

```bash
python3 ops/scripts/1688_sourcing_cdp_collect.py --category all --limit 24
```

If the CDP collector cannot attach or 1688 asks for CAPTCHA/login, do not bypass it. Use the browser manually, run `ops/sourcing/1688-browser-collector.js` in the console, save `candidates.json`, and run the scorecard.

## Search History

Persistent search memory lives here:

```text
ops/sourcing/state/search-history.json
```

The collector uses this file to rotate the next starting query, record blocked CAPTCHA/login events, and avoid collecting offer IDs already saved in prior runs. Repeated dashboard clicks should therefore try a different starting query instead of collecting the same first-page products again.

## Reject Memory

Persistent decisions live here:

```text
ops/sourcing/state/decisions.json
```

When a product is rejected, its 1688 offer ID is saved. Future scoring runs can use:

```bash
python3 ops/scripts/1688_sourcing_score.py \
  --input ops/sourcing/<run>/candidates.json \
  --output-dir ops/sourcing/<run> \
  --stage search \
  --decision-state ops/sourcing/state/decisions.json
```

Previously rejected offers are forced to `Reject` with the concern `previously rejected by operator`.

## Detail-Page Enrichment Gate

Search results can only create `Unverified Leads`. A product should become `Best Lead` / internal `Gold` only after detail-page proof is collected.

Use the detail enricher for a specific shortlisted offer:

```bash
python3 ops/scripts/1688_sourcing_detail_enrich.py --key <1688-offer-id>
```

The detail enricher:

- opens the normal 1688 product page through the logged-in Chrome helper on CDP port `9333`
- stops if 1688 shows login, CAPTCHA, interception, or a punish page
- extracts supplier name/URL, badges, years/rating when visible, dropship terms, dispatch/stock text, size-chart text, availability, IP-risk text, sales/repeat clues, and product images
- downloads vendor images to `ops/sourcing/vendor-images/<1688-offer-id>/`
- writes detail artifacts to `ops/sourcing/detail-enrichment/<1688-offer-id>/`
- rescored the product with `--stage detail`
- updates proof fields in `ops/sourcing/state/decisions.json`
- updates supplier memory in `ops/sourcing/state/vendors.json` when supplier identity is captured

Gold is blocked when critical detail proof is missing. Missing supplier proof, missing size chart, missing dropship/one-piece proof, missing dispatch/ready-stock proof, or missing usable vendor images should keep the product as `Test` or `Reject`.

## Dashboard Buttons

- `Keep`: promising product to inspect on the detail page.
- `Reject`: persistent memory. The product is hidden from active review and should not be researched again unless restored.
- `Restore`: clears a rejected decision.
- `Open 1688`: opens the vendor product page.
- `Verify Detail Proof`: opens the 1688 detail page through the helper browser and runs the detail enrichment gate.
- `Copy Listing Prompt`: copies the fully filled canonical listing request wrapper.
- `Copy Photo Prompt`: copies the 6-image photoshoot prompt. Upload vendor images before using it.
- `Save Proof`: stores the detail-page evidence you checked.
- `Draft Package`: writes a local package with `candidate.json`, `listing-request.txt`, `photoshoot-prompt.md`, and `draft-agent-prompt.md`. The dashboard blocks this button until required proof fields are filled.
- `Copy search command`: copies the collector command for the active category.

## Draft Package Gate

The dashboard only marks a product `Ready` when these fields are filled:

- size chart source
- vendor images path
- generated images path
- dropship confirmation
- dispatch confirmation
- supplier confirmation

Draft packages are written under:

```text
ops/sourcing/draft-packages/<1688-offer-id>/
```

Use `draft-agent-prompt.md` from that folder to create the Shopify draft. The prompt explicitly says to create a DRAFT product only and not publish live.

## New Session Prompt

Use this in a new agent session:

```text
You are working in /Users/fsuels/Projects/dresslikemommy.
Read AGENTS.md and ops/AGENT_WORKLOG.md first.
Then read ops/sourcing/AGENT-SOURCING-WORKFLOW.md.
Open the Dress Like Mommy sourcing dashboard and help me keep each category full of vetted 1688 candidates.
Use logged-in browser-assisted workflows only; do not bypass CAPTCHA.
Respect ops/sourcing/state/decisions.json so rejected 1688 offers are not researched again.
If I choose a product, help me verify detail-page evidence, then copy/use the listing prompt and photoshoot prompt from the dashboard.
When proof is complete, create a draft package and use its draft-agent-prompt.md to create a Shopify DRAFT product with images. Do not publish live unless I explicitly ask.
```

## Listing And Image Handoff

For listing work, the copied prompt includes the canonical instruction to read:

1. `ops/prompts/START-HERE.md`
2. `ops/prompts/shopify-listing-master-prompt.md`
3. `ops/prompts/shopify-listing-from-1688.md`

For images, the copied photoshoot prompt comes from:

```text
ops/prompts/dlm-6-image-photoshoot.md
```

The image prompt starts at IMAGE 1 and waits for `NEXT` between images.
