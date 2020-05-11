from PySide2.QtWidgets import QApplication, QMenu, QWidgetAction, QSlider, QHBoxLayout, QWidget, QLabel
from PySide2.QtCore import Qt

# Class wrapping a menu item

class MenuSlider(QWidgetAction):

    def __init__(self, text=""):
        QWidgetAction.__init__(self, None)

        self.widget = QWidget(None)
        self.layout = QHBoxLayout()
        self.slider = QSlider()
        self.slider.setOrientation(Qt.Horizontal)
        self.label = QLabel()
        self.label.setText(text)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.slider)
        self.widget.setLayout(self.layout)

        self.setDefaultWidget(self.widget)

    def connectvalueChanged(self, callback):
        self.slider.valueChanged.connect(callback)

    def value(self):
        return self.slider.value()

    def setMin(self, val):
        self.slider.setMinimum(val)

    def setMax(self, val):
        self.slider.setMaximum(val)


if __name__ == "__main__":
    app = QApplication()
    menu = QMenu()
    demo = MenuSlider("Demo slider")
    demo.setMin(-1)


    def cb(value):
        print(value)
        # print(demo.value())
        # demo.label.setText(str(demo.value()))


    demo.connectvalueChanged(cb)

    menu.addAction("test")
    menu.addAction(demo)

    # Insert a custom widget into the menu

    lb = QWidgetAction(None)
    lbl = QLabel('Static text')
    lb.setDefaultWidget(lbl)

    menu.addAction(lb)

    menu.exec_()