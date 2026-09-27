#!/usr/bin/env python3
"""Attach reviewed IMAGE 1/3/5/6 to a RESTORED (previously live) product.

Unlike attach_images.py (new drafts, vendor placeholder removed), restored
products keep their existing gallery: the 4 photoshoot images are uploaded and
moved to the front (positions 1-4); older photos follow, which also raises the
Merchant Center "images per offer" signal. Idempotent by alt text.
Usage: attach_restored.py handle [handle ...]   (handles listed in restored_jobs.json)
"""
import json
import pathlib
import sys
import time
import urllib.request

ROOT = pathlib.Path("/Users/fsuels/Projects/dresslikemommy")
HERE = pathlib.Path(__file__).resolve().parent
TOKEN = json.loads(pathlib.Path("~/.config/dresslikemommy/admin-api-token.json").expanduser().read_text())["access_token"]
URL = "https://dresslikemommy-com.myshopify.com/admin/api/2025-01/graphql.json"
LABELS = {"image1.png": "family in matching {n} Christmas pajamas by the tree",
          "image3.png": "Christmas morning in matching {n} family pajamas",
          "image5.png": "{n} matching pajama sets for adult and child, product view",
          "image6.png": "family relaxing together in matching {n} pajamas"}


def gql(query, variables=None):
    req = urllib.request.Request(URL, data=json.dumps({"query": query, "variables": variables or {}}).encode(),
                                 headers={"Content-Type": "application/json", "X-Shopify-Access-Token": TOKEN})
    out = json.loads(urllib.request.urlopen(req).read())
    if out.get("errors"):
        raise SystemExit(f"GraphQL error: {out['errors']}")
    return out["data"]


def upload(pid, path, alt):
    t = gql("mutation($i:[StagedUploadInput!]!){stagedUploadsCreate(input:$i){stagedTargets{url resourceUrl parameters{name value}} userErrors{message}}}",
            {"i": [{"resource": "IMAGE", "filename": path.name, "mimeType": "image/png", "httpMethod": "POST"}]})["stagedUploadsCreate"]["stagedTargets"][0]
    boundary = "----dlmrestored"
    body = b""
    for p in t["parameters"]:
        body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"{p['name']}\"\r\n\r\n{p['value']}\r\n".encode()
    body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{path.name}\"\r\nContent-Type: image/png\r\n\r\n".encode() + path.read_bytes() + f"\r\n--{boundary}--\r\n".encode()
    urllib.request.urlopen(urllib.request.Request(t["url"], data=body, headers={"Content-Type": f"multipart/form-data; boundary={boundary}"}))
    gql("mutation($pid:ID!,$m:[CreateMediaInput!]!){productCreateMedia(productId:$pid,media:$m){mediaUserErrors{message}}}",
        {"pid": pid, "m": [{"originalSource": t["resourceUrl"], "mediaContentType": "IMAGE", "alt": alt}]})


def main():
    jobs = json.loads((HERE / "restored_jobs.json").read_text())
    for handle in sys.argv[1:]:
        pid = "gid://shopify/Product/" + jobs[handle]
        folder = ROOT / "uploads" / handle / "ai"
        name = gql("query($id:ID!){product(id:$id){title}}", {"id": pid})["product"]["title"].split(" - ")[0].replace("Christmas Pajamas", "").replace("Pajama Set", "").replace("Pajamas", "").strip(' "-')
        plan = [(f, LABELS[f].format(n=name)) for f in ("image1.png", "image3.png", "image5.png", "image6.png")]
        existing = {n["alt"] for n in gql("query($id:ID!){product(id:$id){media(first:50){nodes{alt}}}}", {"id": pid})["product"]["media"]["nodes"]}
        for f, alt in plan:
            if alt not in existing:
                upload(pid, folder / f, alt)
        for _ in range(30):
            nodes = gql("query($id:ID!){product(id:$id){media(first:50){nodes{id alt status}}}}", {"id": pid})["product"]["media"]["nodes"]
            ours = [next((n for n in nodes if n["alt"] == alt), None) for _, alt in plan]
            if all(o and o["status"] == "READY" for o in ours):
                break
            time.sleep(4)
        moves = [{"id": o["id"], "newPosition": str(i)} for i, o in enumerate(ours)]
        gql("mutation($id:ID!,$m:[MoveInput!]!){productReorderMedia(id:$id,moves:$m){mediaUserErrors{message}}}", {"id": pid, "m": moves})
        time.sleep(3)
        final = gql("query($id:ID!){product(id:$id){media(first:50){nodes{alt status}}}}", {"id": pid})["product"]["media"]["nodes"]
        ok = [n["alt"] for n in final[:4]] == [a for _, a in plan] and all(n["status"] == "READY" for n in final[:4])
        print(handle[:50], "OK" if ok else "CHECK", f"{len(final)} media")


if __name__ == "__main__":
    main()
