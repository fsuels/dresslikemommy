#!/usr/bin/env python3
"""Packet economics rows must be accepted by the activation gate's per-variant check with no tolerance noise."""
from __future__ import annotations

import copy
import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from ops.sourcing import packet_economics as pe  # noqa: E402

GATE_TEST = ROOT / "ops/tests/test_listing_quality_activation_gate.py"
KW = dict(fx_cny_per_usd=6.6459, domestic_cny=7.8, freight_cny=80.88, services_cny=13.5, quote_as_of="2026-11-07T00:00:00+00:00")
PRICES = (45.99, 49.99, 38.99, 60.99)


def legacy_row(variant_key, price, cost):
    """The old builder: round the stored parts but derive net from unrounded landed and deductions."""
    fx = KW["fx_cny_per_usd"]
    landed = (cost + KW["domestic_cny"] + KW["freight_cny"] + KW["services_cny"]) / fx
    fees, ref = .029 * price + .30, .037 * price
    return {"variant_key": variant_key, "price": price, "landed": round(landed, 2), "net_margin": (price - landed - fees - ref) / price,
            "breakdown": {"product": round(cost / fx, 2), "domestic": round(KW["domestic_cny"] / fx, 2),
                          "freight": round(KW["freight_cny"] / fx, 2), "services": round(KW["services_cny"] / fx, 2)},
            "deductions": {"fees": round(fees, 2), "refunds": round(ref, 2), "other": 0.0}, "quote_as_of": KW["quote_as_of"]}


class RowTests(unittest.TestCase):
    def test_row_is_rounded_to_cents_and_net_is_derived_from_stored_values(self):
        for price in PRICES:
            row = pe.variant_economics(variant_key="v", price=price, cny_unit_cost=43, **KW)
            for value in (*row["breakdown"].values(), *row["deductions"].values(), row["landed"]):
                self.assertEqual(value, round(value, 2))
            derived = (row["price"] - row["landed"] - sum(row["deductions"].values())) / row["price"]
            self.assertAlmostEqual(row["net_margin"], derived, delta=1e-12)
            self.assertLessEqual(abs(sum(row["breakdown"].values()) - row["landed"]), 0.01 + 1e-9)

    def test_legacy_unrounded_net_is_rejected_by_the_same_check(self):
        bad = [legacy_row("v", p, 43) for p in PRICES]
        self.assertTrue(any(abs(r["net_margin"] - (r["price"] - r["landed"] - sum(r["deductions"].values())) / r["price"]) > pe.GATE_NET_TOLERANCE for r in bad))
        with self.assertRaises(ValueError):
            for r in bad:
                pe.check_gate_consistency(r)

    def test_summary_counts_and_extra_keys(self):
        rows = [pe.variant_economics(variant_key=f"v{i}", price=p, cny_unit_cost=43, size="S", **KW) for i, p in enumerate(PRICES)]
        self.assertEqual(rows[0]["size"], "S")
        summary = pe.summarize(rows)
        self.assertEqual((summary["variants"], summary["pass_both"]), (4, 3))


@unittest.skipUnless(GATE_TEST.exists() and (ROOT / "ops/category-team/listing_quality_gate.py").exists(),
                     "activation gate and its fixture are not in this checkout")
class RealGateTests(unittest.TestCase):
    """Run the actual gate's validate() with packet-builder rows (gate and its tests are read-only here)."""

    def setUp(self):
        spec = importlib.util.spec_from_file_location("gate_fixture_for_packet_economics", GATE_TEST)
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        self.gate_tests = module
        self.quality = module.quality
        self.receipt, self.product, self.registry, self.closeout = module.fixture()
        for node, price in zip(self.product["variants"]["nodes"], (45.99, 49.99)):
            node["price"] = f"{price:.2f}"
        self.receipt["product_fingerprint"] = self.quality.fingerprint(self.product)
        self.quote = module.date_before(3)

    def rows(self, cost=43):
        return [pe.variant_economics(variant_key=n["id"], price=float(n["price"]), cny_unit_cost=cost,
                                     **{**KW, "quote_as_of": self.quote}) for n in self.product["variants"]["nodes"]]

    def validate(self):
        return self.quality.validate(self.receipt, self.product, self.gate_tests.HANDLE, self.registry, self.closeout, self.gate_tests.NOW)

    def test_gate_accepts_builder_rows(self):
        self.receipt["economics"] = self.rows()
        self.assertEqual(self.validate()["status"], "passed")

    def test_gate_rejects_legacy_rows_with_the_same_inputs(self):
        self.receipt["economics"] = [dict(legacy_row(n["id"], float(n["price"]), 43), quote_as_of=self.quote) for n in self.product["variants"]["nodes"]]
        with self.assertRaises(self.quality.QualityHold):
            self.validate()


if __name__ == "__main__":
    unittest.main()
