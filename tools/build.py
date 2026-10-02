# -*- coding: utf-8 -*-
"""Génère le site statique (4 langues) à partir de tools/content.py.
Usage : python3 tools/build.py
Produit : index.html, tiny-house.html, studio-perche.html, en/…, de/…, nl/…, sitemap.xml, robots.txt
"""
import datetime, html, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content import SITE, UNITS, SETTING_PHOTOS, LANGS, LANG_NAMES, LOCALES, T  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = json.load(open(os.path.join(ROOT, 'tools', 'images.json')))
TODAY = datetime.date.today().isoformat()
e = html.escape


# ---------------------------------------------------------------------------
# URLs
# ---------------------------------------------------------------------------
def path(lang, page):
    """page: 'home' | 'tiny' | 'studio' -> chemin public sans .html (cleanUrls)."""
    prefix = '' if lang == 'fr' else '/' + lang
    if page == 'home':
        return prefix + '/' if prefix == '' else prefix
    return prefix + '/' + UNITS[page]['slug']


def abs_url(lang, page):
    return SITE['url'] + path(lang, page)


def out_file(lang, page):
    d = ROOT if lang == 'fr' else os.path.join(ROOT, lang)
    name = 'index.html' if page == 'home' else UNITS[page]['slug'] + '.html'
    return os.path.join(d, name)


# ---------------------------------------------------------------------------
# Morceaux HTML
# ---------------------------------------------------------------------------
def picture(name, alt, sizes='(max-width: 700px) 100vw, 50vw', eager=False, cls=''):
    v = IMG[name]
    srcset = ', '.join(f'/img/{name}-{w}.webp {v[w][0]}w' for w in v)
    big = max(v, key=int)
    w, h = v[big]
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    c = f' class="{cls}"' if cls else ''
    return (f'<img{c} src="/img/{name}-{big}.webp" srcset="{srcset}" sizes="{sizes}" '
            f'width="{w}" height="{h}" alt="{e(alt)}" {load}>')


def lang_switch(lang, page):
    items = []
    for l in LANGS:
        cur = ' aria-current="true"' if l == lang else ''
        items.append(f'<a href="{path(l, page)}" hreflang="{l}" lang="{l}"{cur}>{l.upper()}</a>')
    return f'<nav class="langs" aria-label="{e(T[lang]["lang_label"])}">' + ''.join(items) + '</nav>'


def head(lang, page, title, desc, jsonld):
    t = T[lang]
    alts = '\n'.join(f'<link rel="alternate" hreflang="{l}" href="{abs_url(l, page)}">' for l in LANGS)
    alts += f'\n<link rel="alternate" hreflang="x-default" href="{abs_url("fr", page)}">'
    og_locale_alt = '\n'.join(f'<meta property="og:locale:alternate" content="{LOCALES[l]}">' for l in LANGS if l != lang)
    gsc = f'<meta name="google-site-verification" content="{SITE["gsc_meta"]}">\n' if lang == 'fr' and page == 'home' else ''
    ld = '\n'.join(f'<script type="application/ld+json">{json.dumps(j, ensure_ascii=False)}</script>' for j in jsonld)
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{abs_url(lang, page)}">
{alts}
{gsc}<meta property="og:type" content="website">
<meta property="og:site_name" content="{e(SITE['name'])}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{abs_url(lang, page)}">
<meta property="og:image" content="{SITE['url']}/img/og-image.jpg">
<meta property="og:locale" content="{LOCALES[lang]}">
{og_locale_alt}
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#1f4d3a">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=Inter:wght@400;500;600&display=swap">
<link rel="stylesheet" href="/styles.css">
{ld}
</head>
<body>
<a class="skip" href="#main">{e(t["skip"])}</a>
'''


def header(lang, page):
    t = T[lang]
    home = path(lang, 'home')
    anchor = '' if page == 'home' else home
    return f'''<header class="site-header">
  <div class="wrap header-inner">
    <a class="brand" href="{home}">
      <span class="brand-name">{e(SITE['name'])}</span>
      <span class="brand-sub">{e(t['tagline'])}</span>
    </a>
    <nav class="main-nav" aria-label="Menu">
      <a href="{path(lang, 'tiny')}"{' aria-current="page"' if page == 'tiny' else ''}>{e(t['nav_tiny'])}</a>
      <a href="{path(lang, 'studio')}"{' aria-current="page"' if page == 'studio' else ''}>{e(t['nav_studio'])}</a>
      <a href="{anchor}#acces" class="hide-sm">{e(t['nav_access'])}</a>
      <a href="{anchor}#contact" class="hide-sm">{e(t['nav_contact'])}</a>
    </nav>
    {lang_switch(lang, page)}
  </div>
