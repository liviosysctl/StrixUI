// A message from the system or an app, top right under the bar.
// urgency "critical": the frame turns to the accent and a hair line drains along the bottom.
import QtQuick

Surface {
    id: root

    property string iconName: "bell"
    property string title
    property string body
    property string time
    property string urgency: "normal"
    /// Labels of up to two actions; action(index) fires when one is pressed.
    property var actions: []
    /// How long the critical line takes to drain, in milliseconds.
    property int timeout: 8000

    signal action(int index)
    signal dismissed()

    implicitWidth: 300
    implicitHeight: col.implicitHeight + 2 * Theme.space2
    elevation: "panel"
    borderColor: urgency === "critical" ? Theme.accent : Theme.border
    clip: true

    // The symbol plays its motion once when the message has slid in (the bell rings), and again under the pointer.
    Icon {
        id: symbol
        x: Theme.space3
        y: Theme.space2 + 3
        name: root.iconName
        hovered: here.hovered
        size: 12
        color: root.urgency === "critical" ? Theme.accentText : Theme.textMuted
    }

    HoverHandler { id: here }
    Timer { interval: Theme.durSlow; running: true; onTriggered: if (!Theme.reducedMotion) symbol.play() }

    Column {
        id: col
        x: Theme.space3 + 12 + Theme.space2
        y: Theme.space2
        width: parent.width - x - Theme.space3 - stamp.implicitWidth - Theme.space2
        Label { width: parent.width; text: root.title; textStyle: "label"; elide: Text.ElideRight }
        Label { width: parent.width; text: root.body; textStyle: "caption"; color: Theme.textMuted; wrapMode: Text.WordWrap; maximumLineCount: 3; elide: Text.ElideRight }
        Row {
            visible: root.actions.length > 0
            spacing: Theme.space2
            topPadding: 6
            bottomPadding: 2
            Repeater {
                model: root.actions
                Button { small: true; text: modelData; variant: index === 0 ? "default" : "quiet"; onClicked: root.action(index) }
            }
        }
    }

    Label {
        id: stamp
        anchors.right: parent.right
        anchors.rightMargin: Theme.space3
        y: Theme.space2
        text: root.time
        font.pixelSize: 10
        color: Theme.textFaint
    }

    Rectangle {
        visible: root.urgency === "critical"
        anchors.bottom: parent.bottom
        height: Theme.lineHair
        color: Theme.accent
        width: parent.width
        NumberAnimation on width {
            running: root.urgency === "critical" && root.visible
            from: root.width
            to: 0
            duration: root.timeout
        }
    }
}
