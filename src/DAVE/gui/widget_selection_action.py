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
        return QtCore.Qt.DockWidgetArea.RightDockWidgetArea

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

    def all_of_type(self, types):
        source = self.guiSelection.copy()

        r = None

        for t in types:
            check = [isinstance(e, t) for e in source]
            if r is None:
                r = check
            else:
                r = np.logical_or(r, check)

        if np.all(r):
            return source
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

        name = self.guiScene.available_name_like("quick_action")

        # Here we manually define all the possible quick-actions
        #
        # each quick-action defines its own button

        # p2 = self.find_nodes([nodes.Poi, nodes.Poi])
        # if p2:
        #     button = QPushButton('Create cable', self.ui.frame)
        #
        #     code = f's.new_cable("{name}", poiA="{p2[0].name}", poiB = "{p2[1].name}")'
        #     button.pressed.connect(lambda : self.guiRunCodeCallback(code, guiEventType.MODEL_STRUCTURE_CHANGED))
        #
        #     self.buttons.append(button)

        # creating cables between points and sheaves
        poi_and_sheave = self.all_of_type([Poi, Sheave])
        if poi_and_sheave:
            if len(poi_and_sheave) > 1:
                if len(poi_and_sheave) > 2:
                    names = ''.join([f'"{e.name}",' for e in poi_and_sheave[1:-1]])
                    sheaves = f', sheaves = [{names[:-1]}]'
                    button = QPushButton('Create cable with sheaves', self.ui.frame)
                else:
                    sheaves = ''
                    button = QPushButton('Create cable', self.ui.frame)

                code = f's.new_cable("{name}", poiA="{poi_and_sheave[0].name}", poiB = "{poi_and_sheave[-1].name}"{sheaves})'
                button.pressed.connect(lambda: self.guiRunCodeCallback(code, guiEventType.MODEL_STRUCTURE_CHANGED))

                self.buttons.append(button)

        # add all buttons to the layout

        for button in self.buttons:
            self.ui.frame.layout().addWidget(button)






