// Text that rolls when it changes: the new value comes up from below while the old one leaves
// upwards (downwards when `rising` is false). For figures that change in place: the meters of the
// bar, the clock of the lock screen.
//   Ticker { text: Math.round(cpu * 100) + "%"; textStyle: "caption" }
import QtQuick

Item {
    id: root

    property string text
    property string textStyle: "body"
    property color color: Theme.text
    property int weight: -1
    /// The direction of the roll: true moves up (a larger value, a later time)
    property bool rising: true

    readonly property var s: Theme.styles[textStyle] || Theme.styles.body
    /// A large serif sets its first line in a box taller than its line height: the ticker keeps to
    /// the line height, with the figures in its middle, so stacked tickers sit as close as lines do
    readonly property real rest: (s.lineHeight - now.implicitHeight) / 2

    implicitWidth: now.implicitWidth
    implicitHeight: s.lineHeight
    clip: true
    Behavior on implicitWidth { NumberAnimation { duration: Theme.durFast; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeOut } }

    onTextChanged: {
        if (now.text === root.text) return
        before.text = now.text
        now.text = root.text
        if (before.text !== "") roll.restart()
    }
    Component.onCompleted: now.text = root.text

    Label {
        id: before
        textStyle: root.textStyle
        color: root.color
        font.weight: root.weight >= 0 ? root.weight : s.weight
        y: root.rest
        opacity: 0
    }
    Label {
        id: now
        textStyle: root.textStyle
        color: root.color
        font.weight: root.weight >= 0 ? root.weight : s.weight
        y: root.rest
    }

    ParallelAnimation {
        id: roll
        readonly property real distance: (root.rising ? 1 : -1) * root.height * 0.8
        NumberAnimation { target: before; property: "y"; from: root.rest; to: root.rest - roll.distance; duration: Theme.durSlow; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeOut }
        NumberAnimation { target: before; property: "opacity"; from: 1; to: 0; duration: Theme.durBase; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeIn }
        NumberAnimation { target: now; property: "y"; from: root.rest + roll.distance; to: root.rest; duration: Theme.durSlow; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeOut }
        NumberAnimation { target: now; property: "opacity"; from: 0; to: 1; duration: Theme.durSlow; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeOut }
    }
}
