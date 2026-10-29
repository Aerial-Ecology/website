# Aerial Ecology website

Source for www.aerial-ecology.co.uk, published with GitHub Pages.

- `src/pages/` holds the page content. Each file starts with a short header (title, description, nav and so on), then `---`, then the page body.
- `src/build.py` combines each page with the shared header and footer and writes the finished pages into `site/`, along with `sitemap.xml` and `robots.txt`.
- `site/css`, `site/js` and `site/images` hold the design, scripts and images.

## Editing

1. Edit a page in `src/pages/`.
2. Run `python3 src/build.py`.
3. Open `site/index.html` in a browser to check it.

Merging to `main` publishes the site automatically (see `.github/workflows/pages.yml`).

## Settings in `src/build.py`

- `FORM_ACCESS_KEY`: the Web3Forms access key for the enquiry form. Empty means the form opens a pre-filled email instead.
- `COMPANY_NUMBER`: shown in the footer when set.

## Custom domain

Live at www.aerial-ecology.co.uk. The custom domain is set in the repository's Settings, Pages (no `CNAME` file is needed with the Actions deploy). Only the website DNS records point at GitHub; keep the Microsoft 365 email records unchanged.
