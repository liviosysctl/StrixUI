#!/usr/bin/env python3
"""Makes the engraving wallpapers in src/wallpapers/.

One plate per god of the pantheon (tools/pantheon.py). Each is downloaded from an open-access
collection (Art Institute of Chicago, CC0, or Rijksmuseum, public domain), cropped to the upper
body at 16:9, and printed in two inks of the god's aspect: paper becomes the cream `line` colour,
ink becomes the aspect's `background`, and ink inside one disc becomes its `accent`. The picture is darkened toward
the edges, hardest along the top (bar) and the bottom (dock), and gets a little grain.

    python3 tools/wallpapers.py            # all plates
    python3 tools/wallpapers.py janus      # one plate

Needs: Pillow, numpy.
"""
import io, math, os, sys, urllib.request
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pantheon

OUT = os.path.join(ROOT, 'src', 'wallpapers')
CACHE = os.path.join(ROOT, 'build', 'engravings')
W, H = 2560, 1440
CREAM = np.array([0xd8, 0xd0, 0xc0], float)

# god: (source, crop as x0, y0, x1 of the scan (y1 follows from 16:9), disc centre x, y and radius in px, credit[, options for make()])
# source is ('aic', IIIF image id) or ('rijks', Micrio id, width to fetch)
PLATES = {
    'saturnus': (('aic', '2e6b4b94-95de-045f-2826-7f76c23b6a17'), (0.15, 0.15, 0.85), (1320, 610, 250),
                 'Hendrick Goltzius after Polidoro da Caravaggio, Saturnus, from Eight Pagan Gods, 1592. Art Institute of Chicago 2023.968, CC0'),
    'janus': (('rijks', 'jGPOs', 6098), (0.36, 0.23, 0.74), (1110, 450, 300),
              'Janus opens the door of the year, engraved by Robert van Audenaerd after Carlo Maratta, 1685 to 1723. Rijksmuseum RP-P-OB-67.432, public domain'),
    'apollo': (('aic', '3e8aab9a-660c-7742-733d-5a36fc648418'), (0.10, 0.08, 0.90), (1360, 346, 280),
               'Hendrick Goltzius, Apollo, 1588. Art Institute of Chicago 2012.409, CC0'),
    'mars': (('rijks', 'yzhwS', 3064), (0.22, 0.17, 0.84), (1060, 560, 260),
             'Hubert Quellinus after Artus Quellinus, Mars in the west gallery of the Amsterdam town hall, 1655. Rijksmuseum RP-P-AO-22-1Q-1, public domain'),
    'minerva': (('aic', '27c735cb-2d28-bf3f-d67b-3bea6278957c'), (0.0, 0.10, 1.0), (1580, 700, 300),
                'Jan Saenredam after Hendrick Goltzius, Pallas Athena, from Three Goddesses, about 1595. Art Institute of Chicago 2023.161, CC0'),
    'mercurius': (('aic', '907c2a05-541d-ddee-7d23-75ee68dfe50e'), (0.15, 0.15, 0.85), (1318, 447, 260),
                  'Hendrick Goltzius after Polidoro da Caravaggio, Mercurius, from Eight Pagan Gods, 1592. Art Institute of Chicago 2023.975, CC0'),
    'pluto': (('aic', '875c8e28-faf6-4991-b34a-e9e991476d81'), (0.15, 0.15, 0.85), (1335, 475, 260),
              'Hendrick Goltzius after Polidoro da Caravaggio, Pluto, from Eight Pagan Gods, 1592. Art Institute of Chicago 2023.970, CC0'),
    'bacchus': (('aic', 'b87ec199-aa10-e7a7-2301-74c18b845d5d'), (0.15, 0.15, 0.85), (1330, 490, 260),
                'Hendrick Goltzius after Polidoro da Caravaggio, Bacchus, from Eight Pagan Gods, 1592. Art Institute of Chicago 2023.974, CC0'),
}

def fetch(source):
    os.makedirs(CACHE, exist_ok=True)
    if source[0] == 'aic':
        path = os.path.join(CACHE, source[1] + '.jpg')
        url = 'https://www.artic.edu/iiif/2/%s/full/3000,/0/default.jpg' % source[1]
    else:
        path = os.path.join(CACHE, 'rijks-%s.jpg' % source[1])
        url = 'https://iiif.micr.io/%s/full/%d,/0/default.jpg' % (source[1], source[2])
    if not os.path.exists(path):
        req = urllib.request.Request(url, headers={'User-Agent': 'strixui-wallpapers'})
        open(path, 'wb').write(urllib.request.urlopen(req, timeout=300).read())
    return path

