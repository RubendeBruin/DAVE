"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

"""Control-Enter action filer


Example:

    self.eventFilter = CtrlEnterKeyPressFilter()
    self.eventFilter.callback = self.run_code_in_teCode

    self.ui.teCode.installEventFilter(self.eventFilter)

"""

import PySide2.QtCore
import PySide2.QtGui
from PySide2.QtCore import Qt

class ShiftEnterKeyPressFilter(PySide2.QtCore.QObject):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.callback = None

    def eventFilter(self, obj, event):

        if isinstance(event, PySide2.QtGui.QKeyEvent):

            if (event.modifiers() == Qt.ShiftModifier):
                if (event.key() == Qt.Key_Return):
                    if event.type() == PySide2.QtCore.QEvent.KeyPress:
                        if self.callback is None:
                            print('Callback not set')
                        else:
                            self.callback()
                            return True

                        event.setAccepted(True)
                        return True

        return False

class CtrlEnterKeyPressFilter(PySide2.QtCore.QObject):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.callback = None

    def eventFilter(self, obj, event):

        if isinstance(event, PySide2.QtGui.QKeyEvent):

            if (event.modifiers() == Qt.ControlModifier):
                if (event.key() == Qt.Key_Return):
                    if event.type() == PySide2.QtCore.QEvent.KeyPress:
                        if self.callback is None:
                            print('Callback not set')
                        else:
                            self.callback()
                            return True

                        event.setAccepted(True)
                        return True

        return False