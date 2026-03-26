#!/usr/bin/env python3
"""Shared local Shopify Admin credential helpers for operator-run scripts."""

from __future__ import annotations

import json
import os
import shlex
from pathlib import Path
from typing import Dict, Iterable, List


DEFAULT_CONFIG_DIR = Path.home() / ".config" / "dresslikemommy"
DEFAULT_ENV_PATH = DEFAULT_CONFIG_DIR / "shopify-admin.env"
DEFAULT_ADMIN_TOKEN_PATH = DEFAULT_CONFIG_DIR / "admin-api-token.json"
DEFAULT_TRANSLATION_TOKEN_PATH = DEFAULT_CONFIG_DIR / "translation-helper-token.json"
DEFAULT_TOKEN_PATH = DEFAULT_ADMIN_TOKEN_PATH
DEFAULT_STORE_DOMAIN = os.environ.get("SHOPIFY_STORE_DOMAIN", "")


def clean(value: str) -> str:
    return (value or "").strip()


def normalize_store_domain(raw_domain: str) -> str:
    value = clean(raw_domain)
    value = value.replace("https://", "").replace("http://", "")
    return value.rstrip("/")


def parse_env_assignments(env_path: Path = DEFAULT_ENV_PATH) -> Dict[str, str]:
    if not env_path.exists():
        return {}

    assignments: Dict[str, str] = {}
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()
        key, separator, value = line.partition("=")
        if not separator:
            continue
        parsed_value = value.strip()
        if parsed_value:
            try:
                parts = shlex.split(parsed_value)
            except ValueError:
                parts = [parsed_value.strip("\"'")]
            parsed_value = parts[0] if parts else ""
        assignments[key.strip()] = parsed_value
    return assignments


def resolve_store_domain(
    explicit_domain: str = "",
    *,
    env_path: Path = DEFAULT_ENV_PATH,
    fallback_domain: str = "",
) -> str:
    env_assignments = parse_env_assignments(env_path)
    domain = (
        normalize_store_domain(explicit_domain)
        or normalize_store_domain(os.environ.get("SHOPIFY_STORE_DOMAIN", ""))
        or normalize_store_domain(env_assignments.get("SHOPIFY_STORE_DOMAIN", ""))
        or normalize_store_domain(fallback_domain)
    )
    if not domain:
        raise RuntimeError(
            "Missing Shopify store domain. Pass --store-domain or define SHOPIFY_STORE_DOMAIN "
            f"in the shell or {env_path}."
        )
    return domain


def load_access_token(
    explicit_token: str = "",
    token_path: Path = DEFAULT_TOKEN_PATH,
    *,
    env_path: Path = DEFAULT_ENV_PATH,
    extra_token_paths: Iterable[Path] = (),
) -> str:
    token = clean(explicit_token) or clean(os.environ.get("SHOPIFY_ADMIN_ACCESS_TOKEN", ""))
    if token:
        return token

    env_assignments = parse_env_assignments(env_path)
    token = clean(env_assignments.get("SHOPIFY_ADMIN_ACCESS_TOKEN", ""))
    if token:
        return token

    candidate_paths: List[Path] = []
    for path in (token_path, DEFAULT_ADMIN_TOKEN_PATH, DEFAULT_TRANSLATION_TOKEN_PATH, *extra_token_paths):
        expanded = Path(path).expanduser()
        if expanded not in candidate_paths:
            candidate_paths.append(expanded)

    for candidate_path in candidate_paths:
        if not candidate_path.exists():
            continue
        payload = json.loads(candidate_path.read_text(encoding="utf-8"))
        token = clean(payload.get("access_token"))
        if token:
            return token

    checked_paths = ", ".join(str(path) for path in candidate_paths)
    raise RuntimeError(
        "Missing Shopify Admin access token. Set SHOPIFY_ADMIN_ACCESS_TOKEN, define it in "
        f"{env_path}, or create one of: {checked_paths}."
    )
