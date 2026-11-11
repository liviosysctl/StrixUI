#!/usr/bin/env python3
"""Builds the design system from src/ and tools/.

    python3 tools/build.py                  writes design-system/ and a local preview under build/preview/
    python3 tools/build.py --artifact DIR   writes the same system as the Claude Design System artifact expects it

Every value comes from tools/palette.py and the tokens() function below; nothing in design-system/ is edited by hand.
"""
import argparse, datetime, json, math, os, re, shutil, random, sys
import palette, pantheon
from palette import C, T

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'src')
OUT = os.path.join(ROOT, 'design-system')
PREVIEW = os.path.join(ROOT, 'build', 'preview')
ARTIFACT = json.load(open(os.path.join(ROOT, 'tools', 'artifact.json'), encoding='utf-8'))
FONTS = ['JetBrainsMono-Variable.woff2', 'JetBrainsMono-Italic-Variable.woff2', 'IMFellEnglish-Regular.woff2', 'IMFellEnglish-Italic.woff2', 'GrenzeGotisch-Variable.woff2']
TITLE = 'Strix'
NS = 'Kit'

C['syntax-comment'] = '#8a847a'
T['bright-black'] = '#857f76'

def w(path, text):
    p = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(text)

# ---------------------------------------------------------------- tokens
USAGE = {
 'background': 'Desktop behind everything, boot splash, installer. Tinted faintly toward the god in each aspect. Ground for text, text-muted, accent-text, error.',
 'surface': 'Windows, panels, the pill, cards, dialogs. Ground for text, text-muted, accent-text, error.',
 'border': 'Decorative lines and frames on surface and background: inactive window border, dividers, progress track.',
 'text': 'Primary text on background, surface and surface-raised (13.9:1 or more). Wordmark, slider thumb.',
 'text-muted': 'Secondary text and resting icons on background, surface and surface-raised (6.2:1 or more).',
 'accent': 'The colour of the god of the moment: Strix red under Saturnus, the default, and one hue per aspect. Fills only: main action, selected segment, active workspace, active window border, running progress, cursor, the disc of the wallpaper. Not for text; use accent-text.',
 'on-accent': 'Text and icons on accent, accent-hover and accent-pressed (4.5:1 or more in every aspect): white on dark accents, near-black on light ones.',
 'focus': 'Focus ring, 2px, after a 2px gap in background. 4.0:1 or more on background, surface and surface-raised in every aspect.',
 'error': 'Error text and the border of a field in error, on background, surface and surface-raised (6.3:1 or more). Always with words.',
 'warning': 'Warnings as text or icon with words, on background and surface (7.7:1 or more). Never a filled box.',
 'surface-raised': 'Hover and selected rows, tooltips, the cover of a media card. One step above surface.',
 'surface-sunken': 'Wells: text fields, switch track, segmented track.',
 'border-strong': 'Borders that carry meaning: controls, secondary buttons, tooltips. 3.2:1 or more on every surface.',
 'text-faint': 'Placeholders, line numbers, timestamps, the :: separator. 3.6:1 or more: never for text a person must read.',
 'accent-hover': 'Primary button under the pointer.',
 'accent-pressed': 'Primary button while pressed.',
 'accent-text': 'The accent as text or icon on background, surface, surface-raised and accent-soft (5.2:1 or more): the list caret, the power icon, links.',
 'accent-soft': 'Quiet ground in the accent hue: hover of a danger button, selection in text.',
 'line': 'Cream line work: wallpaper drawing, bracket frames, the edge of the selected theme card. Drawn at 1px, usually at reduced opacity.',
 'scrim': 'Dimming layer under dialogs, the session menu and the theme picker.',
 'success': 'Success as text or icon with words, on background and surface (7.8:1 or more).',
 'info': 'Neutral information as text or icon with words, on background and surface (7.1:1 or more).',
 'syntax-keyword': 'Code: keywords and storage.',
 'syntax-string': 'Code: strings.',
 'syntax-number': 'Code: numbers and units.',
 'syntax-function': 'Code: function names, set bold.',
 'syntax-type': 'Code: types and modules.',
 'syntax-constant': 'Code: constants, attributes, macros.',
 'syntax-comment': 'Code: comments, set italic. 4.6:1 or more on background and surface.',
 'syntax-operator': 'Code: operators and punctuation.',
 'chart-1': 'Charts: the series that matters. Also the peak bars of the visualizer.',
 'chart-2': 'Charts: second series.',
 'chart-3': 'Charts: third series, and bars at rest.',
 'chart-4': 'Charts: fourth series.',
 'chart-5': 'Charts: fifth series. Series differ in lightness, so they hold without colour.',
}
ORDER = ['background', 'surface', 'surface-raised', 'surface-sunken', 'border', 'border-strong', 'line', 'scrim',
         'text', 'text-muted', 'text-faint', 'accent', 'accent-hover', 'accent-pressed', 'accent-soft', 'accent-text', 'on-accent', 'focus',
         'error', 'warning', 'success', 'info',
         'syntax-keyword', 'syntax-string', 'syntax-number', 'syntax-function', 'syntax-type', 'syntax-constant', 'syntax-comment', 'syntax-operator',
         'chart-1', 'chart-2', 'chart-3', 'chart-4', 'chart-5']