</header>
'''


def footer(lang):
    t = T[lang]
    year = datetime.date.today().year
    return f'''<footer class="site-footer">
  <div class="wrap footer-inner">
    <div>
      <p class="footer-brand">{e(SITE['name'])}</p>
      <p>{e(SITE['street'])}<br>{SITE['postal']} {e(SITE['city'])}, France</p>
    </div>
    <div>
      <p><a href="tel:{SITE['phone']}">{SITE['phone_display']}</a><br>
      <a href="mailto:{SITE['email']}">{SITE['email']}</a></p>
    </div>
    <div>
      <p><a href="{path(lang, 'tiny')}">{e(t['nav_tiny'])}</a><br>
      <a href="{path(lang, 'studio')}">{e(t['nav_studio'])}</a></p>
    </div>
  </div>
  <p class="wrap copyright">© {year} {e(SITE['name'])} — {e(t['footer_rights'])}</p>
</footer>
<script src="/site.js" defer></script>
</body>
</html>
'''


def address_ld():
    return {"@type": "PostalAddress", "streetAddress": SITE['street'], "postalCode": SITE['postal'],
            "addressLocality": SITE['city'], "addressRegion": SITE['region'], "addressCountry": SITE['country']}


def business_ld(lang):
    t = T[lang]
    return {
        "@context": "https://schema.org",
        "@type": "LodgingBusiness",
        "@id": SITE['url'] + '/#business',
        "name": SITE['name'],
        "alternateName": SITE['alt_name'],
        "description": t['home_desc'],
        "url": abs_url(lang, 'home'),
        "telephone": SITE['phone'],
        "email": SITE['email'],
        "image": [SITE['url'] + '/img/og-image.jpg'],
        "address": address_ld(),
        "hasMap": SITE['maps_link'],
        "amenityFeature": [
            {"@type": "LocationFeatureSpecification", "name": n, "value": True}
            for n in ("Wi-Fi", "Parking", "Kitchen", "Garden", "River access")
        ],
        "containsPlace": [{"@id": abs_url(lang, u) + '#accommodation'} for u in ('tiny', 'studio')],
        "sameAs": [UNITS['tiny']['airbnb'], UNITS['studio']['airbnb'], UNITS['tiny']['booking'], UNITS['studio']['booking']],
        "availableLanguage": ["fr", "en", "de", "nl"],
    }


def breadcrumb_ld(lang, page):
    t = T[lang]
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": SITE['name'], "item": abs_url(lang, 'home')},
        {"@type": "ListItem", "position": 2, "name": t[page]['name'], "item": abs_url(lang, page)},
    ]}


def unit_ld(lang, key):
    t = T[lang][key]; u = UNITS[key]
    d = {
        "@context": "https://schema.org",
        "@type": "Accommodation" if key == 'studio' else "House",
        "@id": abs_url(lang, key) + '#accommodation',
        "name": f"{t['name']} — {SITE['name']}",
        "description": t['desc'],
        "url": abs_url(lang, key),
        "image": [f"{SITE['url']}/img/{p}-{max(IMG[p], key=int)}.webp" for p in u['photos']],
        "address": address_ld(),
        "occupancy": {"@type": "QuantitativeValue", "maxValue": u['guests']},
        "amenityFeature": [{"@type": "LocationFeatureSpecification", "name": f, "value": True} for f in t['features']],
        "containedInPlace": {"@id": SITE['url'] + '/#business'},
    }
    if u['size']:
        d["floorSize"] = {"@type": "QuantitativeValue", "value": u['size'], "unitCode": "MTK"}
    return d


def faq_html(lang):
    t = T[lang]
    items = ''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in t['faq'])
    return f'<section class="section wrap" id="faq"><h2>{e(t["faq_h2"])}</h2><div class="faq">{items}</div></section>'


def li(items):
    return '<ul class="checks">' + ''.join(f'<li>{e(i)}</li>' for i in items) + '</ul>'


def book_buttons(lang, key, small=False):
    t = T[lang]; u = UNITS[key]
    s = ' btn-sm' if small else ''
    return (f'<div class="actions"><a class="btn btn-airbnb{s}" href="{u["airbnb"]}" target="_blank" rel="noopener">{e(t["book_airbnb"])}</a>'
            f'<a class="btn btn-booking{s}" href="{u["booking"]}" target="_blank" rel="noopener">{e(t["book_booking"])}</a></div>')


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------
def home_page(lang):
    t = T[lang]
    cards = ''
    for key in ('tiny', 'studio'):
        u = UNITS[key]; tu = t[key]
        meta = [t['guests'].format(n=u['guests'])]
        if u['size']:
            meta.append(t['m2'].format(n=u['size']))
        cards += f'''<article class="card">
  <a href="{path(lang, key)}" class="card-img">{picture(u['cover'], tu['alts'][0], '(max-width: 700px) 100vw, 540px')}</a>
  <div class="card-body">
    <h3><a href="{path(lang, key)}">{e(tu['name'])}</a></h3>
    <p class="meta">{' · '.join(e(m) for m in meta)}</p>
    <p>{e(tu['short'])}</p>
    <a class="btn btn-primary" href="{path(lang, key)}">{e(t['see_unit'])} →</a>
  </div>
