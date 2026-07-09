# -*- coding: utf-8 -*-
"""Generates the per-language static pages for china-flag.cn from scripts/content.py.

Usage: python scripts/build.py
Regenerate this way whenever content.py changes - the generated
/xx/index.html files and /assets/<lang>/*.svg files are committed
as plain static output, there is no build step at request time.
"""
import json
import os
import re
import shutil

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content import (
    LANGS, LANG_META, GALLERY_ITEMS, GALLERY_GROUPS, CONTENT,
    HISTORICAL_ITEMS, COLORING_BASE_FILE,
)

SITE_URL = "https://www.china-flag.cn"


def esc(s):
    return s if s is None else s.replace("&", "&amp;")


def nav_links(lang):
    c = CONTENT[lang]["nav"]
    return f"""
      <a href="#gallery">{esc(c['gallery'])}</a>
      <a href="#meaning">{esc(c['meaning'])}</a>
      <a href="#history">{esc(c['history'])}</a>
      <a href="#historic">{esc(c['historic'])}</a>
      <a href="#data">{esc(c['data'])}</a>
      <a href="#coloring">{esc(c['coloring'])}</a>
      <a href="#etiquette">{esc(c['etiquette'])}</a>
      <a href="#faq">{esc(c['faq'])}</a>"""


def lang_switcher(current):
    opts = []
    for code in LANGS:
        meta = LANG_META[code]
        cls = " class=\"active\"" if code == current else ""
        opts.append(f'<a href="/{code}/"{cls} lang="{meta["html_lang"]}">{meta["native"]}</a>')
    return "\n          ".join(opts)


def meaning_section(lang):
    c = CONTENT[lang]["meaning"]
    cards = ""
    swatches = ["swatch-red", "swatch-star card-swatch-big", "swatch-star", "icon", "swatch-yellow"]
    for i, card in enumerate(c["cards"]):
        if swatches[i] == "icon":
            visual = '<div class="card-icon">✦→✪</div>'
        else:
            visual = f'<div class="card-swatch {swatches[i]}"></div>'
        cards += f"""
        <article class="card">
          {visual}
          <h3>{esc(card['title'])}</h3>
          <p>{esc(card['text'])}</p>
        </article>"""
    return f"""
  <section id="meaning" class="section section-alt">
    <div class="container">
      <h2 class="section-title">{esc(c['title'])}</h2>
      <p class="section-intro">{esc(c['intro'])}</p>
      <div class="card-grid">{cards}
      </div>
    </div>
  </section>"""


def history_section(lang):
    c = CONTENT[lang]["history"]
    items = ""
    for item in c["items"]:
        items += f"""
        <div class="timeline-item">
          <div class="timeline-date">{esc(item['date'])}</div>
          <p>{esc(item['text'])}</p>
        </div>"""
    return f"""
  <section id="history" class="section">
    <div class="container">
      <h2 class="section-title">{esc(c['title'])}</h2>
      <div class="timeline">{items}
      </div>
    </div>
  </section>"""


def data_section(lang):
    c = CONTENT[lang]["data"]
    r = c["ratio"]
    g = c["grid"]
    col = c["colors"]
    orient = c["orientation"]
    return f"""
  <section id="data" class="section">
    <div class="container">
      <h2 class="section-title">{esc(c['title'])}</h2>
      <div class="data-grid">
        <div class="data-card">
          <h3>{esc(r['title'])}</h3>
          <p class="data-big">3:2</p>
          <p>{esc(r['text'])}</p>
        </div>
        <div class="data-card">
          <h3>{esc(g['title'])}</h3>
          <p>{esc(g['text'])}</p>
        </div>
        <div class="data-card">
          <h3>{esc(col['title'])}</h3>
          <div class="color-row"><span class="color-dot" style="background:#DE2910"></span>{esc(col['red'])}</div>
          <div class="color-row"><span class="color-dot" style="background:#FFDE00"></span>{esc(col['yellow'])}</div>
          <p class="fine-print">{esc(col['note'])}</p>
        </div>
        <div class="data-card">
          <h3>{esc(orient['title'])}</h3>
          <p>{esc(orient['text'])}</p>
        </div>
      </div>
    </div>
  </section>"""


