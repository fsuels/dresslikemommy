(() => {
  if (window.__dlmHomepageCollectionCardImagesInit) return;
  window.__dlmHomepageCollectionCardImagesInit = true;

  const CARD_SELECTOR = '[data-homepage-collection-card]';
  const IMAGE_SELECTOR = '[data-homepage-collection-image]';
  const CANDIDATE_SELECTOR = '.homepage-collection-card__image-candidates';
  const RANDOM_WINDOW_SIZE = 4;

  function normalizeCandidate(candidate) {
    if (!candidate || typeof candidate !== 'object') return null;

    const key = String(candidate.key || '').trim();
    const src = String(candidate.src || '').trim();
    if (!key || !src) return null;

    return {
      key,
      src,
      srcset: String(candidate.srcset || '').trim(),
      alt: String(candidate.alt || '').trim(),
      width: Number(candidate.width) || 0,
      height: Number(candidate.height) || 0,
    };
  }

  function shuffle(items) {
    const clone = items.slice();

    for (let index = clone.length - 1; index > 0; index -= 1) {
      const randomIndex = Math.floor(Math.random() * (index + 1));
      const currentItem = clone[index];
      clone[index] = clone[randomIndex];
      clone[randomIndex] = currentItem;
    }

    return clone;
  }

  function parseCandidates(card) {
    const script = card.querySelector(CANDIDATE_SELECTOR);
    if (!script) return [];

    try {
      const parsed = JSON.parse(script.textContent);
      if (!Array.isArray(parsed)) return [];
      return parsed.map(normalizeCandidate).filter(Boolean);
    } catch (error) {
      return [];
    }
  }

  function buildCandidateOrder(candidates) {
    if (candidates.length <= 1) return candidates.slice();

    const freshnessWindow = Math.min(RANDOM_WINDOW_SIZE, candidates.length);
    const freshCandidates = shuffle(candidates.slice(0, freshnessWindow));
    const olderCandidates = candidates.slice(freshnessWindow);

    return freshCandidates.concat(olderCandidates);
  }

  function applyCandidate(image, candidate) {
    image.src = candidate.src;

    if (candidate.srcset) {
      image.srcset = candidate.srcset;
    } else {
      image.removeAttribute('srcset');
    }

    if (candidate.alt) {
      image.alt = candidate.alt;
    }

    if (candidate.width) {
      image.width = candidate.width;
    }

    if (candidate.height) {
      image.height = candidate.height;
    }

    image.dataset.homepageCollectionImageKey = candidate.key;
    image.dataset.homepageCollectionImageSrc = candidate.src;
  }

  function reserveExistingImage(image, usedKeys, usedSrcs) {
    const existingKey = String(image.dataset.homepageCollectionImageKey || '').trim();
    const existingSrc = String(image.currentSrc || image.src || '').trim();

    if (existingKey) usedKeys.add(existingKey);
    if (existingSrc) usedSrcs.add(existingSrc);
  }

  function refreshHomepageCollectionImages(root = document) {
    const cards = Array.from(root.querySelectorAll(CARD_SELECTOR));
    if (!cards.length) return;

    const usedKeys = new Set();
    const usedSrcs = new Set();

    cards.forEach((card) => {
      const image = card.querySelector(IMAGE_SELECTOR);
      if (!image) return;

      const candidates = buildCandidateOrder(parseCandidates(card));
      if (!candidates.length) {
        reserveExistingImage(image, usedKeys, usedSrcs);
        return;
      }

      const selectedCandidate =
        candidates.find((candidate) => !usedKeys.has(candidate.key) && !usedSrcs.has(candidate.src)) ||
        candidates.find((candidate) => !usedSrcs.has(candidate.src)) ||
        candidates.find((candidate) => !usedKeys.has(candidate.key)) ||
        candidates[0];

      applyCandidate(image, selectedCandidate);
      usedKeys.add(selectedCandidate.key);
      usedSrcs.add(selectedCandidate.src);
    });
  }

  function onReady(callback) {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', callback, { once: true });
      return;
    }

    callback();
  }

  onReady(() => {
    refreshHomepageCollectionImages();
  });

  document.addEventListener('shopify:section:load', (event) => {
    refreshHomepageCollectionImages(event.target.ownerDocument || document);
  });
})();
