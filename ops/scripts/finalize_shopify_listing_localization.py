#!/usr/bin/env python3
"""Run the mandatory localization closeout after a Shopify listing create/update.

This is the synchronous listing-workflow gate. It deliberately overrides the
background worker's five-minute minimum age because a generated listing runner
must not report success before its new product translations are complete.
"""

from __future__ import annotations

import argparse
import json
import re
import shlex
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_TRANSLATION_PYTHON = Path("/usr/bin/python3")
HANDLE_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


@dataclass(frozen=True)
class GateStep:
    name: str
    command: list[str]
    report_path: Path | None = None


def normalize_handles(raw: str) -> list[str]:
    handles = sorted({item.strip() for item in raw.split(",") if item.strip()})
    if not handles:
        raise ValueError("At least one product handle is required.")
    invalid = [handle for handle in handles if not HANDLE_PATTERN.fullmatch(handle)]
    if invalid:
        raise ValueError(f"Invalid Shopify handle(s): {', '.join(invalid)}")
    return handles


def add_locales(command: list[str], locales: str) -> list[str]:
    if locales.strip():
        command.extend(["--locales", locales.strip()])
    return command


def build_gate_steps(
    *,
    repo_root: Path,
    python_executable: Path,
    handles: list[str],
    work_dir: Path,
    locales: str = "",
) -> list[GateStep]:
    scripts = repo_root / "ops" / "scripts"
    handles_arg = ",".join(handles)
    runtime = str(python_executable)

    admin_before_json = work_dir / "admin_translation_before_size_repair.json"
    admin_before_csv = work_dir / "admin_translation_before_size_repair.csv"
    size_execute_json = work_dir / "size_chart_execute.json"
    size_execute_csv = work_dir / "size_chart_execute.csv"
    admin_after_json = work_dir / "admin_translation_after_size_repair.json"
    admin_after_csv = work_dir / "admin_translation_after_size_repair.csv"
    size_readback_json = work_dir / "size_chart_readback.json"
    size_readback_csv = work_dir / "size_chart_readback.csv"
    variant_json = work_dir / "variant_mapping_readback.json"
    variant_csv = work_dir / "variant_mapping_readback.csv"

    return [
        GateStep(
            "translate_full_product",
            add_locales(
                [
                    runtime,
                    str(scripts / "poll_shopify_product_translations.py"),
                    "--handles",
                    handles_arg,
                    "--min-age-seconds",
                    "0",
                    "--execute",
                    "--force-refresh",
                ],
                locales,
            ),
        ),
        GateStep(
            "audit_full_product_before_size_repair",
            add_locales(
                [
                    runtime,
                    str(scripts / "audit_shopify_product_translation_completeness.py"),
                    "--handles",
                    handles_arg,
                    "--report-json",
                    str(admin_before_json),
                    "--report-csv",
                    str(admin_before_csv),
                    "--fail-on-issues",
                ],
                locales,
            ),
            admin_before_json,
        ),
        GateStep(
            "repair_localized_size_charts",
            add_locales(
                [
                    runtime,
                    str(scripts / "repair_localized_product_size_charts.py"),
                    "--handles",
                    handles_arg,
                    "--execute",
                    "--report-json",
                    str(size_execute_json),
                    "--report-csv",
                    str(size_execute_csv),
                ],
                locales,
            ),
            size_execute_json,
        ),
        GateStep(
            "audit_full_product_after_size_repair",
            add_locales(
                [
                    runtime,
                    str(scripts / "audit_shopify_product_translation_completeness.py"),
                    "--handles",
                    handles_arg,
                    "--report-json",
                    str(admin_after_json),
                    "--report-csv",
                    str(admin_after_csv),
                    "--fail-on-issues",
                ],
                locales,
            ),
            admin_after_json,
        ),
        GateStep(
            "audit_localized_size_charts",
            add_locales(
                [
                    runtime,
                    str(scripts / "repair_localized_product_size_charts.py"),
                    "--handles",
                    handles_arg,
                    "--report-json",
                    str(size_readback_json),
                    "--report-csv",
                    str(size_readback_csv),
                    "--fail-on-missing",
                ],
                locales,
            ),
            size_readback_json,
        ),
        GateStep(
            "audit_variant_size_chart_mapping",
            add_locales(
                [
                    runtime,
                    str(scripts / "audit_localized_size_chart_variant_mapping.py"),
                    "--handles",
                    handles_arg,
                    "--report-json",
                    str(variant_json),
                    "--report-csv",
                    str(variant_csv),
                    "--fail-on-unmatched",
                ],
                locales,
            ),
            variant_json,
        ),
    ]


