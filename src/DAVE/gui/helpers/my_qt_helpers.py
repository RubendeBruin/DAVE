
import PySide2.QtCore
import PySide2.QtGui
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QComboBox, QWidget


class BlockSigs():
    """Little helper class to pause rendering and refresh using with(...)

    with(DelayRenderingTillDone(Viewport):
        do_updates


    Creates an attribute _DelayRenderingTillDone_lock on the parent viewport to
    keep this action exclusive to the first caller.

    """
    def __init__(self, widget : QWidget):
        self.widget = widget

    def __enter__(self):
        self.remember = self.widget.signalsBlocked()
        self.widget.blockSignals(True)

    def __exit__(self, *args, **kwargs):
        self.widget.blockSignals(self.remember)


def combobox_update_items(combobox : QComboBox, items, doBlock=True):
    """Updates the items of the combobox while maintaining the current text if possible"""

    blocked = combobox.signalsBlocked()
    if doBlock:
        combobox.blockSignals(True)
    cur = combobox.currentText()
    combobox.clear()
    combobox.addItems(items)
    combobox.setCurrentText(cur)

    if doBlock:
        combobox.blockSignals(blocked)

"""
Example:

    self.eventFilter = CtrlEnterKeyPressFilter()
    self.eventFilter.callback = self.run_code_in_teCode

    self.ui.teCode.installEventFilter(self.eventFilter)

"""


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