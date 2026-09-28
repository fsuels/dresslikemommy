"""Rewrite the ranking Thanksgiving article and link the others to the new collection."""
import json, sys, html
sys.path.insert(0, "/private/tmp/claude-501/-Users-fsuels-Projects-dresslikemommy/4297430a-559f-4c33-8ff6-032d877466c9/scratchpad")
from gql import gql
import plan

P = json.load(open("/private/tmp/claude-501/-Users-fsuels-Projects-dresslikemommy/4297430a-559f-4c33-8ff6-032d877466c9/scratchpad/tg_products.json"))
COL = "/collections/thanksgiving-family-outfits"

def card(h, blurb):
    p = P[h]
    return (f'<h3>{html.escape(p["title"])}</h3>'
            f'<p><img src="{p["img"]}&width=800" alt="{html.escape(p["alt"])}" loading="lazy" width="800" style="max-width:100%;height:auto;border-radius:12px;"></p>'
            f'<p>{blurb} <a href="/products/{h}">See sizes and details</a></p>')

TITLE = "Matching Family Thanksgiving Outfits: Ideas for Dinner and Photos"
SUMMARY = "Matching family Thanksgiving outfit ideas for 2026: plaid shirts, cozy knits and fall sweatshirts for mom, dad and kids, plus color, sizing and photo tips."
BODY = f"""<p>Matching family Thanksgiving outfits make the dinner table and the group photo look planned without anyone feeling overdressed. The trick is choosing clothes that are warm, comfortable enough for a long meal, and in colors that suit November light. Below are the looks we'd pick this year, all from our <a href="{COL}">matching family Thanksgiving outfits</a> collection, where each family member chooses their own size.</p>
<h2>1. Classic plaid for the whole family</h2>
<p>Plaid is the easiest Thanksgiving match: it reads as "fall" in photos, and a button-up works over a tee for kids and dads alike.</p>
{card("red-plaid-family-matching-tops", "Red and green plaid button-ups in adult and kids sizes; wear them open over a white tee or buttoned with jeans.")}
<h2>2. Cozy knits in burgundy and cream</h2>
<p>Burgundy is the color of the season. Pair a cardigan for mom and daughter with a crewneck for dad and son, and the family matches without wearing identical pieces.</p>
{card("burgundy-ruffle-mommy-and-me-sweaters", "Mommy and me burgundy cardigans with lace ruffle trim, a softer take on the family knit.")}
{card("burgundy-trim-crew-daddy-and-me-sweaters", "The daddy and me pair: burgundy crewnecks with cream trim to sit beside the cardigans.")}
<h2>3. Navy knits for a classic look</h2>
<p>Navy looks polished at a formal dinner and hides the occasional gravy drip.</p>
{card("navy-pearl-gingham-mommy-and-me-sweaters", "Navy cable-knit cardigans with gingham collars and pearl details for mom and daughter.")}
{card("navy-cable-crew-daddy-and-me-sweaters", "Matching navy cable crewnecks for dad and son.")}
<h2>4. Everyone in one sweater</h2>
<p>If you want the whole family in the same design, a patterned or cable-knit crewneck is the simplest choice.</p>
{card("nordic-yoke-family-matching-sweaters", "Cream and gray knits with a Nordic yoke, from kids to adult sizes.")}
{card("cable-horse-family-matching-tops", "Cream cable knits with a small horse patch, relaxed enough for the whole day.")}
<h2>5. Comfy sweatshirts for a long day</h2>
<p>Cooking, football and a second helping of pie call for something relaxed. Matching sweatshirts still look coordinated in photos.</p>
{card("little-heart-family-matching-sweatshirts", "Burgundy crewneck sweatshirts with a small heart, for the whole family.")}
<h2>Tips for Thanksgiving family photos</h2>
<ul>
<li><strong>Pick one color family.</strong> Burgundy and cream, or navy and gray, and give everyone a piece in it.</li>
<li><strong>Take the photo before dinner.</strong> Natural light fades early in late November, and outfits are still spotless.</li>
<li><strong>Size for comfort.</strong> Use the size chart on each product page, and size up if someone is between sizes; knits should feel relaxed at the table.</li>
<li><strong>Order early.</strong> Thanksgiving is Thursday, November 26, 2026. Each product page shows its estimated delivery window, so check it before you order. Standard shipping is included.</li>
</ul>
<p>Planning past Thanksgiving? See <a href="/collections/family-sweaters">matching family sweaters</a> and <a href="/collections/christmas-pajamas">matching family Christmas pajamas</a> for December.</p>"""

R = {}
aid = "gid://shopify/Article/559651979361"
before = gql('query($id:ID!){article(id:$id){title summary body}}', {"id": aid})["article"]
R[aid] = {"before": before}
res = gql('mutation($id:ID!,$a:ArticleUpdateInput!){articleUpdate(id:$id,article:$a){article{id title} userErrors{field message}}}',
          {"id": aid, "a": {"title": TITLE, "summary": SUMMARY, "body": BODY}})["articleUpdate"]
assert not res["userErrors"], res
R[aid]["after_title"] = res["article"]["title"]

arts = {a["handle"]: a for a in json.load(open("articles_before.json"))}
for h in ["cozy-matching-outfits-for-the-thanksgiving-holiday", "thanksgiving-family-matching-outfit-ideas", "mommy-and-me-thanksgiving-style-guide", "fall-family-photo-outfits-for-november"]:
    a = arts[h]
    cur = gql('query($id:ID!){article(id:$id){body}}', {"id": a["id"]})["article"]["body"]
    if COL in cur:
        continue
    # insert after the first text paragraph (the one after the lead image)
    idx = cur.find("</p>", cur.find("</p>") + 4)
    assert idx > 0, h
    new = cur[: idx + 4] + plan.THANKSGIVING_LINK_P + cur[idx + 4 :]
    res = gql('mutation($id:ID!,$a:ArticleUpdateInput!){articleUpdate(id:$id,article:$a){article{id} userErrors{field message}}}',
              {"id": a["id"], "a": {"body": new}})["articleUpdate"]
    assert not res["userErrors"], res
    R[a["id"]] = {"handle": h, "before_body": cur, "inserted": plan.THANKSGIVING_LINK_P}
json.dump(R, open("receipts_articles.json", "w"), indent=1)
print("updated", len(R))