def load_report(path: Path | None) -> dict[str, Any] | None:
    if not path or not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def output_tail(value: str, limit: int = 6000) -> str:
    value = value.strip()
    return value[-limit:] if len(value) > limit else value


def write_closeout_report(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def execute_steps(
    steps: list[GateStep],
    *,
    repo_root: Path,
    handles: list[str],
    report_path: Path,
) -> int:
    records: list[dict[str, Any]] = []
    for step in steps:
        print(f"[listing-localization] {step.name}: {shlex.join(step.command)}", flush=True)
        result = subprocess.run(
            step.command,
            cwd=repo_root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if result.stdout:
            print(result.stdout.rstrip(), flush=True)
        if result.stderr:
            print(result.stderr.rstrip(), file=sys.stderr, flush=True)

        record = {
            "name": step.name,
            "command": step.command,
            "exit_code": result.returncode,
            "stdout_tail": output_tail(result.stdout),
            "stderr_tail": output_tail(result.stderr),
            "report": load_report(step.report_path),
        }
        records.append(record)
        if result.returncode != 0:
            write_closeout_report(
                report_path,
                {
                    "handles": handles,
                    "status": "failed",
                    "failed_step": step.name,
                    "steps": records,
                },
            )
            print(
                f"[listing-localization] FAILED at {step.name}; listing closeout is not complete. "
                f"Evidence: {report_path}",
                file=sys.stderr,
            )
            return result.returncode

    write_closeout_report(
        report_path,
        {
            "handles": handles,
            "status": "passed",
            "failed_step": "",
            "steps": records,
        },
    )
    print(f"[listing-localization] PASS. Evidence: {report_path}", flush=True)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--handles", required=True, help="Comma-separated Shopify product handles.")
    parser.add_argument("--locales", default="", help="Defaults to every published non-primary Shopify locale.")
    parser.add_argument(
        "--python",
        default=str(DEFAULT_TRANSLATION_PYTHON),
        help="Python runtime with the Shopify/translation dependencies installed.",
    )
    parser.add_argument(
        "--report-json",
        default="",
        help="Closeout evidence path. Defaults to ops/listings/<handle>-localization-closeout.json for one handle.",
    )
    parser.add_argument(
        "--print-plan",
        action="store_true",
        help="Print the exact gate commands without running Shopify reads or writes.",
    )
    args = parser.parse_args()

    try:
        handles = normalize_handles(args.handles)
    except ValueError as exc:
        parser.error(str(exc))

    python_executable = Path(args.python).expanduser()
    if not python_executable.is_file():
        parser.error(f"Translation Python runtime does not exist: {python_executable}")

    if args.report_json:
        report_path = Path(args.report_json).expanduser()
        if not report_path.is_absolute():
            report_path = REPO_ROOT / report_path
    elif len(handles) == 1:
        report_path = REPO_ROOT / "ops" / "listings" / f"{handles[0]}-localization-closeout.json"
    else:
        parser.error("--report-json is required when closing out multiple handles.")

    with tempfile.TemporaryDirectory(prefix="dlm-listing-localization-") as temp_dir:
        steps = build_gate_steps(
            repo_root=REPO_ROOT,
            python_executable=python_executable,
            handles=handles,
            work_dir=Path(temp_dir),
            locales=args.locales,
        )
        if args.print_plan:
            print(
                json.dumps(
                    {
                        "handles": handles,
                        "report_json": str(report_path),
                        "steps": [{"name": step.name, "command": step.command} for step in steps],
                    },
                    indent=2,
                    ensure_ascii=False,
                )
            )
            return 0
        return execute_steps(
            steps,
            repo_root=REPO_ROOT,
            handles=handles,
            report_path=report_path,
        )


if __name__ == "__main__":
    raise SystemExit(main())
