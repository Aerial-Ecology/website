#!/usr/bin/env python3
"""Build the Aerial Ecology static site.

Each file in src/pages/ starts with a small header block, then the page body:

    title: Page title
    description: Meta description
    nav: services
    ---
    <section>...</section>

Run:  python3 src/build.py   (writes the finished pages into site/)
"""
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = ROOT / "src" / "pages"
OUT = ROOT / "site"
SITE_URL = "https://www.aerial-ecology.co.uk"

# Enquiry form endpoint. Paste the form service URL here (for example a Formspree form URL such as
# https://formspree.io/f/abcdwxyz), then rebuild. Left empty, the form falls back to opening an email.
FORM_ENDPOINT = "https://formspree.io/f/xbggggav"

# Company number for the footer (Companies House). Left empty, it is not shown.
COMPANY_NUMBER = "16701025"

LOGO = '<img src="images/logo-reversed.png" alt="Aerial Ecology" width="{w}" height="{h}">'

HEAD = """<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">{base}
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical}">
<meta property="og:locale" content="en_GB">
<meta property="og:site_name" content="Aerial Ecology">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="https://www.aerial-ecology.co.uk/images/og-image.jpg">
<link rel="icon" type="image/png" href="images/favicon.png">
<link rel="apple-touch-icon" href="images/apple-touch-icon.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="https://www.aerial-ecology.co.uk/images/og-image.jpg">{robots}
<meta name="theme-color" content="#081110">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/site.css">
{schema}</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site">
  <nav class="wrap nav" id="nav" aria-label="Main">
    <a class="logo" href="index.html">{logo}</a>
    <ul class="menu">
      <li class="has-sub">
        <a href="services.html" aria-haspopup="true"{cur_services}>Services</a>
        <ul class="sub">
          <li><a href="dabes.html">Thermal bat surveys<small>Aerial and ground-based emergence and re-entry</small></a></li>
          <li><a href="skylarks.html">Skylark nest surveys<small>Two-stage thermal nest detection</small></a></li>
          <li><a href="services.html#habitat">Habitat mapping &amp; GIS<small>Aerial imagery, LiDAR and spatial analysis</small></a></li>
          <li><a href="services.html">All services</a></li>
        </ul>
      </li>
      <li><a href="work.html"{cur_work}>Our work</a></li>
      <li><a href="about.html"{cur_about}>About</a></li>
      <li><a href="contact.html"{cur_contact}>Contact</a></li>
    </ul>
    <a class="btn" href="contact.html">Discuss a project</a>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="nav">Menu</button>
  </nav>
</header>
<main id="main">
"""

FOOT = """</main>
<footer class="site">
  <div class="wrap">
    <div class="foot">
      <div class="stack">
        <a class="logo logo-lg" href="index.html">{logo}</a>
        <p>Specialist ecological survey services: aerial and ground-based thermal imaging, drone surveys, habitat mapping and GIS for ecological consultancies across the UK.</p>
      </div>
      <div>
        <h4>Explore</h4>
        <ul>
          <li><a href="dabes.html">Thermal bat surveys</a></li>
          <li><a href="skylarks.html">Skylark nest surveys</a></li>
          <li><a href="services.html">All services</a></li>
          <li><a href="work.html">Our work</a></li>
          <li><a href="about.html">About</a></li>
          <li><a href="contact.html">Contact</a></li>
        </ul>
      </div>
      <div>
        <h4>Contact</h4>
        <ul>
          <li><a href="mailto:info@aerial-ecology.co.uk">info@aerial-ecology.co.uk</a></li>
          <li><a href="https://www.linkedin.com/company/aerial-ecology" rel="noopener">LinkedIn</a></li>
          <li><a href="https://www.youtube.com/@Aerial_Ecology" rel="noopener">YouTube</a></li>
          <li><a href="https://sketchfab.com/Aerial-Ecology" rel="noopener">Sketchfab</a></li>
        </ul>
      </div>
      <div>
        <h4>Registered office</h4>
        <address>Aerial Ecology Ltd<br>Suite 1 Just Simply Organised<br>Ringles Cross<br>Uckfield, England<br>TN22 1HB</address>
      </div>
    </div>
    <div class="legal">
      <span>&copy; <span id="year">2026</span> Aerial Ecology Ltd. Registered in England and Wales{company}. <a href="privacy.html">Privacy notice</a></span>
      <span>Based in East Sussex, working across the UK</span>
    </div>
  </div>
</footer>
<script src="js/site.js"></script>
</body>
</html>
"""

