#!/usr/bin/env python3
"""Fill Shopify structured apparel metafields from the audited top revenue candidates.

Default mode is dry-run. Live updates are intentionally limited to the rows in
`high_confidence_attribute_fill_candidates_top20_by_revenue.csv`, and each
attribute is written independently only when:

1. The product-level Shopify field is still blank in live data.
2. The audit confidence for that field is `high`.
3. Every candidate value maps deterministically to a valid Shopify metaobject.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib import error, request

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ops.scripts.shopify_admin_config import load_access_token, resolve_store_domain  # noqa: E402


API_VERSION = "2026-01"
TIMEOUT_SECONDS = 120
DEFAULT_INPUT_CSV = Path(
    "ops/feed-engineering/2026-03-29-phase-3e-apparel-attribute-audit/high_confidence_attribute_fill_candidates_top20_by_revenue.csv"
)
DEFAULT_OUTPUT_DIR = Path("ops/feed-engineering/2026-03-29-phase-3f-apparel-attribute-fill")
SUPPORTED_FIELDS = ("gender", "age_group", "size", "color")
CONFIDENCE_RANK = {"low": 1, "medium": 2, "high": 3}

PRODUCT_QUERY = """
query Product($handle: String!) {
  productByHandle(handle: $handle) {
    id
    legacyResourceId
    handle
    title
    gender: metafield(namespace: "shopify", key: "target-gender") {
      id
      type
      value
      references(first: 20) {
        nodes {
          ... on Metaobject {
            id
            handle
            displayName
          }
        }
      }
    }
    age_group: metafield(namespace: "shopify", key: "age-group") {
      id
      type
      value
      references(first: 20) {
        nodes {
          ... on Metaobject {
            id
            handle
            displayName
          }
        }
      }
    }
    size: metafield(namespace: "shopify", key: "size") {
      id
      type
      value
      references(first: 50) {
        nodes {
          ... on Metaobject {
            id
            handle
            displayName
          }
        }
      }
    }
    color: metafield(namespace: "shopify", key: "color-pattern") {
      id
      type
      value
      references(first: 30) {
        nodes {
          ... on Metaobject {
            id
            handle
            displayName
          }
        }
      }
    }
  }
}
"""

METAOBJECTS_QUERY = """
query Metaobjects($type: String!, $first: Int!, $after: String) {
  metaobjects(type: $type, first: $first, after: $after) {
    pageInfo {
      hasNextPage
      endCursor
    }
    nodes {
      id
      type
      handle
      displayName
      fields {
        key
        value
      }
    }
  }
}
"""

METAFIELDS_SET_MUTATION = """
mutation SetMetafields($metafields: [MetafieldsSetInput!]!) {
  metafieldsSet(metafields: $metafields) {
    metafields {
      id
      namespace
      key
      value
    }
    userErrors {
      field
      message
      code
    }
  }
}
"""


@dataclass
class CandidateRow:
    revenue_rank: int
    product_id: str
    handle: str
    title: str
    missing_attributes: list[str]
    candidate_value: dict[str, str]
    candidate_confidence: dict[str, str]
    candidate_source: dict[str, str]


@dataclass
class MetaobjectRef:
    id: str
    handle: str
    display_name: str


@dataclass
class ProductState:
    product_gid: str
    product_id: str
    handle: str
    title: str
    current_refs: dict[str, list[MetaobjectRef]]
    current_raw: dict[str, str]


@dataclass
class PlannedChange:
    product_id: str
    product_gid: str
    handle: str
    title: str
    field: str
    current_value: str
    current_reference_labels: str
    candidate_value: str
    candidate_confidence: str
    candidate_source: str
    normalized_labels: str
    reference_ids: str
    reference_labels: str
    status: str
    reason: str


class ShopifyClient:
    def __init__(self, store_domain: str, access_token: str) -> None:
        self.endpoint = f"https://{store_domain}/admin/api/{API_VERSION}/graphql.json"
        self.access_token = access_token

    def graphql(self, query: str, variables: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = json.dumps({"query": query, "variables": variables or {}}).encode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": self.access_token,
        }
        for attempt in range(6):
            req = request.Request(self.endpoint, data=payload, method="POST", headers=headers)
            try:
                with request.urlopen(req, timeout=TIMEOUT_SECONDS) as response:
                    body = json.loads(response.read().decode("utf-8"))
            except error.HTTPError as exc:
                body = exc.read().decode("utf-8", errors="replace")
                if exc.code in {429, 500, 502, 503, 504} and attempt < 5:
                    time.sleep(2**attempt)
                    continue
                raise RuntimeError(f"Shopify GraphQL HTTP {exc.code}: {body}") from exc

            if body.get("errors"):
                raise RuntimeError(f"Shopify GraphQL errors: {body['errors']}")
            return body["data"]
        raise RuntimeError("Shopify GraphQL request failed after retries.")

    def fetch_product_state(self, handle: str) -> ProductState:
        data = self.graphql(PRODUCT_QUERY, {"handle": handle})["productByHandle"]
        if not data:
            raise RuntimeError(f"Product not found for handle `{handle}`.")

        current_refs: dict[str, list[MetaobjectRef]] = {}
        current_raw: dict[str, str] = {}
        for field in SUPPORTED_FIELDS:
            metafield = data.get(field)
            current_raw[field] = clean((metafield or {}).get("value"))
            refs = []
            for node in ((metafield or {}).get("references") or {}).get("nodes") or []:
                refs.append(
                    MetaobjectRef(
                        id=clean(node.get("id")),
                        handle=clean(node.get("handle")),
                        display_name=clean(node.get("displayName")),
                    )
                )
            current_refs[field] = refs

        return ProductState(
            product_gid=clean(data.get("id")),
            product_id=clean(data.get("legacyResourceId")),
            handle=clean(data.get("handle")),
            title=clean(data.get("title")),
            current_refs=current_refs,
            current_raw=current_raw,
        )

    def fetch_metaobjects(self, object_type: str) -> list[MetaobjectRef]:
        refs: list[MetaobjectRef] = []
        after: str | None = None
        while True:
            data = self.graphql(METAOBJECTS_QUERY, {"type": object_type, "first": 100, "after": after})["metaobjects"]
            for node in data["nodes"]:
                refs.append(
                    MetaobjectRef(
                        id=clean(node.get("id")),
                        handle=clean(node.get("handle")),
                        display_name=clean(node.get("displayName")),
                    )
                )
            if not data["pageInfo"]["hasNextPage"]:
                break
            after = data["pageInfo"]["endCursor"]
        return refs

    def set_metafield_references(
        self,
        *,
        product_gid: str,
        key: str,
        reference_ids: list[str],
    ) -> list[str]:
        metafields = [
            {
                "ownerId": product_gid,
                "namespace": "shopify",
                "key": key,
                "type": "list.metaobject_reference",
                "value": json.dumps(reference_ids),
            }
        ]
        data = self.graphql(METAFIELDS_SET_MUTATION, {"metafields": metafields})["metafieldsSet"]
        errors = []
        for item in data.get("userErrors") or []:
            parts = item.get("field") or []
            prefix = " / ".join(parts)
            if prefix:
                errors.append(f"{prefix}: {item.get('message', '')}")
            else:
                errors.append(item.get("message", "Unknown error"))
        return errors


def clean(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip())


def normalize_text(value: str) -> str:
    return clean(value).lower()


def split_pipe(value: str) -> list[str]:
    return [clean(part) for part in value.split("|") if clean(part)]


def split_csv(value: str) -> list[str]:
    return [clean(part) for part in value.split(",") if clean(part)]


def metafield_present(raw_value: str, refs: list[MetaobjectRef]) -> bool:
    return bool(refs or (clean(raw_value) and clean(raw_value) != "[]"))


def confidence_meets_threshold(confidence: str, threshold: str) -> bool:
    return CONFIDENCE_RANK.get(normalize_text(confidence), 0) >= CONFIDENCE_RANK.get(normalize_text(threshold), 0)


def uniq_preserve(values: list[str]) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []
    for value in values:
        key = normalize_text(value)
        if not key or key in seen:
            continue
        seen.add(key)
        output.append(clean(value))
    return output


def load_candidates(path: Path) -> list[CandidateRow]:
    rows: list[CandidateRow] = []
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            rows.append(
                CandidateRow(
                    revenue_rank=int(row["revenue_rank"]),
                    product_id=clean(row["product_id"]),
                    handle=clean(row["handle"]),
                    title=clean(row["title"]),
                    missing_attributes=split_pipe(row["missing_attributes"]),
                    candidate_value={field: clean(row[f"candidate_{field}"]) for field in SUPPORTED_FIELDS},
                    candidate_confidence={field: clean(row[f"candidate_{field}_confidence"]) for field in SUPPORTED_FIELDS},
                    candidate_source={field: clean(row[f"candidate_{field}_source"]) for field in SUPPORTED_FIELDS},
                )
            )
    return rows


def build_metaobject_index(refs: list[MetaobjectRef]) -> dict[str, MetaobjectRef]:
    indexed: dict[str, MetaobjectRef] = {}
    for ref in refs:
        if ref.handle and ref.handle not in indexed:
            indexed[ref.handle] = ref
        display_key = normalize_text(ref.display_name)
        if display_key and display_key not in indexed:
            indexed[display_key] = ref
    return indexed


def choose_preferred_reference(refs: list[MetaobjectRef], *, preferred_handle: str | None = None, display_name: str | None = None) -> MetaobjectRef | None:
    if preferred_handle:
        for ref in refs:
            if ref.handle == preferred_handle:
                return ref
    if display_name:
        target = normalize_text(display_name)
        for ref in refs:
            if normalize_text(ref.display_name) == target:
                return ref
    return refs[0] if refs else None


def normalize_gender_values(raw_value: str) -> tuple[list[str], list[str]]:
    token = normalize_text(raw_value)
    mapping = {"female": "female", "male": "male", "unisex": "unisex"}
    if token in mapping:
        return [mapping[token]], []
    return [], [raw_value]


def normalize_age_group_values(raw_value: str) -> tuple[list[str], list[str]]:
    values: list[str] = []
    unresolved: list[str] = []
    mapping = {
        "adult": "Adults",
        "kids": "Kids",
        "toddler": "Toddlers",
        "infant": "Babies",
    }
    for token in split_pipe(raw_value):
        key = normalize_text(token)
        label = mapping.get(key)
        if label:
            values.append(label)
        else:
            unresolved.append(token)
    return uniq_preserve(values), unresolved


def canonicalize_size_token(raw_value: str) -> str:
    text = normalize_text(raw_value)
    text = re.sub(r"\([^)]*\)", " ", text)
    text = re.sub(r"\b(baby girl|baby boy)\b", " ", text)
    text = re.sub(r"\b(mother|father|mom|dad|adult|women|woman|men|man|girl|boy|child|baby)\b", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"\byears old\b", "years", text)
    text = re.sub(r"\byear old\b", "year", text)
    text = re.sub(r"\byrs\b", "years", text)
    text = re.sub(r"\byr\b", "year", text)
    text = re.sub(r"\bmos\b", "months", text)
    text = re.sub(r"\bmo\b", "months", text)
    text = re.sub(r"\bmonth\b", "months", text)
    text = text.replace("xxxl", "3xl")
    text = text.replace("xxl", "2xl")
    leading_alpha = re.match(r"^(xxs|xs|s|m|l|xl|2xl|3xl|4xl|5xl)\b", text)
    if leading_alpha:
        text = leading_alpha.group(1)
    if re.fullmatch(r"(xs|s|m|l|xl|2xl|3xl|4xl|5xl)", text):
        return text.upper().replace("2XL", "2XL").replace("3XL", "3XL").replace("4XL", "4XL").replace("5XL", "5XL")
    return clean(text)


def map_single_size_value(raw_value: str, refs: list[MetaobjectRef]) -> tuple[str, MetaobjectRef | None, str]:
    exact_index = build_metaobject_index(refs)
    token = canonicalize_size_token(raw_value)
    normalized = normalize_text(token)

    exact_candidates = {
        "s": "S",
        "m": "M",
        "l": "L",
        "xl": "XL",
        "2xl": "2XL",
        "3xl": "3XL",
        "4xl": "4XL",
        "0-3 months": "0-3 months",
        "3-6 months": "3-6 months",
        "3 months": "0-3 months",
        "6-9 months": "6-9 months",
        "6 months": "6-9 months",
        "9-12 months": "9-12 months",
        "9 months": "9-12 months",
        "12-18 months": "12-18 months",
        "12 months": "12-18 months",
        "1": "1",
        "1 year": "1",
        "1 years": "1",
        "1-2 years": "1-2 years",
        "90cm": "2-3 years",
        "2 years": "2-3 years",
        "2-3 years": "2-3 years",
        "100cm": "3-4 years",
        "3 years": "3-4 years",
        "3-4 years": "3-4 years",
        "110cm": "4-5 years",
        "4 years": "4-5 years",
        "4-5 years": "4-5 years",
        "120cm": "5-6 years",
        "5 years": "5-6 years",
        "5-6 years": "5-6 years",
        "130cm": "6-7 years",
        "6": "6",
        "6 years": "6",
        "6-7 years": "6-7 years",
        "140cm": "7-8 years",
        "7-8 years": "7-8 years",
        "150cm": "10",
        "8": "8",
        "8 years": "8",
        "8-9 years": "8-9 years",
        "160cm": "12",
        "10": "10",
        "10 years": "10",
        "12": "12",
        "12 years": "12",
    }
    if normalized in exact_candidates:
        label = exact_candidates[normalized]
        ref = choose_preferred_reference(refs, preferred_handle=normalize_text(label).replace(" ", "-"), display_name=label)
        return label, ref, "" if ref else f"no_metaobject_for:{label}"

    compact = re.sub(r"\s+", "", normalized)
    compact_matches = {
        "2t": "2-3 years",
        "3t": "3-4 years",
        "4t": "4-5 years",
        "6t": "6",
        "8t": "8",
        "10t": "10",
    }
    if compact in compact_matches:
        label = compact_matches[compact]
        ref = choose_preferred_reference(refs, preferred_handle=label.replace(" ", "-"), display_name=label)
        return label, ref, "" if ref else f"no_metaobject_for:{label}"

    embedded = re.search(r"\((\d{1,2}\s*-\s*\d{1,2})(m|mo|months|y)\)", normalized)
    if embedded:
        range_part = clean(embedded.group(1))
        suffix = embedded.group(2)
        label = ""
        if suffix in {"m", "mo", "months"}:
            if range_part == "6 - 9" or range_part == "6-9":
                label = "6-9 months"
            elif range_part == "9 - 12" or range_part == "9-12":
                label = "9-12 months"
            elif range_part == "12 - 18" or range_part == "12-18":
                label = "12-18 months"
        elif suffix == "y":
            label = range_part.replace(" ", "") + " years"
            label = label.replace("-", "-")
        if label:
            ref = choose_preferred_reference(refs, preferred_handle=normalize_text(label).replace(" ", "-"), display_name=label)
            return label, ref, "" if ref else f"no_metaobject_for:{label}"

    return "", None, f"unresolved_size:{raw_value}"


def normalize_size_values(raw_value: str, refs: list[MetaobjectRef]) -> tuple[list[str], list[MetaobjectRef], list[str]]:
    labels: list[str] = []
    mapped_refs: list[MetaobjectRef] = []
    unresolved: list[str] = []
    seen_ref_ids: set[str] = set()

    for token in split_pipe(raw_value):
        label, ref, problem = map_single_size_value(token, refs)
        if problem:
            unresolved.append(problem)
            continue
        if label:
            labels.append(label)
        if ref and ref.id not in seen_ref_ids:
            seen_ref_ids.add(ref.id)
            mapped_refs.append(ref)

    return uniq_preserve(labels), mapped_refs, unresolved


def normalize_color_values(raw_value: str, refs: list[MetaobjectRef]) -> tuple[list[str], list[MetaobjectRef], list[str]]:
    labels: list[str] = []
    mapped_refs: list[MetaobjectRef] = []
    unresolved: list[str] = []
    ref_index = build_metaobject_index(refs)
    seen_ref_ids: set[str] = set()

    for token in split_pipe(raw_value):
        label = clean(token)
        ref = ref_index.get(normalize_text(label))
        if not ref:
            unresolved.append(f"unresolved_color:{token}")
            continue
        labels.append(ref.display_name)
        if ref.id not in seen_ref_ids:
            seen_ref_ids.add(ref.id)
            mapped_refs.append(ref)

    return uniq_preserve(labels), mapped_refs, unresolved


def resolve_field_references(
    *,
    field: str,
    raw_value: str,
    refs_by_field: dict[str, list[MetaobjectRef]],
) -> tuple[list[str], list[MetaobjectRef], list[str]]:
    refs = refs_by_field[field]

    if field == "gender":
        labels, unresolved = normalize_gender_values(raw_value)
        if unresolved:
            return [], [], unresolved
        resolved_refs = []
        for label in labels:
            ref = choose_preferred_reference(refs, preferred_handle=normalize_text(label), display_name=label)
            if not ref:
                return [], [], [f"no_metaobject_for:{label}"]
            resolved_refs.append(ref)
        return labels, resolved_refs, []

    if field == "age_group":
        labels, unresolved = normalize_age_group_values(raw_value)
        if unresolved:
            return [], [], [f"unresolved_age_group:{value}" for value in unresolved]
        resolved_refs = []
        for label in labels:
            preferred_handle = normalize_text(label)
            if preferred_handle == "adults":
                preferred_handle = "adults"
            elif preferred_handle == "toddlers":
                preferred_handle = "toddlers"
            elif preferred_handle == "babies":
                preferred_handle = "babies"
            elif preferred_handle == "kids":
                preferred_handle = "kids"
            ref = choose_preferred_reference(refs, preferred_handle=preferred_handle, display_name=label)
            if not ref:
                return [], [], [f"no_metaobject_for:{label}"]
            resolved_refs.append(ref)
        return labels, resolved_refs, []

    if field == "size":
        return normalize_size_values(raw_value, refs)

    if field == "color":
        return normalize_color_values(raw_value, refs)

    raise RuntimeError(f"Unsupported field `{field}`.")


def plan_changes(
    rows: list[CandidateRow],
    *,
    client: ShopifyClient,
    refs_by_field: dict[str, list[MetaobjectRef]],
    min_confidence: str,
    target_fields: set[str],
    required_size_labels: set[str],
) -> list[PlannedChange]:
    planned: list[PlannedChange] = []
    for row in rows:
        product = client.fetch_product_state(row.handle)
        for field in SUPPORTED_FIELDS:
            if field not in target_fields:
                continue
            current_refs = product.current_refs[field]
            current_raw = product.current_raw[field]
            current_labels = "|".join(ref.display_name for ref in current_refs)
            confidence = row.candidate_confidence[field]
            source = row.candidate_source[field]
            candidate_value = row.candidate_value[field]

            status = "skip"
            reason = ""
            normalized_labels: list[str] = []
            resolved_refs: list[MetaobjectRef] = []

            if field not in row.missing_attributes:
                reason = "field_not_missing_in_audit"
            elif metafield_present(current_raw, current_refs):
                reason = "field_already_present_live"
            elif not candidate_value:
                reason = "candidate_blank"
            elif not confidence_meets_threshold(confidence, min_confidence):
                reason = f"confidence_below_threshold:{confidence}"
            elif field == "size" and required_size_labels:
                candidate_labels = {normalize_text(canonicalize_size_token(value) or value) for value in split_pipe(candidate_value)}
                if not candidate_labels.intersection(required_size_labels):
                    reason = "size_label_not_in_scope"
                else:
                    normalized_labels, resolved_refs, unresolved = resolve_field_references(
                        field=field,
                        raw_value=candidate_value,
                        refs_by_field=refs_by_field,
                    )
                    if unresolved:
                        reason = "|".join(unresolved)
                    elif not resolved_refs:
                        reason = "no_reference_ids_resolved"
                    else:
                        status = "plan"
                        reason = "ready"
            else:
                normalized_labels, resolved_refs, unresolved = resolve_field_references(
                    field=field,
                    raw_value=candidate_value,
                    refs_by_field=refs_by_field,
                )
                if unresolved:
                    reason = "|".join(unresolved)
                elif not resolved_refs:
                    reason = "no_reference_ids_resolved"
                else:
                    status = "plan"
                    reason = "ready"

            planned.append(
                PlannedChange(
                    product_id=product.product_id,
                    product_gid=product.product_gid,
                    handle=product.handle,
                    title=product.title,
                    field=field,
                    current_value=current_raw,
                    current_reference_labels=current_labels,
                    candidate_value=candidate_value,
                    candidate_confidence=confidence,
                    candidate_source=source,
                    normalized_labels="|".join(normalized_labels),
                    reference_ids="|".join(ref.id for ref in resolved_refs),
                    reference_labels="|".join(ref.display_name for ref in resolved_refs),
                    status=status,
                    reason=reason,
                )
            )
    return planned


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def execute_changes(client: ShopifyClient, changes: list[PlannedChange], *, execute: bool, pause_ms: int) -> dict[str, Any]:
    planned_changes = [change for change in changes if change.status == "plan"]
    summary = {
        "execute": bool(execute),
        "planned_attribute_updates": len(planned_changes),
        "applied_attribute_updates": 0,
        "errors": [],
    }

    if not execute:
        return summary

    for change in planned_changes:
        errors = client.set_metafield_references(
            product_gid=change.product_gid,
            key={
                "gender": "target-gender",
                "age_group": "age-group",
                "size": "size",
                "color": "color-pattern",
            }[change.field],
            reference_ids=split_pipe(change.reference_ids),
        )
        if errors:
            summary["errors"].append(
                {
                    "handle": change.handle,
                    "field": change.field,
                    "errors": errors,
                }
            )
        else:
            summary["applied_attribute_updates"] += 1
        if pause_ms > 0:
            time.sleep(pause_ms / 1000.0)
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Fill Shopify structured apparel fields from top revenue audit candidates.")
    parser.add_argument("--store-domain", default="", help="Shopify store domain.")
    parser.add_argument("--access-token", default="", help="Shopify Admin API access token.")
    parser.add_argument("--input-csv", default=str(DEFAULT_INPUT_CSV), help="Input CSV of audited top revenue candidates.")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="Directory for dry-run / execution artifacts.")
    parser.add_argument(
        "--fields",
        default=",".join(SUPPORTED_FIELDS),
        help="Comma-separated subset of fields to plan/apply (gender,age_group,size,color).",
    )
    parser.add_argument(
        "--require-size-labels",
        default="",
        help="Comma-separated normalized size labels required for a size row to be in scope (for example: 6-7 years,7-8 years,8-9 years,3XL).",
    )
    parser.add_argument("--min-confidence", default="high", choices=["high", "medium"], help="Minimum audit confidence required.")
    parser.add_argument("--execute", action="store_true", help="Apply planned attribute updates live.")
    parser.add_argument("--pause-ms", type=int, default=250, help="Pause between live updates.")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    client = ShopifyClient(
        resolve_store_domain(args.store_domain, fallback_domain="dresslikemommy-com.myshopify.com"),
        load_access_token(args.access_token),
    )
    rows = load_candidates(Path(args.input_csv))
    requested_fields = {normalize_text(field).replace("-", "_") for field in split_csv(args.fields)}
    invalid_fields = sorted(requested_fields.difference(SUPPORTED_FIELDS))
    if invalid_fields:
        raise RuntimeError(f"Unsupported fields requested: {', '.join(invalid_fields)}")
    if not requested_fields:
        raise RuntimeError("At least one field must be selected with --fields.")
    required_size_labels = {normalize_text(label) for label in split_csv(args.require_size_labels)}
    refs_by_field = {
        "gender": client.fetch_metaobjects("shopify--target-gender"),
        "age_group": client.fetch_metaobjects("shopify--age-group"),
        "size": client.fetch_metaobjects("shopify--size"),
        "color": client.fetch_metaobjects("shopify--color-pattern"),
    }
    changes = plan_changes(
        rows,
        client=client,
        refs_by_field=refs_by_field,
        min_confidence=args.min_confidence,
        target_fields=requested_fields,
        required_size_labels=required_size_labels,
    )
    execution = execute_changes(client, changes, execute=args.execute, pause_ms=max(args.pause_ms, 0))

    fieldnames = [
        "product_id",
        "handle",
        "title",
        "field",
        "current_value",
        "current_reference_labels",
        "candidate_value",
        "candidate_confidence",
        "candidate_source",
        "normalized_labels",
        "reference_labels",
        "reference_ids",
        "status",
        "reason",
    ]
    write_csv(
        output_dir / "planned_apparel_attribute_changes.csv",
        [
            {
                "product_id": item.product_id,
                "handle": item.handle,
                "title": item.title,
                "field": item.field,
                "current_value": item.current_value,
                "current_reference_labels": item.current_reference_labels,
                "candidate_value": item.candidate_value,
                "candidate_confidence": item.candidate_confidence,
                "candidate_source": item.candidate_source,
                "normalized_labels": item.normalized_labels,
                "reference_labels": item.reference_labels,
                "reference_ids": item.reference_ids,
                "status": item.status,
                "reason": item.reason,
            }
            for item in changes
        ],
        fieldnames,
    )

    summary = {
        "input_csv": str(Path(args.input_csv)),
        "target_rows": len(rows),
        "selected_fields": sorted(requested_fields),
        "required_size_labels": sorted(required_size_labels),
        "planned_attribute_updates": sum(1 for item in changes if item.status == "plan"),
        "skipped_attribute_updates": sum(1 for item in changes if item.status != "plan"),
        "planned_by_field": {
            field: sum(1 for item in changes if item.status == "plan" and item.field == field)
            for field in SUPPORTED_FIELDS
        },
        "skipped_by_field": {
            field: sum(1 for item in changes if item.status != "plan" and item.field == field)
            for field in SUPPORTED_FIELDS
        },
        "skip_reasons": {},
        "execution": execution,
    }
    skip_reasons: dict[str, int] = {}
    for item in changes:
        if item.status == "plan":
            continue
        skip_reasons[item.reason] = skip_reasons.get(item.reason, 0) + 1
    summary["skip_reasons"] = skip_reasons
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
