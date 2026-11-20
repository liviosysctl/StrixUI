// One setting per row: a bold title, one line that says what it does, the control at the right.
//   SettingRow { title: "Change theme"; text: "Every 10 minutes"; Switch { checked: true } }
import QtQuick

Item {
    id: root

    property string title
    property string text
    property bool last: false
    default property alias control: slot.data

    implicitWidth: 480
    // A multiple of 4: at a scale of 125 %, 150 % or 175 % the rows of a page then start on whole
    // pixels of the screen, and the hairlines under them are all equally thin
    implicitHeight: Math.ceil((Math.max(words.implicitHeight, slot.childrenRect.height) + 20) / 4) * 4

    Column {
        id: words
        anchors.verticalCenter: parent.verticalCenter
        width: parent.width - slot.childrenRect.width - Theme.space5
        Label { width: parent.width; text: root.title; textStyle: "label"; elide: Text.ElideRight }
        Label { width: parent.width; visible: root.text !== ""; text: root.text; textStyle: "caption"; color: Theme.textMuted; wrapMode: Text.WordWrap }
    }

    Item {
        id: slot
        anchors.right: parent.right
        anchors.verticalCenter: parent.verticalCenter
        width: childrenRect.width
        height: childrenRect.height
    }

    Rectangle {
        visible: !root.last
        anchors.bottom: parent.bottom
        width: parent.width
        height: Theme.lineHair
        color: Theme.border
    }
}
