# Enable Apple Pay & Shop Pay — DressLikeMommy

These are Shopify admin settings that need to be toggled on manually. They cannot be enabled through theme code.

## Apple Pay Setup

1. Go to **Shopify Admin** → **Settings** → **Payments**
2. Under **Shopify Payments**, click **Manage**
3. Scroll to **Accelerated checkouts**
4. Check the box for **Apple Pay**
5. Click **Save**

**Requirements:**
- Shopify Payments must be enabled as your payment provider
- Your store must use HTTPS (enabled by default on Shopify)
- Apple Pay will appear automatically on Safari browsers and Apple devices

## Shop Pay Setup

1. Go to **Shopify Admin** → **Settings** → **Payments**
2. Under **Shopify Payments**, click **Manage**
3. Scroll to **Accelerated checkouts**
4. Check the box for **Shop Pay**
5. Click **Save**

**Benefits:**
- Shop Pay has a 1.72x higher conversion rate than regular checkout (Shopify data)
- Returning customers can check out with one tap
- Appears in both cart page and cart drawer dynamic checkout buttons

## Google Pay Setup (Bonus)

1. Same location: **Settings** → **Payments** → **Manage Shopify Payments**
2. Check **Google Pay** under accelerated checkouts
3. Click **Save**

## Where They Appear

Once enabled, these payment methods will automatically appear:
- In the **cart page** (the dynamic checkout buttons section is already coded in your theme)
- In the **cart drawer** (if you add `{{ content_for_additional_checkout_buttons }}` — currently not in the drawer)
- On **product pages** with Buy Now buttons
- At **checkout**

## Verification

After enabling, test by:
1. Adding a product to cart
2. Going to the cart page
3. Below the "Checkout" button, you should see Apple Pay / Shop Pay / Google Pay buttons
4. On mobile Safari, you should see the Apple Pay button

---
*No theme code changes required — these are admin-level settings.*
