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
    [theme.plate]
    source = "rijks:Tgakd:3200"          # rijks:<Micrio id>:<width>, aic:<IIIF id>, or file:<path in the repository>
    crop = [0.05, 0.42, 0.95]            # x0, y0, x1 of the scan; the height follows from 16:9
    disc = [1330, 520, 260]              # centre and radius of the accent disc on the 2560 by 1440 picture
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
    """Every colour token of the design system for this theme: the derived ones, the rest as in the default theme."""
    derived = colours(spec['accent'])
    one = targets.theme_table(t, [{'id': 'saturnus'}])['saturnus']
    cols = dict(one['colors'])
    term = dict(one['terminal'])
    for k, v in derived.items():
        if k in ('cursor', 'selection'):
            term[k] = v
        elif k in cols:
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
        wallpapers.make(source_path(repo, plate['source']), tuple(plate['crop']), tuple(plate['disc']), os.path.join(d, 'wallpaper.jpg'),
                        bg=tab['colors']['background'], accent=tab['colors']['accent'], **({'paper': plate['paper']} if 'paper' in plate else {}))
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
