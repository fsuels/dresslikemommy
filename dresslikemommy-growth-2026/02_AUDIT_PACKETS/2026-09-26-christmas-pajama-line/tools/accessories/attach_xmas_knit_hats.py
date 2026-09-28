import sys, time
from pathlib import Path
sys.path.insert(0, "/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-26-christmas-pajama-line/tools/ai_images")
import attach_images as A
H = "christmas-knit-family-matching-hats"
D = Path("/Users/fsuels/Projects/dresslikemommy/uploads") / H / "ai"
plan = [("image1.png", "Family in matching red and green Christmas knit elf hats with pom-poms by the Christmas tree."),
        ("image3.png", "Family opening gifts on Christmas morning in matching Christmas knit hats."),
        ("image5.png", "Tree Stripe and Garland Christmas knit hats in adult and child sizes, laid out without models."),
        ("image6.png", "Mom and daughter in matching Christmas knit elf hats with pom-poms.")]
p = A.gql("query($h:String!){productByHandle(handle:$h){id status}}", {"h": H})["productByHandle"]
assert p["status"] == "DRAFT"
have = [n["alt"] for n in A.media_nodes(p["id"])]
for f, alt in plan:
    if alt not in have:
        A.upload(p["id"], D / f, alt)
for _ in range(30):
    nodes = A.media_nodes(p["id"])
    if all(n["status"] == "READY" for n in nodes): break
    time.sleep(3)
print([ (n["alt"][:40], n["status"]) for n in A.media_nodes(p["id"])])
