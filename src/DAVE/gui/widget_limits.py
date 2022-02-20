"""
This is the limits dock-widget
"""
from PySide2.QtCore import QObject, QEvent, Qt
from PySide2.QtGui import QColor, QKeyEvent
from PySide2.QtWidgets import QTableWidgetItem, QHeaderView

from DAVE.settings_visuals import UC_CMAP
from DAVE.gui.helpers.my_qt_helpers import combobox_update_items, DeleteEventFilter

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
from DAVE.gui.forms.widget_limits import Ui_DockLimits

# from DAVE.settings import DAVE_REPORT_PROPS




class WidgetLimits(guiDockWidget):

    def guiCreate(self):
        """
        Add gui components to self.contents

        Do not fill the controls with actual values here. This is executed
        upon creation and guiScene etc are not yet available.

        """

        self.ui = Ui_DockLimits()
        self.ui.setupUi(self.contents)

        self.delete_event_filter = DeleteEventFilter()
        self.delete_event_filter.callback = self.delete_limit

        self.contents.installEventFilter(self.delete_event_filter)

        self.ui.pbApply.setEnabled(False)
        self.ui.pbRemove.setEnabled(False)

        self.ui.table.setColumnCount(5)
        self.ui.table.setHorizontalHeaderLabels(('Node','Property','Value','Limit','UC'))
        self.ui.table.verticalHeader().setVisible(False)

        self.ui.lineEdit.textChanged.connect(self.limit_value_changed)
        self.ui.lineEdit.returnPressed.connect(self.apply_limit)

        self.ui.cbNode.currentIndexChanged.connect(self.node_selected_in_cb)
        self.ui.cbProperty.currentIndexChanged.connect(self.node_property_updated)

        self.ui.table.currentCellChanged.connect(self.selection_changed)

        self.ui.pbApply.clicked.connect(self.apply_limit)
        self.ui.pbRemove.clicked.connect(self.delete_limit)

        self.ui.lblError.setVisible(False)

    def guiProcessEvent(self, event):
        """
        Add processing that needs to be done.

        After creation of the widget this event is called with guiEventType.FULL_UPDATE
        """

        if event in [guiEventType.FULL_UPDATE,
                     guiEventType.MODEL_STATE_CHANGED,
                     guiEventType.SELECTED_NODE_MODIFIED,
                     guiEventType.MODEL_STEP_ACTIVATED, ]:
            self.fill_table()

        if event in [guiEventType.FULL_UPDATE,
                     guiEventType.SELECTION_CHANGED,
                     guiEventType.MODEL_STRUCTURE_CHANGED,
                     guiEventType.MODEL_STEP_ACTIVATED,
                     ]:
            self.fill_edit_section()


    def guiDefaultLocation(self):
        return QtCore.Qt.DockWidgetArea.RightDockWidgetArea

    # ======




    def node_selected_in_cb(self):
        try:
            node = self.guiScene[self.ui.cbNode.currentText()]
        except:
            return

        self.guiSelectNode(node)  # this triggers the fill_edit_section


    def fill_edit_section(self):
        self.ui.widget.blockSignals(True)

        # the node drop-down

        cbN = self.ui.cbNode
        cbN.blockSignals(True)
        combobox_update_items(cbN, [node.name for node in self.guiScene.unmanged_nodes])

        if self.guiSelection:
            node = self.guiSelection[0]
            if node.manager is None:
                cbN.setCurrentText(node.name)
                self.ui.lbNodeClass.setText(f'Node type: {node.class_name}')
                self.ui.lblError.setVisible(False)
            else:
                self.ui.lblError.setText(f'{node.name} is managed by {node.manager.name}' )
                self.ui.lblError.setVisible(True)

        cbN.blockSignals(False)

        # the properties drop-down
        cbP = self.ui.cbProperty
        cbP.blockSignals(True)

        if cbN.currentText():
            node = self.guiScene[cbN.currentText()]
            props = self.guiScene.give_properties_for_node(node)

            exclude = ('name','UC','UC_governing_details','manager','parent_for_export','visible','class_name','parent','footprint','fixed','intertia','inertia_position','inertia_radii')

            props_without_name_and_UC = [p for p in props if p not in exclude]
            combobox_update_items(cbP, props_without_name_and_UC)

            if node.manager is None:
                self.ui.widgetLimitEdit.setEnabled(True)
            else:
                self.ui.widgetLimitEdit.setEnabled(False)   # NOTE: This actually never happens as the names of the
                                                            # managed nodes are not in the drop-down box
                self.ui.lbNodeClass.setText(f'This node is managed by {node.manager.name}')


        else:
            cbP.clear()

        cbP.blockSignals(False)

        self.ui.widget.blockSignals(False)

        self.node_property_updated()

    def node_property_updated(self):

        try:
            node = self.guiScene[self.ui.cbNode.currentText()]
        except:
            return

        prop_name = self.ui.cbProperty.currentText()

        if prop_name == '':
            # no properties available
            self.ui.pbRemove.setEnabled(False)
            self.ui.pbApply.setEnabled(False)
            self.ui.lbPropHelp.setText('')
            return


        # get the property documentation
        # step1 = DAVE_REPORT_PROPS[DAVE_REPORT_PROPS['class'] == node.class_name]
        # step2 = step1[step1['property'] == prop_name]
        # doc = step2['doc']
        #
        # if doc.empty:
        #     doc = 'No help available, sorry :-/'
        # else:
        #     doc = doc.item()

        doc = self.guiScene.give_documentation(node, prop_name).doc_long

        # get the actual value of the property
        actual_value = getattr(node, prop_name)
        if isinstance(actual_value, float):
            actual_value = f'{actual_value:.3f}'
        doc += f'\nActual value = {actual_value}'

        self.ui.lbPropHelp.setText(doc)

        if self.ui.lineEdit.hasFocus():
            return

        if prop_name in node.limits:
            self.ui.lineEdit.setText(str(node.limits[prop_name]))
            self.ui.pbRemove.setEnabled(True)
        else:
            self.ui.lineEdit.setText('')
            self.ui.pbRemove.setEnabled(False)

    def limit_value_changed(self):

        try:
            node = self.guiScene[self.ui.cbNode.currentText()]
        except:
            return

        prop_name = self.ui.cbProperty.currentText()
        limit_value = self.ui.lineEdit.text()

        if limit_value == '':
            message = f'use:\n- 123.456 to define a max-abs limit\n- (start, stop) to define a range'
            self.ui.lbResult.setText(message)
            self.ui.pbApply.setEnabled(False)
            return

        # see if we have a valid limit
        try:
            a = eval(limit_value)
        except:
            a = limit_value

        node.limits[prop_name] = a

        uc = None
        try:
            uc = node.give_UC(prop_name)
        except Exception as E:
            del node.limits[prop_name]
            message = f'Invalid limit, use:\n- 123.456 to define a max-abs limit\n- (start, stop) to define a range\n\nError message:\n{str(E)}'
            self.ui.lbResult.setText(message)
            self.ui.pbApply.setEnabled(False)

        if uc is not None:
            self.ui.lbResult.setText(f'UC = {uc:.2f}')
            self.ui.pbApply.setEnabled(True)



    def fill_table(self):

        table = self.ui.table # alias
        table.blockSignals(True)

        unmanged_nodes_with_limit = [node for node in self.guiScene.unmanged_nodes if node.limits is not None]
        managed_nodes_with_limit = [node for node in self.guiScene.manged_nodes if node.limits is not None]

        irow = 0
        table.setRowCount(0)

        for node in (*unmanged_nodes_with_limit, *managed_nodes_with_limit):

            for key, value in node.limits.items():

                if isinstance(value, float):  # do not list unset limits (limit < 0)
                    if value < 0:
                        continue

                table.setRowCount(irow+1)

                # ('Node','Property','Value','Limit','UC')
                table.setItem(irow, 0, QTableWidgetItem(node.name))
                table.setItem(irow, 1, QTableWidgetItem(key))

                prop_value = getattr(node, key)
                if isinstance(prop_value, float):  # round floats to 3 decimals
                    prop_value = f'{prop_value:.3f}'
                table.setItem(irow, 2, QTableWidgetItem(str(prop_value)))

                table.setItem(irow, 3, QTableWidgetItem(str(value)))
                uc = node.give_UC(key)

                if uc > 1:
                    uc_paint = (1, 0, 1)  # ugly pink
                else:
                    uc_paint = UC_CMAP(round(100*uc))

                uc_item = QTableWidgetItem(f'{uc:.2f}')
                uc_item.setBackgroundColor(QColor(255*uc_paint[0],
                                                  255 * uc_paint[1],
                                                  255 * uc_paint[2],
                                                  254
                                                  ))

                if uc > 0.2 and uc < 0.7:
                    uc_item.setTextColor(QColor(0,0,0,255))
                else:
                    uc_item.setTextColor(QColor(255, 255, 255, 255))
                table.setItem(irow, 4, uc_item)

                irow += 1


        table.resizeColumnsToContents()
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.blockSignals(False)

    def selection_changed(self, cur_row, cur_col, prev_row, prev_col):
        """Select the node via the gui, then select the property"""

        node = self.ui.table.item(cur_row,0).text()
        prop = self.ui.table.item(cur_row, 1).text()

        self.guiSelectNode(self.guiScene[node])

        self.ui.cbProperty.setCurrentText(prop)

    def apply_limit(self):
        print('apply')

        if self.ui.pbApply.isEnabled():  # event is called by pressing enter as well
            node_name = self.ui.cbNode.currentText()
            prop_name = self.ui.cbProperty.currentText()
            limit_value = self.ui.lineEdit.text()
            code = f"s['{node_name}'].limits['{prop_name}'] = {limit_value}"
            self.guiRunCodeCallback(code, guiEventType.SELECTED_NODE_MODIFIED)

    def delete_limit(self):
        if self.ui.pbRemove.isEnabled():  # event is called by pressing enter as well
            node_name = self.ui.cbNode.currentText()
            prop_name = self.ui.cbProperty.currentText()
            code = f"del s['{node_name}'].limits['{prop_name}']"
            self.guiRunCodeCallback(code, guiEventType.SELECTED_NODE_MODIFIED)


    # def action(self):
    #
    #     # never executed in the example
    #     self.guiRunCodeCallback("print('Hi, I am an exampe')", guiEventType.SELECTED_NODE_MODIFIED)   # call the callback to execute code
    #     self.guiSelectNode('Node-name') # to globally select a node
