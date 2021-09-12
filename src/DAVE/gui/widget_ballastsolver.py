"""
Ballastsolver
"""

"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Ruben de Bruin - 2019
"""

from DAVE.gui.dockwidget import *
from PySide2 import QtGui, QtCore, QtWidgets
from DAVE.gui.forms.widgetUI_ballastsolver import Ui_BallastSolver
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
        self._bs = None             # selected ballast system

        self.ui.pushButton.clicked.connect(self.determineRequiredBallast)
        self.ui.pushButton_2.clicked.connect(self.solve_method1)
        self.ui.pushButton_3.clicked.connect(self.solve_method2)
        self.ui.doubleSpinBox.valueChanged.connect(self.determineRequiredBallast)

        self.ui.widget_2.setEnabled(False)


    def guiProcessEvent(self, event):
        """
        Add processing that needs to be done.

        After creation of the widget this event is called with guiEventType.FULL_UPDATE
        """

        if event in [guiEventType.FULL_UPDATE, guiEventType.SELECTION_CHANGED]:
            self.ballast_system_selected()




    def guiDefaultLocation(self):
        return QtCore.Qt.DockWidgetArea.LeftDockWidgetArea

    # ======

    def assert_selection_valid(self):
        try:
            self.guiScene[self._bs.name]
            return True
        except:
            print('Please select a ballast system first')
            return False

    def ballast_system_selected(self):
        if self.guiSelection:
            if isinstance(self.guiSelection[0], nodes.BallastSystem):
                self._bs = self.guiSelection[0]
                self._vesselNode = self._bs.parent

                self.ui.label_4.setText(self._vesselNode.name)

    def determineRequiredBallast(self):
        if not self.assert_selection_valid():
            return

        # code = 'from DAVE.solvers.ballast import force_vessel_to_evenkeel_and_draft'
        # code += '\ns["{}"].empty_all_usable_tanks()'.format(self._bs.name)
        # code += '\ns.required_ballast = force_vessel_to_evenkeel_and_draft(scene=s,vessel="{}",z={})'.format(self._vesselNode.name, self.ui.doubleSpinBox.value())
        #
        code = f"s['{self._bs.name}'].target_elevation = {self.ui.doubleSpinBox.value()}"

        self.guiRunCodeCallback(code, guiEventType.MODEL_STATE_CHANGED)
        self.ui.tableWidget.item(0,0)
        self.ui.tableWidget.setItem(0, 0, QtWidgets.QTableWidgetItem(f'{-self._bs._target_weight:.3f}'))
        self.ui.tableWidget.setItem(0, 1, QtWidgets.QTableWidgetItem(f'{self._bs._target_cog[0]:.3f}'))
        self.ui.tableWidget.setItem(0, 2, QtWidgets.QTableWidgetItem(f'{self._bs._target_cog[1]:.3f}'))

        self.ui.widget_2.setEnabled(True)

    def solve_method1(self):
        self.solveBallast(method=1)

    def solve_method2(self):
        self.solveBallast(method=2)

    def solveBallast(self, method=1):
        if not self.assert_selection_valid():
            return


        code = f"s['{self._bs.name}'].solve_ballast(method={method}, use_current_fill={self.ui.cbUseCurrentFills.isChecked()})"

        self.guiRunCodeCallback(code,guiEventType.SELECTED_NODE_MODIFIED)

    def draftChanged(self):
        self.determineRequiredBallast()
        self.solveBallast()

