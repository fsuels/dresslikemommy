#!/usr/bin/env python3
"""Decision-level examples for the proposal-only acquisition calculator."""

import importlib.util
from decimal import Decimal as D
from pathlib import Path
import unittest

path = Path(__file__).resolve().parents[1] / "scripts" / "plan_marketing_economics.py"
spec = importlib.util.spec_from_file_location("economics", path)
economics = importlib.util.module_from_spec(spec)
spec.loader.exec_module(economics)


class EconomicsTest(unittest.TestCase):
    def example(self, **changes):
        inputs = dict(order_value=D("100"), cost_rate=D(".5"), return_loss_rate=D(".05"),
                      profit_rate=D(".3"), conversion_rate=D(".01"), cpc_cap=D(".15"))
        inputs.update(changes)
        return economics.evaluate(**inputs)

    def test_hundred_dollar_order_retains_thirty(self):
        result = self.example()
        self.assertEqual(D(result["target_cpa_ceiling"]), D("15"))
        self.assertEqual(D(result["profit_rate_if_spending_at_input_cpc"]), D(".30"))
        self.assertTrue(result["input_cpc_meets_profit_target"])
        self.assertEqual(result["live_authority"], "NONE")

    def test_cheap_clicks_can_still_be_unprofitable(self):
        result = self.example(conversion_rate=D(".005"))
        self.assertEqual(D(result["proposed_cpc_ceiling"]), D(".075"))
        self.assertEqual(D(result["cpa_if_spending_at_input_cpc"]), D("30"))
        self.assertFalse(result["input_cpc_meets_profit_target"])

    def test_owner_cpc_cap_is_not_raised(self):
        result = self.example(conversion_rate=D(".03"))
        self.assertEqual(D(result["economic_cpc_ceiling"]), D(".45"))
        self.assertEqual(D(result["proposed_cpc_ceiling"]), D(".15"))

    def test_no_positive_allowance_does_not_recommend_spend(self):
        result = self.example(return_loss_rate=D(".25"))
        self.assertEqual(result["status"], "NO_POSITIVE_AD_ALLOWANCE")
        self.assertEqual(D(result["proposed_cpc_ceiling"]), D("0"))
        self.assertIsNone(result["minimum_revenue_roas"])

    def test_zero_nan_and_invalid_rates_are_rejected(self):
        for changes in ({"conversion_rate": D("0")}, {"order_value": D("NaN")},
                        {"return_loss_rate": D("-.1")}, {"cost_rate": D("1.1")}):
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                self.example(**changes)

    def test_return_loss_must_be_explicit(self):
        with self.assertRaises(TypeError):
            economics.evaluate(order_value=D("100"), cost_rate=D(".5"), profit_rate=D(".3"),
                               conversion_rate=D(".01"), cpc_cap=D(".15"))


if __name__ == "__main__":
    unittest.main()
