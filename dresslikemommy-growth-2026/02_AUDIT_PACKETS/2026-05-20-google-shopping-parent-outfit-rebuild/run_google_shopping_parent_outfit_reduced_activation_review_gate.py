#!/usr/bin/env python3
"""Build the read-only reduced activation-review gate for parent-outfit Shopping.

This script performs no external reads or writes. It uses the latest local
read-only Merchant/feed gate output, the exact unresolved-offer exclusion CSV,
and the exact out-of-stock hold CSV to create a reduced review scope.
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PACKET_DIR = Path(__file__).resolve().parent
READY_LABEL = "us_parent_outfit_ready_v20260520"
SPEC_CSV = PACKET_DIR / "merchant_label_update_spec.csv"
UNRESOLVED_SCOPE_CSV = (
    PACKET_DIR / "google_shopping_parent_outfit_unresolved_offer_exclusion_scope_20260521T095911Z.csv"
)
OUT_OF_STOCK_HOLD_CSV = (
    PACKET_DIR / "google_shopping_parent_outfit_eligibility_out_of_stock_rows_20260521T095911Z.csv"
)


def utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def latest_ready_products_csv() -> Path:
    files = sorted(PACKET_DIR.glob("google_shopping_parent_outfit_ready_products_*.csv"))
    if not files:
        raise FileNotFoundError("No google_shopping_parent_outfit_ready_products_*.csv files found")
    return files[-1]


def gate_json_for_ready_csv(ready_csv: Path) -> Path:
    timestamp = ready_csv.stem.rsplit("_", 1)[-1]
    gate_path = PACKET_DIR / f"google_shopping_parent_outfit_merchant_feed_gate_{timestamp}.json"
    if not gate_path.exists():
        raise FileNotFoundError(f"Expected matching gate JSON not found: {gate_path}")
    return gate_path


def labels_match(spec_row: dict[str, str], live_row: dict[str, str]) -> bool:
    return all(
        live_row.get(f"custom_label_{index}", "") == spec_row.get(f"proposed_custom_label_{index}", "")
        for index in range(5)
    )


def build_report_markdown(payload: dict[str, Any], approval_packet_path: Path) -> str:
    candidate = payload["candidate_scope"]
    source = payload["source_counts"]
    safety = payload["safety_checks"]
    evidence = payload["evidence"]
    return f"""# Google Shopping Parent-Outfit Reduced Activation-Review Gate

Generated: `{payload['generated_at_utc']}`

Mode: read-only local evidence build. No Merchant, Shopify, Google & YouTube, Google Ads, campaign, product group, budget, bid, status, conversion, billing, feed, product-data, inventory, source reset, broad sync, activation, or unpause write occurred.

## Decision

Reduced read-only activation-review gate: `{'PASS' if payload['gate_passed'] else 'FAIL_CLOSED'}`

Reason: `{payload['reason']}`

## Source Inputs

- Latest local ready-products CSV: `{Path(evidence['ready_products_csv']).name}`
- Matching gate JSON: `{Path(evidence['gate_json']).name}`
- Exact unresolved-offer exclusion CSV: `{Path(evidence['unresolved_scope_csv']).name}`
- Exact out-of-stock hold CSV: `{Path(evidence['out_of_stock_hold_csv']).name}`
- Included Merchant spec rows: `{source['included_spec_rows']}`
- Latest ready-label rows: `{source['latest_ready_label_rows']}`
- Exact unresolved-offer exclusion rows held out: `{source['unresolved_scope_rows']}`
- Exact out-of-stock hold rows held out: `{source['out_of_stock_hold_rows']}`
- Unresolved rows that are now ready but still held out by exact scope: `{source['unresolved_rows_now_ready_but_held']}`

## Reduced Candidate Scope

- Candidate rows: `{candidate['rows']}`
- Candidate parent products: `{candidate['parent_products']}`
- Candidate rows by lane: `{candidate['rows_by_lane']}`
- Candidate parent products by lane: `{candidate['parent_products_by_lane']}`
- Candidate rows by subgroup: `{candidate['rows_by_subgroup']}`

## Safety Checks

