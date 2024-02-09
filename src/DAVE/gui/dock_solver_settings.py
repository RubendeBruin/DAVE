"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Ruben de Bruin - 2023
"""

from DAVE.gui.dock_system.dockwidget import *
from dataclasses import fields

from DAVE.gui.helpers.property_editor import PropertyEditorPopup, PropertyEditorWidget
from DAVE.settings import SolverSettings


class WidgetSolverSettings(guiDockWidget):
    def guiCreate(self):
        """
        Add gui components to self.contents

        Do not fill the controls with actual values here. This is executed
        upon creation and guiScene etc are not yet available.

        """
        self._created = False

    def getter_callback(self, name):
        return getattr(self.guiScene.solver_settings, name)

    def setter_callback(self, name, value):
        code = f"s.solver_settings.{name} = {value}"
        self.guiRunCodeCallback(code, guiEventType.NOTHING)

    def guiProcessEvent(self, event):
        """
        Add processing that needs to be done.

        After creation of the widget this event is called with guiEventType.FULL_UPDATE
        """

        if self._created and event in [
            guiEventType.FULL_UPDATE,
        ]:
            self.editor_widget.load_data()

        if self._created:
            return

        names = [k.name for k in fields(SolverSettings)]
        types = [k.type for k in fields(SolverSettings)]
        info = names

        assert names  == ['timeout_s',
                 'mobility',
                 'tolerance',
                 'max_newton_iterations',
                 'do_linear_first',
                 'tolerance_during_linear_phase',
                 'do_local_descent',
                 'do_newton',
                 'do_global_descent',
                 'up_is_up_factor',
                 'do_deterministic',
                 'deterministic_global_steps',
                 'deterministic_local_steps'], "SolverSettings has changed, please update dock_solver_settings.py"

        info = ['maximum time in seconds to run solver',
                 '0..100, higher is faster, but less stable',
                 'tolerance',
                 'maximum number of newton iterations (local solver)',
                 'solve translations DOFs before rotations',
                 'tolerance during translations phase',
                 'use local descent solver',
                 'use local (newton) solver',
                 'use global descent solver',
                 '0...1, attempt to restrict flipping over, <0 for no restriction',
                 'use fixed relative cycle counts for solvers (instead of first available)',
                 'fixed cycle counts for global descent solver',
                 'fixed cycle counts for local descent solver']


        self.editor_widget = PropertyEditorWidget(
            prop_names=names,
            prop_types=types,
            getter_callback=self.getter_callback,
            setter_callback=self.setter_callback,
            info=info,
            parent=self,
        )

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.editor_widget)
        self.contents.setLayout(layout)

        self._created = True

    def guiDefaultLocation(self):
        return PySide6QtAds.DockWidgetArea.RightDockWidgetArea
