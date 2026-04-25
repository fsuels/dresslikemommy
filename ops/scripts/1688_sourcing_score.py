#!/usr/bin/env python3
"""Score 1688 sourcing candidates and build a visual shortlist report.

This is a dev/operator tool. It does not log into 1688, scrape private APIs, or
write to Shopify. Feed it candidate data gathered from a logged-in browser
session, and it creates local review artifacts for merchandising decisions.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import html
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit


DEFAULT_OUTPUT_ROOT = Path("ops/sourcing")
VERDICT_ORDER = {"Gold": 0, "Test": 1, "Reject": 2}
CSV_FIELDNAMES = [
    "candidate_id",
    "review_stage",
    "verdict",
    "score",
    "product_url",
    "image_url",
    "title",
    "vendor_name",
    "vendor_url",
    "vendor_location",
    "price_cny",
    "moq",
    "monthly_sales",
    "repurchase_rate_pct",
    "rating",
    "years_on_1688",
    "badges",
    "service_flags",
    "dropship_supported",
    "size_chart",
    "category_match",
    "style_fit",
    "image_quality",
    "ip_risk_flags",
    "positive_signals",
    "concerns",
    "next_action",
    "raw_card_text",
    "notes",
]

ALIASES = {
    "product_url": ("product_url", "url", "link", "href", "detail_url", "offer_url", "product link"),
    "image_url": ("image_url", "image", "img", "image_src", "main_image", "thumbnail", "picture"),
    "title": ("title", "product_title", "name", "product_name"),
    "vendor_name": ("vendor_name", "supplier", "supplier_name", "shop", "shop_name", "company"),
    "vendor_url": ("vendor_url", "supplier_url", "shop_url", "company_url"),
    "vendor_location": ("vendor_location", "location", "region", "province", "city"),
    "price_cny": ("price_cny", "price", "price_rmb", "unit_price", "min_price"),
    "moq": ("moq", "minimum_order", "min_order", "min_qty", "起批量"),
    "monthly_sales": ("monthly_sales", "sales", "orders", "sold", "成交", "recent_sales"),
    "repurchase_rate_pct": ("repurchase_rate_pct", "repurchase_rate", "return_rate", "repeat_rate", "回头率"),
    "rating": ("rating", "service_score", "shop_score", "score"),
    "years_on_1688": ("years_on_1688", "years", "supplier_years", "诚信通年限", "经营年限"),
    "badges": ("badges", "badge", "certifications", "certification", "seller_badges"),
    "service_flags": ("service_flags", "services", "shipping_flags", "delivery_flags", "保障"),
    "dropship_supported": ("dropship_supported", "dropship", "one_piece_dropship", "一件代发"),
    "size_chart": ("size_chart", "has_size_chart", "sizechart", "尺码表", "size_chart_available"),
    "category_match": ("category_match", "category_fit", "listing_fit", "fit"),
    "style_fit": ("style_fit", "style_score", "brand_fit"),
    "image_quality": ("image_quality", "image_score", "photo_quality"),
    "ip_risk_flags": ("ip_risk_flags", "ip_risk", "brand_risk", "copyright_risk", "risk_flags"),
    "raw_card_text": ("raw_card_text", "raw_text", "text", "card_text", "visible_text"),
    "notes": ("notes", "note", "comments", "comment"),
}

POSITIVE_BADGE_PATTERNS = {
    "实力商家": ("实力商家", "strength merchant", "powerful merchant"),
    "超级工厂": ("超级工厂", "super factory"),
    "深度验厂": ("深度验厂", "深度认证", "验厂", "deep verification"),
    "真实工厂": ("真实工厂", "real factory"),
    "买家保障": ("买家保障", "buyer protection"),
    "品质保障": ("品质保障", "quality guarantee"),
    "官方物流": ("官方物流", "official logistics"),
    "48小时发货": ("48小时发货", "48h", "48 h", "48-hour", "48 hour"),
    "24小时发货": ("24小时发货", "24h", "24 h", "24-hour", "24 hour"),
    "现货": ("现货", "ready stock", "in stock"),
    "一件代发": ("一件代发", "dropship", "drop ship", "one piece"),
    "包换": ("包换", "15天包换", "return/exchange"),
}

IP_RISK_TERMS = (
    "disney",
    "mickey",
    "minnie",
    "nike",
    "adidas",
    "barbie",
    "hello kitty",
    "snoopy",
    "pokemon",
    "marvel",
    "frozen",
    "logo",
    "branded",
    "character",
    "迪士尼",
    "米奇",
    "米妮",
    "耐克",
    "阿迪",
    "芭比",
    "凯蒂猫",
    "史努比",
    "宝可梦",
    "漫威",
    "冰雪奇缘",
    "卡通",
    "联名",
    "品牌",
)


@dataclass
class Candidate:
    candidate_id: str
    product_url: str = ""
    image_url: str = ""
    title: str = ""
    vendor_name: str = ""
    vendor_url: str = ""
    vendor_location: str = ""
    price_cny: str = ""
    moq: str = ""
    monthly_sales: str = ""
    repurchase_rate_pct: str = ""
    rating: str = ""
    years_on_1688: str = ""
    badges: str = ""
    service_flags: str = ""
    dropship_supported: str = ""
    size_chart: str = ""
    category_match: str = ""
    style_fit: str = ""
    image_quality: str = ""
    ip_risk_flags: str = ""
    raw_card_text: str = ""
    notes: str = ""
    score: int = 0
    verdict: str = "Test"
    breakdown: dict[str, float] = field(default_factory=dict)
    positive_signals: list[str] = field(default_factory=list)
    concerns: list[str] = field(default_factory=list)
    next_action: str = ""
    listing_request: str = ""
    review_stage: str = "search"


def clean(value: Any) -> str:
    if value is None:
        return ""
    return re.sub(r"\s+", " ", str(value)).strip()


def normalize_key(key: str) -> str:
    return re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "_", clean(key).lower()).strip("_")


def first_value(row: dict[str, Any], field: str) -> str:
    normalized = {normalize_key(key): value for key, value in row.items()}
    for alias in ALIASES[field]:
        key = normalize_key(alias)
        if key in normalized and clean(normalized[key]):
            return clean(normalized[key])
    return ""


def load_rows(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    if path.suffix.lower() == ".json":
        payload = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(payload, dict):
            if isinstance(payload.get("candidates"), list):
                return payload["candidates"]
            if isinstance(payload.get("items"), list):
                return payload["items"]
        if isinstance(payload, list):
            return payload
        raise ValueError("JSON input must be an array or an object with a candidates/items array.")

    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def number(value: str) -> float | None:
    text = clean(value).replace(",", "")
    if not text:
        return None
    match = re.search(r"-?\d+(?:\.\d+)?", text)
    if not match:
        return None
    return float(match.group(0))


def percent(value: str) -> float | None:
    parsed = number(value)
    if parsed is None:
        return None
    if parsed <= 1 and "%" not in value:
        parsed *= 100
    return max(0.0, min(parsed, 100.0))


def yes_no_unknown(value: str) -> bool | None:
    text = clean(value).lower()
    if not text:
        return None
    yes_terms = ("yes", "y", "true", "1", "supported", "support", "has", "有", "是", "支持", "可", "一件代发")
    no_terms = ("no", "n", "false", "0", "none", "not", "没有", "无", "否", "不支持")
    if any(term in text for term in yes_terms):
        return True
    if any(term in text for term in no_terms):
        return False
    return None


def score_0_to_5(value: str, default: float) -> float:
    parsed = number(value)
    if parsed is None:
        return default
    return max(0.0, min(parsed, 5.0))


def compact_url(url: str) -> str:
    text = clean(url)
    if not text:
        return ""
    try:
        parts = urlsplit(text)
    except ValueError:
        return text
    if not parts.scheme:
        return text
    return f"{parts.netloc}{parts.path}"


def offer_key(product_url: str) -> str:
    match = re.search(r"/offer/(\d+)\.html", clean(product_url))
    if match:
        return match.group(1)
    return clean(product_url)


def load_rejected_keys(path: Path | None) -> set[str]:
    if not path or not path.exists():
        return set()
    payload = json.loads(path.read_text(encoding="utf-8"))
    items = payload.get("items", {}) if isinstance(payload, dict) else {}
    rejected: set[str] = set()
    for key, item in items.items():
        if not isinstance(item, dict) or item.get("action") != "reject":
            continue
        rejected.add(clean(key))
        product_url = clean(item.get("product_url"))
        if product_url:
            rejected.add(offer_key(product_url))
    return {key for key in rejected if key}


def stable_id(row: dict[str, Any], index: int) -> str:
    seed = first_value(row, "product_url") or first_value(row, "title") or json.dumps(row, ensure_ascii=False)
    digest = hashlib.sha1(seed.encode("utf-8")).hexdigest()[:8]
    return f"C{index:03d}-{digest}"


def detect_signals(candidate: Candidate) -> set[str]:
    haystack = " ".join(
        [
            candidate.title,
            candidate.badges,
            candidate.service_flags,
            candidate.raw_card_text,
        ]
    ).lower()
    signals: set[str] = set()
    for label, patterns in POSITIVE_BADGE_PATTERNS.items():
        if any(pattern.lower() in haystack for pattern in patterns):
            signals.add(label)
    return signals


def detect_ip_risks(candidate: Candidate) -> list[str]:
    text = " ".join([candidate.title, candidate.ip_risk_flags, candidate.raw_card_text]).lower()
    return sorted({term for term in IP_RISK_TERMS if term in text})


def is_search_stage_promising(
    *,
    candidate: Candidate,
    total: int,
    category_fit: float,
    moq: float | None,
    repurchase: float | None,
    monthly_sales: float | None,
) -> bool:
    """Search pages rarely expose full supplier evidence; keep good leads alive."""
    if total < 52:
        return False
    if category_fit < 3.5:
        return False
    if not candidate.image_url:
        return False
    if moq is not None and moq > 3:
        return False
    if repurchase is not None and repurchase >= 25:
        return True
    if monthly_sales is not None and monthly_sales >= 50:
        return True
    return False


def score_candidate(
    candidate: Candidate,
    review_stage: str = "search",
    rejected_keys: set[str] | None = None,
) -> Candidate:
    review_stage = "detail" if review_stage == "detail" else "search"
    rejected_keys = rejected_keys or set()
    signals = detect_signals(candidate)
    ip_risks = detect_ip_risks(candidate)
    positive: list[str] = []
    concerns: list[str] = []
    hard_reject_reasons: list[str] = []
    caps: list[str] = []

    size_chart = yes_no_unknown(candidate.size_chart)
    dropship = yes_no_unknown(candidate.dropship_supported)
    moq = number(candidate.moq)
    years = number(candidate.years_on_1688)
    monthly_sales = number(candidate.monthly_sales)
    repurchase = percent(candidate.repurchase_rate_pct)
    rating = number(candidate.rating)
    category_fit = score_0_to_5(candidate.category_match, 3.0)
    style_fit = score_0_to_5(candidate.style_fit, 3.0)
    image_quality = score_0_to_5(candidate.image_quality, 3.0 if candidate.image_url else 1.0)

    if offer_key(candidate.product_url) in rejected_keys:
        hard_reject_reasons.append("previously rejected by operator")
    if not candidate.product_url:
        hard_reject_reasons.append("missing product URL")
    if category_fit <= 1:
        hard_reject_reasons.append("poor fit for Dress Like Mommy categories")
    if size_chart is False:
        hard_reject_reasons.append("no vendor size chart evidence")
    if moq is not None and moq > 10:
        hard_reject_reasons.append(f"MOQ too high for dropshipping ({moq:g})")
    elif moq is not None and moq > 3:
        caps.append(f"MOQ needs review ({moq:g})")
    if dropship is False and (moq is None or moq > 1):
        hard_reject_reasons.append("not one-piece/dropship friendly")
    if ip_risks:
        hard_reject_reasons.append("possible IP/brand risk")

    if not candidate.image_url:
        caps.append("missing product image URL")
    if size_chart is None:
        caps.append("size chart not confirmed")
    if dropship is None and (moq is None or moq > 1):
        caps.append("dropship support not confirmed")

    fit_score = 0.0
    fit_score += (category_fit / 5) * 8
    fit_score += (style_fit / 5) * 6
    fit_score += (image_quality / 5) * 5
    if size_chart is True:
        fit_score += 6
        positive.append("size chart confirmed")
    elif size_chart is None:
        fit_score += 2
        concerns.append("size chart still needs confirmation")
    else:
        concerns.append("size chart missing")

    reliability_score = 0.0
    if years is None:
        reliability_score += 2
        concerns.append("supplier operating years missing")
    elif years >= 5:
        reliability_score += 6
        positive.append(f"{years:g}+ years on 1688")
    elif years >= 3:
        reliability_score += 4.5
        positive.append(f"{years:g} years on 1688")
    elif years >= 1:
        reliability_score += 2
        concerns.append(f"newer supplier ({years:g} years)")
    else:
        concerns.append("very new supplier")

    badge_score = 0.0
    badge_weights = {
        "超级工厂": 4,
        "实力商家": 3,
        "深度验厂": 3,
        "真实工厂": 2,
        "买家保障": 2,
        "品质保障": 2,
    }
    for signal, points in badge_weights.items():
        if signal in signals:
            badge_score += points
            positive.append(signal)
    reliability_score += min(12, badge_score)

    if repurchase is None:
        reliability_score += 1.5
        concerns.append("repeat-buyer rate missing")
    elif repurchase >= 40:
        reliability_score += 5
        positive.append(f"strong repeat-buyer signal ({repurchase:g}%)")
    elif repurchase >= 25:
        reliability_score += 3.5
        positive.append(f"healthy repeat-buyer signal ({repurchase:g}%)")
    elif repurchase >= 10:
        reliability_score += 2
        concerns.append(f"modest repeat-buyer signal ({repurchase:g}%)")
    else:
        concerns.append(f"low repeat-buyer signal ({repurchase:g}%)")

    if rating is None:
        reliability_score += 1
        concerns.append("shop/service rating missing")
    elif rating >= 4.8:
        reliability_score += 4
        positive.append(f"high shop/service rating ({rating:g})")
    elif rating >= 4.6:
        reliability_score += 2.5
    else:
        concerns.append(f"weak shop/service rating ({rating:g})")

    if monthly_sales is None:
        reliability_score += 1
        concerns.append("recent sales/order volume missing")
    elif monthly_sales >= 200:
        reliability_score += 3
        positive.append(f"strong recent sales volume ({monthly_sales:g})")
    elif monthly_sales >= 50:
        reliability_score += 2
    elif monthly_sales > 0:
        reliability_score += 1
        concerns.append(f"low recent sales volume ({monthly_sales:g})")

    fulfillment_score = 0.0
    if "24小时发货" in signals:
        fulfillment_score += 8
        positive.append("24h dispatch signal")
    elif "48小时发货" in signals:
        fulfillment_score += 7
        positive.append("48h dispatch signal")
    elif "现货" in signals:
        fulfillment_score += 4
        positive.append("ready-stock signal")
    else:
        fulfillment_score += 2
        concerns.append("fast dispatch signal missing")

    if dropship is True or "一件代发" in signals:
        fulfillment_score += 6
        positive.append("one-piece/dropship signal")
    elif dropship is None:
        fulfillment_score += 2
        concerns.append("one-piece/dropship support unknown")
    else:
        concerns.append("not dropship friendly")

    if moq is None:
        fulfillment_score += 2
        concerns.append("MOQ missing")
    elif moq <= 1:
        fulfillment_score += 5
        positive.append("MOQ 1")
    elif moq <= 3:
        fulfillment_score += 3
        concerns.append(f"small but non-ideal MOQ ({moq:g})")
    else:
        fulfillment_score += 1
        concerns.append(f"MOQ {moq:g}")

    if "官方物流" in signals:
        fulfillment_score += 3
        positive.append("official logistics signal")

    raw_response = " ".join([candidate.service_flags, candidate.raw_card_text]).lower()
    if "响应" in raw_response or "response" in raw_response:
        fulfillment_score += 2
    elif rating is not None and rating >= 4.8:
        fulfillment_score += 2
    else:
        fulfillment_score += 1

    readiness_score = 0.0
    if ip_risks:
        concerns.append("possible IP/brand terms: " + ", ".join(ip_risks[:6]))
    else:
        readiness_score += 6
        positive.append("no obvious IP-risk terms")

    if "买家保障" in signals or "品质保障" in signals:
        readiness_score += 4
    elif "包换" in signals:
        readiness_score += 3
    else:
        readiness_score += 1
        concerns.append("buyer/quality protection signal missing")

    if "现货" in signals:
        readiness_score += 4
    else:
        readiness_score += 1.5

    populated = sum(
        1
        for value in [
            candidate.product_url,
            candidate.image_url,
            candidate.title,
            candidate.vendor_name,
            candidate.price_cny,
            candidate.moq,
            candidate.badges or candidate.service_flags,
            candidate.size_chart,
            candidate.dropship_supported,
        ]
        if clean(value)
    )
    readiness_score += min(6, populated / 9 * 6)
    if populated < 6:
        concerns.append("candidate data is thin")

    fit_score = min(25, fit_score)
    reliability_score = min(30, reliability_score)
    fulfillment_score = min(25, fulfillment_score)
    readiness_score = min(20, readiness_score)
    total = round(fit_score + reliability_score + fulfillment_score + readiness_score)

    search_promising = is_search_stage_promising(
        candidate=candidate,
        total=total,
        category_fit=category_fit,
        moq=moq,
        repurchase=repurchase,
        monthly_sales=monthly_sales,
    )

    if hard_reject_reasons:
        verdict = "Reject"
    elif review_stage == "detail" and total >= 78 and not caps:
        verdict = "Gold"
    elif total >= 58 or (review_stage == "search" and search_promising):
        verdict = "Test"
    else:
        verdict = "Reject"

    if caps and verdict == "Gold":
        verdict = "Test"

    for reason in hard_reject_reasons:
        concerns.insert(0, reason)
    for reason in caps:
        concerns.append(reason)

    if verdict == "Gold":
        next_action = "Move to listing intake: save size-chart screenshot, collect product images, then use the canonical LISTING REQUEST."
    elif verdict == "Test":
        if review_stage == "search":
            next_action = "Open the product detail page, confirm size chart, one-piece shipping, dispatch speed, and supplier proof before listing."
        else:
            next_action = "Verify missing supplier evidence first: size chart, one-piece shipping, dispatch speed, and product photos before listing."
    else:
        next_action = "Do not list from this candidate unless the reject reason changes with better evidence."

    candidate.score = int(total)
    candidate.verdict = verdict
    candidate.breakdown = {
        "product_fit": round(fit_score, 1),
        "vendor_reliability": round(reliability_score, 1),
        "fulfillment": round(fulfillment_score, 1),
        "risk_readiness": round(readiness_score, 1),
    }
    candidate.positive_signals = dedupe(positive)
    candidate.concerns = dedupe(concerns)
    candidate.next_action = next_action
    candidate.listing_request = build_listing_request(candidate)
    candidate.review_stage = review_stage
    return candidate


def dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        clean_value = clean(value)
        key = clean_value.lower()
        if clean_value and key not in seen:
            seen.add(key)
            result.append(clean_value)
    return result


def build_listing_request(candidate: Candidate) -> str:
    return "\n".join(
        [
            "LISTING REQUEST",
            "",
            f"VENDOR_URL: {candidate.product_url}",
            "SIZE_CHART_SOURCE: attached image",
            "LISTING_MODE: Family Matching",
            "PRIMARY_CATEGORY: auto",
            "DESIGNS_TO_LIST: auto",
            "EXCLUDE_ITEMS:",
            f"NOTES: Sourcing verdict {candidate.verdict}; score {candidate.score}. Confirmed from sourcing report: {candidate.title}",
            "PRICE_OVERRIDES:",
            "SHORTCODE_OVERRIDE:",
            "COLOR_TOKEN_OVERRIDE:",
            "FORCE_SPEC_PRICES: true",
        ]
    )


def candidate_from_row(row: dict[str, Any], index: int) -> Candidate:
    return Candidate(
        candidate_id=clean(row.get("candidate_id")) or stable_id(row, index),
        product_url=first_value(row, "product_url"),
        image_url=first_value(row, "image_url"),
        title=first_value(row, "title"),
        vendor_name=first_value(row, "vendor_name"),
        vendor_url=first_value(row, "vendor_url"),
        vendor_location=first_value(row, "vendor_location"),
        price_cny=first_value(row, "price_cny"),
        moq=first_value(row, "moq"),
        monthly_sales=first_value(row, "monthly_sales"),
        repurchase_rate_pct=first_value(row, "repurchase_rate_pct"),
        rating=first_value(row, "rating"),
        years_on_1688=first_value(row, "years_on_1688"),
        badges=first_value(row, "badges"),
        service_flags=first_value(row, "service_flags"),
        dropship_supported=first_value(row, "dropship_supported"),
        size_chart=first_value(row, "size_chart"),
        category_match=first_value(row, "category_match"),
        style_fit=first_value(row, "style_fit"),
        image_quality=first_value(row, "image_quality"),
        ip_risk_flags=first_value(row, "ip_risk_flags"),
        raw_card_text=first_value(row, "raw_card_text"),
        notes=first_value(row, "notes"),
    )


def dedupe_candidates(candidates: list[Candidate]) -> list[Candidate]:
    seen: set[str] = set()
    result: list[Candidate] = []
    for candidate in candidates:
        key = candidate.product_url or candidate.title or candidate.candidate_id
        key = key.lower().strip()
        if key in seen:
            continue
        seen.add(key)
        result.append(candidate)
    return result


def write_csv(path: Path, candidates: list[Candidate]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDNAMES)
        writer.writeheader()
        for candidate in candidates:
            writer.writerow(
                {
                    "candidate_id": candidate.candidate_id,
                    "review_stage": candidate.review_stage,
                    "verdict": candidate.verdict,
                    "score": candidate.score,
                    "product_url": candidate.product_url,
                    "image_url": candidate.image_url,
                    "title": candidate.title,
                    "vendor_name": candidate.vendor_name,
                    "vendor_url": candidate.vendor_url,
                    "vendor_location": candidate.vendor_location,
                    "price_cny": candidate.price_cny,
                    "moq": candidate.moq,
                    "monthly_sales": candidate.monthly_sales,
                    "repurchase_rate_pct": candidate.repurchase_rate_pct,
                    "rating": candidate.rating,
                    "years_on_1688": candidate.years_on_1688,
                    "badges": candidate.badges,
                    "service_flags": candidate.service_flags,
                    "dropship_supported": candidate.dropship_supported,
                    "size_chart": candidate.size_chart,
                    "category_match": candidate.category_match,
                    "style_fit": candidate.style_fit,
                    "image_quality": candidate.image_quality,
                    "ip_risk_flags": candidate.ip_risk_flags,
                    "positive_signals": " | ".join(candidate.positive_signals),
                    "concerns": " | ".join(candidate.concerns),
                    "next_action": candidate.next_action,
                    "raw_card_text": candidate.raw_card_text,
                    "notes": candidate.notes,
                }
            )


def candidate_to_dict(candidate: Candidate) -> dict[str, Any]:
    return {
        "candidate_id": candidate.candidate_id,
        "review_stage": candidate.review_stage,
        "verdict": candidate.verdict,
        "score": candidate.score,
        "breakdown": candidate.breakdown,
        "product_url": candidate.product_url,
        "image_url": candidate.image_url,
        "title": candidate.title,
        "vendor_name": candidate.vendor_name,
        "vendor_url": candidate.vendor_url,
        "vendor_location": candidate.vendor_location,
        "price_cny": candidate.price_cny,
        "moq": candidate.moq,
        "monthly_sales": candidate.monthly_sales,
        "repurchase_rate_pct": candidate.repurchase_rate_pct,
        "rating": candidate.rating,
        "years_on_1688": candidate.years_on_1688,
        "badges": candidate.badges,
        "service_flags": candidate.service_flags,
        "dropship_supported": candidate.dropship_supported,
        "size_chart": candidate.size_chart,
        "category_match": candidate.category_match,
        "style_fit": candidate.style_fit,
        "image_quality": candidate.image_quality,
        "ip_risk_flags": candidate.ip_risk_flags,
        "positive_signals": candidate.positive_signals,
        "concerns": candidate.concerns,
        "next_action": candidate.next_action,
        "listing_request": candidate.listing_request,
        "raw_card_text": candidate.raw_card_text,
        "notes": candidate.notes,
    }


def write_json(path: Path, candidates: list[Candidate], source: str) -> None:
    payload = {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "source": source,
        "candidates": [candidate_to_dict(candidate) for candidate in candidates],
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def pill(text: str, kind: str = "") -> str:
    cls = "pill" + (f" pill-{kind}" if kind else "")
    return f'<span class="{cls}">{html.escape(text)}</span>'


def split_list(value: str) -> list[str]:
    return [clean(part) for part in re.split(r"[|,;，、]+", value or "") if clean(part)]


def metric(label: str, value: str) -> str:
    safe_value = html.escape(value or "—")
    return f"<div class=\"metric\"><span>{html.escape(label)}</span><strong>{safe_value}</strong></div>"


def status_note(candidate: Candidate) -> str:
    if candidate.verdict == "Gold":
        return "Ready for listing intake after the size chart and images are saved."
    if candidate.verdict == "Test":
        return "Promising lead. Open 1688 and verify the missing proof before listing."
    return "Skip unless new evidence fixes the concern."


def render_candidate_card(candidate: Candidate) -> str:
    badge_texts = split_list(candidate.badges) + split_list(candidate.service_flags)
    signal_pills = "".join(pill(value) for value in badge_texts[:8])
    positive = "".join(f"<li>{html.escape(value)}</li>" for value in candidate.positive_signals[:6])
    concerns = "".join(f"<li>{html.escape(value)}</li>" for value in candidate.concerns[:7])
    if not positive:
        positive = "<li>No strong positive signal captured yet.</li>"
    if not concerns:
        concerns = "<li>No major concern captured.</li>"

    score_pct = max(0, min(candidate.score, 100))
    img = html.escape(candidate.image_url)
    title = html.escape(candidate.title or "Untitled 1688 candidate")
    product_url = html.escape(candidate.product_url)
    vendor_url = html.escape(candidate.vendor_url)
    listing_request = html.escape(candidate.listing_request)
    raw_text = html.escape(candidate.raw_card_text)
    verdict_class = candidate.verdict.lower()
    status = html.escape(status_note(candidate))

    return f"""
    <article class="card" data-id="{html.escape(candidate.candidate_id)}" data-verdict="{html.escape(candidate.verdict)}" data-score="{candidate.score}" data-search="{html.escape((candidate.title + ' ' + candidate.vendor_name + ' ' + candidate.badges + ' ' + candidate.service_flags).lower())}">
      <div class="image-wrap">
        {'<img loading="lazy" src="' + img + '" alt="' + title + '">' if candidate.image_url else '<div class="image-missing">No image URL</div>'}
        <div class="verdict verdict-{verdict_class}">{html.escape(candidate.verdict)}</div>
      </div>
      <div class="card-body">
        <div class="decision-row">
          <button class="decision keep" type="button" title="Select this product for detail review">Keep</button>
          <button class="decision hide-card" type="button" title="Hide this product from the active shortlist">Hide</button>
        </div>
        <div class="score-row">
          <div>
            <div class="candidate-id">{html.escape(candidate.candidate_id)}</div>
            <h2>{title}</h2>
          </div>
          <div class="score">{candidate.score}</div>
        </div>
        <div class="score-bar" aria-label="Score {candidate.score} out of 100"><span style="width:{score_pct}%"></span></div>
        <p class="status-note">{status}</p>
        <div class="vendor-line">{html.escape(candidate.vendor_name or 'Supplier not captured')}{' · ' + html.escape(candidate.vendor_location) if candidate.vendor_location else ''}</div>
        <div class="metrics">
          {metric('Price CNY', candidate.price_cny)}
          {metric('MOQ', candidate.moq)}
          {metric('Sales', candidate.monthly_sales)}
          {metric('Repeat', candidate.repurchase_rate_pct)}
          {metric('Rating', candidate.rating)}
          {metric('Years', candidate.years_on_1688)}
        </div>
        <div class="pill-row">{signal_pills or pill('No badge text captured', 'muted')}</div>
        <div class="breakdown">
          {metric('Fit', str(candidate.breakdown.get('product_fit', 0)))}
          {metric('Supplier', str(candidate.breakdown.get('vendor_reliability', 0)))}
          {metric('Fulfillment', str(candidate.breakdown.get('fulfillment', 0)))}
          {metric('Risk', str(candidate.breakdown.get('risk_readiness', 0)))}
        </div>
        <div class="why">
          <section>
            <h3>Signals</h3>
            <ul>{positive}</ul>
          </section>
          <section>
            <h3>Concerns</h3>
            <ul>{concerns}</ul>
          </section>
        </div>
        <p class="next"><strong>Next:</strong> {html.escape(candidate.next_action)}</p>
        <div class="actions">
          {'<a class="button" href="' + product_url + '" target="_blank" rel="noreferrer" title="Open the 1688 product detail page">Open 1688</a>' if candidate.product_url else ''}
          {'<a class="button secondary" href="' + vendor_url + '" target="_blank" rel="noreferrer" title="Open the supplier shop page">Supplier</a>' if candidate.vendor_url else ''}
          <button class="button secondary copy" type="button" data-copy="{listing_request}" title="Copy the canonical prompt block for the listing agent">Copy request</button>
        </div>
        {'<details><summary>Raw captured text</summary><p>' + raw_text + '</p></details>' if raw_text else ''}
      </div>
    </article>
    """


def write_html(path: Path, candidates: list[Candidate], source: str) -> None:
    counts = {verdict: sum(1 for c in candidates if c.verdict == verdict) for verdict in ("Gold", "Test", "Reject")}
    average = round(sum(c.score for c in candidates) / len(candidates), 1) if candidates else 0
    cards = "\n".join(render_candidate_card(candidate) for candidate in candidates)
    generated = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    data_json = (
        json.dumps([candidate_to_dict(c) for c in candidates], ensure_ascii=False)
        .replace("&", "\\u0026")
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
    )

    document = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>1688 Sourcing Shortlist</title>
  <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='12' fill='%23c45d45'/%3E%3Cpath d='M17 36h30M22 25h20M26 47h12' stroke='white' stroke-width='6' stroke-linecap='round'/%3E%3C/svg%3E">
  <style>
    :root {{
      --bg: #f5f7f6;
      --ink: #1f2523;
      --muted: #68716b;
      --line: #d8ded9;
      --panel: #ffffff;
      --gold: #b98513;
      --gold-bg: #fff3ce;
      --test: #287d7d;
      --test-bg: #dff4f1;
      --reject: #a6423b;
      --reject-bg: #ffe3df;
      --accent: #c45d45;
      --selected: #2f6f5e;
      --selected-bg: #e3f3ec;
      --hidden-bg: #edf0ef;
      --shadow: 0 18px 45px rgba(31, 37, 35, .10);
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: var(--bg);
      color: var(--ink);
    }}
    header {{
      padding: 28px clamp(18px, 4vw, 46px) 18px;
      background: linear-gradient(180deg, #fbfdfb 0%, #f5f7f6 100%);
      border-bottom: 1px solid var(--line);
    }}
    .topline {{
      display: flex;
      gap: 18px;
      align-items: end;
      justify-content: space-between;
      flex-wrap: wrap;
    }}
    h1 {{
      margin: 0;
      font-size: clamp(26px, 3vw, 42px);
      line-height: 1.05;
      letter-spacing: 0;
    }}
    .subtitle {{
      margin: 10px 0 0;
      color: var(--muted);
      max-width: 920px;
      line-height: 1.45;
    }}
    .summary {{
      display: grid;
      grid-template-columns: repeat(7, minmax(110px, 1fr));
      gap: 10px;
      margin-top: 22px;
    }}
    .summary-card {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 14px;
    }}
    .summary-card span, .metric span {{
      display: block;
      color: var(--muted);
      font-size: 12px;
      line-height: 1.2;
    }}
    .summary-card strong {{
      display: block;
      margin-top: 5px;
      font-size: 24px;
    }}
    .legend {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-top: 14px;
    }}
    .status-chip {{
      display: inline-flex;
      align-items: center;
      min-height: 30px;
      padding: 5px 10px;
      border: 1px solid var(--line);
      border-radius: 999px;
      background: var(--panel);
      color: var(--muted);
      font-size: 13px;
    }}
    .status-chip strong {{
      margin-right: 5px;
      color: var(--ink);
    }}
    .toolbar {{
      position: sticky;
      top: 0;
      z-index: 5;
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      align-items: center;
      padding: 14px clamp(18px, 4vw, 46px);
      background: rgba(245, 247, 246, .94);
      border-bottom: 1px solid var(--line);
      backdrop-filter: blur(12px);
    }}
    input, select, button, .button {{
      min-height: 40px;
      border-radius: 8px;
      border: 1px solid var(--line);
      font: inherit;
    }}
    input {{
      flex: 1 1 300px;
      min-width: 220px;
      padding: 0 12px;
      background: #fff;
      color: var(--ink);
    }}
    select {{
      padding: 0 12px;
      background: #fff;
      color: var(--ink);
    }}
    .filter {{
      padding: 0 13px;
      background: #fff;
      color: var(--ink);
      cursor: pointer;
    }}
    .filter.active {{
      border-color: var(--accent);
      color: #7b301f;
      background: #fff1ec;
    }}
    .toolbar-action {{
      padding: 0 13px;
      background: var(--ink);
      color: #fff;
      border-color: var(--ink);
      cursor: pointer;
      font-weight: 750;
    }}
    .toolbar-action.secondary {{
      background: #fff;
      color: var(--ink);
      border-color: var(--line);
    }}
    main {{
      padding: 24px clamp(18px, 4vw, 46px) 52px;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(330px, 1fr));
      gap: 18px;
      align-items: start;
    }}
    .card {{
      overflow: hidden;
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      box-shadow: var(--shadow);
    }}
    .card.selected {{
      border-color: var(--selected);
      box-shadow: 0 0 0 3px rgba(47, 111, 94, .16), var(--shadow);
    }}
    .card.user-hidden {{
      opacity: .58;
      background: var(--hidden-bg);
    }}
    .image-wrap {{
      position: relative;
      aspect-ratio: 4 / 3;
      background: #e7ece9;
      overflow: hidden;
    }}
    .image-wrap img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
    }}
    .image-missing {{
      height: 100%;
      display: grid;
      place-items: center;
      color: var(--muted);
      font-weight: 700;
    }}
    .verdict {{
      position: absolute;
      top: 12px;
      left: 12px;
      padding: 7px 11px;
      border-radius: 999px;
      font-size: 12px;
      font-weight: 800;
      letter-spacing: 0;
      border: 1px solid rgba(255,255,255,.7);
    }}
    .verdict-gold {{ background: var(--gold-bg); color: #6f4d07; }}
    .verdict-test {{ background: var(--test-bg); color: #135b5a; }}
    .verdict-reject {{ background: var(--reject-bg); color: #7a211b; }}
    .card-body {{ padding: 16px; }}
    .decision-row {{
      display: flex;
      gap: 8px;
      margin-bottom: 12px;
    }}
    .decision {{
      min-height: 36px;
      padding: 0 12px;
      cursor: pointer;
      font-weight: 800;
      background: #fff;
    }}
    .decision.keep {{
      color: var(--selected);
      border-color: #a9ccb9;
    }}
    .card.selected .decision.keep {{
      background: var(--selected-bg);
      border-color: var(--selected);
    }}
    .decision.hide-card {{
      color: #7a211b;
      border-color: #e5b8b1;
    }}
    .card.user-hidden .decision.hide-card {{
      background: var(--reject-bg);
      border-color: var(--reject);
    }}
    .score-row {{
      display: flex;
      gap: 12px;
      justify-content: space-between;
      align-items: start;
    }}
    .candidate-id {{
      color: var(--muted);
      font-size: 12px;
      margin-bottom: 4px;
    }}
    h2 {{
      margin: 0;
      font-size: 18px;
      line-height: 1.25;
      letter-spacing: 0;
    }}
    .score {{
      min-width: 54px;
      text-align: center;
      font-size: 28px;
      font-weight: 850;
      line-height: 1;
      color: var(--accent);
    }}
    .score-bar {{
      height: 8px;
      margin: 13px 0 10px;
      background: #e4e9e6;
      border-radius: 999px;
      overflow: hidden;
    }}
    .score-bar span {{
      display: block;
      height: 100%;
      background: linear-gradient(90deg, var(--accent), var(--test));
    }}
    .vendor-line {{
      color: var(--muted);
      font-size: 13px;
      min-height: 20px;
    }}
    .status-note {{
      margin: 0 0 10px;
      color: #39413d;
      font-size: 13px;
      line-height: 1.4;
    }}
    .metrics, .breakdown {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 8px;
      margin-top: 13px;
    }}
    .breakdown {{ grid-template-columns: repeat(4, 1fr); }}
    .metric {{
      padding: 9px;
      background: #f7faf8;
      border: 1px solid #e2e8e4;
      border-radius: 8px;
      min-width: 0;
    }}
    .metric strong {{
      display: block;
      margin-top: 3px;
      font-size: 14px;
      overflow-wrap: anywhere;
    }}
    .pill-row {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin-top: 12px;
    }}
    .pill {{
      display: inline-flex;
      align-items: center;
      max-width: 100%;
      min-height: 26px;
      padding: 4px 8px;
      border-radius: 999px;
      background: #edf5ef;
      color: #2d6040;
      font-size: 12px;
      overflow-wrap: anywhere;
    }}
    .pill-muted {{ background: #e9eeeb; color: var(--muted); }}
    .why {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
      margin-top: 14px;
    }}
    h3 {{
      margin: 0 0 7px;
      font-size: 13px;
      letter-spacing: 0;
    }}
    ul {{
      margin: 0;
      padding-left: 18px;
      color: var(--muted);
      font-size: 13px;
      line-height: 1.45;
    }}
    .next {{
      margin: 14px 0 0;
      color: #39413d;
      line-height: 1.45;
      font-size: 14px;
    }}
    .actions {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-top: 14px;
    }}
    .button {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      padding: 0 12px;
      background: var(--ink);
      color: #fff;
      text-decoration: none;
      cursor: pointer;
      border-color: var(--ink);
      font-weight: 750;
    }}
    .button.secondary {{
      background: #fff;
      color: var(--ink);
      border-color: var(--line);
    }}
    details {{
      margin-top: 12px;
      border-top: 1px solid var(--line);
      padding-top: 10px;
      color: var(--muted);
      font-size: 13px;
    }}
    summary {{ cursor: pointer; color: var(--ink); font-weight: 700; }}
    details p {{ overflow-wrap: anywhere; line-height: 1.45; }}
    .hidden {{ display: none !important; }}
    @media (max-width: 760px) {{
      .summary {{ grid-template-columns: repeat(2, 1fr); }}
      .grid {{ grid-template-columns: 1fr; }}
      .why {{ grid-template-columns: 1fr; }}
      .breakdown {{ grid-template-columns: repeat(2, 1fr); }}
    }}
  </style>
</head>
<body>
  <header>
    <div class="topline">
      <div>
        <h1>1688 Sourcing Shortlist</h1>
        <p class="subtitle">Browser-assisted candidate review for Dress Like Mommy. This report shows product images, source URLs, supplier evidence, score reasons, and the next action before anything enters Shopify.</p>
      </div>
      <div class="candidate-id">Generated {html.escape(generated)}<br>Source: {html.escape(source)}</div>
    </div>
    <div class="summary">
      <div class="summary-card"><span>Total</span><strong>{len(candidates)}</strong></div>
      <div class="summary-card"><span>Gold</span><strong>{counts['Gold']}</strong></div>
      <div class="summary-card"><span>Test</span><strong>{counts['Test']}</strong></div>
      <div class="summary-card"><span>Reject</span><strong>{counts['Reject']}</strong></div>
      <div class="summary-card"><span>Kept</span><strong id="selected-count">0</strong></div>
      <div class="summary-card"><span>Hidden</span><strong id="hidden-count">0</strong></div>
      <div class="summary-card"><span>Avg Score</span><strong>{average}</strong></div>
    </div>
    <div class="legend" aria-label="Verdict meaning">
      <div class="status-chip"><strong>Gold</strong> verified enough for listing intake</div>
      <div class="status-chip"><strong>Test</strong> promising, needs detail-page proof</div>
      <div class="status-chip"><strong>Reject</strong> skip unless evidence changes</div>
    </div>
  </header>
  <div class="toolbar">
    <input id="search" type="search" placeholder="Search title, supplier, badge, service flag">
    <button class="filter active" data-filter="All">All</button>
    <button class="filter" data-filter="Selected">Kept</button>
    <button class="filter" data-filter="Hidden">Hidden</button>
    <button class="filter" data-filter="Gold">Gold</button>
    <button class="filter" data-filter="Test">Test</button>
    <button class="filter" data-filter="Reject">Reject</button>
    <select id="sort">
      <option value="default">Sort by verdict</option>
      <option value="score-desc">Score high to low</option>
      <option value="score-asc">Score low to high</option>
    </select>
    <button id="copy-selected" class="toolbar-action" type="button">Copy kept URLs</button>
    <button id="download-selected" class="toolbar-action secondary" type="button">Download kept JSON</button>
    <button id="reset-choices" class="toolbar-action secondary" type="button">Reset choices</button>
  </div>
  <main>
    <div class="grid" id="grid">
      {cards}
    </div>
  </main>
  <script id="candidate-data" type="application/json">{data_json}</script>
  <script>
    const grid = document.querySelector('#grid');
    const cards = Array.from(document.querySelectorAll('.card'));
    const search = document.querySelector('#search');
    const sort = document.querySelector('#sort');
    const selectedCount = document.querySelector('#selected-count');
    const hiddenCount = document.querySelector('#hidden-count');
    const copySelected = document.querySelector('#copy-selected');
    const downloadSelected = document.querySelector('#download-selected');
    const resetChoices = document.querySelector('#reset-choices');
    const candidateData = JSON.parse(document.querySelector('#candidate-data').textContent);
    const candidateById = new Map(candidateData.map(item => [item.candidate_id, item]));
    const storageKey = `dlm-1688-shortlist:${{location.pathname}}`;
    let activeFilter = 'All';
    let choices = loadChoices();

    function loadChoices() {{
      try {{
        return JSON.parse(localStorage.getItem(storageKey)) || {{}};
      }} catch {{
        return {{}};
      }}
    }}

    function saveChoices() {{
      localStorage.setItem(storageKey, JSON.stringify(choices));
    }}

    function cardChoice(card) {{
      return choices[card.dataset.id] || {{}};
    }}

    function setCardChoice(card, patch) {{
      const current = cardChoice(card);
      choices[card.dataset.id] = {{ ...current, ...patch }};
      if (!choices[card.dataset.id].selected && !choices[card.dataset.id].hidden) {{
        delete choices[card.dataset.id];
      }}
      saveChoices();
      syncChoiceUi();
      applyFilters();
    }}

    function selectedCards() {{
      return cards.filter(card => {{
        const choice = cardChoice(card);
        return choice.selected && !choice.hidden;
      }});
    }}

    function hiddenCards() {{
      return cards.filter(card => cardChoice(card).hidden);
    }}

    function syncChoiceUi() {{
      cards.forEach(card => {{
        const choice = cardChoice(card);
        const keep = card.querySelector('.keep');
        const hide = card.querySelector('.hide-card');
        card.classList.toggle('selected', Boolean(choice.selected));
        card.classList.toggle('user-hidden', Boolean(choice.hidden));
        keep.textContent = choice.selected ? 'Kept' : 'Keep';
        hide.textContent = choice.hidden ? 'Restore' : 'Hide';
      }});
      selectedCount.textContent = String(selectedCards().length);
      hiddenCount.textContent = String(hiddenCards().length);
    }}

    function applyFilters() {{
      const term = search.value.trim().toLowerCase();
      cards.forEach(card => {{
        const choice = cardChoice(card);
        let verdictMatch = false;
        if (activeFilter === 'All') {{
          verdictMatch = !choice.hidden;
        }} else if (activeFilter === 'Selected') {{
          verdictMatch = choice.selected && !choice.hidden;
        }} else if (activeFilter === 'Hidden') {{
          verdictMatch = choice.hidden;
        }} else {{
          verdictMatch = card.dataset.verdict === activeFilter && !choice.hidden;
        }}
        const searchMatch = !term || card.dataset.search.includes(term);
        card.classList.toggle('hidden', !(verdictMatch && searchMatch));
      }});
    }}

    function applySort() {{
      const mode = sort.value;
      const order = {{ Gold: 0, Test: 1, Reject: 2 }};
      const sorted = [...cards].sort((a, b) => {{
        if (mode === 'score-desc') return Number(b.dataset.score) - Number(a.dataset.score);
        if (mode === 'score-asc') return Number(a.dataset.score) - Number(b.dataset.score);
        return order[a.dataset.verdict] - order[b.dataset.verdict] || Number(b.dataset.score) - Number(a.dataset.score);
      }});
      sorted.forEach(card => grid.appendChild(card));
    }}

    function downloadJson(filename, items) {{
      const blob = new Blob([JSON.stringify(items, null, 2)], {{ type: 'application/json' }});
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      link.remove();
      URL.revokeObjectURL(url);
    }}

    function flash(button, text) {{
      const old = button.textContent;
      button.textContent = text;
      setTimeout(() => button.textContent = old, 1200);
    }}

    document.querySelectorAll('.filter').forEach(button => {{
      button.addEventListener('click', () => {{
        document.querySelectorAll('.filter').forEach(item => item.classList.remove('active'));
        button.classList.add('active');
        activeFilter = button.dataset.filter;
        applyFilters();
      }});
    }});
    search.addEventListener('input', applyFilters);
    sort.addEventListener('change', () => {{ applySort(); applyFilters(); }});

    async function copyText(text) {{
      if (navigator.clipboard?.writeText && window.isSecureContext) {{
        try {{
          await navigator.clipboard.writeText(text);
          return;
        }} catch {{
        }}
      }}
      const area = document.createElement('textarea');
      area.value = text;
      area.setAttribute('readonly', '');
      area.style.position = 'fixed';
      area.style.left = '-9999px';
      document.body.appendChild(area);
      area.select();
      document.execCommand('copy');
      area.remove();
    }}

    document.querySelectorAll('.copy').forEach(button => {{
      button.addEventListener('click', async () => {{
        try {{
          await copyText(button.dataset.copy);
          flash(button, 'Copied');
        }} catch {{
          flash(button, 'Copy failed');
        }}
      }});
    }});

    document.querySelectorAll('.keep').forEach(button => {{
      button.addEventListener('click', () => {{
        const card = button.closest('.card');
        const choice = cardChoice(card);
        setCardChoice(card, {{ selected: !choice.selected, hidden: false }});
      }});
    }});

    document.querySelectorAll('.hide-card').forEach(button => {{
      button.addEventListener('click', () => {{
        const card = button.closest('.card');
        const choice = cardChoice(card);
        setCardChoice(card, {{ hidden: !choice.hidden, selected: choice.hidden ? choice.selected : false }});
      }});
    }});

    copySelected.addEventListener('click', async () => {{
      const urls = selectedCards()
        .map(card => candidateById.get(card.dataset.id)?.product_url)
        .filter(Boolean);
      if (!urls.length) {{
        flash(copySelected, 'Keep products first');
        return;
      }}
      try {{
        await copyText(urls.join('\\n'));
        flash(copySelected, 'Copied URLs');
      }} catch {{
        flash(copySelected, 'Copy failed');
      }}
    }});

    downloadSelected.addEventListener('click', () => {{
      const items = selectedCards()
        .map(card => candidateById.get(card.dataset.id))
        .filter(Boolean);
      if (!items.length) {{
        flash(downloadSelected, 'Keep products first');
        return;
      }}
      downloadJson('1688-kept-candidates.json', items);
      flash(downloadSelected, 'Downloaded');
    }});

    resetChoices.addEventListener('click', () => {{
      choices = {{}};
      saveChoices();
      syncChoiceUi();
      applyFilters();
      flash(resetChoices, 'Reset');
    }});

    syncChoiceUi();
    applySort();
    applyFilters();
  </script>
</body>
</html>
"""
    clean_document = "\n".join(line.rstrip() for line in document.splitlines()) + "\n"
    path.write_text(clean_document, encoding="utf-8")


