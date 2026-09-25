# German image-caption translation review

Status: PASS_LOCAL_TRANSLATION_AND_LENGTH_CHECKS.

127/127 exact English keys preserved in source order; no missing or extra keys. Translations use English keys only, not the Portuguese translations. Unicode character counts include spaces and punctuation.

| Assessed field type | Keys | Minimum | Maximum | Limit | Over limit |
|---|---:|---:|---:|---:|---:|
| Caption-like | 64 | 20 | 35 | 35 | 0 |
| Descriptive alt text | 63 | 26 | 60 | 90 | 0 |

The 90-character alt limit follows root’s fresh native UI readback, superseding the earlier 100-character task assumption. Field-role classification is based on source wording; the dictionary contains no native role metadata. Root must apply each string to its corresponding observed field.

Uncertainties: the exact key `ordinated family tops and bottoms` is truncated. Its translation assumes “coordinated”; root must confirm the actual source field before applying this entry. Mother/child descriptions without “in” are conservatively translated as clothing for those wearers, avoiding an invented claim that people appear in the image. “Swimsuits” is rendered as broad “Bademode” unless the source explicitly says one-piece.

People, relationships, colors, patterns, product-only wording, front/back views, close-ups and adult/child distinctions are preserved. No prices, offers, promises or new visual details were added. Photographs were not inspected by this worker. This dictionary is not native acceptance or image/alt compatibility evidence; root retains picture/crop verification and target-only asset ownership.

Source SHA256: `25fb1a23fc635012976e70db3611f1dde955509cea1c4a10d446519566c1ce83`
Output SHA256: `2b07bfea8e550b2767eaf131d35ce162ff42984cab213be206cdc8c35a385bfc`

## Character counts per exact source key

