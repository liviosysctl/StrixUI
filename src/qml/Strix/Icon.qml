// A Lucide symbol as a vector path, drawn in a 1.25px line at any size: Icon { name: "power"; color: Theme.accentText }
import QtQuick
import QtQuick.Shapes

Item {
    id: root

    property string name
    property int size: 14
    property color color: Theme.textMuted
    /// Line width in pixels on screen.
    property real stroke: 1.25

    implicitWidth: size
    implicitHeight: size

    Shape {
        width: 24
        height: 24
        scale: root.size / 24
        transformOrigin: Item.TopLeft
        preferredRendererType: Shape.CurveRenderer

        ShapePath {
            strokeColor: root.color
            strokeWidth: root.stroke * 24 / root.size
            fillColor: "transparent"
            capStyle: ShapePath.RoundCap
            joinStyle: ShapePath.RoundJoin
            PathSvg { path: Icons.path(root.name) }
        }
    }
}
