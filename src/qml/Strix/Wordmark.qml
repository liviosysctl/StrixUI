// The blackletter wordmark, optionally with the lozenge rule and the motto under it.
import QtQuick

Column {
    id: root

    property string name: "Strix"
    property string motto: "nocte vigilat"
    /// "emblem" (44px) or "display" (96px, lock screen and splash)
    property string size: "emblem"

    spacing: 2

    Label { id: mark; anchors.horizontalCenter: parent.horizontalCenter; text: root.name; textStyle: root.size; lineHeight: root.size === "display" ? 96 : 40 }
    Rule { visible: root.motto !== ""; width: Math.max(mark.implicitWidth, motto.implicitWidth); anchors.horizontalCenter: parent.horizontalCenter }
    Label { id: motto; visible: root.motto !== ""; anchors.horizontalCenter: parent.horizontalCenter; text: root.motto; textStyle: "motto"; color: Theme.textMuted }
}
