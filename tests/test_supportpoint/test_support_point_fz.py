from numpy.testing import assert_allclose

from DAVE import Scene

def model():
    s = Scene()
    f = s.new_frame('frame')
    p = s.new_point('point')

    # sp = SupportPoint(s, 'sp')
    sp = s.new_supportpoint('sp', 'frame','point',kz=1000)
    sp.frame = f
    sp.point = p

    s.update()

    return s.copy()

def test_support_point0():
    s = model()
    sp = s['sp']
    frame = s['frame']
    point = s['point']

    assert sp.fz == 0

def test_support_point1000():
    s = model()
    sp = s['sp']
    frame = s['frame']
    point = s['point']

    frame.z = 1
    sp.kz = 1000

    s.update()

    print(sp.contact_force_global)

    assert_allclose(sp.fz, 1000)
    assert_allclose(sp.fx, 0)
    assert_allclose(sp.fy, 0)

def test_copy_all_props():
    s = model()
    p2 = s.new_supportpoint('sp2', 'frame', 'point', kx=1,ky=2, kz=3, delta_z = 4)

    s2 = s.copy()
    p2 = s2['sp2']
    assert p2.kx == 1
    assert p2.ky == 2
    assert p2.kz == 3
    assert p2.delta_z == 4
    assert p2.point.name == 'point'
    assert p2.frame.name == 'frame'


if __name__ == '__main__':
    test_support_point1000()
