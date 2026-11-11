// A hair line; the done part in the accent. indeterminate: a short piece runs along it.
// With label or valueText it gets the line of text above it ("Downloading", "62%").
import QtQuick
import QtQuick.Templates as T

T.ProgressBar {
    id: control

    property string label
    property string valueText

    readonly property bool hasText: label !== "" || valueText !== ""

    implicitWidth: 240
    implicitHeight: hasText ? 16 + 6 + Theme.lineBold : Theme.lineBold

    contentItem: Item {
        Row {
            visible: control.hasText
            width: parent.width
            Label { textStyle: "caption"; color: Theme.textMuted; text: control.label; width: parent.width - v.width }
            Label { id: v; textStyle: "caption"; font.weight: Font.DemiBold; text: control.valueText }
        }
        Item {
            id: line
            anchors.bottom: parent.bottom
            width: parent.width
            height: Theme.lineBold
            clip: true
            Rectangle { y: 0.5; width: parent.width; height: Theme.lineHair; color: Theme.border }
            Rectangle {
                visible: !control.indeterminate
                width: control.visualPosition * parent.width
                height: parent.height
                color: Theme.accent
                Behavior on width { NumberAnimation { duration: Theme.durSlow; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeOut } }
            }
            Rectangle {
                id: piece
                visible: control.indeterminate
                width: parent.width * 0.18
                height: parent.height
                color: Theme.accent
                NumberAnimation on x {
                    running: control.indeterminate && control.visible
                    loops: Animation.Infinite
                    from: -piece.width * 1.1
                    to: piece.width * 5.6
                    duration: Theme.durLoop
                    easing.type: Easing.BezierSpline
                    easing.bezierCurve: Theme.easeInOut
                }
            }
        }
    }
}
