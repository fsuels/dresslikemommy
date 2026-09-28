#!/usr/bin/env python3
"""Attach the owner-approved AI photoshoot images (IMAGE 1, 3, 5, 6) to a
2026 Christmas pajama DRAFT, then remove the placeholder vendor image
(owner decision 2026-09-26: "Remove it").

Only DRAFT, unpublished products are touched. The vendor image is identified by
its exact runner alt text; nothing else is deleted. Idempotent: images already
attached (same alt) are not uploaded twice.

Usage: attach_images.py handle [handle ...]
"""
from __future__ import annotations

import json
import mimetypes
import sys
import time
from pathlib import Path

import requests

ROOT = Path("/Users/fsuels/Projects/dresslikemommy")
TOOLS = ROOT / "dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-26-christmas-pajama-line/tools"
sys.path.insert(0, str(ROOT))
from ops.scripts.shopify_admin_config import load_access_token, resolve_store_domain  # noqa: E402

API = f"https://{resolve_store_domain('', fallback_domain='dresslikemommy-com.myshopify.com')}/admin/api/2025-01/graphql.json"
TOKEN = load_access_token("")


def gql(query: str, variables: dict | None = None) -> dict:
    r = requests.post(API, headers={"X-Shopify-Access-Token": TOKEN, "Content-Type": "application/json"},
                      json={"query": query, "variables": variables or {}}, timeout=120)
    r.raise_for_status()
    data = r.json()
    if data.get("errors"):
        raise RuntimeError(json.dumps(data["errors"]))
    return data["data"]


def alts_for(spec: dict) -> list[tuple[str, str]]:
    """Alt text per image, worded for what the listing actually sells."""
    name = spec["print_name"]
    mode, role = spec.get("mode", "family_christmas"), spec.get("knit_role")
    if mode == "family_sweatshirt":
        garment = "knit sweaters" if spec.get("garment") == "sweater" else "sweatshirts"
        who = {"mommy": "Mom and daughter", "daddy": "Dad and son"}.get(role, "Family")
        adult = {"mommy": "a woman", "daddy": "a man"}.get(role, "an adult")
        rest = [(f"{who} out together in matching {name} {garment}."),
                (f"{name} matching {garment} for {adult} and a child, laid out without models."),
                (f"{who} relaxing together at home in matching {name} {garment}.")]
    elif mode == "mommy_me":
        rest = [(f"Mom and daughter in matching {name} pajamas at home."),
                (f"{name} matching pajama sets for a woman and a child, laid out without models."),
                (f"Mom and daughter relaxing together in matching {name} pajamas.")]
    elif mode == "family_pet":
        rest = [(f"Dog in the {name} vest with the family at Christmas."),
                (f"{name} dog vest laid out without models."),
                (f"Dog in the {name} vest relaxing at home.")]
    else:
        rest = [(f"Family in matching {name} Christmas pajamas on Christmas morning by the tree."),
                (f"{name} matching Christmas pajama sets for an adult and a child, laid out without models."),
                (f"Family relaxing together at home in matching {name} Christmas pajamas.")]
    return [("image1.png", spec["media_alt"]), ("image3.png", rest[0]), ("image5.png", rest[1]), ("image6.png", rest[2])]


def legacy_alts(spec: dict) -> list[str]:
    name = spec["print_name"]
    return [f"Family in matching {name} Christmas pajamas on Christmas morning by the tree.",
            f"{name} matching Christmas pajama sets for an adult and a child, laid out without models.",
            f"Family relaxing together at home in matching {name} Christmas pajamas."]


def media_nodes(pid: str) -> list[dict]:
    return gql("query($id:ID!){product(id:$id){media(first:50){nodes{id alt status mediaContentType}}}}", {"id": pid})["product"]["media"]["nodes"]


def upload(pid: str, path: Path, alt: str) -> None:
    mime = mimetypes.guess_type(path.name)[0] or "image/png"
    staged = gql("""mutation($input:[StagedUploadInput!]!){stagedUploadsCreate(input:$input){
        stagedTargets{url resourceUrl parameters{name value}} userErrors{field message}}}""",
                 {"input": [{"filename": path.name, "mimeType": mime, "resource": "IMAGE", "httpMethod": "POST"}]})["stagedUploadsCreate"]
    if staged["userErrors"]:
        raise RuntimeError(staged["userErrors"])
    t = staged["stagedTargets"][0]
    with path.open("rb") as fh:
        requests.post(t["url"], data={p["name"]: p["value"] for p in t["parameters"]},
                      files={"file": (path.name, fh, mime)}, timeout=180).raise_for_status()
    res = gql("""mutation($pid:ID!,$media:[CreateMediaInput!]!){productCreateMedia(productId:$pid,media:$media){
        media{id} mediaUserErrors{field message}}}""",
              {"pid": pid, "media": [{"originalSource": t["resourceUrl"], "mediaContentType": "IMAGE", "alt": alt}]})["productCreateMedia"]
    if res["mediaUserErrors"]:
        raise RuntimeError(res["mediaUserErrors"])


def main() -> None:
    report = {}
    for handle in sys.argv[1:]:
        spec = json.loads((TOOLS / "specs" / f"{handle}.json").read_text(encoding="utf-8"))
        folder = ROOT / "uploads" / handle / "ai"
        plan = alts_for(spec)
        missing = [f for f, _ in plan if not (folder / f).is_file()]
        if missing:
            raise SystemExit(f"{handle}: missing {missing}")
        product = gql("query($h:String!){productByHandle(handle:$h){id status publishedAt}}", {"h": handle})["productByHandle"]
        if not product or product["status"] != "DRAFT" or product["publishedAt"]:
            raise SystemExit(f"{handle}: not an unpublished DRAFT")
        pid = product["id"]
        existing_alts = [n["alt"] for n in media_nodes(pid)]
        if [a for a in existing_alts] == [alt for _, alt in plan]:  # already attached and vendor image removed: idempotent no-op
            print(handle, "OK", len(existing_alts), "images (already attached)")
            continue
        for fname, alt in plan:
            if alt in existing_alts and fname != "image1.png":
                continue
            if fname == "image1.png" and existing_alts.count(alt) >= 2:
                continue  # vendor image and image1 share the hero alt until the vendor image is removed
            upload(pid, folder / fname, alt)
        # wait for processing, then drop the vendor placeholder (the FIRST media with the hero alt)
        for _ in range(30):
            nodes = media_nodes(pid)
            if all(n["status"] == "READY" for n in nodes):
                break
            time.sleep(3)
        nodes = media_nodes(pid)
        hero = [n for n in nodes if n["alt"] == spec["media_alt"]]
        if len(hero) == 2:
            res = gql("""mutation($pid:ID!,$ids:[ID!]!){productDeleteMedia(productId:$pid,mediaIds:$ids){
                deletedMediaIds mediaUserErrors{field message}}}""", {"pid": pid, "ids": [hero[0]["id"]]})["productDeleteMedia"]
            if res["mediaUserErrors"]:
                raise RuntimeError(res["mediaUserErrors"])
        final = media_nodes(pid)
        expected = [alt for _, alt in plan]
        ok = [n["alt"] for n in final] == expected and all(n["status"] == "READY" for n in final)
        report[handle] = {"product_id": pid, "media": [(n["alt"][:40], n["status"]) for n in final], "ok": ok}
        print(handle, "OK" if ok else "CHECK", len(final), "images")
    out = TOOLS / "ai_images" / "logs" / "attach_report.json"
    prev = json.loads(out.read_text()) if out.exists() else {}
    prev.update(report)
    out.write_text(json.dumps(prev, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
