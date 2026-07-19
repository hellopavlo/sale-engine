# Sale engine

Shared front-end engine for the static sale-catalog sites — plain HTML/CSS/vanilla
JS, no build step. Consumed by each site as a git submodule mounted at `engine/`.

- `engine/app.js` — catalog logic (reads each site's `data/config.json` + Google Sheet)
- `engine/styles.css` — styling; the accent color is driven by CSS variables
  (`--accent`, `--accent-dark`, `--accent-hover`) that each site overrides in its
  own `data/theme.css`. Defaults here are neutral greens.

Each consuming site keeps its own `index.html`, `data/config.json`, `data/theme.css`,
`CNAME`, `favicon.ico`, and `assets/images/`. To ship an engine update: commit here,
then in each site bump the submodule pointer and the `?v=N` cache-buster in `index.html`.
