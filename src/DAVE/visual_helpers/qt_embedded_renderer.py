import numpy as np

# enforce PySide6 on vtk
import vtkmodules.qt
from vtkmodules.vtkInteractionWidgets import (
    vtkOrientationMarkerWidget,
    vtkCameraOrientationWidget,
)
from vtkmodules.vtkRenderingAnnotation import vtkAxesActor

from DAVE.settings_visuals import ViewportSettings

vtkmodules.qt.PyQtImpl = "PySide6"

from PySide6.QtWidgets import QWidget, QVBoxLayout, QApplication
from DAVE.visual_helpers.vtkBlenderLikeInteractionStyle import BlenderStyle

from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from vtkmodules.vtkRenderingCore import (
    vtkRenderer,
    vtkRenderWindow,
    vtkCamera,
    vtkPropCollection,
)
from vtkmodules.vtkRenderingOpenGL2 import (
    vtkOpenGLRenderer,
    vtkOpenGLFXAAPass,
    vtkSSAOPass,
    vtkSequencePass,
    vtkRenderStepsPass,
    vtkRenderPassCollection,
)

from DAVE.visual_helpers.constants import ActorType, COLOR_BG1_GUI
from DAVE.visual_helpers.scene_renderer import AbstractSceneRenderer


class QtEmbeddedSceneRenderer(AbstractSceneRenderer):
    def __init__(
        self, scene, target_widget: QWidget, settings: ViewportSettings or None = None
    ):
        # these can be assigned
        self.cycle_next_painterset = None
        self.cycle_previous_painterset = None
        self.mouseRightEvent = None

        self.target_widget = target_widget  # used in create_rendering_pipeline

        self.Style = BlenderStyle()

        super().__init__(scene, settings=settings)

        self.add_axis_widget()
        self.interactor.Initialize()  # do this after the style is set and the renderers are added

        # privates
        self._ssao_on = False
        self._wavefield = None
        self._create_SSAO_pass()

        #

    def create_rendering_pipeline(
        self,
    ) -> tuple[vtkRenderer, list[vtkRenderer], vtkCamera, vtkRenderWindow]:
        """Creates the rendering pipeline for the viewport"""

        vl = QVBoxLayout()
        self.target_widget.setLayout(vl)

        margin = 1
        vl.setContentsMargins(
           margin, margin, margin, margin
        )  # leave a small border such that we can see the outline when we have the focus

        renderer = vtkOpenGLRenderer()

        renderer.SetBackground(COLOR_BG1_GUI)

        self.vtkWidget = QVTKRenderWindowInteractor()
        vl.addWidget(self.vtkWidget)

        # change the color of the parent widget when the interactor gets/looses focus
        self.vtkWidget.focusInEvent = self.get_focus
        self.vtkWidget.focusOutEvent = self.focus_lost

        renwin = self.vtkWidget.GetRenderWindow()
        renwin.AddRenderer(renderer)

        iren = renwin.GetInteractor()
        self.interactor = iren

        # apply style
        self.Style.callbackCameraDirectionChanged = self._camera_direction_changed
        self.Style.callbackCameraMoved = self._camera_moved
        self.Style.callbackAnyKey = self.keyPressFunction

        style = self.Style
        iren.SetInteractorStyle(style)
        # iren.Initialize()  # not here, do it after the entire pipeline is set up and the PBR is set

        camera = renderer.GetActiveCamera()

        return renderer, [renderer], camera, renwin

    def get_focus(self, *args):
        self.target_widget.setStyleSheet("border: 1px solid palette(dark);")

    def focus_lost(self, *args):
        self.target_widget.setStyleSheet("border: 1px solid palette(light); ")

    def _camera_moved(self):
        if self._ssao_on:
            self._update_SSAO_settings()

    def show(self):
        self.interactor.Start()

    def focus_on(self, position):
        """Places the camera focus on position"""

        c = self.camera
        cur_focus = np.array(c.GetFocalPoint())
        if np.linalg.norm(cur_focus - np.array(position)) < 1e-3:
            # already has focus, zoom in
            distance = np.array(c.GetPosition()) - cur_focus
            c.SetPosition(cur_focus + 0.9 * distance)
            self.renderer.ResetCameraClippingRange()
        else:
            self.camera.SetFocalPoint(position)

    def keyPressFunction(self, key):
        """Most key-pressed are handled by the Style,

        here we override some specific ones.

        Returning True make the style ignore the key-press

        """
        KEY = key.upper()

        if KEY == "A":
            self.zoom_all()
            self.refresh_embeded_view()
            return True

        if KEY == "BRACKETLEFT":
            if self.cycle_next_painterset is not None:
                self.cycle_next_painterset()
                return True

        if KEY == "BRACKETRIGHT":
            if self.cycle_previous_painterset is not None:
                self.cycle_previous_painterset()
                return True

    def refresh_embeded_view(self):
        if self.vtkWidget is not None:
            self.vtkWidget.update()

    def onMouseRight(self, info):
        if self.mouseRightEvent is not None:
            self.mouseRightEvent(info)

    def initialize_node_drag(self, nodes, text_info=None):
        # Initialize dragging on selected node

        actors = []
        outlines = []

        for node in nodes:
            node_actor = self.actor_from_node(node)
            if node_actor is not None:
                actors.extend([*node_actor.actors.values()])
                outlines.extend(
                    [
                        ol.outline_actor
                        for ol in self.node_outlines
                        if ol.outlined_actor in actors
                    ]
                )

        self.Style.StartDragOnProps([*actors, *outlines], info_text=text_info)

    ## SSAO

    def _create_SSAO_pass(self):
        """Creates self.ssao and self.SSAO_fxaaP"""

        passes = vtkRenderPassCollection()
        passes.AddItem(vtkRenderStepsPass())

        seq = vtkSequencePass()
        seq.SetPasses(passes)

        self.ssao = vtkSSAOPass()
        self.ssao.SetDelegatePass(seq)
        self.ssao.SetBlur(True)
        self.SSAO_fxaaP = vtkOpenGLFXAAPass()  # include Anti-Aliasing

        # options = vtk.vtkFXAAOptions()
        # options.SetSubpixelBlendLimit(0.1)
        # self.SSAO_fxaaP.SetFXAAOptions(options)

        self.SSAO_fxaaP.SetDelegatePass(self.ssao)

        self._update_SSAO_settings()

    def _update_SSAO_settings(self, radius=0.005, bias=0.2, kernel_size=64):
        if self.renderer is None:
            return

        bounds = np.asarray(self.renderer.ComputeVisiblePropBounds())

        b_r = np.linalg.norm(
            [bounds[1] - bounds[0], bounds[3] - bounds[2], bounds[5] - bounds[4]]
        )

        occlusion_radius = b_r * radius
        occlusion_bias = bias

        self.ssao.SetRadius(occlusion_radius)
        self.ssao.SetBias(occlusion_bias)
        self.ssao.SetKernelSize(kernel_size)

    def EnableSSAO(self):
        # from documentation:
        # virtual void 	UseSSAOOn ()
        # virtual void 	UseSSAOOff ()
        #
        # but does not work
        if self._ssao_on:
            return

        for r in self.renderers:
            r.SetPass(self.SSAO_fxaaP)
            self._update_SSAO_settings()
            r.Modified()

        self._ssao_on = True

    def DisableSSAO(self):
        if self._ssao_on == False:
            return

        for r in self.renderers:
            r.SetPass(None)
            r.Modified()

        self._ssao_on = False

    def deselect_all(self):
        for v in self.node_visuals:
            if v._is_selected:
                v._is_selected = False
                v.update_paint(self.settings)

    def add_dynamic_wave_plane(self, waveplane):
        self.remove_dynamic_wave_plane()
        self.add(waveplane.actor)
        self.add(waveplane.line_actor)
        self._wavefield = waveplane

        self.settings.show_sea = False
        #
        # if self.settings.show_global = False:
        #     self._staticwaveplane = True
        #     self.global_visual.off()
        # else:
        #     self._staticwaveplane = False

    def remove_dynamic_wave_plane(self):
        if self._wavefield is not None:
            self.remove(self._wavefield.actor)
            self.remove(self._wavefield.line_actor)
            self._wavefield = None

            # if self._staticwaveplane:
            #     self.global_visual.on()

    def update_dynamic_waveplane(self, t):
        if self._wavefield is not None:
            self._wavefield.update(t)

    def hide_actors_of_type(self, types):
        for V in self.node_visuals:
            for A in V.actors.values():
                if A.actor_type in types:
                    A.off()

    def show_actors_of_type(self, types):
        for V in self.node_visuals:
            for A in V.actors.values():
                if A.actor_type in types:
                    A.on()

    def set_alpha(self, alpha, exclude_nodes=None):
        """Sets the alpha (transparency) of for ALL actors in all visuals except the GLOBAL actors or visuals belonging to a node in exclude_nodes"""

        if exclude_nodes is None:
            exclude_nodes = []
        for V in self.node_visuals:
            for A in V.actors.values():
                if V.node in exclude_nodes:
                    continue

                if A.actor_type == ActorType.GLOBAL:
                    continue
                A.alpha(alpha)

    def toggle_2D(self):
        """Toggles between 2d and 3d mode. Returns True if mode is 2d after toggling"""
        self.Style.ToggleParallelProjection()
        return bool(self.renderer.GetActiveCamera().GetParallelProjection())

    def _scaled_force_vector(self, vector):
        r = np.array(vector)
        len = np.linalg.norm(r)
        if len == 0:
            return r
        if self.settings.force_do_normalize:
            r *= 1000 / len
        r *= self.settings.force_scale / 1000
        return r

    def shutdown_qt(self):
        """Stops the renderer such that the application can close without issues"""
        self.window.Finalize()
        self.interactor.TerminateApp()

    def add_axis_widget(self):
        """Adds an axis widget to the view"""

        axes = vtkAxesActor()

        # makeup
        axes.SetShaftTypeToCylinder()
        axes.SetAxisLabels(False)

        widget = vtkOrientationMarkerWidget()
        widget.SetOrientationMarker(axes)

        widget.SetInteractor(self.interactor)
        widget.SetViewport(0, 0, 0.15, 0.15)
        widget.SetEnabled(True)
        widget.SetInteractive(False)

        self.__axis_widget = widget  # keep from being destructed,

    def add_orientation_widget(self):
        """Adds the orientation widget (interactive).

        - The colors are different from the rest and can not be changed
        - The Rotation works differently than the rest of DAVE, this widget does not keep the
          z axis vertical or the manipulation is inconsistent
        """

        iom = vtkCameraOrientationWidget()
        iom.SetParentRenderer(self.renderer)
        iom.On()

        # rep = iom.GetRepresentation()
        #
        # Attempt to change the colors
        # not working; not all the actors seem to show up
        # props = vtkPropCollection()
        # rep.GetActors(props)
        #
        # # for a in actors:
        # for prop in props:
        #     print(prop.GetProperty().GetVertexColor())
        # # actors.GetProperty().SetColor([1, 0, 1])

        self._orientationwidget = (
            iom  # needed to keep it away from the garbage collector
        )


if __name__ == "__main__":
    from DAVE import Scene, Cable

    s = Scene()
    s.load_scene("res: grid10.dave")

    app = QApplication([])

    widget = QWidget()

    from cProfile import Profile
    from pstats import SortKey, Stats

    viewer = QtEmbeddedSceneRenderer(s, widget)

    viewer.settings.show_sea = False
    # viewer.renderer.SetBackground(COLOR_BG1_GUI)
    viewer.update_visibility()

    viewer.update_outlines()

    # viewer.EnableSSAO()
    #
    # viewer.load_hdr(r"C:\Users\MS12H\Downloads\kloppenheim_05_puresky_2k.hdr")
    # viewer.load_hdr(r"C:\data\DAVE\public\DAVE\src\DAVE\resources\gimp.hdr") # needs to be a 32bit (integer) hdr
    # #
    # viewer.background_color([0.8,1,0.8])

    viewer.interactor.Initialize()
    # viewer.add_axis_widget()

    widget.show()
    viewer.interactor.Start()

    viewer.zoom_all()

    # viewer.SkyBoxOn()

    app.exec()

    #
