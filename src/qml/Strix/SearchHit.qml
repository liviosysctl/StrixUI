// One hit of Search: symbol, the name with the matched letters bold, where it lives as a serif
// path ("Settings › Display"), and at the right what Enter does or its keys.
// kind "command" writes the name as a shell line with "$ " in front.
import QtQuick
import QtQuick.Templates as T

T.ItemDelegate {
    id: control

    property string iconName
    /// Indices of the matched characters in text.
    property var hits: []
    /// Breadcrumbs: ["Settings", "Display"]
    property var path: []
    property string kind: "app"
    /// Keys of the action, or the word for what Enter does ("Open").
    property string keys
    property string enterText
    property bool selected: highlighted

    function marked(t, h) {
        const esc = s => s.replace(/&/g, "&amp;").replace(/</g, "&lt;")
        let out = ""
        for (let i = 0; i < t.length; i++) out += h.indexOf(i) >= 0 ? "<b>" + esc(t[i]) + "</b>" : esc(t[i])
        return out
    }

    implicitWidth: 552
    implicitHeight: 40
    leftPadding: 24
    rightPadding: Theme.space3
    hoverEnabled: true

    contentItem: Row {
        spacing: Theme.space3
        Icon { name: control.iconName; size: 16; hovered: control.hovered || control.selected; color: control.selected || control.hovered ? Theme.text : Theme.textMuted; anchors.verticalCenter: parent.verticalCenter }
        Column {
            width: parent.width - 16 - tailRow.width - 2 * parent.spacing
            anchors.verticalCenter: parent.verticalCenter
            Label {
                width: parent.width
                textFormat: Text.StyledText
                text: (control.kind === "command" ? "<font color='" + Theme.accentText + "'>$ </font>" : "") + control.marked(control.text, control.hits)
                color: control.kind === "command" || control.selected || control.hovered ? Theme.text : Theme.textMuted
                elide: Text.ElideRight
            }
            Label {
                visible: control.path.length > 0
                width: parent.width
                text: control.path.join("  ›  ")
                font.family: Theme.serif
                font.italic: true
                font.pixelSize: 12
                lineHeight: 16
                color: Theme.textMuted
                elide: Text.ElideRight
            }
        }
        Row {
            id: tailRow
            spacing: Theme.space2
            anchors.verticalCenter: parent.verticalCenter
            Label { visible: control.enterText !== "" && control.selected; text: control.enterText; font.pixelSize: 10; color: Theme.textMuted; anchors.verticalCenter: parent.verticalCenter }
            KeyCaps { keys: control.keys; ink: Theme.textFaint; anchors.verticalCenter: parent.verticalCenter }
        }
    }

    background: Rectangle {
        radius: Theme.radiusXs
        color: control.selected || control.hovered ? Theme.surfaceRaised : "transparent"
        Behavior on color { ColorAnimation { duration: Theme.durFast } }
        Label {
            x: control.selected ? 9 : 5
            anchors.verticalCenter: parent.verticalCenter
            text: ">"
            font.weight: Font.DemiBold
            color: Theme.accentText
            opacity: control.selected ? 1 : 0
            Behavior on opacity { NumberAnimation { duration: Theme.durFast } }
            Behavior on x { NumberAnimation { duration: Theme.durFast } }
        }
    }
}
