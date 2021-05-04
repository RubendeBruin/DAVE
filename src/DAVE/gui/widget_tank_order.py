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
from DAVE.gui.forms.widgetUI_tank_order import Ui_widget_tank_order

class WidgetTankOrder(guiDockWidget):

    def guiCreate(self):
        """
        Add gui components to self.contents

        Do not fill the controls with actual values here. This is executed
        upon creation and guiScene etc are not yet available.

        """

        # # or from a generated file
        self.ui = Ui_widget_tank_order()
        self.ui.setupUi(self.contents)

        self._bs = None  # selected ballast system

        self.ui.pbElevation.clicked.connect(lambda : self.run_action("order_tanks_by_elevation()"))
        self.ui.pbMaximizeRadii.clicked.connect(lambda: self.run_action("order_tanks_to_maximize_inertia_moment()"))
        self.ui.pbMinimizeRadii.clicked.connect(lambda: self.run_action("order_tanks_to_minimize_inertia_moment()"))

        self.ui.pbFurthest.clicked.connect(lambda: self.point(", reverse=False"))
        self.ui.pbNearest.clicked.connect(lambda: self.point(", reverse=True"))


    def guiProcessEvent(self, event):
        """
        Add processing that needs to be done.

        After creation of the widget this event is called with guiEventType.FULL_UPDATE
        """

        if event in [guiEventType.SELECTION_CHANGED,
                     guiEventType.FULL_UPDATE,
                     guiEventType.MODEL_STATE_CHANGED,
                     guiEventType.SELECTED_NODE_MODIFIED]:
            self.fill()

    def guiDefaultLocation(self):
        return QtCore.Qt.DockWidgetArea.LeftDockWidgetArea

    def run_action(self, action):
        if self._bs is None:
            return

        code = 's["{}"].{}'.format(self._bs.name, action)
        self.guiRunCodeCallback(code, guiEventType.SELECTED_NODE_MODIFIED)

    def point(self,additional=''):
        x = self.ui.dsX.value()
        y = self.ui.dsX_2.value()
        z = self.ui.dsX_3.value()
        action = 'order_tanks_by_distance_from_point(({},{},{}){})'.format(x,y,z, additional)
        self.run_action(action)

    def fill(self):
        # display the name of the selected node
        if self.guiSelection:
            node = self.guiSelection[0]
            if isinstance(node, nodes.BallastSystem):
                self._bs = node



