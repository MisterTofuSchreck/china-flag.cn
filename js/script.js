(function () {
  var navToggle = document.getElementById('navToggle');
  var siteNav = document.getElementById('siteNav');
  if (navToggle && siteNav) {
    navToggle.addEventListener('click', function () {
      var open = siteNav.classList.toggle('open');
      navToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    siteNav.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        siteNav.classList.remove('open');
        navToggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

  var langCurrent = document.getElementById('langCurrent');
  var langMenu = document.getElementById('langMenu');
  if (langCurrent && langMenu) {
    langCurrent.addEventListener('click', function (e) {
      e.stopPropagation();
      langMenu.classList.toggle('open');
    });
    document.addEventListener('click', function (e) {
      if (!langMenu.contains(e.target) && e.target !== langCurrent) {
        langMenu.classList.remove('open');
      }
    });
  }

  var yearEl = document.getElementById('year');
  if (yearEl) { yearEl.textContent = new Date().getFullYear(); }

  var CONSENT_KEY = 'cf-consent';
  var banner = document.getElementById('consentBanner');
  var acceptBtn = document.getElementById('consentAccept');
  var declineBtn = document.getElementById('consentDecline');
  var settingsBtn = document.getElementById('consentSettings');

  function loadAnalytics() {
    if (window.__gaLoaded || !window.CF_GA_ID) return;
    window.__gaLoaded = true;
    gtag('consent', 'update', { 'analytics_storage': 'granted' });
    gtag('js', new Date());
    gtag('config', window.CF_GA_ID);
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + window.CF_GA_ID;
    document.head.appendChild(s);
  }

  function setConsent(value) {
    try { localStorage.setItem(CONSENT_KEY, value); } catch (e) {}
    if (banner) { banner.hidden = true; }
    if (value === 'granted') { loadAnalytics(); }
  }

  if (banner) {
    var stored = null;
    try { stored = localStorage.getItem(CONSENT_KEY); } catch (e) {}
    if (stored === 'granted') {
      loadAnalytics();
    } else if (stored !== 'denied') {
      banner.hidden = false;
    }
    if (acceptBtn) { acceptBtn.addEventListener('click', function () { setConsent('granted'); }); }
    if (declineBtn) { declineBtn.addEventListener('click', function () { setConsent('denied'); }); }
  }
  if (settingsBtn && banner) {
    settingsBtn.addEventListener('click', function () { banner.hidden = false; });
  }

  document.querySelectorAll('.download-png').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var src = btn.getAttribute('data-src');
      var filename = btn.getAttribute('data-filename');
      fetch(src)
        .then(function (res) { return res.text(); })
        .then(function (svgText) {
          var svgUrl = URL.createObjectURL(new Blob([svgText], { type: 'image/svg+xml;charset=utf-8' }));
          var img = new Image();
          img.onload = function () {
            var size = 1000;
            var canvas = document.createElement('canvas');
            canvas.width = size;
            canvas.height = size;
            canvas.getContext('2d').drawImage(img, 0, 0, size, size);
            URL.revokeObjectURL(svgUrl);
            canvas.toBlob(function (blob) {
              var blobUrl = URL.createObjectURL(blob);
              var link = document.createElement('a');
              link.href = blobUrl;
              link.download = filename;
              document.body.appendChild(link);
              link.click();
              document.body.removeChild(link);
              URL.revokeObjectURL(blobUrl);
            }, 'image/png');
          };
          img.src = svgUrl;
        });
    });
  });
})();
