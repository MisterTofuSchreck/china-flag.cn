# China-Flag.cn

An informative static website about the flag of the People's Republic of China — the Five-Star Red Flag (五星红旗) — available in 13 languages, each as its own subpage for SEO (`/en/`, `/zh/`, `/de/`, `/fr/`, `/es/`, `/it/`, `/hi/`, `/ar/`, `/pt/`, `/ja/`, `/sv/`, `/nl/`, `/pl/`).

## Contents

- **Meaning & Symbolism** — what the red field, the large star and the four small stars represent
- **History & Origin** — adoption in 1949, designer Zeng Liansong, national standards
- **Technical Data** — official proportions (3:2), construction grid, star geometry, colors
- **Gallery** — 33 flag-themed illustrations (everyday objects, animals popular in China, landmarks and the map of China), each with a translated filename and alt text per language
- **Display & Etiquette** — basic rules for flying the flag

## Stack

Plain HTML, CSS and vanilla JavaScript at request time — no server-side build, no dependencies. The per-language pages and image copies are generated ahead of time by a small Python script and committed as static output (see below).

## Editing content / adding a language

All translated text lives in `scripts/lang_<code>.py` (one file per language) plus shared structure in `scripts/content.py`. To change copy or add a language:

1. Edit the relevant `scripts/lang_<code>.py` (or add a new one and register it in `scripts/content.py` and `LANGS`).
2. Regenerate every page and image copy:
   ```
   python scripts/build.py
   ```
   This rewrites `/xx/index.html` for each language, copies the 33 base SVGs in `assets/` into `assets/<lang>/` with translated filenames and `<title>` text, rewrites the root redirect page, and regenerates `sitemap.xml`.
3. Commit the generated output along with your source changes.

The master illustrations (`assets/chinese-flag-shaped-*.svg` and `assets/flag.svg`) are the source of truth for artwork; don't edit the per-language copies directly since they're overwritten on every build.

## Running locally

Serve the repository root with any static file server, e.g.:

```
python -m http.server 5500
```

Then open `http://localhost:5500` (redirects to `/en/`).

## Disclaimer

This is an independent, unofficial informational project. It is not affiliated with, endorsed by, or operated on behalf of any government.
