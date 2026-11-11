// A share of a whole at a glance: load, memory, battery. value from 0 to 1; label below the ring.
import QtQuick
import QtQuick.Shapes

Column {
    id: root

    property real value: 0
    property string label
    property string valueText: Math.round(value * 100) + "%"
    property int size: 60

    spacing: 6

    Item {
        width: root.size
        height: root.size
        anchors.horizontalCenter: parent.horizontalCenter

        Shape {
            anchors.fill: parent
            preferredRendererType: Shape.CurveRenderer
            ShapePath {
                strokeColor: Theme.border
                strokeWidth: 1
                fillColor: "transparent"
                PathAngleArc { centerX: root.size / 2; centerY: root.size / 2; radiusX: root.size / 2 - 1.5; radiusY: radiusX; startAngle: 0; sweepAngle: 360 }
            }
            ShapePath {
                strokeColor: Theme.accent
                strokeWidth: Theme.lineBold
                fillColor: "transparent"
                capStyle: ShapePath.FlatCap
                PathAngleArc {
                    centerX: root.size / 2; centerY: root.size / 2; radiusX: root.size / 2 - 1.5; radiusY: radiusX
                    startAngle: -90
                    sweepAngle: 360 * Math.max(0, Math.min(1, root.shown))
                }
            }
        }

        Label {
            anchors.centerIn: parent
            text: root.valueText
            font.weight: Font.Medium
            lineHeight: 16
        }
    }

    property real shown: value
    Behavior on shown { NumberAnimation { duration: Theme.durReveal; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeOut } }

    Label {
        visible: root.label !== ""
        anchors.horizontalCenter: parent.horizontalCenter
        text: root.label
        textStyle: "caption"
        color: Theme.textMuted
    }
}
