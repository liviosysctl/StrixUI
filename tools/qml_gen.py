"""The generated parts of the QML module: Theme.qml (every token) and Icons.qml (the symbols as paths)."""
import json, re

from targets import GENERATED, TERMINAL, camel, px, text_styles, tok

PALETTE = TERMINAL[4:]


# ---------------------------------------------------------------- icons: Lucide SVG to one path per icon

def _num(s):
    return float(s)


def svg_to_path(inner):
    """Every shape of a Lucide icon as one SVG path string (QtQuick.Shapes PathSvg reads it)."""
    out = []
    for m in re.finditer(r'<(path|circle|line|polyline|polygon|rect|ellipse)\b([^>]*)/?>', inner):
        kind, attrs = m.group(1), dict(re.findall(r'([a-z-]+)="([^"]*)"', m.group(2)))
        g = lambda k, d=0.0: _num(attrs.get(k, d))
        if kind == 'path':
            d = attrs['d'].strip()
            # every <path> starts on its own; once joined, a leading relative move would hang off the last path.
            # Make that first point absolute and keep what follows relative (implicit pairs after m are relative lines).
            m = re.match(r'm\s*(-?(?:\d+\.?\d*|\.\d+))[\s,]*(-?(?:\d+\.?\d*|\.\d+))\s*(.*)$', d, re.S)
            if m:
                rest = m.group(3)
                d = 'M%s %s' % (m.group(1), m.group(2)) + (('l' + rest) if rest and not rest[0].isalpha() else rest)
            out.append(d)
        elif kind in ('circle', 'ellipse'):
            cx, cy = g('cx'), g('cy')
            rx = g('r') if kind == 'circle' else g('rx')
            ry = g('r') if kind == 'circle' else g('ry')
            out.append('M%g %gA%g %g 0 1 0 %g %gA%g %g 0 1 0 %g %gZ' % (cx - rx, cy, rx, ry, cx + rx, cy, rx, ry, cx - rx, cy))
        elif kind == 'line':
            out.append('M%g %gL%g %g' % (g('x1'), g('y1'), g('x2'), g('y2')))
        elif kind in ('polyline', 'polygon'):
            pts = re.findall(r'-?[\d.]+', attrs['points'])
            pairs = [(pts[i], pts[i + 1]) for i in range(0, len(pts), 2)]
            out.append('M' + 'L'.join('%s %s' % p for p in pairs) + ('Z' if kind == 'polygon' else ''))
        elif kind == 'rect':
            x, y, w, h = g('x'), g('y'), g('width'), g('height')
            rx = g('rx', attrs.get('ry', 0))
            ry = g('ry', attrs.get('rx', 0))
            if rx or ry:
                out.append('M%g %gH%gA%g %g 0 0 1 %g %gV%gA%g %g 0 0 1 %g %gH%gA%g %g 0 0 1 %g %gV%gA%g %g 0 0 1 %g %gZ' % (
                    x + rx, y, x + w - rx, rx, ry, x + w, y + ry, y + h - ry, rx, ry, x + w - rx, y + h, x + rx, rx, ry, x, y + h - ry, y + ry, rx, ry, x + rx, y))
            else:
                out.append('M%g %gH%gV%gH%gZ' % (x, y, x + w, y + h, x))
    return ' '.join(out)


def icons_qml(icons):
    entries = ',\n'.join('        %s: %s' % (json.dumps(n), json.dumps(svg_to_path(s))) for n, s in sorted(icons.items()))
    return '''// The Lucide symbols in use (ISC), each as one path on a 24 by 24 grid. %s
pragma Singleton
import QtQuick

QtObject {
    readonly property var paths: ({
%s
    })

    function path(name) {
        return paths[name] || ""
    }
}
''' % (GENERATED, entries)


# ---------------------------------------------------------------- Theme.qml

def _js(v):
    return json.dumps(v, ensure_ascii=False)