</article>'''

    gallery = ''.join(
        f'<a class="g-item" href="/img/{p}-{max(IMG[p], key=int)}.webp">{picture(p, t["setting_alts"][i], "(max-width: 700px) 50vw, 33vw")}</a>'
        for i, p in enumerate(SETTING_PHOTOS))

    reviews = ''.join(f'<a class="btn btn-outline" href="{href}" target="_blank" rel="noopener">{e(label)}</a>' for label, href in [
        (t['rv_airbnb_tiny'], UNITS['tiny']['airbnb'] + '#reviews'),
        (t['rv_airbnb_studio'], UNITS['studio']['airbnb'] + '#reviews'),
        (t['rv_booking_tiny'], UNITS['tiny']['booking'] + '#tab-reviews'),
        (t['rv_booking_studio'], UNITS['studio']['booking'] + '#tab-reviews'),
        (t['rv_google'], SITE['google_reviews']),
    ])

    body = f'''<main id="main">
<section class="hero">
  {picture('vue-aerienne-maison-pulligny', t['hero_alt'], '100vw', eager=True, cls='hero-bg')}
  <div class="hero-shade"></div>
  <div class="wrap hero-content">
    <p class="kicker">{e(t['hero_kicker'])}</p>
    <h1>{e(t['hero_h1'])}</h1>
    <p class="lead">{e(t['hero_p'])}</p>
    <div class="actions">
      <a class="btn btn-primary" href="#logements">{e(t['hero_cta1'])}</a>
      <a class="btn btn-light" href="{path(lang, 'tiny')}#dispo">{e(t['hero_cta2'])}</a>
    </div>
    <p class="badge">★ {e(t['badge'])}</p>
  </div>
</section>

<section class="section wrap" id="logements">
  <h2>{e(t['units_h2'])}</h2>
  <div class="cards">{cards}</div>
</section>

<section class="section band" id="cadre">
  <div class="wrap split">
    <div>
      <h2>{e(t['setting_h2'])}</h2>
      <p>{e(t['setting_p'])}</p>
      {li(t['setting_list'])}
    </div>
    <div class="gallery gallery-3" data-gallery>{gallery}</div>
  </div>
</section>

<section class="section wrap two-col">
  <div>
    <h2>{e(t['road_h2'])}</h2>
    <p>{e(t['road_p'])}</p>
    {li(t['road_list'])}
  </div>
  <div>
    <h2>{e(t['pro_h2'])}</h2>
    <p>{e(t['pro_p'])}</p>
  </div>
</section>

<section class="section band" id="avis">
  <div class="wrap">
    <h2>{e(t['reviews_h2'])}</h2>
    <p>{e(t['reviews_p'])}</p>
    <div class="actions wrap-actions">{reviews}</div>
  </div>
</section>

<section class="section wrap split" id="acces">
  <div>
    <h2>{e(t['access_h2'])}</h2>
    <address>{e(SITE['street'])}<br>{SITE['postal']} {e(SITE['city'])}, France</address>
    {li(t['access_list'])}
    <a class="btn btn-outline" href="{SITE['maps_link']}" target="_blank" rel="noopener">{e(t['open_maps'])}</a>
  </div>
  <div class="map"><iframe title="{e(t['access_h2'])} — {e(SITE['city'])}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="{SITE['maps_embed']}"></iframe></div>
</section>

{faq_html(lang)}

<section class="section band" id="contact">
  <div class="wrap">
    <h2>{e(t['contact_h2'])}</h2>
    <p>{e(t['contact_p'])}</p>
    <div class="actions">
      <a class="btn btn-primary" href="tel:{SITE['phone']}">☎ {SITE['phone_display']}</a>
      <a class="btn btn-outline" href="mailto:{SITE['email']}">✉ {SITE['email']}</a>
    </div>
  </div>
