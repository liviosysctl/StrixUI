#!/usr/bin/env python3
"""Makes the engraving wallpapers in src/wallpapers/.

Each plate is downloaded from the open-access collection of the Art Institute of Chicago (CC0),
cropped to the upper body at 16:9, and printed in two inks: paper becomes the cream `line` colour,
ink becomes `background`, and ink inside one disc becomes `accent`. The picture is darkened toward
the edges, hardest along the top (bar) and the bottom (dock), and gets a little grain.

    python3 tools/wallpapers.py            # all plates
    python3 tools/wallpapers.py laocoon    # one plate

Needs: Pillow, numpy.
"""
import io, math, os, sys, urllib.request
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'src', 'wallpapers')
CACHE = os.path.join(ROOT, 'build', 'engravings')
W, H = 2560, 1440
BG = np.array([0x0b, 0x0a, 0x09], float)
CREAM = np.array([0xd8, 0xd0, 0xc0], float)
RED = np.array([0xc8, 0x10, 0x2e], float)

# file: (IIIF image id, crop box as fractions of the scan, disc centre x, y and radius in px, credit)
PLATES = {
    'apollo-belvedere.jpg': ('fed2add8-1ef4-aee4-b063-09fb4363b207', (0.12, 0.08, 0.88, 0.40), (1010, 430, 330),
                             'Hendrick Goltzius, The Apollo Belvedere, about 1592. Art Institute of Chicago 1990.498, CC0'),
    'laocoon.jpg': ('8dd87c71-89f2-e7fa-a69d-e327ae3c4845', (0.05, 0.12, 0.95, 0.485), (1290, 560, 330),
                    'Nicolas Beatrizet, Laocoon, 1540 to 1565. Art Institute of Chicago 1920.1991, CC0'),
    'hercules.jpg': ('56edfa21-bb17-cdc9-d988-9319d4be92aa', (0.105, 0.05, 0.925, 0.415), (700, 360, 300),
                     'Hendrick Goltzius, Hercules and Telephos, about 1592. Art Institute of Chicago 1990.499, CC0'),
}

def fetch(image_id):
    os.makedirs(CACHE, exist_ok=True)
    path = os.path.join(CACHE, image_id + '.jpg')
    if not os.path.exists(path):
        url = 'https://www.artic.edu/iiif/2/%s/full/3000,/0/default.jpg' % image_id
        req = urllib.request.Request(url, headers={'User-Agent': 'strixui-wallpapers'})
        data = urllib.request.urlopen(req, timeout=180).read()
        open(path, 'wb').write(data)
    return path

def make(src, box, disc, out, paper=0.46, vig=0.92, seed=3):
    im = Image.open(src).convert('L'); w, h = im.size
    x0, y0, x1, y1 = box
    crop = im.crop((int(x0 * w), int(y0 * h), int(x1 * w), int(y1 * h))).resize((W, H), Image.LANCZOS)
    crop = crop.filter(ImageFilter.UnsharpMask(radius=2, percent=60))
    g = np.asarray(crop, float)
    lo, hi = np.percentile(g, 3), np.percentile(g, 97)
    l = np.clip((g - lo) / (hi - lo), 0, 1) ** 1.7            # 0 ink, 1 paper
    yy, xx = np.mgrid[0:H, 0:W]
    cx, cy, r = disc
    d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    m = np.clip((r - d) / 1.5 + 0.5, 0, 1)[..., None]       # antialiased disc mask
    ink = BG * (1 - m) + RED * 0.92 * m
    rgb = ink * (1 - l[..., None]) + CREAM * paper * l[..., None]
    dv = np.sqrt(((xx - cx) / (W * 0.62)) ** 2 + ((yy - cy) / (H * 0.78)) ** 2)
    v = 1 - vig * np.clip((dv - 0.25) / 0.75, 0, 1) ** 1.4
    top = np.clip(yy / 110, 0.35, 1); bot = np.clip((H - yy) / 90, 0.45, 1)
    f = np.maximum(v * top * bot, m[..., 0] * 0.9)
    rgb = BG + (rgb - BG) * f[..., None]
    rgb += np.random.default_rng(seed).normal(0, 3.2, (H, W, 1))
    img = Image.fromarray(np.clip(rgb, 0, 255).astype('uint8'))
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
        fn = n if n.endswith('.jpg') else n + '.jpg'
        image_id, box, disc, credit = PLATES[fn]
        make(fetch(image_id), box, disc, os.path.join(OUT, fn))
        print('%s  %d bytes  (%s)' % (fn, os.path.getsize(os.path.join(OUT, fn)), credit))

if __name__ == '__main__':
    main()
