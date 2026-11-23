// The one plate of the system: smoked glass with a hair line, the corners of every plate and a
// shadow. Panels, cards that float, dialogs, menus and the buttons of the top bar stand on it.
//   Surface { elevation: "pop"; ... }
import QtQuick
import QtQuick.Effects

Item {
    id: root

    /// none, pop (the top bar, tooltips), window, panel (panels, dialogs)
    property string elevation: "panel"
    property int radius: Theme.radiusMd
    /// The colour of the smoke: a control on glass of its own raises it under the pointer
    property color tint: Theme.surface
    property color borderColor: Theme.glassEdge
    default property alias content: inner.data

    readonly property var shadows: ({ pop: [3, 10, 0.5], window: [8, 22, 0.5], panel: [14, 36, 0.6] })
    readonly property var sh: shadows[elevation]

    Rectangle {
        id: ground
        anchors.fill: parent
        radius: root.radius
        border.width: Theme.lineHair
        border.color: root.borderColor
        // A little light on the upper edge, as on glass that stands upright
        gradient: Gradient {
            GradientStop { position: 0; color: Theme.smoke(Theme.mix(root.tint, Theme.text, 0.07)) }
            GradientStop { position: 1; color: Theme.smoke(root.tint) }
        }
        layer.enabled: !!root.sh
        layer.effect: MultiEffect {
            shadowEnabled: true
            shadowColor: Qt.rgba(0, 0, 0, root.sh ? root.sh[2] : 0)
            shadowVerticalOffset: root.sh ? root.sh[0] : 0
            blurMax: 64
            shadowBlur: root.sh ? root.sh[1] / 64 : 0
        }
    }

    Item {
        id: inner
        anchors.fill: parent
    }
}
