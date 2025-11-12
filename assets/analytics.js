window.dataLayer = window.dataLayer || [];
(function(){
  function pushViewItem(){
    try {
      var el = document.querySelector('script[id^="ProductJSON-"]');
      if(!el) return;
      var p = JSON.parse(el.textContent);
      var priceCents = p.price || (p.variants && p.variants[0] && p.variants[0].price) || 0;
      var price = (typeof priceCents === 'number' ? priceCents : parseFloat(priceCents)) / 100;
      var variantId = (p.current_variant_id) || (p.variants && p.variants[0] && p.variants[0].id) || null;
      var currencyMeta = document.querySelector('meta[property="og:price:currency"]');
      var currency = (currencyMeta && currencyMeta.content) || 'USD';
      window.dataLayer.push({
        event: 'view_item',
        ecommerce: { items: [{ item_id: p.id, item_name: p.title, item_variant: variantId, price: price, currency: currency }] }
      });
    } catch(e) {}
  }

  document.addEventListener('DOMContentLoaded', function(){
    pushViewItem();
  });

  if (typeof subscribe === 'function') {
    try {
      subscribe('cart-update', function(){ window.dataLayer.push({ event: 'add_to_cart' }); });
    } catch(e) {}
  }

  document.addEventListener('click', function(e){
    var t = e.target;
    if (t && t.name === 'checkout') {
      window.dataLayer.push({ event: 'begin_checkout' });
    }
  });
})();

