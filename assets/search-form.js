class SearchForm extends HTMLElement {
  constructor() {
    super();
    this.input = this.querySelector('input[type="search"]');
    this.resetButton = this.querySelector('button[type="reset"]');

    if (this.input) {
      if (this.input.form) {
        this.input.form.addEventListener('submit', this.onFormSubmit.bind(this));
        this.input.form.addEventListener('reset', this.onFormReset.bind(this));
      }
      this.input.addEventListener(
        'input',
        debounce((event) => {
          this.onChange(event);
        }, 300).bind(this)
      );
    }
  }

  toggleResetButton() {
    const resetIsHidden = this.resetButton.classList.contains('hidden');
    if (this.input.value.length > 0 && resetIsHidden) {
      this.resetButton.classList.remove('hidden');
    } else if (this.input.value.length === 0 && !resetIsHidden) {
      this.resetButton.classList.add('hidden');
    }
  }

  getQuery() {
    return this.input?.value?.trim() || '';
  }

  normalizeSearchQuery(query) {
    return String(query || '')
      .toLowerCase()
      .replace(/&/g, ' and ')
      .replace(/[^a-z0-9]+/g, ' ')
      .replace(/\s+/g, ' ')
      .trim();
  }

  getSmartSearchShortcut(query = this.getQuery()) {
    const normalizedQuery = this.normalizeSearchQuery(query);
    if (!normalizedQuery) return null;

    const exactPajamaQueries = new Set([
      'pajama',
      'pajamas',
      'pjs',
      'matching pajama',
      'matching pajamas',
      'matching pjs',
      'family pajama',
      'family pajamas',
      'family pjs',
      'matching family pajamas',
      'matching family pjs',
      'mommy and me pajama',
      'mommy and me pajamas',
      'mommy and me pjs',
      'mommy me pajamas',
      'mom and me pajamas',
      'mom and me pjs',
      'mother daughter pajama',
      'mother daughter pajamas',
      'mother daughter pjs',
      'mother daughter matching pajamas',
      'mother and daughter pajamas',
      'mother and daughter pjs',
    ]);

    if (!exactPajamaQueries.has(normalizedQuery)) return null;

    const pajamaCollectionUrl = this.input?.form?.dataset?.pajamaCollectionUrl || '/collections/pajamas';

    return {
      collectionHandle: 'pajamas',
      label: 'Shop Pajamas',
      query: normalizedQuery,
      url: pajamaCollectionUrl,
    };
  }

  onChange() {
    this.toggleResetButton();
  }

  onFormSubmit(event) {
    const query = this.getQuery();
    if (!query.length) {
      event.preventDefault();
      return;
    }

    const smartShortcut = this.getSmartSearchShortcut(query);
    if (!smartShortcut || !smartShortcut.url) return;

    event.preventDefault();
    window.location.assign(smartShortcut.url);
  }

  shouldResetForm() {
    return !document.querySelector('[aria-selected="true"] a');
  }

  onFormReset(event) {
    // Prevent default so the form reset doesn't set the value gotten from the url on page load
    event.preventDefault();
    // Don't reset if the user has selected an element on the predictive search dropdown
    if (this.shouldResetForm()) {
      this.input.value = '';
      this.input.focus();
      this.toggleResetButton();
    }
  }
}

customElements.define('search-form', SearchForm);
