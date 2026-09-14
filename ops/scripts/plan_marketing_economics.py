#!/usr/bin/env python3
"""Calculate a proposal-only acquisition ceiling; never authorize or place ads.

Use booked merchandise revenue after discounts, before refunds, excluding tax.
The return-loss rate is incremental loss after recoveries, relative to that same
revenue base. Do not subtract refunds here if already removed from input revenue.
Cost and return-loss inputs must be disjoint: a recovery already reducing the
cost rate cannot also reduce the return-loss rate. Allocate each recovery once.
"""

from __future__ import annotations

import argparse
import json
from decimal import Decimal


def evaluate(*, order_value: Decimal, cost_rate: Decimal, return_loss_rate: Decimal,
             profit_rate: Decimal, conversion_rate: Decimal, cpc_cap: Decimal) -> dict:
    values = (order_value, cost_rate, return_loss_rate, profit_rate, conversion_rate, cpc_cap)
    if not all(value.is_finite() for value in values):
        raise ValueError("Inputs must be finite numbers; unknown inputs cannot be zero-filled.")
    if order_value <= 0 or cpc_cap <= 0:
        raise ValueError("Order value and CPC cap must be positive.")
    if not all(Decimal(0) <= rate <= Decimal(1)
               for rate in (cost_rate, return_loss_rate, profit_rate)):
        raise ValueError("Cost, return-loss, and profit rates must be between zero and one.")
    if not Decimal(0) < conversion_rate <= Decimal(1):
        raise ValueError("Conversion rate must be greater than zero and at most one.")
    ad_share = Decimal(1) - cost_rate - return_loss_rate - profit_rate
    allowance = max(Decimal(0), ad_share)
    cpa = order_value * allowance
    economic_cpc = cpa * conversion_rate
    return {
        "status": "PROPOSAL_ONLY" if allowance > 0 else "NO_POSITIVE_AD_ALLOWANCE",
        "live_authority": "NONE",
        "revenue_basis": "booked_after_discounts_before_refunds_excluding_tax",
        "input_order_value": str(order_value),
        "input_cost_rate": str(cost_rate),
        "input_incremental_return_loss_rate": str(return_loss_rate),
        "input_profit_rate": str(profit_rate),
        "input_conversion_rate": str(conversion_rate),
        "input_cpc_cap": str(cpc_cap),
        "available_ad_revenue_share": str(allowance),
        "target_cpa_ceiling": str(cpa),
        "minimum_revenue_roas": str(Decimal(1) / allowance) if allowance > 0 else None,
        "economic_cpc_ceiling": str(economic_cpc),
        "proposed_cpc_ceiling": str(min(cpc_cap, economic_cpc)),
        "cpa_if_spending_at_input_cpc": str(cpc_cap / conversion_rate),
        "profit_rate_if_spending_at_input_cpc": str(
            Decimal(1) - cost_rate - return_loss_rate - cpc_cap / conversion_rate / order_value
        ),
        "input_cpc_meets_profit_target": cpc_cap <= economic_cpc,
        "limitation": "Scenario math only. Cost and return-loss inputs must be disjoint; allocate each refund/recovery once. Validate margins, return loss, conversion quality, attribution, and exact budget authority before spend.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("order-value", "cost-rate", "return-loss-rate", "profit-rate", "conversion-rate", "cpc-cap"):
        parser.add_argument(f"--{name}", required=True, type=Decimal)
    args = parser.parse_args()
    try:
        result = evaluate(**vars(args))
    except ValueError as error:
        parser.error(str(error))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
