"""
This is an example/template of how to setup a new dockwidget
"""

"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Ruben de Bruin - 2019
"""

from DAVE.gui.dockwidget import *
from PySide2 import QtGui, QtCore, QtWidgets
import DAVE.scene as nodes
import DAVE.settings as ds
from DAVE.gui.forms.widgetUI_environment import Ui_frmEnvironment


class WidgetEnvironment(guiDockWidget):
    def guiCreate(self):
        """
        Add gui components to self.contents

        Do not fill the controls with actual values here. This is executed
        upon creation and guiScene etc are not yet available.

        """

        self.ui = Ui_frmEnvironment()
        self.ui.setupUi(self.contents)

        self._settings = (
            "g",
            "waterlevel",
            "rho_air",
            "rho_water",
            "wind_direction",
            "wind_velocity",
            "current_direction",
            "current_velocity",
        )

        for s in self._settings:
            widget = getattr(self.ui, s)
            widget.valueChanged.connect(
                lambda x, n=s: self.action(x, n)
            )  # see https://docs.python-guide.org/writing/gotchas/#late-binding-closures

    def guiProcessEvent(self, event):
        """
        Add processing that needs to be done.

        After creation of the widget this event is called with guiEventType.FULL_UPDATE
        """

        if event in [
            guiEventType.FULL_UPDATE,
            guiEventType.ENVIRONMENT_CHANGED,
        ]:
            self.fill()

    def guiDefaultLocation(self):
        return QtCore.Qt.DockWidgetArea.LeftDockWidgetArea

    # ======

    def fill(self):

        # display the name of the selected node
        for s in self._settings:
            widget = getattr(self.ui, s)
            widget.blockSignals(True)
            widget.setValue(getattr(self.guiScene, s))
            widget.blockSignals(False)

    def action(self, value, name):
        widget = getattr(self.ui, name)
        decs = widget.decimals()
        value = np.round(value, decimals=decs)
        code = f"s.{name} = {value}"
        self.guiRunCodeCallback(code, event=guiEventType.ENVIRONMENT_CHANGED)