- Candidate rows all in included spec: `{safety['candidate_all_in_spec']}`
- Candidate rows all in latest ready-label CSV: `{safety['candidate_all_ready']}`
- Candidate excludes all exact unresolved-offer rows: `{safety['candidate_excludes_unresolved_scope']}`
- Candidate excludes all exact out-of-stock hold rows: `{safety['candidate_excludes_out_of_stock_hold']}`
- Candidate labels match spec: `{safety['candidate_labels_match_spec']}`
- Candidate product images match proposed parent hero images: `{safety['candidate_images_match_spec']}`
- Candidate availability all `IN_STOCK`: `{safety['candidate_all_in_stock']}`
- Latest gate label mismatches: `{safety['latest_gate_label_mismatches']}`
- Latest gate image mismatches: `{safety['latest_gate_image_mismatches']}`
- Latest gate missing live images: `{safety['latest_gate_missing_live_images']}`
- V2 campaigns paused / status safe: `{safety['campaign_status_ok']}`
- Old test campaign paused: `{safety['old_campaign_paused']}`
- Bad catchall listing units: `{safety['bad_catchall_units']}`

## Approval Boundary

This gate does not authorize activation. It only proves a reduced review surface after holding out the exact `141` unresolved-offer rows and exact `20` out-of-stock rows.

Separate activation approval packet:

- `{approval_packet_path.name}`

## Recommended Next Action

Review the separate reduced-scope activation approval packet first. This is better than another upload/resync because the clean candidate rows already pass the local label/image/catchall/paused-safety checks while the held-out rows are isolated for a later repair lane.

## Evidence Outputs

- `{Path(evidence['json']).name}`
- `{Path(evidence['candidate_csv']).name}`
- `{Path(evidence['report_md']).name}`
"""


def build_activation_packet(payload: dict[str, Any]) -> str:
    candidate = payload["candidate_scope"]
    evidence = payload["evidence"]
    return f"""# Google Shopping Parent-Outfit Reduced-Scope Activation Approval Packet

Generated: `{payload['generated_at_utc']}`

Mode: approval packet only. No Shopping activation, unpause, budget, bid, status, product group, conversion, billing, Merchant feed/source, Google & YouTube sync, Shopify product/publication/inventory/title/price/handle/SEO, broad sync, source reset, or product-data write is authorized by this document.

## Reduced Scope Proven Read-Only

The reduced activation-review gate passed using:

- Exact `141` unresolved-offer exclusion scope: `google_shopping_parent_outfit_unresolved_offer_exclusion_scope_20260521T095911Z.csv`.
- Exact `20` out-of-stock hold: `google_shopping_parent_outfit_eligibility_out_of_stock_rows_20260521T095911Z.csv`.
- Latest local ready-label readback: `{Path(evidence['ready_products_csv']).name}`.

Reduced candidate counts:

- Candidate rows: `{candidate['rows']}`.
- Candidate parent products: `{candidate['parent_products']}`.
- Rows by lane: `{candidate['rows_by_lane']}`.
- Parent products by lane: `{candidate['parent_products_by_lane']}`.
- Rows by subgroup: `{candidate['rows_by_subgroup']}`.

The gate also confirmed:

- Candidate rows are included spec rows and latest ready-label rows.
- Candidate rows exclude all exact unresolved-offer rows and all exact out-of-stock hold rows.
- Candidate labels/images match the spec.
- Candidate rows are `IN_STOCK`.
- V2 Shopping campaigns and the old test campaign remain paused in the source gate.
- Bad catchall listing units remain `0`.

## Approval Phrase

If approved later, paste a fresh exact action-time approval phrase that names the allowed activation action and keeps every non-activation surface blocked. Do not infer approval from this packet.

Suggested phrase:

```text
Approve Google Shopping parent-outfit reduced-scope activation only: using the passed reduced activation-review gate {Path(evidence['report_md']).name}, activate only the already-built paused parent-outfit V2 Shopping campaign/ad-group/product-ad structures for the {candidate['rows']} candidate ready-label in-stock rows, keeping the exact 141 unresolved-offer rows and exact 20 out-of-stock rows held out. Do not change Merchant feeds/sources, trigger Google & YouTube sync, change Shopify products/publications/inventory/prices/titles/handles/SEO, change budgets, change bids, change conversion goals, change billing, broaden product scope, reset sources, or alter held-out rows. Capture before-state and after-state readbacks and stop immediately after activation readback.
```

## Still Not Approved

- Do not activate or unpause without fresh owner approval.
- Do not change budget, bid, product group, campaign structure, conversion, billing, Merchant source/feed, Shopify product data, Shopify inventory, publication, Google & YouTube sync, source reset, broad sync, or held-out scope.
- Do not include the `141` unresolved-offer rows or the `20` out-of-stock rows in an activation surface until a separate repair/readback proves them clean.

## Evidence

