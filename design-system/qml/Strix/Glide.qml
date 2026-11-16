// The selection that glides from row to row instead of jumping: the raised background and the
// accent caret of a selected ListRow or SearchHit. Rows with `glide: true` leave that look to it.
// As the highlight of a ListView it is moved by the view; elsewhere it follows `target`.
//   ListView { highlight: Glide {}; highlightMoveDuration: Theme.durBase; highlightMoveVelocity: -1 }
//   Glide { target: rows.itemAt(current); caretX: 7 }
import QtQuick

Rectangle {
    id: root

    /// The row to sit under; leave empty as the highlight of a ListView
    property Item target: null
    /// Where the caret sits: 9 for SearchHit, 7 for ListRow
    property real caretX: 9

    x: target ? target.x : 0
    y: target ? target.y : 0
    width: target ? target.width : (parent ? parent.width : 0)
    height: target ? target.height : 0
    visible: !target || target.visible
    radius: Theme.radiusXs
    color: Theme.surfaceRaised

    Behavior on y { enabled: !!root.target; NumberAnimation { duration: Theme.durBase; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeOut } }
    Behavior on height { enabled: !!root.target; NumberAnimation { duration: Theme.durBase; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeOut } }

    // The caret leans into the move: back a step, then home
    onYChanged: if (!nudge.running) nudge.restart()
    Label {
        id: caret
        x: root.caretX
        anchors.verticalCenter: parent.verticalCenter
        text: ">"
        font.weight: Font.DemiBold
        color: Theme.accentText
    }
    SequentialAnimation {
        id: nudge
        NumberAnimation { target: caret; property: "x"; to: root.caretX - 3; duration: Theme.durInstant; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeIn }
        NumberAnimation { target: caret; property: "x"; to: root.caretX; duration: Theme.durBase; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeSpring }
    }
}