def theme_qml(t, table, gods, plates):
    names = [x['name'] for x in t['color']['tokens'] if not x['name'].startswith('term-')]
    order = [g['id'] for g in gods]
    themes = ',\n'.join('        %s: { %s }' % (g['id'], ', '.join('%s: "%s"' % (_js(n), table[g['id']]['colors'][n]) for n in names)) for g in gods)
    terms = ',\n'.join('        %s: { %s }' % (g['id'], ', '.join('%s: "%s"' % (_js(n), table[g['id']]['terminal'][n]) for n in TERMINAL)) for g in gods)
    info = ',\n'.join('        %s: { name: %s, description: %s, wallpaper: "%s.jpg", plate: %s }' % (
        g['id'], _js(g['name']), _js(g['description']), g['id'], _js(plates[g['id']])) for g in gods)
    colour_props = '\n'.join('    readonly property color %s: c[%s]' % (camel(n), _js(n)) for n in names)
    term_props = '\n'.join('    readonly property color %s: tc[%s]' % (camel('term-' + n), _js(n)) for n in TERMINAL)

    dims = []
    for group in ['spacing', 'radius', 'line', 'size']:
        for name, value, usage in tok(t, group):
            dims.append('    readonly property int %s: %d  // %s' % (camel(name), px(value), usage))
    durs = []
    for name, value, usage in tok(t, 'duration'):
        ms = int(value[:-1]) * 1000 if value.endswith('s') and not value.endswith('ms') else int(value[:-2])
        if name == 'theme-cycle':
            durs.append('    readonly property int themeCycle: %d  // %s' % (ms, usage))
        else:
            durs.append('    readonly property int %s: reducedMotion ? 1 : %d  // %s' % (camel(name), ms, usage))
    eases = []
    for name, value, usage in tok(t, 'easing'):
        nums = [float(n) for n in re.findall(r'-?[\d.]+', value)]
        eases.append('    readonly property var %s: [%s, 1, 1]  // %s' % (camel(name), ', '.join('%g' % n for n in nums), usage))
    opac = '\n'.join('    readonly property real %s: %s  // %s' % (camel(n), v, u) for n, v, u in tok(t, 'opacity'))
    styles = ',\n'.join('        %s: { family: %s, pixelSize: %g, lineHeight: %g, weight: %d, italic: %s, letterSpacing: %g }' % (
        _js(s['name']), _js(FAMILY_QML[s['family']]), s['size'], round(s['line'], 2), s['weight'], str(s['italic']).lower(), s['spacing'])
        for s in text_styles(t))
    return THEME % dict(generated=GENERATED, order=_js(order), themes=themes, terms=terms, info=info, colours=colour_props, term=term_props,
                        dims='\n'.join(dims), durs='\n'.join(durs), eases='\n'.join(eases), opac=opac, styles=styles,
                        palette=_js(PALETTE), default=order[0], mono=FAMILY_QML['mono'], serif=FAMILY_QML['serif'], fraktur=FAMILY_QML['fraktur'])


FAMILY_QML = {'mono': 'JetBrains Mono', 'serif': 'IM Fell English', 'fraktur': 'Grenze Gotisch'}

