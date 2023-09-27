from DAVE import *

def box_model():
    s = Scene()

    b = s.new_rigidbody("Box", mass=2500, fixed=False)
    b = s.new_buoyancy("shape", parent=b)
    b.trimesh.load_obj("res: cube.obj", scale=(100, 10, 4))

    return s

def test_copy_in_equilibruim():
    s = box_model()
    s.solve_statics()
    assert s.verify_equilibrium()

    print(s['Box'].z)

    s.print_python_code()

    s2 = s.copy()
    assert s2.verify_equilibrium()

def test_copy_in_equilibruim_nosolved():
    s = box_model()
    s.solve_statics()
    assert s.verify_equilibrium()

    print(s["Box"].z)

    s._export_code_with_solved_function = False
    s.print_python_code()

    s2 = s.copy()
    assert s2.verify_equilibrium()

