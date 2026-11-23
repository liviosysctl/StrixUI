// What is playing: cover, title in serif italic, artist, the three controls and the position.
// With Quickshell, bind it to Mpris.players (Quickshell.Services.Mpris).
import QtQuick

Surface {
    id: root

    property string title
    property string artist
    property url cover
    property bool playing: false
    /// Position and length in seconds.
    property real position: 0
    property real length: 0

    signal previous()
    signal toggle()
    signal next()

    function clock(s) { s = Math.max(0, Math.floor(s)); return Math.floor(s / 60) + ":" + ("0" + s % 60).slice(-2) }

    implicitWidth: 320
    implicitHeight: 2 * Theme.space3 + art.height + Theme.space2 + Theme.control
    elevation: "panel"

    Rectangle {
        id: art
        x: Theme.space3
        y: Theme.space3
        width: Theme.space7
        height: Theme.space7
        radius: Theme.radiusMd
        color: Theme.surfaceRaised
        border.width: Theme.lineHair
        border.color: Theme.border
        clip: true
        Icon { anchors.centerIn: parent; visible: img.status !== Image.Ready; name: "music"; color: Theme.textFaint }
        Image { id: img; anchors.fill: parent; anchors.margins: Theme.lineHair; source: root.cover; fillMode: Image.PreserveAspectCrop }
    }

    Column {
        anchors.left: art.right
        anchors.leftMargin: Theme.space3
        anchors.right: parent.right
        anchors.rightMargin: Theme.space3
        anchors.verticalCenter: art.verticalCenter
        Label { width: parent.width; text: root.title; textStyle: "aside"; elide: Text.ElideRight }
        Label { width: parent.width; text: root.artist; textStyle: "caption"; color: Theme.textMuted; elide: Text.ElideRight }
    }

    Row {
        x: Theme.space3
        y: art.y + art.height + Theme.space2
        width: parent.width - 2 * Theme.space3
        spacing: Theme.space1
        IconButton { iconName: "skip-back"; onClicked: root.previous() }
        IconButton { iconName: root.playing ? "pause" : "play"; onClicked: root.toggle() }
        IconButton { iconName: "skip-forward"; onClicked: root.next() }
        Label { width: Theme.space6; horizontalAlignment: Text.AlignRight; text: root.clock(root.position); textStyle: "micro"; color: Theme.textFaint; anchors.verticalCenter: parent.verticalCenter }
        Item {
            width: parent.width - 3 * Theme.control - 2 * Theme.space6 - 5 * parent.spacing
            height: Theme.lineBold
            anchors.verticalCenter: parent.verticalCenter
            Rectangle { y: 0.5; width: parent.width; height: Theme.lineHair; color: Theme.border }
            Rectangle { width: root.length > 0 ? parent.width * root.position / root.length : 0; height: parent.height; color: Theme.accent }
        }
        Label { width: Theme.space6; text: root.clock(root.length); textStyle: "micro"; color: Theme.textFaint; anchors.verticalCenter: parent.verticalCenter }
    }
}