def font_link(lang):
    """Google-Fonts stylesheet link for the page: Inter always, plus the
    language's script font from LANG_META['gfont'] if set. Chinese/Japanese
    also need the 900 weight for the hero headline. Emitted BEFORE style.css."""
    meta = LANG_META[lang]
    fams = ["Inter:wght@400;500;600;700;800"]
    gfont = meta.get("gfont")
    if gfont:
        weights = "400;500;700;900" if lang in ("zh", "ja") else "400;500;700"
        fams.append(gfont.replace(" ", "+") + f":wght@{weights}")
    url = "https://fonts.googleapis.com/css2?" + "&".join("family=" + f for f in fams) + "&display=swap"
    return f'<link href="{url}" rel="stylesheet">'


def font_body_style(lang):
    """Inline override that applies the script font to <body>. Must be emitted
    AFTER style.css so it wins over the generic `body{font-family:...}` rule."""
    gfont = LANG_META[lang].get("gfont")
    if not gfont:
        return ""
    return f"<style>body{{font-family:'{gfont}','Inter',sans-serif;}}</style>"


def download_row(lang, slug, name, png_w=None, png_h=None):
    """Shared SVG/PNG download row used by gallery, historic and coloring sections."""
    dl = CONTENT[lang]["download"]
    svg_label = esc(dl["svg"].format(name=name))
    png_label = esc(dl["png"].format(name=name))
    size_attrs = f' data-w="{png_w}" data-h="{png_h}"' if png_w and png_h else ""
    return f"""<div class="gallery-downloads">
            <a class="download-link" href="/assets/{lang}/{slug}.svg" download="{slug}.svg" aria-label="{svg_label}">SVG</a>
            <span class="download-sep" aria-hidden="true">&middot;</span>
            <button type="button" class="download-link download-png" data-src="/assets/{lang}/{slug}.svg" data-filename="{slug}.png"{size_attrs} aria-label="{png_label}">PNG</button>
          </div>"""


def gallery_section(lang):
    c = CONTENT[lang]["gallery"]
    gi = c["items"]
    groups_html = ""
    for group_key, group_title in GALLERY_GROUPS:
        figures = ""
        for key in GALLERY_ITEMS:
            if GALLERY_ITEMS[key]["group"] != group_key:
                continue
            item = gi[key]
            slug = item["slug"]
            figures += f"""
        <figure class="gallery-item">
          <img src="/assets/{lang}/{slug}.svg" width="400" height="400" alt="{esc(item['text'])}" loading="lazy" decoding="async">
          <figcaption>{esc(item['text'])}</figcaption>
          {download_row(lang, slug, item['text'])}
        </figure>"""
        groups_html += f"""
      <h3 class="gallery-group-title">{esc(c['groups'][group_key])}</h3>
      <div class="gallery-grid">{figures}
      </div>"""
    return f"""
  <section id="gallery" class="section">
    <div class="container">
      <h2 class="section-title">{esc(c['title'])}</h2>
      <p class="section-intro">{esc(c['intro'])}</p>
      {groups_html}
      <p class="fine-print centered">{esc(c['disclaimer'])}</p>
      <p class="fine-print centered" id="license">{esc(c['license'])}</p>
    </div>
  </section>"""


def historic_section(lang):
    c = CONTENT[lang]["historical"]
    figures = ""
    for key in HISTORICAL_ITEMS:
        it = c["items"][key]
        slug = it["slug"]
        figures += f"""
        <figure class="gallery-item">
          <img src="/assets/{lang}/{slug}.svg" width="400" height="400" alt="{esc(it['alt'])}" loading="lazy" decoding="async">
          <figcaption>{esc(it['name'])} · {esc(it['period'])}</figcaption>
          <p class="historic-text">{esc(it['text'])}</p>
          {download_row(lang, slug, it['name'])}
        </figure>"""
    return f"""
  <section id="historic" class="section section-alt">
    <div class="container">
      <h2 class="section-title">{esc(c['title'])}</h2>
      <p class="section-intro">{esc(c['intro'])}</p>
      <div class="gallery-grid">{figures}
      </div>
    </div>
  </section>"""


