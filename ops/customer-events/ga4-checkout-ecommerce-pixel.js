/*
  Shopify Customer Events custom pixel for hosted checkout GA4 ecommerce events.
  Paste into Shopify Admin -> Settings -> Customer events -> Add custom pixel.

  This loads the existing GTM container only when checkout step events fire, so
  storefront GTM loaded by the theme is not duplicated on regular storefront pages.
*/

const GTM_CONTAINER_ID = 'GTM-5QVH4W3';

window.dataLayer = window.dataLayer || [];

const checkoutAnalyticsState = {
  gtmLoaded: false,
  lastEventSignatureByName: {},
};

function normalizeText(value) {
  if (value === null || value === undefined) return '';
  return String(value).trim();
}

function cleanObject(input) {
  const output = {};

  Object.keys(input || {}).forEach((key) => {
    const value = input[key];
    if (value === undefined || value === null || value === '') return;
    output[key] = value;
  });

  return output;
}

function parseMoney(money) {
  const amount = money && money.amount;
  const parsed = typeof amount === 'number' ? amount : parseFloat(amount);
  if (!Number.isFinite(parsed)) return null;
  return Math.round(parsed * 100) / 100;
}

function ensureCheckoutGtm() {
  if (checkoutAnalyticsState.gtmLoaded || !GTM_CONTAINER_ID) return;

  checkoutAnalyticsState.gtmLoaded = true;
  window.dataLayer.push({ 'gtm.start': Date.now(), event: 'gtm.js' });

  const script = document.createElement('script');
  script.async = true;
  script.src = `https://www.googletagmanager.com/gtm.js?id=${encodeURIComponent(
    GTM_CONTAINER_ID
  )}`;

  const head = document.head || document.getElementsByTagName('head')[0];
  if (head) {
    head.appendChild(script);
  }
}

function getCheckoutCurrency(checkout) {
  return normalizeText(checkout && checkout.currencyCode) || 'USD';
}

function getDiscountCode(checkout) {
  const discountApplications =
    checkout && Array.isArray(checkout.discountApplications) ? checkout.discountApplications : [];

  for (let i = 0; i < discountApplications.length; i += 1) {
    const application = discountApplications[i];
    if (!application || normalizeText(application.type) !== 'DISCOUNT_CODE') continue;

    const title = normalizeText(application.title);
    if (title) return title;
  }

  return '';
}

function buildCheckoutItem(lineItem, index) {
  if (!lineItem) return null;

  const variant = lineItem.variant || {};
  const product = variant.product || {};
  const quantity = parseInt(lineItem.quantity, 10);
  const resolvedQuantity = Number.isFinite(quantity) && quantity > 0 ? quantity : 1;
  const unitPrice = parseMoney(variant.price);
  const finalLinePrice = parseMoney(lineItem.finalLinePrice);
  const fallbackUnitPrice =
    unitPrice !== null
      ? unitPrice
      : finalLinePrice !== null
        ? Math.round((finalLinePrice / resolvedQuantity) * 100) / 100
        : null;

  const item = cleanObject({
    item_id: normalizeText(product.id || variant.id || lineItem.id),
    item_name: normalizeText(lineItem.title || product.title),
    item_brand: normalizeText(product.vendor),
    item_variant: normalizeText(variant.sku || variant.title || variant.id),
    item_category: normalizeText(product.type),
    price: fallbackUnitPrice,
    quantity: resolvedQuantity,
    index: index + 1,
  });

  return item.item_id || item.item_name ? item : null;
}

function buildCheckoutItems(checkout) {
  const lineItems = checkout && Array.isArray(checkout.lineItems) ? checkout.lineItems : [];
  const items = [];

  for (let i = 0; i < lineItems.length; i += 1) {
    const item = buildCheckoutItem(lineItems[i], i);
    if (item) items.push(item);
  }

  return items;
}

function buildCheckoutEcommerce(checkout, extraFields) {
  const items = buildCheckoutItems(checkout);

  return cleanObject(
    Object.assign(
      {
        currency: getCheckoutCurrency(checkout),
        value: parseMoney(checkout && checkout.totalPrice),
        coupon: getDiscountCode(checkout),
        items,
      },
      extraFields || {}
    )
  );
}

function getShippingTier(checkout) {
  const delivery = checkout && checkout.delivery;
  const selectedDeliveryOptions =
    delivery && Array.isArray(delivery.selectedDeliveryOptions)
      ? delivery.selectedDeliveryOptions
      : [];

  if (selectedDeliveryOptions.length) {
    const selectedTitle = normalizeText(selectedDeliveryOptions[0] && selectedDeliveryOptions[0].title);
    if (selectedTitle) return selectedTitle;
  }

  return normalizeText(checkout && checkout.shippingLine && checkout.shippingLine.title);
}

function getPaymentType(checkout) {
  const transactions = checkout && Array.isArray(checkout.transactions) ? checkout.transactions : [];

  for (let i = 0; i < transactions.length; i += 1) {
    const transaction = transactions[i];
    if (!transaction) continue;

    const paymentMethodName = normalizeText(
      transaction.paymentMethod && transaction.paymentMethod.name
    );
    if (paymentMethodName) return paymentMethodName;

    const paymentMethodType = normalizeText(
      transaction.paymentMethod && transaction.paymentMethod.type
    );
    if (paymentMethodType) return paymentMethodType;

    const gateway = normalizeText(transaction.gateway);
    if (gateway) return gateway;
  }

  return '';
}

function pushCheckoutEcommerceEvent(eventName, ecommerce, signatureParts) {
  const signature = signatureParts.map((part) => normalizeText(part)).join('|');
  if (checkoutAnalyticsState.lastEventSignatureByName[eventName] === signature) return;

  checkoutAnalyticsState.lastEventSignatureByName[eventName] = signature;

  ensureCheckoutGtm();
  window.dataLayer.push({ ecommerce: null });
  window.dataLayer.push({
    event: eventName,
    ecommerce,
  });
}

analytics.subscribe('checkout_shipping_info_submitted', (event) => {
  const checkout = event && event.data && event.data.checkout;
  if (!checkout) return;

  const shippingAmount = parseMoney(checkout.shippingLine && checkout.shippingLine.price);
  const shippingTier = getShippingTier(checkout);
  const ecommerce = buildCheckoutEcommerce(checkout, {
    shipping: shippingAmount,
    shipping_tier: shippingTier,
  });

  pushCheckoutEcommerceEvent('add_shipping_info', ecommerce, [
    checkout.token,
    ecommerce.value,
    ecommerce.shipping,
    ecommerce.shipping_tier,
    ecommerce.items && ecommerce.items.length,
  ]);
});

analytics.subscribe('payment_info_submitted', (event) => {
  const checkout = event && event.data && event.data.checkout;
  if (!checkout) return;

  const paymentType = getPaymentType(checkout);
  const ecommerce = buildCheckoutEcommerce(checkout, {
    payment_type: paymentType,
  });

  pushCheckoutEcommerceEvent('add_payment_info', ecommerce, [
    checkout.token,
    ecommerce.value,
    ecommerce.payment_type,
    ecommerce.items && ecommerce.items.length,
  ]);
});
