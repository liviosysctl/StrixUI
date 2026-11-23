// One action in a Menu. shortcut: keys at the right ("Ctrl C"); danger: the action destroys data.
import QtQuick
import QtQuick.Templates as T

T.MenuItem {
    id: control

    // The hand over what can be pressed, as on every clickable part of the shell
    HoverHandler { cursorShape: Qt.PointingHandCursor }

    property string iconName
    property string shortcut
    property bool danger: false

    implicitWidth: 184
    implicitHeight: Theme.control
    leftPadding: Theme.space2
    rightPadding: Theme.space2
    hoverEnabled: true
    opacity: enabled ? 1 : Theme.dimDisabled

    contentItem: Row {
        spacing: Theme.space2
        Icon { visible: control.iconName !== ""; name: control.iconName; hovered: control.hovered || control.highlighted; color: control.danger ? Theme.error : Theme.textMuted; anchors.verticalCenter: parent.verticalCenter }
        Label {
            width: parent.width - (control.iconName !== "" ? Theme.icon + parent.spacing : 0) - (k.visible ? k.implicitWidth + parent.spacing : 0)
            text: control.text
            color: control.danger ? Theme.error : Theme.text
            elide: Text.ElideRight
            anchors.verticalCenter: parent.verticalCenter
        }
        Label { id: k; visible: control.shortcut !== ""; text: control.shortcut; textStyle: "micro"; color: Theme.textFaint; anchors.verticalCenter: parent.verticalCenter }
    }

    background: Rectangle {
        radius: Theme.radiusMd
        color: control.highlighted || control.hovered ? Theme.surfaceRaised : "transparent"
        Behavior on color { ColorAnimation { duration: Theme.durInstant } }
    }
}
