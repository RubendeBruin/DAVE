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
from DAVE.gui.forms.widget_stability_displUI import Ui_WidgetDispDrivenStability
import DAVE.scene as nodes
import DAVE.settings as ds
import numpy as np

class WidgetDisplacedStability(guiDockWidget):

    def guiCreate(self):
        """
        Add gui components to self.contents

        Do not fill the controls with actual values here. This is executed
        upon creation and guiScene etc are not yet available.

        """

        # or from a generated file
        self.ui = Ui_WidgetDispDrivenStability()
        self.ui.setupUi(self.contents)

        self.ui.stability_go.clicked.connect(self.action)
        self.ui.pushButton.clicked.connect(self.movie)

        self._previously_selected = None


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
        self.ui.node_name.clear()

        # try to intelligently select the right axis
        #
        # Indicators are:
        # - axis is free
        # - axis has a buoyancy module or hydspring as child
        # - axis does not have a parent

        axis = self.guiScene.nodes_of_type(nodes.Axis)
        if axis:
            names = [a.name for a in axis]
            score = dict.fromkeys(names, 0)

            score_no_parent = 1
            score_free = 5
            score_buoyancy_child = 3

            for a in axis:
                if a.parent is None:
                    score[a.name] += score_no_parent
                if not np.any(a.fixed): # all are False
                    score[a.name] += score_free

            for bs in [*self.guiScene.nodes_of_type(nodes.Buoyancy), *self.guiScene.nodes_of_type(nodes.HydSpring)]:
                score[bs.parent.name] += score_buoyancy_child

            # find the winner
            most_likely_vessel = axis[0].name
            max_score = 0

            for key, value in score.items():
                if value > max_score:
                    most_likely_vessel = key
                    max_score = value

            self.ui.node_name.addItems(names)

            if self._previously_selected not in names:
                self._previously_selected = None

            if self._previously_selected:
                self.ui.node_name.setCurrentText(self._previously_selected)
            else:
                self.ui.node_name.setCurrentText(most_likely_vessel)



    def action(self):

        self.gui.savepoint_restore()

        self._previously_selected = self.ui.node_name.currentText()

        code = 'from DAVE.marine import GZcurve_DisplacementDriven\n'
        code += """GZcurve_DisplacementDriven(scene = s,
                    noshow = True,
                    vessel_node = "{}",
                    displacement_kN={},
                    minimum_heel= {},
                    maximum_heel={},
                    steps={},
                    teardown={},
                    allow_surge={},
                    allow_sway={},
                    allow_yaw={},
                    allow_trim={})""".format(self.ui.node_name.currentText(),
                                             self.ui.stability_displacement.value(),
                                             self.ui.stability_heel_start.value(),
                                             self.ui.stability_heel_max.value(),
                                             self.ui.stability_n_steps.value(),
                                             self.ui.stability_do_teardown.isChecked(),
                                             self.ui.stability_surge.isChecked(),
                                             self.ui.stability_sway.isChecked(),
                                             self.ui.stability_yaw.isChecked(),
                                             self.ui.stability_trim.isChecked())

        self.guiRunCodeCallback(code, guiEventType.NOTHING)   # call the callback to execute code

        import matplotlib.pyplot as plt
        plt.show()

    def movie(self):


        self.gui.savepoint_restore()
        self.guiScene.savepoint_make()

        self._previously_selected = self.ui.node_name.currentText()

        self.guiScene._gui_stability_dofs = None

        code = 'from DAVE.marine import GZcurve_DisplacementDriven\n'
        code += """GZcurve_DisplacementDriven(scene = s,
                    noshow = True,
                    vessel_node = "{}",
                    displacement_kN={},
                    minimum_heel= {},
                    maximum_heel={},
                    steps={},
                    teardown=False,
                    allow_surge={},
                    allow_sway={},
                    allow_yaw={},
                    allow_trim={})""".format(self.ui.node_name.currentText(),
                                             self.ui.stability_displacement.value(),
                                             self.ui.stability_heel_start.value(),
                                             self.ui.stability_heel_max.value(),
                                             self.ui.stability_n_steps.value(),
                                             self.ui.stability_surge.isChecked(),
                                             self.ui.stability_sway.isChecked(),
                                             self.ui.stability_yaw.isChecked(),
                                             self.ui.stability_trim.isChecked())

        self.guiRunCodeCallback(code, guiEventType.NOTHING)   # call the callback to execute code

        # See if a movie was produced
        if self.guiScene._gui_stability_dofs is not None:
            d0 = self.guiScene._vfc.get_dofs()
            n = len(self.guiScene._gui_stability_dofs)
            t = range(n)
            self.gui.animation_start(t, self.guiScene._gui_stability_dofs, True, d0, do_not_reset_time=True)