C['scrim'] = '#000000b8'
TERM_USAGE = {'background': 'Terminal ground.', 'foreground': 'Terminal text.', 'cursor': 'Terminal cursor, a block.', 'selection': 'Terminal selection ground; foreground stays readable on it.'}

ASPECTS = pantheon.all_aspects()
GOD_IDS = [g[0] for g in pantheon.GODS]

def per_god(token, base):
    """A colour value for every aspect: the god's own where the aspect sets the token, else the default's."""
    v = {GOD_IDS[0]: base}
    for gid in GOD_IDS[1:]:
        if token in ASPECTS[gid] and ASPECTS[gid][token] != base:
            v[gid] = ASPECTS[gid][token]
    return v

def tokens():
    color = [{'name': n, 'value': per_god(n, C[n]), 'usage': USAGE[n]} for n in ORDER]
    ansi = ['black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']
    for k in ['background', 'foreground', 'cursor', 'selection'] + ansi + ['bright-' + a for a in ansi]:
        val = per_god('background' if k == 'background' else k, T[k]) if k in ('background', 'cursor', 'selection') else {GOD_IDS[0]: T[k]}
        color.append({'name': 'term-' + k, 'value': val, 'usage': TERM_USAGE.get(k, 'ANSI ' + k.replace('-', ' ') + '.')})
    mono = '"JetBrains Mono", ui-monospace, "Cascadia Mono", Consolas, monospace'
    serif = '"IM Fell English", "Iowan Old Style", Georgia, serif'
    fraktur = '"Grenze Gotisch", "IM Fell English", Georgia, serif'
    fonts = [
        {'family': 'JetBrains Mono', 'file': 'fonts/JetBrainsMono-Variable.woff2', 'weight': '100 800', 'style': 'normal'},
        {'family': 'JetBrains Mono', 'file': 'fonts/JetBrainsMono-Italic-Variable.woff2', 'weight': '100 800', 'style': 'italic'},
        {'family': 'IM Fell English', 'file': 'fonts/IMFellEnglish-Regular.woff2', 'weight': '400', 'style': 'normal'},
        {'family': 'IM Fell English', 'file': 'fonts/IMFellEnglish-Italic.woff2', 'weight': '400', 'style': 'italic'},
        {'family': 'Grenze Gotisch', 'file': 'fonts/GrenzeGotisch-Variable.woff2', 'weight': '100 900', 'style': 'normal'},
    ]
    groups = [
        {'name': 'Blackletter', 'family': 'fraktur', 'styles': [
            {'name': 'display', 'fontSize': '96px', 'lineHeight': 1, 'fontWeight': 300, 'sample': 'Strix', 'usage': 'The wordmark on the lock screen, greeter and splash.'},
            {'name': 'emblem', 'fontSize': '44px', 'lineHeight': 1, 'fontWeight': 300, 'sample': 'Strix', 'usage': 'Theme names on the picker card, the system name in About, the wordmark in system info. Names only, one or two words.'},
        ]},
        {'name': 'Old style', 'family': 'serif', 'styles': [
            {'name': 'title-lg', 'fontSize': '26px', 'lineHeight': '30px', 'fontWeight': 400, 'fontStyle': 'italic', 'sample': '10 November', 'usage': 'The one large line of a panel: the date.'},
            {'name': 'title', 'fontSize': '22px', 'lineHeight': '26px', 'fontWeight': 400, 'sample': 'Shut down now?', 'usage': 'Dialog titles, page titles in settings.'},
            {'name': 'subtitle', 'fontSize': '18px', 'lineHeight': '22px', 'fontWeight': 400, 'sample': 'Ghostty', 'usage': 'Card titles.'},
            {'name': 'aside', 'fontSize': '16px', 'lineHeight': '20px', 'fontWeight': 400, 'fontStyle': 'italic', 'sample': 'November 2026', 'usage': 'Italic asides: calendar month, panel headings, track titles, empty states, plate captions.'},
            {'name': 'motto', 'fontSize': '13px', 'lineHeight': '18px', 'fontWeight': 400, 'fontStyle': 'italic', 'letterSpacing': '0.22em', 'sample': 'nocte vigilat', 'usage': 'The motto and greetings. Lowercase, spaced, italic. One line, never a label.'},
        ]},
        {'name': 'Interface', 'family': 'mono', 'styles': [
            {'name': 'clock', 'fontSize': '112px', 'lineHeight': 0.92, 'fontWeight': 200, 'letterSpacing': '-0.04em', 'sample': '21', 'usage': 'The stacked clock of the lock screen: hours over minutes, very light.'},
            {'name': 'heading', 'fontSize': '13px', 'lineHeight': '20px', 'fontWeight': 600, 'sample': 'Lock screen', 'usage': 'Section headings inside apps.'},
            {'name': 'body', 'fontSize': '12px', 'lineHeight': '18px', 'fontWeight': 400, 'sample': 'Installs every package the app needs.', 'usage': 'Running text, list rows, field text, code and the terminal.'},
            {'name': 'label', 'fontSize': '12px', 'lineHeight': '18px', 'fontWeight': 600, 'sample': 'Kernel', 'usage': 'Labels and the left side of a label :: value pair. Semibold, sentence case.'},
            {'name': 'value', 'fontSize': '12px', 'lineHeight': '18px', 'fontWeight': 400, 'sample': '6.18.2', 'usage': 'Values. Regular weight.'},
            {'name': 'caption', 'fontSize': '11px', 'lineHeight': '16px', 'fontWeight': 400, 'sample': 'Checked just now', 'usage': 'Descriptions, the top bar, the dock, help text, segmented labels.'},
            {'name': 'micro', 'fontSize': '10px', 'lineHeight': '14px', 'fontWeight': 500, 'sample': '3 new', 'usage': 'Badges, key hints, timestamps. Nothing smaller exists.'},
        ]},
    ]
    def fam(rows):
        return {'tokens': [{'name': n, 'value': v, 'usage': u} for n, v, u in rows]}
    return {
        'name': TITLE, 'version': 1,
        'color': {'themes': [{'id': g[0], 'name': g[1]} for g in pantheon.GODS], 'tokens': color},
        'type': {'fonts': fonts, 'families': {'mono': mono, 'serif': serif, 'fraktur': fraktur}, 'groups': groups},
        'spacing': fam([
            ('space-1', '4px', 'Gap between an icon and its value; padding inside the pill.'),
            ('space-2', '8px', 'Gap between related controls; gap from pill to panel.'),
            ('space-3', '12px', 'Padding of buttons and segments. Gap between tiled windows.'),
            ('space-4', '16px', 'Padding of panels, cards and windows. Side inset of the top bar.'),
            ('space-5', '24px', 'Padding of dialogs; gap between groups.'),
            ('space-6', '32px', 'Gap between sections.'),
            ('space-7', '48px', 'Outer margin of full-screen layouts.'),
            ('space-8', '64px', 'Left inset of the lock screen column.'),
        ]),
        'radius': fam([
            ('radius-xs', '1px', 'Checkbox, list rows, segmented thumb, tooltip, calendar day.'),
            ('radius-sm', '2px', 'Buttons, fields, segmented track.'),
            ('radius-md', '4px', 'Windows, panels, cards, dialogs, notifications.'),
            ('radius-lg', '8px', 'Large media: theme previews in the store and settings.'),
            ('radius-pill', '999px', 'Switch, radio, count badges, the active workspace, the search field.'),
        ]),
        'shadow': fam([
            ('shadow-pop', '0 3px 10px rgba(0, 0, 0, 0.5)', 'Small floating parts: toolbar, tooltip.'),
            ('shadow-window', '0 8px 22px rgba(0, 0, 0, 0.5)', 'Tiled and floating windows.'),
            ('shadow-panel', '0 14px 36px rgba(0, 0, 0, 0.6)', 'Panels, dialogs, menus, notifications.'),
            ('focus-ring', '0 0 0 2px %s, 0 0 0 4px %s' % (C['background'], C['focus']), 'Keyboard focus on every control: a 2px gap in background, then 2px of focus.'),
        ]),
        'line': fam([
            ('line-hair', '1px', 'Every border and divider.'),
            ('line-bold', '2px', 'The filled part of a progress line and of a ring. Tracks stay at one pixel.'),
        ]),
        'size': fam([
            ('bar-height', '26px', 'Height of the top bar.'),
            ('control-sm', '22px', 'Small buttons and icon buttons inside panels.'),
            ('control-md', '28px', 'Buttons, fields, list rows.'),
            ('dock-rest', '5px', 'Height of the dock at rest: a thin tab on the bottom edge.'),
            ('dock-height', '28px', 'Height of the dock once the pointer reaches the bottom edge.'),
            ('osd-height', '28px', 'Height of the OSD.'),
        ]),
        'duration': fam([
            ('dur-instant', '80ms', 'Press feedback, menu hover.'),
            ('dur-fast', '140ms', 'Hover, focus, tooltips, small fades, border colour.'),
            ('dur-base', '220ms', 'Switch, segmented thumb, tab change, dialogs, list items entering, window focus.'),
            ('dur-slow', '360ms', 'Panel growing out of the pill, carousel, windows opening and moving, workspace change, rolling numbers.'),
            ('dur-reveal', '640ms', 'Circular reveal of a new theme, unlocking, ring gauges filling.'),
            ('dur-loop', '1400ms', 'One pass of an indeterminate progress line.'),
            ('god-cycle', '600s', 'How often the god of the desktop changes by itself, unless kept in the pantheon.'),
            ('stagger', '30ms', 'Delay between neighbours when a list enters.'),
        ]),
        'easing': fam([
            ('ease-out', 'cubic-bezier(0.2, 0.8, 0.2, 1)', 'Things arriving: open, enter, hover.'),
            ('ease-in', 'cubic-bezier(0.5, 0, 0.9, 0.3)', 'Things leaving: close, dismiss.'),
            ('ease-in-out', 'cubic-bezier(0.65, 0, 0.35, 1)', 'Things travelling: thumb, carousel, workspace change, reveal.'),
            ('ease-spring', 'cubic-bezier(0.3, 1.4, 0.5, 1)', 'A small overshoot: switch thumb, check mark, window pop.'),
        ]),
        'opacity': fam([
            ('dim-disabled', '0.4', 'Disabled controls.'),
            ('dim-inactive', '0.92', 'Inactive windows.'),
            ('dim-wallpaper', '0.55', 'Wallpaper brightness under the lock screen and the theme picker.'),
        ]),
    }

