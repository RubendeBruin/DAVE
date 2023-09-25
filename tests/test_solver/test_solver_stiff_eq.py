from DAVE import *


def model(EA):
    s = Scene()

    
    # code for Body
    s.new_rigidbody(
        name="Body",
        mass=1000, fixed=False
    )
    
    # code for Point2
    s.new_point(name="Point2", position=(5, 5, 25))
    
    # code for Buoyancy
    mesh = s.new_buoyancy(name="Buoyancy", parent="Body")
    mesh.trimesh.load_file(
        r"res: cube.obj",
        scale=(10.0, 10.0, 10.0),
        rotation=(0.0, 0.0, 0.0),
        offset=(0.0, 0.0, 0.0),
    )
    
    # code for Point
    s.new_point(name="Point", parent="Body", position=(5, 5, 5))
    
    # code for Cable
    s.new_cable(name="Cable", endA="Point", endB="Point2", length=19, EA=EA)

    return s

def test_stiff_eqe10():
    s = model(EA=1e10)
    s.solve_statics()
    s.verify_equilibrium()

def test_stiff_eqe12():
    s = model(EA=1e12)
    s.solve_statics()
    s.verify_equilibrium()

if __name__ == '__main__':
    s = model(EA=1e10)
    s.solve_statics()
    s.verify_equilibrium()