import PySide2
from PySide2.QtWidgets import QGraphicsPolygonItem

"""Assing .callback and/or .callback_doubleclick to handle events"""

class ClickablePolygonItem(QGraphicsPolygonItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.callback = None
        self.callback_doubleclick = None

    def mousePressEvent(self, event):

        if event.type() == PySide2.QtCore.QEvent.Type.GraphicsSceneMousePress:
            if self.callback is not None:
                self.callback(self)
        if event.type() == PySide2.QtCore.QEvent.Type.GraphicsSceneMouseDoubleClick:
            if self.callback_doubleclick is not None:
                self.callback_doubleclick(self)

if __name__ == '__main__':
    import PySide2
    from PySide2 import QtWidgets
    from PySide2.QtCore import Qt, QPointF
    from PySide2.QtGui import QBrush, QPen, QPolygonF, QPalette
    from PySide2.QtWidgets import QDialog, QApplication, QGraphicsView, QVBoxLayout, QGraphicsScene, \
        QGraphicsPolygonItem

    a = QApplication()
    d = QDialog()

    gf = QGraphicsView()

    gray = d.palette

    gf.setBackgroundBrush(d.palette().brush(QPalette.ColorRole.Window))
    gf.setFrameShape(QtWidgets.QFrame.NoFrame)

    layout = QVBoxLayout()
    layout.addWidget(gf)
    d.setLayout(layout)

    green_brush = QBrush(Qt.green)
    yellow_brush = QBrush(Qt.yellow)
    blue_pen = QPen(Qt.blue)
    blue_pen.setWidth(4)

    scene = QGraphicsScene()


    # But can add a event items added in this way (without the convenience methods)
    p1 = QPointF(0, 0)
    p2 = QPointF(100, 100)
    p3 = QPointF(0, 200)
    p4 = QPointF(200, 200)
    p = QPolygonF([p1, p2, p3])

    poly = ClickablePolygonItem(p)
    poly.setBrush(green_brush)
    scene.addItem(poly)

    p = QPolygonF([p4, p2, p3])

    poly2 = ClickablePolygonItem(p)
    poly2.setBrush(green_brush)
    scene.addItem(poly2)


    def click(item):
        item.setBrush(yellow_brush)
        print('normal click ' + item.text)

    def dbl_click(item):
        item.setBrush(green_brush)
        print('double click ' + item.text)


    poly.callback = click
    poly.callback_doubleclick = dbl_click
    poly.text = 'poly 1'
    poly2.callback = click
    poly2.callback_doubleclick = dbl_click
    poly2.text = 'poly 2'

    gf.setScene(scene)
    bounding_rect = scene.sceneRect()
    gf.fitInView(bounding_rect)


    def update(event):
        gf.fitInView(bounding_rect)
        print('update')


    d.resizeEvent = update

    d.show()
    a.exec_()
