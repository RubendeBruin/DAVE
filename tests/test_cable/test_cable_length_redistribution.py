from numpy.testing import assert_allclose

from DAVE import *

def do_test_cable_segment_length_redistribution(loop=True):
    s = Scene()
    f = s.new_frame("global")
    
    p1 = s.new_point("p1", position=(-10, 0, 0), parent=f)
    s.new_point("p2", position=(1, 2, 0), parent=f)
    s.new_point("p3", position=(4, 4, 0), parent=f)

    s.new_point("p4", position=(4, 4, 4), parent=f)

    if loop:
        s.new_cable(
            connections=["p1", "p2", "p3", "p1"], name="cable", EA=122345, mass=1000, length=30
        )
    else:
        s.new_cable(
            connections=["p1", "p2", "p3","p4"], name="cable", EA=122345, mass=1000, length=30
        )

    #
    s["cable"].solve_segment_lengths = True
    s.update()

    assert len(s._vfc.get_dofs()) == 2

    s.solve_statics()
    assert s.verify_equilibrium()

    p1.gz = 2

    s.solver_settings.timeout_s = 5
    s.solve_statics()

    assert len(s._vfc.get_dofs()) == 2

    s.update()
    
def test_cable_segment_length_redistribution():
    do_test_cable_segment_length_redistribution(loop=False)

def test_cable_segment_length_redistribution_loop():
    assert False, "Does not converge - experimental feature"
    # do_test_cable_segment_length_redistribution(loop=True)



def test_sheaved_catenary():
    assert False, "Does not converge - experimental feature"
    s = Scene()
    f = s.new_frame('global')

    p1 = s.new_point('p1', position=(-10, 0, 0), parent=f)
    s.new_point('p2', position=(1, 2, 0), parent=f)
    s.new_point('p3', position=(4, 4, 0), parent=f)

    s.new_cable(connections=['p1', 'p2', 'p3','p1'], name='cable', EA=122345, mass = 1000, length=30)
    #
    s._save_coredump()

    s["cable"].solve_segment_lengths = True
    s.update()

    print(s["cable"]._vfNode._get_shifts())
    print(s["cable"].friction_forces)
    
    print(f"DOFS = {s._vfc.get_dofs()}")

    s.solve_statics(terminate_after_s=3)

    p1.gz = 2

    s.solve_statics(terminate_after_s=3)

    s.update()

    assert s.verify_equilibrium()

def test_sheaved_catenary_with_3dof_body():
    s = Scene()
    f = s.new_frame("global")

    p1 = s.new_point("p1", position=(-10, 0, 0), parent=f)
    s.new_point("p2", position=(1, 2, 0), parent=f)
    s.new_point("p3", position=(4, 4, 0), parent=f)

    s.new_cable(
        connections=["p1", "p2", "p3", "p1"],
        name="cable",
        EA=122345,
        mass=1000,
        length=30,
    )
    #

    s["cable"].solve_segment_lengths = False

    s['cable'].length = 40.0
    s.new_rigidbody(name = 'Body',mass=100).fixed = (False, False, False, True, True, True)

    s.new_point('Point', parent = 'Body')

    s['cable'].connections = ('p1','p2','Point','p3','p1')

    s.solve_statics()


def test_two_points_one_mass():
    s = Scene()

    s.new_frame(name='global')


    # code for Body
    s.new_rigidbody(name='Body',
                    mass=100,
                    fixed =(False, False, False, True, True, True) )

    # code for p1
    s.new_point(name='p1',
                parent='global',
                position=(-10,
                          0,
                          0))

    # code for p3
    s.new_point(name='p3',
                parent='global',
                position=(4, 4,  3))

    s.new_point(name='Point', parent='Body')
    c = s.new_cable(name='cable',
                endA='p1',
                endB='p3',
                length=40,
                mass_per_length=0.1,
                EA=122345.0,
                sheaves = ['Point'])

    c.solve_segment_lengths = True

    s.solve_statics()

    assert_allclose(s['Point'].gz, -17, atol=2)

def test_three_parts():

    s = Scene()
    f = s.new_frame("global")

    p1 = s.new_point("p1", position=(-10, 0, 0), parent=f)
    s.new_point("p2", position=(1, 2, 0), parent=f)
    s.new_point("p3", position=(4, 4, 0), parent=f)

    s.new_cable(
        connections=["p1", "p2", "p3", "p1"],
        name="cable",
        EA=122345,
        mass=1000,
        length=30,
    )
    #


    s["cable"].solve_segment_lengths = False

    s['cable'].length = 40.0
    s.new_rigidbody(name = 'Body',mass=100).fixed = (False, False, False, True, True, True)

    s.new_point('Point', parent = 'Body')

    s['cable'].connections = ('p1','p2','Point','p3','p1')

    s.solve_statics()

    s["cable"].solve_segment_lengths = True
    s['Body'].fixed = True

    try:
        s.solver_settings.timeout_s = 5
        s.solve_statics() # <-- will not converge; but should at least not crash
    except ValueError as M:
        assert "Solver maximum time of 5" in str(M)
        pass # <-- will not converge; but should at least not crash

    # from DAVE.gui import Gui
    # Gui(s)


if __name__ == '__main__':
    test_sheaved_catenary()