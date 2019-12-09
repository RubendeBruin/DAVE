"""
WidgetBallastConfiguration
"""

"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Ruben de Bruin - 2019
"""

from DAVE.gui2.dockwidget import *
from DAVE.gui2.forms.widgetUI_ballastconfiguration import Ui_widget_ballastsystem
from PySide2 import QtGui, QtCore, QtWidgets
import DAVE.scene as nodes
import DAVE.settings as ds

class WidgetBallastConfiguration(guiDockWidget):

    def guiCreate(self):
        """
        Add gui components to self.contents

        Do not fill the controls with actual values here. This is executed
        upon creation and guiScene etc are not yet available.

        """

        # # or from a generated file
        self.ui = Ui_widget_ballastsystem()
        self.ui.setupUi(self.contents)

        self.ui.tableWidget.verticalHeader().setSectionsMovable(True)



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
        return QtCore.Qt.DockWidgetArea.RightDockWidgetArea

    # ======

    def fill(self):

        # display the name of the selected node
        if self.guiSelection:
            node = self.guiSelection[0]

            if isinstance(node, nodes.BallastSystem):
                tw = self.ui.tableWidget
                for i,t in enumerate(node.tanks):
                    rows = i

                    tw.setRowCount(rows + 1)
                    tw.setVerticalHeaderItem(rows, QtWidgets.QTableWidgetItem(t.name))
                    tw.setItem(rows, 0, QtWidgets.QTableWidgetItem('{:e}'.format(t.capacity())))
                    tw.setItem(rows, 1, QtWidgets.QTableWidgetItem('{:.1f}'.format(t.fillpct())))
                    tw.setItem(rows, 2, QtWidgets.QTableWidgetItem('{:e}'.format(t.position[0])))
                    tw.setItem(rows, 3, QtWidgets.QTableWidgetItem('{:e}'.format(t.position[1])))
                    tw.setItem(rows, 4, QtWidgets.QTableWidgetItem('{:e}'.format(t.position[2])))

    def action(self):
        pass

