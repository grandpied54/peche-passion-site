# -*- coding: utf-8 -*-
"""Convertit les photos originales (assets/*.jpg) en WebP optimisés dans img/.
Usage : python3 tools/images.py   (nécessite Pillow : pip install pillow)"""
import json, os
from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAMES = {
    'hero-1': 'vue-aerienne-maison-pulligny', 'hero-10': 'arc-en-ciel-campagne-pulligny',
    'hero-3': 'cygnes-riviere-madon', 'hero-2': 'cygnes-jardin-bord-riviere',
    'hero-4': 'jardin-terrasse-riviere', 'hero-5': 'chene-jardin-riviere',
    'hero-6': 'jardin-sous-la-neige', 'hero-7': 'chardonneret-mangeoire',
    'hero-8': 'coin-detente-jardin', 'hero-9': 'poste-de-peche-riviere',
    'tiny-1': 'tiny-house-chalet-bois', 'tiny-2': 'tiny-house-exterieur-jardin',
    'tiny-3': 'tiny-house-lit-double', 'tiny-4': 'tiny-house-cuisine',
    'tiny-5': 'tiny-house-douche', 'tiny-6': 'tiny-house-tv',
    'studio-1': 'studio-perche-maison-escalier', 'studio-2': 'studio-perche-terrasse-vue-riviere',
    'studio-3': 'studio-perche-sejour', 'studio-4': 'studio-perche-cuisine',
    'studio-5': 'studio-perche-douche', 'studio-6': 'studio-perche-chambre',
}

def main():
    os.makedirs(os.path.join(ROOT, 'img'), exist_ok=True)
    man = {}
    for src, name in NAMES.items():
        im = ImageOps.exif_transpose(Image.open(os.path.join(ROOT, 'assets', src + '.jpg'))).convert('RGB')
        man[name] = {}
        for w in (640, 1280):
            if w == 1280 and max(im.size) <= 640:
                continue
            c = im.copy(); c.thumbnail((w, w))
            c.save(os.path.join(ROOT, 'img', f'{name}-{w}.webp'), 'WEBP', quality=78, method=6)
            man[name][str(w)] = list(c.size)
    og = ImageOps.exif_transpose(Image.open(os.path.join(ROOT, 'assets', 'hero-1.jpg'))).convert('RGB')
    og.thumbnail((1200, 1200)); og.save(os.path.join(ROOT, 'img', 'og-image.jpg'), quality=82)
    json.dump(man, open(os.path.join(ROOT, 'tools', 'images.json'), 'w'), indent=1)
    print('OK', len(man), 'photos')

if __name__ == '__main__':
    main()
