// The selection that glides from row to row instead of jumping: the raised ground and the accent
// line of a selected ListRow or SearchHit. Rows with `glide: true` leave that look to it.
// As the highlight of a ListView it is moved by the view; elsewhere it follows `target`.
//   ListView { highlight: Glide {}; highlightMoveDuration: Theme.durBase; highlightMoveVelocity: -1 }
//   Glide { target: rows.itemAt(current) }
import QtQuick

Rectangle {
    id: root

    /// The row to sit under; leave empty as the highlight of a ListView
    property Item target: null

    x: target ? target.x : 0
    y: target ? target.y : 0
    width: target ? target.width : (parent ? parent.width : 0)
    height: target ? target.height : 0
    visible: !target || target.visible
    radius: Theme.radiusMd
    color: Theme.surfaceRaised

    Behavior on y { enabled: !!root.target; NumberAnimation { duration: Theme.durBase; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeOut } }
    Behavior on height { enabled: !!root.target; NumberAnimation { duration: Theme.durBase; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeOut } }
    // The line stretches into the move and settles
    onYChanged: if (!stretch.running) stretch.restart()

    Rectangle {
        id: mark
        anchors.verticalCenter: parent.verticalCenter
        width: Theme.lineBold
        height: Theme.icon
        radius: width / 2
        color: Theme.accent
    }
    SequentialAnimation {
        id: stretch
        NumberAnimation { target: mark; property: "height"; to: Theme.icon + Theme.space2; duration: Theme.durInstant; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeIn }
        NumberAnimation { target: mark; property: "height"; to: Theme.icon; duration: Theme.durBase; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeSpring }
    }
}
