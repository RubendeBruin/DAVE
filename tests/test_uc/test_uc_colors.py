from DAVE import *
from DAVE.visual_helpers.image_screen_renderer import ImageRenderer

def test_uc_colors():

    s = Scene()
    for i in range(12):
        p = s.new_point(f"Point {i}", position = (i, 0, 0))
        p.limits['x'] = 10

    ucs = [node.UC for node in s.nodes_where(kind = Point)]
    print(ucs)

    s.update()

    img = ImageRenderer(s)
    img.settings.paint_uc = True
    img.settings.show_origin = False
    img.zoom_all()

    img.show()
