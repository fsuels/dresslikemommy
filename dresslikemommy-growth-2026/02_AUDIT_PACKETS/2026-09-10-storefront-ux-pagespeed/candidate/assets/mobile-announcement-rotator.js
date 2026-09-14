(() => {
  const MOBILE_MEDIA_QUERY = '(max-width: 989px)';
  const ROTATE_EVERY_MS = 3200;
  const FADE_DURATION_MS = 220;

  const mobileMedia = window.matchMedia(MOBILE_MEDIA_QUERY);
  const activeRotators = new WeakMap();

  const hasEmoji = (value) => /\p{Extended_Pictographic}/u.test(value);

  const addEmoji = (value) => {
    const text = value.trim();
    if (!text || hasEmoji(text)) return text;

    if (/shipping/i.test(text)) return `🚚 ${text}`;
    if (/return/i.test(text)) return `↩️ ${text}`;
    if (/secure|checkout/i.test(text)) return `🔒 ${text}`;
    return `✨ ${text}`;
  };

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
    stopRotator(messageNode);

    if (!mobileMedia.matches) {
      messageNode.textContent = originalText;
      return;
    }

    const parts = originalText
      .split('|')
      .map((part) => part.trim())
      .filter(Boolean);

    if (parts.length <= 1) {
      messageNode.textContent = addEmoji(originalText);
      return;
    }

    let index = 0;
    messageNode.style.opacity = '1';
    messageNode.style.transition = `opacity ${FADE_DURATION_MS}ms ease`;
    messageNode.textContent = addEmoji(parts[index]);

    const intervalId = window.setInterval(() => {
      messageNode.style.opacity = '0';
      window.setTimeout(() => {
        index = (index + 1) % parts.length;
        messageNode.textContent = addEmoji(parts[index]);
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
