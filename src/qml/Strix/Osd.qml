// The answer to a hardware key: volume, brightness, mute. A plate at the bottom centre, above the dock.
import QtQuick

Surface {
    id: root

    property string iconName: "volume-2"
    /// 0 to 1
    property real value: 0.5

    implicitWidth: 240
    implicitHeight: Theme.control + 2 * Theme.space1
    elevation: "pop"

    Row {
        anchors.fill: parent
        anchors.leftMargin: Theme.space3
        anchors.rightMargin: Theme.space3
        spacing: Theme.space2
        Icon { name: root.iconName; color: Theme.text; anchors.verticalCenter: parent.verticalCenter }
        Item {
            width: parent.width - Theme.icon - out.width - 2 * parent.spacing
            height: Theme.lineBold
            anchors.verticalCenter: parent.verticalCenter
            Rectangle { y: 0.5; width: parent.width; height: Theme.lineHair; color: Theme.border }
            Rectangle {
                width: parent.width * Math.max(0, Math.min(1, root.value))
                height: parent.height
                radius: height / 2
                color: Theme.accent
                Behavior on width { NumberAnimation { duration: Theme.durFast; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeOut } }
            }
        }
        Label { id: out; width: Theme.space5; horizontalAlignment: Text.AlignRight; text: Math.round(root.value * 100); textStyle: "caption"; font.weight: Font.Medium; anchors.verticalCenter: parent.verticalCenter }
    }
}
