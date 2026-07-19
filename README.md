# Sale engine

Shared front-end engine for the static sale-catalog sites — plain HTML/CSS/vanilla
JS, no build step. Served from this repo via GitHub Pages and loaded by each site by URL:

    https://hellopavlo.github.io/sale-engine/engine/app.js
    https://hellopavlo.github.io/sale-engine/engine/styles.css

- `engine/app.js` — catalog logic (reads each site's `data/config.json` + Google Sheet)
- `engine/styles.css` — styling; the accent color is driven by CSS variables
  (`--accent`, `--accent-dark`, `--accent-hover`) that each site overrides in its
  own `data/theme.css`. Defaults here are neutral greens.

Each consuming site keeps its own `index.html` (with the two URLs above), `data/config.json`,
`data/theme.css`, `CNAME`, `favicon.ico`, and `assets/images/`.

**Shipping an update:** commit and push here. Both live sites pick it up automatically
once GitHub Pages purges its CDN (~minutes) — no per-site commits. A bad push reaches
every site at once, so test before pushing.

## tools/

- `tools/optimize-images.py` — resizes a sale's originals in `assets/images/` into the
  `web/` + `thumb/` copies the sites serve. Run it from a sale repo's root (needs Pillow).
  Kept here as the canonical home; it is intentionally not committed to the individual
  sale repos.
