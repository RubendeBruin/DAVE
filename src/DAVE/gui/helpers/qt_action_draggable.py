"""This is a draggable QWidgetAction that can be used in a QMenu.

It is specifically designed to be used in the DAVE GUI in combination with selecting nodes.

Clicked will fire if a node is clicked.
The menu will be closed only if the shift or control key is NOT down.


"""
from PySide6.QtGui import QDrag
from PySide6.QtWidgets import QApplication, QMenu, QWidgetAction, QPushButton, QHBoxLayout, QWidget, QLabel
from PySide6.QtCore import Qt, QMimeData, Signal


# Class wrapping a menu item

class QDraggableNodeActionWidget(QWidgetAction):


    def __init__(self, text = "", mime_text = None):

        self.startPos = None

        QWidgetAction.__init__(self, None)
        self.text = text

        if mime_text is None:
            mime_text = text

        self.mime_text = mime_text

        self.label = QLabel()
        self.label.setText(self.text)

        self.label.mouseMoveEvent = self.mouseMoveEvent
        self.label.mousePressEvent = self.mousePressEvent
        self.label.mouseReleaseEvent = self.mouseReleaseEvent

        self.setDefaultWidget(self.label)

    @Signal
    def clicked(self):
        pass

    def mouseReleaseEvent(self, event):
        self.clicked.emit()

        # if the shift or control key is NOT down, close the menu
        if not (event.modifiers() & Qt.ShiftModifier or event.modifiers() & Qt.ControlModifier):
            self.triggered.emit()  # close the menu

    def mousePressEvent(self, event):
        self.startPos = event.position()

    def mouseMoveEvent(self, event):
        if self.startPos is None:
            return
        if event.buttons() != Qt.LeftButton:
            return
        if (event.position() - self.startPos).manhattanLength() < QApplication.startDragDistance():
            return
        drag = QDrag(self)
        data = QMimeData()
        data.setText(self.mime_text)
        drag.setMimeData(data)
        drag.setPixmap(self.label.pixmap())
        drag.exec()

    def setBold(self, bold):
        if bold:
            self.label.setStyleSheet('font-weight: bold')
        else:
            self.label.setStyleSheet('font-weight: normal')


if __name__ == '__main__':

    app = QApplication()
    menu = QMenu()
    demo = QDraggableNodeActionWidget("Drag me or click me", "mime_text")
    demo.clicked.connect(lambda: print('clicked'))

    a = menu.addAction("Other action")


    menu.addAction(demo)
    menu.exec()
