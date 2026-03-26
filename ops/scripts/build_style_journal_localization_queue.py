#!/usr/bin/env python3
"""Build a localization rollout plan for winning Style Journal articles."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import List

import publish_blog_articles as publisher


ROOT = Path(__file__).resolve().parents[2]

LOCALIZATION_CANDIDATES = [
    {
        "locale": "fr",
        "handle": "how-to-choose-mommy-and-me-matching-outfits-for-family-photos",
        "reason": "aligns with the current family-outfit coordination query opportunity in French notes",
    },
    {
        "locale": "fr",
        "handle": "the-complete-guide-to-family-matching-outfits",
        "reason": "broad family-matching pillar that can accumulate localized internal links over time",
    },
    {
        "locale": "es",
        "handle": "best-family-swimsuits-for-beach-vacations-and-pool-days",
        "reason": "aligns with current swim-intent demand and summer seasonality in Spanish",
    },
    {
        "locale": "es",
        "handle": "mother-daughter-matching-swimsuits-complete-guide-for-summer-2026",
        "reason": "supports the mother-daughter swim cluster with strong seasonal purchase intent",
    },
]


def build_plan(winner_handles: List[str]) -> str:
    unique_winners = {handle.strip() for handle in winner_handles if handle.strip()}
    drafts = publisher.load_drafts(publisher.DEFAULT_ARTICLES_DIR)
    draft_map = {draft.handle: draft for draft in drafts}

    lines = [
        "# Style Journal Localization Queue",
        "",
    ]

    if not unique_winners:
        lines.append("No winner handles were supplied, so no localization rollout is queued.")
        lines.append("")
        lines.append("Pass `--winner-handles handle-one,handle-two` after English articles prove collection-click traction.")
        return "\n".join(lines) + "\n"

    lines.append("## Winners Evaluated")
    lines.append("")
    for handle in sorted(unique_winners):
        draft = draft_map.get(handle)
        if draft is None:
            lines.append(f"- `{handle}` (not found in `ops/content/style-journal/articles/`)")
        else:
            lines.append(f"- `{handle}`: {draft.title}")

    lines.append("")
    lines.append("## Eligible Rollout")
    lines.append("")

    eligible = [candidate for candidate in LOCALIZATION_CANDIDATES if candidate["handle"] in unique_winners]
    if not eligible:
        lines.append("None of the supplied winners are in the current strategy-approved localization queue.")
        lines.append("")
        lines.append("Keep the rollout limited to the strategy candidates unless the keyword map is updated.")
        return "\n".join(lines) + "\n"

    lines.append("| Locale | Handle | Title | Why first |")
    lines.append("| --- | --- | --- | --- |")
    for candidate in eligible:
        draft = draft_map.get(candidate["handle"])
        title = draft.title if draft else "(draft missing)"
        lines.append(
            f"| `{candidate['locale']}` | `{candidate['handle']}` | {title} | {candidate['reason']} |"
        )

    lines.append("")
    lines.append("## Execution Notes")
    lines.append("")
    lines.append("- Localize titles, summaries, body copy, and in-body anchor text together.")
    lines.append("- Keep collection destinations aligned with the localized article intent instead of copying English anchor phrasing verbatim.")
    lines.append("- Do not translate additional English drafts until the next winner set is confirmed.")

    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--winner-handles", default="", help="Comma-separated English winner article handles")
    parser.add_argument("--output", default="", help="Optional output path for the generated markdown plan")
    args = parser.parse_args()

    plan = build_plan([part.strip() for part in args.winner_handles.split(",") if part.strip()])

    if args.output:
        output_path = (ROOT / args.output).resolve() if not Path(args.output).is_absolute() else Path(args.output)
        output_path.write_text(plan, encoding="utf-8")
        print(f"Wrote {output_path}")
    else:
        print(plan, end="")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
