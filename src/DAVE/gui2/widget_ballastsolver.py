"""
Ballastsolver
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

class WidgetBallastSolver(guiDockWidget):

    def guiCreate(self):
        """
        Add gui components to self.contents

        Do not fill the controls with actual values here. This is executed
        upon creation and guiScene etc are not yet available.

        """
        # or from a generated file
        self.ui = Ui_BallastSolver()
        self.ui.setupUi(self.contents)

        self._vesselNode = None
        self.ui.comboBox.currentTextChanged.connect(self.ballast_system_selected)
        self.ui.pushButton.pressed.connect(self.determineRequiredBallast)
        self.ui.pushButton_2.pressed.connect(self.solveBallast)


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
                    self.ui.comboBox.setCurrentText(self.guiSelection[0].name)


    def guiDefaultLocation(self):
        return QtCore.Qt.DockWidgetArea.LeftDockWidgetArea

    # ======

    def fill(self):
        # get all ballast-systems
        self.ui.comboBox.clear()
        for bs in self.guiScene.nodes_of_type(nodes.BallastSystem):
            self.ui.comboBox.addItem(bs.name)

        if self.guiSelection:
            if isinstance(self.guiSelection[0], nodes.BallastSystem):
                self.ui.comboBox.setCurrentText(self.guiSelection[0].name)


    def ballast_system_selected(self):
        name = self.ui.comboBox.currentText()
        try:
            bs = self.guiScene[name]
        except ValueError:
            return

        self._vesselNode = bs.parent
        self.ui.label_4.setText(self._vesselNode.name)

    def determineRequiredBallast(self):

        code = 's["{}"].empty_all_usable_tanks()\n'.format(self.ui.comboBox.currentText())
        code += 's.required_ballast = force_vessel_to_evenkeel_and_draft(scene=s,vessel="{}",z={})'.format(self._vesselNode.name, self.ui.doubleSpinBox.value())
        self.guiRunCodeCallback(code, guiEventType.MODEL_STATE_CHANGED)
        self.ui.tableWidget.item(0,0)
        self.ui.tableWidget.setItem(0, 0, QtWidgets.QTableWidgetItem(str(-self.guiScene.required_ballast[0])))
        self.ui.tableWidget.setItem(0, 1, QtWidgets.QTableWidgetItem(str(self.guiScene.required_ballast[1])))
        self.ui.tableWidget.setItem(0, 2, QtWidgets.QTableWidgetItem(str(self.guiScene.required_ballast[2])))

    def solveBallast(self):
        code = 'bss = BallastSystemSolver(s["{}"])\n'.format(self.ui.comboBox.currentText())
        code += 'bso.ballast_to(cogx = s.required_ballast[1], cogy = s.required_ballast[2], weight = -s.required_ballast[0])'
        self.guiRunCodeCallback(code,guiEventType.MODEL_STATE_CHANGED)

