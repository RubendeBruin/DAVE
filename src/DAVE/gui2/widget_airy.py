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
import DAVE.gui2.forms.widgetUI_airy
from PySide2 import QtGui, QtCore, QtWidgets
import DAVE.scene as nodes
import DAVE.settings as ds
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
        self.ui = DAVE.gui2.forms.widgetUI_airy.Ui_frmAiryWave()
        self.ui.setupUi(self.contents)
        self.d0 = None

        self.ui.heading.valueChanged.connect(self.action)
        self.ui.amplitude.valueChanged.connect(self.action)
        self.ui.period.valueChanged.connect(self.action)
        self.ui.pushButton.pressed.connect(self.prepare_for_wave_interaction)
        self.ui.pushButton_2.pressed.connect(self.plot_raos)

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

    def prepare_for_wave_interaction(self):
        self.guiRunCodeCallback('prepare_for_fd(s)',guiEventType.MODEL_STRUCTURE_CHANGED)

    def plot_raos(self):

        code = """wave_direction = 90
min = 0.01
max = 4
steps = 100
plot_RAO_1d(s, np.linspace(min,max,steps), wave_direction)
plt.show()
"""

        self.guiRunCodeCallback(code, guiEventType.NOTHING)



    def action(self):

        if self.d0 is None:
            raise ValueError('No equilibrium position available')

        wave_direction = self.ui.heading.value()
        amplitude = self.ui.amplitude.value()
        period = self.ui.period.value()
        x = fd.RAO_1d(s=self.guiScene, omegas =2 * np.pi / period, wave_direction=wave_direction)

        n_frames = int(60*period)

        self.ui.label.setText(str(wave_direction) + '[deg]')

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
                            nx = 100, ny = 100, dx=200,dy=200)

        self.gui.animation_terminate()
        self.gui.visual.add_dynamic_wave_plane(wf)
        self.gui.animation_start(t, dofs, True, self.d0)





