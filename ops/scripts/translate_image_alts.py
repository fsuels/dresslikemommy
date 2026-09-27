#!/usr/bin/env python3
"""Translate storefront image alt text into every published storefront language.

Shopify serves the translated alt on localized routes (/es, /fr, ...) both as
the <img alt> and, through snippets/jsonld-seo.liquid, as the Product JSON-LD
ImageObject caption. Without a translation the English alt is shown.

Scope: images of ACTIVE/DRAFT products (MEDIA_IMAGE), collection images
(COLLECTION_IMAGE) and blog featured images (ARTICLE_IMAGE).

Subcommands (read-only unless --execute is passed):

  queue   List every image alt that has no current translation in one or more
          published locales, plus the unique English strings to translate.
  apply   Validate translations from JSON files shaped
          {"<locale>": {"<exact English alt>": "<translated alt>"}} and
          register them with the live content digest, then read them back.
          A translation is only used when its English key still equals the
          live alt, so an alt edited after the queue is never mistranslated.

Translations are written by a reviewer (a person or a Claude task); this tool
does not call a machine-translation service.

Shopify does not reliably flag a translation as outdated when the English alt
changes (the 2026-09-26 alt rewrite left old translations "current"), so each
written translation's source digest is recorded in a local state file and a
translation whose digest no longer matches the live alt is queued again.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ops.scripts.image_seo import (  # noqa: E402
    BANNED_ALT_PATTERNS,
    DEFAULT_EVIDENCE_DIR,
    ShopifyClient,
    build_client,
    clean,
    iso,
    utc_now,
)

DEFAULT_STATE_PATH = Path.home() / ".config" / "dresslikemommy" / "image-alt-translation-state.json"
TRANSLATED_ALT_MAX_LENGTH = 200
RESOURCE_BATCH = 25
REGISTER_BATCH = 10
EXTRA_RESOURCE_TYPES = ("COLLECTION_IMAGE", "ARTICLE_IMAGE")

SHOP_LOCALES_QUERY = "query { shopLocales { locale primary published } }"
PRODUCT_MEDIA_QUERY = """
query ImageAltProductMedia($after: String, $query: String) {
  products(first: 100, after: $after, query: $query) {
    pageInfo { hasNextPage endCursor }
    nodes { id handle media(first: 100) { nodes { id mediaContentType } } }
  }
}
"""
RESOURCE_IDS_QUERY = """
query ImageAltResourceIds($after: String, $type: TranslatableResourceType!) {
  translatableResources(first: 250, after: $after, resourceType: $type) {
    pageInfo { hasNextPage endCursor }
    nodes { resourceId }
  }
}
"""


def locale_alias(locale: str) -> str:
    return "t_" + re.sub(r"[^A-Za-z0-9]", "_", locale)


def resources_query(locales: List[str]) -> str:
    fragments = "\n".join(
        f'{locale_alias(locale)}: translations(locale: "{locale}") {{ key value outdated }}' for locale in locales
    )
    return f"""
