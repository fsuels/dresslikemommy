"""Offline validation of independent, current QA before product activation."""
import hashlib
import json
import math
from decimal import Decimal, InvalidOperation
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHECKS = (
    "supplier_current", "offer_current", "source_sizes_measured", "variant_mapping",
    "media_fidelity", "all_colors_shown", "seo_truthful", "all_published_locales",
    "language_review", "category_specific_gates", "all_variants_economics",
)
LOCALIZATION_STEPS = frozenset((
    "translate_full_product", "audit_full_product_before_size_repair",
    "repair_localized_size_charts", "audit_full_product_after_size_repair",
    "audit_localized_size_charts", "audit_variant_size_chart_mapping",
))
REGISTRIES = {"codex": "team.json", "claude": "claude_team.json"}


class QualityHold(ValueError):
    pass


def fingerprint(product):
    return hashlib.sha256(json.dumps(product, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def _timestamp(value):
    try:
        result = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if result.tzinfo is None:
            raise ValueError("timezone required")
        return result
    except (AttributeError, TypeError, ValueError) as exc:
        raise QualityHold("invalid dated QA evidence") from exc


def _number(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise QualityHold("invalid economics number")
    return value


def _variants(product):
    connection = product.get("variants")
    if not isinstance(connection, dict):
        raise QualityHold("current variant readback required")
    page = connection.get("pageInfo")
    if not isinstance(page, dict) or page.get("hasNextPage") is not False:
        raise QualityHold("variant readback is incomplete")
    nodes = connection.get("nodes")
    if not isinstance(nodes, list) or not nodes:
        raise QualityHold("current variants are missing")
    prices, colors = {}, {}
    for node in nodes:
        if not isinstance(node, dict):
            raise QualityHold("invalid current variant")
        key = node.get("id")
        if not isinstance(key, str) or not key or key in prices:
            raise QualityHold("current variant identities missing/duplicated")
        try:
            raw_price = node["price"]
            if isinstance(raw_price, bool):
                raise ValueError("boolean price")
            price = Decimal(str(raw_price))
            if not price.is_finite() or price <= 0:
                raise ValueError("nonpositive price")
        except (KeyError, InvalidOperation, ValueError) as exc:
            raise QualityHold("invalid current variant price") from exc
        prices[key] = price
        options = node.get("selectedOptions")
        if not isinstance(options, list) or any(not isinstance(o, dict) for o in options):
            raise QualityHold("current variant options required")
        for option in options:
            if str(option.get("name", "")).strip().casefold() in ("color", "colour", "colorway", "colourway"):
                color = option.get("value")
                if not isinstance(color, str) or not color.strip():
                    raise QualityHold("invalid offered color")
                media = node.get("media")
                images = media.get("nodes", []) if isinstance(media, dict) else []
                has_image = any(isinstance(m, dict) and isinstance(m.get("image"), dict) and m["image"].get("id") for m in images)
                colors[color] = colors.get(color, False) or has_image
    if not all(colors.values()):
        raise QualityHold("each offered color needs an associated current image")
    return prices


def validate(receipt, product, handle, registry, closeout_bytes, now=None):
    now = now or datetime.now(timezone.utc)
    if not all(isinstance(value, dict) for value in (receipt, product, registry)):
        raise QualityHold("invalid QA/product/registry structure")
    if registry.get("rollout_status") != "READY":
        raise QualityHold("category rollout is not READY")
    quality_id = registry.get("roles", {}).get("quality", {}).get("thread_id")
    if not quality_id or receipt.get("reviewer_thread_id") != quality_id:
        raise QualityHold("review must come from current canonical Quality role")
    if receipt.get("creator_thread_id") == quality_id or not receipt.get("creator_thread_id"):
        raise QualityHold("independent creator and reviewer required")
    creators = {v.get("thread_id") for k, v in registry.get("roles", {}).items() if k not in ("quality", "organic")}
    if receipt.get("creator_thread_id") not in creators:
        raise QualityHold("creator is not a current product owner")
    if receipt.get("handle") != handle or receipt.get("product_id") != product.get("id"):
        raise QualityHold("QA product identity mismatch")
    if product.get("status") != "DRAFT" or not product.get("updatedAt"):
        raise QualityHold("current dated DRAFT readback required")
    if receipt.get("product_fingerprint") != fingerprint(product):
        raise QualityHold("product changed after QA")
    live_prices = _variants(product)
    media = product.get("mediaCount", {}).get("count")
    if type(media) is not int or media < 4:
        raise QualityHold("at least four reviewed base images required")
    reviewed = _timestamp(receipt.get("reviewed_at"))
    if not timedelta(0) <= now - reviewed <= timedelta(hours=24):
        raise QualityHold("QA is future-dated or expired")
    revision = _timestamp(product["updatedAt"])
    if revision > reviewed:
        raise QualityHold("QA predates current product revision")
    if any(receipt.get("checks", {}).get(key) is not True for key in CHECKS):
        raise QualityHold("one or more independent QA checks are incomplete")
    if receipt.get("localization_closeout_sha256") != hashlib.sha256(closeout_bytes).hexdigest():
        raise QualityHold("localization closeout changed or missing")
    try:
        closeout = json.loads(closeout_bytes)
    except (TypeError, ValueError) as exc:
        raise QualityHold("invalid localization closeout") from exc
    if not isinstance(closeout, dict):
        raise QualityHold("invalid localization closeout")
    steps = closeout.get("steps", [])
    if (closeout.get("status") != "passed" or handle not in closeout.get("handles", [])
            or not isinstance(steps, list) or len(steps) != len(LOCALIZATION_STEPS)
            or any(not isinstance(s, dict) or type(s.get("exit_code")) is not int or s["exit_code"] != 0 for s in steps)
            or {s.get("name") for s in steps} != LOCALIZATION_STEPS):
        raise QualityHold("all six current localization phases must pass")
    completed = _timestamp(closeout.get("completed_at"))
    if (completed.utcoffset() != timedelta(0) or not revision <= completed <= reviewed
            or not timedelta(0) <= now - completed <= timedelta(hours=24)):
        raise QualityHold("localization closeout must be current UTC and bound to this revision before QA")
    bindings = closeout.get("source_bindings")
    binding = bindings.get(handle) if isinstance(bindings, dict) else None
    if not isinstance(binding, dict) or binding.get("status") != "stable":
        raise QualityHold("localization requires before/after source binding")
    before, after = binding.get("before"), binding.get("after")
    if not isinstance(before, dict) or not isinstance(after, dict):
        raise QualityHold("localization source snapshots are missing")
    for snapshot in (before, after):
        digest = snapshot.get("source_sha256")
        locales = snapshot.get("locales")
        if (snapshot.get("product_id") != product["id"] or _timestamp(snapshot.get("updated_at")) != revision
                or not isinstance(digest, str) or len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest)
                or not isinstance(locales, list) or not locales or any(not isinstance(locale, str) or not locale.strip() for locale in locales)
                or len(set(locales)) != len(locales)):
            raise QualityHold("localization source identity/revision/digests/locales are incomplete")
    if before["source_sha256"] != after["source_sha256"] or sorted(before["locales"]) != sorted(after["locales"]):
        raise QualityHold("localization source or published locales changed during closeout")
    current_locales = product.get("publishedLocales")
    if (not isinstance(current_locales, list) or not current_locales or any(not isinstance(locale, str) or not locale for locale in current_locales)
            or len(set(current_locales)) != len(current_locales) or sorted(current_locales) != sorted(after["locales"])):
        raise QualityHold("localization must cover the currently published locale set")
    if not revision <= _timestamp(before.get("observed_at")) <= _timestamp(after.get("observed_at")) <= completed:
        raise QualityHold("localization source observation order is invalid")
    economics = receipt.get("economics")
    if not isinstance(economics, list) or not economics:
        raise QualityHold("per-variant landed economics required")
    seen = set()
    for row in economics:
        if not isinstance(row, dict):
            raise QualityHold("invalid variant economics row")
        key = row.get("variant_key")
        if not isinstance(key, str) or not key or key in seen:
            raise QualityHold("variant economics identities missing/duplicated")
        seen.add(key)
        price, landed, net = (_number(row.get(k)) for k in ("price", "landed", "net_margin"))
        if key not in live_prices or live_prices[key] != Decimal(str(price)):
            raise QualityHold("economics must match current variant identities and prices")
        parts = row.get("breakdown")
        deductions = row.get("deductions")
        if not isinstance(parts, dict) or not isinstance(deductions, dict):
            raise QualityHold("explicit landed breakdown and net deductions required")
        values = [_number(parts.get(k)) for k in ("product", "domestic", "freight", "services")]
        deducted = [_number(deductions.get(k)) for k in ("fees", "refunds", "other")]
        derived_net = (price - landed - sum(deducted)) / price if price > 0 else -1
        if (price <= 0 or landed <= 0 or min(values + deducted) < 0 or abs(sum(values) - landed) > .02
                or landed > price * .5 or not .35 <= derived_net <= 1 or abs(net - derived_net) > .000001):
            raise QualityHold("actual landed/net economics fail owner targets")
        quoted = _timestamp(row.get("quote_as_of"))
        if not timedelta(0) <= now - quoted <= timedelta(hours=72):
            raise QualityHold("current freight/services quote required")
    if seen != set(live_prices):
        raise QualityHold("economics must cover every current variant exactly once")
    return {"status": "passed", "handle": handle, "reviewer_thread_id": quality_id, "product_fingerprint": fingerprint(product)}


def require_ready(handle, product, root=ROOT):
    if not handle or any(c not in "abcdefghijklmnopqrstuvwxyz0123456789-" for c in handle):
        raise QualityHold("invalid product handle")
    try:
        receipt = json.loads((root / "ops/category-team/receipts" / (handle + "-qa.json")).read_text())
        # Owner, 2026-11-25: a receipt marked runtime "claude" is checked against the Claude team registry.
        # Only the identity registry differs; every check in validate() applies unchanged.
        if not isinstance(receipt, dict) or receipt.get("runtime", "codex") not in REGISTRIES:
            raise QualityHold("unknown QA runtime")
        registry = json.loads((root / "ops/category-team" / REGISTRIES[receipt.get("runtime", "codex")]).read_text())
        closeout = (root / "ops/listings" / (handle + "-localization-closeout.json")).read_bytes()
    except (OSError, ValueError) as exc:
        raise QualityHold("independent QA receipt/registry/closeout unavailable") from exc
    return validate(receipt, product, handle, registry, closeout)
