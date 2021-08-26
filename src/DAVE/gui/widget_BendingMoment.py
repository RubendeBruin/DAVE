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
from DAVE.visual import create_momentline_actors, create_shearline_actors
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

        self.ui.pbBending.clicked.connect(lambda : self._action(True))
        self.ui.pbShear.clicked.connect(lambda : self._action(False))

    def guiProcessEvent(self, event):
        """
        Add processing that needs to be done.

        After creation of the widget this event is called with guiEventType.FULL_UPDATE
        """

        if event in [guiEventType.FULL_UPDATE,
                     guiEventType.MODEL_STRUCTURE_CHANGED]:
            self.fill()


    def guiDefaultLocation(self):
        return QtCore.Qt.DockWidgetArea.RightDockWidgetArea

    # ======

    def fill(self):

        axes = [n.name for n in self.guiScene.nodes_of_type((nodes.Frame, nodes.RigidBody))]

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

    def _action(self, bending):

        self.gui.visual.remove_temporary_actors()

        target = self.ui.cbAxis.currentText()
        orientation = self.ui.cbOrientation.currentText()

        if orientation == 'Same as reported':
            orientation = target

        target = self.guiScene[target]
        orientation = self.guiScene[orientation]

        self.guiScene.update()

        scale = self.ui.sbScale.value()

        if bending:
            actor_axis, actor_graph = create_momentline_actors(target, scale_to=scale, at=orientation)
        else:
            actor_axis, actor_graph = create_shearline_actors(target, scale_to=scale, at=orientation)

        self.gui.visual.add_temporary_actor(actor_axis)
        self.gui.visual.add_temporary_actor(actor_graph)

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



