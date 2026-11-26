"""Per-variant economics rows for ops/listings/<handle>-activation-packet.json.

One shared function for every packet builder, so the numbers written into a packet are
exactly the numbers ops/category-team/listing_quality_gate.validate re-derives:

  breakdown parts   each rounded to cents (USD)
  landed            sum of the rounded parts, rounded to cents (gate: |sum(parts) - landed| <= 0.02)
  deductions        fees, refunds, other, each rounded to cents
  net_margin        (price - landed - sum([fees, refunds, other])) / price, NOT rounded
                    (gate: |net_margin - derived| <= 0.000001, derived from the stored price/landed/deductions)

Computing net from unrounded landed or fees while storing rounded ones is what made packets
differ from the gate in the 4th decimal. Do not round net_margin and do not derive it from
anything but the stored rounded values.
"""
from __future__ import annotations

GATE_NET_TOLERANCE = 0.000001
GATE_BREAKDOWN_TOLERANCE = 0.02


def _cents(value: float) -> float:
    return round(float(value), 2)


def variant_economics(*, variant_key: str, price: float, cny_unit_cost: float, fx_cny_per_usd: float,
                      domestic_cny: float, freight_cny: float, services_cny: float, quote_as_of: str,
                      fee_rate: float = 0.029, fee_fixed: float = 0.30, refund_rate: float = 0.037,
                      other: float = 0.0, **extra) -> dict:
    """Return one packet economics row (the shape the gate reads). `extra` keys (size, color, ...) are kept."""
    price = float(price)
    if price <= 0 or fx_cny_per_usd <= 0:
        raise ValueError("price and fx must be positive")
    breakdown = {
        "product": _cents(cny_unit_cost / fx_cny_per_usd),
        "domestic": _cents(domestic_cny / fx_cny_per_usd),
        "freight": _cents(freight_cny / fx_cny_per_usd),
        "services": _cents(services_cny / fx_cny_per_usd),
    }
    landed = _cents(sum(breakdown.values()))
    deductions = {"fees": _cents(fee_rate * price + fee_fixed), "refunds": _cents(refund_rate * price), "other": _cents(other)}
    net = (price - landed - sum([deductions["fees"], deductions["refunds"], deductions["other"]])) / price
    row = {"variant_key": variant_key, **extra, "cny_unit_cost": cny_unit_cost, "price": price, "landed": landed,
           "net_margin": net, "breakdown": breakdown, "deductions": deductions, "quote_as_of": quote_as_of,
           "landed_pct_of_price": _cents(landed / price * 100)}
    check_gate_consistency(row)
    return row


def check_gate_consistency(row: dict) -> None:
    """Raise ValueError if the row would not survive the gate's own re-derivation (same formula, same tolerances)."""
    price, landed, net = row["price"], row["landed"], row["net_margin"]
    parts = [row["breakdown"][k] for k in ("product", "domestic", "freight", "services")]
    deducted = [row["deductions"][k] for k in ("fees", "refunds", "other")]
    derived = (price - landed - sum(deducted)) / price
    if abs(sum(parts) - landed) > GATE_BREAKDOWN_TOLERANCE:
        raise ValueError(f"breakdown {sum(parts)} does not sum to landed {landed}")
    if abs(net - derived) > GATE_NET_TOLERANCE:
        raise ValueError(f"net_margin {net} differs from the gate's derived {derived}")


def summarize(rows: list) -> dict:
    """The packet 'summary' block, from the stored rows."""
    pcts = [r["landed_pct_of_price"] for r in rows]
    return {"variants": len(rows),
            "pass_both": sum(1 for r in rows if r["landed"] <= r["price"] * .5 and r["net_margin"] >= .35),
            "landed_usd_min": min(r["landed"] for r in rows), "landed_usd_max": max(r["landed"] for r in rows),
            "min_landed_pct": min(pcts), "max_landed_pct": max(pcts), "min_net": round(min(r["net_margin"] for r in rows), 4)}
