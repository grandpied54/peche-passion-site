# -*- coding: utf-8 -*-
"""Génère un mini-site dédié à UN logement (Tiny House ou Studio Perché), en 4 langues.
Usage : python3 tools/build_unit.py tiny  <dossier_sortie>
        python3 tools/build_unit.py studio <dossier_sortie>
"""
import datetime, json, os, shutil, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build as B  # noqa: E402  (réutilise les briques HTML du site principal)
from content import SITE, UNITS, SETTING_PHOTOS, LANGS, LOCALES, T  # noqa: E402

ROOT = B.ROOT
e = B.e

# Adresse publique de chaque mini-site (= nom du projet Vercel). À changer si domaine perso.
UNIT_SITES = {
    "tiny": {"url": "https://tiny-house-pulligny.vercel.app", "name": "Tiny House Pulligny"},
    "studio": {"url": "https://studio-perche-pulligny.vercel.app", "name": "Studio Perché Pulligny"},
}
MAIN_URL = "https://peche-passion-site.vercel.app"

EXTRA = {
    "fr": {"sister": "Le logement voisin", "sister_btn": "Voir le site du {n}", "main": "Tous nos hébergements",
           "reviews_unit": "Les voyageurs de ce logement citent surtout la propreté, l'accueil, le calme et l'emplacement au bord de l'eau. Lisez leurs avis :"},
    "en": {"sister": "Next door", "sister_btn": "Visit the {n} website", "main": "All our rentals",
           "reviews_unit": "Guests mostly mention cleanliness, hospitality, the peace and quiet and the riverside location. Read their reviews:"},
    "de": {"sister": "Gleich nebenan", "sister_btn": "Zur Website des {n}", "main": "Alle unsere Unterkünfte",
           "reviews_unit": "Gäste loben vor allem Sauberkeit, Gastfreundschaft, Ruhe und die Lage am Wasser. Lesen Sie ihre Bewertungen:"},
    "nl": {"sister": "Hiernaast", "sister_btn": "Naar de website van de {n}", "main": "Al onze verblijven",
           "reviews_unit": "Gasten noemen vooral de netheid, de gastvrijheid, de rust en de ligging aan het water. Lees hun beoordelingen:"},
}


def p(lang):
    return '/' if lang == 'fr' else '/' + lang


def url(base, lang):
    return base + ('/' if lang == 'fr' else '/' + lang)


def head(key, lang, jsonld):
    t = T[lang][key]; base = UNIT_SITES[key]['url']
    alts = '\n'.join(f'<link rel="alternate" hreflang="{l}" href="{url(base, l)}">' for l in LANGS)
    alts += f'\n<link rel="alternate" hreflang="x-default" href="{url(base, "fr")}">'
    og_img = f"{base}/img/{UNITS[key]['cover']}-{max(B.IMG[UNITS[key]['cover']], key=int)}.webp"
    ld = '\n'.join(f'<script type="application/ld+json">{json.dumps(j, ensure_ascii=False)}</script>' for j in jsonld)
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(t['title'])}</title>
<meta name="description" content="{e(t['desc'])}">
<link rel="canonical" href="{url(base, lang)}">
{alts}
<meta property="og:type" content="website">
<meta property="og:site_name" content="{e(UNIT_SITES[key]['name'])}">
<meta property="og:title" content="{e(t['title'])}">
<meta property="og:description" content="{e(t['desc'])}">
<meta property="og:url" content="{url(base, lang)}">
<meta property="og:image" content="{og_img}">
<meta property="og:locale" content="{LOCALES[lang]}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#1f4d3a">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=Inter:wght@400;500;600&display=swap">
<link rel="stylesheet" href="/styles.css">
{ld}
</head>
<body>
<a class="skip" href="#main">{e(T[lang]["skip"])}</a>
'''


def header(key, lang):
    t = T[lang]
    cur = ' aria-current="true"'
    langs = ''.join(f'<a href="{p(l)}" hreflang="{l}" lang="{l}"{cur if l == lang else ""}>{l.upper()}</a>' for l in LANGS)
    return f'''<header class="site-header">
  <div class="wrap header-inner">
    <a class="brand" href="{p(lang)}">
      <span class="brand-name">{e(UNIT_SITES[key]['name'])}</span>
      <span class="brand-sub">{e(SITE['name'])} · {e(t['tagline'])}</span>
    </a>
    <nav class="main-nav" aria-label="Menu">
      <a href="#dispo">{e(t['avail_h2'])}</a>
      <a href="#acces" class="hide-sm">{e(t['nav_access'])}</a>
      <a href="#contact" class="hide-sm">{e(t['nav_contact'])}</a>
    </nav>
    <nav class="langs" aria-label="{e(t['lang_label'])}">{langs}</nav>
  </div>
