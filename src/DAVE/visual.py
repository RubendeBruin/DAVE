"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Ruben de Bruin - 2019

"""

# enforce PySide6 on vtk
import vtkmodules.qt
from vtkmodules.vtkIOImage import vtkPNGReader

vtkmodules.qt.PyQtImpl = "PySide6"

import logging
from warnings import warn

from DAVE.visual_helpers.scene_renderer import AbstractSceneRenderer

from DAVE.visual_helpers.actors import VisualActor
from DAVE.visual_helpers.constants import ActorType

from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtkmodules.vtkRenderingCore import vtkActor2D, vtkRenderer, vtkCamera, vtkRenderWindowInteractor, vtkRenderWindow, \
    vtkImageMapper
from vtkmodules.vtkRenderingOpenGL2 import vtkOpenGLFXAAPass, vtkSSAOPass

from DAVE.visual_helpers.vtkBlenderLikeInteractionStyle import BlenderStyle

from DAVE.settings_visuals import (
    COLOR_BG1,
)

import DAVE.scene as dn

"""

"""

from DAVE.visual_helpers.vtkHelpers import *


class EmbeddedViewport(AbstractSceneRenderer):
    """
    V

    """

    def __init__(self, scene):
        super().__init__(scene)

        """SSAO effect and passes"""
        self._ssao_on = False
        self.SSAO_fxaaP: vtkOpenGLFXAAPass or None = None
        self.SSAO_pass: vtkSSAOPass or None = None

        """These are the temporary visuals"""
        self.temporary_actors: list[vtkActor] = list()

        self.vtkWidget = None
        """Qt viewport, if any"""

        self.quick_updates_only = (
            False  # Do not perform slow updates ( make animations quicker)
        )

        self._wavefield = None
        """WaveField object"""


        self._create_SSAO_pass()

        # colorbar image
        png = vtkPNGReader()
        png.SetFileName(
            str(Path(__file__).parent / "resources" / "uc_colorbar_smaller.png")
        )
        png.Update()

        imagemapper = vtkImageMapper()
        imagemapper.SetInputData(png.GetOutput())
        imagemapper.SetColorWindow(255)
        imagemapper.SetColorLevel(127.5)

        image = vtkActor2D()
        image.SetMapper(imagemapper)
        image.SetPosition(0, 0.95)

        self.colorbar_actor = image
        """The colorbar for UCs is a static image"""

        self.cycle_next_painterset = None
        self.cycle_previous_painterset = None

        self.Style = BlenderStyle()
        self.Style.callbackCameraDirectionChanged = self._camera_direction_changed
        self.Style.callbackCameraMoved = self._camera_moved
        self.Style.callbackAnyKey = self.keyPressFunction

    #
    # def show_as_qt_app(self, painters=None):
    #     from PySide6.QtWidgets import QWidget, QApplication
    #
    #     app = QApplication.instance() or QApplication()
    #
    #     widget = QWidget()
    #
    #     if painters is None:
    #         from DAVE.settings_visuals import PAINTERS
    #
    #         painters = PAINTERS["Construction"]
    #
    #     v = self
    #
    #     v.settings.painter_settings = painters
    #
    #     v.show_embedded(widget)
    #     v.quick_updates_only = False
    #
    #     v.create_node_visuals()
    #
    #     v.position_visuals()
    #     v.add_new_node_actors_to_screen()  # position visuals may create new actors
    #     v.update_visibility()
    #
    #     v.zoom_all()
    #
    #     widget.show()
    #
    #     from PySide6.QtCore import QEventLoop
    #
    #     if not QEventLoop().isRunning():
    #         app.exec_()



