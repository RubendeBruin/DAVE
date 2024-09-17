from pathlib import Path
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication

from DAVE import Scene
from DAVE.settings_visuals import PAINTERS
from DAVE.visual_helpers.image_screen_renderer import ImageRenderer


def give_pixmap_from_DAVE_model(file : Path, resource_provider = None):
    s = Scene()
    if resource_provider is not None:
        s.resource_provider = resource_provider

    s.load(file, allow_error_during_load=True)

    ren = ImageRenderer(s)
    ren.settings.show_sea = False
    ren.set_painters(PAINTERS["Visual"])
    ren.zoom_all()

    pil_image = ren.produce_pil_image()
    #
    #
    # QPixmap()
    assert QApplication.instance() is not None  # else the conversion will fail

    image = pil_image.toqpixmap()
    return image


