if (!customElements.get('media-gallery')) {
  customElements.define(
    'media-gallery',
    class MediaGallery extends HTMLElement {
      constructor() {
        super();
        this.elements = {
          liveRegion: this.querySelector('[id^="GalleryStatus"]'),
          viewer: this.querySelector('[id^="GalleryViewer"]'),
          thumbnails: this.querySelector('[id^="GalleryThumbnails"]'),
          mobileShareButton: this.querySelector('[data-mobile-share-button]'),
        };
        this.mql = window.matchMedia('(min-width: 750px)');
        this.mobileViewportMql = window.matchMedia('(max-width: 749px)');
        this.mobileShareClickHandler = this.handleMobileShareClick.bind(this);
        this.mobileSharePositionHandler = debounce(this.syncMobileShareButtonPosition.bind(this), 120);
        this.viewerSlideChangeHandler = debounce(this.syncMobileShareButtonPosition.bind(this), 80);
        this.mobileShareLoadHandler = this.mobileSharePositionHandler;
        this.galleryCounterPositionHandler = debounce(this.syncGalleryCounterPosition.bind(this), 120);
        this.galleryCounterSlideHandler = debounce(this.syncGalleryCounterPosition.bind(this), 80);

        if (this.elements.mobileShareButton) {
          this.elements.mobileShareButton.addEventListener('click', this.mobileShareClickHandler);
          if (this.elements.viewer) {
            this.syncMobileShareButtonPosition();
            window.requestAnimationFrame(() => this.syncMobileShareButtonPosition());
            window.setTimeout(() => this.syncMobileShareButtonPosition(), 220);
            this.elements.viewer.addEventListener('slideChanged', this.viewerSlideChangeHandler);
            if ('ResizeObserver' in window) {
              this.mobileShareResizeObserver = new ResizeObserver(this.mobileSharePositionHandler);
              this.mobileShareResizeObserver.observe(this.elements.viewer);
              const mediaList = this.elements.viewer.querySelector('.product__media-list');
              if (mediaList) this.mobileShareResizeObserver.observe(mediaList);
            }
          }
          window.addEventListener('load', this.mobileShareLoadHandler);
          window.addEventListener('resize', this.mobileSharePositionHandler);
          window.addEventListener('orientationchange', this.mobileSharePositionHandler);
          if (this.mobileViewportMql.addEventListener) {
            this.mobileViewportMql.addEventListener('change', this.mobileSharePositionHandler);
          } else if (this.mobileViewportMql.addListener) {
            this.mobileViewportMql.addListener(this.mobileSharePositionHandler);
          }
        }

        if (this.elements.viewer && this.querySelector('[data-gallery-stepper]')) {
          this.syncGalleryCounterPosition();
          window.requestAnimationFrame(() => this.syncGalleryCounterPosition());
          window.setTimeout(() => this.syncGalleryCounterPosition(), 220);
          this.elements.viewer.addEventListener('slideChanged', this.galleryCounterSlideHandler);
          if ('ResizeObserver' in window) {
            this.galleryCounterResizeObserver = new ResizeObserver(this.galleryCounterPositionHandler);
            this.galleryCounterResizeObserver.observe(this.elements.viewer);
            const mediaList = this.elements.viewer.querySelector('.product__media-list');
            if (mediaList) this.galleryCounterResizeObserver.observe(mediaList);
          }
          window.addEventListener('load', this.galleryCounterPositionHandler);
          window.addEventListener('resize', this.galleryCounterPositionHandler);
          window.addEventListener('orientationchange', this.galleryCounterPositionHandler);
        }

        if (!this.elements.thumbnails) return;

        this.elements.viewer.addEventListener('slideChanged', debounce(this.onSlideChanged.bind(this), 500));
        this.elements.thumbnails.querySelectorAll('[data-target]').forEach((mediaToSwitch) => {
          mediaToSwitch
            .querySelector('button')
            .addEventListener('click', this.setActiveMedia.bind(this, mediaToSwitch.dataset.target));
        });
        if (this.dataset.desktopLayout.includes('thumbnail') && this.mql.matches) this.removeListSemantic();
      }

      disconnectedCallback() {
        if (this.elements.mobileShareButton) {
          this.elements.mobileShareButton.removeEventListener('click', this.mobileShareClickHandler);
          if (this.elements.viewer) {
            this.elements.viewer.removeEventListener('slideChanged', this.viewerSlideChangeHandler);
          }
          if (this.mobileShareResizeObserver) {
            this.mobileShareResizeObserver.disconnect();
          }
          window.removeEventListener('load', this.mobileShareLoadHandler);
          window.removeEventListener('resize', this.mobileSharePositionHandler);
          window.removeEventListener('orientationchange', this.mobileSharePositionHandler);
          if (this.mobileViewportMql.removeEventListener) {
            this.mobileViewportMql.removeEventListener('change', this.mobileSharePositionHandler);
          } else if (this.mobileViewportMql.removeListener) {
            this.mobileViewportMql.removeListener(this.mobileSharePositionHandler);
          }
        }
        if (this.elements.viewer) {
          this.elements.viewer.removeEventListener('slideChanged', this.galleryCounterSlideHandler);
        }
        if (this.galleryCounterResizeObserver) {
          this.galleryCounterResizeObserver.disconnect();
        }
        window.removeEventListener('load', this.galleryCounterPositionHandler);
        window.removeEventListener('resize', this.galleryCounterPositionHandler);
        window.removeEventListener('orientationchange', this.galleryCounterPositionHandler);
      }

      onSlideChanged(event) {
        const thumbnail = this.elements.thumbnails.querySelector(
          `[data-target="${event.detail.currentElement.dataset.mediaId}"]`
        );
        this.setActiveThumbnail(thumbnail);
        this.syncGalleryCounter(event.detail.currentElement.dataset.mediaId);
        this.syncGalleryCounterPosition();
        this.syncMobileShareButtonPosition();
      }

      handleMobileShareClick() {
        const shareUrl = window.location.href;

        if (navigator.share) {
          navigator.share({ url: shareUrl, title: document.title }).catch(() => {});
          return;
        }

        if (navigator.clipboard && window.isSecureContext) {
          navigator.clipboard
            .writeText(shareUrl)
            .then(() => {
              this.elements.mobileShareButton.classList.add('is-copied');
              window.setTimeout(() => {
                this.elements.mobileShareButton.classList.remove('is-copied');
              }, 1400);
            })
            .catch(() => {});
        }
      }

      setActiveMedia(mediaId, options = {}) {
        const { preventScroll = false } = options;
        const isDesktopViewport = this.mql.matches;
        const activeMedia =
          this.elements.viewer.querySelector(`[data-media-id="${mediaId}"]`) ||
          this.elements.viewer.querySelector('[data-media-id]');
        if (!activeMedia) {
          return;
        }
        this.elements.viewer.querySelectorAll('[data-media-id]').forEach((element) => {
          element.classList.remove('is-active');
        });
        activeMedia?.classList?.add('is-active');
        this.syncGalleryCounter(mediaId);
        this.syncGalleryCounterPosition();
        this.syncMobileShareButtonPosition();

        this.preventStickyHeader();
        window.setTimeout(() => {
          if (!isDesktopViewport || this.elements.thumbnails) {
            activeMedia.parentElement.scrollTo({ left: activeMedia.offsetLeft });
          }
          if (preventScroll || !isDesktopViewport) return;
          const activeMediaRect = activeMedia.getBoundingClientRect();
          // Don't scroll if the image is already in view
          if (activeMediaRect.top > -0.5) return;
          const top = activeMediaRect.top + window.scrollY;
          window.scrollTo({ top: top, behavior: 'smooth' });
          this.syncGalleryCounterPosition();
        });
        this.playActiveMedia(activeMedia);

        if (!this.elements.thumbnails) return;
        const activeThumbnail = this.elements.thumbnails.querySelector(`[data-target="${mediaId}"]`);
        this.setActiveThumbnail(activeThumbnail);
        this.announceLiveRegion(activeMedia, activeThumbnail.dataset.mediaPosition);
      }

      syncMobileShareButtonPosition() {
        const { mobileShareButton, viewer } = this.elements;
        if (!mobileShareButton || !viewer) return;

        if (!this.mobileViewportMql.matches) {
          mobileShareButton.style.removeProperty('top');
          mobileShareButton.style.removeProperty('right');
          mobileShareButton.style.removeProperty('left');
          mobileShareButton.style.removeProperty('bottom');
          return;
        }

        const cornerInset = this.getMobileCornerInsetPx();
        mobileShareButton.style.setProperty('top', `${Math.round(cornerInset)}px`, 'important');
        mobileShareButton.style.setProperty('right', `${Math.round(cornerInset)}px`, 'important');
        mobileShareButton.style.setProperty('left', 'auto', 'important');
        mobileShareButton.style.setProperty('bottom', 'auto', 'important');
      }

      getMobileCornerInsetPx() {
        const mediaProgress = this.querySelector('[data-gallery-stepper]');
        if (mediaProgress) {
          const progressStyles = window.getComputedStyle(mediaProgress);
          const progressRight = Number.parseFloat(progressStyles.right);
          if (!Number.isNaN(progressRight) && progressRight > 0) return progressRight;
        }

        const rootFontSize = Number.parseFloat(window.getComputedStyle(document.documentElement).fontSize) || 16;
        return rootFontSize * 0.65;
      }

      syncGalleryCounter(mediaId) {
        const mediaProgress = this.querySelector('[data-gallery-stepper]');
        if (!mediaProgress || !this.elements.viewer) return;

        const mediaItems = this.elements.viewer.slider
          ? Array.from(this.elements.viewer.slider.querySelectorAll(':scope > [data-media-id]'))
          : Array.from(this.elements.viewer.querySelectorAll('.product__media-list > [data-media-id]'));
        if (!mediaItems.length) return;

        let activeIndex = mediaItems.findIndex((item) => item.dataset.mediaId === mediaId);
        if (activeIndex < 0) {
          activeIndex = mediaItems.findIndex((item) => item.classList.contains('is-active'));
        }
        const current = activeIndex >= 0 ? activeIndex + 1 : 1;
        const total = mediaItems.length;
        const progress = Math.min(100, Math.max(0, (current / total) * 100));

        const currentElement = mediaProgress.querySelector('.product-media-progress__current');
        const totalElement = mediaProgress.querySelector('.product-media-progress__total');
        if (currentElement) currentElement.textContent = current;
        if (totalElement) totalElement.textContent = total;
        mediaProgress.style.setProperty('--media-progress', `${progress}%`);
      }

      syncGalleryCounterPosition() {
        const mediaProgress = this.querySelector('[data-gallery-stepper]');
        if (!mediaProgress || !this.elements.viewer) return;

        if (this.mobileViewportMql.matches) {
          const inset = this.getMobileCornerInsetPx();
          const roundedInset = Math.round(inset);
          mediaProgress.style.setProperty('right', `${roundedInset}px`, 'important');
          mediaProgress.style.setProperty('bottom', `${roundedInset}px`, 'important');
          mediaProgress.style.setProperty('left', 'auto', 'important');
          mediaProgress.style.setProperty('top', 'auto', 'important');
          mediaProgress.style.setProperty('max-width', `calc(100% - ${roundedInset * 2}px)`, 'important');
          return;
        }

        const viewerRect = this.elements.viewer.getBoundingClientRect();
        const activeMediaItem =
          this.elements.viewer.querySelector('.product__media-list > .product__media-item.is-active') ||
          this.elements.viewer.querySelector('.product__media-list > .product__media-item');
        if (!activeMediaItem) return;

        const mediaFrame =
          activeMediaItem.querySelector('.product-media-container .product__media') ||
          activeMediaItem.querySelector('.product__media') ||
          activeMediaItem;
        const frameRect = mediaFrame.getBoundingClientRect();

        const inset = 10;
        const right = Math.max(0, viewerRect.right - frameRect.right) + inset;
        const bottom = Math.max(0, viewerRect.bottom - frameRect.bottom) + inset;

        mediaProgress.style.setProperty('right', `${Math.round(right)}px`, 'important');
        mediaProgress.style.setProperty('bottom', `${Math.round(bottom)}px`, 'important');
        mediaProgress.style.setProperty('left', 'auto', 'important');
        mediaProgress.style.setProperty('top', 'auto', 'important');
        mediaProgress.style.setProperty('max-width', `calc(100% - ${Math.round(right) + inset}px)`, 'important');
      }

      setActiveThumbnail(thumbnail) {
        if (!this.elements.thumbnails || !thumbnail) return;

        this.elements.thumbnails
          .querySelectorAll('button')
          .forEach((element) => element.removeAttribute('aria-current'));
        thumbnail.querySelector('button').setAttribute('aria-current', true);
        if (this.elements.thumbnails.isSlideVisible(thumbnail, 10)) return;

        this.elements.thumbnails.slider.scrollTo({ left: thumbnail.offsetLeft });
      }

      announceLiveRegion(activeItem, position) {
        const image = activeItem.querySelector('.product__modal-opener--image img');
        if (!image) return;
        image.onload = () => {
          this.elements.liveRegion.setAttribute('aria-hidden', false);
          this.elements.liveRegion.innerHTML = window.accessibilityStrings.imageAvailable.replace('[index]', position);
          setTimeout(() => {
            this.elements.liveRegion.setAttribute('aria-hidden', true);
          }, 2000);
        };
        image.src = image.src;
      }

      playActiveMedia(activeItem) {
        window.pauseAllMedia();
        const deferredMedia = activeItem.querySelector('.deferred-media');
        if (deferredMedia) deferredMedia.loadContent(false);
      }

      preventStickyHeader() {
        this.stickyHeader = this.stickyHeader || document.querySelector('sticky-header');
        if (!this.stickyHeader) return;
        this.stickyHeader.dispatchEvent(new Event('preventHeaderReveal'));
      }

      removeListSemantic() {
        if (!this.elements.viewer.slider) return;
        this.elements.viewer.slider.setAttribute('role', 'presentation');
        this.elements.viewer.sliderItems.forEach((slide) => slide.setAttribute('role', 'presentation'));
      }
    }
  );
}
