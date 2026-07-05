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
from content import LANGS, LANG_META, GALLERY_ITEMS, GALLERY_GROUPS, CONTENT

SITE_URL = "https://china-flag.cn"


def esc(s):
    return s if s is None else s.replace("&", "&amp;")


def nav_links(lang):
    c = CONTENT[lang]["nav"]
    return f"""
      <a href="#gallery">{esc(c['gallery'])}</a>
      <a href="#meaning">{esc(c['meaning'])}</a>
      <a href="#history">{esc(c['history'])}</a>
      <a href="#data">{esc(c['data'])}</a>
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
  <section id="data" class="section section-alt">
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


def gallery_section(lang):
    c = CONTENT[lang]["gallery"]
    gi = c["items"]
    dl = CONTENT[lang]["download"]
    groups_html = ""
    for group_key, group_title in GALLERY_GROUPS:
        figures = ""
        for key in GALLERY_ITEMS:
            if GALLERY_ITEMS[key]["group"] != group_key:
                continue
            item = gi[key]
            slug = item["slug"]
            svg_label = esc(dl["svg"].format(name=item["text"]))
            png_label = esc(dl["png"].format(name=item["text"]))
            figures += f"""
        <figure class="gallery-item">
          <img src="/assets/{lang}/{slug}.svg" width="400" height="400" alt="{esc(item['text'])}" loading="lazy">
          <figcaption>{esc(item['text'])}</figcaption>
          <div class="gallery-downloads">
            <a class="download-link" href="/assets/{lang}/{slug}.svg" download="{slug}.svg" aria-label="{svg_label}">SVG</a>
            <span class="download-sep" aria-hidden="true">&middot;</span>
            <button type="button" class="download-link download-png" data-src="/assets/{lang}/{slug}.svg" data-filename="{slug}.png" aria-label="{png_label}">PNG</button>
          </div>
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
  <section id="faq" class="section section-alt">
    <div class="container faq-container">
      <h2 class="section-title">{esc(c['title'])}</h2>{items}
    </div>
  </section>"""


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


def images_jsonld(lang):
    g = CONTENT[lang]["gallery"]
    gi = g["items"]
    entries = []
    for pos, key in enumerate(GALLERY_ITEMS, 1):
        it = gi[key]
        entries.append({
            "@type": "ListItem",
            "position": pos,
            "item": {
                "@type": "ImageObject",
                "name": it["text"],
                "contentUrl": f"{SITE_URL}/assets/{lang}/{it['slug']}.svg",
                "encodingFormat": "image/svg+xml",
                "creator": {"@type": "Organization", "name": "China-Flag.cn"},
                "creditText": "China-Flag.cn",
                "copyrightNotice": "China-Flag.cn",
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

<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-T8ESP5R6HR"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());

  gtag('config', 'G-T8ESP5R6HR');
</script>
<title>{esc(c['meta']['title'])}</title>
<meta name="description" content="{esc(c['meta']['description'])}">
<meta name="theme-color" content="#DE2910">
<link rel="canonical" href="{SITE_URL}/{lang}/">
{hreflangs}
<link rel="icon" href="/assets/flag.svg" type="image/svg+xml">

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
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Noto+Sans+SC:wght@400;500;700;900&family=Noto+Sans+JP:wght@400;500;700;900&family=Noto+Sans+Arabic:wght@400;500;700&family=Noto+Sans+Devanagari:wght@400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/css/style.css">

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
        <img src="/assets/flag.svg" width="300" height="200" alt="{esc(hero['flag_alt'])}">
      </div>
      <h1>{esc(hero['title'])}</h1>
      <p class="hero-sub">{esc(hero['subtitle'])}</p>
      <p class="hero-meta">{esc(hero['meta'])}</p>
    </div>
  </section>
{gallery_section(lang)}
{meaning_section(lang)}
{history_section(lang)}
{data_section(lang)}

  <section id="etiquette" class="section">
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
    </p>
  </div>
</footer>

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


def build_images():
    src_assets = os.path.join(BASE, "assets")
    for lang in LANGS:
        outdir = os.path.join(src_assets, lang)
        os.makedirs(outdir, exist_ok=True)
        gi = CONTENT[lang]["gallery"]["items"]
        for key, meta in GALLERY_ITEMS.items():
            src_file = os.path.join(src_assets, meta["base_file"])
            with open(src_file, "r", encoding="utf-8") as f:
                svg = f.read()
            item = gi[key]
            new_title = item["text"]
            svg = re.sub(r"(<title id=\"t\">).*?(</title>)", lambda m: m.group(1) + new_title + m.group(2), svg, count=1, flags=re.S)
            slug = item["slug"]
            with open(os.path.join(outdir, slug + ".svg"), "w", encoding="utf-8") as f:
                f.write(svg)
        print(f"wrote {len(GALLERY_ITEMS)} images for /{lang}/")


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


def build_sitemap():
    urls = []
    for lang in LANGS:
        gi = CONTENT[lang]["gallery"]["items"]
        images = "\n".join(
            f'    <image:image>\n      <image:loc>{SITE_URL}/assets/{lang}/{gi[key]["slug"]}.svg</image:loc>\n      <image:title>{esc(gi[key]["text"])}</image:title>\n    </image:image>'
            for key in GALLERY_ITEMS
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


if __name__ == "__main__":
    build_pages()
    build_images()
    build_root_redirect()
    build_sitemap()
    print("done")