def coloring_section(lang):
    c = CONTENT[lang]["coloring"]
    slug = c["slug"]
    return f"""
  <section id="coloring" class="section section-alt">
    <div class="container">
      <h2 class="section-title">{esc(c['title'])}</h2>
      <p class="section-intro">{esc(c['text'])}</p>
      <figure class="gallery-item coloring-item">
        <img src="/assets/{lang}/{slug}.svg" width="900" height="600" alt="{esc(c['alt'])}" loading="lazy" decoding="async">
        <figcaption>{esc(c['caption'])}</figcaption>
        {download_row(lang, slug, c['caption'], png_w=1200, png_h=800)}
      </figure>
    </div>
  </section>"""


def emoji_section(lang):
    c = CONTENT[lang]["emoji"]
    return f"""
  <section id="emoji" class="section">
    <div class="container">
      <h2 class="section-title">{esc(c['title'])}</h2>
      <p class="section-intro">{esc(c['text'])}</p>
      <div class="emoji-box">
        <span class="emoji-char">🇨🇳</span>
        <button type="button" class="emoji-copy" id="emojiCopy" data-copied="{esc(c['copied'])}">{esc(c['copy'])}</button>
      </div>
      <p class="fine-print centered">{esc(c['note'])}</p>
    </div>
  </section>"""


def faq_section(lang):
    c = CONTENT[lang]["faq"]
    items = ""
    for it in c["items"]:
        items += f"""
      <details class="faq-item">
        <summary>{esc(it['q'])}</summary>
        <p>{esc(it['a'])}</p>
      </details>"""
    return f"""
  <section id="faq" class="section">
    <div class="container faq-container">
      <h2 class="section-title">{esc(c['title'])}</h2>{items}
    </div>
  </section>"""


def org_jsonld():
    """Organization schema with logo — enables the site logo in search results."""
    data = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "China-Flag.cn",
        "url": f"{SITE_URL}/",
        "logo": f"{SITE_URL}/android-chrome-512x512.png",
    }
    return json.dumps(data, ensure_ascii=False)


def breadcrumb_jsonld(lang):
    """BreadcrumbList: site home -> current language page (native name)."""
    data = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "China Flag",
             "item": f"{SITE_URL}/"},
            {"@type": "ListItem", "position": 2, "name": LANG_META[lang]["native"],
             "item": f"{SITE_URL}/{lang}/"},
        ],
    }
    return json.dumps(data, ensure_ascii=False)


def faq_jsonld(lang):
    c = CONTENT[lang]["faq"]
    data = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": it["q"],
                "acceptedAnswer": {"@type": "Answer", "text": it["a"]},
            }
            for it in c["items"]
        ],
    }
    return json.dumps(data, ensure_ascii=False, indent=1)


def downloadable_images(lang):
    """(name, slug) pairs of every downloadable image on a language page:
    33 gallery motifs, the historical flags and the coloring page."""
    c = CONTENT[lang]
    pairs = [(c["gallery"]["items"][k]["text"], c["gallery"]["items"][k]["slug"])
             for k in GALLERY_ITEMS]
    pairs += [(c["historical"]["items"][k]["name"], c["historical"]["items"][k]["slug"])
              for k in HISTORICAL_ITEMS]
    pairs.append((c["coloring"]["caption"], c["coloring"]["slug"]))
    return pairs


def images_jsonld(lang):
    g = CONTENT[lang]["gallery"]
    entries = []
    for pos, (name, slug) in enumerate(downloadable_images(lang), 1):
        entries.append({
            "@type": "ListItem",
            "position": pos,
            "item": {
                "@type": "ImageObject",
                "name": name,
                "contentUrl": f"{SITE_URL}/assets/{lang}/{slug}.svg",
                "encodingFormat": "image/svg+xml",
                "creator": {"@type": "Organization", "name": "China-Flag.cn"},
                "creditText": "China-Flag.cn",
                "copyrightNotice": "China-Flag.cn",
                "license": f"{SITE_URL}/{lang}/#license",
                "acquireLicensePage": f"{SITE_URL}/{lang}/#license",
            },
        })
    data = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": g["title"],
        "itemListElement": entries,
    }
    return json.dumps(data, ensure_ascii=False)


