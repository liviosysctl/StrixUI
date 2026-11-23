// One row to pick from: app finder results, clipboard history, networks, devices.
// The selected row is raised and carries a short accent line on its left edge.
import QtQuick
import QtQuick.Templates as T

T.ItemDelegate {
    id: control

    // The hand over what can be pressed, as on every clickable part of the shell
    HoverHandler { cursorShape: Qt.PointingHandCursor }

    property string iconName
    /// Small text at the right: a size, a time, a state.
    property string detail
    property bool selected: highlighted
    /// The selected look comes from a Glide that moves between the rows
    property bool glide: false

    implicitWidth: 320
    implicitHeight: Theme.control
    leftPadding: Theme.space2
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
            width: parent.width - (control.iconName !== "" ? Theme.icon + parent.spacing : 0) - (d.visible ? d.implicitWidth + parent.spacing : 0)
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
            textStyle: "caption"
            color: Theme.textFaint
            anchors.verticalCenter: parent.verticalCenter
        }
    }

    background: Rectangle {
        radius: Theme.radiusMd
        color: control.hovered && !(control.glide && control.selected) || control.selected && !control.glide ? Theme.surfaceRaised : "transparent"
        Behavior on color { ColorAnimation { duration: Theme.durFast } }

        Rectangle {
            anchors.verticalCenter: parent.verticalCenter
            width: Theme.lineBold
            height: control.selected && !control.glide ? Theme.icon : 0
            radius: width / 2
            color: Theme.accent
            opacity: control.selected && !control.glide ? 1 : 0
            Behavior on opacity { NumberAnimation { duration: Theme.durFast } }
            Behavior on height { NumberAnimation { duration: Theme.durFast; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeOut } }
        }
        FocusRing { target: control }
    }
}