query ImageAltTranslations($ids: [ID!]!, $first: Int!) {{
  translatableResourcesByIds(resourceIds: $ids, first: $first) {{
    nodes {{
      resourceId
      translatableContent {{ key value digest locale }}
      {fragments}
    }}
  }}
}}
"""


def register_mutation(count: int) -> str:
    params = ", ".join(f"$id{i}: ID!, $t{i}: [TranslationInput!]!" for i in range(count))
    calls = "\n".join(
        f"r{i}: translationsRegister(resourceId: $id{i}, translations: $t{i}) "
        "{ translations { key locale value } userErrors { field message code } }"
        for i in range(count)
    )
    return f"mutation ImageAltRegister({params}) {{\n{calls}\n}}"


# ------------------------------------------------------------------ reading


def published_locales(client: ShopifyClient) -> List[str]:
    rows = client.graphql(SHOP_LOCALES_QUERY)["shopLocales"]
    return sorted(row["locale"] for row in rows if row.get("published") and not row.get("primary"))


def image_resource_ids(client: ShopifyClient) -> List[Tuple[str, str]]:
    """Return (resource_id, kind) for every in-scope image."""
    found: List[Tuple[str, str]] = []
    seen = set()
    for product in client.paginate(PRODUCT_MEDIA_QUERY, "products", {"query": "status:active OR status:draft"}):
        for media in (product.get("media") or {}).get("nodes") or []:
            if media.get("mediaContentType") == "IMAGE" and media["id"] not in seen:
                seen.add(media["id"])
                found.append((media["id"], "product_media"))
    for resource_type in EXTRA_RESOURCE_TYPES:
        for node in client.paginate(RESOURCE_IDS_QUERY, "translatableResources", {"type": resource_type}):
            if node["resourceId"] not in seen:
                seen.add(node["resourceId"])
                found.append((node["resourceId"], resource_type.lower()))
    return found


def parse_resource(node: Dict[str, Any], locales: List[str]) -> Optional[Dict[str, Any]]:
    content = next((item for item in node.get("translatableContent") or [] if item.get("key") == "alt"), None)
    if not content or not clean(content.get("value")):
        return None
    translations = {}
    for locale in locales:
        item = next((t for t in node.get(locale_alias(locale)) or [] if t.get("key") == "alt"), None)
        if item:
            translations[locale] = {"value": item.get("value") or "", "outdated": bool(item.get("outdated"))}
    return {
        "resource_id": node["resourceId"],
        "source": content["value"],
        "digest": content["digest"],
        "translations": translations,
    }


def fetch_resources(client: ShopifyClient, resource_ids: List[str], locales: List[str]) -> Dict[str, Dict[str, Any]]:
    query = resources_query(locales)
    found: Dict[str, Dict[str, Any]] = {}
    for start in range(0, len(resource_ids), RESOURCE_BATCH):
        chunk = resource_ids[start : start + RESOURCE_BATCH]
        data = client.graphql(query, {"ids": chunk, "first": len(chunk)})["translatableResourcesByIds"]
        for node in data["nodes"]:
            parsed = parse_resource(node, locales)
            if parsed:
                found[parsed["resource_id"]] = parsed
    return found


def missing_locales(resource: Dict[str, Any], locales: Iterable[str], state: Optional[Dict[str, Dict[str, str]]] = None) -> List[str]:
    """Locales whose translation is absent, outdated, invalid, or made from an older English alt."""
    recorded = (state or {}).get(resource["resource_id"], {})
    missing = []
    for locale in locales:
        current = resource["translations"].get(locale)
        if (
            not current
            or current["outdated"]
            or validate_translation(resource["source"], current["value"], locale)
            or (locale in recorded and recorded[locale] != resource["digest"])
        ):
            missing.append(locale)
    return missing


def load_digest_state(path: Path) -> Dict[str, Dict[str, str]]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def save_digest_state(path: Path, state: Dict[str, Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    tmp.replace(path)


def load_state(client: ShopifyClient, locales_arg: str) -> Tuple[List[str], Dict[str, str], Dict[str, Dict[str, Any]]]:
    locales = [clean(v) for v in locales_arg.split(",") if clean(v)] if locales_arg else published_locales(client)
    ids = image_resource_ids(client)
    kinds = dict(ids)
    resources = fetch_resources(client, [rid for rid, _ in ids], locales)
    return locales, kinds, resources


# --------------------------------------------------------------- validation


def validate_translation(source: str, value: str, locale: str) -> List[str]:
    text = clean(value)
    issues = []
    if not text:
        return ["empty"]
    if len(text) > TRANSLATED_ALT_MAX_LENGTH:
        issues.append("too_long")
    if value != text:
        issues.append("untrimmed_or_multiline")
    if text.lower() == clean(source).lower() and not locale.lower().startswith("en"):
        issues.append("same_as_english")
    if re.search(r"<[^>]+>|\{\{|\{%|QZXTOKEN|DLMTOKEN", text):
        issues.append("markup_or_placeholder")
    lowered = text.lower()
    if any(re.search(pattern, lowered) for pattern in BANNED_ALT_PATTERNS):
        issues.append("banned_term")
    return issues


def load_translations(paths: List[str]) -> Dict[str, Dict[str, str]]:
    merged: Dict[str, Dict[str, str]] = defaultdict(dict)
    for path in paths:
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise SystemExit(f"{path}: expected an object keyed by locale")
        for locale, mapping in payload.items():
            if not isinstance(mapping, dict):
                raise SystemExit(f"{path}: {locale} must map English alt -> translation")
            for source, value in mapping.items():
                merged[locale][source] = value
    return merged


def plan_writes(
    resources: Dict[str, Dict[str, Any]],
    locales: List[str],
    translations: Dict[str, Dict[str, str]],
    *,
    force: bool = False,
    state: Optional[Dict[str, Dict[str, str]]] = None,
) -> Tuple[Dict[str, List[Dict[str, str]]], List[Dict[str, Any]], Dict[str, int]]:
    writes: Dict[str, List[Dict[str, str]]] = defaultdict(list)
    rejected: List[Dict[str, Any]] = []
    counts = defaultdict(int)
    for resource_id, resource in resources.items():
        targets = locales if force else missing_locales(resource, locales, state)
        for locale in targets:
            value = translations.get(locale, {}).get(resource["source"])
            if value is None:
                counts["untranslated"] += 1
                continue
            issues = validate_translation(resource["source"], value, locale)
            if issues:
                rejected.append({"resource_id": resource_id, "locale": locale, "source": resource["source"], "value": value, "issues": issues})
                continue
            current = resource["translations"].get(locale)
            if current and current["value"] == value and not current["outdated"]:
                counts["already_current"] += 1
                continue
            writes[resource_id].append(
                {"locale": locale, "key": "alt", "value": value, "translatableContentDigest": resource["digest"]}
            )
            counts["planned"] += 1
    counts["rejected"] = len(rejected)
    return dict(writes), rejected, dict(counts)


# ----------------------------------------------------------------- commands


def command_queue(args: argparse.Namespace) -> int:
    client = build_client(args)
    locales, kinds, resources = load_state(client, args.locales)
    state = load_digest_state(Path(args.state_path))
    rows = []
    unique: Dict[str, List[str]] = defaultdict(list)
    for resource_id, resource in resources.items():
        missing = missing_locales(resource, locales, state)
        if not missing:
            continue
        rows.append({"resource_id": resource_id, "kind": kinds.get(resource_id), "source": resource["source"], "missing_locales": missing})
        for locale in missing:
            if resource["source"] not in unique[locale]:
                unique[locale].append(resource["source"])
    report = {
        "generated_at": iso(utc_now()),
        "locales": locales,
        "resources_with_alt": len(resources),
        "resources_needing_translation": len(rows),
        "missing_pairs": sum(len(row["missing_locales"]) for row in rows),
        "unique_sources": sorted({row["source"] for row in rows}),
        "unique_sources_by_locale": {locale: len(values) for locale, values in sorted(unique.items())},
        "rows": rows,
    }
    Path(args.output).write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("resources_with_alt", "resources_needing_translation", "missing_pairs", "unique_sources_by_locale")}, indent=2))
    print(f"unique English strings: {len(report['unique_sources'])}; queue: {args.output}")
    return 0


def register(client: ShopifyClient, writes: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, Any]]:
    errors = []
    items = list(writes.items())
    for start in range(0, len(items), REGISTER_BATCH):
        chunk = items[start : start + REGISTER_BATCH]
        variables = {}
        for i, (resource_id, translations) in enumerate(chunk):
            variables[f"id{i}"] = resource_id
            variables[f"t{i}"] = translations
        data = client.graphql(register_mutation(len(chunk)), variables)
        for i, (resource_id, _) in enumerate(chunk):
            for error in (data.get(f"r{i}") or {}).get("userErrors") or []:
                errors.append({"resource_id": resource_id, **error})
    return errors


def command_apply(args: argparse.Namespace) -> int:
    client = build_client(args)
    translations = load_translations(args.translations)
    locales, kinds, resources = load_state(client, args.locales)
    state_path = Path(args.state_path)
    state = load_digest_state(state_path)
    writes, rejected, counts = plan_writes(resources, locales, translations, force=args.force, state=state)
    receipt: Dict[str, Any] = {
        "generated_at": iso(utc_now()),
        "mode": "execute" if args.execute else "dry_run",
        "locales": locales,
        "counts": counts,
        "rejected": rejected,
        "writes": [
            {"resource_id": rid, "kind": kinds.get(rid), "source": resources[rid]["source"], "locale": t["locale"], "value": t["value"],
             "before": (resources[rid]["translations"].get(t["locale"]) or {}).get("value", "")}
            for rid, items in writes.items()
            for t in items
        ],
    }
    exit_code = 0
    if args.execute and writes:
        receipt["user_errors"] = register(client, writes)
        after = fetch_resources(client, list(writes), locales)
        mismatches = []
        for resource_id, items in writes.items():
            for item in items:
                current = (after.get(resource_id) or {}).get("translations", {}).get(item["locale"])
                if not current or current["value"] != item["value"] or current["outdated"]:
                    mismatches.append({"resource_id": resource_id, "locale": item["locale"], "expected": item["value"], "live": current})
        receipt["readback_mismatches"] = mismatches
        receipt["readback_checked"] = sum(len(items) for items in writes.values())
        failed = {(row["resource_id"], row["locale"]) for row in mismatches}
        # Re-read so a concurrent run's entries for other locales are kept.
        state = load_digest_state(state_path)
        for resource_id, items in writes.items():
            for item in items:
                if (resource_id, item["locale"]) not in failed:
                    state.setdefault(resource_id, {})[item["locale"]] = item["translatableContentDigest"]
        save_digest_state(state_path, state)
        if receipt["user_errors"] or mismatches:
            exit_code = 1
    if args.receipt:
        Path(args.receipt).parent.mkdir(parents=True, exist_ok=True)
        Path(args.receipt).write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    summary = {"mode": receipt["mode"], **counts}
    if args.execute:
        summary.update(user_errors=len(receipt.get("user_errors", [])), readback_mismatches=len(receipt.get("readback_mismatches", [])))
    print(json.dumps(summary, indent=2))
    for row in rejected[:20]:
        print(f"REJECTED {row['locale']} {row['resource_id']}: {','.join(row['issues'])} :: {row['value']}")
    return exit_code or (1 if rejected and args.execute else 0)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--store-domain", default="")
    parser.add_argument("--access-token", default="")
    parser.add_argument("--locales", default="", help="Comma-separated locales (default: all published non-primary)")
    parser.add_argument("--state-path", default=str(DEFAULT_STATE_PATH), help="Local record of the English digest each translation was made from")
    sub = parser.add_subparsers(dest="command", required=True)

    queue = sub.add_parser("queue")
    queue.add_argument("--output", required=True)
    queue.set_defaults(func=command_queue)

    apply = sub.add_parser("apply")
    apply.add_argument("--translations", action="append", required=True, help="JSON {locale: {English alt: translation}}; repeatable")
    apply.add_argument("--receipt", default=str(DEFAULT_EVIDENCE_DIR / "translations" / "apply_receipt.json"))
    apply.add_argument("--execute", action="store_true")
    apply.add_argument("--force", action="store_true", help="Also rewrite current translations that differ")
    apply.set_defaults(func=command_apply)
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