</header>
'''


def footer(key, lang):
    t = T[lang]; x = EXTRA[lang]
    other = 'studio' if key == 'tiny' else 'tiny'
    year = datetime.date.today().year
    return f'''<footer class="site-footer">
  <div class="wrap footer-inner">
    <div>
      <p class="footer-brand">{e(UNIT_SITES[key]['name'])}</p>
      <p>{e(SITE['street'])}<br>{SITE['postal']} {e(SITE['city'])}, France</p>
    </div>
    <div>
      <p><a href="tel:{SITE['phone']}">{SITE['phone_display']}</a><br>
      <a href="mailto:{SITE['email']}">{SITE['email']}</a></p>
    </div>
    <div>
      <p><a href="{url(UNIT_SITES[other]['url'], lang)}">{e(T[lang][other]['name'])}</a><br>
      <a href="{url(MAIN_URL, lang)}">{e(x['main'])}</a></p>
    </div>
  </div>
  <p class="wrap copyright">© {year} {e(SITE['name'])} — {e(t['footer_rights'])}</p>
</footer>
<script src="/site.js" defer></script>
</body>
</html>
'''


def page(key, lang):
    t = T[lang]; tu = t[key]; u = UNITS[key]; x = EXTRA[lang]; base = UNIT_SITES[key]['url']
    other = 'studio' if key == 'tiny' else 'tiny'; ot = t[other]; ou = UNITS[other]
    meta = [t['guests'].format(n=u['guests'])] + ([t['m2'].format(n=u['size'])] if u['size'] else [])
    photos = u['photos']
    big = lambda n: max(B.IMG[n], key=int)
    gallery = (f'<a class="g-item g-main" href="/img/{photos[0]}-{big(photos[0])}.webp">'
               f'{B.picture(photos[0], tu["alts"][0], "(max-width: 700px) 100vw, 60vw", eager=True)}</a>'
               + ''.join(f'<a class="g-item" href="/img/{ph}-{big(ph)}.webp">{B.picture(ph, tu["alts"][i + 1], "(max-width: 700px) 84vw, 20vw")}</a>'
                         for i, ph in enumerate(photos[1:])))
    setting = ''.join(f'<a class="g-item" href="/img/{ph}-{big(ph)}.webp">{B.picture(ph, t["setting_alts"][i], "(max-width: 700px) 50vw, 33vw")}</a>'
                      for i, ph in enumerate(SETTING_PHOTOS))
    reviews = ''.join(f'<a class="btn btn-outline" href="{h}" target="_blank" rel="noopener">{e(l)}</a>' for l, h in [
        (t[f'rv_airbnb_{key}'], u['airbnb'] + '#reviews'),
        (t[f'rv_booking_{key}'], u['booking'] + '#tab-reviews'),
        (t['rv_google'], SITE['google_reviews'])])

    body = f'''<main id="main">
<section class="wrap unit-head">
  <p class="kicker dark-kicker">{e(t['hero_kicker'])}</p>
  <h1>{e(tu['h1'])}</h1>
  <p class="meta">{' · '.join(e(m) for m in meta)} · {e(SITE['city'])} · ★ {e(t['badge'])}</p>
  {B.book_buttons(lang, key)}
</section>
<section class="wrap unit-gallery" data-gallery aria-label="{e(t['gallery_label'])}">{gallery}</section>
<section class="section wrap two-col">
  <div><p class="lead dark">{e(tu['intro'])}</p></div>
  <div><h2>{e(t['features_h2'])}</h2>{B.li(tu['features'])}</div>
</section>
<section class="section band" id="dispo">
  <div class="wrap">
    <h2>{e(t['avail_h2'])}</h2>
    <p class="small">{e(t['avail_note'])}</p>
    <div class="calendar" data-calendar="{u['calendar']}" data-locale="{lang}" data-error="{e(t['avail_err'])}"></div>
    {B.book_buttons(lang, key)}
  </div>
</section>
<section class="section wrap split" id="cadre">
  <div>
    <h2>{e(t['setting_h2'])}</h2>
    <p>{e(t['setting_p'])}</p>
    {B.li(t['setting_list'])}
  </div>
  <div class="gallery gallery-3" data-gallery>{setting}</div>
</section>
<section class="section band">
  <div class="wrap two-col">
    <div><h2>{e(t['road_h2'])}</h2><p>{e(t['road_p'])}</p>{B.li(t['road_list'])}</div>
    <div><h2>{e(t['pro_h2'])}</h2><p>{e(t['pro_p'])}</p></div>
  </div>
