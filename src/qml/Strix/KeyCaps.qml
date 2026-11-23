// Keys as small chips, written as on the cheat sheet: KeyCaps { keys: "Super Shift Return" }
import QtQuick

Row {
    id: root

    property string keys
    property color ink: Theme.textMuted

    spacing: Theme.space1

    Repeater {
        model: root.keys === "" ? [] : root.keys.split(" ")
        Rectangle {
            implicitWidth: Math.max(Theme.mark, k.implicitWidth + 2 * Theme.space1)
            implicitHeight: Theme.mark
            radius: Theme.radiusSm
            color: "transparent"
            border.width: Theme.lineHair
            border.color: Theme.border
            Label { id: k; anchors.centerIn: parent; text: modelData; textStyle: "micro"; color: root.ink }
        }
    }
}