def write_summary(path: Path, candidates: list[Candidate], source: str) -> None:
    counts = {verdict: sum(1 for c in candidates if c.verdict == verdict) for verdict in ("Gold", "Test", "Reject")}
    lines = [
        "# 1688 Sourcing Shortlist Summary",
        "",
        f"- Source: `{source}`",
        f"- Generated: {dt.datetime.now().isoformat(timespec='seconds')}",
        f"- Candidates: {len(candidates)}",
        f"- Gold: {counts['Gold']}",
        f"- Test: {counts['Test']}",
        f"- Reject: {counts['Reject']}",
        "",
        "## Gold Candidates",
        "",
    ]
    gold = [candidate for candidate in candidates if candidate.verdict == "Gold"]
    if not gold:
        lines.append("- None yet.")
    else:
        for candidate in gold:
            lines.append(f"- {candidate.score} — [{candidate.title or candidate.product_url}]({candidate.product_url})")
    lines.extend(["", "## Immediate Review Queue", ""])
    for candidate in [c for c in candidates if c.verdict == "Test"][:10]:
        concern = "; ".join(candidate.concerns[:3])
        suffix = f": {concern}" if concern else ""
        lines.append(f"- {candidate.score} — {candidate.title or candidate.product_url}{suffix}")
    clean_summary = "\n".join(line.rstrip() for line in lines) + "\n"
    path.write_text(clean_summary, encoding="utf-8")