- `{Path(evidence['json']).name}`
- `{Path(evidence['candidate_csv']).name}`
- `{Path(evidence['report_md']).name}`
- `{Path(evidence['ready_products_csv']).name}`
- `{Path(evidence['gate_json']).name}`
"""


def main() -> int:
    generated_at = utc_stamp()
    ready_csv = latest_ready_products_csv()
    gate_json = gate_json_for_ready_csv(ready_csv)
    output_prefix = f"google_shopping_parent_outfit_reduced_activation_review_gate_{generated_at}"
    output_json = PACKET_DIR / f"{output_prefix}.json"
    candidate_csv = PACKET_DIR / f"google_shopping_parent_outfit_reduced_activation_review_candidates_{generated_at}.csv"
    report_md = PACKET_DIR / f"GOOGLE_SHOPPING_PARENT_OUTFIT_REDUCED_ACTIVATION_REVIEW_GATE_{generated_at}.md"
    activation_packet = PACKET_DIR / "GOOGLE_SHOPPING_PARENT_OUTFIT_REDUCED_SCOPE_ACTIVATION_APPROVAL_PACKET_20260521.md"

    spec_rows = [row for row in load_csv(SPEC_CSV) if row.get("decision") == "INCLUDE"]
    ready_rows = load_csv(ready_csv)
    unresolved_rows = load_csv(UNRESOLVED_SCOPE_CSV)
    out_of_stock_rows = load_csv(OUT_OF_STOCK_HOLD_CSV)
    gate = json.loads(gate_json.read_text(encoding="utf-8"))

    spec_by_id = {row["item_id"]: row for row in spec_rows}
    ready_by_id = {row["item_id"]: row for row in ready_rows}
    unresolved_ids = {row["item_id"] for row in unresolved_rows}
    out_of_stock_ids = {row["item_id"] for row in out_of_stock_rows}
    candidate_ids = sorted(set(spec_by_id) & set(ready_by_id) - unresolved_ids - out_of_stock_ids)

    candidate_rows: list[dict[str, Any]] = []
    label_mismatch_ids: list[str] = []
    image_mismatch_ids: list[str] = []
    not_in_stock_ids: list[str] = []
    for item_id in candidate_ids:
        spec = spec_by_id[item_id]
        live = ready_by_id[item_id]
        label_ok = labels_match(spec, live)
        image_ok = live.get("product_image_uri", "") == spec.get("proposed_image_link", "")
        in_stock = live.get("availability") == "IN_STOCK"
        if not label_ok:
            label_mismatch_ids.append(item_id)
        if not image_ok:
            image_mismatch_ids.append(item_id)
        if not in_stock:
            not_in_stock_ids.append(item_id)
        candidate_rows.append(
            {
                "item_id": item_id,
                "parent_product_id": spec.get("parent_product_id", ""),
                "handle": spec.get("handle", ""),
                "lane": spec.get("proposed_custom_label_1", ""),
                "subgroup": spec.get("proposed_custom_label_2", ""),
                "variant_title": spec.get("variant_title", ""),
                "status": live.get("status", ""),
                "availability": live.get("availability", ""),
                "custom_label_0": live.get("custom_label_0", ""),
                "custom_label_1": live.get("custom_label_1", ""),
                "custom_label_2": live.get("custom_label_2", ""),
                "custom_label_3": live.get("custom_label_3", ""),
                "custom_label_4": live.get("custom_label_4", ""),
                "product_image_uri": live.get("product_image_uri", ""),
                "labels_match_spec": str(label_ok).lower(),
                "image_matches_spec": str(image_ok).lower(),
            }
        )

    candidate_parent_ids = {row["parent_product_id"] for row in candidate_rows}
    rows_by_lane = Counter(row["lane"] for row in candidate_rows)
    rows_by_subgroup = Counter(row["subgroup"] for row in candidate_rows)
    parent_products_by_lane: dict[str, int] = {}
    for lane in sorted(rows_by_lane):
        parent_products_by_lane[lane] = len(
            {row["parent_product_id"] for row in candidate_rows if row["lane"] == lane}
        )

    live_ready = gate.get("live_ready_products", {})
    listing_groups = gate.get("listing_group_summary", {})
    source_counts = {
        "included_spec_rows": len(spec_rows),
        "latest_ready_label_rows": len(ready_rows),
        "unresolved_scope_rows": len(unresolved_rows),
        "out_of_stock_hold_rows": len(out_of_stock_rows),
        "unresolved_rows_now_ready_but_held": len(unresolved_ids & set(ready_by_id)),
        "out_of_stock_rows_in_latest_ready": len(out_of_stock_ids & set(ready_by_id)),
    }
    safety_checks = {
        "candidate_all_in_spec": all(item_id in spec_by_id for item_id in candidate_ids),
        "candidate_all_ready": all(item_id in ready_by_id for item_id in candidate_ids),
        "candidate_excludes_unresolved_scope": not (set(candidate_ids) & unresolved_ids),
        "candidate_excludes_out_of_stock_hold": not (set(candidate_ids) & out_of_stock_ids),
        "candidate_labels_match_spec": not label_mismatch_ids,
        "candidate_images_match_spec": not image_mismatch_ids,
        "candidate_all_in_stock": not not_in_stock_ids,
        "latest_gate_label_mismatches": live_ready.get("label_mismatches"),
        "latest_gate_image_mismatches": live_ready.get("image_mismatches"),
        "latest_gate_missing_live_images": live_ready.get("missing_live_images"),
        "campaign_status_ok": gate.get("campaign_status_ok"),
        "old_campaign_paused": gate.get("old_campaign_paused"),
        "bad_catchall_units": listing_groups.get("bad_catchall_units"),
    }
    gate_passed = all(
        [
            safety_checks["candidate_all_in_spec"],
            safety_checks["candidate_all_ready"],
            safety_checks["candidate_excludes_unresolved_scope"],
            safety_checks["candidate_excludes_out_of_stock_hold"],
            safety_checks["candidate_labels_match_spec"],
            safety_checks["candidate_images_match_spec"],
            safety_checks["candidate_all_in_stock"],
            safety_checks["latest_gate_label_mismatches"] == 0,
            safety_checks["latest_gate_image_mismatches"] == 0,
            safety_checks["latest_gate_missing_live_images"] == 0,
            safety_checks["campaign_status_ok"] is True,
            safety_checks["old_campaign_paused"] is True,
            safety_checks["bad_catchall_units"] == 0,
        ]
    )

    payload: dict[str, Any] = {
        "generated_at_utc": generated_at,
        "gate_passed": gate_passed,
        "reason": "REDUCED_READ_ONLY_ACTIVATION_REVIEW_SCOPE_CLEAN"
        if gate_passed
        else "FAIL_CLOSED__REDUCED_READ_ONLY_ACTIVATION_REVIEW_SCOPE_NOT_CLEAN",
        "source_counts": source_counts,
        "candidate_scope": {
            "rows": len(candidate_rows),
            "parent_products": len(candidate_parent_ids),
            "rows_by_lane": dict(sorted(rows_by_lane.items())),
            "parent_products_by_lane": dict(sorted(parent_products_by_lane.items())),
            "rows_by_subgroup": dict(sorted(rows_by_subgroup.items())),
        },
        "held_scope": {
            "unresolved_offer_exclusion_rows": len(unresolved_rows),
            "out_of_stock_hold_rows": len(out_of_stock_rows),
            "unresolved_rows_now_ready_but_still_held": sorted(unresolved_ids & set(ready_by_id)),
        },
        "safety_checks": safety_checks,
        "samples": {
            "label_mismatch_ids": label_mismatch_ids[:20],
            "image_mismatch_ids": image_mismatch_ids[:20],
            "not_in_stock_ids": not_in_stock_ids[:20],
        },
        "evidence": {
            "json": str(output_json.relative_to(PACKET_DIR)),
            "candidate_csv": str(candidate_csv.relative_to(PACKET_DIR)),
            "report_md": str(report_md.relative_to(PACKET_DIR)),
            "ready_products_csv": str(ready_csv.relative_to(PACKET_DIR)),
            "gate_json": str(gate_json.relative_to(PACKET_DIR)),
            "unresolved_scope_csv": str(UNRESOLVED_SCOPE_CSV.relative_to(PACKET_DIR)),
            "out_of_stock_hold_csv": str(OUT_OF_STOCK_HOLD_CSV.relative_to(PACKET_DIR)),
        },
        "guardrails": [
            "No external reads or writes.",
            "No Shopping activation or unpause.",
            "No Merchant feed/source change.",
            "No Shopify product/publication/inventory/product-data change.",
            "No Google Ads campaign/product-group/budget/bid/status/conversion/billing change.",
            "No broad sync or source reset.",
        ],
    }

    write_csv(
        candidate_csv,
        candidate_rows,
        [
            "item_id",
            "parent_product_id",
            "handle",
            "lane",
            "subgroup",
            "variant_title",
            "status",
            "availability",
            "custom_label_0",
            "custom_label_1",
            "custom_label_2",
            "custom_label_3",
            "custom_label_4",
            "product_image_uri",
            "labels_match_spec",
            "image_matches_spec",
        ],
    )
    write_json(output_json, payload)
    report_md.write_text(build_report_markdown(payload, activation_packet), encoding="utf-8")
    if gate_passed:
        activation_packet.write_text(build_activation_packet(payload), encoding="utf-8")

    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if gate_passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
