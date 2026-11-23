// A load figure in the top bar: a thin upright bar that fills, the name and the value. The value
// rolls when it changes. Inside a Chip it is part of one button: bind `hot` to the chip's `lit`.
//   Meter { label: "CPU"; value: 0.08 }
import QtQuick

Row {
    id: root

    property string label
    property real value: 0
    property string valueText: Math.round(value * 100) + "%"
    /// Under the pointer (bound to the button that holds it): the bar takes the accent
    property bool hot: false

    /// Empty the bar and fill it again, after `delay` milliseconds
    function sweep(delay) {
        pause.duration = Math.max(1, delay || 0)
        fillAgain.restart()
    }

    /// The share of the value drawn, 0 to 1, for sweep()
    property real fill: 1

    spacing: Theme.space1

    Rectangle {
        width: Theme.lineBold
        height: Theme.space3
        radius: width / 2
        color: Theme.borderStrong
        anchors.verticalCenter: parent.verticalCenter
        Rectangle {
            anchors.bottom: parent.bottom
            width: parent.width
            height: parent.height * Math.max(0, Math.min(1, root.value)) * root.fill
            color: root.hot ? Theme.accent : Theme.text
            Behavior on height { enabled: !fillAgain.running; NumberAnimation { duration: Theme.durSlow; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeOut } }
            Behavior on color { ColorAnimation { duration: Theme.durFast } }
        }
    }
    Label { text: root.label; textStyle: "caption"; color: root.hot ? Theme.text : Theme.textMuted; anchors.verticalCenter: parent.verticalCenter; Behavior on color { ColorAnimation { duration: Theme.durFast } } }
    Ticker {
        id: figure
        text: root.valueText
        textStyle: "caption"
        weight: Font.Medium
        anchors.verticalCenter: parent.verticalCenter
        property real previous: root.value
        rising: root.value >= previous
        onTextChanged: previous = root.value
    }

    SequentialAnimation {
        id: fillAgain
        PropertyAction { target: root; property: "fill"; value: 0 }
        PauseAnimation { id: pause; duration: 1 }
        NumberAnimation { target: root; property: "fill"; to: 1; duration: Theme.durSlow; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeOut }
    }
}
