from DAVE import  *

def test_cable_constant_pointcount():
    s = Scene()
    s.new_point('p1', position=(5, 0, 0))
    p2 = s.new_point('p2', position=(0, 0, 10))
    s.new_circle('c2', parent='p2', radius=1, axis=(0, 1, 0))
    s.new_point('p3', position=(-5, 0, 0))

    c = s.new_cable(connections=['p3', 'c2', 'p1'], name='cable', EA=122345, mass=10, length=40)

    points1 = c.get_points_for_visual_blender()

    p2.gz = 30

    points2 = c.get_points_for_visual_blender()

    assert points1[10] != points2[10]  # different points
    assert len(points1)==len(points2)  # but same number


