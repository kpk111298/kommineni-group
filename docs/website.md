# Website

The Kommineni Group website is published at pkomm.com/group, inside the pkomm.com portfolio site. One Cloudflare project serves both.

## How it's built

- All page content lives in `tools/build_site.py`: the businesses, the problems and the roadmap.
- Styles and fonts live in `site-src/`. Fonts are self-hosted (Cormorant Garamond and Jost, both SIL Open Font License).
- The logos come from `brand/`. The build copies them in, and draws the favicon and share image (`pip install cairosvg` for the PNGs).
- Every link starts with `/group`, so the pages work inside the portfolio site.
- `site/` holds the latest build, so the pages can be read straight from this repo.

## Publishing

The portfolio repo, `kpk111298/Pkomm-Portfolio`, serves these pages from its `Pkomm Portfolio/group/` folder. To publish a change, build straight into it from this repo's root:

```
OUT="../pkomm-portfolio/Pkomm Portfolio/group" python3 tools/build_site.py
```

Then commit in the portfolio repo. Cloudflare publishes it like any other portfolio change: the `development` branch to dev.pkomm.com/group, and `main` to pkomm.com/group.

The portfolio site owns the shared files: the 404 page, `_redirects`, `_headers`, `robots.txt` and `sitemap.xml`. Short addresses such as pkomm.com/group/motors are set in its `_redirects`.

## Pages

| Address | Page |
|---|---|
| `/group/` | Home: the family of businesses, latest problems, how a day runs |
| `/group/meel-motors/` and one per business | What the business does, its data, what makes it hard, its problems |
| `/group/engineering/` | Every logged problem and the roadmap |
| `/group/about/` | How the company works, what's real and what isn't, the tool map |

## Preview on your machine

From the portfolio repo, run `npm run serve` and open http://localhost:8788/group/.
