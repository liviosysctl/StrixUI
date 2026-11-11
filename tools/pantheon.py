#!/usr/bin/env python3
"""The pantheon of the default theme: eight Roman gods, each a wallpaper and an aspect.

An aspect is a small set of colour tokens that follows the god: a tinted background and its
surfaces, the accent and everything derived from it, and the terminal cursor and selection.
Text, line, the status colours and syntax stay as they are in every aspect.

    python3 tools/pantheon.py          # print every aspect and check its contrast

The accent of each god is picked by hand; the rest is derived in OKLCH so that every aspect has
the same lightness steps as Saturnus, the default.
"""
import math

# name, Latin name, accent fill, short note on the colour.
# Dark academia: every accent is muted (OKLCH chroma 0.05 to 0.10, against 0.2 for a pure colour) and
# leans warm, like leather, brass, ink and old bindings. Only Saturnus, the default, keeps the full Strix red.
def _acc(L, C, H):
    return oklch(L, C, H)

GODS_SPEC = [
    ('saturnus',  'Saturnus',  '#c8102e',               'Strix red. Saturn, lord of time and of the night hours; the default.'),
    ('janus',     'Janus',     (0.59, 0.048, 168),      'Patina, the green of old bronze doors and keys.'),
    ('apollo',    'Apollo',    (0.68, 0.085, 78),       'Antique gold, worn brass.'),
    ('mars',      'Mars',      (0.57, 0.105, 45),       'Rust, iron and burnt sienna.'),
    ('minerva',   'Minerva',   (0.60, 0.065, 112),      'Olive leaf, moss on stone.'),
    ('mercurius', 'Mercurius', (0.57, 0.048, 248),      'Slate and ink blue.'),
    ('pluto',     'Pluto',     (0.55, 0.060, 305),      'Heather, faded plum.'),
    ('bacchus',   'Bacchus',   (0.52, 0.085, 10),      'Claret, old wine.'),
]
DEFAULT = 'saturnus'

# The default's tokens, used as the reference for lightness; the hand-made values stay exact for Saturnus
BASE = {
    'background': '#0b0a09', 'surface': '#131211', 'surface-raised': '#1b1917', 'surface-sunken': '#070606',
    'border': '#2f2c28', 'accent': '#c8102e', 'accent-hover': '#dc1f3d', 'accent-pressed': '#a50d26',
    'accent-soft': '#2a0c12', 'accent-text': '#f2556a', 'on-accent': '#ffffff', 'focus': '#e8324a',
    'cursor': '#c8102e', 'selection': '#3a1219',
}
TEXT, MUTED, FAINT, BSTRONG = '#ece6da', '#a09a8f', '#77726a', '#6e6a63'
ASPECT_TOKENS = list(BASE)


# ---------------------------------------------------------------- colour maths
def _lin(c):
    c /= 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

def _gam(c):
    c = max(0.0, min(1.0, c))
    return 255 * (12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055)

def hex2rgb(h):
    h = h.lstrip('#'); return [int(h[i:i + 2], 16) for i in (0, 2, 4)]

def rgb2hex(rgb):
    return '#%02x%02x%02x' % tuple(int(round(max(0, min(255, v)))) for v in rgb)

def to_oklch(h):
    r, g, b = [_lin(v) for v in hex2rgb(h)]
    l = (0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b) ** (1 / 3)
    m = (0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b) ** (1 / 3)
    s = (0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b) ** (1 / 3)
    L = 0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s
    a = 1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s
    bb = 0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s
    return L, math.hypot(a, bb), math.degrees(math.atan2(bb, a)) % 360

def _oklch_rgb(L, C, H):
    a, b = C * math.cos(math.radians(H)), C * math.sin(math.radians(H))
    l = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3
    m = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3
    s = (L - 0.0894841775 * a - 1.2914855480 * b) ** 3
    return (4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
            -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
            -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s)

def oklch(L, C, H):
    """OKLCH to hex; chroma is reduced until the colour fits sRGB."""
    while C > 0:
        rgb = _oklch_rgb(L, C, H)
        if all(-1e-4 <= v <= 1 + 1e-4 for v in rgb):
            break
        C -= 0.002
    return rgb2hex([_gam(v) for v in _oklch_rgb(L, max(C, 0), H)])

