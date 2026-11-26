// The dock as part of the bottom edge, of smoked glass: at rest a tab 5px high with a short accent
// line, its corners flaring into the edge. out: it rises to hold one row of controls and widens to
// fit them.
// In Quickshell put it in a PanelWindow anchored to the bottom and set `out` from a HoverHandler.
import QtQuick
import QtQuick.Shapes

Item {
    id: root

    property bool out: false
    default property alias content: row.data

    readonly property int restWidth: 4 * Theme.space6
    readonly property int openWidth: row.implicitWidth + 2 * Theme.space1
    /// One row of controls and a step above and below it
    readonly property int openHeight: Theme.control + 2 * Theme.space1
    /// How far the corners flare into the screen edge
    readonly property int flare: Theme.radiusMd

    implicitWidth: openWidth + 2 * flare
    implicitHeight: openHeight

    Item {
        id: tab
        anchors.bottom: parent.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        width: root.out ? root.openWidth : root.restWidth
        height: root.out ? root.openHeight : Theme.dockRest
        Behavior on width { NumberAnimation { duration: Theme.durSlow; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeOut } }
        Behavior on height { NumberAnimation { duration: Theme.durBase; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeOut } }

        // the tab with open bottom, and the two flares into the screen edge
        Shape {
            anchors.fill: parent
            anchors.leftMargin: -root.flare
            anchors.rightMargin: -root.flare
            preferredRendererType: Shape.CurveRenderer
            ShapePath {
                id: path
                readonly property real f: root.flare
                // The chips stand one small step inside: the corners run parallel to theirs
                readonly property real r: Math.min(Theme.radiusMd + Theme.space1, tab.height)
                fillColor: Theme.smoke(Theme.surface)
                strokeColor: Theme.glassEdge
                strokeWidth: Theme.lineHair
                startX: 0; startY: tab.height
                PathArc { x: path.f; y: tab.height - path.f; radiusX: path.f; radiusY: path.f; direction: PathArc.Counterclockwise }
                PathLine { x: path.f; y: Math.min(tab.height - path.f, path.r) }
                PathLine { x: path.f; y: path.r }
                PathArc { x: path.f + path.r; y: 0; radiusX: path.r; radiusY: path.r }
                PathLine { x: tab.width + path.f - path.r; y: 0 }
                PathArc { x: tab.width + path.f; y: path.r; radiusX: path.r; radiusY: path.r }
                PathLine { x: tab.width + path.f; y: Math.max(path.r, tab.height - path.f) }
                PathArc { x: tab.width + 2 * path.f; y: tab.height; radiusX: path.f; radiusY: path.f; direction: PathArc.Counterclockwise }
            }
        }

        Rectangle {
            anchors.horizontalCenter: parent.horizontalCenter
            y: Theme.lineHair
            width: Theme.space5
            height: Theme.lineHair
            color: Theme.accent
            opacity: root.out ? 0 : 1
            Behavior on opacity { NumberAnimation { duration: Theme.durFast } }
        }

        Row {
            id: row
            anchors.verticalCenter: parent.verticalCenter
            x: Theme.space1
            spacing: Theme.space1
            clip: true
            opacity: root.out ? 1 : 0
            visible: opacity > 0
            Behavior on opacity { NumberAnimation { duration: root.out ? Theme.durBase : Theme.durFast } }
        }
    }

    // Opening, the symbols rise 4px into place one after another, `stagger` apart and at most eight steps,
    // after the content has started to fade in.
    onOutChanged: {
        if (!out || Theme.reducedMotion)
            return
        for (var i = 0; i < row.children.length; i++) {
            var c = row.children[i]
            if (!c.visible)
                continue
            rise.createObject(root, { target: c, delay: Theme.durFast + Math.min(i, 7) * Theme.stagger }).start()
        }
    }

    Component {
        id: rise
        SequentialAnimation {
            id: a
            property Item target
            property int delay
            PropertyAction { target: a.target; property: "y"; value: Theme.space1 }
            PauseAnimation { duration: a.delay }
            NumberAnimation { target: a.target; property: "y"; to: 0; duration: Theme.durBase; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeSpring }
            onFinished: a.destroy()
        }
    }
}
