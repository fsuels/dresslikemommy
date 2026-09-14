# Dress Like Mommy Google Ads API Tool Design Document

Prepared for: Google Ads API Basic Access application

Company: Dress Like Mommy

Website: https://dresslikemommy.com

Manager account: 700-107-9966

## 1. Tool Overview

Dress Like Mommy uses an internal Google Ads API workflow for read-only ecommerce advertising analysis. The tool is used to support Search keyword research, Keyword Planner forecast validation, campaign reporting, and ROAS decision support for the company's own Shopify store.

The tool is not a public product, agency platform, marketplace, or client-facing dashboard. It is an internal operator workflow used only for Dress Like Mommy's own Google Ads account.

## 2. Business Context

Dress Like Mommy is a direct-to-consumer Shopify ecommerce apparel business. Product categories include mommy-and-me dresses, mother-daughter matching outfits, family matching outfits, pajamas, beach and swim looks, wedding guest dresses, daddy-and-me shirts, and family vacation outfits.

Google Ads is used to acquire profitable online purchases. The business optimizes toward purchase revenue/subtotal, excluding shipping and tax, with purchase as the primary conversion.

## 3. Users And Access

Access is limited to internal operators and approved contractors working on Dress Like Mommy advertising operations. There are no external users, no public sign-in, and no client-facing access.

The tool uses local secure credentials controlled by the owner/operator. API credentials are stored outside the repository and are not embedded in code, logs, reports, or uploaded artifacts.

## 4. Google Ads API Capabilities Requested

The requested capabilities are:

- Reporting
- Keyword Planning Services

The immediate need is KeywordPlanIdeaService access for:

- GenerateKeywordHistoricalMetrics
- GenerateKeywordForecastMetrics

These methods are required to validate long-tail Search keyword candidates using the correct target geography, English language, Google Search network, exact or phrase match, and explicit max CPC bids.

## 5. Data Read And Data Written

The tool reads:

- Keyword Planner historical metrics
- Keyword forecast metrics
- Campaign and reporting data used for ROAS analysis

The tool writes only local operator evidence files, such as CSV, JSON, and Markdown reports. It does not write Google Ads campaign changes.

The tool does not:

- Create Google Ads accounts
- Change billing
- Create, upload, enable, pause, or remove campaigns
- Change budgets, bids, statuses, assets, audiences, feeds, or conversion goals
- Send customer PII to local reports
- Expose Google Ads data to external users

## 6. Workflow

1. An operator prepares a keyword table with ad group, keyword, match type, market, language, network, and CPC gate.
2. The script loads Google Ads credentials from the secure local configuration path.
3. The script calls KeywordPlanIdeaService for historical and forecast metrics.
4. The script writes local CSV and JSON evidence in an audit packet.
5. A human reviews the outputs before any campaign build, upload, or serving change.

All live campaign changes remain outside this tool and require a separate explicit approval process.

## 7. Controls And Safeguards

The tool is intentionally read-only for Google Ads. It has a narrow scope and contains guardrails in code and operator instructions:

- Read-only API services are used for the current workflow.
- Output files are local only.
- Credentials are stored outside the repository.
- Secrets are never printed or written into tracked artifacts.
- Campaign mutations require a separate approval workflow and are not part of this API access request.
- The tool records assumptions, request parameters, and blockers so the owner can audit decisions before action.

## 8. Current Example Use Case

Dress Like Mommy needs to evaluate 29 long-tail Search keywords for 2026 launch planning. The requested validation uses:

- Geography: United States
- Language: English
- Network: Google Search
- Match types: exact and phrase
- Max CPC bid: 200,000 micros ($0.20)

Explorer Access currently blocks KeywordPlanIdeaService methods, so Basic Access is required to complete the forecast and historical metrics export.

## 9. Data Retention

Generated reports are retained locally in the Dress Like Mommy operator repository as audit evidence. They contain keyword planning and aggregate performance metrics only. They do not contain customer-level PII, payment data, OAuth secrets, refresh tokens, API keys, or developer tokens.

## 10. Summary

This is an internal, read-only ecommerce advertising analysis tool for one advertiser. Basic Access is requested so Dress Like Mommy can use Keyword Planning Services and reporting against its own production Google Ads account with a reviewed, documented workflow.
