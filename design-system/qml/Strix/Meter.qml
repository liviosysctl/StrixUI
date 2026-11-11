// A load figure in the top bar: a thin upright bar that fills, the name and the value.
//   Meter { label: "CPU"; value: 0.08 }
import QtQuick

Row {
    id: root

    property string label
    property real value: 0
    property string valueText: Math.round(value * 100) + "%"

    spacing: 5

    Rectangle {
        width: 2
        height: 10
        color: Theme.borderStrong
        anchors.verticalCenter: parent.verticalCenter
        Rectangle {
            anchors.bottom: parent.bottom
            width: parent.width
            height: parent.height * Math.max(0, Math.min(1, root.value))
            color: Theme.text
            Behavior on height { NumberAnimation { duration: Theme.durSlow; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeOut } }
        }
    }
    Label { text: root.label; textStyle: "caption"; color: Theme.textMuted; anchors.verticalCenter: parent.verticalCenter }
    Label { text: root.valueText; textStyle: "caption"; font.weight: Font.Medium; anchors.verticalCenter: parent.verticalCenter }
}
