"""Planned copy for the 2026-09-28 GSC English SEO fixes (see README.md).

Every string is written from store data only: collection membership, product
types and existing store promises (standard shipping included, size chart on
every product page). No stock, warehouse, review or urgency claims.
"""

SHIPPING = "Standard shipping is included, and each product page shows its estimated delivery window."

COLLECTIONS = {
    # GSC: 3.7K impressions, pos 50.9; top queries "mommy and me outfits",
    # "mommy and me clothes", "mom and daughter matching outfits".
    "mommy-and-me": {
        "seo_title": "Mommy and Me Outfits – Matching Mother Daughter Clothes",
        "seo_description": "Mommy and me outfits: matching mother daughter dresses, pajamas, swimsuits, sweaters and sets, sized separately for mom and girls. Shipping included.",
        "body": f"""<p>Mommy and me outfits put you and your daughter in the same print, so everyday moments, birthdays and family photos feel a little more special. This collection holds our mother daughter matching clothes: dresses, pajamas, swimsuits, sweaters and two-piece sets, with mom's size and the girls' size chosen separately on each product.</p>
<h2>Find your matching mother daughter look</h2>
<ul>
<li><a href="/collections/mother-daughter-matching-dresses">Mother daughter matching dresses</a> for parties, church, photos and holidays</li>
<li><a href="/collections/pajamas">Mommy and me pajamas</a> for sleepovers, movie nights and holiday mornings</li>
<li><a href="/collections/swimsuits">Mommy and me swimsuits</a> for the pool, the beach and cruises</li>
<li><a href="/collections/sweaters">Mommy and me sweaters and cardigans</a> for fall and winter</li>
</ul>
<h2>How to choose</h2>
<p><strong>Start with the occasion.</strong> Florals and sundresses suit spring and summer; knits, plaids and long sleeves work for fall photos and the holidays. <strong>Size each person separately</strong> with the size chart on every product page: compare bust and waist for mom and height for your daughter. If she is between sizes, size up so the outfit lasts longer.</p>
<p>Want dad and brother in the picture too? See <a href="/collections/matching-outfits">family matching outfits</a>. {SHIPPING}</p>""",
    },
    # GSC: 3.38K impressions, pos 40.9; queries "his and hers matching clothes",
    # "men and women matching outfits", "matching couple outfits".
    "couples": {
        "seo_title": "Matching Couple Outfits – His and Hers Matching Clothes",
        "seo_description": "Matching couple outfits: his and hers sweaters, Christmas pajamas, heart tees and tropical shirts for men and women, in separate adult sizes. Shipping included.",
        "body": f"""<p>Matching couple outfits let the two of you coordinate without dressing identically: the same knit, print or holiday pattern, cut for men and for women. Here you'll find his and hers matching clothes for the season: cable-knit and Fair Isle sweaters, matching Christmas pajamas, heart-graphic tees and sweatshirts, and tropical shirt-and-dress sets for vacations.</p>
<h2>Ideas for matching as a couple</h2>
<ul>
<li><strong>Holiday cards and Christmas morning:</strong> <a href="/collections/christmas-pajamas">matching Christmas pajamas</a> or <a href="/collections/christmas-sweaters">Christmas sweaters</a>.</li>
<li><strong>Date nights and fall photos:</strong> coordinating knits in burgundy, navy or cream.</li>
<li><strong>Trips and cruises:</strong> a floral shirt for him and a matching dress for her.</li>
</ul>
<h2>How to order for two</h2>
<p>Each person is a separate choice. Pick his size and style, add it to your bag, then pick hers and add it too. Check the size chart on each product page, since men's and women's cuts measure differently. Planning to include the kids later? Most styles also come in <a href="/collections/matching-outfits">family matching sizes</a>. {SHIPPING}</p>""",
    },
    # GSC: "mommy and me matching pajamas" 316 impressions, pos 10.4, 0 clicks;
    # Google shows the homepage, not this page. The H1 was just "Pajamas".
    "pajamas": {
        "title": "Mommy and Me Pajamas",
        "seo_title": "Mommy and Me Matching Pajamas – Mother Daughter PJ Sets",
        "seo_description": "Mommy and me matching pajamas: soft mother daughter PJ sets and nightgowns in cotton and gauze prints, long or short sleeve, sized for mom and girls.",
        "body": f"""<p>Mommy and me matching pajamas are the easiest way to match: comfy, photo-ready and worn again every week. This collection is only mother daughter pajamas: button-up PJ sets, cotton and gauze sleepwear and nightgowns in the same print for mom and her girl.</p>
<h2>Choosing mommy and me PJs</h2>
<p><strong>Season:</strong> long-sleeve sets and multi-layer cotton gauze suit fall and winter; short-sleeve sets and nightgowns are cooler for spring and summer. <strong>Print:</strong> florals, gingham, fruit and animal prints photograph well on holiday mornings and birthdays. <strong>Sizing:</strong> pajamas are meant to be relaxed, so size each person with the chart on the product page and go up if your daughter is between sizes.</p>
<p>Want the whole family in pajamas? Shop <a href="/collections/family-pajamas">matching family pajamas</a> or <a href="/collections/christmas-pajamas">matching family Christmas pajamas</a>. {SHIPPING}</p>""",
    },
    # GSC: "family matching shirts" 1.11K impr pos 16.8 and "matching family
    # shirts" 956 impr pos 18, 0 clicks; Google ranks one heart-tee product
    # plus this collection. Retitle this collection to own the shirts term.
    "family-tops": {
        "title": "Family Matching Shirts & Tops",
        "seo_title": "Family Matching Shirts – Tees, Sweatshirts & Button-Ups",
        "seo_description": "Family matching shirts for mom, dad and kids: matching T-shirts, sweatshirts, sweaters and button-up shirts, sized per person from baby to adult.",
        "body": f"""<p>Family matching shirts are the simplest way to coordinate everyone: pick one design and choose a size for each person, from baby to adult. This collection covers matching family T-shirts, sweatshirts, knit sweaters and button-up shirts.</p>
<h2>Which matching family shirts to choose</h2>
<ul>
<li><strong>T-shirts:</strong> heart, stripe and graphic tees for birthdays, trips, theme-park days and casual photos.</li>
<li><strong>Button-up shirts:</strong> tropical, palm and plaid prints for vacations, cruises and dressier pictures.</li>
<li><strong>Sweatshirts and sweaters:</strong> crewnecks and knits for fall photos, <a href="/collections/thanksgiving-family-outfits">Thanksgiving</a> and the holidays.</li>
</ul>
<p><strong>Sizing:</strong> each shirt lists separate adult and kids' sizes, and the size chart on every product page shows chest and length. Pair a shirt with jeans or shorts everyone already owns, or see <a href="/collections/matching-outfits">family matching outfits</a> for full sets and dresses. {SHIPPING}</p>""",
    },
    # GSC: "matching family sweaters" 286 impr pos 26.5; this page already gets
    # 272 of them (no cannibalization). Put the exact phrase first.
    "family-sweaters": {
        "seo_title": "Matching Family Sweaters, Cardigans & Sweatshirts",
        "seo_description": "Matching family sweaters for mom, dad and kids: cable knits, Fair Isle, cardigans and crewneck sweatshirts for fall photos, Thanksgiving and Christmas.",
        "body": f"""<p>Matching family sweaters make fall and winter photos look planned while keeping everyone warm. This collection brings together family matching knits, cardigans and crewneck sweatshirts, sized per person from kids to adults.</p>
<h2>Picking a matching family sweater</h2>
<p><strong>For fall and Thanksgiving:</strong> cable knits, heart graphics and neutral crewnecks in burgundy, navy, cream and gray; see our <a href="/collections/thanksgiving-family-outfits">Thanksgiving family outfits</a>. <strong>For Christmas:</strong> reindeer, Santa and Fair Isle designs; see <a href="/collections/christmas-sweaters">Christmas sweaters</a>. <strong>For everyday:</strong> sweatshirts wash easily and layer over tees.</p>
<p><strong>Sizing:</strong> knits vary by style, so check the size chart on each product page for chest and length. If someone is between sizes, go up for a relaxed fit. Shopping for just mom and daughter? See <a href="/collections/sweaters">mommy and me sweaters</a>. {SHIPPING}</p>""",
    },
}

