// First-visit localization. Config and rationale: snippets/auto-localization.liquid.
(() => {
  const COUNTRY_FLAG = 'dlm_auto_country';
  const LANGUAGE_FLAG = 'dlm_language_prompt';
  const BOT_PATTERN =
    /bot|crawl|spider|slurp|lighthouse|headless|facebookexternalhit|preview|mediapartners|apis-google|feedfetcher|ahrefs|semrush/i;

  // Offer text, written in the language being offered.
  const PROMPTS = {
    ar: ['عرض الموقع باللغة العربية', 'لا، شكرًا'],
    cs: ['Zobrazit web v češtině', 'Ne, děkuji'],
    da: ['Se siden på dansk', 'Nej tak'],
    de: ['Seite auf Deutsch anzeigen', 'Nein, danke'],
    el: ['Προβολή του ιστότοπου στα ελληνικά', 'Όχι, ευχαριστώ'],
    en: ['View this site in English', 'No thanks'],
    es: ['Ver el sitio en español', 'No, gracias'],
    fi: ['Näytä sivusto suomeksi', 'Ei kiitos'],
    fr: ['Voir le site en français', 'Non merci'],
    he: ['הצגת האתר בעברית', 'לא, תודה'],
    hi: ['साइट हिंदी में देखें', 'नहीं, धन्यवाद'],
    it: ['Visualizza il sito in italiano', 'No, grazie'],
    ja: ['日本語でサイトを表示', '閉じる'],
    ko: ['한국어로 사이트 보기', '닫기'],
    nl: ['Bekijk de site in het Nederlands', 'Nee, bedankt'],
    no: ['Se siden på norsk', 'Nei takk'],
    pl: ['Zobacz stronę po polsku', 'Nie, dziękuję'],
    pt: ['Ver o site em português', 'Agora não'],
    ro: ['Vezi site-ul în limba română', 'Nu, mulțumesc'],
    ru: ['Открыть сайт на русском', 'Нет, спасибо'],
    sv: ['Visa sidan på svenska', 'Nej tack'],
  };
  const RTL = ['ar', 'he'];

  const configElement = document.getElementById('AutoLocalizationConfig');
  if (!configElement || navigator.webdriver || BOT_PATTERN.test(navigator.userAgent)) return;

  let config;
  try {
    config = JSON.parse(configElement.textContent);
  } catch (error) {
    return;
  }

  const hasFlag = (name) => {
    try {
      if (localStorage.getItem(name)) return true;
    } catch (error) {
      // Storage blocked: the cookie below still works.
    }
    return document.cookie.split('; ').some((cookie) => cookie.startsWith(`${name}=`));
  };

  const setFlag = (name) => {
    try {
      localStorage.setItem(name, '1');
    } catch (error) {
      // Storage blocked: the cookie below still works.
    }
    document.cookie = `${name}=1; path=/; max-age=31536000; SameSite=Lax`;
  };

  const baseLanguage = (code) => String(code || '').toLowerCase().split('-')[0];
  const root = (window.Shopify && window.Shopify.routes && window.Shopify.routes.root) || '/';

  const submitLocalization = (fields) => {
    const form = document.createElement('form');
    form.method = 'post';
    form.action = `${root}localization`;
    form.acceptCharset = 'UTF-8';
    form.hidden = true;
    const values = {
      form_type: 'localization',
      utf8: '✓',
      _method: 'put',
      return_to: window.location.pathname + window.location.search,
      ...fields,
    };
    Object.entries(values).forEach(([name, value]) => {
      const input = document.createElement('input');
      input.type = 'hidden';
      input.name = name;
      input.value = value;
      form.appendChild(input);
    });
    document.body.appendChild(form);
    form.submit();
  };

  const showLanguagePrompt = (language) => {
    const prompt = PROMPTS[baseLanguage(language)];

    const style = document.createElement('style');
    style.textContent = `
      .auto-language-prompt{position:fixed;left:50%;bottom:1.6rem;z-index:1001;transform:translateX(-50%);
        display:flex;align-items:center;gap:.4rem;width:max-content;max-width:calc(100% - 3.2rem);
        padding:.6rem;border-radius:4rem;background:rgb(var(--color-background,255,255,255));
        color:rgb(var(--color-foreground,18,18,18));box-shadow:0 .4rem 1.6rem rgba(0,0,0,.18);
        font-size:1.4rem;line-height:1.3}
      .auto-language-prompt button{font:inherit;cursor:pointer;border:0;border-radius:4rem;padding:.9rem 1.6rem;min-height:4.4rem}
      .auto-language-prompt__accept{background:rgb(var(--color-button,18,18,18));color:rgb(var(--color-button-text,255,255,255))}
      .auto-language-prompt__dismiss{background:transparent;color:inherit;text-decoration:underline}`;

    const container = document.createElement('div');
    container.className = 'auto-language-prompt';
    container.setAttribute('role', 'region');
    container.setAttribute('aria-label', prompt[0]);
    container.lang = language;
    if (RTL.includes(baseLanguage(language))) container.dir = 'rtl';

    const accept = document.createElement('button');
    accept.type = 'button';
    accept.className = 'auto-language-prompt__accept';
    accept.textContent = prompt[0];
    accept.addEventListener('click', () => {
      setFlag(LANGUAGE_FLAG);
      submitLocalization({ locale_code: language });
    });

    const dismiss = document.createElement('button');
    dismiss.type = 'button';
    dismiss.className = 'auto-language-prompt__dismiss';
    dismiss.textContent = prompt[1];
    dismiss.addEventListener('click', () => {
      setFlag(LANGUAGE_FLAG);
      container.remove();
    });

    container.append(accept, dismiss);
    document.head.appendChild(style);
    document.body.appendChild(container);
  };

  const run = async () => {
    // An explicit ?country= (ads, feeds, shared links) is a deliberate choice: keep it.
    if (new URLSearchParams(window.location.search).has('country')) setFlag(COUNTRY_FLAG);

    const decideCountry = !hasFlag(COUNTRY_FLAG);
    const decideLanguage = !hasFlag(LANGUAGE_FLAG);
    if (!decideCountry && !decideLanguage) return;

    let data;
    try {
      const response = await fetch(
        `${root}browsing_context_suggestions.json?country[enabled]=true&language[enabled]=true` +
          `&language[exclude]=${encodeURIComponent(config.language)}`,
        { credentials: 'same-origin', headers: { Accept: 'application/json' } }
      );
      if (!response.ok) return;
      data = await response.json();
    } catch (error) {
      return;
    }

    if (decideCountry) {
      setFlag(COUNTRY_FLAG);
      const detected = data && data.detected_values && data.detected_values.country;
      const detectedCountry = detected && String(detected.handle || '').toUpperCase();
      // Only move visitors still on the default country; never override a country they picked.
      if (
        detectedCountry &&
        detectedCountry !== config.country &&
        config.country === config.primaryCountry &&
        config.countries.includes(detectedCountry)
      ) {
        submitLocalization({ country_code: detectedCountry });
        return;
      }
    }

    if (decideLanguage) {
      const suggestion = ((data && data.suggestions) || []).find((item) => item.parts && item.parts.language);
      const language = suggestion && suggestion.parts.language.handle;
      if (
        language &&
        baseLanguage(language) !== baseLanguage(config.language) &&
        config.languages.includes(language) &&
        PROMPTS[baseLanguage(language)]
      ) {
        // Stays on later pages until the visitor answers it.
        showLanguagePrompt(language);
      } else {
        setFlag(LANGUAGE_FLAG);
      }
    }
  };

  run();
})();
