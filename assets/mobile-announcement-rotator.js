(() => {
  const MOBILE_MEDIA_QUERY = '(max-width: 989px)';
  const ROTATE_EVERY_MS = 3200;
  const FADE_DURATION_MS = 220;

  const mobileMedia = window.matchMedia(MOBILE_MEDIA_QUERY);
  const activeRotators = new WeakMap();

  const originalMarkup = new WeakMap();

  const stopRotator = (messageNode) => {
    const state = activeRotators.get(messageNode);
    if (state?.intervalId) window.clearInterval(state.intervalId);
    activeRotators.delete(messageNode);
  };

  const setupRotator = (messageNode) => {
    if (!messageNode) return;

    const originalText = (messageNode.dataset.mobileAnnouncementOriginal || messageNode.textContent || '').trim();
    if (!originalText) return;

    messageNode.dataset.mobileAnnouncementOriginal = originalText;
    if (!originalMarkup.has(messageNode)) originalMarkup.set(messageNode, messageNode.innerHTML);
    stopRotator(messageNode);

    if (!mobileMedia.matches) {
      messageNode.innerHTML = originalMarkup.get(messageNode);
      messageNode.style.opacity = '';
      return;
    }

    const parts = originalText
      .split('|')
      .map((part) => part.trim())
      .filter(Boolean);

    if (parts.length <= 1) {
      messageNode.textContent = originalText;
      return;
    }

    let index = 0;
    messageNode.style.opacity = '1';
    messageNode.style.transition = `opacity ${FADE_DURATION_MS}ms ease`;
    messageNode.textContent = parts[index];

    const intervalId = window.setInterval(() => {
      messageNode.style.opacity = '0';
      window.setTimeout(() => {
        index = (index + 1) % parts.length;
        messageNode.textContent = parts[index];
        messageNode.style.opacity = '1';
      }, FADE_DURATION_MS);
    }, ROTATE_EVERY_MS);

    activeRotators.set(messageNode, { intervalId });
  };

  const init = (root = document) => {
    const scope = root instanceof Element ? root : document;
    scope.querySelectorAll('.announcement-bar__message > span').forEach(setupRotator);
  };

  document.addEventListener('DOMContentLoaded', () => init(document));

  document.addEventListener('shopify:section:load', (event) => {
    init(event.target || document);
  });

  mobileMedia.addEventListener('change', () => {
    init(document);
  });
})();
