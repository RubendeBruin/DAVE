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

class WidgetExample(guiDockWidget):

    def guiCreate(self):
        """
        Add gui components to self.contents

        Do not fill the controls with actual values here. This is executed
        upon creation and guiScene etc are not yet available.

        """

        # manual:

        self.label = QtWidgets.QLabel(self.contents)
        self.label.setText("Select a node to display its name")
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.dispPropTree)
        self.contents.setLayout(layout)



        # # or from a generated file
        # self.ui = DAVE.forms.widget_dynprop.Ui_widget_dynprop()
        # self.ui.setupUi(self.contents)



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
            self.label.setText(self.guiSelection[0].name)  # access to selected nodes

    def action(self):

        # never executed in the example
        self.guiRunCodeCallback("print('Hi, I am an exampe')", guiEventType.SELECTED_NODE_MODIFIED)   # call the callback to execute code
        self.guiSelectNode('Node-name') # to globally select a node