def tokens_css(t):
    first = t['color']['themes'][0]['id']
    out = ['/* %s — generated from tokens.json */' % TITLE, ':root, [data-theme="%s"] {' % first]
    for c in t['color']['tokens']:
        out.append('  --%s: %s;' % (c['name'], c['value'][first]))
    for s in t['shadow']['tokens']:
        out.append('  --%s: %s;' % (s['name'], s['value']))
    out.append('}')
    for th in t['color']['themes'][1:]:
        out.append('[data-theme="%s"] {' % th['id'])
        for c in t['color']['tokens']:
            if th['id'] in c['value']:
                out.append('  --%s: %s;' % (c['name'], c['value'][th['id']]))
        out.append('}')
    out.append(':root {')
    for famname in ('spacing', 'radius', 'line', 'size', 'duration', 'easing', 'opacity'):
        for s in t[famname]['tokens']:
            out.append('  --%s: %s;' % (s['name'], s['value']))
    for k, v in t['type']['families'].items():
        out.append('  --font-%s: %s;' % (k, v))
    out.append('}')
    for g in t['type']['groups']:
        for s in g['styles']:
            lh = s['lineHeight']
            out.append('.%s { font-family: var(--font-%s); font-size: %s; line-height: %s; font-weight: %s;%s%s }' % (
                s['name'], g['family'], s['fontSize'], lh, s['fontWeight'],
                ' font-style: %s;' % s['fontStyle'] if 'fontStyle' in s else '',
                ' letter-spacing: %s;' % s['letterSpacing'] if 'letterSpacing' in s else ''))
    for f in t['type']['fonts']:
        out.append('@font-face { font-family: "%s"; src: url("%s") format("woff2"); font-weight: %s; font-style: %s; font-display: block; }' % (f['family'], f['file'], f['weight'], f['style']))
    return '\n'.join(out) + '\n'

