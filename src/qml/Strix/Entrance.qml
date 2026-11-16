// Lets the item it sits in arrive: it rises a few pixels and fades in after `delay`. Neighbours
// with growing delays (Theme.stagger apart) come in one after the other.
//   Label { text: "09"; Entrance { delay: 2 * Theme.stagger } }
//   Entrance { target: field }   for an item whose children go elsewhere (TextField)
import QtQuick

Item {
    id: root

    /// The item that arrives: the one it sits in, unless set
    property Item target: parent
    property int delay: 0
    property real distance: 10
    property int duration: Theme.durSlow
    /// Arrive as soon as the item is made; play() arrives again
    property bool auto: true

    function play() {
        if (!root.target) return
        root.target.transform = [shift]
        arrive.restart()
    }

    visible: false
    Component.onCompleted: if (root.auto) root.play()

    Translate { id: shift }

    SequentialAnimation {
        id: arrive
        PropertyAction { target: root.target; property: "opacity"; value: 0 }
        PropertyAction { target: shift; property: "y"; value: root.distance }
        PauseAnimation { duration: Math.max(1, root.delay) }
        ParallelAnimation {
            NumberAnimation { target: root.target; property: "opacity"; to: 1; duration: root.duration; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeOut }
            NumberAnimation { target: shift; property: "y"; to: 0; duration: root.duration; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeOut }
        }
    }
}