def run(
    input_path: Path,
    output_dir: Path,
    review_stage: str = "search",
    decision_state_path: Path | None = None,
) -> list[Path]:
    rows = load_rows(input_path)
    rejected_keys = load_rejected_keys(decision_state_path)
    candidates = [
        score_candidate(candidate_from_row(row, index), review_stage=review_stage, rejected_keys=rejected_keys)
        for index, row in enumerate(rows, start=1)
    ]
    candidates = dedupe_candidates(candidates)
    candidates.sort(key=lambda c: (VERDICT_ORDER.get(c.verdict, 99), -c.score, c.title.lower()))

    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / "scored-candidates.csv"
    json_path = output_dir / "scored-candidates.json"
    html_path = output_dir / "shortlist.html"
    summary_path = output_dir / "summary.md"
    write_csv(csv_path, candidates)
    write_json(json_path, candidates, str(input_path))
    write_html(html_path, candidates, str(input_path))
    write_summary(summary_path, candidates, str(input_path))
    return [html_path, csv_path, json_path, summary_path]


def main() -> None:
    parser = argparse.ArgumentParser(description="Score 1688 sourcing candidates and build a shortlist report.")
    parser.add_argument("--input", required=True, help="CSV or JSON candidate file gathered from a logged-in browser workflow.")
    parser.add_argument("--output-dir", default="", help="Output directory for report artifacts.")
    parser.add_argument(
        "--stage",
        choices=("search", "detail"),
        default="search",
        help="Use search for first-pass shortlist data, detail after each product page has been verified.",
    )
    parser.add_argument(
        "--decision-state",
        default="",
        help="Optional sourcing decisions JSON. Previously rejected offer IDs are scored as Reject.",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    if args.output_dir:
        output_dir = Path(args.output_dir)
    else:
        stamp = dt.datetime.now().strftime("%Y-%m-%d-%H%M")
        output_dir = DEFAULT_OUTPUT_ROOT / f"{stamp}-1688-sourcing-shortlist"

    decision_state_path = Path(args.decision_state) if args.decision_state else None
    paths = run(input_path, output_dir, review_stage=args.stage, decision_state_path=decision_state_path)
    for path in paths:
        print(path)


if __name__ == "__main__":
    main()