</section>
<section class="section wrap" id="avis">
  <h2>{e(t['reviews_h2'])}</h2>
  <p>{e(x['reviews_unit'])}</p>
  <div class="actions wrap-actions">{reviews}</div>
</section>
<section class="section band" id="acces">
  <div class="wrap split">
    <div>
      <h2>{e(t['access_h2'])}</h2>
      <address>{e(SITE['street'])}<br>{SITE['postal']} {e(SITE['city'])}, France</address>
      {B.li(t['access_list'])}
      <a class="btn btn-outline" href="{SITE['maps_link']}" target="_blank" rel="noopener">{e(t['open_maps'])}</a>
    </div>
    <div class="map"><iframe title="{e(t['access_h2'])} — {e(SITE['city'])}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="{SITE['maps_embed']}"></iframe></div>
  </div>
</section>
<section class="section wrap">
  <h2>{e(x['sister'])} : {e(ot['name'])}</h2>
  <article class="card card-row">
    <a href="{url(UNIT_SITES[other]['url'], lang)}" class="card-img">{B.picture(ou['cover'], ot['alts'][0], '(max-width: 700px) 100vw, 400px')}</a>
    <div class="card-body">
      <p>{e(ot['short'])}</p>
      <a class="btn btn-primary" href="{url(UNIT_SITES[other]['url'], lang)}">{e(x['sister_btn'].format(n=ot['name']))} →</a>
    </div>
  </article>
</section>
{B.faq_html(lang)}
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
    acc = B.unit_ld(lang, key)
    acc['@id'] = url(base, lang) + '#accommodation'
    acc['url'] = url(base, lang)
    acc['image'] = [f"{base}/img/{ph}-{big(ph)}.webp" for ph in photos]
    acc['containedInPlace'] = {"@id": base + '/#business'}
    biz = {
        "@context": "https://schema.org", "@type": "LodgingBusiness", "@id": base + '/#business',
        "name": UNIT_SITES[key]['name'], "alternateName": SITE['name'], "description": tu['desc'],
        "url": url(base, lang), "telephone": SITE['phone'], "email": SITE['email'],
        "image": acc['image'][:1], "address": B.address_ld(), "hasMap": SITE['maps_link'],
        "sameAs": [u['airbnb'], u['booking']], "availableLanguage": LANGS,
    }
    return head(key, lang, [biz, acc]) + header(key, lang) + body + footer(key, lang)


def main(key, out):
    base = UNIT_SITES[key]['url']
    os.makedirs(os.path.join(out, 'img'), exist_ok=True)
    for lang in LANGS:
        f = os.path.join(out, 'index.html') if lang == 'fr' else os.path.join(out, lang, 'index.html')
        B.write(f, page(key, lang))
    # images utilisées seulement
    other = 'studio' if key == 'tiny' else 'tiny'
    needed = set(UNITS[key]['photos']) | set(SETTING_PHOTOS) | {UNITS[other]['cover']}
    for n in needed:
        for w in B.IMG[n]:
            shutil.copy(os.path.join(ROOT, 'img', f'{n}-{w}.webp'), os.path.join(out, 'img'))
    for f in ('styles.css', 'site.js', 'favicon.ico', 'favicon-16x16.png', 'favicon-32x32.png', 'apple-touch-icon.png'):
        shutil.copy(os.path.join(ROOT, f), out)
    today = datetime.date.today().isoformat()
    alts = lambda: ''.join(f'\n    <xhtml:link rel="alternate" hreflang="{l}" href="{url(base, l)}"/>' for l in LANGS) + \
        f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{url(base, "fr")}"/>'
    B.write(os.path.join(out, 'sitemap.xml'),
            '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
            + '\n'.join(f'  <url>\n    <loc>{url(base, l)}</loc>\n    <lastmod>{today}</lastmod>{alts()}\n  </url>' for l in LANGS)
            + '\n</urlset>\n')
    B.write(os.path.join(out, 'robots.txt'), f'User-agent: *\nAllow: /\n\nSitemap: {base}/sitemap.xml\n')
    B.write(os.path.join(out, 'vercel.json'), json.dumps({
        "cleanUrls": True, "trailingSlash": False,
        "headers": [{"source": "/img/(.*)", "headers": [{"key": "Cache-Control", "value": "public, max-age=31536000, immutable"}]}]
    }, indent=2) + '\n')
    print('OK', key, '->', out, '(', base, ')')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
