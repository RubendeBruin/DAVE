"""This is a simple scene renderer, used for demonstrartion purposes. """
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
from vtkmodules.vtkRenderingCore import vtkRenderer, vtkRenderWindow, vtkRenderWindowInteractor, vtkCamera
from vtkmodules.vtkRenderingOpenGL2 import vtkOpenGLRenderer

from .constants import COLOR_BG1
from .scene_renderer import AbstractSceneRenderer

class SimpleSceneRenderer(AbstractSceneRenderer):

    def __init__(self, scene):
        super().__init__(scene)

    def create_rendering_pipeline(self) -> tuple[vtkRenderer, list[vtkRenderer], vtkCamera, vtkRenderWindow]:
        """Creates the rendering pipeline for the viewport"""

        renderer = vtkOpenGLRenderer()

        renderer.SetBackground(COLOR_BG1)

        renwin = vtkRenderWindow()
        renwin.SetSize(600, 600)
        renwin.AddRenderer(renderer)

        self.interactor = vtkRenderWindowInteractor()
        self.interactor.SetRenderWindow(renwin)

        style = vtkInteractorStyleTrackballCamera()
        self.interactor.SetInteractorStyle(style)

        camera = renderer.GetActiveCamera()

        return renderer, [renderer], camera, renwin


    def show(self):
        self.interactor.Start()




