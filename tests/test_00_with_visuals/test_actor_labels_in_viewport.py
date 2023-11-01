from DAVE import *
from DAVE.visual import Viewport
def test_viewport_with_custom_labels():
    s = Scene()
    s.new_point(name="Point", position=(0, 0, 0))
    s.new_point(name="Point2", position=(4, 0, 0))
    p3 = s.new_point(name="Point3", position=(6, 0, 0))

    p3._custom_property = "demo"

    v = Viewport(s)
    v.settings.label_scale=4
    v.settings.label_property = '_custom_property'
    # v.show_as_qt_app()


