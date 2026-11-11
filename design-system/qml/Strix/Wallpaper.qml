// The engraving of a god, filling its parent. dim: darker and a little blurred, as under the lock
// screen and the theme picker. Without `source` it shows the wallpaper of the current theme.
import QtQuick
import QtQuick.Effects

Item {
    id: root

    property url source: Theme.wallpaper()
    property bool dim: false

    Rectangle { anchors.fill: parent; color: Theme.background }

    Image {
        id: img
        anchors.fill: parent
        source: root.source
        fillMode: Image.PreserveAspectCrop
        asynchronous: true
        visible: false
    }

    MultiEffect {
        anchors.fill: parent
        source: img
        scale: root.dim ? 1.02 : 1
        blurEnabled: true
        blurMax: 8
        blur: root.dim ? 3 / 8 : 0
        Behavior on blur { NumberAnimation { duration: Theme.durReveal; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeOut } }
        Behavior on scale { NumberAnimation { duration: Theme.durReveal; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeOut } }
    }

    // dim-wallpaper is a brightness factor: black over the image at 1 - factor multiplies it
    Rectangle {
        anchors.fill: parent
        color: "black"
        opacity: root.dim ? 1 - Theme.dimWallpaper : 0
        Behavior on opacity { NumberAnimation { duration: Theme.durReveal; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeOut } }
    }
}
