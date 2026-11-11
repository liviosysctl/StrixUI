#!/usr/bin/env python3
"""Builds a theme repository: themes that are not among the eight gods, with the same colours rules and the
same wallpaper treatment.

    python3 tools/pack.py ../strix-theme-lucifer         every theme in its source.toml
    python3 tools/pack.py ../strix-theme-lucifer --check  only check what is there

A theme repository (layout 1, see the README of strix-theme-template) holds strix-themes.toml and
themes/<id>/ with theme.toml (theme engine format 1), wallpaper.jpg and wallpaper.toml. Its source.toml
is the recipe this tool reads:

    [[theme]]
    id = "lucifer"
    name = "Lucifer"
    description = "One line about the colour."
    accent = [0.55, 0.10, 32]            # OKLCH lightness, chroma, hue; or "#rrggbb"
    accent2 = [0.74, 0.10, 85]           # optional second colour: lines and letters (accent-text, focus) and discs2
    [theme.plate]
    source = "rijks:Tgakd:3200"          # rijks:<Micrio id>:<width>, aic:<IIIF id>, or file:<path in the repository>
    crop = [0.05, 0.42, 0.95]            # x0, y0, x1 of the scan; the height follows from 16:9
    # or, for a scene taller than 16:9, set it whole on a ground of ink instead of crop:
    # fit = [0.04, 0.03, 0.95, 0.86]     # x0, y0, x1, y1 of the scan
    # place = [1500, 0.96]               # centre x on the 2560 by 1440 picture, height as a share of 1440
    disc = [1330, 520, 260]              # centre and radius of the accent disc on the 2560 by 1440 picture
    discs2 = [[900, 300, 120]]           # optional, with accent2: discs in the second colour
    caption = "What it shows and who made it."
    credit = "Maker, title, date. Collection, number, licence"
    licence = "public domain"            # public domain or CC0 only

Needs Pillow and numpy, like tools/wallpapers.py.
"""
import argparse, json, os, re, sys, tomllib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import themes, targets
from themes import TEXT, MUTED, FAINT, BSTRONG, contrast

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKENS = os.path.join(ROOT, 'design-system', 'tokens.json')
LICENCES = ('public domain', 'CC0')


def colours(accent):
    acc = accent if isinstance(accent, str) else themes.oklch(*accent)
    return themes.derive_all(acc)


def table(spec, t):
    """Every colour token of the design system for this theme: the derived ones, the rest as in the default theme.
    With accent2, a dual-colour theme: accent fills everything that is filled (buttons, progress, the first disc),
    the second colour takes everything that is a line or a letter (accent-text, focus) and the second disc."""
    derived = colours(spec['accent'])
    if 'accent2' in spec:
        second = colours(spec['accent2'])
        derived['accent-text'] = themes._lighten_to(None, max(derived['surface-raised'], derived['accent-soft'], key=themes.luminance), 5.0,
                                                    *(lambda L, C, H: (H, min(C, 0.16), max(L, 0.70)))(*themes.to_oklch(second['accent'])))
        derived['focus'] = themes._lighten_to(None, derived['surface-raised'], 4.0,
                                              *(lambda L, C, H: (H, C, L + 0.06))(*themes.to_oklch(second['accent'])))
        derived['accent-2'] = second['accent']
    one = targets.theme_table(t, [{'id': 'saturnus'}])['saturnus']
    cols = dict(one['colors'])
    term = dict(one['terminal'])
    for k, v in derived.items():
        if k in ('cursor', 'selection'):
            term[k] = v
        elif k in cols or k == 'accent-2':
            cols[k] = v
    term['background'] = cols['background']
    return {'colors': cols, 'terminal': term}


def checks(spec, tab):
    c, tm = tab['colors'], tab['terminal']
    fails = []
    def need(what, a, b, minimum):
        r = contrast(a, b)
        if r < minimum:
            fails.append('%s: %s %.2f < %s' % (spec['id'], what, r, minimum))
    for g in ('background', 'surface', 'surface-raised'):
        need('text on ' + g, c['text'], c[g], 4.5)
        need('text-muted on ' + g, c['text-muted'], c[g], 4.5)
        need('accent-text on ' + g, c['accent-text'], c[g], 4.5)
        need('error on ' + g, c['error'], c[g], 4.5)
        need('focus on ' + g, c['focus'], c[g], 3)
        need('border-strong on ' + g, c['border-strong'], c[g], 3)
    for k in ('accent', 'accent-hover', 'accent-pressed'):
        need('on-accent on ' + k, c['on-accent'], c[k], 4.5)
    need('terminal foreground', tm['foreground'], tm['background'], 4.5)
    return fails


