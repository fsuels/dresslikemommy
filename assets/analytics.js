window.dataLayer = window.dataLayer || [];
(function(){
  function getExperimentContext(){
    try {
      var cfg = window.experimentConfig || {};
      var enabled = !!cfg.enabled;
      var flags = [];
      if (cfg.flags && typeof cfg.flags === 'object') {
        for (var key in cfg.flags) {
          if (!Object.prototype.hasOwnProperty.call(cfg.flags, key)) continue;
          if (cfg.flags[key]) flags.push(key);
        }
      } else if (Array.isArray(cfg.flags)) {
        flags = cfg.flags;
      }
      return {
        experiments_enabled: enabled,
        experiment_flags: flags
      };
    } catch(e) {
      return {};
    }
  }

  function pushToDataLayer(payload){
    try {
      var exp = getExperimentContext();
      if (exp && Object.keys(exp).length) {
        payload = Object.assign({}, exp, payload);
      }
      window.dataLayer.push(payload);
    } catch(e) {}
  }

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
      pushToDataLayer({
        event: 'view_item',
        ecommerce: { items: [{ item_id: p.id, item_name: p.title, item_variant: variantId, price: price, currency: currency }] }
      });
    } catch(e) {}
  }

  function initHeroAnalytics(){
    var hero = document.querySelector('[data-hero-id="family-fit"]');
    if(!hero) return;
    var sectionId = hero.getAttribute('data-hero-section');
    var heroId = 'family_fit';
    var video = hero.querySelector('[data-hero-video]');

    if(video && 'IntersectionObserver' in window){
      var viewed = false;
      var observer = new IntersectionObserver(function(entries){
        entries.forEach(function(entry){
          if(viewed) return;
          if(entry.isIntersecting && entry.intersectionRatio >= 0.6){
            viewed = true;
            pushToDataLayer({
              event: 'hero_video_view',
              heroId: heroId,
              sectionId: sectionId
            });
            observer.disconnect();
          }
        });
      }, { threshold: [0.6] });
      observer.observe(video);
    }

  }

  function initHomepageCtas(){
    document.addEventListener('click', function(evt){
      var btn = evt.target && evt.target.closest && evt.target.closest('[data-cta-id]');
      if(!btn) return;
      var scope = btn.getAttribute('data-cta-scope') || '';
      pushToDataLayer({
        event: 'homepage_cta_click',
        ctaId: btn.getAttribute('data-cta-id'),
        ctaScope: scope,
        ctaText: btn.textContent.trim(),
        destination: btn.getAttribute('href') || '',
        productHandle: btn.getAttribute('data-product-handle') || ''
      });

      if(scope === 'hero'){
        var heroEl = btn.closest('[data-hero-id]');
        pushToDataLayer({
          event: 'hero_cta_click',
          heroId: heroEl ? heroEl.getAttribute('data-hero-id') : 'family_fit',
          sectionId: heroEl ? heroEl.getAttribute('data-hero-section') : undefined,
          ctaId: btn.getAttribute('data-cta-id'),
          ctaText: btn.textContent.trim()
        });
      }
    });
  }

  document.addEventListener('DOMContentLoaded', function(){
    pushViewItem();
    initHeroAnalytics();
    initHomepageCtas();
  });

if (typeof subscribe === 'function') {
  try {
    subscribe('cart-update', function(evt){
      try {
        var variantId = evt && (evt.productVariantId || evt.variantId);
        var pEl = document.querySelector('script[id^="ProductJSON-"]');
        if(pEl){
          var p = JSON.parse(pEl.textContent);
          var v = null;
          if(variantId){
            var vid = String(variantId);
            v = (p.variants||[]).find(x=> String(x.id)===vid) || null;
          }
          var priceCents = v ? (v.price || v.priceV2?.amount*100) : (p.price || p.variants?.[0]?.price || 0);
          var price = (typeof priceCents === 'number' ? priceCents : parseFloat(priceCents)) / 100;
          var currencyMeta = document.querySelector('meta[property="og:price:currency"]');
          var currency = (currencyMeta && currencyMeta.content) || 'USD';
          pushToDataLayer({
            event: 'add_to_cart',
            ecommerce: { items: [{ item_id: p.id, item_name: p.title, item_variant: variantId || (p.variants?.[0]?.id), price: price, currency: currency, quantity: 1 }]}
          });
          return;
        }
        pushToDataLayer({ event: 'add_to_cart' });
      } catch(e) { pushToDataLayer({ event: 'add_to_cart' }); }
    });
  } catch(e) {}
}

  document.addEventListener('click', function(e){
    var t = e.target;
    if (t && t.name === 'checkout') {
      pushToDataLayer({ event: 'begin_checkout' });
    }
  });
})();
