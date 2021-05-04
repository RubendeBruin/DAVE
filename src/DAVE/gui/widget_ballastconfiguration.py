"""
WidgetBallastConfiguration
"""

"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Ruben de Bruin - 2019
"""

from DAVE.gui.dockwidget import *
from DAVE.gui.forms.widgetUI_ballastconfiguration import Ui_widget_ballastsystem
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
        self.ui.tableWidget.currentCellChanged.connect(self.selection_changed)

        self.ui.tableWidget.cellChanged.connect(self.tankfillchanged)

        self.ui.pbFreezeAll.clicked.connect(self.freeze_all)
        self.ui.pbUnfreezeAll.clicked.connect(self.unfreeze_all)
        self.ui.pbToggleFreeze.clicked.connect(self.toggle_freeze)

        self.ui.pbFillAll.clicked.connect(lambda : self.fill_all_to(100))
        self.ui.pbEmptyAll.clicked.connect(lambda: self.fill_all_to(0))

        self.ui.pbGenerate.clicked.connect(self.report_python)

        self._bs = None # active ballast system
        self._filling_table = True



    def guiProcessEvent(self, event):
        """
        Add processing that needs to be done.

        After creation of the widget this event is called with guiEventType.FULL_UPDATE
        """

        if event in [guiEventType.FULL_UPDATE,
                     guiEventType.MODEL_STATE_CHANGED,
                     guiEventType.SELECTED_NODE_MODIFIED]:
            self.fill()

        if event in [guiEventType.SELECTION_CHANGED]:
            self.select_row_for_tank()



    def guiDefaultLocation(self):
        return QtCore.Qt.DockWidgetArea.RightDockWidgetArea

    # ======

    def select_row_for_tank(self):
        if self.guiSelection:
            name = self.guiSelection[0].name
            for i in range(self.ui.tableWidget.rowCount()):
                if self.ui.tableWidget.verticalHeaderItem(i).text() == name:
                    self.ui.tableWidget.selectRow(i)
                    return


    def selection_changed(self,cur_row, cur_col, prev_row, prev_col):
        item = self.ui.tableWidget.verticalHeaderItem(cur_row)
        if item is not None:
            name = item.text()
            self.update_outlines(name=name)

    def update_outlines(self, name = ""):
        if self._bs is None:
            return

        for tank in self._bs.tanks:
            actor = tank.visual.actors[0]  # wireframe

            if tank.name == name:
                actor.lw(5)
                actor.c((254,0,0))
            else:
                actor.lw(1)
                actor.c(ds.COLOR_TANK_MESH_LINES)

            #
            # outline_actor = None
            # for outline in self.gui.visual.outlines:
            #     if outline.parent_vp_actor == actor:
            #         outline_actor = outline.outline_actor
            #         break
            #
            #
            # if outline_actor is not None:
            #     if tank.name == name:
            #         outline_actor.GetProperty().SetLineWidth(5)
            #         outline_actor.GetProperty().SetColor(254,0,0)
            #     else:
            #         outline_actor.GetProperty().SetLineWidth(self.gui.visual.outline_width)
            #         outline_actor.GetProperty().SetColor(0, 0, 0)

        self.gui.visual.refresh_embeded_view()


    def freeze_all(self):
        if self._bs is None:
            return
        self._bs.frozen = [t.name for t in self._bs.tanks]
        self.fill()

    def unfreeze_all(self):
        if self._bs is None:
            return
        self._bs.frozen = list()
        self.fill()

    def toggle_freeze(self):
        if self._bs is None:
            return

        new_frozen = []

        for t in self._bs.tanks:
            if self._bs.is_frozen(t.name):
                pass
            else:
                new_frozen.append(t.name)

        self._bs.frozen = new_frozen
        self.fill()

    def fill_all_to(self,pct):
        code = ''
        for t in self._bs.tanks:
            code += '\ns["{}"].fill_pct = {}'.format(t.name, pct)
        self.guiRunCodeCallback(code, guiEventType.SELECTED_NODE_MODIFIED)

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

        for i,t in enumerate(self._bs.tanks):
            rows = i

            tw.setRowCount(rows + 1)
            tw.setVerticalHeaderItem(rows, QtWidgets.QTableWidgetItem(t.name))

            item = QtWidgets.QTableWidgetItem('{:.1f}'.format(t.capacity))
            item.setFlags(QtCore.Qt.ItemIsEditable)
            tw.setItem(rows, 0, item)

            item = QtWidgets.QTableWidgetItem('{:.1f}'.format(t.fill_pct))
            if t.fill_pct >= 99.9:
                item.setBackground(QBrush(full))
                item.setTextColor(empty)

            elif t.fill_pct > 0.1:
                item.setBackground(QBrush(partial))
            else:
                item.setBackground(QBrush(empty))
            tw.setItem(rows, 1, item)

            item = QtWidgets.QCheckBox()
            item.setChecked(self._bs.is_frozen(t.name))
            item.stateChanged.connect(self.tankFrozenChanged)
            tw.setCellWidget (rows, 2, item)

            for j in range(3):

                item = QtWidgets.QTableWidgetItem('{:.3f}'.format(t.cog_local[j]))
                item.setFlags(QtCore.Qt.ItemIsEditable)
                tw.setItem(rows, 3+j, item)

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

        if b == 1:
            fill = self.ui.tableWidget.item(a,b).text()

            if fill == 'f':
                fill = 100
            if fill == 'e':
                fill = 0

            code = 's["{}"].fill_pct = {}'.format(tank_name, fill)
            self.guiRunCodeCallback(code, guiEventType.SELECTED_NODE_MODIFIED)
        else:
            raise Exception('This cell is not supposed to be editable')

        self.ui.tableWidget.setCurrentCell(a,b)
        self.ui.tableWidget.setFocus()

    def tankFrozenChanged(self):
        if self._filling_table:
            return

        # no idea which entry was changed....
        for i_row in range(self.ui.tableWidget.rowCount()):
            tank_name = self.ui.tableWidget.verticalHeaderItem(i_row).text()

            # frozen = self._cbFrozen[i_row].isChecked()
            frozen = self.ui.tableWidget.cellWidget(i_row, 2).isChecked()

            if self._bs.is_frozen(tank_name) != frozen:
                if frozen:
                    code = 's["{}"].frozen.append("{}")'.format(self._bs.name, tank_name)
                else:
                    code = 's["{}"].frozen.remove("{}")'.format(self._bs.name, tank_name)
                self.guiRunCodeCallback(code, guiEventType.SELECTED_NODE_MODIFIED)
                return

    def report_python(self):
        """Runs the current tank fillings in python"""

        code = ''
        for t in self._bs.tanks:
            code += '\ns["{}"].fill_pct = {}'.format(t.name, t.fill_pct)
        self.guiRunCodeCallback(code, guiEventType.SELECTED_NODE_MODIFIED)



