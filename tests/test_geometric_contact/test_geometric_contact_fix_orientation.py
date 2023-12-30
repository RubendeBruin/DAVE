from pathlib import Path

from numpy.testing import assert_allclose

from DAVE import *


def model():
    s = Scene()

    a = s.new_frame("A")
    b = s.new_rigidbody(
        "B",
        mass=1,
        cog=(
            0.1,
            0,
            0.1,
        ),
    )

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

def model_shackles():
    s = Scene()

    p = Path(__file__).parent.parent.parent.parent.parent / 'modules' / 'DAVE_rigging' / 'src' / 'DAVE_rigging' / 'resources'
    s.resource_provider.addPath(p)

    # Exporting Shackle
    # Create Shackle
    sh = s.new_shackle("Shackle", kind="GP500")
    sh.position = (0, 0, 0)
    sh.rotation = (0, 0, 0)

    # Exporting Shackle2
    # Create Shackle
    sh = s.new_shackle("Shackle2", kind="GP500")
    sh.position = (-0, -0, -0.9005)
    sh.rotation = (-0, -0, -0)

    s.new_geometriccontact(name='Geometric_connection of Shackle2/bow on Shackle/pin',
                           child='Shackle2/bow',
                           parent='Shackle/pin',
                           inside=False,
                           rotation_on_parent=150,
                           child_rotation=250)

    s['Shackle/pin_point']._visible = False

    s['Shackle/bow_point']._visible = False

    s['Shackle/inside_circle_center']._visible = False

    s['Shackle2/pin_point']._visible = False

    s['Shackle2/bow_point']._visible = False

    s['Shackle2/inside_circle_center']._visible = False

    solved_dofs = [
        ('Geometric_connection of Shackle2/bow on Shackle/pin/_pin_hole_connection', 'ry', 150.0),
        ('Geometric_connection of Shackle2/bow on Shackle/pin/_axis_on_child', 'ry', 250.00000000000003),
    ]
    for dof in solved_dofs:
        try:
            setattr(s[dof[0]], dof[1], dof[2])
        except:
            pass

    return s


def test_unsolvable_model_raises_correct_error():
    s = model()

    s.new_point(name="Point")
    s["Point"].global_position = (13.639, 1.034, 1.125)
    s.new_cable("Cable", endA="p2", endB="Point")
    s["Cable"].EA = 1.0

    s.solver_settings.timeout_s = 0.5

    try:
        s.solve_statics()
        raise AssertionError("Should have raised an ValueError")
    except ValueError as e:
        assert "geometric contacts" in str(e)

def test_shackles():
    s = model_shackles()

    s.solver_settings.do_linear_first = True
    s.solver_settings.up_is_up_factor = 1.0

    s.solve_statics()

    assert_allclose(s['Shackle2'].gz,-0.718)

def test_shackles_managed():
    s = model_shackles()

    gc = s['Geometric_connection of Shackle2/bow on Shackle/pin']

    point = s.new_point("dummy")
    gc.manager = point

    s.solver_settings.do_linear_first = True
    s.solver_settings.up_is_up_factor = 1.0

    s.solve_statics()
    assert_allclose(s['Shackle2'].gz,-0.718)



if __name__ == "__main__":
    s = model_shackles()

    from DAVE.gui import Gui

    Gui(s)
