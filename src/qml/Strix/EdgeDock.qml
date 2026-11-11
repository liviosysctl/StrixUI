// The dock as part of the bottom edge: at rest a tab 5px high and 132px wide with a short accent line,
// its corners flaring into the edge. out: it rises to 28px and widens to fit its content.
// In Quickshell put it in a PanelWindow anchored to the bottom and set `out` from a HoverHandler.
import QtQuick
import QtQuick.Shapes

Item {
    id: root

    property bool out: false
    default property alias content: row.data

    readonly property int restWidth: 132
    readonly property int openWidth: row.implicitWidth + 12

    implicitWidth: openWidth + 12
    implicitHeight: Theme.dockHeight

    Item {
        id: tab
        anchors.bottom: parent.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        width: root.out ? root.openWidth : root.restWidth
        height: root.out ? Theme.dockHeight : Theme.dockRest
        Behavior on width { NumberAnimation { duration: Theme.durSlow; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeOut } }
        Behavior on height { NumberAnimation { duration: Theme.durBase; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeOut } }

        // the tab with open bottom, and the two flares into the screen edge
        Shape {
            anchors.fill: parent
            anchors.leftMargin: -6
            anchors.rightMargin: -6
            preferredRendererType: Shape.CurveRenderer
            readonly property real w: width
            readonly property real h: height
            readonly property real r: Math.min(Theme.radiusMd, h)
            ShapePath {
                fillColor: Theme.surface
                strokeColor: Theme.border
                strokeWidth: Theme.lineHair
                startX: 0; startY: tab.height
                PathArc { x: 6; y: tab.height - 6; radiusX: 6; radiusY: 6; direction: PathArc.Counterclockwise }
                PathLine { x: 6; y: Math.min(tab.height - 6, 4) }
                PathLine { x: 6; y: 4 }
                PathArc { x: 10; y: 0; radiusX: 4; radiusY: 4 }
                PathLine { x: tab.width + 2; y: 0 }
                PathArc { x: tab.width + 6; y: 4; radiusX: 4; radiusY: 4 }
                PathLine { x: tab.width + 6; y: Math.max(4, tab.height - 6) }
                PathArc { x: tab.width + 12; y: tab.height; radiusX: 6; radiusY: 6; direction: PathArc.Counterclockwise }
            }
        }

        Rectangle {
            anchors.horizontalCenter: parent.horizontalCenter
            y: 1
            width: 24
            height: 1
            color: Theme.accent
            opacity: root.out ? 0 : 1
            Behavior on opacity { NumberAnimation { duration: Theme.durFast } }
        }

        Row {
            id: row
            anchors.verticalCenter: parent.verticalCenter
            x: 6
            spacing: 1
            clip: true
            opacity: root.out ? 1 : 0
            visible: opacity > 0
            Behavior on opacity { NumberAnimation { duration: root.out ? Theme.durBase : Theme.durFast } }
        }
    }
}
