// One action in a Menu. shortcut: keys at the right ("Ctrl C"); danger: the action destroys data.
import QtQuick
import QtQuick.Templates as T

T.MenuItem {
    id: control

    property string iconName
    property string shortcut
    property bool danger: false

    implicitWidth: 184
    implicitHeight: 24
    leftPadding: Theme.space2
    rightPadding: Theme.space2
    hoverEnabled: true
    opacity: enabled ? 1 : Theme.dimDisabled

    contentItem: Row {
        spacing: Theme.space2
        Icon { visible: control.iconName !== ""; name: control.iconName; size: 12; color: control.danger ? Theme.error : Theme.textMuted; anchors.verticalCenter: parent.verticalCenter }
        Label {
            width: parent.width - (control.iconName !== "" ? 12 + parent.spacing : 0) - (k.visible ? k.implicitWidth + parent.spacing : 0)
            text: control.text
            color: control.danger ? Theme.error : Theme.text
            elide: Text.ElideRight
            anchors.verticalCenter: parent.verticalCenter
        }
        Label { id: k; visible: control.shortcut !== ""; text: control.shortcut; font.pixelSize: 10; color: Theme.textFaint; anchors.verticalCenter: parent.verticalCenter }
    }

    background: Rectangle {
        radius: Theme.radiusXs
        color: control.highlighted || control.hovered ? Theme.surfaceRaised : "transparent"
        Behavior on color { ColorAnimation { duration: Theme.durInstant } }
    }
}