# GSC: ~690 Thanksgiving impressions in 3 months, 0 clicks; no collection
# existed, Google ranked a 2016-dated blog post at ~pos 30.
THANKSGIVING = {
    "handle": "thanksgiving-family-outfits",
    "title": "Matching Family Thanksgiving Outfits",
    "seo_title": "Matching Family Thanksgiving Outfits – Sweaters & Plaid",
    "seo_description": "Matching family Thanksgiving outfits: plaid button-ups, cable-knit sweaters, cardigans and fall sweatshirts for mom, dad and kids, sized per person.",
    "body": f"""<p>Matching family Thanksgiving outfits look great at the dinner table and in the group photo. Everything here is chosen for November: plaid button-up shirts, cable-knit and Fair Isle sweaters, cardigans and cozy crewneck sweatshirts in warm fall colors, with a separate size for every family member.</p>
<h2>Thanksgiving outfit ideas</h2>
<ul>
<li><strong>Classic plaid:</strong> matching plaid button-ups for the whole family, easy to pair with jeans.</li>
<li><strong>Cozy knits:</strong> burgundy, navy, red and charcoal sweaters and cardigans, including mommy and me and daddy and me pairs.</li>
<li><strong>Relaxed and comfy:</strong> heart and graphic sweatshirts for a long day of cooking, football and leftovers.</li>
</ul>
<h2>Tips for Thanksgiving photos</h2>
<p>Pick one color family (burgundy and cream, or navy and gray) and let everyone wear a piece in it; it looks coordinated without being identical. Size each person with the chart on the product page. Thanksgiving is on Thursday, November 26, 2026: check the estimated delivery window on each product page and order early so everything arrives before dinner.</p>
<p>Looking ahead to December? See <a href="/collections/christmas-pajamas">matching family Christmas pajamas</a> and <a href="/collections/family-sweaters">matching family sweaters</a>. Standard shipping is included.</p>""",
    "members": [
        "red-plaid-family-matching-tops",
        "burgundy-ruffle-mommy-and-me-sweaters",
        "burgundy-trim-crew-daddy-and-me-sweaters",
        "nordic-yoke-family-matching-sweaters",
        "cable-horse-family-matching-tops",
        "navy-pearl-gingham-mommy-and-me-sweaters",
        "navy-cable-crew-daddy-and-me-sweaters",
        "family-matching-cable-knit-sweaters-heart-embroidered-unisex-pullovers",
        "family-matching-red-cable-knit-cardigans-elegant-heart-button-design",
        "charcoal-cream-collar-mommy-and-me-sweaters",
        "charcoal-layered-daddy-and-me-sweaters",
        "red-cable-cardigan-mommy-and-me-sweaters",
        "red-cable-crew-daddy-and-me-sweaters",
        "red-lace-bow-mommy-and-me-sweaters",
        "red-striped-cuff-daddy-and-me-sweaters",
        "matching-family-striped-cardigans-navy-and-red-heart-embroidery-knit-sweaters-for-mom-dad-and-kids",
        "together-heart-family-matching-sweaters",
        "cream-heart-mommy-and-me-cardigans",
        "navy-gingham-bow-mommy-and-me-cardigans",
        "color-block-mommy-and-me-sweaters",
        "black-and-white-stripe-mommy-and-me-sweaters",
        "family-matching-oversized-heart-patch-sweaters-trendy-streetwear-style",
        "pom-pom-star-family-matching-sweaters",
        "little-heart-family-matching-sweatshirts",
        "little-lamb-family-matching-sweatshirts",
        "starry-sky-family-matching-sweatshirts",
        "moon-and-star-family-matching-sweatshirts",
        "smiley-heart-family-matching-sweatshirts",
        "eternal-bliss-hearts-family-matching-sweatshirts",
        "good-luck-smile-family-matching-sweatshirts",
    ],
}

# The heart T-shirt product gets ~1.8K impressions for the shirts queries at
# pos ~17 with 0 clicks. Put the searched phrase first in its title tag.
PRODUCT_SEO_TITLES = {
    "matching-family-minimalist-heart-t-shirt-set-simple-love-design-in-4-colors":
        "Matching Family Shirts – Minimalist Heart T-Shirts, 4 Colors",
}

THANKSGIVING_LINK_P = (
    '<p><strong>Shop the looks:</strong> see our <a href="/collections/thanksgiving-family-outfits">'
    "matching family Thanksgiving outfits</a>: plaid shirts, cozy knits and fall sweatshirts in a size for everyone.</p>"
)
