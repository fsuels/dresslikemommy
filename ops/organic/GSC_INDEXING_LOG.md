
## 2026-09-29 03:35 UTC request-indexing batch

- https://www.dresslikemommy.com/blogs/news/matching-couples-christmas-pajamas-and-sweaters | not on Google (unknown to Google) | N/A | Indexing requested (CEO session)
- https://www.dresslikemommy.com/collections/christmas-pajamas | on Google | Sep 25, 2026 | Indexing requested
- https://www.dresslikemommy.com/collections/matching-family-christmas-outfits | on Google | Sep 26, 2026 | Indexing requested
- https://www.dresslikemommy.com/collections/christmas-sweaters | on Google | Sep 9, 2026 | Indexing requested
- https://www.dresslikemommy.com/collections/family-sweaters | on Google | Sep 28, 2026 | Indexing requested
- https://www.dresslikemommy.com/collections/thanksgiving-family-outfits | on Google | Sep 28, 2026 | Indexing requested
- https://www.dresslikemommy.com/collections/christmas-tops | on Google | Aug 10, 2026 | REJECTED: live test says "Excluded by 'noindex' tag" (noindex detected in robots meta tag); fix the noindex, then re-request

## 2026-09-29 13:50 UTC request-indexing batch (CEO loop)

- https://www.dresslikemommy.com/blogs/news/daddy-and-me-christmas-outfits | on Google (already indexed) | Indexing requested
- https://www.dresslikemommy.com/blogs/news/matching-family-christmas-shirts | on Google (already indexed) | Indexing requested
- https://www.dresslikemommy.com/collections/couples | on Google | Sep 28, 2026 | Indexing requested
- https://www.dresslikemommy.com/blogs/news/best-fall-colors-for-family-matching-looks | on Google | Sep 27, 2026 | Indexing requested
- https://www.dresslikemommy.com/blogs/news/october-family-style-cozy-matching-looks-for-autumn | on Google | Aug 15, 2026 | Indexing requested

## 2026-09-29 16:55 UTC request-indexing attempt (CEO loop)

- https://www.dresslikemommy.com/blogs/news/matching-family-shirts-for-pictures | not on Google (unknown to Google) | N/A | REQUEST BLOCKED: "Quota exceeded" (daily indexing quota used up); retry next UTC day
- https://www.dresslikemommy.com/blogs/news/family-christmas-card-photo-ideas | not inspected (quota) | retry next UTC day

## 2026-09-30 00:55 UTC request-indexing attempt (CEO loop)

- https://www.dresslikemommy.com/blogs/news/matching-family-shirts-for-pictures | on Google (indexed) | no request needed
- https://www.dresslikemommy.com/blogs/news/father-and-son-matching-button-up-shirts | not on Google (unknown to Google) | REQUEST BLOCKED: "Quota Exceeded" again at 00:55Z (quota is not resetting at 00:00 UTC; likely Pacific-time day, so try after ~07:00Z)
- Other I1 URLs not inspected (quota).

## 2026-09-30 06:52 UTC inspection (CEO loop)

Inspection works again (no quota error); all inspected URLs report "URL is on Google / Page is indexed", so no request was needed:
- /blogs/news/father-and-son-matching-button-up-shirts, /babys-first-christmas-matching-family-outfits, /matching-family-cruise-outfits, /new-years-eve-matching-family-outfits, /mother-daughter-matching-dresses-guide, /family-christmas-card-photo-ideas | indexed
- /nl/collections/dresses | indexed

## 2026-10-01 00:55 UTC (CEO loop)

BLOCKED: Chrome's Search Console is signed in as a different Google account than the property owner's, and shows "Oops, you don't have access to this property" for sc-domain:dresslikemommy.com. Account switch is a stop condition, so no change was made. Pending: /blogs/news/matching-family-hawaiian-outfits (published 2026-10-01 00:24Z).

## 2026-10-01 04:55 UTC (CEO loop)

Browser 1 loaded the property.
- https://www.dresslikemommy.com/blogs/news/matching-family-pajamas-sizing-newborn-to-adult | not on Google (unknown to Google) | N/A | Indexing requested
- Next URL (winter-sweatshirts) not inspected: extension contention (tab left the group after the first request). Pending: hawaiian, daddy-daughter-dance, mommy-and-me-winter-sweatshirts-and-loungewear.

## 2026-10-01T05:08Z (main session, Browser 1)
- https://www.dresslikemommy.com/collections/matching-family-sweatshirts | not on Google (unknown) | Indexing requested
- https://www.dresslikemommy.com/blogs/news/mommy-and-me-winter-sweatshirts-and-loungewear | not on Google (unknown) | Indexing requested
- https://www.dresslikemommy.com/blogs/news/daddy-daughter-dance-matching-outfits | ON GOOGLE (indexed on its own ~3.5 h after publish) | no request needed
- https://www.dresslikemommy.com/blogs/news/matching-family-hawaiian-outfits | not on Google (unknown) | Indexing requested
- Pending: none from 2026-10-01 so far.

## 2026-10-01T23:00Z (CEO loop, Browser 1, property loaded)
- https://www.dresslikemommy.com/blogs/news/one-family-outfit-for-thanksgiving-and-christmas | ON GOOGLE (indexed on its own) | no request needed
- Pending: none. Next publishes (#15a, #16, #19, #20) are after 00:00Z 10-02.

## 2026-10-02T00:58Z (CEO loop, Browser 1, property loaded)
- https://www.dresslikemommy.com/blogs/news/matching-family-halloween-pajamas | not on Google (unknown) | Indexing requested
- Pending: none.
