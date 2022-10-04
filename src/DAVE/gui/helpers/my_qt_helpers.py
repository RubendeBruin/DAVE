
import PySide2.QtCore
import PySide2.QtGui
from PySide2 import QtWidgets
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QComboBox, QWidget, QCompleter


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

class CustomEventFilters(PySide2.QtCore.QObject):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.callback = None


class DeleteEventFilter(CustomEventFilters):

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


class EnterKeyPressFilter(CustomEventFilters):

    def eventFilter(self, obj, event):
        if isinstance(event, PySide2.QtGui.QKeyEvent):
            if (event.key() == Qt.Key_Return):
                self.callback()
                event.setAccepted(True)
                return True

        return False

def update_combobox_items_with_completer(comboBox: QtWidgets.QComboBox, items):
    """Updates the possible items of the combobox and adds a completer
    Suppresses signals and preserves the current text
    """
    with BlockSigs(comboBox):
        ct = comboBox.currentText()
        comboBox.clear()
        comboBox.addItems(items)

        # set QCompleter
        completer = QCompleter(items)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setModelSorting(QCompleter.UnsortedModel)
        completer.setFilterMode(Qt.MatchContains)
        comboBox.setCompleter(completer)
        comboBox.setCurrentText(ct)