def theme_toml(spec, tab):
    c, tm = tab['colors'], tab['terminal']
    o = ['# %s. %s' % (spec['name'], spec['description']),
         '# Made with tools/pack.py of StrixUI from source.toml. Change source.toml and build again.',
         'format = 1', 'name = "%s"' % spec['name'], 'description = %s' % json.dumps(spec['description']), 'default-variant = "dark"', '',
         '[variants.dark]', 'name = "Dark"', 'appearance = "dark"', '', '[variants.dark.colors]']
    o += ['%s = "%s"' % (n, c[n]) for n in targets.REQUIRED]
    o.append('# every other token of the design system, under its own name')
    o += ['%s = "%s"' % (n, v) for n, v in c.items() if n not in targets.REQUIRED]
    o += ['', '[variants.dark.terminal]'] + ['%s = "%s"' % (n, tm[n]) for n in targets.TERMINAL]
    return '\n'.join(o) + '\n'


def wallpaper_toml(plate):
    return 'caption = %s\ncredit = %s\nlicence = %s\n' % (json.dumps(plate['caption']), json.dumps(plate['credit']), json.dumps(plate['licence']))


def source_path(repo, src):
    kind, _, rest = src.partition(':')
    if kind == 'file':
        return os.path.join(repo, rest)
    import wallpapers
    if kind == 'aic':
        return wallpapers.fetch(('aic', rest))
    if kind == 'rijks':
        mid, _, width = rest.partition(':')
        return wallpapers.fetch(('rijks', mid, int(width or 3000)))
    raise SystemExit('unknown plate source: ' + src)


def fitted(scan, fit, place):
    """A whole scene that is taller than 16:9: the part `fit` (x0, y0, x1, y1 of the scan) is set whole on a
    2560 by 1440 ground of ink, `place` = [centre x, height as a share of 1440], its edges fading into the ink."""
    from PIL import Image, ImageFilter
    import numpy as np
    im = Image.open(scan).convert('L'); w, h = im.size
    part = im.crop((int(fit[0] * w), int(fit[1] * h), int(fit[2] * w), int(fit[3] * h)))
    ph = int(1440 * place[1]); pw = int(part.width * ph / part.height)
    part = part.resize((pw, ph), Image.LANCZOS)
    ground = Image.new('L', (2560, 1440), 0)
    x, y = int(place[0] - pw / 2), (1440 - ph) // 2
    # fade the edges of the picture into the ink over 120 px
    yy, xx = np.mgrid[0:ph, 0:pw]
    edge = np.minimum(np.minimum(xx, pw - 1 - xx), np.minimum(yy, ph - 1 - yy))
    mask = np.clip(edge / 120, 0, 1) ** 1.5
    faded = Image.fromarray((np.asarray(part, float) * mask).astype('uint8'))
    ground.paste(faded, (x, y))
    out = os.path.join(ROOT, 'build', 'engravings', 'fitted-%s.png' % os.path.basename(scan).rsplit('.', 1)[0])
    ground.save(out)
    return out


def build(repo, only_check=False):
    src = tomllib.load(open(os.path.join(repo, 'source.toml'), 'rb'))
    t = json.load(open(TOKENS, encoding='utf-8'))
    fails = []
    for spec in src.get('theme', []):
        if not re.fullmatch(r'[a-z][a-z0-9]*(-[a-z0-9]+)*', spec['id']) or len(spec['id']) > 32:
            fails.append('%s: the id must be lowercase letters, digits and single hyphens' % spec['id'])
        plate = spec['plate']
        if plate.get('licence') not in LICENCES:
            fails.append('%s: the picture must be public domain or CC0' % spec['id'])
        tab = table(spec, t)
        fails += checks(spec, tab)
        d = os.path.join(repo, 'themes', spec['id'])
        if only_check:
            continue
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, 'theme.toml'), 'w').write(theme_toml(spec, tab))
        open(os.path.join(d, 'wallpaper.toml'), 'w').write(wallpaper_toml(plate))
        import wallpapers
        scan = source_path(repo, plate['source'])
        more = [tuple(x) + (tab['colors']['accent-2'],) for x in plate.get('discs2', [])] if 'accent-2' in tab['colors'] else []
        if 'fit' in plate:
            scan = fitted(scan, plate['fit'], plate.get('place', [1280, 0.96]))
        wallpapers.make(scan, tuple(plate.get('crop', (0, 0, 1))), tuple(plate['disc']), os.path.join(d, 'wallpaper.jpg'),
                        bg=tab['colors']['background'], accent=tab['colors']['accent'], more=more, **{k: plate[k] for k in ('paper', 'vig') if k in plate})
        print('%s  accent %s on %s' % (spec['id'], tab['colors']['accent'], tab['colors']['background']))
    for f in fails:
        print('FAIL ' + f)
    print('FAILS %d' % len(fails))
    return not fails


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('repo')
    ap.add_argument('--check', action='store_true')
    a = ap.parse_args()
    sys.exit(0 if build(os.path.abspath(a.repo), a.check) else 1)
