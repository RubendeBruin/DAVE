"""This is a simple scene renderer, used for demonstrartion purposes. """
from pathlib import Path

import PIL
import numpy as np
from vtkmodules.util.numpy_support import vtk_to_numpy
from vtkmodules.vtkCommonCore import vtkUnsignedCharArray
from vtkmodules.vtkFiltersHybrid import vtkRenderLargeImage
from vtkmodules.vtkIOImage import vtkPNGWriter
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
from vtkmodules.vtkRenderingCore import (
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkCamera,
)
from vtkmodules.vtkRenderingOpenGL2 import vtkOpenGLRenderer

from DAVE.visual_helpers.constants import COLOR_BG1
from DAVE.visual_helpers.scene_renderer import AbstractSceneRenderer


class ImageRenderer(AbstractSceneRenderer):
    def __init__(self, scene):
        super().__init__(scene)

    def create_rendering_pipeline(
        self,
    ) -> tuple[vtkRenderer, list[vtkRenderer], vtkCamera, vtkRenderWindow]:
        """Creates the rendering pipeline for the viewport"""

        renderer = vtkOpenGLRenderer()

        renderer.SetBackground(COLOR_BG1)

        renwin = vtkRenderWindow()
        renwin.SetOffScreenRendering(True)
        renwin.AddRenderer(renderer)
        camera = renderer.GetActiveCamera()

        return renderer, [renderer], camera, renwin

    def _set_size(self, width, height):
        width = int(width)
        height = int(height)

        size = self.window.GetSize()
        if (width != size[0]) or (height != size[0]):
            self.window.SetSize(width, height)

    def produce(self, width, height, filename: str or Path, scale: int = 1):
        self._set_size(width, height)

        output = vtkRenderLargeImage()
        output.SetInput(self.renderer)
        output.SetMagnification(scale)

        png = vtkPNGWriter()
        png.SetFileName(str(filename))
        png.SetInputConnection(output.GetOutputPort())

        png.Write()

    def produce_pil_image(self, width=800, height=600, transparent: bool = False):
        self._set_size(width, height)

        nx, ny = self.window.GetSize()

        self.window.Render()

        arr = vtkUnsignedCharArray()
        self.window.GetRGBACharPixelData(0, 0, nx - 1, ny - 1, 0, arr)

        if transparent:
            narr = vtk_to_numpy(arr).T[:4].T.reshape([ny, nx, 4])
        else:
            narr = vtk_to_numpy(arr).T[:3].T.reshape([ny, nx, 3])

        narr = np.flip(narr, axis=0)

        pil_img = PIL.Image.fromarray(narr)

        return pil_img


if __name__ == "__main__":
    from DAVE import Scene

    s = Scene()

    # code for Point
    s.new_point(name="Point", position=(10, 0, 0))

    # code for Frame
    s.new_frame(
        name="Frame",
        position=(0, 0, 0),
        rotation=(0, 0, 0),
        fixed=(True, True, True, True, True, True),
    )

    # code for Visual
    s.new_visual(
        name="Visual",
        parent="Frame",
        path=r"res: cube_with_bevel.obj",
        offset=(0, 0, 0),
        rotation=(0, 0, 0),
        scale=(1, 1, 1),
    )

    image_producer = ImageRenderer(s)

    image_producer.load_hdr(s.get_resource_path("res: day.hdr"))
    image_producer.SkyBoxOn()

    p1 = image_producer.produce_pil_image()
    p1.show()
