#!/usr/bin/env python3.13
"""Frozen channel-continuation failures; old exact-retrieval suite is a holdout."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "ops/scripts"))

from compile_task_context import compile_task_context, contains_exact_entity, extract_entities
from session_context import channel_for_query, channel_matches, record_dates
from test_compile_task_context import CURRENT_STATE


HEADERS = (
    "Priority", "Status", "Action", "Owner agent", "Gate", "Evidence/source",
    "Lane", "Checkpoint", "Owner input", "Completed milestone", "Next step",
    "Checkpoint date", "Task title",
)


def task(action, owner, gate, milestone, step, lane="Free + paid"):
    return ["P0", "YELLOW", action, owner, gate, "fixture-receipt.json", lane,
            "Acceptance pending", "None", milestone, step, "2026-01-10", action]


TASKS = [
    task("TA-01 Finish Google Ads setup under manager7001112223", "root01abcdef Ads owner",
         "Account setup unverified; full-paid NONE", "Merchant receipt complete",
         "Read operating Ads6501112223 under the existing owner"),
    task("TA-02 Verify retained GA4330111222 receiver", "root02abcdef Analytics owner",
         "Report receipt and genuine purchase acceptance open", "Migration and duplicate cleanup verified",
         "Verify receiver; preserve legacy disconnection", "Measurement + profit"),
    task("TA-03 Verify Merchant513111222 eligibility", "root03abcdef Merchant owner",
         "Website review pending; receipt is not serving approval", "492 fixture offers received",
         "Read review result without another submission", "Free listings"),
    task("TA-04 Repair Shopify product headings", "root04abcdef product owner",
         "Published rendering open", "Source headings saved", "Verify published headings", "Store conversion"),
    task("TA-05 Release reviewed Shopify theme", "root05abcdef theme owner",
         "Publication requires owner", "Preview verified", "Owner publishes after conflict check", "Store conversion"),
    task("TA-06 Microsoft Ads receiving", "root06abcdef Microsoft owner",
         "UET receipt open", "Local campaigns prepared", "Read UET receiver", "Paid traffic"),
    task("TA-07 Pinterest measurement", "root07abcdef Pinterest owner",
         "Consent acceptance conflicted", "Local callbacks verified", "Verify consent restoration", "Free + paid"),
]

WORKLOG = """AGENT_CONTINUITY_ANCHOR: 2026-01-01-merchant-zero
task_entities: Merchant513111222,TA-03
task_stage: DIAGNOSE
No offers received on January 1.
---
AGENT_CONTINUITY_ANCHOR: 2026-01-10-google-ads-setup
task_entities: Ads6501112223,manager7001112223,TA-01
task_stage: HANDOFF
next_action_id: READ_ONLY_MARKETING_RECONCILIATION
Google Ads setup still needs an exact readback.
---
AGENT_CONTINUITY_ANCHOR: 2026-01-10-merchant-receipt
task_entities: Merchant513111222,TA-03
task_stage: VERIFY
next_action_id: READ_ONLY_MARKETING_RECONCILIATION
492 fixture offers received; website review pending. Approval and serving unverified.
---
AGENT_CONTINUITY_ANCHOR: 2026-01-10-ga4-cleanup
task_entities: GA4330111222,TA-02
task_stage: HANDOFF
next_action_id: READ_ONLY_MARKETING_RECONCILIATION
Migration and duplicate cleanup complete. Receiver and genuine purchase acceptance open.
---
AGENT_CONTINUITY_ANCHOR: 2026-01-10-shopify-product
task_entities: Product7771112223,TA-04
task_stage: VERIFY
Shopify source headings saved; published check remains.
---
AGENT_CONTINUITY_ANCHOR: 2026-01-10-shopify-theme
task_entities: theme8881112223,TA-05
task_stage: HANDOFF
Shopify preview verified; owner publication pending.
---
AGENT_CONTINUITY_ANCHOR: 2026-01-11-unrelated-latest
task_entities: PROB-2026-01-11-UNRELATED
task_stage: BUILD
Unrelated local work is globally newest.
---
"""


class SessionContextTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.paths = {name: self.root / name for name in (
            "AGENT_WORKLOG.md", "current_marketing_state.md", "PROBLEM_TRACKER.md",
            "AGENT_COORDINATION.md", "action_queue.md", "GROWTH_NORTH_STAR.md",
        )}
        self.paths["AGENT_WORKLOG.md"].write_text(WORKLOG)
        self.paths["current_marketing_state.md"].write_text(CURRENT_STATE)
        self.paths["PROBLEM_TRACKER.md"].write_text("# Problems\n")
        self.paths["GROWTH_NORTH_STAR.md"].write_text(
            "# Growth North Star\n\n## Owner's Goal In Plain English\n\n"
            "Build profitable matching-outfit sales at the sourced fixture ROAS target.\n\n"
            "## Historical details\nDo not use this as the current goal.\n"
        )
        table = "\n".join("| " + " | ".join(row) + " |" for row in [HEADERS, ["---"] * len(HEADERS), *TASKS])
        self.paths["action_queue.md"].write_text(
            "# Queue\n## Current turnaround tasks — fixture\n" + table +
            "\n## Historical queue\n| P0 | DONE | TA-99 Old Google Ads launch | retired |\n"
        )
        claim_headers = ["Workstream", "Surface", "Status", "Owner / Agent", "Allowed Actions",
                         "Blocked Actions", "Last Evidence / Handoff", "Notes"]
        claims = [
            ["Current Google Ads setup", "Ads6501112223", "HANDOFF_SETUP_OPEN", "root01abcdef",
             "Read only", "No spend", "2026-01-10-google-ads-setup; TA-01", "Current Ads owner"],
            ["Current Merchant repair", "Merchant513111222", "RECEIVED_REVIEW_PENDING", "root03abcdef",
             "Own exact nonspend scope", "No paid action", "2026-01-10-merchant-receipt; TA-03",
             "Complete claim notes " + "preserve scope " * 50 + "END_OF_COMPLETE_CLAIM"],
            ["Retained Google Analytics", "GA4330111222", "CLEANUP_DONE_RECEIVER_GATED", "root02abcdef",
             "Read only", "No migration replay", "2026-01-10-ga4-cleanup; TA-02", "Receiver acceptance open"],
            ["Current Shopify product work", "Product7771112223", "VERIFY", "root04abcdef",
             "Own product", "No theme release", "2026-01-10-shopify-product; TA-04", "Preserve headings"],
            ["Current Shopify theme release", "theme8881112223", "HANDOFF", "root05abcdef",
             "Own preview", "No publish without owner", "2026-01-10-shopify-theme; TA-05", "Release gate"],
            ["Old Google Ads setup", "Ads6501112223", "DONE", "root09abcdef",
             "Historic only", "No current scope", "2025-05-01-old-ads", "Obsolete setup"],
        ]
        self.paths["AGENT_COORDINATION.md"].write_text(
            "# Coordination\n## Active Workstreams\n" + "\n".join(
                "| " + " | ".join(row) + " |" for row in [claim_headers, ["---"] * 8, *claims]
            ) + "\n"
        )

    def compile(self, query, **kwargs):
        return compile_task_context(
            query, worklog_path=self.paths["AGENT_WORKLOG.md"],
            current_state_path=self.paths["current_marketing_state.md"],
            problem_tracker_path=self.paths["PROBLEM_TRACKER.md"],
            coordination_path=self.paths["AGENT_COORDINATION.md"],
            action_queue_path=self.paths["action_queue.md"],
            goal_path=self.paths["GROWTH_NORTH_STAR.md"], **kwargs,
        )

    def add_x_fixture(self):
        row = task("TA-08 Continue X organic pilot", "root08abcdef X owner",
                   "Publishing connection required; paid NONE", "First post published",
                   "Use the existing scheduled cohort", "Free traffic")
        queue = self.paths["action_queue.md"]
        queue.write_text(queue.read_text().replace(
            "\n## Historical queue", "\n| " + " | ".join(row) + " |\n## Historical queue"))
        worklog = self.paths["AGENT_WORKLOG.md"]
        worklog.write_text(worklog.read_text() + (
            "AGENT_CONTINUITY_ANCHOR: 2026-01-10-x-organic-pilot\n"
            "task_entities: Xdresslikemommy,TA-08\ntask_stage: HANDOFF\n"
            "X organic pilot has one published post; preserve its existing cohort.\n---\n"
        ))
        claims = self.paths["AGENT_COORDINATION.md"]
        claims.write_text(claims.read_text() + (
            "| Current X organic pilot | Xdresslikemommy | HANDOFF | root08abcdef | "
            "Own existing organic scope | No paid action | "
            "2026-01-10-x-organic-pilot; TA-08 | Keep the published cohort |\n"
        ))

    def test_x_channel_inventory_and_exact_account_holdout(self):
        self.add_x_fixture()
        for query in ("continue X", "resume Twitter", "work on X"):
            with self.subTest(query=query):
                result = self.compile(query)
                self.assertEqual(result["diagnostics"]["status"], "OK")
                brief = result["session_brief"]
                self.assertEqual(brief["channel"], "x")
                self.assertEqual([r["id"] for r in brief["current_tasks"]], ["TA-08"])
                self.assertEqual([r["anchor_id"] for r in brief["recent_anchors"]],
                                 ["2026-01-10-x-organic-pilot"])
                self.assertIn("root08abcdef", brief["coordination_claims"][0]["text"])
                self.assertEqual(result["authority"]["fields"]["approved_external_scope"], "NONE")
                self.assertFalse(brief["external_write_authorized"])
        exact = self.compile("Xdresslikemommy", explicit_entities=("Xdresslikemommy",))
        self.assertEqual(exact["selected_anchor"]["anchor_id"], "2026-01-10-x-organic-pilot")
        self.assertIsNone(exact["session_brief"])

    def test_x_current_operation_continuation_queries(self):
        # The current task moved from a pilot/profile label to an ongoing
        # operation. Freeze that source wording and its newer linked handoff.
        self.add_x_fixture()
        queue = self.paths["action_queue.md"]
        queue.write_text(queue.read_text().replace(
            "Continue X organic pilot",
            "Grow qualified traffic through the ongoing Dress Like Mommy X operation"))
        worklog = self.paths["AGENT_WORKLOG.md"]
        latest = "2026-01-11-x-proactive-traffic-loop-and-api-boundary"
        worklog.write_text(worklog.read_text() + (
            f"AGENT_CONTINUITY_ANCHOR: {latest}\n"
            "task_entities: Xdresslikemommy,TA-08\ntask_stage: HANDOFF\n"
            "next_action_id: READ_ONLY_MARKETING_RECONCILIATION\n"
            "Existing schedules preserved; new publication connection remains required.\n---\n"
        ))
        for subject in ("Shopify shirt Size x Color", "X operationz", "X operational costs"):
            self.assertFalse(channel_matches("x", subject, task=True))
        for query in ("continue X", "continue working on X", "resume Twitter", "work on Twitter"):
            with self.subTest(query=query):
                result = self.compile(query)
                self.assertEqual(result["diagnostics"]["status"], "OK")
                brief = result["session_brief"]
                self.assertEqual([row["id"] for row in brief["current_tasks"]], ["TA-08"])
                current = brief["current_tasks"][0]
                self.assertEqual(current["fields"]["Owner agent"], "root08abcdef X owner")
                self.assertEqual(current["fields"]["Gate"], "Publishing connection required; paid NONE")
                self.assertEqual(current["identity_evidence"]["anchor_id"], latest)
                self.assertIn(latest, [row["anchor_id"] for row in brief["recent_anchors"]])
                self.assertEqual(result["authority"]["fields"]["approved_external_scope"], "NONE")
                self.assertFalse(brief["external_write_authorized"])
                self.assertIsNone(result["selected_anchor"])

    def test_x_channel_does_not_relax_relevance_or_authority(self):
        self.add_x_fixture()
        for subject in ("Shopify shirt Size x Color", "Shopify product X large",
                        "Microsoft Ads", "Google Ads", "Pinterest",
                        "Xylophone product", "Xero account", "X accountancy",
                        "X profilez", "Shopify product X organic cotton dress",
                        "unrelated-latest"):
            with self.subTest(subject=subject):
                self.assertFalse(channel_matches("x", subject, task=True))
        queue = self.paths["action_queue.md"]
        unrelated = task("TA-09 Shopify product X organic cotton dress", "root09abcdef",
                         "Source only", "Body reviewed", "Verify product source")
        queue.write_text(queue.read_text().replace(
            "\n## Historical queue", "\n| " + " | ".join(unrelated) + " |\n## Historical queue"))
        inventory = self.compile("continue X")["session_brief"]
        self.assertEqual([row["id"] for row in inventory["current_tasks"]], ["TA-08"])
        for query in ("continue X and Pinterest", "continue Xylophone", "resume x axis"):
            self.assertIsNone(channel_for_query(query))
            self.assertEqual(self.compile(query)["diagnostics"]["status"], "FAILED_CLOSED")
        split = self.compile("continue X", explicit_entities=("Xdresslikemommy", "330111222"))
        self.assertIn("REQUIRED_ENTITIES_NOT_COLOCATED", split["diagnostics"]["errors"])
        self.assertIsNone(split["session_brief"])
        queue = self.paths["action_queue.md"]
        saved_queue = queue.read_text()
        queue.write_text("\n".join(line for line in saved_queue.splitlines() if "TA-08" not in line))
        missing = self.compile("continue X")
        self.assertEqual(missing["diagnostics"]["status"], "FAILED_CLOSED")
        self.assertIn("NO_CURRENT_CHANNEL_TASKS", missing["diagnostics"]["errors"])
        self.assertFalse(missing["session_brief"]["external_write_authorized"])
        queue.write_text(saved_queue)
        control = self.paths["current_marketing_state.md"]
        control.write_text(CURRENT_STATE.replace("- `approved_external_scope`: `NONE`",
                                                "approved_external_scope: NONE."))
        malformed = self.compile("continue X")
        self.assertEqual(malformed["diagnostics"]["status"], "FAILED_CLOSED")
        self.assertIn("malformed authoritative control field line(s)", malformed["diagnostics"]["errors"])
        self.assertFalse(malformed["session_brief"]["external_write_authorized"])

    def assert_x_relationship_cases(self, cases):
        self.add_x_fixture()
        saved = {name: self.paths[name].read_text() for name in (
            "action_queue.md", "AGENT_WORKLOG.md", "AGENT_COORDINATION.md")}
        for name, evidence, other_evidence, metadata, expected_entity in cases:
            with self.subTest(case=name):
                self.paths["action_queue.md"].write_text("\n".join(
                    line.replace("fixture-receipt.json", evidence) if "TA-08" in line else line
                    for line in saved["action_queue.md"].splitlines()) + "\n")
                self.paths["AGENT_WORKLOG.md"].write_text(saved["AGENT_WORKLOG.md"] + (
                    "AGENT_CONTINUITY_ANCHOR: 2026-01-11-x-operation-current\n"
                    f"task_entities: Xdresslikemommy,TA-08,{metadata}\n"
                    "task_stage: HANDOFF\nExisting X ownership and publishing gate remain.\n---\n"
                ))
                self.paths["AGENT_COORDINATION.md"].write_text(saved["AGENT_COORDINATION.md"] + (
                    "| Collection recovery | Shopify product | HANDOFF | root05abcdef | "
                    "Read only | No publication | 2026-01-11; " + other_evidence +
                    "; TA-05 | Preserve the collection owner |\n"
                ))
                result = self.compile("continue X")
                self.assertEqual(result["diagnostics"]["status"], "OK")
                brief = result["session_brief"]
                self.assertEqual([row["id"] for row in brief["current_tasks"]], ["TA-08"])
                self.assertEqual(brief["current_tasks"][0]["fields"]["Owner agent"], "root08abcdef X owner")
                self.assertEqual(result["authority"]["fields"]["approved_external_scope"], "NONE")
                self.assertFalse(brief["external_write_authorized"])
                related = [row for row in brief["coordination_claims"]
                           if row["fields"]["Workstream"] == "Collection recovery"]
                if expected_entity is None:
                    self.assertEqual(related, [])
                else:
                    self.assertEqual(len(related), 1)
                    basis = related[0]["task_link_basis"]["TA-08"]
                    self.assertFalse(basis["explicit_task_id"])
                    self.assertIn(expected_entity, basis["exact_entities"])

    def test_filename_dates_do_not_create_cross_lane_relationships(self):
        self.assert_x_relationship_cases((
            ("different receipt paths", "ops/evidence/x-20260911.json",
             "ops/evidence/collection-20260911.json", "", None),
            ("labeled date directory", "ops/evidence/proactive-20260911/READBACK.md",
             "collection-recovery-20260911.json", "", None),
            ("different bare filenames", "x-20260911-receipt.json",
             "collection-20260911-receipt.csv", "", None),
            ("account versus target filename date", "Merchant20260911",
             "ops/evidence/collection-20260911.md", "", None),
            ("date derived from metadata", "fixture-receipt.json", "Merchant20260911",
             "ops/evidence/x-20260911.json", None),
        ))

    def test_real_account_path_and_exact_relationship_holdouts(self):
        self.assert_x_relationship_cases((
            ("same complete dated path", "ops/evidence/shared-20260911.json",
             "ops/evidence/shared-20260911.json", "", "ops/evidence/shared-20260911.json"),
            ("typed date-shaped account", "Merchant20260911", "20260911", "", "20260911"),
            ("standalone date-shaped account", "20260911", "Merchant20260911", "", "20260911"),
            ("existing Merchant account", "Merchant513111222", "513111222", "", "513111222"),
            ("account in path", "accounts/20260911", "Merchant20260911", "", "20260911"),
            ("account directory with file", "accounts/20260911/report.json",
             "Merchant20260911", "", "20260911"),
            ("real account beside dated filenames", "ops/evidence/x-20260911.json Merchant20260911",
             "ops/evidence/collection-20260911.json Merchant20260911", "", "20260911"),
        ))

    def test_explicit_date_shaped_account_selector_holdout(self):
        path = self.paths["AGENT_WORKLOG.md"]
        path.write_text(WORKLOG + (
            "AGENT_CONTINUITY_ANCHOR: 2026-01-12-account-proof\n"
            "task_entities: Merchant20260911\ntask_stage: VERIFY\n"
            "Account identity is explicit, even though its digits resemble a date.\n---\n"
        ))
        result = self.compile("continue account", explicit_entities=("20260911",))
        self.assertEqual(result["diagnostics"]["status"], "OK")
        self.assertEqual(result["selected_anchor"]["anchor_id"], "2026-01-12-account-proof")
        self.assertIsNone(result["session_brief"])
        self.assertEqual(result["entities"], ["20260911"])

    def test_ads_channel_current_owner_goal_and_provenance(self):
        result = self.compile("continue Google Ads")
        self.assertEqual(result["diagnostics"]["status"], "OK")
        brief = result["session_brief"]
        self.assertEqual(brief["channel"], "google-ads")
        self.assertEqual(result["authority"]["fields"]["approved_external_scope"], "NONE")
        self.assertFalse(brief["external_write_authorized"])
        self.assertIn("profitable matching-outfit sales", brief["business_goal"]["text"])
        self.assertEqual([r["id"] for r in brief["current_tasks"]], ["TA-01"])
        self.assertIn("root01abcdef", brief["coordination_claims"][0]["fields"]["Owner / Agent"])
        self.assertNotIn("Old Google Ads setup", json.dumps(brief["coordination_claims"]))
        for record in [brief["business_goal"], *brief["current_tasks"], *brief["coordination_claims"], *brief["recent_anchors"]]:
            self.assertTrue(Path(record["source_path"]).is_file())
            lines = Path(record["source_path"]).read_text().splitlines()
            self.assertEqual(record["text"], "\n".join(lines[record["start_line"]-1:record["end_line"]]))
        self.assertEqual(result, self.compile("continue Google Ads"))

    def test_merchant_receipt_review_and_compact_identity(self):
        result = self.compile("continue Google Merchant")
        self.assertEqual(result["diagnostics"]["status"], "OK")
        brief = result["session_brief"]
        self.assertIn("492 fixture offers received", brief["current_tasks"][0]["fields"]["Completed milestone"])
        self.assertIn("review pending", brief["current_tasks"][0]["fields"]["Gate"])
        self.assertIn("END_OF_COMPLETE_CLAIM", brief["coordination_claims"][0]["text"])
        self.assertEqual(brief["recent_anchors"][0]["anchor_id"], "2026-01-10-merchant-receipt")
        self.assertIn("513111222", extract_entities("continue Merchant513111222"))
        for query in ("continue Merchant513111222", "continue Merchant 513111222"):
            exact = self.compile(query, explicit_entities=("513111222",))
            self.assertEqual(exact["selected_anchor"]["anchor_id"], "2026-01-10-merchant-receipt")
        self.assertFalse(contains_exact_entity("Merchant9513111222", "513111222"))
        # A current claim can conflict with the task queue; do not silently choose it.
        path = self.paths["AGENT_COORDINATION.md"]
        path.write_text(path.read_text().replace("root03abcdef", "root08abcdef"))
        conflicted = self.compile("continue Google Merchant")["session_brief"]
        self.assertTrue(conflicted["conflicts"])
        self.assertIn("root03abcdef", json.dumps(conflicted["current_tasks"]))
        self.assertIn("root08abcdef", json.dumps(conflicted["coordination_claims"]))

    def test_broad_shopify_inventory_and_other_channel_routing(self):
        result = self.compile("continue Shopify")
        self.assertEqual(result["diagnostics"]["status"], "OK")
        self.assertIsNone(result["selected_anchor"])
        self.assertEqual(result["session_brief"]["mode"], "CHANNEL_INVENTORY")
        self.assertEqual([r["id"] for r in result["session_brief"]["current_tasks"]], ["TA-04", "TA-05"])
        self.assertNotIn("unrelated-latest", json.dumps(result["session_brief"]))
        for channel, expected in (("Microsoft Ads", "TA-06"), ("Pinterest", "TA-07")):
            payload = self.compile("continue " + channel)
            self.assertEqual(payload["diagnostics"]["status"], "OK")
            self.assertEqual([r["id"] for r in payload["session_brief"]["current_tasks"]], [expected])

    def test_ga4_cleanup_preserved_receiver_gate_and_scope_holdout(self):
        result = self.compile("continue Google Analytics")
        self.assertEqual(result["diagnostics"]["status"], "OK")
        brief = result["session_brief"]
        self.assertIn("duplicate cleanup verified", brief["current_tasks"][0]["fields"]["Completed milestone"])
        self.assertIn("genuine purchase acceptance open", brief["current_tasks"][0]["fields"]["Gate"])
        self.assertIn("330111222", extract_entities("GA4330111222"))
        exact = self.compile("continue Google Analytics", explicit_entities=("330111222",))
        self.assertEqual(exact["selected_anchor"]["anchor_id"], "2026-01-10-ga4-cleanup")
        split = self.compile("continue Google Analytics", explicit_entities=("330111222", "513111222"))
        self.assertEqual(split["diagnostics"]["status"], "FAILED_CLOSED")
        self.assertIn("REQUIRED_ENTITIES_NOT_COLOCATED", split["diagnostics"]["errors"])

    def test_safe_metadata_punctuation_and_authority_rejection_holdout(self):
        path = self.paths["AGENT_WORKLOG.md"]
        path.write_text(WORKLOG.replace("task_stage: HANDOFF", "task_stage: HANDOFF.")
                        .replace("next_action_id: READ_ONLY_MARKETING_RECONCILIATION",
                                 "next_action_id: READ_ONLY_MARKETING_RECONCILIATION."))
        result = self.compile("continue GA4330111222", explicit_entities=("330111222",))
        self.assertEqual(result["diagnostics"]["status"], "OK")
        self.assertEqual(result["task_stage"], "HANDOFF")
        self.assertEqual(result["selected_anchor"]["metadata"]["next_action_id"], "READ_ONLY_MARKETING_RECONCILIATION")
        control = self.paths["current_marketing_state.md"]
        control.write_text(CURRENT_STATE.replace("- `approved_external_scope`: `NONE`", "approved_external_scope: NONE."))
        malformed = self.compile("continue Google Ads")
        self.assertEqual(malformed["diagnostics"]["status"], "FAILED_CLOSED")
        self.assertIn("malformed authoritative control field line(s)", malformed["diagnostics"]["errors"])
        self.assertFalse(malformed["session_brief"]["external_write_authorized"])

    def test_implicit_numeric_query_exposes_newer_same_entity_context(self):
        # Additional observed defect after the five frozen failures: preserve
        # the original implicit relevance selector, but never hide newer state.
        old = (
            "AGENT_CONTINUITY_ANCHOR: 2026-01-02-analytics-prose\n"
            "task_entities: 330111222\ntask_stage: DIAGNOSE\n"
            "Google Analytics report setup originally needs migration.\n---\n"
        )
        self.paths["AGENT_WORKLOG.md"].write_text(old + WORKLOG)
        result = self.compile("continue Google Analytics 330111222")
        self.assertEqual(result["selected_anchor"]["anchor_id"], "2026-01-02-analytics-prose")
        self.assertEqual(result["selected_anchor"]["currentness"], "UNRESOLVED_NEWER_SAME_ENTITY_RECORDS_EXIST")
        self.assertTrue(any("newer same-entity records" in warning for warning in result["diagnostics"]["warnings"]))
        newer = result["newer_same_entity_records"][0]
        self.assertEqual(newer["anchor_id"], "2026-01-10-ga4-cleanup")
        self.assertIn("duplicate cleanup complete", newer["text"])
        self.assertTrue(Path(newer["source_path"]).is_file())

    def test_older_unresolved_claims_and_derived_identity_keep_provenance(self):
        path = self.paths["AGENT_COORDINATION.md"]
        path.write_text(path.read_text().replace("| DONE | root09abcdef", "| ACTIVE_WRITE_CLAIM | root09abcdef"))
        ads = self.compile("continue Google Ads")["session_brief"]
        self.assertNotIn("Old Google Ads setup", json.dumps(ads["coordination_claims"]))
        self.assertEqual(ads["older_coordination_claims"][0]["status"], "ACTIVE_WRITE_CLAIM")
        self.assertIn("neither clears a lock", ads["older_coordination_claims"][0]["handling"])
        queue = self.paths["action_queue.md"]
        queue.write_text(queue.read_text().replace("Merchant513111222", "Google Merchant"))
        brief = self.compile("continue Google Merchant")["session_brief"]
        self.assertIn("513111222", brief["current_tasks"][0]["identity_evidence"]["entities"])
        comparison = brief["source_comparisons"][0]
        self.assertIn("513111222", comparison["match_basis"]["exact_entities"])

    def test_role_prefixed_same_owner_is_not_a_conflict(self):
        path = self.paths["AGENT_COORDINATION.md"]
        path.write_text(path.read_text().replace("| root01abcdef |", "| root09abcdef parent; Merchant01abcdef owns channel |"))
        brief = self.compile("continue Google Ads")["session_brief"]
        self.assertTrue(brief["source_comparisons"])
        self.assertEqual(brief["conflicts"], [])

    def test_shared_account_dependency_is_not_an_owner_conflict(self):
        path = self.paths["AGENT_COORDINATION.md"]
        path.write_text(path.read_text().replace("root03abcdef", "root08abcdef")
                        .replace("2026-01-10-merchant-receipt; TA-03", "2026-01-10-merchant-receipt"))
        brief = self.compile("continue Google Merchant")["session_brief"]
        self.assertTrue(brief["source_comparisons"])
        self.assertFalse(brief["source_comparisons"][0]["match_basis"]["explicit_task_id"])
        self.assertEqual(brief["conflicts"], [])

    def add_microsoft_fixture(self):
        worklog = self.paths["AGENT_WORKLOG.md"]
        worklog.write_text(worklog.read_text() + (
            "AGENT_CONTINUITY_ANCHOR: 2026-01-10-microsoft-receiver\n"
            "task_entities: TA-06,Microsoft477439,36005151,PROB-2026-01-10-MS-CONSENT\n"
            "task_stage: HANDOFF\nnext_action_id: READ_ONLY_MARKETING_RECONCILIATION\n"
            "Microsoft receiver proof remains open under its existing owner.\n---\n"
        ))
        claims = self.paths["AGENT_COORDINATION.md"]
        claims.write_text(claims.read_text() + (
            "| Current Microsoft Ads repair | Microsoft477439 UET36005151 | HANDOFF | root06abcdef | "
            "Read only | No paid action | 2026-01-10-microsoft-receiver; TA-06 | "
            "Receiver acceptance and current owner preserved |\n"
        ))

    def test_mixed_handoff_does_not_assign_peer_identity(self):
        self.add_microsoft_fixture()
        queue = self.paths["action_queue.md"]
        queue.write_text("\n".join(
            line.replace("fixture-receipt.json", "PROB-2026-01-10-MS-CONSENT")
            if "TA-06" in line else line for line in queue.read_text().splitlines()) + "\n")
        worklog = self.paths["AGENT_WORKLOG.md"]
        saved = worklog.read_text()
        for name, metadata in (
            ("mixed parent receipt", "TA-01,TA-06,Ads6501112223"),
            ("peer task sharing a problem", "TA-01,Ads6501112223,PROB-2026-01-10-MS-CONSENT"),
        ):
            with self.subTest(case=name):
                latest = "2026-01-12-parent-receipt"
                worklog.write_text(saved + (
                    f"AGENT_CONTINUITY_ANCHOR: {latest}\ntask_entities: {metadata}\n"
                    "task_stage: VERIFY\nnext_action_id: READ_ONLY_MARKETING_RECONCILIATION\n"
                    "Google editor receipt and a separate TA-06 Microsoft follow-up. No ownership transfer.\n---\n"
                ))
                result = self.compile("continue Microsoft Ads")
                self.assertEqual(result["diagnostics"]["status"], "OK")
                brief = result["session_brief"]
                self.assertEqual([row["id"] for row in brief["current_tasks"]], ["TA-06"])
                identity = brief["current_tasks"][0]["identity_evidence"]
                self.assertEqual(identity["anchor_id"], "2026-01-10-microsoft-receiver")
                self.assertNotIn("6501112223", identity["entities"])
                self.assertEqual([row["fields"]["Workstream"] for row in brief["coordination_claims"]],
                                 ["Current Microsoft Ads repair"])
                self.assertIn(latest, [row["anchor_id"] for row in brief["recent_anchors"]])
                self.assertFalse(brief["external_write_authorized"])

    def test_microsoft_mailbox_and_browser_are_not_ads_scope(self):
        self.add_microsoft_fixture()
        claims = self.paths["AGENT_COORDINATION.md"]
        saved = claims.read_text()
        for surface in ("Connected Microsoft mailbox", "Microsoft Edge browser", "Microsoft365 mailbox"):
            with self.subTest(surface=surface):
                claims.write_text(saved + (
                    "| Google identity evidence in owner mail | " + surface + " | HANDOFF | root09abcdef | "
                    "Read only | No account change | 2026-01-11-mail-evidence | Mailbox only |\n"
                ))
                brief = self.compile("continue Microsoft Ads")["session_brief"]
                self.assertEqual([row["fields"]["Workstream"] for row in brief["coordination_claims"]],
                                 ["Current Microsoft Ads repair"])
        for surface in ("Microsoft Ads", "Microsoft Advertising", "Microsoft477439", "Bing Ads", "UET receiver"):
            self.assertTrue(channel_matches("microsoft-ads", surface), surface)

    def test_compact_receipt_date_keeps_current_microsoft_claim(self):
        self.add_microsoft_fixture()
        path = self.paths["AGENT_COORDINATION.md"]
        path.write_text(path.read_text().replace(
            "2026-01-10-microsoft-receiver; TA-06",
            "2026-01-09-microsoft-receiver; ops/microsoft/heartbeat-20260110-0243/READBACK.md; TA-06"))
        result = self.compile("continue Microsoft Ads")
        brief = result["session_brief"]
        self.assertEqual([row["fields"]["Workstream"] for row in brief["coordination_claims"]],
                         ["Current Microsoft Ads repair"])
        self.assertEqual(brief["coordination_claims"][0]["record_date"], "2026-01-10")
        self.assertEqual(brief["coordination_claims"][0]["evidence_grade"], "REPO_KNOWN")
        self.assertEqual(result["authority"]["fields"]["approved_external_scope"], "NONE")
        self.assertFalse(brief["external_write_authorized"])

    def test_microsoft_owner_conflict_and_selector_holdouts(self):
        self.add_microsoft_fixture()
        path = self.paths["AGENT_COORDINATION.md"]
        saved = path.read_text()
        path.write_text(saved.replace("| root06abcdef |", "| root09abcdef |"))
        result = self.compile("continue Microsoft Ads")
        self.assertEqual(len(result["session_brief"]["conflicts"]), 1)
        self.assertEqual(result["session_brief"]["conflicts"][0]["kind"], "OWNER_MISMATCH_REQUIRES_RECONCILIATION")
        path.write_text(saved)
        exact = self.compile("continue Microsoft Ads", explicit_entities=("36005151",))
        self.assertEqual(exact["selected_anchor"]["anchor_id"], "2026-01-10-microsoft-receiver")
        self.assertIsNone(exact["session_brief"])
        split = self.compile("continue Microsoft Ads", explicit_entities=("36005151", "6501112223"))
        self.assertIn("REQUIRED_ENTITIES_NOT_COLOCATED", split["diagnostics"]["errors"])
        self.assertIsNone(split["session_brief"])
        worklog = self.paths["AGENT_WORKLOG.md"]
        worklog.write_text(worklog.read_text() + (
            "AGENT_CONTINUITY_ANCHOR: second-receiver-receipt\n"
            "task_entities: 36005151\ntask_stage: HANDOFF\nMicrosoft receiver evidence.\n---\n"
        ))
        ambiguous = self.compile("continue Microsoft receiver")
        self.assertEqual(ambiguous["diagnostics"]["status"], "FAILED_CLOSED")
        self.assertIn("AMBIGUOUS_RELEVANT_ANCHOR", ambiguous["diagnostics"]["errors"])
        self.assertIsNone(ambiguous["session_brief"])

    def test_account_numbers_and_invalid_dates_do_not_refresh_claims(self):
        self.add_microsoft_fixture()
        path = self.paths["AGENT_COORDINATION.md"]
        saved = path.read_text()
        for evidence in ("Microsoft20290110", "20290110", "accounts/20290110/report.json",
                         "ops/microsoft/heartbeat-20260230/READBACK.md"):
            with self.subTest(evidence=evidence):
                path.write_text(saved.replace("2026-01-10-microsoft-receiver; TA-06",
                                              "2026-01-09-microsoft-receiver; " + evidence + "; TA-06"))
                brief = self.compile("continue Microsoft Ads")["session_brief"]
                self.assertEqual(brief["coordination_claims"], [])
                self.assertEqual(brief["older_coordination_claims"][0]["record_date"], "2026-01-09")
                self.assertIn("neither clears a lock", brief["older_coordination_claims"][0]["handling"])

    def test_ga4_exact_purchase_receiver_keeps_ads_operating_claim(self):
        queue = self.paths["action_queue.md"]
        queue.write_text("\n".join(
            line.replace("Verify receiver; preserve legacy disconnection",
                         "Verify Ads7760272273 purchase receiver; preserve legacy disconnection")
            if "TA-02" in line else line for line in queue.read_text().splitlines()) + "\n")
        claims = self.paths["AGENT_COORDINATION.md"]
        claims.write_text(claims.read_text().replace(
            "| Current Google Ads setup | Ads6501112223 |",
            "| Current Google Ads setup | Ads6501112223; Purchase7760272273 |"))
        worklog = self.paths["AGENT_WORKLOG.md"]
        worklog.write_text(worklog.read_text() + (
            "AGENT_CONTINUITY_ANCHOR: 2026-01-12-mixed-ads-analytics-receipt\n"
            "task_entities: TA-01,TA-02,Ads6501112223\ntask_stage: HANDOFF\n"
            "Separate Ads and Analytics receipts; preserve their exact receiver dependency.\n---\n"
        ))
        brief = self.compile("continue Google Analytics")["session_brief"]
        operating = [row for row in brief["coordination_claims"]
                     if row["fields"]["Workstream"] == "Current Google Ads setup"]
        self.assertEqual(len(operating), 1)
        basis = operating[0]["task_link_basis"]["TA-02"]
        self.assertEqual(basis, {"explicit_task_id": False, "exact_entities": ["7760272273"]})
        self.assertFalse(brief["external_write_authorized"])
        self.assertIn("7760272273", extract_entities("Purchase7760272273"))
        self.assertTrue(contains_exact_entity("Purchase7760272273", "7760272273"))
        for text in ("Purchase17760272273", "Purchase7760272273x", "OtherPurchase7760272273"):
            self.assertFalse(contains_exact_entity(text, "7760272273"), text)
        claims.write_text(claims.read_text().replace("Purchase7760272273", "Purchase17760272273"))
        changed = self.compile("continue Google Analytics")["session_brief"]
        self.assertNotIn("Current Google Ads setup", [row["fields"]["Workstream"]
                                                     for row in changed["coordination_claims"]])

    def test_action_dates_do_not_create_microsoft_claim_links(self):
        self.add_microsoft_fixture()
        saved = {name: self.paths[name].read_text() for name in (
            "action_queue.md", "AGENT_WORKLOG.md", "AGENT_COORDINATION.md")}
        cases = (
            ("different dated actions", "TA15-COMPLETED-DAY-20260914-0643",
             "ADS650-DRAFT-RECOVERY-20260914-0255", ""),
            ("single-task metadata action", "fixture-receipt.json",
             "ADS650-DRAFT-RECOVERY-20260914-0255", "TA15-COMPLETED-DAY-20260914-0643"),
            ("action source versus bare account", "TA15-COMPLETED-DAY-20260914-0643",
             "20260914", ""),
            ("typed account versus target action", "Merchant20260914",
             "ADS650-DRAFT-RECOVERY-20260914-0255", ""),
            ("metadata action versus typed account", "fixture-receipt.json",
             "Merchant20260914", "TA15-COMPLETED-DAY-20260914-0643"),
            ("extensionless receipt names", "heartbeat-20260914-0643",
             "review-20260914-0255", ""),
        )
        for name, evidence, other_evidence, metadata in cases:
            with self.subTest(case=name):
                self.paths["action_queue.md"].write_text("\n".join(
                    line.replace("fixture-receipt.json", evidence) if "TA-06" in line else line
                    for line in saved["action_queue.md"].splitlines()) + "\n")
                self.paths["AGENT_WORKLOG.md"].write_text(saved["AGENT_WORKLOG.md"] + (
                    "AGENT_CONTINUITY_ANCHOR: 2026-01-12-microsoft-action-receipt\n"
                    f"task_entities: TA-06,{metadata}\ntask_stage: HANDOFF\n"
                    "Microsoft completed-day evidence; account ownership unchanged.\n---\n"
                ))
                self.paths["AGENT_COORDINATION.md"].write_text(
                    saved["AGENT_COORDINATION.md"].replace(
                        "2026-01-10-google-ads-setup; TA-01",
                        "2026-01-10-google-ads-setup; " + other_evidence + "; TA-01"))
                result = self.compile("continue Microsoft Ads")
                brief = result["session_brief"]
                self.assertEqual(result["diagnostics"]["status"], "OK")
                self.assertEqual([row["id"] for row in brief["current_tasks"]], ["TA-06"])
                self.assertEqual([row["fields"]["Workstream"] for row in brief["coordination_claims"]],
                                 ["Current Microsoft Ads repair"])
                self.assertIn("root06abcdef", brief["coordination_claims"][0]["fields"]["Owner / Agent"])
                self.assertNotIn("20260914", brief["current_tasks"][0]["identity_evidence"]["entities"])
                self.assertIn("2026-01-12-microsoft-action-receipt",
                              [row["anchor_id"] for row in brief["recent_anchors"]])
                self.assertEqual(brief["conflicts"], [])
                self.assertEqual(result["authority"]["fields"]["approved_external_scope"], "NONE")
                self.assertFalse(brief["external_write_authorized"])

    def test_action_date_account_and_complete_identifier_holdouts(self):
        self.assert_x_relationship_cases((
            ("typed account beside action", "TA15-COMPLETED-DAY-20260914-0643 Merchant20260914",
             "ADS650-DRAFT-RECOVERY-20260914-0255 Merchant20260914", "", "20260914"),
            ("bare date-shaped account", "20260914", "Merchant20260914", "", "20260914"),
            ("numeric account directory", "ops/accounts/20260914/READBACK.md",
             "Merchant20260914", "", "20260914"),
            ("eight-digit non-date account", "51311122", "Merchant51311122", "", "51311122"),
            ("invalid calendar component", "action-20261399", "Merchant20261399", "", "20261399"),
            ("exact complete compound identifier", "TASK-REVIEW-20260914-0643",
             "TASK-REVIEW-20260914-0643", "", "TASK-REVIEW-20260914-0643"),
            ("exact complete dated receipt", "ops/heartbeat-20260914-0643/readback.json",
             "ops/heartbeat-20260914-0643/readback.json", "",
             "ops/heartbeat-20260914-0643/readback.json"),
            ("typed receiver beside actions", "TA15-COMPLETED-DAY-20260914-0643 Purchase7760272273",
             "ADS650-DRAFT-RECOVERY-20260914-0255 Ads7760272273", "", "7760272273"),
        ))

    def test_action_dates_preserve_explicit_selection_and_receipt_recency(self):
        worklog = self.paths["AGENT_WORKLOG.md"]
        worklog.write_text(worklog.read_text() + (
            "AGENT_CONTINUITY_ANCHOR: 2026-01-12-explicit-action-receipt\n"
            "task_entities: TASK-REVIEW-20260914-0643,Purchase7760272273\n"
            "task_stage: VERIFY\nExact action and receiver evidence.\n---\n"
        ))
        selected = self.compile("continue receipt", explicit_entities=("20260914", "7760272273"))
        self.assertEqual(selected["diagnostics"]["status"], "OK")
        self.assertEqual(selected["selected_anchor"]["anchor_id"], "2026-01-12-explicit-action-receipt")
        self.assertIsNone(selected["session_brief"])
        split = self.compile("continue receipt", explicit_entities=("20260914", "6501112223"))
        self.assertIn("REQUIRED_ENTITIES_NOT_COLOCATED", split["diagnostics"]["errors"])
        self.assertIsNone(split["session_brief"])
        self.assertEqual(record_dates("TA15-COMPLETED-DAY-20260914-0643"), [])
        self.assertEqual(record_dates("ops/heartbeat-20260914-0643/readback.json"), ["2026-09-14"])
        self.assertEqual(record_dates("ops/accounts/20260914/readback.json Merchant20260914"), [])


if __name__ == "__main__":
    unittest.main()
