"""
This is an example/template of how to setup a new dockwidget
"""
import subprocess

from PySide2.QtGui import QIcon

"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Ruben de Bruin - 2019
"""

from DAVE.gui.dockwidget import *
from PySide2 import QtGui, QtCore, QtWidgets
import DAVE.scene as ds
from DAVE.gui.forms.widget_footprints import Ui_FootprintForm
from PySide2.QtWidgets import QTreeWidgetItem, QMessageBox
from DAVE.gui.helpers.gridedit import GridEdit
from DAVE import settings


class WidgetFootprints(guiDockWidget):
    def guiCreate(self):
        """
        Add gui components to self.contents

        Do not fill the controls with actual values here. This is executed
        upon creation and guiScene etc are not yet available.

        """

        self._element = None

        # # or from a generated file
        self.ui = Ui_FootprintForm()
        self.ui.setupUi(self.contents)

        self.grid = GridEdit(parent=self.contents)
        self.lblInfo = QtWidgets.QLabel()
        self.lblInfo.setText("Select a node")
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.lblInfo)
        layout.addWidget(self.grid)
        self.ui.widget.setLayout(layout)

        # # Example with raw data
        self.grid.addColumn("x", float)
        self.grid.addColumn("y", float)
        self.grid.addColumn("z", float)
        self.grid.activateColumns()
        self.grid.onChanged = self.update_footprint
        self.grid.setData([[]], allow_add_or_remove_rows=True)

        self.ui.treeView.activated.connect(
            self.tree_select_node
        )  # fires when a user presses [enter]
        self.ui.treeView.doubleClicked.connect(self.tree_select_node)
        self.ui.treeView.itemClicked.connect(self.item_clicked)


    def guiProcessEvent(self, event):
        """
        Add processing that needs to be done.

        After creation of the widget this event is called with guiEventType.FULL_UPDATE
        """

        if event in [guiEventType.MODEL_STATE_CHANGED,
                     guiEventType.FULL_UPDATE,
                     guiEventType.MODEL_STRUCTURE_CHANGED]:
            self.fill()

        if event in [guiEventType.SELECTION_CHANGED]:
            self.element_selected()

    def guiDefaultLocation(self):
        return QtCore.Qt.DockWidgetArea.RightDockWidgetArea

    # ======

    def fill(self):

        """
        Updates the tree and assembles the node-data

        This data is obtained from scene.nodes and assumes that
        each of the nodes has a visual assigned to it.

        """

        self.items = dict()

        self.guiScene.sort_nodes_by_parent()
        self.ui.treeView.clear()
        self.ui.treeView.guiScene = self.guiScene

        for node in self.guiScene._nodes:

            # create a tree item
            text = node.name
            item = QTreeWidgetItem()
            item.setText(0, text)

            # if we have a parent, then put the items under the parent,
            # else put it under the root

            if isinstance(node, ds.Frame):
                item.setIcon(0, QIcon(":/icons/axis_blue.png"))
            elif isinstance(node, ds.RigidBody):
                item.setIcon(0, QIcon(":/icons/cube.png"))
            elif isinstance(node, ds.Point):
                item.setIcon(0, QIcon(":/icons/point_blue.png"))
            else:
                continue

            try:
                parent = node.parent
            except:
                parent = None

            self.items[node.name] = item

            if parent is None:
                self.ui.treeView.invisibleRootItem().addChild(item)
            else:
                if parent.name in self.items:
                    self.items[parent.name].addChild(item)

        self.ui.treeView.expandAll()

    def item_clicked(self, data):
        name = data.text(0)
        self.guiSelectNode(name)

    def tree_select_node(self, index):
        if index.column() == 0:
            node_name = index.data()
            self.guiSelectNode(node_name)

    def update_footprint(self):
        footprint = self.grid.getData()
        valid_data = []
        for row in footprint:
            try:
                assert3f(row)
                valid_data.append(row)
            except:
                pass

        self.grid.highlight_invalid_data()
        code = f"s['{self._element.name}'].footprint = {str(valid_data)}"

        # Safe, this widget itself does not
        self.guiRunCodeCallback(code,
                                event=guiEventType.SELECTED_NODE_MODIFIED,
                                )

    # --------------------------------------

    def element_selected(self):
        try:
            element = self.guiSelection[0]
        except:
            return

        if not isinstance(element, (Frame, Point)):
            return

        self._element = element
        self.lblInfo.setText(f"Footprint for {self._element.name} :")
        self.grid.setData(self._element.footprint, allow_add_or_remove_rows=True)
        self.grid.grid.resizeColumnsToContents()

        # select in the tree as well
        self.ui.treeView.blockSignals(True)

        # dict self.items[element.name]  # created then the tree was filled
        for name in self.items.keys():

            if name == element.name:
                self.items[name].setSelected(True)
                self.ui.treeView.scrollToItem(self.items[name])
            else:
                self.items[name].setSelected(False)

        self.ui.treeView.blockSignals(False)

