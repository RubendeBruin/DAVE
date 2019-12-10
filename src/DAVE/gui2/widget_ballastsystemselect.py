"""
WidgetBallastSystemSelect
"""

"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Ruben de Bruin - 2019
"""

from DAVE.gui2.dockwidget import *
from PySide2 import QtGui, QtCore, QtWidgets
from DAVE.gui2.forms.widgetUI_ballastsolver import Ui_BallastSolver
import DAVE.scene as nodes
import DAVE.settings as ds
from DAVE.solvers.ballast import force_vessel_to_evenkeel_and_draft, BallastSystemSolver

class WidgetBallastSystemSelect(guiDockWidget):

    def guiCreate(self):
        """
        Add gui components to self.contents

        Do not fill the controls with actual values here. This is executed
        upon creation and guiScene etc are not yet available.

        """
        self.label0 = QtWidgets.QLabel(self.contents)
        self.label0.setText("Select ballast system:")

        self.comboBox = QtWidgets.QComboBox(self.contents)
        self.label = QtWidgets.QLabel(self.contents)
        self.label.setText("On vessel [XXXXX]")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.label0)
        layout.addWidget(self.comboBox)
        layout.addWidget(self.label)
        self.contents.setLayout(layout)

        self.resize(0,20)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())

        self.comboBox.currentTextChanged.connect(self.ballast_system_selected)


    def guiProcessEvent(self, event):
        """
        Add processing that needs to be done.

        After creation of the widget this event is called with guiEventType.FULL_UPDATE
        """

        if event in [guiEventType.FULL_UPDATE, guiEventType.MODEL_STRUCTURE_CHANGED]:
            self.fill()

        if event == guiEventType.SELECTION_CHANGED:
            if self.guiSelection:
                if isinstance(self.guiSelection[0], nodes.BallastSystem):
                    if self.comboBox.currentText() != self.guiSelection[0].name:
                        self.comboBox.setCurrentText(self.guiSelection[0].name)


    def guiDefaultLocation(self):
        return QtCore.Qt.DockWidgetArea.LeftDockWidgetArea

    # ======

    def fill(self):
        # get all ballast-systems
        self.comboBox.clear()
        for bs in self.guiScene.nodes_of_type(nodes.BallastSystem):
            self.comboBox.addItem(bs.name)

        if self.guiSelection:
            if isinstance(self.guiSelection[0], nodes.BallastSystem):
                self.comboBox.setCurrentText(self.guiSelection[0].name)


    def ballast_system_selected(self):
        name = self.comboBox.currentText()
        try:
            bs = self.guiScene[name]
            self.label.setText("on vessel '{}'".format(bs.parent.name))
        except ValueError:
            return

        self.guiSelection.clear()
        self.guiSelection.append(bs)
        self.guiEmitEvent(guiEventType.SELECTION_CHANGED)
