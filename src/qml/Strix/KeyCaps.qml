// Keys as small chips, written as on the cheat sheet: KeyCaps { keys: "Super Shift Return" }
import QtQuick

Row {
    id: root

    property string keys
    property color ink: Theme.textMuted

    spacing: 3

    Repeater {
        model: root.keys === "" ? [] : root.keys.split(" ")
        Rectangle {
            implicitWidth: k.implicitWidth + 8
            implicitHeight: 16
            radius: Theme.radiusXs
            color: "transparent"
            border.width: Theme.lineHair
            border.color: Theme.border
            Label { id: k; anchors.centerIn: parent; text: modelData; font.pixelSize: 10; font.weight: Font.Normal; lineHeight: 14; color: root.ink }
        }
    }
}
