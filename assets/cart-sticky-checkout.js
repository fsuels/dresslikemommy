// Mobile cart page: sticky "Check out" bar. Shown only while the main
// #checkout button is out of view. The bar's button submits the same #cart form.
(function () {
  var bar = document.querySelector('[data-cart-sticky-checkout]');
  var main = document.getElementById('checkout');
  var footer = document.getElementById('main-cart-footer');
  if (!bar || !main || !footer || !('IntersectionObserver' in window)) return;

  var button = bar.querySelector('button');
  var amount = bar.querySelector('[data-cart-sticky-amount]');
  var mainInView = false;

  function render() {
    var show = !mainInView && !footer.classList.contains('is-empty');
    bar.classList.toggle('is-visible', show);
    if (button) button.tabIndex = show ? 0 : -1;
  }

  function syncAmount() {
    var source = footer.querySelector('.totals__total-value');
    if (source && amount && source.textContent.trim()) amount.textContent = source.textContent.trim();
    render();
  }

  new IntersectionObserver(function (entries) {
    mainInView = entries[entries.length - 1].isIntersecting;
    render();
  }).observe(main);

  var subtotal = document.getElementById('main-cart-footer-subtotal');
  if (subtotal && 'MutationObserver' in window) {
    new MutationObserver(syncAmount).observe(subtotal, { childList: true, subtree: true, characterData: true });
  }
  new MutationObserver(render).observe(footer, { attributes: true, attributeFilter: ['class'] });

  bar.classList.add('is-ready');
})();
