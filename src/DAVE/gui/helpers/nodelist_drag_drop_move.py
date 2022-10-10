from PySide2.QtCore import QMimeData
from PySide2.QtGui import QDrag
from PySide2 import QtCore
from PySide2.QtWidgets import QApplication, QListWidget, QWidget, QVBoxLayout, QLabel


def call_from_drop_Event(list_widget, event):
    list = list_widget

    # dropping onto something?
    point = event.pos()
    drop_onto = list.itemAt(point)

    if drop_onto:
        row = list.row(drop_onto)
    else:
        row = -1

    if event.source() == list:
        item = list.currentItem()
        name = item.text()
        delrow = list.row(item)
        list.takeItem(delrow)
    else:
        name = event.mimeData().text()

    if row >= 0:
        list.insertItem(row, name)
    else:
        list.addItem(name)

def call_from_dragEnterEvent(list_widget, scene, allowed_nodetypes, event):
    if event.source() == list_widget:
        event.accept()
    else:
        try:
            name = event.mimeData().text()
            print(f'receiving {name}')
            node = scene[name]
            if isinstance(node, allowed_nodetypes):
                event.accept()
                print('accepted')
        except:
            return


if __name__ == '__main__':
    app = QApplication()

    widget = QWidget()
    layout = QVBoxLayout()

    from DAVE import Scene, Point, Circle

    scene = Scene()

    scene.new_point('test')

    list = QListWidget()
    label = QLabel("Drag me out!")

    layout.addWidget(label)
    layout.addWidget(list)

    widget.setLayout(layout)

    widget.show()

    list.setDragEnabled(True)
    list.setAcceptDrops(True)
    list.setDragEnabled(True)

    def mousePressed(event):
        data = QMimeData()
        data.setText("test")
        drag = QDrag(label)
        drag.setMimeData(data)
        drag.start(QtCore.Qt.MoveAction)


    label.mousePressEvent = mousePressed

    def drag(*args):
        call_from_dragEnterEvent(list, scene, (Point, Circle), *args)
        print('Regenerate code')
    def drop(*args):
        call_from_drop_Event(list, *args)
        print('Regenerate code')

    list.dragEnterEvent = drag
    list.dropEvent = drop

    list.addItems(["One","Two","Three"])

    app.exec_()