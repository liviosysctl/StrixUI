// A framed block with a serif title and one line of text. interactive: it lifts under the pointer.
import QtQuick

Rectangle {
    id: root

    property string title
    property string text
    property bool interactive: false
    default property alias content: extra.data
    signal clicked()

    implicitWidth: 240
    implicitHeight: col.implicitHeight + 2 * Theme.space3
    radius: Theme.radiusMd
    color: Theme.surface
    border.width: Theme.lineHair
    border.color: interactive && hover.hovered ? Theme.borderStrong : Theme.border
    transform: Translate { y: root.interactive && hover.hovered ? -2 : 0; Behavior on y { NumberAnimation { duration: Theme.durFast } } }
    Behavior on border.color { ColorAnimation { duration: Theme.durFast } }

    HoverHandler { id: hover; enabled: root.interactive; cursorShape: Qt.PointingHandCursor }
    TapHandler { enabled: root.interactive; onTapped: root.clicked() }

    Column {
        id: col
        x: Theme.space4
        y: Theme.space3
        width: parent.width - 2 * Theme.space4
        spacing: 2
        Label { visible: root.title !== ""; text: root.title; textStyle: "subtitle"; width: parent.width; elide: Text.ElideRight }
        Label { visible: root.text !== ""; text: root.text; textStyle: "caption"; color: Theme.textMuted; width: parent.width; wrapMode: Text.WordWrap }
        Item { id: extra; width: parent.width; implicitHeight: childrenRect.height; height: implicitHeight }
    }
}
