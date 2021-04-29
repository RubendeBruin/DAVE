"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Ruben de Bruin - 2019
"""

from DAVE.gui.dockwidget import *
import DAVE.gui.forms.widgetUI_airy
from PySide2 import QtCore
import DAVE.frequency_domain as fd
import numpy as np
from mafredo.helpers import wavelength

class WidgetAiry(guiDockWidget):

    def guiCreate(self):
        """
        Add gui components to self.contents

        Do not fill the controls with actual values here. This is executed
        upon creation and guiScene etc are not yet available.
        """

        # # or from a generated file
        self.ui = DAVE.gui.forms.widgetUI_airy.Ui_frmAiryWave()
        self.ui.setupUi(self.contents)
        self.d0 = None

        self.ui.heading.valueChanged.connect(self.action)
        self.ui.amplitude.valueChanged.connect(self.action)
        self.ui.period.valueChanged.connect(self.action)
        self.ui.pushButton_2.clicked.connect(self.plot_raos)

    def guiProcessEvent(self, event):
        """
        Add processing that needs to be done.

        After creation of the widget this event is called with guiEventType.FULL_UPDATE
        """

        if event in [guiEventType.FULL_UPDATE,
                     guiEventType.MODEL_STRUCTURE_CHANGED,
                     guiEventType.SELECTED_NODE_MODIFIED]:

            self.gui.animation_terminate()
            if self.guiScene.verify_equilibrium():
                self.d0 = self.guiScene._vfc.get_dofs()
            else:
                self.d0 = None

    def guiDefaultLocation(self):
        return QtCore.Qt.DockWidgetArea.LeftDockWidgetArea

    # ======


    def plot_raos(self):

        code = """from DAVE.frequency_domain import plot_RAO_1d
import matplotlib.pyplot as plt
wave_direction = 90
min = 0.01
max = 4
steps = 100
plot_RAO_1d(s, np.linspace(min,max,steps), wave_direction)
plt.show()
"""

        self.guiRunCodeCallback(code, guiEventType.NOTHING)



    def action(self):

        if self.d0 is None:

            if self.guiScene.verify_equilibrium():
                self.d0 = self.guiScene._vfc.get_dofs()

            else:
                self.guiScene.solve_statics()
                if self.guiScene.verify_equilibrium():
                    self.d0 = self.guiScene._vfc.get_dofs()
                else:
                    raise ValueError('No equilibrium position available')
        else:
            self.guiScene._vfc.set_dofs(self.d0)

        self.guiScene.solve_statics()

        wave_direction = self.ui.heading.value()
        amplitude = self.ui.amplitude.value()
        period = self.ui.period.value()

        try:
            x = fd.RAO_1d(s=self.guiScene, omegas =2 * np.pi / period, wave_direction=wave_direction)
        except Exception as m:
            self.gui.show_exception(m)
            return

        n_frames = int(60*period)

        self.ui.lblHeading.setText(str(wave_direction) + '[deg]')
        dofs = fd.generate_unitwave_response(s=self.guiScene, d0 = self.d0, rao=x[:,0], wave_amplitude=amplitude, n_frames=n_frames)
        t = np.linspace(0, period, n_frames)


        import DAVE.visual

        omega = 2*np.pi / period
        wave_length = wavelength(omega,0) # infinite waterdepth

        wf = DAVE.visual.WaveField()
        wf.create_waveplane(wave_direction=wave_direction,
                            wave_amplitude=amplitude,
                            wave_length=wave_length,
                            wave_period = period,
                            nt = n_frames,
                            nx = 50, ny = 50, dx=400,dy=400)

        self.gui.animation_terminate()
        self.gui.visual.add_dynamic_wave_plane(wf)
        self.gui.animation_start(t, dofs, True, self.d0)





