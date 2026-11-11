// The answer to a hardware key: volume, brightness, mute. A pill at the bottom centre, above the dock.
import QtQuick

Surface {
    id: root

    property string iconName: "volume-2"
    property real value: 0.5

    implicitWidth: 200
    implicitHeight: Theme.osdHeight
    elevation: "pop"

    Row {
        anchors.fill: parent
        anchors.leftMargin: Theme.space3
        anchors.rightMargin: Theme.space3
        spacing: Theme.space2
        Icon { name: root.iconName; color: Theme.text; anchors.verticalCenter: parent.verticalCenter }
        Item {
            width: parent.width - 14 - out.width - 2 * parent.spacing
            height: Theme.lineBold
            anchors.verticalCenter: parent.verticalCenter
            Rectangle { y: 0.5; width: parent.width; height: Theme.lineHair; color: Theme.border }
            Rectangle {
                width: parent.width * Math.max(0, Math.min(1, root.value))
                height: parent.height
                color: Theme.accent
                Behavior on width { NumberAnimation { duration: Theme.durFast; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeOut } }
            }
        }
        Label { id: out; width: 3 * 7.2; horizontalAlignment: Text.AlignRight; text: Math.round(root.value * 100); textStyle: "caption"; font.weight: Font.Medium; anchors.verticalCenter: parent.verticalCenter }
    }
}
