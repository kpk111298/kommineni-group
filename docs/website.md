# Website

The Kommineni Group website lives in `site/` and is published at group.pkomm.com.

## How it's built

- All page content lives in `tools/build_site.py`: the businesses, the problems and the roadmap.
- Run `python3 tools/build_site.py` from the repo root to rebuild every page into `site/`.
- Styles are in `site/assets/site.css`. Fonts are self-hosted (Cormorant Garamond and Jost, both SIL Open Font License).
- The logos come from `brand/`. The build copies them in, and draws the favicon and share image (`pip install cairosvg` for the PNGs).
- Commit the built pages. Cloudflare publishes `site/` as it is, with no build step.

## Pages

| Address | Page |
|---|---|
| `/` | Home: the family of businesses, latest problems, how a day runs |
| `/meel-motors/` and one per business | What the business does, its data, what makes it hard, its problems |
| `/engineering/` | Every logged problem and the roadmap |
| `/about/` | How the company works, what's real and what isn't, the tool map |

Short addresses like `/motors` and `/problems` redirect (see `site/_redirects`).

## Cloudflare Pages setup

1. In Cloudflare, go to Workers & Pages and create a Pages project connected to `kpk111298/kommineni-group`.
2. Production branch: `main`. Build command: leave empty. Build output directory: `site`.
3. Under the project's Custom domains, add `group.pkomm.com`. Cloudflare adds the DNS record because pkomm.com is already on Cloudflare.

## Preview on your machine

From `site/`, run `python3 -m http.server 8000` and open http://localhost:8000.
