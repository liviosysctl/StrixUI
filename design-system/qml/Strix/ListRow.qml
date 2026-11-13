// One row to pick from: app finder results, clipboard history, networks, devices.
// The selected row shows the accent caret ">" at its left.
import QtQuick
import QtQuick.Templates as T

T.ItemDelegate {
    id: control

    property string iconName
    /// Small text at the right: a size, a time, a state.
    property string detail
    property bool selected: highlighted

    implicitWidth: 320
    implicitHeight: Theme.controlMd
    leftPadding: 20
    rightPadding: Theme.space2
    hoverEnabled: true
    focusPolicy: Qt.StrongFocus
    opacity: enabled ? 1 : Theme.dimDisabled

    contentItem: Row {
        spacing: Theme.space2
        Icon {
            visible: control.iconName !== ""
            name: control.iconName
            color: control.selected || control.hovered ? Theme.text : Theme.textMuted
            hovered: control.hovered
            anchors.verticalCenter: parent.verticalCenter
        }
        Label {
            width: parent.width - (control.iconName !== "" ? 14 + parent.spacing : 0) - (d.visible ? d.implicitWidth + parent.spacing : 0)
            text: control.text
            color: control.selected || control.hovered ? Theme.text : Theme.textMuted
            elide: Text.ElideRight
            anchors.verticalCenter: parent.verticalCenter
            Behavior on color { ColorAnimation { duration: Theme.durFast } }
        }
        Label {
            id: d
            visible: control.detail !== ""
            text: control.detail
            font.pixelSize: 11
            color: Theme.textFaint
            anchors.verticalCenter: parent.verticalCenter
        }
    }

    background: Rectangle {
        radius: Theme.radiusXs
        color: control.selected || control.hovered ? Theme.surfaceRaised : "transparent"
        Behavior on color { ColorAnimation { duration: Theme.durFast } }

        Label {
            x: control.selected ? 7 : 3
            anchors.verticalCenter: parent.verticalCenter
            text: ">"
            font.weight: Font.DemiBold
            color: Theme.accentText
            opacity: control.selected ? 1 : 0
            Behavior on opacity { NumberAnimation { duration: Theme.durFast } }
            Behavior on x { NumberAnimation { duration: Theme.durFast; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeOut } }
        }

        FocusRing { target: control; targetRadius: Theme.radiusXs }
    }
}
