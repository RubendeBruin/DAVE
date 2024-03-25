"""This is a simple scene renderer, used for demonstrartion purposes. """
from pathlib import Path

from vtkmodules.vtkFiltersHybrid import vtkRenderLargeImage
from vtkmodules.vtkIOImage import vtkPNGWriter
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
from vtkmodules.vtkRenderingCore import vtkRenderer, vtkRenderWindow, vtkRenderWindowInteractor, vtkCamera
from vtkmodules.vtkRenderingOpenGL2 import vtkOpenGLRenderer

from DAVE.visual_helpers.constants import COLOR_BG1
from DAVE.visual_helpers.scene_renderer import AbstractSceneRenderer

class ImageRenderer(AbstractSceneRenderer):

    def __init__(self, scene):
        super().__init__(scene)

    def create_rendering_pipeline(self) -> tuple[vtkRenderer, list[vtkRenderer], vtkCamera, vtkRenderWindow]:
        """Creates the rendering pipeline for the viewport"""

        renderer = vtkRenderer()

        renderer.SetBackground(COLOR_BG1)

        renwin = vtkRenderWindow()
        renwin.SetOffScreenRendering(True)
        renwin.AddRenderer(renderer)
        camera = renderer.GetActiveCamera()

        return renderer, [renderer], camera, renwin

    def produce(self, width, height, filename : str or Path, scale: int = 1):

        size = self.window.GetSize()
        if (width != size[0]) or (height != size[0]):
            self.window.SetSize(width, height)

        output = vtkRenderLargeImage()
        output.SetInput(self.renderer)
        output.SetMagnification(scale)

        png = vtkPNGWriter()
        png.SetFileName(str(filename))
        png.SetInputConnection(output.GetOutputPort())

        png.Write()

if __name__ == '__main__':

    from DAVE import Scene
    s = Scene()

    # code for Point
    s.new_point(name='Point',
                position=(10,
                          0,
                          0))

    # code for Frame
    s.new_frame(name='Frame',
                position=(0,
                          0,
                          0),
                rotation=(0,
                          0,
                          0),
                fixed=(True, True, True, True, True, True),
                )

    # code for Visual
    s.new_visual(name='Visual',
                 parent='Frame',
                 path=r'res: cube_with_bevel.obj',
                 offset=(0, 0, 0),
                 rotation=(0, 0, 0),
                 scale=(1, 1, 1))

    image_producer = ImageRenderer(s)

    import tempfile

    filename = tempfile.gettempdir() + '/test.png'
    filename2 = tempfile.gettempdir() + '/test2.png'
    print(filename)

    image_producer.camera.SetPosition(10,0,10)
    image_producer.camera.SetFocalPoint(0,0,0)

    image_producer.load_hdr(r"C:\Users\MS12H\Downloads\cosmos-1-HDR.hdr")

    image_producer.produce(800,600,filename,2)
    print(filename)
    image_producer.camera.SetPosition((100,0,10))
    image_producer.produce(800,600,filename2,2)
    print(filename2)

    from PIL import Image

    img = Image.open(filename)
    img2 = Image.open(filename2)




