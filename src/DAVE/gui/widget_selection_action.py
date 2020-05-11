"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Ruben de Bruin - 2019
"""

from DAVE.gui.dockwidget import *
from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtWidgets import QPushButton
import DAVE.scene as nodes
import DAVE.settings as ds
from DAVE.gui.forms.widget_selection_actions import Ui_SelectionActions

class WidgetSelectionActions(guiDockWidget):

    def guiCreate(self):
        """
        Add gui components to self.contents

        Do not fill the controls with actual values here. This is executed
        upon creation and guiScene etc are not yet available.

        """

        # # or from a generated file
        self.ui = Ui_SelectionActions()
        self.ui.setupUi(self.contents)

        layout = QtWidgets.QVBoxLayout()
        self.ui.frame.setLayout(layout)


        self.buttons = []



    def guiProcessEvent(self, event):
        """
        Add processing that needs to be done.

        After creation of the widget this event is called with guiEventType.FULL_UPDATE
        """

        if event in [guiEventType.SELECTION_CHANGED]:
            self.fill()

    def guiDefaultLocation(self):
        return None # QtCore.Qt.DockWidgetArea.RightDockWidgetArea

    # ======

    def find_nodes(self, types):
        r = []
        source = self.guiSelection.copy()

        for t in types:
            for s in source:
                if isinstance(s, t):
                    r.append(s)
                    source.remove(s)
                    break

        if len(r) == len(types):
            return r
        else:
            return None



    def fill(self):

        # display the name of the selected node
        text = ''
        for node in self.guiSelection:
            text += ' ' + node.name

        self.ui.label.setText(text)

        for button in self.buttons:
            button.deleteLater()

        self.buttons.clear()


        if self.find_nodes([nodes.Poi, nodes.Poi]):
            self.ui.label.setText('Two pois')
            self.buttons.append(QPushButton('Create cable', self.ui.frame))



        for button in self.buttons:
            self.ui.frame.layout().addWidget(button)






