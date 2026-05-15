#!/usr/bin/env python3
"""Check local Google Ads API config without printing secrets.

This is an operator-side helper. It never writes credentials to the repo and
redacts any present secret-like values in output.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path


SECURE_CONFIG_DIR = Path.home() / ".config/dresslikemommy/google-ads-api"
SECURE_CONFIG_PATH = SECURE_CONFIG_DIR / "google-ads.yaml"
DEFAULT_HOME_CONFIG_PATH = Path.home() / "google-ads.yaml"
ENV_PATH_KEY = "GOOGLE_ADS_CONFIGURATION_FILE_PATH"

REQUIRED_OAUTH_FIELDS = ("client_id", "client_secret", "refresh_token")
REQUIRED_ENV_OAUTH_FIELDS = tuple(f"GOOGLE_ADS_{field.upper()}" for field in REQUIRED_OAUTH_FIELDS)


def parse_simple_yaml(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip().strip("'\"")
        if key:
            values[key] = value
    return values


def config_candidates() -> list[Path]:
    candidates: list[Path] = []
    env_path = os.environ.get(ENV_PATH_KEY)
    if env_path:
        candidates.append(Path(env_path).expanduser())
    candidates.extend([SECURE_CONFIG_PATH, DEFAULT_HOME_CONFIG_PATH])
    seen: set[Path] = set()
    unique: list[Path] = []
    for candidate in candidates:
        resolved = candidate.expanduser()
        if resolved not in seen:
            unique.append(resolved)
            seen.add(resolved)
    return unique


def present_env_config() -> dict[str, bool]:
    keys = [
        "GOOGLE_ADS_DEVELOPER_TOKEN",
        "GOOGLE_ADS_LOGIN_CUSTOMER_ID",
        *REQUIRED_ENV_OAUTH_FIELDS,
        "GOOGLE_ADS_USE_APPLICATION_DEFAULT_CREDENTIALS",
        "GOOGLE_ADS_JSON_KEY_FILE_PATH",
    ]
    return {key: bool(os.environ.get(key)) for key in keys}


def evaluate_yaml_config(path: Path) -> dict[str, object]:
    values = parse_simple_yaml(path)
    has_developer_token = bool(values.get("developer_token"))
    has_oauth = all(bool(values.get(field)) for field in REQUIRED_OAUTH_FIELDS)
    has_adc = values.get("use_application_default_credentials", "").lower() == "true"
    has_service_account = bool(values.get("json_key_file_path"))
    return {
        "path": str(path),
        "exists": True,
        "has_developer_token": has_developer_token,
        "has_login_customer_id": bool(values.get("login_customer_id")),
        "has_oauth_client_id": bool(values.get("client_id")),
        "has_oauth_client_secret": bool(values.get("client_secret")),
        "has_refresh_token": bool(values.get("refresh_token")),
        "has_application_default_credentials_flag": has_adc,
        "has_json_key_file_path": has_service_account,
        "ready": has_developer_token and (has_oauth or has_adc or has_service_account),
        "auth_mode": (
            "oauth_refresh_token"
            if has_oauth
            else "application_default_credentials"
            if has_adc
            else "service_account"
            if has_service_account
            else "missing_auth"
        ),
    }


def evaluate() -> dict[str, object]:
    candidates = config_candidates()
    checked_paths = [str(path) for path in candidates]
    existing = [path for path in candidates if path.exists()]
    yaml_results = [evaluate_yaml_config(path) for path in existing]
    env = present_env_config()
    env_has_oauth = all(env[key] for key in REQUIRED_ENV_OAUTH_FIELDS)
    env_ready = env["GOOGLE_ADS_DEVELOPER_TOKEN"] and (
        env_has_oauth
        or env["GOOGLE_ADS_USE_APPLICATION_DEFAULT_CREDENTIALS"]
        or env["GOOGLE_ADS_JSON_KEY_FILE_PATH"]
    )
    ready_yaml = next((item for item in yaml_results if item["ready"]), None)
    return {
        "ready": bool(ready_yaml or env_ready),
        "ready_source": ready_yaml["path"] if ready_yaml else "environment" if env_ready else "",
        "checked_paths": checked_paths,
        "yaml_results": yaml_results,
        "environment_presence": env,
        "next_setup_target": str(SECURE_CONFIG_PATH),
        "safe_template_command": (
            "python3.13 ops/scripts/check_google_ads_api_config.py --write-template"
        ),
        "run_forecast_command": (
            "python3.13 dresslikemommy-growth-2026/02_AUDIT_PACKETS/"
            "2026-05-14-automation-cpc-validation-decision-kit/"
            "run_google_ads_api_cpc_forecast.py --customer-id 3990976848"
        ),
    }


def write_template() -> Path:
    SECURE_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    template_path = SECURE_CONFIG_DIR / "google-ads.yaml.example"
    if not template_path.exists():
        template_path.write_text(
            "\n".join(
                [
                    "# Copy to google-ads.yaml in this same directory and replace placeholders.",
                    "# Keep the real google-ads.yaml outside the repo.",
                    "developer_token: INSERT_GOOGLE_ADS_DEVELOPER_TOKEN",
                    "client_id: INSERT_OAUTH_CLIENT_ID",
                    "client_secret: INSERT_OAUTH_CLIENT_SECRET",
                    "refresh_token: INSERT_OAUTH_REFRESH_TOKEN",
                    "# Optional for manager accounts. Leave blank or remove if not needed.",
                    "login_customer_id: INSERT_MANAGER_CUSTOMER_ID_WITHOUT_DASHES",
                    "use_proto_plus: true",
                    "",
                ]
            ),
            encoding="utf-8",
        )
        template_path.chmod(0o600)
    return template_path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-template", action="store_true")
    args = parser.parse_args()

    template_path = write_template() if args.write_template else None
    result = evaluate()
    if template_path:
        result["template_written"] = str(template_path)
    print(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return 0 if result["ready"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