def render_page(lang):
    c = CONTENT[lang]
    meta = LANG_META[lang]
    hero = c["hero"]
    etiquette = c["etiquette"]
    consent = c["consent"]
    footer = c["footer"]

    hreflangs = "\n".join(
        f'<link rel="alternate" hreflang="{LANG_META[code]["html_lang"]}" href="{SITE_URL}/{code}/">'
        for code in LANGS
    )
    hreflangs += f'\n<link rel="alternate" hreflang="x-default" href="{SITE_URL}/en/">'

    html = f"""<!DOCTYPE html>
<html lang="{meta['html_lang']}" dir="{meta['dir']}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<!-- Google tag (gtag.js) — wird erst nach Consent geladen, siehe js/script.js -->
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('consent', 'default', {{
    'ad_storage': 'denied',
    'ad_user_data': 'denied',
    'ad_personalization': 'denied',
    'analytics_storage': 'denied'
  }});
  window.CF_GA_ID = 'G-T8ESP5R6HR';
</script>
<title>{esc(c['meta']['title'])}</title>
<meta name="description" content="{esc(c['meta']['description'])}">
<meta name="theme-color" content="#DE2910">
<link rel="canonical" href="{SITE_URL}/{lang}/">
{hreflangs}
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="/assets/flag.svg" type="image/svg+xml">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">

<meta property="og:type" content="website">
<meta property="og:site_name" content="China-Flag.cn">
<meta property="og:title" content="{esc(c['meta']['title'])}">
<meta property="og:description" content="{esc(c['meta']['description'])}">
<meta property="og:url" content="{SITE_URL}/{lang}/">
<meta property="og:image" content="{SITE_URL}/assets/og-image.png">
<meta property="og:image:type" content="image/png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{esc(c['hero']['flag_alt'])}">
<meta property="og:locale" content="{meta['og_locale']}">

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(c['meta']['title'])}">
<meta name="twitter:description" content="{esc(c['meta']['description'])}">
<meta name="twitter:image" content="{SITE_URL}/assets/og-image.png">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
{font_link(lang)}
<link rel="stylesheet" href="/css/style.css">
{font_body_style(lang)}

<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "name": "{esc(c['meta']['title'])}",
  "url": "{SITE_URL}/{lang}/",
  "description": "{esc(c['meta']['description'])}",
  "inLanguage": "{meta['html_lang']}",
  "about": {{
    "@type": "Thing",
    "name": "Flag of the People's Republic of China",
    "alternateName": "Five-Star Red Flag"
  }},
  "publisher": {{
    "@type": "Organization",
    "name": "China-Flag.cn"
  }}
}}
</script>
<script type="application/ld+json">
{faq_jsonld(lang)}
</script>
<script type="application/ld+json">
{images_jsonld(lang)}
</script>
<script type="application/ld+json">
{org_jsonld()}
</script>
<script type="application/ld+json">
{breadcrumb_jsonld(lang)}
</script>
</head>
<body>

<header class="site-header">
  <div class="container header-inner">
    <a href="/{lang}/" class="brand">
      <img src="/assets/flag.svg" width="30" height="20" alt="" class="brand-flag">
      <span>{esc(c['brand'])}</span>
    </a>
    <nav class="site-nav" id="siteNav">{nav_links(lang)}
    </nav>
    <div class="header-actions">
      <div class="lang-switch-dropdown">
        <button type="button" class="lang-current" id="langCurrent">{meta['native']}</button>
        <div class="lang-menu" id="langMenu">
          {lang_switcher(lang)}
        </div>
      </div>
      <button type="button" class="nav-toggle" id="navToggle" aria-label="Toggle navigation" aria-expanded="false">
        <span></span><span></span><span></span>
      </button>
    </div>
  </div>
</header>

<main id="top">

  <section class="hero">
    <div class="container hero-inner">
      <div class="hero-flag">
        <img src="/assets/flag.svg" width="300" height="200" fetchpriority="high" alt="{esc(hero['flag_alt'])}">
      </div>
      <h1>{esc(hero['title'])}</h1>
      <p class="hero-sub">{esc(hero['subtitle'])}</p>
      <p class="hero-meta">{esc(hero['meta'])}</p>
    </div>
  </section>
{gallery_section(lang)}
{meaning_section(lang)}
{history_section(lang)}
{historic_section(lang)}
{data_section(lang)}
{coloring_section(lang)}
{emoji_section(lang)}

  <section id="etiquette" class="section section-alt">
    <div class="container">
      <h2 class="section-title">{esc(etiquette['title'])}</h2>
      <p>{esc(etiquette['text'])}</p>
    </div>
  </section>
{faq_section(lang)}
</main>

<footer class="site-footer">
  <div class="container">
    <p>{esc(footer['disclaimer'])}</p>
    <p class="footer-meta">
      <span>© <span id="year"></span> China-Flag.cn</span>
      <button type="button" id="consentSettings" class="consent-settings">{esc(consent['settings'])}</button>
    </p>
  </div>
</footer>

<div class="consent-banner" id="consentBanner" hidden>
  <p>{esc(consent['text'])}</p>
  <div class="consent-actions">
    <button type="button" id="consentAccept" class="consent-btn consent-accept">{esc(consent['accept'])}</button>
    <button type="button" id="consentDecline" class="consent-btn consent-decline">{esc(consent['decline'])}</button>
  </div>
</div>

<script src="/js/script.js"></script>
</body>
</html>
"""
    return html


