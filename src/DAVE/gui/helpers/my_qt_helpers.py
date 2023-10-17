
import PySide6.QtCore
import PySide6.QtGui
from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QComboBox, QWidget, QCompleter


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

def remove_from_stylesheet(stylesheet : str, identifier : str) -> str:
    lines = stylesheet.split('\n')
    new_lines = list()
    active = True
    for line in lines:
        if identifier in line:
            active = False

        if active:
            new_lines.append(line)

        if '}' in line:
            active = True

    return '\n'.join(new_lines)


def set_text_no_signal(widget, text):
    widget.blockSignals(True)
    widget.setText(text)
    widget.blockSignals(False)

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

class CustomEventFilters(PySide6.QtCore.QObject):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.callback = None


class CustomKeyEventFilter(CustomEventFilters):
    key = Qt.Key_Delete

    def eventFilter(self, obj, event):



        if isinstance(event, PySide6.QtGui.QKeyEvent):

            if (event.key() == self.key):
                if event.type() == PySide6.QtCore.QEvent.KeyPress:
                    if self.callback is None:
                        print('Callback not set')
                    else:
                        self.callback()
                        return True

                    event.setAccepted(True)
                    return True

        return False


class DeleteEventFilter(CustomKeyEventFilter):
    key = Qt.Key_Delete

class EnterKeyPressFilter(CustomKeyEventFilter):
    key = Qt.Key_Return

class EscKeyPressFilter(CustomKeyEventFilter):
    key = Qt.Key_Escape



class RightClickEventFilter(CustomEventFilters):

    def eventFilter(self, obj, event):
        if isinstance(event, PySide6.QtGui.QMouseEvent):
            if (event.type() == PySide6.QtCore.QEvent.Type.MouseButtonPress):
                if event.button() == PySide6.QtCore.Qt.MouseButton.RightButton:
                    self.callback(event)
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