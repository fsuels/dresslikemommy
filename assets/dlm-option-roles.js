/*
 * Language-independent option roles for the PDP variant pickers.
 *
 * The visible option names are translated ("Maat", "Kleur", "Méret"), so word lists
 * (snippets/product-variant-picker.liquid) always miss some language. The shop's primary
 * language product JSON (the un-prefixed /products/<handle>.js) carries the untranslated names;
 * this marks each native option group with data-option-role="size" | "color" | "other" from
 * those names, and component-product-desktop-ux.css hides the size and colour groups above the
 * matching-set builder, which has its own pickers for them.
 */
(function () {
  'use strict';

  function roleFor(name) {
    var n = String(name || '').toLowerCase();
    if (/\bsize\b/.test(n)) return 'size';
    if (/\bcolou?r\b/.test(n)) return 'color';
    return 'other';
  }

  function mark(groups, options) {
    if (!groups.length || groups.length !== options.length) return 0;
    groups.forEach(function (group, index) {
      group.setAttribute('data-option-role', roleFor(options[index] && options[index].name));
    });
    return groups.length;
  }

  function handleFromPath(pathname) {
    var match = String(pathname || '').match(/\/products\/([^\/?#]+)/);
    return match ? match[1] : '';
  }

  function start() {
    var info = document.querySelector('[data-has-matching-set="true"]');
    var selects = document.querySelector('variant-selects');
    var handle = handleFromPath(window.location && window.location.pathname);
    if (!info || !selects || !handle || typeof window.fetch !== 'function') return;
    window
      .fetch('/products/' + handle + '.js', { credentials: 'same-origin', headers: { Accept: 'application/json' } })
      .then(function (response) { return response.ok ? response.json() : null; })
      .then(function (product) {
        if (!product || !Array.isArray(product.options)) return;
        var groups = Array.prototype.slice.call(selects.querySelectorAll(':scope > .product-form__input'));
        mark(groups, product.options);
      })
      ['catch'](function () {});
  }

  window.DLMOptionRoles = { roleFor: roleFor, mark: mark, handleFromPath: handleFromPath };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start);
  else start();
})();