def slugify_latin(text):
    text = text.lower()
    repl = {
        "ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss",
        "à": "a", "á": "a", "â": "a", "ã": "a", "å": "a",
        "è": "e", "é": "e", "ê": "e", "ë": "e",
        "ì": "i", "í": "i", "î": "i", "ï": "i",
        "ò": "o", "ó": "o", "ô": "o", "õ": "o",
        "ù": "u", "ú": "u", "û": "u",
        "ñ": "n", "ç": "c",
        "ą": "a", "ć": "c", "ę": "e", "ł": "l", "ń": "n",
        "ó": "o", "ś": "s", "ź": "z", "ż": "z",
    }
    for a, b in repl.items():
        text = text.replace(a, b)
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text


def build_pages():
    for lang in LANGS:
        outdir = os.path.join(BASE, lang)
        os.makedirs(outdir, exist_ok=True)
        with open(os.path.join(outdir, "index.html"), "w", encoding="utf-8") as f:
            f.write(render_page(lang))
        print(f"wrote /{lang}/index.html")


def copy_localized_svg(src_assets, outdir, base_file, title, slug):
    with open(os.path.join(src_assets, base_file), "r", encoding="utf-8") as f:
        svg = f.read()
    svg = re.sub(r"(<title id=\"t\">).*?(</title>)", lambda m: m.group(1) + title + m.group(2), svg, count=1, flags=re.S)
    with open(os.path.join(outdir, slug + ".svg"), "w", encoding="utf-8") as f:
        f.write(svg)


def build_images():
    src_assets = os.path.join(BASE, "assets")
    for lang in LANGS:
        outdir = os.path.join(src_assets, lang)
        os.makedirs(outdir, exist_ok=True)
        c = CONTENT[lang]
        n = 0
        for key, meta in GALLERY_ITEMS.items():
            item = c["gallery"]["items"][key]
            copy_localized_svg(src_assets, outdir, meta["base_file"], item["text"], item["slug"])
            n += 1
        for key, meta in HISTORICAL_ITEMS.items():
            item = c["historical"]["items"][key]
            copy_localized_svg(src_assets, outdir, meta["base_file"], item["alt"], item["slug"])
            n += 1
        copy_localized_svg(src_assets, outdir, COLORING_BASE_FILE,
                           c["coloring"]["alt"], c["coloring"]["slug"])
        n += 1
        print(f"wrote {n} images for /{lang}/")