# ---------------------------------------------------------------- wallpaper
def wallpaper(inline):
    """A star-chart drawing: a few fine cream arcs, one graduated circle, a meridian, and a single flat red disc."""
    W, H = 2560, 1440
    line = 'var(--line)' if inline else C['line']
    acc = 'var(--accent)' if inline else C['accent']
    bg = 'var(--background)' if inline else C['background']
    def st(col, extra=''):
        return 'style="stroke:%s;fill:none;%s"' % (col, extra)
    cx, cy = 1560, 1010          # centre of the chart, low and right of the middle
    p = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" preserveAspectRatio="xMidYMid slice">' % (W, H),
         '<rect width="%d" height="%d" style="fill:%s"/>' % (W, H, bg)]
    # the disc
    dx, dy, dr = 1560, 660, 250
    p.append('<circle cx="%d" cy="%d" r="%d" style="fill:%s"/>' % (dx, dy, dr, acc))
    # concentric arcs
    for r, o, wd in ((430, 0.55, 1.5), (640, 0.5, 1.5), (900, 0.42, 1.5), (1210, 0.34, 1.5), (1560, 0.26, 1.5)):
        p.append('<circle cx="%d" cy="%d" r="%d" %s/>' % (cx, cy, r, st(line, 'stroke-width:%s;opacity:%s' % (wd, o))))
    # graduated ring: ticks every 2 degrees between two close circles
    r1, r2 = 640, 664
    p.append('<circle cx="%d" cy="%d" r="%d" %s/>' % (cx, cy, r2, st(line, 'stroke-width:1.5;opacity:0.5')))
    ticks = []
    for i in range(180):
        a = math.radians(i * 2)
        long_ = i % 5 == 0
        ra = r1 - (16 if long_ else 0)
        ticks.append('M%.1f %.1fL%.1f %.1f' % (cx + ra * math.cos(a), cy + ra * math.sin(a), cx + r2 * math.cos(a), cy + r2 * math.sin(a)))
    p.append('<path d="%s" %s/>' % (''.join(ticks), st(line, 'stroke-width:1.5;opacity:0.4')))
    # tilted ellipse (the ecliptic) and the meridian through the disc
    p.append('<ellipse cx="%d" cy="%d" rx="1210" ry="360" transform="rotate(-23.4 %d %d)" %s/>' % (cx, cy, cx, cy, st(line, 'stroke-width:1.5;opacity:0.5')))
    p.append('<path d="M%d -40L%d %d" %s/>' % (cx, cx, H + 40, st(line, 'stroke-width:1.5;opacity:0.4')))
    p.append('<path d="M-40 %dL%d %d" %s/>' % (cy, W + 40, cy, st(line, 'stroke-width:1.5;opacity:0.3')))
    # a handful of stars as small crosses, fixed positions
    rnd = random.Random(7)
    stars = []
    for _ in range(11):
        x, y, s = rnd.randint(140, W - 140), rnd.randint(120, H - 420), rnd.choice((7, 7, 10))
        if (x - dx) ** 2 + (y - dy) ** 2 < (dr + 60) ** 2:
            continue
        stars.append('M%d %dh%dM%d %dv%d' % (x - s, y, 2 * s, x, y - s, 2 * s))
    p.append('<path d="%s" %s/>' % (''.join(stars), st(line, 'stroke-width:1.5;opacity:0.75')))
    p.append('</svg>')
    return ''.join(p)

