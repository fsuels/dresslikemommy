#!/usr/bin/env python3
"""Interactively create a local Google Ads API config outside the repo.

Run this in a terminal. It prompts for secrets without echoing them and writes
only to ~/.config/dresslikemommy/google-ads-api/google-ads.yaml.
"""

from __future__ import annotations

import getpass
import json
import os
from pathlib import Path


CONFIG_DIR = Path.home() / ".config/dresslikemommy/google-ads-api"
CONFIG_PATH = CONFIG_DIR / "google-ads.yaml"


def prompt(label: str, *, secret: bool = False, required: bool = True) -> str:
    while True:
        value = getpass.getpass(f"{label}: ").strip() if secret else input(f"{label}: ").strip()
        if value or not required:
            return value
        print("Required. Paste the value, or press Control-C to stop.")


def clean_customer_id(value: str) -> str:
    return value.replace("-", "").replace(" ", "")


def main() -> int:
    print("Google Ads API local config setup")
    print("Do not paste these values into chat. This writes outside the repo.")
    print(f"Target file: {CONFIG_PATH}")
    print()

    developer_token = prompt("Google Ads API developer_token", secret=True)
    client_id = prompt("OAuth client_id", secret=True)
    client_secret = prompt("OAuth client_secret", secret=True)
    refresh_token = prompt("OAuth refresh_token", secret=True)
    login_customer_id = clean_customer_id(
        prompt("Optional login_customer_id / manager ID without dashes (blank if none)", required=False)
    )

    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    if CONFIG_PATH.exists():
        backup_path = CONFIG_PATH.with_suffix(".yaml.bak")
        CONFIG_PATH.replace(backup_path)
        backup_path.chmod(0o600)
        print(f"Existing config backed up to: {backup_path}")

    lines = [
        "developer_token: " + json.dumps(developer_token),
        "client_id: " + json.dumps(client_id),
        "client_secret: " + json.dumps(client_secret),
        "refresh_token: " + json.dumps(refresh_token),
    ]
    if login_customer_id:
        lines.append("login_customer_id: " + json.dumps(login_customer_id))
    lines.append("use_proto_plus: true")
    CONFIG_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    CONFIG_PATH.chmod(0o600)
    print()
    print(f"Wrote config: {CONFIG_PATH}")
    print("Next check:")
    print("python3.13 ops/scripts/check_google_ads_api_config.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
