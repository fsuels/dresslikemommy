#!/usr/bin/env python3
"""Detect and repair drift between GitHub origin/main and the live Shopify theme.

Shopify's GitHub integration sometimes drops pushes (observed 2026-09-26/27: 26
code files on main never reached the live theme while "Update from Shopify"
sync-back commits interleaved with rapid pushes). This compares every
.liquid/.js/.css file under layout/ sections/ snippets/ assets/ blocks/ in
origin/main with the live theme by MD5 and, with --apply, writes the differing
files to the live theme via themeFilesUpsert (new snippets/assets first).
JSON (templates, config, locales) is excluded: Shopify re-serializes it and the
admin editor owns settings_data.

Usage: python3 ops/scripts/sync_live_theme_from_main.py [--apply]
Run from a clean checkout/worktree of origin/main (it reads files from `git show origin/main:<path>`).
"""
import hashlib
import json
import pathlib
import subprocess
import sys
import urllib.request

LIVE_THEME = "gid://shopify/OnlineStoreTheme/133290917985"
URL = "https://dresslikemommy-com.myshopify.com/admin/api/2025-01/graphql.json"
TOKEN = json.loads(pathlib.Path("~/.config/dresslikemommy/admin-api-token.json").expanduser().read_text())["access_token"]


def gql(query, variables=None):
    req = urllib.request.Request(URL, data=json.dumps({"query": query, "variables": variables or {}}).encode(),
                                 headers={"Content-Type": "application/json", "X-Shopify-Access-Token": TOKEN})
    out = json.loads(urllib.request.urlopen(req).read())
    if out.get("errors"):
        raise SystemExit(f"GraphQL error: {out['errors']}")
    return out["data"]


def main_file(path):
    return subprocess.check_output(["git", "show", f"origin/main:{path}"])


def live_checksums(files):
    out = {}
    for i in range(0, len(files), 50):
        d = gql("query($t:ID!,$f:[String!]!){theme(id:$t){files(first:50,filenames:$f){nodes{filename checksumMd5}}}}",
                {"t": LIVE_THEME, "f": files[i:i + 50]})
        out.update({n["filename"]: n["checksumMd5"] for n in d["theme"]["files"]["nodes"]})
    return out


def main():
    subprocess.run(["git", "fetch", "-q", "origin"], check=True)
    files = [f for f in subprocess.check_output(["git", "ls-tree", "-r", "--name-only", "origin/main", "layout", "sections", "snippets", "assets", "blocks"]).decode().split()
             if f.endswith((".liquid", ".js", ".css"))]
    live = live_checksums(files)
    drift = [f for f in files if live.get(f) != hashlib.md5(main_file(f)).hexdigest()]
    print(f"{len(files)} code files on main; {len(drift)} differ from live")
    for f in drift:
        print("  ", f, "(missing on live)" if f not in live else "")
    if "--apply" not in sys.argv or not drift:
        return
    new = [f for f in drift if f not in live]
    changed = [f for f in drift if f in live]
    for batch in (new, changed):
        for i in range(0, len(batch), 20):
            chunk = batch[i:i + 20]
            r = gql("mutation($t:ID!,$f:[OnlineStoreThemeFilesUpsertFileInput!]!){themeFilesUpsert(themeId:$t,files:$f){upsertedThemeFiles{filename} userErrors{filename message}}}",
                    {"t": LIVE_THEME, "f": [{"filename": f, "body": {"type": "TEXT", "value": main_file(f).decode("utf-8")}} for f in chunk]})
            if r["themeFilesUpsert"]["userErrors"]:
                raise SystemExit(r["themeFilesUpsert"]["userErrors"])
    live = live_checksums(drift)
    bad = [f for f in drift if live.get(f) != hashlib.md5(main_file(f)).hexdigest()]
    print(f"applied {len(drift)}; verified {len(drift) - len(bad)}; mismatches {bad}")


if __name__ == "__main__":
    main()