# ---------------------------------------------------------------- icons
ICON_NAMES = ['search', 'cpu', 'memory-stick', 'thermometer', 'music', 'bell', 'power', 'video', 'settings', 'wifi', 'bluetooth', 'volume-2',
              'sun', 'cloud', 'chevron-left', 'chevron-right', 'x', 'minus', 'square', 'check', 'lock', 'log-out', 'moon', 'rotate-cw',
              'play', 'pause', 'skip-back', 'skip-forward', 'layout-grid', 'hard-drive', 'download', 'trash-2', 'copy', 'clipboard',
              'folder', 'file', 'terminal', 'info', 'triangle-alert', 'usb', 'package', 'image', 'calendar', 'monitor', 'plus',
              'arrow-right', 'eye', 'eye-off', 'refresh-cw', 'palette', 'camera', 'crop', 'app-window', 'keyboard', 'gauge', 'disc-3', 'circle-alert', 'cloud-sun',
              'sliders-horizontal', 'zap', 'corner-down-left', 'arrow-up', 'book-open', 'pipette', 'scan-line', 'history', 'square-terminal', 'wallpaper', 'swatch-book', 'type', 'moon-star', 'scan', 'clock', 'hard-drive-download', 'images']
def icons():
    d = {}
    for n in ICON_NAMES:
        p = os.path.join(SRC, 'icons', n + '.svg')
        s = open(p, encoding='utf-8').read()
        s = re.sub(r'<!--.*?-->', '', s, flags=re.S)
        inner = re.search(r'<svg[^>]*>(.*)</svg>', s, re.S).group(1)
        d[n] = re.sub(r'\s+', ' ', inner).strip()
    return d

