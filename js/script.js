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
