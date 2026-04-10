(() => {
  if (window.__dlmHomepageCollectionCardImagesInit) return;
  window.__dlmHomepageCollectionCardImagesInit = true;

  const CARD_SELECTOR = '[data-homepage-collection-card]';
  const IMAGE_SELECTOR = '[data-homepage-collection-image]';
  const CANDIDATE_SELECTOR = '.homepage-collection-card__image-candidates';
  const RESERVED_IMAGE_SELECTOR = '[data-homepage-reserve-image]';
  const SPOTLIGHT_CARD_SELECTOR = '[data-homepage-spotlight-card]';
  const SPOTLIGHT_IMAGE_SELECTOR = '[data-homepage-spotlight-image]';
  const SPOTLIGHT_CANDIDATE_SELECTOR = '.homepage-spotlight-card__product-candidates';
  const SPOTLIGHT_CAPTION_SELECTOR = '[data-homepage-spotlight-caption]';
  const SPOTLIGHT_PRICE_SELECTOR = '[data-homepage-spotlight-price]';
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

  function normalizeSpotlightCandidate(candidate) {
    if (!candidate || typeof candidate !== 'object') return null;

    const productId = Number(candidate.productId) || 0;
    const variantId = Number(candidate.variantId) || 0;
    const imageKey = String(candidate.imageKey || '').trim();
    const imageSrc = String(candidate.imageSrc || '').trim();
    const productUrl = String(candidate.url || '').trim();

    if (!productId || !imageKey || !imageSrc || !productUrl) return null;

    return {
      productId,
      variantId,
      handle: String(candidate.handle || '').trim(),
      title: String(candidate.title || '').trim(),
      vendor: String(candidate.vendor || '').trim(),
      variant: String(candidate.variant || '').trim(),
      priceCents: Number(candidate.priceCents) || 0,
      category1: String(candidate.category1 || '').trim(),
      subcategory: String(candidate.subcategory || '').trim(),
      subcategory2: String(candidate.subcategory2 || '').trim(),
      type: String(candidate.type || '').trim(),
      style: String(candidate.style || '').trim(),
      pattern: String(candidate.pattern || '').trim(),
      url: productUrl,
      caption: String(candidate.caption || '').trim(),
      priceHtml: String(candidate.priceHtml || '').trim(),
      imageKey,
      imageSrc,
      imageSrcset: String(candidate.imageSrcset || '').trim(),
      imageAlt: String(candidate.imageAlt || '').trim(),
      imageWidth: Number(candidate.imageWidth) || 0,
      imageHeight: Number(candidate.imageHeight) || 0,
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

  function parseSpotlightCandidates(card) {
    const script = card.querySelector(SPOTLIGHT_CANDIDATE_SELECTOR);
    if (!script) return [];

    try {
      const parsed = JSON.parse(script.textContent);
      if (!Array.isArray(parsed)) return [];
      return parsed.map(normalizeSpotlightCandidate).filter(Boolean);
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

  function applySpotlightCandidate(card, candidate) {
    const image = card.querySelector(SPOTLIGHT_IMAGE_SELECTOR);
    const mediaLink = card.querySelector('[data-homepage-spotlight-link="media"]');
    const titleLink = card.querySelector('[data-homepage-spotlight-link="title"]');
    const ctaLink = card.querySelector('[data-homepage-spotlight-link="cta"]');
    const caption = card.querySelector(SPOTLIGHT_CAPTION_SELECTOR);
    const price = card.querySelector(SPOTLIGHT_PRICE_SELECTOR);

    if (image) {
      image.src = candidate.imageSrc;

      if (candidate.imageSrcset) {
        image.srcset = candidate.imageSrcset;
      } else {
        image.removeAttribute('srcset');
      }

      if (candidate.imageAlt) {
        image.alt = candidate.imageAlt;
      }

      if (candidate.imageWidth) {
        image.width = candidate.imageWidth;
      }

      if (candidate.imageHeight) {
        image.height = candidate.imageHeight;
      }

      image.dataset.homepageCollectionImageKey = candidate.imageKey;
      image.dataset.homepageCollectionImageSrc = candidate.imageSrc;
    }

    [mediaLink, titleLink, ctaLink].forEach((link) => {
      if (link) link.href = candidate.url;
    });

    if (titleLink && candidate.title) {
      titleLink.textContent = candidate.title;
    }

    if (caption) {
      if (candidate.caption) {
        caption.textContent = candidate.caption;
        caption.hidden = false;
      } else {
        caption.textContent = '';
        caption.hidden = true;
      }
    }

    if (price && candidate.priceHtml) {
      price.innerHTML = candidate.priceHtml;
    }

    card.dataset.analyticsProductId = String(candidate.productId);
    card.dataset.analyticsVariantId = candidate.variantId ? String(candidate.variantId) : '';
    card.dataset.analyticsHandle = candidate.handle;
    card.dataset.analyticsTitle = candidate.title;
    card.dataset.analyticsVendor = candidate.vendor;
    card.dataset.analyticsVariant = candidate.variant;
    card.dataset.analyticsPriceCents = String(candidate.priceCents || 0);
    card.dataset.analyticsCategory1 = candidate.category1;
    card.dataset.analyticsSubcategory = candidate.subcategory;
    card.dataset.analyticsSubcategory2 = candidate.subcategory2;
    card.dataset.analyticsType = candidate.type;
    card.dataset.analyticsStyle = candidate.style;
    card.dataset.analyticsPattern = candidate.pattern;
  }

  function reserveExistingImage(image, usedKeys, usedSrcs) {
    const existingKey = String(image.dataset.homepageCollectionImageKey || '').trim();
    const existingSrc = String(image.currentSrc || image.src || '').trim();

    if (existingKey) usedKeys.add(existingKey);
    if (existingSrc) usedSrcs.add(existingSrc);
  }

  function reserveHomepageImages(root, usedKeys, usedSrcs) {
    root.querySelectorAll(RESERVED_IMAGE_SELECTOR).forEach((image) => {
      reserveExistingImage(image, usedKeys, usedSrcs);
    });
  }

  function refreshHomepageCollectionImages(root = document) {
    const cards = Array.from(root.querySelectorAll(CARD_SELECTOR));
    if (!cards.length) return;

    const usedKeys = new Set();
    const usedSrcs = new Set();
    reserveHomepageImages(root, usedKeys, usedSrcs);

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

  function refreshHomepageSpotlightProducts(root = document) {
    const cards = Array.from(root.querySelectorAll(SPOTLIGHT_CARD_SELECTOR));
    if (!cards.length) return;

    const usedKeys = new Set();
    const usedSrcs = new Set();
    const usedProductIds = new Set();
    reserveHomepageImages(root, usedKeys, usedSrcs);

    cards.forEach((card) => {
      const image = card.querySelector(SPOTLIGHT_IMAGE_SELECTOR);
      const candidates = buildCandidateOrder(parseSpotlightCandidates(card));

      if (!candidates.length) {
        if (image) reserveExistingImage(image, usedKeys, usedSrcs);
        const existingProductId = Number(card.dataset.analyticsProductId) || 0;
        if (existingProductId) usedProductIds.add(existingProductId);
        return;
      }

      const selectedCandidate =
        candidates.find(
          (candidate) =>
            !usedProductIds.has(candidate.productId) &&
            !usedKeys.has(candidate.imageKey) &&
            !usedSrcs.has(candidate.imageSrc)
        ) ||
        candidates.find(
          (candidate) => !usedProductIds.has(candidate.productId) && !usedKeys.has(candidate.imageKey)
        ) ||
        candidates.find((candidate) => !usedProductIds.has(candidate.productId)) ||
        candidates.find((candidate) => !usedKeys.has(candidate.imageKey) && !usedSrcs.has(candidate.imageSrc)) ||
        candidates[0];

      applySpotlightCandidate(card, selectedCandidate);
      usedProductIds.add(selectedCandidate.productId);
      usedKeys.add(selectedCandidate.imageKey);
      usedSrcs.add(selectedCandidate.imageSrc);
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
    refreshHomepageSpotlightProducts();
  });

  document.addEventListener('shopify:section:load', (event) => {
    refreshHomepageCollectionImages(event.target.ownerDocument || document);
    refreshHomepageSpotlightProducts(event.target.ownerDocument || document);
  });
})();
