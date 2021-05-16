"""
This is an example/template of how to setup a new dockwidget
"""
import subprocess

"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Ruben de Bruin - 2019
"""

from DAVE.gui.dockwidget import *
from DAVE.gui.forms.widget_bendingmomentpreview import Ui_WidgetBendingMomentPreview
from PySide2 import QtGui, QtCore, QtWidgets
import DAVE.scene as nodes
import vedo as vd
from DAVE import settings

class WidgetBendingMoment(guiDockWidget):

    def guiCreate(self):
        """
        Add gui components to self.contents

        Do not fill the controls with actual values here. This is executed
        upon creation and guiScene etc are not yet available.

        """
        self.ui = Ui_WidgetBendingMomentPreview()
        self.ui.setupUi(self.contents)

        self.actor_axis = None
        self.actor_graph = None

        self.ui.pbReport.clicked.connect(self.write_report)

        self.ui.rbBending.toggled.connect(self.action)
        self.ui.rbShear.toggled.connect(self.action)
        self.ui.rbNothing.toggled.connect(self.action)
        self.ui.sbScale.valueChanged.connect(self.action)
        self.ui.cbAxis.currentIndexChanged.connect(self.action)
        self.ui.cbOrientation.currentIndexChanged.connect(self.action)


    def guiProcessEvent(self, event):
        """
        Add processing that needs to be done.

        After creation of the widget this event is called with guiEventType.FULL_UPDATE
        """

        if event in [guiEventType.FULL_UPDATE,
                     guiEventType.MODEL_STRUCTURE_CHANGED]:
            self.fill()
        if event in [guiEventType.MODEL_STRUCTURE_CHANGED,
                     guiEventType.MODEL_STATE_CHANGED,
                     guiEventType.SELECTED_NODE_MODIFIED]:
            self.autoupdate()

    def guiDefaultLocation(self):
        return QtCore.Qt.DockWidgetArea.RightDockWidgetArea

    # ======

    def fill(self):

        axes = [n.name for n in self.guiScene.nodes_of_type((nodes.Axis, nodes.RigidBody))]

        self.ui.cbAxis.blockSignals(True)
        self.ui.cbOrientation.blockSignals(True)

        _axis = self.ui.cbAxis.currentText()
        _orientation = self.ui.cbOrientation.currentText()

        self.ui.cbAxis.clear()
        self.ui.cbAxis.addItems(axes)
        self.ui.cbOrientation.clear()
        self.ui.cbOrientation.addItems(['Same as reported', *axes])

        if _axis:
            self.ui.cbAxis.setCurrentText(_axis)
        if _orientation:
            self.ui.cbOrientation.setCurrentText(_orientation)

        self.ui.cbAxis.blockSignals(False)
        self.ui.cbOrientation.blockSignals(False)

    def autoupdate(self):
        if self.ui.cbLiveUpdates.isChecked():
            self.action()

    def action(self):

        if self.actor_graph is not None:
            self.gui.visual.screen.remove(self.actor_graph)
        if self.actor_axis is not None:
            self.gui.visual.screen.remove(self.actor_axis)

        if self.ui.rbNothing.isChecked():
            return

        target = self.ui.cbAxis.currentText()
        orientation = self.ui.cbOrientation.currentText()

        if orientation == 'Same as reported':
            orientation = target

        target = self.guiScene[target]
        orientation = self.guiScene[orientation]

        self.guiScene.update()

        lsm = target.give_load_shear_moment_diagram(orientation)

        x,Fz, My = lsm.give_shear_and_moment()

        report_axis = self.guiScene.new_axis('__moment_graph_dummy_axis')
        report_axis.position = target.position
        report_axis.rotation = orientation.rotation

        start = report_axis.to_glob_position((x[0],0,0))
        end = report_axis.to_glob_position((x[-1], 0, 0))

        n = len(x)
        scale = self.ui.sbScale.value()

        if self.ui.rbBending.isChecked():
            value = My
            color = 'green'
        elif self.ui.rbShear.isChecked():
            value = Fz
            color = 'blue'
        else:
            raise ValueError('Cannot be here')

        scale = scale / np.max(np.abs(value))
        line = [report_axis.to_glob_position((x[i], 0, scale * value[i])) for i in range(n)]

        self.guiScene.delete('__moment_graph_dummy_axis')

        # add to screen
        self.actor_axis = vd.Line((start, end)).c('black')
        self.actor_graph = vd.Line(line).c(color)

        self.gui.visual.screen.add(self.actor_axis)
        self.gui.visual.screen.add(self.actor_graph)

        self.gui.visual.refresh_embeded_view()

    def write_report(self):

        element = self.ui.cbAxis.currentText()
        orientation = self.ui.cbOrientation.currentText()

        if orientation == 'Same as reported':
            target = ""
        else:
            target = f'axis_system = s["{orientation}"]'

        filename = settings.PATH_TEMP / "lsm.pdf"
        code = "s.solve_statics()\n"
        code += f's["{element}"].give_load_shear_moment_diagram({target}).plot(filename = r"{filename}")'
        self.guiRunCodeCallback(code, None)

        command = 'explorer "{}"'.format(filename)
        subprocess.Popen(command)



