/**
 * Minimal experiment harness.
 * Reads data attributes emitted from layout/theme.liquid and exposes
 * experiment info via window.dataLayer + console (design-mode only).
 */
(function () {
  if (typeof window === 'undefined' || !document || !document.body) return;

  var body = document.body;
  var enabled = body.dataset.experimentsEnabled === 'true';
  var notes = body.dataset.experimentNotes || '';
  var flags = (body.dataset.experimentFlags || '')
    .split(' ')
    .map(function (flag) {
      return flag.trim();
    })
    .filter(function (flag) {
      return flag.length > 0;
    });

  window.dataLayer = window.dataLayer || [];
  window.dataLayer.push({
    event: 'experiments_ready',
    experiments_enabled: enabled,
    experiment_flags: flags,
    experiment_notes: notes
  });

  if (!enabled || !window.Shopify || !Shopify.designMode) {
    return;
  }

  console.info('[experiments]', 'flags:', flags, notes ? 'notes: ' + notes : '');
})();