THEME = '''// Every token of the Strix design system. %(generated)s
//
// The colours follow the theme engine at runtime: Strix.Shell's ThemeFile reads
// /run/strix/theme/tokens.json and calls apply(). Without it (a gallery, a test) the
// built-in themes below are used, picked by `current`.
pragma Singleton
import QtQuick

QtObject {
    id: theme

    // ------------------------------------------------------------ which theme
    /// Id of the theme in use. Set it to preview a god; apply() sets it from the engine.
    property string current: "%(default)s"
    /// Ids in the order of the theme picker, the default first.
    readonly property var order: %(order)s
    /// Name, description, wallpaper file and plate caption of every theme.
    readonly property var gods: ({
%(info)s
    })
    /// Folder of the wallpapers, with a trailing slash. The shell may point it elsewhere.
    property url wallpapers: Qt.resolvedUrl("../../assets/Wallpapers/")
    /// A theme from a connected theme repository: id, name, description, dir (its folder), plate. Set by apply().
    property var external: null
    /// Name, description and plate of the theme in use, built in or external.
    readonly property var about: gods[current] || (external && external.id === current ? external : gods["%(default)s"])
    function wallpaper(id) {
        id = id || current
        if (gods[id]) return wallpapers + gods[id].wallpaper
        if (external && external.id === id) return "file://" + external.dir + "/wallpaper.jpg"
        return wallpapers + gods["%(default)s"].wallpaper
    }

    /// Colours read from the engine's tokens.json; empty until apply() ran.
    property var live: null
    property var liveTerminal: null

    /// Takes the engine's tokens.json (already parsed). Unknown or missing colours fall back to the built-in theme.
    function apply(tokens) {
        if (!tokens || !tokens.colors) return
        if (tokens.theme && !themes[tokens.theme])
            external = { id: tokens.theme, name: tokens.name || tokens.theme, description: tokens.description || "", dir: tokens.dir || "", plate: tokens.plate || "", wallpaper: "wallpaper.jpg" }
        if (tokens.theme) current = tokens.theme
        const base = themes[current] || themes["%(default)s"]
        const merged = Object.assign({}, base)
        for (const k in tokens.colors) if (k in base) merged[k] = tokens.colors[k]
        live = merged
        const t = tokens.terminal
        if (t) {
            const term = Object.assign({}, terminals[current] || terminals["%(default)s"])
            for (const k of ["background", "foreground", "cursor", "selection"]) if (t[k]) term[k] = t[k]
            const names = %(palette)s
            if (t.palette) for (let i = 0; i < names.length && i < t.palette.length; i++) term[names[i]] = t.palette[i]
            liveTerminal = term
        }
    }

    /// Back to the built-in theme of `id` (or of `current`).
    function preview(id) {
        live = null
        liveTerminal = null
        if (id) current = id
    }

    /// a mixed with b: t = 0 gives a, t = 1 gives b (CSS color-mix in srgb)
    function mix(a, b, t) { return Qt.rgba(a.r + (b.r - a.r) * t, a.g + (b.g - a.g) * t, a.b + (b.b - a.b) * t, a.a + (b.a - a.a) * t) }
    /// The colour with another opacity.
    function alpha(c, a) { return Qt.rgba(c.r, c.g, c.b, a) }

    readonly property var c: live || themes[current] || themes["%(default)s"]
    readonly property var tc: liveTerminal || terminals[current] || terminals["%(default)s"]

    // ------------------------------------------------------------ colours
%(colours)s

    // terminal
%(term)s

    // ------------------------------------------------------------ sizes in pixels at scale 1
%(dims)s

    // ------------------------------------------------------------ motion
    /// True when the person asked for less motion; every duration but the theme cycle becomes 1 ms.
    property bool reducedMotion: false
%(durs)s
    // easing.bezierCurve for Easing.BezierSpline: x1, y1, x2, y2 and the end point
%(eases)s

    // ------------------------------------------------------------ opacity
%(opac)s

    // ------------------------------------------------------------ type
    readonly property string mono: "%(mono)s"
    readonly property string serif: "%(serif)s"
    readonly property string fraktur: "%(fraktur)s"
    /// Text styles of the brand book. Label { textStyle: "caption" } applies one.
    readonly property var styles: ({
%(styles)s
    })

    /// The fonts ship with the module, so a gallery or a test needs nothing installed.
    readonly property list<FontLoader> fonts: [
        FontLoader { source: "fonts/JetBrainsMono-Variable.woff2" },
        FontLoader { source: "fonts/JetBrainsMono-Italic-Variable.woff2" },
        FontLoader { source: "fonts/IMFellEnglish-Regular.woff2" },
        FontLoader { source: "fonts/IMFellEnglish-Italic.woff2" },
        FontLoader { source: "fonts/GrenzeGotisch-Variable.woff2" }
    ]

    // ------------------------------------------------------------ the built-in themes
    readonly property var themes: ({
%(themes)s
    })
    readonly property var terminals: ({
%(terms)s
    })
}
'''
