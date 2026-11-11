// A small accent dot: unread, recording. live: it breathes.
import QtQuick

Rectangle {
    property bool live: false

    implicitWidth: 5
    implicitHeight: 5
    radius: width / 2
    color: Theme.accent

    SequentialAnimation on opacity {
        running: parent && live
        loops: Animation.Infinite
        NumberAnimation { from: 1; to: 0.35; duration: Theme.durLoop; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeInOut }
        NumberAnimation { from: 0.35; to: 1; duration: Theme.durLoop; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeInOut }
    }
}
