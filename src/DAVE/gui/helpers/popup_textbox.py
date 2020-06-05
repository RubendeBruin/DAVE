from PySide2.QtWidgets import QApplication, QMenu, QWidgetAction, QLineEdit
from PySide2.QtCore import Qt, QPoint
import PySide2
import PySide2.QtGui

def get_text(suggestion = '', pos = QPoint(100,100), input_valid_callback = None):

    menu = QMenu()

    class EnterKeyPressFilter(PySide2.QtCore.QObject):

        def eventFilter(self, obj, event):
            if isinstance(event, PySide2.QtGui.QKeyEvent):
                if (event.key() == Qt.Key_Return):
                    self.ok = True
                    self.callback()

            return False

    lb = QWidgetAction(None)
    le = QLineEdit()

    def done():
        menu.close()

    def check_input():
        if input_valid_callback:
            result = input_valid_callback(le.text())
            if result:
                le.setStyleSheet('')
            else:
                le.setStyleSheet('background: pin')



    le.textEdited.connect(check_input)
    eventFilter = EnterKeyPressFilter()
    eventFilter.callback = done
    eventFilter.ok = False
    le.installEventFilter(eventFilter)

    lb.setDefaultWidget(le)

    menu.addAction(lb)

    le.setText(suggestion)
    le.setFocus()
    le.selectAll()
    menu.exec_(pos)

    if eventFilter.ok:
        return le.text()
    else:
        return None

if __name__ == "__main__":

    app = QApplication()

    def valid(text):
        if text=='no':
            return False
        else:
            return True

    print(get_text(input_valid_callback=valid, suggestion = 'type name here'))
