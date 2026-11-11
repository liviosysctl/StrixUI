// The ground of panels, cards that float, dialogs and menus: surface fading a little toward background,
// a hair border, 4px corners and a shadow. Surface { elevation: "pop"; ... }
import QtQuick
import QtQuick.Effects

Item {
    id: root

    /// none, pop (toolbar, tooltip), window, panel (panels, dialogs)
    property string elevation: "panel"
    property int radius: Theme.radiusMd
    property color borderColor: Theme.border
    default property alias content: inner.data

    readonly property var shadows: ({ pop: [3, 10, 0.5], window: [8, 22, 0.5], panel: [14, 36, 0.6] })
    readonly property var sh: shadows[elevation]

    Rectangle {
        id: ground
        anchors.fill: parent
        radius: root.radius
        border.width: Theme.lineHair
        border.color: root.borderColor
        gradient: Gradient {
            GradientStop { position: 0; color: Theme.surface }
            GradientStop { position: 1; color: Theme.mix(Theme.surface, Theme.background, 0.3) }
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