def build_root_redirect():
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta http-equiv="refresh" content="0; url=/en/">
<link rel="canonical" href="{SITE_URL}/en/">
<title>China Flag — redirecting…</title>
</head>
<body>
<p>Redirecting to <a href="/en/">the English version of China-Flag.cn</a>…</p>
</body>
</html>
"""
    with open(os.path.join(BASE, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote root index.html redirect")


def build_404():
    """Custom 404 page. GitHub Pages serves /404.html for any unknown URL,
    so all asset paths must be absolute. noindex keeps it out of search."""
    lang_links = "\n        ".join(
        f'<a href="/{code}/" lang="{LANG_META[code]["html_lang"]}">{LANG_META[code]["native"]}</a>'
        for code in LANGS
    )
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex">
<title>404 — Page not found | China-Flag.cn</title>
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="/assets/flag.svg" type="image/svg+xml">
<link rel="stylesheet" href="/css/style.css">
</head>
<body>
<main class="section" style="min-height:70vh; display:flex; align-items:center;">
  <div class="container" style="text-align:center; max-width:720px;">
    <img src="/assets/flag.svg" width="150" height="100" alt="Flag of the People's Republic of China"
         style="margin:0 auto 28px; border-radius:8px; box-shadow:var(--shadow);">
    <h1 style="font-size:clamp(3rem,8vw,5rem); margin-bottom:8px;">404</h1>
    <p style="font-size:1.1rem; color:var(--ink-soft); margin:0 0 6px;">
      This page does not exist — but the Chinese flag does, in 30 languages:
    </p>
    <p class="fine-print" style="margin:0 0 28px;">Diese Seite existiert nicht · 页面不存在 · Cette page n'existe pas</p>
    <nav style="display:flex; flex-wrap:wrap; gap:10px 18px; justify-content:center; font-size:0.95rem;">
        {lang_links}
    </nav>
  </div>
</main>
</body>
</html>
"""
    with open(os.path.join(BASE, "404.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote 404.html")


def build_sitemap():
    urls = []
    for lang in LANGS:
        images = "\n".join(
            f'    <image:image>\n      <image:loc>{SITE_URL}/assets/{lang}/{slug}.svg</image:loc>\n      <image:title>{esc(name)}</image:title>\n    </image:image>'
            for name, slug in downloadable_images(lang)
        )
        alt_links = "\n".join(
            f'    <xhtml:link rel="alternate" hreflang="{LANG_META[code]["html_lang"]}" href="{SITE_URL}/{code}/"/>'
            for code in LANGS
        )
        urls.append(f"""  <url>
    <loc>{SITE_URL}/{lang}/</loc>
    <changefreq>monthly</changefreq>
    <priority>{"1.0" if lang == "en" else "0.8"}</priority>
{alt_links}
    <image:image>
      <image:loc>{SITE_URL}/assets/flag.svg</image:loc>
      <image:title>Flag of the People's Republic of China (Five-Star Red Flag)</image:title>
    </image:image>
{images}
  </url>""")

    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
{chr(10).join(urls)}
</urlset>
"""
    with open(os.path.join(BASE, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(xml)
    print("wrote sitemap.xml")


def validate_content():
    """Every language must define exactly the same (nested) keys as English.
    Fails the build on missing or extra keys so no language can silently
    fall out of sync with the content structure."""
    def keys_of(d, prefix=""):
        out = set()
        for k, v in d.items():
            path = f"{prefix}.{k}" if prefix else str(k)
            out.add(path)
            if isinstance(v, dict):
                out |= keys_of(v, path)
        return out

    ref = keys_of(CONTENT["en"])
    problems = []
    for lang in LANGS:
        got = keys_of(CONTENT[lang])
        missing = ref - got
        extra = got - ref
        if missing:
            problems.append(f"[{lang}] fehlt: {', '.join(sorted(missing)[:8])}")
        if extra:
            problems.append(f"[{lang}] ueberzaehlig: {', '.join(sorted(extra)[:8])}")
    if problems:
        for p in problems:
            print("VALIDIERUNG:", p)
        raise SystemExit("Content-Validierung fehlgeschlagen — Build abgebrochen.")
    print(f"content ok: {len(LANGS)} Sprachen strukturgleich")


if __name__ == "__main__":
    validate_content()
    build_pages()
    build_images()
    build_root_redirect()
    build_404()
    build_sitemap()
    print("done")
