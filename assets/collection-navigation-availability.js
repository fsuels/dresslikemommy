(() => {
  const initAvailability = () => {
    window.DLMCollectionNavigationAvailability?.init();
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAvailability, { once: true });
    return;
  }

  initAvailability();
})();
