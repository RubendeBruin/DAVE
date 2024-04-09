"""Used for drawing an overlay actor on the screen.
Can be images or text.
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from vtkmodules.util.numpy_support import numpy_to_vtk
from vtkmodules.vtkCommonCore import VTK_UNSIGNED_CHAR
from vtkmodules.vtkRenderingCore import vtkRenderWindow


class OverlayActor:
    def __init__(self):
        self._vtk_pixel_data = None
        self._width = 0
        self._height = 0


    def set_text(self, text:str, font : ImageFont):
        """Set the overlay actor to the provided text."""
        _,_,w,h = font.getbbox(text)

        image = Image.new('RGBA', (w, h), (255, 255, 255, 0))  # background is transparent
        bitmap = ImageDraw.Draw(image)
        bitmap.text((0, 0), text, (0, 0, 0), font=font)

        np_img = np.array(image)

        # flip upside down
        np_img = np.flipud(np_img)
        np_img_flat = np_img.ravel()

        self._vtk_pixel_data = numpy_to_vtk(np_img_flat, deep=True, array_type=VTK_UNSIGNED_CHAR)
        self._width = w
        self._height = h

    def render_at(self, render_window : vtkRenderWindow, x : int ,y : int):
        """Render the overlay actor at the specified position."""

        x = int(x)
        y = int(y)

        x1 = x
        x2 = x + self._width - 1
        y1 = y
        y2 = y + self._height - 1

        front = 0
        blend = 1
        right = 0

        # check size (to avoid out of bounds fatal errors)
        n = self._vtk_pixel_data.GetSize()
        assert n == (x2-x1+1) * (y2-y1+1) * 4, f"Size mismatch: {n} != {(x2-x1+1) * (y2-y1+1) * 4}"

        render_window.SetRGBACharPixelData(x1, y1, x2, y2, self._vtk_pixel_data, front, blend, right)


