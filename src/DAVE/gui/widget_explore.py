"""
Explore widget
"""

"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Ruben de Bruin - 2019
"""

from DAVE.gui.dockwidget import *
from PySide2 import QtGui, QtCore, QtWidgets
from DAVE.gui.forms.widgetUI_explore import Ui_widgetExplore11
import DAVE.scene as nodes
import DAVE.settings as ds

class WidgetExplore(guiDockWidget):

    def guiCreate(self):
        """
        Add gui components to self.contents

        Do not fill the controls with actual values here. This is executed
        upon creation and guiScene etc are not yet available.

        """

        # # or from a generated file
        self.ui = Ui_widgetExplore11()
        self.ui.setupUi(self.contents)

        # triggers
        self.ui.editEvaluate.textChanged.connect(self.test_evaluation)
        self.ui.btnGoalSeek.clicked.connect(self.goalseek)
        self.ui.btnGraph.clicked.connect(self.plot)




    def guiProcessEvent(self, event):
        """
        Add processing that needs to be done.

        After creation of the widget this event is called with guiEventType.FULL_UPDATE
        """
        pass


    def guiDefaultLocation(self):
        return QtCore.Qt.DockWidgetArea.LeftDockWidgetArea

    # ======

    def test_evaluation(self):
        text = self.ui.editEvaluate.toPlainText()
        s = self.guiScene
        try:
            r = eval(text)

            try:
                f = float(r)
            except:
                raise Exception("Expression evaluates to: \n\n{} \n\nBut we need a (floating-point) number".format(r))

            self.ui.editResult.setPlainText(str(f) + "\n\nWell done :-)")
            self.ui.editResult.setStyleSheet("background-color: white;")
        except Exception as E:
            self.ui.editResult.setPlainText(str(E))
            self.ui.editResult.setStyleSheet("background-color: pink;")


    # ==== Goal-seel

    def goalseek(self):
        """Setup the goal-seek code and run"""

        # def goal_seek(self, set_node, set_property, target, change_node, change_property, bracket=None, tol=1e-3):

        # set is something like

        # s['node'].property

        set = self.ui.editSet.text()
        set = set.split('.')
        node = set[0][3:-2]
        property = set[1]

        code = 's.goal_seek(evaluate="{}",\n    target={},\n    change_property="{}",\n    change_node="{}")'.format(
            self.ui.editEvaluate.toPlainText(),
            self.ui.editTarget.value(),
            property,
            node)

        self.guiRunCodeCallback(code, guiEventType.MODEL_STATE_CHANGED)

    def plot(self):

        set = self.ui.editSet.text()
        set = set.split('.')
        node = set[0][3:-2]
        property = set[1]

        code = 's.plot_effect(evaluate="{}",\n   change_property="{}",\n    change_node="{}",\n    start={},\n    to={},\n    steps={})'.format(
            self.ui.editEvaluate.toPlainText(),
            property,
            node,
            self.ui.editFrom.value(), self.ui.editTo.value(), self.ui.editSteps.value())

        code += '\nimport matplotlib.pyplot as plt'
        code += '\nplt.show()'

        self.guiRunCodeCallback(code, guiEventType.NOTHING)