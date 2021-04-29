from PySide2.QtWidgets import QApplication, QMenu, QWidgetAction, QLineEdit, QWidget,QHBoxLayout, QPushButton
from PySide2.QtCore import Qt, QPoint
import PySide2
import PySide2.QtGui


class EnterKeyPressFilter(PySide2.QtCore.QObject):

    def eventFilter(self, obj, event):
        if isinstance(event, PySide2.QtGui.QKeyEvent):
            if (event.key() == Qt.Key_Return):
                self.callback()

        return False




class TextInput():

    def __init__(self, suggestion='', input_valid_callback = None):

        self.input_valid_callback = input_valid_callback

        self.menu = QMenu()

        self.lb = QWidgetAction(None)

        self.widget = QWidget(None)
        self.layout = QHBoxLayout()
        self.button = QPushButton()
        self.button.setText("Ok")
        self.le = QLineEdit()

        self.layout.addWidget(self.le)
        self.layout.addWidget(self.button)
        self.widget.setLayout(self.layout)

        self.button.clicked.connect(self.done)

        self.le.textEdited.connect(self.check_input)
        self.eventFilter = EnterKeyPressFilter()
        self.eventFilter.callback = self.done
        self.le.installEventFilter(self.eventFilter)

        self.lb.setDefaultWidget(self.widget)

        self.menu.addAction(self.lb)

        self.le.setText(suggestion)
        self.le.setFocus()
        self.le.selectAll()

        self.result = None

    def show(self, pos):
        self.menu.exec_(pos)
        return self.result

    def done(self):
        self.result = self.le.text()
        self.menu.close()

    def check_input(self):
        if self.input_valid_callback is not None:
            result = self.input_valid_callback(self.le.text())
            if result:
                self.le.setStyleSheet('')
            else:
                self.le.setStyleSheet('background: pink')



        return None

def get_text(suggestion = '', pos = QPoint(100,100), input_valid_callback = None):
    a = TextInput(suggestion=suggestion, input_valid_callback=input_valid_callback)
    return a.show(pos)



if __name__ == "__main__":

    app = QApplication()

    def valid(text):
        if text=='no':
            return False
        else:
            return True

    print(get_text(input_valid_callback=valid, suggestion = 'type name here'))
