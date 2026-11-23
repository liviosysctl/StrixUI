// A hair line between groups of a Menu.
import QtQuick
import QtQuick.Templates as T

T.MenuSeparator {
    implicitWidth: 184
    implicitHeight: Theme.space2 + Theme.lineHair
    padding: 0
    topPadding: Theme.space1
    bottomPadding: Theme.space1
    contentItem: Rectangle { implicitHeight: Theme.lineHair; color: Theme.border }
}
