// Actions for the thing under the pointer. Fill it with MenuItem and MenuSeparator; open it with popup().
import QtQuick
import QtQuick.Templates as T

T.Menu {
    id: control

    implicitWidth: Math.max(190, contentItem.implicitWidth + leftPadding + rightPadding)
    implicitHeight: contentItem.implicitHeight + topPadding + bottomPadding
    padding: 3
    margins: 0
    transformOrigin: Item.TopLeft

    enter: Transition {
        ParallelAnimation {
            NumberAnimation { property: "opacity"; from: 0; to: 1; duration: Theme.durFast; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeOut }
            NumberAnimation { property: "scale"; from: 0.98; to: 1; duration: Theme.durFast; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeOut }
        }
    }
    exit: Transition { NumberAnimation { property: "opacity"; to: 0; duration: Theme.durInstant } }

    delegate: MenuItem {}

    contentItem: ListView {
        implicitHeight: contentHeight
        implicitWidth: 184
        model: control.contentModel
        interactive: false
        clip: true
        currentIndex: control.currentIndex
    }

    background: Surface {
        implicitWidth: 190
        elevation: "pop"
    }
}
