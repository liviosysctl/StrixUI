// A hair rule with a small lozenge, as between sections of an old title page.
import QtQuick

Item {
    implicitWidth: 120
    implicitHeight: 8
    opacity: 0.45

    Rectangle { anchors.verticalCenter: parent.verticalCenter; x: 0; width: (parent.width - 7) / 2 - Theme.space2 + 4; height: Theme.lineHair; color: Theme.line }
    Rectangle { anchors.verticalCenter: parent.verticalCenter; anchors.right: parent.right; width: (parent.width - 7) / 2 - Theme.space2 + 4; height: Theme.lineHair; color: Theme.line }
    Rectangle {
        anchors.centerIn: parent
        width: 5
        height: 5
        rotation: 45
        color: "transparent"
        border.width: Theme.lineHair
        border.color: Theme.line
    }
}
