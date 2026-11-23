// The tall slanted card of the theme picker: the god's engraving cut as a parallelogram.
// selected: it comes to full light and shows the name in serif italic with a caption.
// lift, from 0 to 1, is how far it has widened into the chosen card. It follows `selected` at once;
// a carousel binds it to its own position, so all its cards move as one however fast it is turned.
import QtQuick
import QtQuick.Shapes

Item {
    id: root

    property url source
    property string name
    property string caption
    property color accent: Theme.accent
    property bool selected: false
    property real lift: selected ? 1 : 0
    readonly property int skew: 40
    readonly property int narrow: 96
    readonly property int wide: 420

    signal clicked()

    width: narrow + (wide - narrow) * lift
    height: 220 + 30 * lift

    // The engraving cropped to the card around its middle, where the god stands. The shape fills
    // with this layer: an Image alone would hand over its whole picture unscaled, and a narrow
    // card would show only its dark corner.
    Item {
        id: art
        anchors.fill: parent
        visible: false
        layer.enabled: true
        layer.smooth: true
        Image {
            anchors.fill: parent
            source: root.source
            fillMode: Image.PreserveAspectCrop
            asynchronous: true
        }
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
            strokeColor: Theme.alpha(Theme.line, 0.7 * root.lift)
            strokeWidth: Theme.lineHair
            PathPolyline { path: [Qt.point(root.skew + 0.5, 0.5), Qt.point(root.width - 0.5, 0.5), Qt.point(root.width - root.skew - 0.5, root.height - 0.5), Qt.point(0.5, root.height - 0.5), Qt.point(root.skew + 0.5, 0.5)] }
        }
        // the veil of cards that are not chosen: darker, but the god stays to be seen
        ShapePath {
            fillColor: Qt.rgba(0, 0, 0, (hover.hovered ? 0.2 : 0.4) * (1 - root.lift))
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
        // The name comes once the card is more than half open
        opacity: Math.max(0, 2 * root.lift - 1)
        Label { anchors.horizontalCenter: parent.horizontalCenter; text: root.name; textStyle: "emblem"; color: Theme.accentText }
        Row {
            anchors.horizontalCenter: parent.horizontalCenter
            spacing: Theme.space2
            Rectangle { width: Theme.space1; height: Theme.space1; radius: width / 2; color: root.accent; anchors.verticalCenter: parent.verticalCenter }
            // Inside the slanted edges: a long caption ends in an ellipsis instead of running out of the card
            Label { text: root.caption; textStyle: "note"; color: Theme.textMuted
                width: Math.min(implicitWidth, root.width - 2 * root.skew - 2 * Theme.space4); elide: Text.ElideRight }
        }
    }
}