def luminance(h):
    r, g, b = [_lin(v) for v in hex2rgb(h)]
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def contrast(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


GODS = [(n, l, a if isinstance(a, str) else oklch(*a), d) for n, l, a, d in GODS_SPEC]

# ---------------------------------------------------------------- aspects
def _lighten_to(fg, bg, minimum, H, C, L):
    """Raise L until fg reaches the contrast minimum on bg."""
    c = oklch(L, C, H)
    while contrast(c, bg) < minimum and L < 0.97:
        L += 0.01; c = oklch(L, C, H)
    return c

def aspect(name):
    acc = dict((g[0], g[2]) for g in GODS)[name]
    if name == DEFAULT:
        return dict(BASE)
    La, Ca, Ha = to_oklch(acc)
    t = {}
    # grounds: the default's lightness, a faint tint of the god's hue
    for k, c in (('background', 0.010), ('surface', 0.011), ('surface-raised', 0.012), ('surface-sunken', 0.008), ('border', 0.016)):
        Lb = to_oklch(BASE[k])[0]
        t[k] = oklch(Lb, c, Ha)
    # fills and the label on them: white where it reads, else the darkest ground; the fills move in
    # lightness (never in hue) until the label reaches 4.5:1 on all three
    white, dark = '#ffffff', t['surface-sunken']
    def fills(L):
        return oklch(L, Ca, Ha), oklch(L + 0.04, Ca, Ha), oklch(L - 0.05, Ca, Ha)
    def worst(label, L):
        return min(contrast(label, f) for f in fills(L))
    label = white if worst(white, La) >= worst(dark, La) else dark
    step = -0.005 if label == white else 0.005
    while worst(label, La) < 4.5:
        La += step
    t['accent'], t['accent-hover'], t['accent-pressed'] = fills(La)
    t['on-accent'] = label
    t['accent-soft'] = oklch(0.22, min(Ca * 0.35, 0.06), Ha)
    t['selection'] = oklch(0.27, min(Ca * 0.4, 0.07), Ha)
    lightest = max(t['surface-raised'], t['accent-soft'], t['background'], key=luminance)
    t['accent-text'] = _lighten_to(None, lightest, 5.0, Ha, min(Ca, 0.16), max(La, 0.70))
    t['focus'] = _lighten_to(None, t['surface-raised'], 4.0, Ha, Ca, La + 0.06)
    t['cursor'] = t['accent']
    return t

def checks(name, t):
    S = ['background', 'surface', 'surface-raised']
    rows = []
    def chk(fg, fgc, bgs, minimum):
        for b in bgs:
            r = contrast(fgc, t[b]); rows.append((name, fg, b, r, minimum))
    chk('text', TEXT, S, 4.5); chk('text-muted', MUTED, S, 4.5); chk('text-faint', FAINT, S, 3); chk('border-strong', BSTRONG, S, 3)
    chk('accent-text', t['accent-text'], S + ['accent-soft'], 4.5)
    chk('focus', t['focus'], S, 3)
    chk('accent', t['accent'], ['background', 'surface'], 3)
    for k in ('accent', 'accent-hover', 'accent-pressed'):
        rows.append((name, 'on-accent', k, contrast(t['on-accent'], t[k]), 4.5))
    rows.append((name, 'term text', 'selection', contrast('#e6e0d4', t['selection']), 4.5))
    rows.append((name, 'cursor', 'background', contrast(t['cursor'], t['background']), 3))
    return rows

def all_aspects():
    return {g[0]: aspect(g[0]) for g in GODS}

if __name__ == '__main__':
    fails = 0
    for g in GODS:
        t = aspect(g[0])
        print('%-10s ' % g[0] + ' '.join('%s=%s' % (k.replace('accent-', 'a-').replace('surface', 's'), v) for k, v in t.items()))
        for row in checks(g[0], t):
            if row[3] < row[4]:
                fails += 1; print('   FAIL %-14s on %-14s %.2f (min %s)' % row[1:])
        lo = min(checks(g[0], t), key=lambda r: r[3] / r[4])
        print('   lowest margin: %s on %s %.2f (min %s)' % (lo[1], lo[2], lo[3], lo[4]))
    print('FAILS', fails)
