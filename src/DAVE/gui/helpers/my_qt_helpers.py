def combobox_update_items(combobox, items):
    """Updates the items of the combobox while maintaining the current text if possible"""
    cur = combobox.currentText()
    combobox.clear()
    combobox.addItems(items)
    combobox.setCurrentText(cur)

"""
Example:

    self.eventFilter = CtrlEnterKeyPressFilter()
    self.eventFilter.callback = self.run_code_in_teCode

    self.ui.teCode.installEventFilter(self.eventFilter)

"""

import PySide2.QtCore
import PySide2.QtGui
from PySide2.QtCore import Qt

class DeleteEventFilter(PySide2.QtCore.QObject):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.callback = None

    def eventFilter(self, obj, event):

        if isinstance(event, PySide2.QtGui.QKeyEvent):

            if (event.key() == Qt.Key_Delete):
                if event.type() == PySide2.QtCore.QEvent.KeyPress:
                    if self.callback is None:
                        print('Callback not set')
                    else:
                        self.callback()
                        return True

                    event.setAccepted(True)
                    return True

        return False