def rgb(h):
    return np.array(pantheon.hex2rgb(h), float)

def make(src, box, disc, out, bg='#0b0a09', accent='#c8102e', paper=0.46, vig=0.92, seed=3):
    BG, ACC = rgb(bg), rgb(accent)
    im = Image.open(src).convert('L'); w, h = im.size
    x0, y0, x1 = box
    cw = (x1 - x0) * w; ch = cw * H / W
    crop = im.crop((int(x0 * w), int(y0 * h), int(x1 * w), int(y0 * h + ch))).resize((W, H), Image.LANCZOS)
    crop = crop.filter(ImageFilter.UnsharpMask(radius=2, percent=60))
    g = np.asarray(crop, float)
    lo, hi = np.percentile(g, 3), np.percentile(g, 97)
    l = np.clip((g - lo) / (hi - lo), 0, 1) ** 1.7            # 0 ink, 1 paper
    yy, xx = np.mgrid[0:H, 0:W]
    cx, cy, r = disc
    d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    m = np.clip((r - d) / 1.5 + 0.5, 0, 1)[..., None]       # antialiased disc mask
    # outside the disc: dark ink on dim cream paper. Inside: the paper takes the accent and the ink
    # stays dark, so light accents (gold, olive) keep the engraving readable as well as red does
    ink = BG
    # the disc is printed like ink on old paper: the accent, a little dulled by the cream under it
    pap = CREAM * paper * (1 - m) + (ACC * 0.90 + CREAM * paper * 0.12) * m
    img = ink * (1 - l[..., None]) + pap * l[..., None]
    dv = np.sqrt(((xx - cx) / (W * 0.62)) ** 2 + ((yy - cy) / (H * 0.78)) ** 2)
    v = 1 - vig * np.clip((dv - 0.25) / 0.75, 0, 1) ** 1.4
    top = np.clip(yy / 110, 0.35, 1); bot = np.clip((H - yy) / 90, 0.45, 1)
    f = np.maximum(v * top * bot, m[..., 0] * 0.9)
    img = BG + (img - BG) * f[..., None]
    img += np.random.default_rng(seed).normal(0, 3.2, (H, W, 1))
    img = Image.fromarray(np.clip(img, 0, 255).astype('uint8'))
    # hair lines around the disc: two circles, a graduated ring, a meridian
    S = 2; ov = Image.new('RGBA', (W * S, H * S), (0, 0, 0, 0)); dr = ImageDraw.Draw(ov); c = (0xd8, 0xd0, 0xc0)
    for rr, a in ((r + 56, 120), (r + 64, 70), (r + 260, 60)):
        dr.ellipse(((cx - rr) * S, (cy - rr) * S, (cx + rr) * S, (cy + rr) * S), outline=c + (a,), width=2)
    for i in range(0, 360, 3):
        a = math.radians(i); r1 = r + 64; r2 = r + 64 + (18 if i % 15 == 0 else 9)
        dr.line(((cx + r1 * math.cos(a)) * S, (cy + r1 * math.sin(a)) * S, (cx + r2 * math.cos(a)) * S, (cy + r2 * math.sin(a)) * S), fill=c + (70,), width=2)
    dr.line((cx * S, 0, cx * S, H * S), fill=c + (40,), width=2)
    ov = ov.resize((W, H), Image.LANCZOS)
    img = Image.alpha_composite(img.convert('RGBA'), ov).convert('RGB')
    img.save(out, quality=84, optimize=True, progressive=True)

def main():
    names = sys.argv[1:] or list(PLATES)
    os.makedirs(OUT, exist_ok=True)
    for n in names:
        source, box, disc, credit = PLATES[n][:4]
        extra = PLATES[n][4] if len(PLATES[n]) > 4 else {}    # per plate: paper brightness for a print with much bare paper
        t = pantheon.aspect(n)
        out = os.path.join(OUT, n + '.jpg')
        make(fetch(source), box, disc, out, bg=t['background'], accent=t['accent'], **extra)
        print('%s  %d bytes  (%s)' % (n + '.jpg', os.path.getsize(out), credit))

if __name__ == '__main__':
    main()
