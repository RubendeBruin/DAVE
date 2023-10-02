from DAVE import  *

def test_cable_constant_pointcount_update():
    s = Scene()
    s.new_point('p1', position=(5, 0, 0))
    p2 = s.new_point('p2', position=(0, 0, 10))
    s.new_circle('c2', parent='p2', radius=1, axis=(0, 1, 0))
    s.new_point('p3', position=(-5, 0, 0))

    c = s.new_cable(connections=['p3', 'c2', 'p1'], name='cable', EA=122345, mass=10, length=40)

    c.update()
    points1 = c.get_points_for_visual_blender()

    p2.gz = 30
    c.update()

    points2 = c.get_points_for_visual_blender()

    assert points1[10] != points2[10]  # different points
    assert len(points1)==len(points2)  # but same number


def test_cable_constant_tension_if_no_mass():
    s = Scene()
    s.new_point(name='p1', position=(0, -1, 0))
    s.new_point(name='p2', position=(0, 1, 0))
    b = s.new_rigidbody(name='body', mass=1, fixed=True)
    b.fixed_z = False
    s.new_point('pbody', parent=b)
    c = s.new_circle(name='c1', parent='pbody', radius=1, axis=(1, 0, 0))
    c = s.new_cable(connections=['p1', 'c1', 'p2'], name='cable', EA=1e6, length=20)

    s.solve_statics()

    _, tensions = c.get_points_and_tensions_for_visual()

    for t in tensions:
        assert t == tensions[0]