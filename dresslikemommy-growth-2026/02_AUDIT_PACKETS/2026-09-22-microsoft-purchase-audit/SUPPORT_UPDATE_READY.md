# Ready-to-send update for Microsoft case 7108824779

Status: SENT_IN_LIVE_CHAT on September 22, 2026, at 10:42–10:43 AM EDT after explicit user authorization. The approved body below was sent in six numbered parts because of the 500-character chat limit. Recipient: Microsoft Advertising Support, existing case 7108824779. Case-attachment acknowledgment is tracked in [SUPPORT_SEND_RECEIPT.md](SUPPORT_SEND_RECEIPT.md). Purpose: obtain a supported publisher correction and receiver diagnostics. No customer details, raw click IDs, credentials or attachments. No authority to change campaigns, pixels, privacy settings or account configuration.

Hello, please update existing case 7108824779 for Microsoft Advertising account 477439 and ShopifyImport UET tag 36005151.

Our September 22 audit confirms all nine current campaigns use the same primary purchase goal, ShopifyCheckoutCompleteEventTracking. It matches action=purchase, uses variable revenue, counts All, and has a 30-day click window. MSCLKID and UTM auto-tagging are enabled. For September 19–22, UET receives two purchase events, while campaign reporting shows zero attributed purchases and revenue. We are not claiming that those events should necessarily receive ad credit.

The installed Microsoft Shopify app pixel 931561569 remains version 5ee93563fe31b11d2d65e2f09a5229dc. Its cookie-setting call still supplies expiry text as part of the msclkid cookie-name argument. A separate 90-day localStorage fallback exists, so actual click-ID loss has not been proved. Please confirm whether engineering has accepted the code defect and provide the supported correction and expected release time.

UET also reports missing consent signals for checkout/product/cart events in its EEA/UK/Switzerland sample. The purchase Healthy tooltip says no regional sample. Please identify the supported consent implementation for both the storefront tag and the Shopify app pixel.

Finally, please provide a supported method to verify an individual genuine purchase's value, currency, product details, single delivery and legitimate click attribution. The installed app sends checkout subtotal and its currency; the current UI exposes parameter names but no actual purchase values or order identity. Please confirm the intended revenue definition and duplicate handling.

What is the current investigation status, correction plan, and next update time? Please keep this on the existing case. This message authorizes no account, campaign, app, consent or tracking changes.
