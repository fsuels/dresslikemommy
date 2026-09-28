"""Remove Grinch-branded product blocks (trademark risk) from published articles."""
import json, re, sys
sys.path.insert(0, "/private/tmp/claude-501/-Users-fsuels-Projects-dresslikemommy/4297430a-559f-4c33-8ff6-032d877466c9/scratchpad")
from gql import gql
arts = {a["handle"]: a for a in json.load(open("articles_before.json"))}
R = {}
for h in ["how-to-style-cozy-mommy-and-me-looks-in-january", "best-fall-colors-for-family-matching-looks", "september-style-guide-transitional-family-matching-looks"]:
    aid = arts[h]["id"]
    cur = gql('query($id:ID!){article(id:$id){body}}', {"id": aid})["article"]["body"]
    new = cur
    # product block: <h3>..Grinch..</h3> ... up to and including the Shop link paragraph
    new = re.sub(r'<h3>[^<]*grinch[^<]*</h3>.*?<p><a href="/products/[^"]*grinch[^"]*"[^>]*>.*?</a></p>', "", new, flags=re.I | re.S)
    # standalone image paragraphs of Grinch items
    new = re.sub(r'<p>\s*<img[^>]*grinch[^>]*>\s*</p>', "", new, flags=re.I | re.S)
    assert "grinch" not in new.lower(), (h, re.findall(r'.{0,80}grinch.{0,80}', new, re.I)[:3])
    assert len(new) > 0.5 * len(cur), h
    res = gql('mutation($id:ID!,$a:ArticleUpdateInput!){articleUpdate(id:$id,article:$a){article{id} userErrors{field message}}}', {"id": aid, "a": {"body": new}})["articleUpdate"]
    assert not res["userErrors"], res
    R[aid] = {"handle": h, "before_body": cur, "removed_chars": len(cur) - len(new)}
    print(h, "removed", len(cur) - len(new), "chars")
json.dump(R, open("receipts_grinch_removal.json", "w"), indent=1)
