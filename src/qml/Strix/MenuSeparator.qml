// A hair line between groups of a Menu.
import QtQuick
import QtQuick.Templates as T

T.MenuSeparator {
    implicitWidth: 184
    implicitHeight: 7
    padding: 0
    contentItem: Rectangle { implicitHeight: Theme.lineHair; color: Theme.border }
}