</section>
</main>
'''
    jsonld = [business_ld(lang), {
        "@context": "https://schema.org", "@type": "WebSite", "name": SITE['name'],
        "alternateName": SITE['alt_name'], "url": abs_url(lang, 'home'), "inLanguage": lang}]
    return head(lang, 'home', t['home_title'], t['home_desc'], jsonld) + header(lang, 'home') + body + footer(lang)


def unit_page(lang, key):
    t = T[lang]; tu = t[key]; u = UNITS[key]
    other = 'studio' if key == 'tiny' else 'tiny'
    meta = [t['guests'].format(n=u['guests'])]
    if u['size']:
        meta.append(t['m2'].format(n=u['size']))
    photos = u['photos']
    main_img = (f'<a class="g-item g-main" href="/img/{photos[0]}-{max(IMG[photos[0]], key=int)}.webp">'
                f'{picture(photos[0], tu["alts"][0], "(max-width: 700px) 100vw, 60vw", eager=True)}</a>')
    thumbs = ''.join(
        f'<a class="g-item" href="/img/{p}-{max(IMG[p], key=int)}.webp">{picture(p, tu["alts"][i + 1], "(max-width: 700px) 50vw, 20vw")}</a>'
        for i, p in enumerate(photos[1:]))
    ot = t[other]; ou = UNITS[other]
    body = f'''<main id="main">
<nav class="wrap crumbs" aria-label="Breadcrumb"><a href="{path(lang, 'home')}">{e(t['back_home'])}</a> › <span>{e(tu['name'])}</span></nav>
<section class="wrap unit-head">
  <h1>{e(tu['h1'])}</h1>
  <p class="meta">{' · '.join(e(m) for m in meta)} · {e(SITE['city'])}</p>
  {book_buttons(lang, key)}
</section>
<section class="wrap unit-gallery" data-gallery aria-label="{e(t['gallery_label'])}">
  {main_img}{thumbs}
</section>
<section class="section wrap two-col">
  <div>
    <p class="lead dark">{e(tu['intro'])}</p>
  </div>
  <div>
    <h2>{e(t['features_h2'])}</h2>
    {li(tu['features'])}
  </div>
</section>
<section class="section band" id="dispo">
  <div class="wrap">
    <h2>{e(t['avail_h2'])}</h2>
    <p class="small">{e(t['avail_note'])}</p>
    <div class="calendar" data-calendar="{u['calendar']}" data-locale="{lang}" data-error="{e(t['avail_err'])}"></div>
    {book_buttons(lang, key)}
  </div>
</section>
<section class="section wrap">
  <h2>{e(t['other_unit'])} : {e(ot['name'])}</h2>
  <article class="card card-row">
    <a href="{path(lang, other)}" class="card-img">{picture(ou['cover'], ot['alts'][0], '(max-width: 700px) 100vw, 400px')}</a>
    <div class="card-body">
      <p>{e(ot['short'])}</p>
      <a class="btn btn-primary" href="{path(lang, other)}">{e(t['see_unit'])} →</a>
    </div>
  </article>
</section>
{faq_html(lang)}
</main>
'''
    jsonld = [unit_ld(lang, key), breadcrumb_ld(lang, key)]
    return head(lang, key, tu['title'], tu['desc'], jsonld) + header(lang, key) + body + footer(lang)


# ---------------------------------------------------------------------------
def write(p, s):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(s)


def main():
    for lang in LANGS:
        write(out_file(lang, 'home'), home_page(lang))
        for key in ('tiny', 'studio'):
            write(out_file(lang, key), unit_page(lang, key))

    # sitemap avec alternates hreflang
    urls = []
    for page in ('home', 'tiny', 'studio'):
        for lang in LANGS:
            alts = ''.join(f'\n    <xhtml:link rel="alternate" hreflang="{l}" href="{abs_url(l, page)}"/>' for l in LANGS)
            alts += f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{abs_url("fr", page)}"/>'
            urls.append(f'  <url>\n    <loc>{abs_url(lang, page)}</loc>\n    <lastmod>{TODAY}</lastmod>{alts}\n  </url>')
    write(os.path.join(ROOT, 'sitemap.xml'),
          '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
          + '\n'.join(urls) + '\n</urlset>\n')
    write(os.path.join(ROOT, 'robots.txt'), f'User-agent: *\nAllow: /\n\nSitemap: {SITE["url"]}/sitemap.xml\n')
    print('Site généré :', len(LANGS) * 3, 'pages —', SITE['url'])


if __name__ == '__main__':
    main()
