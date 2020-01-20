import DAVE.gui.forms.widget_dynprop
from PySide2.QtWidgets import QCheckBox
from DAVE.scene import Axis

from DAVE.gui.dockwidget import *


class WidgetDynamicProperties(guiDockWidget):

    def guiCreate(self):

        self.ui = DAVE.gui.forms.widget_dynprop.Ui_widget_dynprop()
        self.ui.setupUi(self.contents)

        self.ui.tableDynProp.itemChanged.connect(self.node_table_cell_edit_done)

    def guiProcessEvent(self, event):

        if event in [guiEventType.SELECTION_CHANGED,
                     guiEventType.SELECTED_NODE_MODIFIED,
                     guiEventType.MODEL_STRUCTURE_CHANGED,
                     guiEventType.FULL_UPDATE]:
            self.fill_nodes_table()

    def guiDefaultLocation(self):
        return QtCore.Qt.DockWidgetArea.RightDockWidgetArea


    def fill_nodes_table(self):

        axes = self.guiScene.nodes_of_type(Axis)
        self._filling_node_table = True

        store_scrollbar_position = self.ui.tableDynProp.verticalScrollBar().sliderPosition()

        for row, b in enumerate(axes):
            self.ui.tableDynProp.setRowCount(row+1)
            self.ui.tableDynProp.setVerticalHeaderItem(row,QtWidgets.QTableWidgetItem(b.name))

            cbs = list()
            for i in range(6):
                cbs.append(QCheckBox())
                self.ui.tableDynProp.setCellWidget(row,i,cbs[i])
                cbs[i].setChecked(b.fixed[i])
                self.ui.tableDynProp.setColumnWidth(i,24)
                cbs[i].node = b
                cbs[i].stateChanged.connect(self.node_table_cell_change_checkbox)
            b._checkboxes = cbs

            self.ui.tableDynProp.setItem(row, 6, QtWidgets.QTableWidgetItem(str(b.inertia)))

            for i in range(3):
                self.ui.tableDynProp.setItem(row, 7+i, QtWidgets.QTableWidgetItem(str(b.inertia_position[i])))
                self.ui.tableDynProp.setItem(row, 10+i, QtWidgets.QTableWidgetItem(str(b.inertia_radii[i])))

        self.ui.tableDynProp.resizeColumnsToContents()

        self.ui.tableDynProp.verticalScrollBar().setSliderPosition(store_scrollbar_position)

        self._filling_node_table = False

    def node_table_cell_change_checkbox(self):
        if self._filling_node_table:
            return

        self.gui.animation_terminate()

        row = self.ui.tableDynProp.currentRow()
        name = self.ui.tableDynProp.verticalHeaderItem(row).text()
        node = self.guiScene[name]

        fixed = [cb.isChecked() for cb in node._checkboxes]

        # self._pause = True
        # self.scene._vfc.set_dofs(self.d0)
        code = 's["{}"].fixed = ({},{},{},{},{},{})'.format(name, *fixed)

        self.guiRunCodeCallback(code, guiEventType.MODEL_STRUCTURE_CHANGED)



    def node_table_cell_edit_done(self, data):
        if self._filling_node_table:
            return

        value = data.text()

        row = data.row()
        col = data.column()

        name = self.ui.tableDynProp.verticalHeaderItem(row).text()
        node = self.guiScene[name]

        code = ''

        if col == 6:  # inertia
            try:
                node.mass
                code = 's["{}"].mass = {}'.format(name, value)
                print('test')
            except:
                code = 's["{}"].inertia = {}'.format(name, value)
                print('test2')

        elif col in (7,8,9): # cog

            pos = [self.ui.tableDynProp.item(row,7).text(),
                   self.ui.tableDynProp.item(row,8).text(),
                   self.ui.tableDynProp.item(row,9).text()]

            try:
                node.mass
                code = 's["{}"].cog = ({},{},{})'.format(name, *pos)
            except:
                code = 's["{}"].inertia_position = ({},{},{})'.format(name, *pos)

        elif col in (10,11,12):  # cog

            pos = [self.ui.tableDynProp.item(row, 10).text(),
                   self.ui.tableDynProp.item(row, 11).text(),
                   self.ui.tableDynProp.item(row, 12).text()]

            code = 's["{}"].inertia_radii = ({},{},{})'.format(name, *pos)

        else:
            print('This column is not supposed to be edited')

        self.guiRunCodeCallback(code, guiEventType.MODEL_STRUCTURE_CHANGED)



