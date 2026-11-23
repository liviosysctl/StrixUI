// Every token of the Strix design system. {{generated}}
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
    property string current: "{{default}}"
    /// Variant of the theme in use: dark or light. apply() sets it from the engine.
    property string variant: "dark"
    /// Ids in the order of the theme picker, the default first.
    readonly property var order: {{order}}
    /// Name, description, wallpaper file and plate caption of every theme.
    readonly property var gods: ({
{{info}}
    })
    /// Folder of the wallpapers, with a trailing slash. The shell may point it elsewhere.
    property url wallpapers: Qt.resolvedUrl("../../assets/Wallpapers/")
    /// A theme from a connected theme repository: id, name, description, dir (its folder), plate. Set by apply().
    property var external: null
    /// Name, description and plate of the theme in use, built in or external.
    readonly property var about: gods[current] || (external && external.id === current ? external : gods["{{default}}"])
    function wallpaper(id) {
        id = id || current
        // Every god has two plates: the dark one and, for the light variant, <god>-light.jpg
        if (gods[id]) return wallpapers + (variant === "light" ? gods[id].wallpaper.replace(".jpg", "-light.jpg") : gods[id].wallpaper)
        if (external && external.id === id) return "file://" + external.dir + "/wallpaper.jpg"
        return wallpapers + gods["{{default}}"].wallpaper
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
        if (tokens.variant) variant = tokens.variant
        const base = themes[current] || themes["{{default}}"]
        const merged = Object.assign({}, base)
        for (const k in tokens.colors) if (k in base) merged[k] = tokens.colors[k]
        live = merged
        const t = tokens.terminal
        if (t) {
            const term = Object.assign({}, terminals[current] || terminals["{{default}}"])
            for (const k of ["background", "foreground", "cursor", "selection"]) if (t[k]) term[k] = t[k]
            const names = {{palette}}
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
    /// A colour of the tokens as QML reads it: CSS writes the opacity last (#rrggbbaa), QML first
    /// (#aarrggbb), so the scrim would turn into a clear blue.
    function css(v) { return typeof v === "string" && v.length === 9 ? "#" + v.slice(7) + v.slice(1, 7) : v }

    readonly property var c: live || themes[current] || themes["{{default}}"]
    readonly property var tc: liveTerminal || terminals[current] || terminals["{{default}}"]

    // ------------------------------------------------------------ colours
{{colours}}

    // terminal
{{term}}

    // ------------------------------------------------------------ sizes in pixels at scale 1
{{dims}}

    // ------------------------------------------------------------ motion
    /// True when the person asked for less motion; every duration but the theme cycle becomes 1 ms.
    property bool reducedMotion: false
{{durs}}
    // easing.bezierCurve for Easing.BezierSpline: x1, y1, x2, y2 and the end point
{{eases}}

    // ------------------------------------------------------------ opacity
{{opac}}

    // ------------------------------------------------------------ type
    readonly property string sans: "{{sans}}"
    readonly property string serif: "{{serif}}"
    readonly property string mono: "{{mono}}"
    /// Text styles of the brand book. Label { textStyle: "caption" } applies one.
    readonly property var styles: ({
{{styles}}
    })

    /// The fonts ship with the module, so a gallery or a test needs nothing installed.
    readonly property list<FontLoader> fonts: [
{{fonts}}
    ]

    // ------------------------------------------------------------ the built-in themes
    readonly property var themes: ({
{{themes}}
    })
    readonly property var terminals: ({
{{terms}}
    })
}
