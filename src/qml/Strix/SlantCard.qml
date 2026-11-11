// The tall slanted card of the theme picker: the god's engraving cut as a parallelogram.
// selected: it widens, comes to full light and shows the name in blackletter with a caption.
import QtQuick
import QtQuick.Shapes

Item {
    id: root

    property url source
    property string name
    property string caption
    property color accent: Theme.accent
    property bool selected: false
    readonly property int skew: 40

    signal clicked()

    width: selected ? 420 : 96
    height: selected ? 250 : 220
    Behavior on width { NumberAnimation { duration: Theme.durSlow; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeInOut } }
    Behavior on height { NumberAnimation { duration: Theme.durSlow; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeInOut } }

    Image {
        id: art
        anchors.fill: parent
        source: root.source
        fillMode: Image.PreserveAspectCrop
        visible: false
    }

    Shape {
        anchors.fill: parent
        preferredRendererType: Shape.CurveRenderer
        ShapePath {
            fillItem: art
            strokeColor: "transparent"
            PathPolyline { path: [Qt.point(root.skew, 0), Qt.point(root.width, 0), Qt.point(root.width - root.skew, root.height), Qt.point(0, root.height), Qt.point(root.skew, 0)] }
        }
        // the cream edge of the selected card
        ShapePath {
            fillColor: "transparent"
            strokeColor: Theme.alpha(Theme.line, root.selected ? 0.7 : 0)
            strokeWidth: Theme.lineHair
            PathPolyline { path: [Qt.point(root.skew + 0.5, 0.5), Qt.point(root.width - 0.5, 0.5), Qt.point(root.width - root.skew - 0.5, root.height - 0.5), Qt.point(0.5, root.height - 0.5), Qt.point(root.skew + 0.5, 0.5)] }
        }
        // the dark veil of cards that are not chosen
        ShapePath {
            fillColor: Qt.rgba(0, 0, 0, root.selected ? 0 : hover.hovered ? 0.4 : 0.6)
            strokeColor: "transparent"
            PathPolyline { path: [Qt.point(root.skew, 0), Qt.point(root.width, 0), Qt.point(root.width - root.skew, root.height), Qt.point(0, root.height), Qt.point(root.skew, 0)] }
        }
    }

    HoverHandler { id: hover; cursorShape: Qt.PointingHandCursor }
    TapHandler { onTapped: root.clicked() }

    Column {
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottom: parent.bottom
        anchors.bottomMargin: Theme.space5
        opacity: root.selected ? 1 : 0
        Behavior on opacity { NumberAnimation { duration: Theme.durBase } }
        Label { anchors.horizontalCenter: parent.horizontalCenter; text: root.name; font.family: Theme.fraktur; font.pixelSize: 46; font.weight: Font.Light; lineHeight: 44 }
        Row {
            anchors.horizontalCenter: parent.horizontalCenter
            spacing: 6
            Rectangle { width: 6; height: 6; radius: 3; color: root.accent; anchors.verticalCenter: parent.verticalCenter }
            Label { text: root.caption; font.family: Theme.serif; font.italic: true; font.pixelSize: 13; font.letterSpacing: 1.8; lineHeight: 16; color: Theme.textMuted }
        }
    }
}
