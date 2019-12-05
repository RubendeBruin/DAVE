"""
This is an example/template of how to setup a new dockwidget
"""

"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Ruben de Bruin - 2019
"""

from DAVE.gui2.dockwidget import *
from PySide2 import QtGui, QtCore, QtWidgets
from DAVE.gui2.forms.widgetUI_modeshapes import Ui_ModeShapesWidget
import DAVE.scene as nodes
import DAVE.settings as ds
import DAVE.frequency_domain
import numpy as np

class WidgetModeShapes(guiDockWidget):

    def guiCreate(self):
        """
        Add gui components to self.contents

        Do not fill the controls with actual values here. This is executed
        upon creation and guiScene etc are not yet available.

        """

        # or from a generated file
        self.ui = Ui_ModeShapesWidget()
        self.ui.setupUi(self.contents)
        self.ui.btnCalc.pressed.connect(self.calc_modeshapes)
        self.ui.horizontalSlider.actionTriggered.connect(self.activate_modeshape)
        self.ui.sliderSize.actionTriggered.connect(self.activate_modeshape)
        self.ui.lblError.setText('')

    def guiProcessEvent(self, event):
        """
        Add processing that needs to be done.

        After creation of the widget this event is called with guiEventType.FULL_UPDATE
        """

        if event in [guiEventType.FULL_UPDATE,
                     guiEventType.MODEL_STRUCTURE_CHANGED,
                     guiEventType.SELECTED_NODE_MODIFIED]:
            self.gui.animation_terminate()
            self._shapes_calculated = False
            self.autocalc()

    def guiDefaultLocation(self):
        return QtCore.Qt.DockWidgetArea.TopDockWidgetArea

    # ======

    def autocalc(self):
        if self.ui.btnCalc.isChecked():
            self.calc_modeshapes()

    def calc_modeshapes(self):
        V, D = DAVE.frequency_domain.mode_shapes(self.guiScene)

        if V is not None:
            self.n_shapes = len(V)
        else:
            self.n_shapes = 0

        warnings = ''

        if np.any(np.iscomplex(V)):
            warnings += 'MASSLESS '
        else:
            V = np.real(V)

        if np.any(np.isnan(V)):
            warnings += ' UNCONTRAINED'

        self.ui.lblError.setText(warnings)

        self.ui.horizontalSlider.setMaximum(self.n_shapes - 1)
        self.omega = V
        self.shapes = D
        self._shapes_calculated = True

    def activate_modeshape(self):

        if not self._shapes_calculated:
            return

        i = self.ui.horizontalSlider.sliderPosition()
        scale = self.ui.sliderSize.sliderPosition() + 1
        scale = 1.05 ** (scale - 30)
        print('Activating mode-shape {} with scale {}'.format(i, scale))

        omega = self.omega[i]
        self.ui.lblPeriod.setText('{:.2f} s'.format(2 * np.pi / omega))
        self.ui.lblRads.setText('{:.2f} rad/s'.format(omega))

        shape = self.shapes[:,i]

        self.gui.animation_terminate()
        d0 = self.guiScene._vfc.get_dofs()

        n_frames = 100
        t_modeshape = 5

        dofs = DAVE.frequency_domain.generate_modeshape_dofs(d0,shape,scale,n_frames,scene=self.guiScene)
        t = np.linspace(0,t_modeshape, n_frames)
        self.gui.animation_start(t,dofs,True, d0)



