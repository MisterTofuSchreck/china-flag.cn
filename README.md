# China-Flag.cn

An informative, bilingual (English / 中文) static website about the flag of the People's Republic of China — the Five-Star Red Flag (五星红旗).

## Contents

- **Meaning & Symbolism** — what the red field, the large star and the four small stars represent
- **History & Origin** — adoption in 1949, designer Zeng Liansong, national standards
- **Technical Data** — official proportions (3:2), construction grid, star geometry, colors
- **Gallery** — illustrated mockups of the flag motif on a box, a car and a phone
- **Display & Etiquette** — basic rules for flying the flag

## Stack

Plain HTML, CSS and vanilla JavaScript — no build step, no dependencies. The flag and gallery illustrations are hand-built SVGs (see `assets/`), using the flag's official construction grid (30×20 units) for accurate star geometry.

## Running locally

Serve the folder with any static file server, e.g.:

```
python -m http.server 5500
```

Then open `http://localhost:5500`.

## Disclaimer

This is an independent, unofficial informational project. It is not affiliated with, endorsed by, or operated on behalf of any government.
