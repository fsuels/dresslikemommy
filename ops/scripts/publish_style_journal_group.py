#!/usr/bin/env python3
"""Audit or publish predefined Style Journal article groups."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

import publish_blog_articles as publisher


ROOT = Path(__file__).resolve().parents[2]
PUBLISH_SCRIPT = ROOT / "ops" / "scripts" / "publish_blog_articles.py"

ARTICLE_GROUPS = {
    "gap_fill": [
        "mother-daughter-matching-dresses-for-easter",
        "how-to-choose-mommy-and-me-matching-outfits-for-family-photos",
        "daddy-and-me-outfit-ideas-for-fathers-day",
        "mommy-and-me-outfits-for-every-season-complete-guide",
    ],
    "couples_rollout": [
        "matching-couple-outfits-date-night-travel-gifts",
        "couple-matching-pajamas-holidays-anniversaries-gifts",
    ],
}


def build_command(args: argparse.Namespace, handles: list[str]) -> list[str]:
    command = [
        sys.executable,
        str(PUBLISH_SCRIPT),
        "--handles",
        ",".join(handles),
        "--blog-handle",
        args.blog_handle,
        "--api-version",
        args.api_version,
    ]

    if args.execute:
        command.append("--execute")
    if args.publish:
        command.append("--publish")
    if args.update_existing:
        command.append("--update-existing")
    if args.store_domain:
        command.extend(["--store-domain", args.store_domain])
    if args.access_token:
        command.extend(["--access-token", args.access_token])

    return command


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--group", choices=sorted(ARTICLE_GROUPS), default="gap_fill")
    parser.add_argument("--blog-handle", default=publisher.DEFAULT_BLOG_HANDLE)
    parser.add_argument("--api-version", default=publisher.DEFAULT_API_VERSION)
    parser.add_argument("--store-domain", default="")
    parser.add_argument("--access-token", default="")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--publish", action="store_true")
    parser.add_argument("--update-existing", action="store_true")
    args = parser.parse_args()

    handles = ARTICLE_GROUPS[args.group]
    drafts = publisher.load_drafts(publisher.DEFAULT_ARTICLES_DIR, handles=handles)
    draft_map = {draft.handle: draft for draft in drafts}

    missing = [handle for handle in handles if handle not in draft_map]
    if missing:
      print(f"Missing drafts for group '{args.group}': {', '.join(missing)}", file=sys.stderr)
      return 1

    print(f"Style Journal group: {args.group}")
    for handle in handles:
        draft = draft_map[handle]
        image_state = "missing" if not draft.image_url else "present"
        print(
            f"- {draft.handle} | publish_date={draft.publish_date or 'unset'} | "
            f"is_published={draft.is_published} | image_url={image_state}"
        )

    command = build_command(args, handles)
    print("")
    print("Running:")
    print(" ".join(command))
    print("")

    result = subprocess.run(command, cwd=ROOT)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
