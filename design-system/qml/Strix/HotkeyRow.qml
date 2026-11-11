// One action in Settings › Hotkeys: name, what it acts on, its keys (press to record new ones),
// and at the right "back to the default" or "remove" for own hotkeys.
import QtQuick
import QtQuick.Templates as T

Item {
    id: root

    property string action
    property string target
    property string keys
    /// "", "reset" (changed from the default) or "remove" (an own hotkey)
    property string tail: ""
    property bool recording: false
    /// A short highlight after the cheat sheet jumped here.
    property bool marked: false

    signal record()
    signal reset()
    signal remove()

    implicitWidth: 560
    implicitHeight: 36

    Rectangle {
        anchors.fill: parent
        color: root.marked ? Theme.accentSoft : "transparent"
        Behavior on color { ColorAnimation { duration: Theme.durSlow } }
    }

    Column {
        anchors.verticalCenter: parent.verticalCenter
        width: parent.width - rec.width - 28 - 2 * Theme.space3
        Label { width: parent.width; text: root.action; elide: Text.ElideRight }
        Label { width: parent.width; text: root.target; font.family: Theme.serif; font.italic: true; font.pixelSize: 12; lineHeight: 16; color: Theme.textMuted; elide: Text.ElideRight }
    }

    T.AbstractButton {
        id: rec
        anchors.right: parent.right
        anchors.rightMargin: 28 + Theme.space3
        anchors.verticalCenter: parent.verticalCenter
        width: Math.max(132, k.implicitWidth + 2 * Theme.space2)
        height: 24
        hoverEnabled: true
        onClicked: root.record()
        background: Rectangle {
            radius: Theme.radiusSm
            color: "transparent"
            border.width: Theme.lineHair
            border.color: root.recording ? Theme.accent : rec.hovered ? Theme.borderStrong : "transparent"
            FocusRing { target: rec }
        }
        contentItem: Item {
            KeyCaps { id: k; visible: !root.recording; keys: root.keys; anchors.right: parent.right; anchors.rightMargin: Theme.space2; anchors.verticalCenter: parent.verticalCenter }
            Label {
                visible: root.recording
                anchors.centerIn: parent
                text: "Press the new keys"
                textStyle: "caption"
                color: Theme.accentText
                SequentialAnimation on opacity {
                    running: root.recording
                    loops: Animation.Infinite
                    NumberAnimation { from: 1; to: 0.35; duration: 900 }
                    NumberAnimation { from: 0.35; to: 1; duration: 900 }
                }
            }
        }
    }

    IconButton {
        visible: root.tail !== ""
        anchors.right: parent.right
        anchors.verticalCenter: parent.verticalCenter
        width: 24
        height: 24
        iconName: root.tail === "remove" ? "trash-2" : "undo-2"
        onClicked: root.tail === "remove" ? root.remove() : root.reset()
    }

    Rectangle { anchors.bottom: parent.bottom; width: parent.width; height: Theme.lineHair; color: Theme.border }
}