# ---------------------------------------------------------------- assemble
def main():
    global OUT
    ap = argparse.ArgumentParser()
    ap.add_argument('--artifact', metavar='DIR', help='write the artifact layout (DIR/project/...) instead of design-system/')
    args = ap.parse_args()
    artifact = bool(args.artifact)
    import components, docs
    if artifact:
        OUT = os.path.join(os.path.abspath(args.artifact), 'project')
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    t = tokens()
    w('tokens.json', json.dumps(t, indent=1, ensure_ascii=False) + '\n')
    fd = os.path.join(OUT, 'fonts'); os.makedirs(fd, exist_ok=True)
    for f in FONTS:
        shutil.copy(os.path.join(SRC, 'fonts', f), os.path.join(fd, f))
    # wallpapers: in the artifact they are uploads named by the index, in the repository plain files
    walls = {fn: '/_blob/' + bid for bid, fn in components.BLOBS.items()}
    if not artifact:
        wd = os.path.join(OUT, 'assets', 'Wallpapers'); os.makedirs(wd, exist_ok=True)
        for f in sorted(os.listdir(os.path.join(SRC, 'fonts'))):
            if f.startswith('LICENSE'):
                shutil.copy(os.path.join(SRC, 'fonts', f), os.path.join(fd, f))
        for fn in walls:
            shutil.copy(os.path.join(SRC, 'wallpapers', fn), os.path.join(wd, fn))
        open(os.path.join(wd, 'star-chart.svg'), 'w').write(wallpaper(False))
    def fix(html):
        for fn, url in walls.items():
            html = html.replace(url, url if artifact else '../../assets/Wallpapers/' + fn)
        return html
    # bundle
    names = [c['name'] for c in components.COMPONENTS]
    header = '/* @ds-bundle: %s */\n' % json.dumps({'format': 4, 'namespace': NS, 'components': [{'name': n} for n in names]})
    js = open(os.path.join(SRC, 'bundle.js'), encoding='utf-8').read()
    js = js.replace('__ICONS__', json.dumps(icons(), ensure_ascii=False)).replace('__WALL__', json.dumps(wallpaper(True)))
    assert '</script' not in js and '<!--' not in js
    w('components/bundle.js', header + js)
    w('components/bundle.css', open(os.path.join(SRC, 'bundle.css'), encoding='utf-8').read())
    w('components/index.d.ts', components.DTS)
    allc = components.COMPONENTS + components.SCREENS
    for c in allc:
        attrs = 'group="%s" height=%d' % (c['group'], c['height'])
        if c.get('width'): attrs += ' width=%d' % c['width']
        html = ('<!-- @dsCard %s -->\n<!doctype html>\n<html lang="en">\n<head><meta charset="utf-8"><title>%s — preview</title>%s</head>\n<body>\n%s\n<script>\nKit.hydrate(document);\n%s\n</script>\n</body>\n</html>\n'
                % (attrs, c['name'], ('<style>\n%s\n</style>' % c['css'].strip()) if c.get('css') else '', c['html'].strip(), c.get('js', '').strip()))
        assert len(html) < 256000
        w('components/%s/preview.html' % c['name'], fix(html))
        w('components/%s/README.md' % c['name'], '# %s\n\n%s\n' % (c['name'], c['doc'].strip()))
    w('components/Cover/preview.html', docs.COVER)
    w('README.md', docs.README)
    for path, text in docs.SECTIONS.items():
        w(path, text)
    w('assets/Wallpapers/README.md', docs.WALL_README)
    tc = tokens_css(t)
    if artifact:
        write_index()
    else:
        # the artifact page compiles tokens.css itself; everywhere else it is part of the system
        w('tokens.css', tc)
        write_preview(allc)
    print('%s: %d components, %d screens' % (os.path.relpath(OUT, os.getcwd()), len(components.COMPONENTS), len(components.SCREENS)))