ORG = {
    "@type": "ProfessionalService",
    "@id": SITE_URL + "/#org",
    "name": "Aerial Ecology Ltd",
    "url": SITE_URL + "/",
    "logo": SITE_URL + "/images/mark-512.png",
    "image": SITE_URL + "/images/og-image.jpg",
    "email": "info@aerial-ecology.co.uk",
    "description": "Specialist ecological survey services combining aerial and ground-based thermal imaging, drone technology and GIS for ecological consultancies.",
    "address": {"@type": "PostalAddress", "streetAddress": "Suite 1 Just Simply Organised, Ringles Cross",
                "addressLocality": "Uckfield", "postalCode": "TN22 1HB", "addressCountry": "GB"},
    "areaServed": ["East Sussex", "West Sussex", "Surrey", "Kent", "Hampshire", "United Kingdom"],
    "sameAs": ["https://www.linkedin.com/company/aerial-ecology", "https://www.youtube.com/@Aerial_Ecology",
               "https://sketchfab.com/Aerial-Ecology"],
}



def parse(path):
    raw = path.read_text(encoding="utf-8")
    meta_block, body = raw.split("\n---\n", 1)
    meta = {}
    for line in meta_block.strip().splitlines():
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip()
    return meta, body


def schema_for(meta, url, crumb):
    graph = [ORG]
    if meta.get("service"):
        graph.append({"@type": "Service", "name": meta["service"], "serviceType": meta["service"],
                      "description": meta["description"], "url": url, "provider": {"@id": SITE_URL + "/#org"},
                      "areaServed": "United Kingdom"})
    if crumb:
        graph.append({"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE_URL + "/"},
            {"@type": "ListItem", "position": 2, "name": crumb, "item": url}]})
    data = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)
    return '<script type="application/ld+json">' + data + "</script>\n"


def main():
    OUT.mkdir(exist_ok=True)
    if not FORM_ENDPOINT:
        print("WARNING: FORM_ENDPOINT is empty, so the enquiry form will open an email instead of sending.")
    urls = []
    for path in sorted(PAGES.glob("*.html")):
        meta, body = parse(path)
        nav = meta.get("nav", "")
        cur = {k: ' aria-current="page"' if nav == k else "" for k in ("services", "work", "about", "contact")}
        slug = "" if path.stem == "index" else path.stem
        canonical = SITE_URL + "/" + slug
        noindex = meta.get("index") == "no"
        if not noindex:
            urls.append(canonical)
        head = HEAD.format(
            title=meta["title"], description=meta["description"], canonical=canonical,
            logo=LOGO.format(w=200, h=48), schema=schema_for(meta, canonical, meta.get("crumb", "")),
            robots='\n<meta name="robots" content="noindex">' if noindex else "",
            base='\n<base href="/">' if meta.get("base") == "root" else "",
            cur_services=cur["services"], cur_work=cur["work"], cur_about=cur["about"], cur_contact=cur["contact"],
        )
        company = ", company no. " + COMPANY_NUMBER if COMPANY_NUMBER else ""
        body = body.replace("{FORM_ENDPOINT}", FORM_ENDPOINT).replace(
            "{FORM_ACTION}", FORM_ENDPOINT or "mailto:info@aerial-ecology.co.uk")
        html = head + body + FOOT.format(logo=LOGO.format(w=250, h=60), company=company)
        (OUT / path.name).write_text(html, encoding="utf-8")
        print("built", path.name)

    today = date.today().isoformat()
    entries = "".join(f"  <url><loc>{u}</loc><lastmod>{today}</lastmod></url>\n" for u in urls)
    (OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + entries + "</urlset>\n", encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n", encoding="utf-8")
    (OUT / ".nojekyll").write_text("", encoding="utf-8")
    print("built sitemap.xml, robots.txt, .nojekyll")


if __name__ == "__main__":
    main()
