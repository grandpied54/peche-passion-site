# La Maison du Pêcheur — site web

Site statique (FR / EN / DE / NL) déployé sur Vercel.

## Modifier le site
1. Modifier les textes dans `tools/content.py` (ou l'adresse du site : `SITE["url"]`).
2. Lancer `python3 tools/build.py` : régénère toutes les pages HTML, `sitemap.xml` et `robots.txt`.
3. Commit + push : Vercel redéploie automatiquement.

## Ajouter / changer des photos
Mettre les originaux dans `assets/`, déclarer le nom dans `tools/images.py`, puis
`pip install pillow && python3 tools/images.py && python3 tools/build.py`.

Ne pas modifier les fichiers `.html` à la main : ils sont écrasés à chaque build.
