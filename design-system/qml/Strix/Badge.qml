// A short state next to a name: "new", "3", "failed". kind: default, accent, error, count.
import QtQuick

Rectangle {
    id: root

    property string text
    property string kind: "default"
    property string iconName

    readonly property color ink: kind === "accent" || kind === "count" ? Theme.onAccent : kind === "error" ? Theme.error : Theme.textMuted

    implicitWidth: Math.max(16, row.implicitWidth + (kind === "count" ? 8 : 10))
    implicitHeight: 16
    radius: kind === "count" ? 8 : Theme.radiusXs
    color: kind === "accent" || kind === "count" ? Theme.accent : "transparent"
    border.width: Theme.lineHair
    border.color: kind === "accent" || kind === "count" ? Theme.accent : kind === "error" ? Theme.error : Theme.borderStrong

    Row {
        id: row
        anchors.centerIn: parent
        spacing: 4
        Icon { visible: root.iconName !== ""; name: root.iconName; size: 10; color: root.ink; anchors.verticalCenter: parent.verticalCenter }
        Label { text: root.text; textStyle: "micro"; color: root.ink; lineHeight: 14; anchors.verticalCenter: parent.verticalCenter }
    }
}
