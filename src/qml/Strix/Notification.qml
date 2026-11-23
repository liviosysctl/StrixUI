// A message from the system or an app, top right under the bar.
// urgency "critical": the frame turns to the accent and a hair line drains along the bottom.
// A click anywhere on it, except on one of its actions, sends it away (dismissed); under the pointer the
// name of the app gives way to an x that says so.
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

    implicitWidth: 320
    implicitHeight: col.implicitHeight + 2 * Theme.space3
    elevation: "panel"
    borderColor: urgency === "critical" ? Theme.accent : Theme.glassEdge
    clip: true

    // The symbol plays its motion once when the message has slid in (the bell rings), and again under the pointer.
    Icon {
        id: symbol
        x: Theme.space3
        y: Theme.space3 + (Theme.styles.label.lineHeight - Theme.icon) / 2
        name: root.iconName
        hovered: here.hovered
        color: root.urgency === "critical" ? Theme.accentText : Theme.textMuted
    }

    HoverHandler { id: here; cursorShape: Qt.PointingHandCursor }
    TapHandler {
        onTapped: point => {
            const at = buttons.mapFromItem(root, point.position)
            if (!buttons.visible || !buttons.contains(at)) root.dismissed()
        }
    }
    Timer { interval: Theme.durSlow; running: true; onTriggered: if (!Theme.reducedMotion) symbol.play() }

    Column {
        id: col
        x: Theme.space3 + Theme.icon + Theme.space2
        y: Theme.space3
        width: parent.width - x - Theme.space3 - stamp.implicitWidth - Theme.space2
        Label { width: parent.width; text: root.title; textStyle: "label"; elide: Text.ElideRight }
        Label { width: parent.width; text: root.body; textStyle: "caption"; color: Theme.textMuted; wrapMode: Text.WordWrap; maximumLineCount: 3; elide: Text.ElideRight }
        Row {
            id: buttons
            visible: root.actions.length > 0
            spacing: Theme.space2
            topPadding: Theme.space2
            Repeater {
                model: root.actions
                Button { text: modelData; variant: index === 0 ? "default" : "quiet"; onClicked: root.action(index) }
            }
        }
    }

    Label {
        id: stamp
        anchors.right: parent.right
        anchors.rightMargin: Theme.space3
        y: Theme.space3
        text: root.time
        textStyle: "micro"
        color: Theme.textFaint
        opacity: here.hovered ? 0 : 1
        Behavior on opacity { NumberAnimation { duration: Theme.durFast } }
    }
    Icon {
        anchors.right: parent.right
        anchors.rightMargin: Theme.space3
        y: Theme.space3 + (Theme.styles.label.lineHeight - Theme.icon) / 2
        name: "x"
        tinted: false
        color: Theme.text
        opacity: here.hovered ? 1 : 0
        Behavior on opacity { NumberAnimation { duration: Theme.durFast } }
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