| Source key | Assessed role | German characters | Limit |
|---|---|---:|---:|
| Mom Dad Kids Matching Shirts | caption-like | 34 | 35 |
| Family of four in matching shirts | descriptive | 44 | 90 |
| Matching Family Shirts | caption-like | 29 | 35 |
| Family in coordinated shirts | descriptive | 42 | 90 |
| Floral Family Shirts | caption-like | 31 | 35 |
| Family in floral print shirts | descriptive | 34 | 90 |
| Family Matching Shirts | caption-like | 29 | 35 |
| Family in matching shirts | descriptive | 32 | 90 |
| Family wearing matching shirts | descriptive | 35 | 90 |
| Tropical Family Shirts | caption-like | 32 | 35 |
| Family in tropical print shirts | descriptive | 40 | 90 |
| Coordinated Family Shirts | caption-like | 26 | 35 |
| Colorful Matching Dresses | caption-like | 28 | 35 |
| Mother and child matching dresses | descriptive | 42 | 90 |
| Mom & Me Matching Dresses | caption-like | 35 | 35 |
| Matching Dresses | caption-like | 22 | 35 |
| Mother and daughter in dresses | descriptive | 30 | 90 |
| Mother Daughter Matching Dresses | caption-like | 35 | 35 |
| Mommy and me matching dresses | descriptive | 35 | 90 |
| Mommy & Me Matching Dresses | caption-like | 35 | 35 |
| Mother and child matching polka dot dresses | descriptive | 53 | 90 |
| Beach Matching Dresses | caption-like | 28 | 35 |
| Mom and child in matching dresses | descriptive | 40 | 90 |
| Casual Matching Dresses | caption-like | 30 | 35 |
| Dresses Side by Side | caption-like | 21 | 35 |
| Two matching dresses side by side | descriptive | 41 | 90 |
| Dress Up Together | caption-like | 25 | 35 |
| Woman and child in matching dresses | descriptive | 40 | 90 |
| Mother & Daughter Dresses | caption-like | 30 | 35 |
| Matching dresses in two sizes | descriptive | 37 | 90 |
| Mommy & Me Dresses | caption-like | 20 | 35 |
| Adult and child matching dresses | descriptive | 45 | 90 |
| Mom, Dad & Kids in Sync | caption-like | 34 | 35 |
| Family of four in matching outfits | descriptive | 45 | 90 |
| Matching Family Clothing | caption-like | 31 | 35 |
| Adult and child matching clothing | descriptive | 46 | 90 |
| Striped Family Looks | caption-like | 24 | 35 |
| Family wearing matching stripes | descriptive | 52 | 90 |
| Coordinated Family Sets | caption-like | 32 | 35 |
| ordinated family tops and bottoms | descriptive | 60 | 90 |
| Share a Print Together | caption-like | 28 | 35 |
| Adults and children in one print | descriptive | 47 | 90 |
| Family Matching Outfits | caption-like | 30 | 35 |
| Family wearing matching outfits | descriptive | 36 | 90 |
| Family Outfit Details | caption-like | 27 | 35 |
| Close-up of matching outfit details | descriptive | 50 | 90 |
| Match for Your Next Getaway | caption-like | 34 | 35 |
| Family posing in matching outfits | descriptive | 41 | 90 |
| Dad & Son Short-Sleeve Shirts | caption-like | 32 | 35 |
| Adult and child short-sleeve shirts | descriptive | 39 | 90 |
| Dad & Son Photo Looks | caption-like | 28 | 35 |
| Man and boy in matching shirts | descriptive | 39 | 90 |
| Father & Son Matching Shirts | caption-like | 32 | 35 |
| Adult and child matching shirts | descriptive | 44 | 90 |
| Blue Shirts for Dad & Son | caption-like | 31 | 35 |
| Blue adult and child shirts | descriptive | 35 | 90 |
| Tropical Prints for Dad & Son | caption-like | 31 | 35 |
| Matching tropical-print shirts | descriptive | 39 | 90 |
| Matching Shirts Side by Side | caption-like | 32 | 35 |
| Adult and child shirts side by side | descriptive | 43 | 90 |
| Matching Collars & Prints | caption-like | 26 | 35 |
| Collars on matching printed shirts | descriptive | 43 | 90 |
| Choose Your Shared Print | caption-like | 29 | 35 |
| Printed adult and child shirts | descriptive | 40 | 90 |
| Matching Floral Shirts | caption-like | 27 | 35 |
| Adult and child floral shirts | descriptive | 46 | 90 |
| Daddy & Me Button-Up Shirts | caption-like | 31 | 35 |
| Adult and child button-up shirts | descriptive | 41 | 90 |
| Dad & Son Hawaiian Shirts | caption-like | 31 | 35 |
| Adult and child Hawaiian shirts | descriptive | 38 | 90 |
| Matching Palm-Print Shirts | caption-like | 27 | 35 |
| Adult and child palm-print shirts | descriptive | 46 | 90 |
| Man and boy in tropical shirts | descriptive | 42 | 90 |
| Sleepwear for Mom & Mini | caption-like | 29 | 35 |
| Adult and child matching sleepwear | descriptive | 49 | 90 |
| Matching Pajama Backs | caption-like | 26 | 35 |
| matching pajama sets | descriptive | 26 | 90 |
| Mommy & Me Pajamas | caption-like | 20 | 35 |
| Adult and child matching pajamas | descriptive | 45 | 90 |
| Matching Pajama Shorts | caption-like | 27 | 35 |
| Matching pajama tops and shorts | descriptive | 41 | 90 |
| Matching Pajama Prints | caption-like | 27 | 35 |
| Matching printed pajama sets | descriptive | 37 | 90 |
| Pajama Prints Up Close | caption-like | 25 | 35 |
| Close-up of matching pajama print | descriptive | 50 | 90 |
| Mother & Daughter Pajamas | caption-like | 30 | 35 |
| Woman and girl in matching pajamas | descriptive | 42 | 90 |
| Pajamas With Playful Prints | caption-like | 31 | 35 |
| Adult and child animal-motif PJs | descriptive | 46 | 90 |
| Short-Sleeve Matching Pajamas | caption-like | 30 | 35 |
| Adult and child short-sleeve PJs | descriptive | 41 | 90 |
| Matching pajama tops and pants | descriptive | 40 | 90 |
| A Matching Bedtime Look | caption-like | 33 | 35 |
| Woman and child in matching pajamas | descriptive | 39 | 90 |
| Matching Looks for Beach Days | caption-like | 26 | 35 |
| Close-up of matching swimwear | descriptive | 39 | 90 |
| Swimwear for Mom & Mini | caption-like | 26 | 35 |
| Woman and child in swimwear by pool | descriptive | 33 | 90 |
| Mommy & Me Swimsuits | caption-like | 21 | 35 |
| Adult and child matching swimsuits | descriptive | 46 | 90 |
| Match for Your Next Pool Day | caption-like | 32 | 35 |
| Matching Swimwear Fronts | caption-like | 32 | 35 |
| Matching One-Piece Swimsuits | caption-like | 33 | 35 |
| Adult and child one-piece swimsuits | descriptive | 47 | 90 |
| Mother & Daughter Swimsuits | caption-like | 31 | 35 |
| Adult and child swimsuits | descriptive | 34 | 90 |
| Black & White Matching Swimwear | caption-like | 34 | 35 |
| Black and white matching swimsuits | descriptive | 37 | 90 |
| Matching swimwear worn at the beach | descriptive | 47 | 90 |
| Striped Swimsuits to Share | caption-like | 34 | 35 |
| Adult and child striped swimsuits | descriptive | 45 | 90 |
| Mother & Daughter Swimwear | caption-like | 31 | 35 |
| Woman and girl in matching swimwear | descriptive | 43 | 90 |
| Black Matching Swimwear | caption-like | 32 | 35 |
| Black matching swimsuits | descriptive | 32 | 90 |
| Mom & Child Matching Sweaters | caption-like | 35 | 35 |
| mother and child in matching sweaters | descriptive | 43 | 90 |
| Matching Sweater Fronts | caption-like | 25 | 35 |
| Family of four in matching sweaters | descriptive | 47 | 90 |
| Matching Family Knitwear | caption-like | 29 | 35 |
| Adult and child matching knitwear | descriptive | 55 | 90 |
| Matching Pullovers for the Family | caption-like | 31 | 35 |
| Adult and child matching pullovers | descriptive | 46 | 90 |
| Family Matching Sweaters | caption-like | 31 | 35 |
| Family wearing matching sweaters | descriptive | 37 | 90 |
| Matching Sweaters for Mom & Mini | caption-like | 31 | 35 |
| Adult and child cable-knit sweaters | descriptive | 46 | 90 |
