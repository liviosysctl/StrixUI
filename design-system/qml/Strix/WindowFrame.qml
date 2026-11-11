// How a window looks. Hyprland draws the frame of ordinary windows; use this for windows the shell
// draws itself and for previews. titleBar: an app title bar with minimise, maximise and close.
import QtQuick

Item {
    id: root

    property string title
    property string subtitle
    property bool active: true
    property bool titleBar: true
    default property alias content: body.data

    signal minimise()
    signal maximise()
    signal close()

    implicitWidth: 480
    implicitHeight: 260
    opacity: active ? 1 : Theme.dimInactive
    Behavior on opacity { NumberAnimation { duration: Theme.durBase } }

    Surface {
        anchors.fill: parent
        elevation: "window"
        borderColor: root.active ? Theme.borderActive : Theme.border
        Behavior on borderColor { ColorAnimation { duration: Theme.durSlow; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeInOut } }
        clip: true

        Item {
            id: bar
            visible: root.titleBar
            width: parent.width
            height: visible ? 26 : 0
            Row {
                x: Theme.space3
                anchors.verticalCenter: parent.verticalCenter
                spacing: Theme.space2
                Label { text: root.title; font.family: Theme.serif; font.pixelSize: 15; lineHeight: 18; anchors.verticalCenter: parent.verticalCenter }
                Label { text: root.subtitle; textStyle: "caption"; color: Theme.textMuted; anchors.verticalCenter: parent.verticalCenter }
            }
            Row {
                anchors.right: parent.right
                Repeater {
                    model: [["minus", "minimise"], ["square", "maximise"], ["x", "close"]]
                    Rectangle {
                        width: 40
                        height: 26
                        color: hh.hovered ? (modelData[1] === "close" ? Theme.accent : Theme.surfaceRaised) : "transparent"
                        HoverHandler { id: hh }
                        TapHandler { onTapped: root[modelData[1]]() }
                        Icon {
                            anchors.centerIn: parent
                            name: modelData[0]
                            size: 10
                            color: hh.hovered ? (modelData[1] === "close" ? Theme.onAccent : Theme.text) : Theme.textMuted
                        }
                    }
                }
            }
            Rectangle { anchors.bottom: parent.bottom; width: parent.width; height: Theme.lineHair; color: Theme.border }
        }

        Item {
            id: body
            anchors.top: bar.bottom
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            anchors.margins: Theme.space3
            anchors.leftMargin: Theme.space4
            anchors.rightMargin: Theme.space4
        }
    }
}
