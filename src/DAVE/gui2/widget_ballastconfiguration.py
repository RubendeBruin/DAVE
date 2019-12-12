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
from PySide2.QtGui import QBrush, QColor
import DAVE.scene as nodes
import DAVE.settings as ds
import numpy as np

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
        self.ui.tableWidget.verticalHeader().sectionMoved.connect(self.reorder_rows)

        self.ui.tableWidget.cellChanged.connect(self.tankfillchanged)

        self._bs = None # active ballast system
        self._filling_table = True



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
                self._bs = node

        if self._bs is None:
            return

        tw = self.ui.tableWidget

        partial = QColor.fromRgb(*254*np.array(ds.COLOR_SELECT))
        full    = QColor.fromRgb(*254*np.array(ds.COLOR_WATER))
        empty = QColor.fromRgb(254,254,254)

        self._filling_table = True

        for i,t in enumerate(self._bs._tanks):
            rows = i

            tw.setRowCount(rows + 1)
            tw.setVerticalHeaderItem(rows, QtWidgets.QTableWidgetItem(t.name))

            item = QtWidgets.QTableWidgetItem('{:e}'.format(t.max))
            item.setFlags(QtCore.Qt.ItemIsEditable)
            tw.setItem(rows, 0, item)

            item = QtWidgets.QTableWidgetItem('{:.1f}'.format(t.pct))
            if t.pct >= 99.9:
                item.setBackground(QBrush(full))
                item.setTextColor(empty)

            elif t.pct > 0.1:
                item.setBackground(QBrush(partial))
            else:
                item.setBackground(QBrush(empty))
            tw.setItem(rows, 1, item)

            for j in range(3):
                item = QtWidgets.QTableWidgetItem('{:e}'.format(t.position[j]))
                item.setFlags(QtCore.Qt.ItemIsEditable)
                tw.setItem(rows, 2+j, item)

        self._filling_table = False


    def reorder_rows(self, a, b, c):
        vh = self.ui.tableWidget.verticalHeader()
        tw = self.ui.tableWidget
        names = list()
        for row in range(tw.rowCount()):
            i = vh.logicalIndex(row)
            names.append(tw.verticalHeaderItem(i).text())

        code = 's["{}"].reorder_tanks(['.format(self._bs.name)
        for name in names:
            code += "'{}',".format(name)

        code = code[:-1]
        code += '])'

        self.guiRunCodeCallback(code, guiEventType.SELECTED_NODE_MODIFIED)

    def tankfillchanged(self,a,b):

        if self._filling_table:
            return

        tank_name = self.ui.tableWidget.verticalHeaderItem(a).text()
        fill = self.ui.tableWidget.item(a,b).text()

        # try:
        #     float(fill)
        # except:
        #     return

        code = 's["{}"].fill_tank("{}",{})'.format(self._bs.name, tank_name, fill)
        self.guiRunCodeCallback(code, guiEventType.SELECTED_NODE_MODIFIED)
