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

        self.ui.pbFreezeAll.pressed.connect(self.freeze_all)
        self.ui.pbUnfreezeAll.pressed.connect(self.unfreeze_all)
        self.ui.pbToggleFreeze.pressed.connect(self.toggle_freeze)

        self.ui.pbFillAll.pressed.connect(lambda : self.fill_all_to(100))
        self.ui.pbEmptyAll.pressed.connect(lambda: self.fill_all_to(0))



        self._bs = None # active ballast system
        self._filling_table = True
        self._cbFrozen = list()



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

    def selection_changed(self,cur_row, cur_col, prev_row, prev_col):
        item = self.ui.tableWidget.verticalHeaderItem(cur_row)
        if item is not None:
            name = item.text()
            self.update_outlines(name=name)

    def update_outlines(self, name = ""):
        if self._bs is None:
            return

        # loop over tanks
        #   find visual
        #       find outline
        #            git outline a different width and color

        # print('selecting tank {}'.format(name))

        for tank in self._bs._tanks:
            actor = tank.actor

            outline_actor = None
            for outline in self.gui.visual.outlines:
                if outline.parent_vp_actor == actor:
                    outline_actor = outline.outline_actor
                    break


            if outline_actor is not None:
                if tank.name == name:
                    outline_actor.GetProperty().SetLineWidth(5)
                    outline_actor.GetProperty().SetColor(254,0,0)
                else:
                    outline_actor.GetProperty().SetLineWidth(self.gui.visual.outline_width)
                    outline_actor.GetProperty().SetColor(0, 0, 0)

        self.gui.visual.refresh_embeded_view()


    def freeze_all(self):
        if self._bs is None:
            return
        for t in self._bs._tanks:
            t.frozen = True
        self.fill()

    def unfreeze_all(self):
        if self._bs is None:
            return
        for t in self._bs._tanks:
            t.frozen = False
        self.fill()

    def toggle_freeze(self):
        if self._bs is None:
            return
        for t in self._bs._tanks:
            t.frozen = not t.frozen
        self.fill()

    def fill_all_to(self,pct):
        code = ''
        for t in self._bs._tanks:
            code += '\ns["{}"]["{}"].pct = {}'.format(self._bs.name, t.name, pct)
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
        self._cbFrozen.clear()

        for i,t in enumerate(self._bs._tanks):
            rows = i

            tw.setRowCount(rows + 1)
            tw.setVerticalHeaderItem(rows, QtWidgets.QTableWidgetItem(t.name))

            item = QtWidgets.QTableWidgetItem('{:.1f}'.format(t.max))
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

            item = QtWidgets.QCheckBox()
            self._cbFrozen.append(item)
            item.setChecked(t.frozen)
            item.stateChanged.connect(self.tankFrozenChanged)
            tw.setCellWidget (rows, 2, item)

            for j in range(3):
                item = QtWidgets.QTableWidgetItem('{:.3f}'.format(t.position[j]))
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

            code = 's["{}"].fill_tank("{}",{})'.format(self._bs.name, tank_name, fill)
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
            frozen = self._cbFrozen[i_row].isChecked()

            if self._bs[tank_name].frozen != frozen:
                self.guiRunCodeCallback('s["{}"]["{}"].frozen = {}'.format(self._bs.name, tank_name, frozen), guiEventType.SELECTED_NODE_MODIFIED)
                return