def write_index():
    a = ARTIFACT
    files, order = {}, []
    for fn, rec in a['wallpapers'].items():
        files[fn] = {'name': fn, 'blob': rec['blob'], 'size': rec['size'], 'type': rec['type']}
        order.append(fn)
    now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    idx = {'v': 3, 'layout': 'files', 'createdOnFiles': {'v': 1, 'at': a['created']}, 'title': TITLE, 'namespace': NS, 'libraries': [], 'sections': {},
           'groups': ['Wallpapers'], 'assetGroups': {'Wallpapers': {'name': 'Wallpapers', 'tile': 'l', 'order': order, 'files': files}},
           'blobs': {}, 'docs': {'sections': []}, 'lastChange': {'by': 'Livio', 'at': now, 'via': 'StrixUI repository', 'note': 'Built from the StrixUI repository.'}}
    w('design-system.json', json.dumps(idx, indent=1) + '\n')

def write_preview(allc):
    """A local copy of what the artifact shows: one page per preview with the tokens, stylesheet and script loaded."""
    if os.path.exists(PREVIEW):
        shutil.rmtree(PREVIEW)
    os.makedirs(PREVIEW)
    rel = os.path.relpath(OUT, PREVIEW)
    head = ('<link rel="stylesheet" href="%s/tokens.css"><link rel="stylesheet" href="%s/components/bundle.css">'
            '<script src="%s/components/bundle.js"></scr' 'ipt>') % (rel, rel, rel)
    links = []
    for c in [{'name': 'Cover', 'group': 'Overview'}] + allc:
        src = open(os.path.join(OUT, 'components', c['name'], 'preview.html'), encoding='utf-8').read()
        src = src.replace('../../assets/', rel + '/assets/')
        src = src.replace('<head>', '<head>' + head, 1).replace('<html lang="en">', '<html lang="en" data-theme="saturnus">')
        open(os.path.join(PREVIEW, c['name'] + '.html'), 'w', encoding='utf-8').write(src)
        links.append('<li><a href="%s.html">%s</a> <small>%s</small></li>' % (c['name'], c['name'], c['group']))
    open(os.path.join(PREVIEW, 'index.html'), 'w', encoding='utf-8').write(
        '<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Strix previews</title>'
        '<style>body{background:#0b0a09;color:#ece6da;font:13px/1.8 monospace;padding:24px}a{color:#f2556a}small{color:#77726a}</style>'
        '</head><body><h1>Strix previews</h1><ul>%s</ul></body></html>\n' % ''.join(links))

if __name__ == '__main__':
    main()
