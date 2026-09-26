#!/usr/bin/env python3
"""Mint a short-lived Shopify Admin API token for local operator scripts.

Shopify no longer lets merchants create legacy custom apps (permanent shpat_
tokens) in the admin. A Dev Dashboard app installed on the store instead
exchanges its client ID and secret for an Admin token that expires after about
24 hours (OAuth client_credentials grant, same flow as
ops/cloudflare/merchant-feed-worker/src/shopify-auth.js).

This script reads the app credentials from
~/.config/dresslikemommy/shopify-dev-app.json:

    {"store_domain": "dresslikemommy-com.myshopify.com",
     "client_id": "...", "client_secret": "..."}

It then writes the fresh token into the three token files that existing scripts
already read, so no other script needs to change:

    admin-api-token.json          access_token (+ expires_at, scope)
    translation-helper-token.json access_token
    shopify-admin.env             SHOPIFY_ADMIN_ACCESS_TOKEN

The token and secret are never printed. Output is the shop name, scopes and expiry.

Usage:
    python3 ops/scripts/refresh_shopify_admin_token.py            # refresh now
    python3 ops/scripts/refresh_shopify_admin_token.py --if-needed  # only when <2h left
    python3 ops/scripts/refresh_shopify_admin_token.py --setup      # save client ID/secret (hidden prompt), then refresh
"""
import getpass
import argparse
import datetime as dt
import json
import os
import pathlib
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

CONFIG_DIR = pathlib.Path.home() / ".config" / "dresslikemommy"
APP_FILE = CONFIG_DIR / "shopify-dev-app.json"
ADMIN_TOKEN_FILE = CONFIG_DIR / "admin-api-token.json"
HELPER_TOKEN_FILE = CONFIG_DIR / "translation-helper-token.json"
ENV_FILE = CONFIG_DIR / "shopify-admin.env"
API_VERSION = "2026-01"
DOMAIN_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.myshopify\.com$")
REFRESH_MARGIN = dt.timedelta(hours=2)


class TokenError(Exception):
    pass


def load_app(path=APP_FILE):
    if not path.exists():
        raise TokenError(f"missing {path} (store_domain, client_id, client_secret)")
    app = json.loads(path.read_text(encoding="utf-8"))
    for key in ("store_domain", "client_id", "client_secret"):
        if not isinstance(app.get(key), str) or not app[key].strip():
            raise TokenError(f"{path.name} has no {key}")
    if not DOMAIN_RE.match(app["store_domain"]):
        raise TokenError("store_domain must be the *.myshopify.com domain")
    return app


def setup(path=APP_FILE, domain="dresslikemommy-com.myshopify.com"):
    """Prompt for the Dev Dashboard credentials; the secret is read without echo."""
    client_id = input("Client ID: ").strip()
    client_secret = getpass.getpass("Client secret (hidden): ").strip()
    if not client_id or not client_secret:
        raise TokenError("client ID and secret are both required")
    path.parent.mkdir(parents=True, exist_ok=True)
    write_private(path, json.dumps({"store_domain": domain, "client_id": client_id, "client_secret": client_secret}, indent=2) + "\n")
    print(f"Saved {path} (mode 600).")


def exchange(app, opener=urllib.request.urlopen, now=None):
    """Return (token, scope, expires_at) from the client_credentials grant."""
    started = now or dt.datetime.now(dt.timezone.utc)
    body = urllib.parse.urlencode({
        "grant_type": "client_credentials",
        "client_id": app["client_id"],
        "client_secret": app["client_secret"],
    }).encode()
    req = urllib.request.Request(
        f"https://{app['store_domain']}/admin/oauth/access_token",
        data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded", "Accept": "application/json"},
    )
    try:
        with opener(req, timeout=30) as resp:
            data = json.loads(resp.read())
    except urllib.error.HTTPError as exc:
        # Never echo the response body: it may reflect request parameters.
        raise TokenError(f"token exchange rejected (HTTP {exc.code}); check the app is installed and the secret is current") from None
    token, expires_in = data.get("access_token"), data.get("expires_in")
    if not isinstance(token, str) or not re.fullmatch(r"[\x21-\x7e]{20,}", token):
        raise TokenError("token exchange returned no usable access_token")
    if not isinstance(expires_in, int) or not 600 <= expires_in <= 172800:
        raise TokenError("token exchange returned an unexpected expires_in")
    # Measure expiry from request start so latency cannot extend the lifetime.
    return token, str(data.get("scope", "")), started + dt.timedelta(seconds=expires_in)


def current_expiry(path=ADMIN_TOKEN_FILE):
    try:
        value = json.loads(path.read_text(encoding="utf-8")).get("expires_at")
        return dt.datetime.fromisoformat(value) if value else None
    except (OSError, ValueError):
        return None


def write_private(path, text):
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.chmod(tmp, 0o600)
    tmp.replace(path)


def store(token, scope, expires_at, app, admin_file=ADMIN_TOKEN_FILE, helper_file=HELPER_TOKEN_FILE, env_file=ENV_FILE):
    admin = {}
    if admin_file.exists():
        admin = json.loads(admin_file.read_text(encoding="utf-8"))
    admin.update({
        "store_domain": app["store_domain"],
        "access_token": token,
        "app_name": admin.get("app_name") or "Dev Dashboard app (client_credentials)",
        "auth_mode": "client_credentials",
        "scope": scope,
        "expires_at": expires_at.isoformat(),
    })
    write_private(admin_file, json.dumps(admin, indent=2) + "\n")
    write_private(helper_file, json.dumps({"access_token": token}) + "\n")
    lines = env_file.read_text(encoding="utf-8").splitlines() if env_file.exists() else []
    line = f"export SHOPIFY_ADMIN_ACCESS_TOKEN={token}"
    replaced = False
    for i, existing in enumerate(lines):
        if re.match(r"^(export\s+)?SHOPIFY_ADMIN_ACCESS_TOKEN=", existing):
            lines[i], replaced = line, True
    if not replaced:
        lines.append(line)
    write_private(env_file, "\n".join(lines) + "\n")


def verify(app, token, opener=urllib.request.urlopen):
    req = urllib.request.Request(
        f"https://{app['store_domain']}/admin/api/{API_VERSION}/graphql.json",
        data=json.dumps({"query": "{ shop { name } }"}).encode(),
        headers={"Content-Type": "application/json", "X-Shopify-Access-Token": token},
    )
    with opener(req, timeout=30) as resp:
        return json.loads(resp.read())["data"]["shop"]["name"]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--setup", action="store_true", help="prompt for and save the Dev Dashboard client ID/secret first")
    parser.add_argument("--if-needed", action="store_true", help="skip when the stored token has more than 2h left")
    args = parser.parse_args(argv)
    try:
        if args.setup:
            setup()
        app = load_app()
        expiry = current_expiry()
        if args.if_needed and expiry and expiry - dt.datetime.now(dt.timezone.utc) > REFRESH_MARGIN:
            print(f"Token still valid until {expiry.isoformat()}; nothing to do.")
            return 0
        token, scope, expires_at = exchange(app)
        shop = verify(app, token)
        store(token, scope, expires_at, app)
    except TokenError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(f"OK: {shop} | expires {expires_at.isoformat()} | scopes: {scope}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
