// A Lucide symbol as a vector path, drawn in a 1.25px line at any size: Icon { name: "power"; color: Theme.accentText }
// Bind hovered to the control that holds it and the symbol plays its own small motion when the pointer arrives
// (the gear turns, the bell swings, an arrow nudges the way it points). A new name pops in.
import QtQuick
import QtQuick.Shapes

Item {
    id: root

    property string name
    property int size: 14
    property color color: Theme.textMuted
    /// Line width in pixels on screen.
    property real stroke: 1.25
    /// The pointer is over the control that holds the symbol. Each time it turns true the symbol plays its motion once
    /// and takes its colour (see tint).
    property bool hovered: false
    /// Take the hover colour. Off where the symbol sits on the accent (a primary button, a chosen segment).
    property bool tinted: true

    /// The colour a symbol takes under the pointer: what it means where it has a meaning (power and delete in error,
    /// a warning or a spark in warning, adding and going ahead in success, signals in info), otherwise the accent.
    readonly property var tints: ({
        "power": "error", "log-out": "error", "trash-2": "error", "x": "error", "circle-alert": "error",
        "zap": "warning", "triangle-alert": "warning", "bell": "warning", "sun": "warning", "cloud-sun": "warning",
        "thermometer": "warning", "lock": "warning",
        "plus": "success", "check": "success", "download": "success", "hard-drive-download": "success",
        "play": "success", "refresh-cw": "success", "rotate-cw": "success", "arrow-right": "success",
        "wifi": "info", "bluetooth": "info", "info": "info", "search": "info", "eye": "info", "eye-off": "info",
        "moon": "info", "moon-star": "info", "cloud": "info", "volume-2": "info", "music": "info"
    })
    readonly property color tint: ({ "error": Theme.error, "warning": Theme.warning, "success": Theme.success,
                                     "info": Theme.info })[tints[name]] || Theme.accentText
    readonly property color ink: hovered && tinted ? tint : color

    implicitWidth: size
    implicitHeight: size

    /// Which motion a symbol plays, by name. Rotations that end on a symmetry of the shape add up, so the symbol never turns back.
    readonly property var motions: ({
        "settings": "turn180", "sun": "turn90", "cloud-sun": "sway", "plus": "turn90", "x": "turn90",
        "refresh-cw": "turn180", "rotate-cw": "turn360", "disc-3": "turn360",
        "undo-2": "rock-left", "history": "rock-left", "moon": "rock-left", "moon-star": "rock-left",
        "bell": "ring", "lock": "shake", "triangle-alert": "shake", "circle-alert": "shake",
        "search": "zoom", "eye": "blink", "eye-off": "blink", "camera": "zoom", "scan": "zoom", "scan-line": "zoom",
        "arrow-right": "right", "chevron-right": "right", "skip-forward": "right", "log-out": "right",
        "corner-down-left": "left", "chevron-left": "left", "skip-back": "left",
        "arrow-up": "up", "download": "down", "hard-drive-download": "down",
        "power": "press", "play": "press", "pause": "press", "square": "press",
        "zap": "flicker", "wifi": "pulse", "bluetooth": "pulse", "volume-2": "pulse", "music": "pulse",
        "trash-2": "rock-left", "palette": "sway", "pipette": "sway", "pencil": "sway", "swatch-book": "sway",
        "wallpaper": "sway", "thermometer": "up", "gauge": "sway"
    })
    readonly property string motion: motions[name] || "lift"

    property bool _ready: false
    Component.onCompleted: _ready = true

    onHoveredChanged: if (hovered && _ready && !Theme.reducedMotion) play()
    onNameChanged: if (_ready && !Theme.reducedMotion) pop.restart()

    function play() {
        var m = motion
        if (m.indexOf("turn") === 0) {
            // Retarget from where the symbol stands, so a quick second hover keeps turning instead of jumping.
            var step = parseInt(m.substring(4))
            turn.stop()
            glyph.rotation = glyph.rotation % 360
            turn.from = glyph.rotation
            turn.to = Math.round(glyph.rotation / step) * step + step
            turn.duration = step >= 180 ? Theme.durReveal : Theme.durSlow
            turn.start()
            return
        }
        var a = ({ "ring": ring, "shake": shake, "rock-left": rock, "sway": sway, "zoom": zoom, "blink": blink,
                   "right": nudge, "left": nudge, "up": nudge, "down": nudge, "press": press,
                   "flicker": flicker, "pulse": pulse, "lift": nudge })[m]
        if (a === nudge) {
            nudge.dx = m === "right" ? 3 : m === "left" ? -3 : 0
            nudge.dy = m === "up" ? -3 : m === "lift" ? -2.5 : m === "down" ? 3 : 0
        }
        a.restart()
    }

    Item {
        id: glyph
        width: root.size
        height: root.size
        // The bell swings from its top; everything else turns around its middle.
        transformOrigin: root.motion === "ring" ? Item.Top : Item.Center
        transform: [shift, squash]

        Shape {
            width: 24
            height: 24
            scale: root.size / 24
            transformOrigin: Item.TopLeft
            preferredRendererType: Shape.CurveRenderer

            ShapePath {
                strokeColor: root.ink
                Behavior on strokeColor { ColorAnimation { duration: Theme.durFast; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeOut } }
                strokeWidth: root.stroke * 24 / root.size
                fillColor: "transparent"
                capStyle: ShapePath.RoundCap
                joinStyle: ShapePath.RoundJoin
                PathSvg { path: Icons.path(root.name) }
            }
        }
    }

    Translate { id: shift }
    Scale { id: squash; origin.x: root.size / 2; origin.y: root.size / 2 }

    // Turning by a symmetry of the shape: the gear by three teeth, the sun by two rays, plus and x by a quarter.
    NumberAnimation {
        id: turn
        target: glyph; property: "rotation"
        easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeSpring
    }

    // The bell swings on its top and settles.
    SequentialAnimation {
        id: ring
        NumberAnimation { target: glyph; property: "rotation"; to: 20; duration: Theme.durSlow / 4; easing.type: Easing.OutQuad }
        NumberAnimation { target: glyph; property: "rotation"; to: -15; duration: Theme.durSlow / 4; easing.type: Easing.InOutQuad }
        NumberAnimation { target: glyph; property: "rotation"; to: 8; duration: Theme.durSlow / 4; easing.type: Easing.InOutQuad }
        NumberAnimation { target: glyph; property: "rotation"; to: 0; duration: Theme.durSlow / 4; easing.type: Easing.OutQuad }
    }

    // A refusal or a warning: three short swings sideways.
    SequentialAnimation {
        id: shake
        NumberAnimation { target: shift; property: "x"; to: 2.5; duration: Theme.durSlow / 6 }
        NumberAnimation { target: shift; property: "x"; to: -2.5; duration: Theme.durSlow / 3 }
        NumberAnimation { target: shift; property: "x"; to: 1.5; duration: Theme.durSlow / 4 }
        NumberAnimation { target: shift; property: "x"; to: 0; duration: Theme.durSlow / 4; easing.type: Easing.OutQuad }
    }

    // Tipping back, the way time or an undo goes, and returning with a small overshoot.
    SequentialAnimation {
        id: rock
        NumberAnimation { target: glyph; property: "rotation"; to: -26; duration: Theme.durFast; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeOut }
        NumberAnimation { target: glyph; property: "rotation"; to: 0; duration: Theme.durSlow; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeSpring }
    }

    // A tool held in the hand: a small tilt forward and back.
    SequentialAnimation {
        id: sway
        NumberAnimation { target: glyph; property: "rotation"; to: 16; duration: Theme.durFast; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeOut }
        NumberAnimation { target: glyph; property: "rotation"; to: 0; duration: Theme.durSlow; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeSpring }
    }

    // Looking closer.
    SequentialAnimation {
        id: zoom
        ParallelAnimation {
            NumberAnimation { target: glyph; property: "scale"; to: 1.22; duration: Theme.durFast; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeOut }
            NumberAnimation { target: glyph; property: "rotation"; to: -12; duration: Theme.durFast; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeOut }
        }
        ParallelAnimation {
            NumberAnimation { target: glyph; property: "scale"; to: 1; duration: Theme.durSlow; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeSpring }
            NumberAnimation { target: glyph; property: "rotation"; to: 0; duration: Theme.durSlow; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeSpring }
        }
    }

    // The eye closes for a moment.
    SequentialAnimation {
        id: blink
        NumberAnimation { target: squash; property: "yScale"; to: 0.1; duration: Theme.durInstant; easing.type: Easing.InQuad }
        NumberAnimation { target: squash; property: "yScale"; to: 1; duration: Theme.durFast; easing.type: Easing.OutQuad }
    }

    // An arrow nudges the way it points; any other symbol lifts a little. Both come back with an overshoot.
    SequentialAnimation {
        id: nudge
        property real dx: 0
        property real dy: -2.5
        ParallelAnimation {
            NumberAnimation { target: shift; property: "x"; to: nudge.dx; duration: Theme.durFast; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeOut }
            NumberAnimation { target: shift; property: "y"; to: nudge.dy; duration: Theme.durFast; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeOut }
        }
        ParallelAnimation {
            NumberAnimation { target: shift; property: "x"; to: 0; duration: Theme.durSlow; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeSpring }
            NumberAnimation { target: shift; property: "y"; to: 0; duration: Theme.durSlow; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeSpring }
        }
    }

    // A switch being pressed: in, and back out with a small overshoot.
    SequentialAnimation {
        id: press
        NumberAnimation { target: glyph; property: "scale"; to: 0.78; duration: Theme.durInstant; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeOut }
        NumberAnimation { target: glyph; property: "scale"; to: 1; duration: Theme.durSlow; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeSpring }
    }

    // A spark: the line flickers twice.
    SequentialAnimation {
        id: flicker
        NumberAnimation { target: glyph; property: "opacity"; to: 0.2; duration: Theme.durInstant / 2 }
        NumberAnimation { target: glyph; property: "opacity"; to: 1; duration: Theme.durInstant / 2 }
        NumberAnimation { target: glyph; property: "opacity"; to: 0.55; duration: Theme.durInstant / 2 }
        NumberAnimation { target: glyph; property: "opacity"; to: 1; duration: Theme.durFast }
    }

    // A signal: the symbol breathes out once.
    SequentialAnimation {
        id: pulse
        NumberAnimation { target: glyph; property: "scale"; to: 1.2; duration: Theme.durFast; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeOut }
        NumberAnimation { target: glyph; property: "scale"; to: 1; duration: Theme.durSlow; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeSpring }
    }

    // A new symbol in the same place (play to pause, copy to check) pops in instead of switching flat.
    ParallelAnimation {
        id: pop
        NumberAnimation { target: glyph; property: "scale"; from: 0.6; to: 1; duration: Theme.durBase; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeSpring }
        NumberAnimation { target: glyph; property: "opacity"; from: 0; to: 1; duration: Theme.durFast; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeOut }
    }
}
