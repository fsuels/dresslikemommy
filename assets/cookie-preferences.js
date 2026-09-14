if (!customElements.get('cookie-preferences')) {
  customElements.define('cookie-preferences', class extends HTMLElement {
    connectedCallback() {
      if (this.button) return;
      this.button = this.querySelector('button');
      this.status = this.querySelector('[role="status"]');
      if (!this.button || !this.status) return;
      this.handleClick = this.openPreferences.bind(this);
      this.button.addEventListener('click', this.handleClick);
    }

    disconnectedCallback() {
      this.button?.removeEventListener('click', this.handleClick);
      this.finishOpening(false);
      this.button = null;
    }

    visibleDialog() {
      return [...document.querySelectorAll('.shopify-pc__prefs__dialog, .shopify-pc__prefs')]
        .find((dialog) => dialog.getClientRects().length > 0
          && window.getComputedStyle(dialog).visibility !== 'hidden'
          && !dialog.closest('[hidden], [aria-hidden="true"]'));
    }

    openPreferences() {
      if (this.attempt) return;
      this.status.textContent = '';
      const privacyBanner = window.privacyBanner;
      if (!privacyBanner || typeof privacyBanner.showPreferences !== 'function') {
        this.status.textContent = this.dataset.unavailableMessage;
        return;
      }

      const attempt = {};
      this.attempt = attempt;
      this.button.disabled = true;
      this.button.setAttribute('aria-busy', 'true');
      const checkDialog = () => {
        if (this.attempt !== attempt) return;
        const dialog = this.visibleDialog();
        if (dialog) {
          this.dialog = dialog;
          clearTimeout(this.openTimeout);
          this.button.removeAttribute('aria-busy');
        } else if (this.dialog) {
          this.finishOpening(true);
        }
      };

      this.observer = new MutationObserver(checkDialog);
      this.observer.observe(document.body, {
        childList: true,
        subtree: true,
        attributes: true,
        attributeFilter: ['class', 'style', 'hidden', 'aria-hidden'],
      });
      this.openTimeout = setTimeout(() => this.openFailed(attempt), 10000);

      try {
        const result = privacyBanner.showPreferences();
        checkDialog();
        // The API result is not a dialog-close signal. Shopify owns dialog focus.
        Promise.resolve(result).catch(() => this.openFailed(attempt));
      } catch (_error) {
        this.openFailed(attempt);
      }
    }

    openFailed(attempt) {
      if (this.attempt !== attempt) return;
      this.finishOpening(false);
      this.status.textContent = this.dataset.unavailableMessage;
    }

    finishOpening(restoreFocus) {
      clearTimeout(this.openTimeout);
      this.observer?.disconnect();
      const activeElement = document.activeElement;
      const focusNeedsReturn = !activeElement || activeElement === document.body
        || !activeElement.isConnected || this.dialog?.contains(activeElement);
      this.dialog = null;
      this.attempt = null;
      if (!this.button) return;
      this.button.disabled = false;
      this.button.removeAttribute('aria-busy');
      if (restoreFocus && focusNeedsReturn && this.button.isConnected) {
        this.button.focus({ preventScroll: true });
      }
    }
  });
}
