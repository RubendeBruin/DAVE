from DAVE import *


def model():
    s = Scene()

    a = s.new_frame("A")
    b = s.new_rigidbody("B", mass=1)

    p1 = s.new_point("p1", a)
    p2 = s.new_point("p2", b)

    c1 = s.new_circle("c1", p1, (0, 1, 0), radius=1)
    c2 = s.new_circle("c2", p2, (0, 1, 0), radius=1)

    gc = s.new_geometriccontact("GC", "c2", "c1")
    gc.swivel = 0

    s.new_visual(name="Visual", parent="B", path="res: cube_with_bevel.obj")
    s["Visual"].scale = (0.4, 0.4, 0.4)

    s["c2"].color = (170, 255, 255)
    s["Visual"].color = (170, 255, 255)
    s["c1"].color = (170, 85, 0)

    return s


if __name__ == "__main__":
    s = model()

    s.solve_statics()
    work_done, messages = s._check_and_fix_geometric_contact_orientations()

    assert work_done

    from DAVE.gui import Gui

    Gui(s)
