from DAVE import *

def model():
    """Force on body, body is rotated 90 degrees about x axis

    Returns:

    """
    s = Scene()
    s.new_frame("f1", rotation=(90,0,0))
    s.new_point("p1", "f1")
    f = s.new_force("force", "p1", force=(0,0,-10), moment=(0,0,-10))

    return s, f


def test_create_default_force():
    s,f = model()
    assert f.force == (0,0,-10)
    assert f.moment == (0,0,-10)
    assert f.global_force == (0,0,-10)
    assert f.global_moment == (0,0,-10)

def test_create_local_force():
    s,f = model()
    f.is_global = False
    assert f.force == (0,0,-10)
    assert f.global_force == (0,10,0)
    assert f.moment == (0,0,-10)
    assert f.global_moment == (0,10,0)

def test_demo_model():

    s = Scene()

    # code for Frame
    s.new_frame(name='Frame',
                fixed =(False, True, False, False, False, False),
                )

    # code for Frame2
    s.new_frame(name='Frame2',
                position=(0,
                          0,
                          0),
                rotation=(0,
                          0,
                          0),
                fixed =(True, True, True, True, True, True),
                )

    # code for Frame3
    s.new_frame(name='Frame3',
                fixed =(False, False, False, False, False, False),
                )

    # code for Frame4
    s.new_frame(name='Frame4',
                position=(0,
                          0,
                          -5),
                rotation=(0,
                          0,
                          0),
                fixed =(True, True, True, True, True, True),
                )

    # code for beam Beam
    s.new_beam(name='Beam',
               nodeA='Frame2',
               nodeB='Frame',
               n_segments=10.0,
               tension_only=False,
               EIy =1000,
               EIz =1000,
               GIp =10,
               EA =1000,
               mass =0,
               L =10) # L can possibly be omitted

    # code for beam Beam2
    s.new_beam(name='Beam2',
               nodeA='Frame4',
               nodeB='Frame3',
               n_segments=10.0,
               tension_only=False,
               EIy =1000,
               EIz =1000,
               GIp =10,
               EA =1000,
               mass =0,
               L =10) # L can possibly be omitted

    # code for Point
    s.new_point(name='Point',
                parent='Frame',
                position=(0,
                          0,
                          0))

    # code for Visual
    s.new_visual(name='Visual',
                 parent='Frame2',
                 path=r'res: cube_with_bevel.obj',
                 offset=(-1, 0, -3),
                 rotation=(0, 0, 0),
                 scale=(1, 1, 6) )

    # code for Point2
    s.new_point(name='Point2',
                parent='Frame3',
                position=(0,
                          0,
                          0))

    # code for Local Force
    s.new_force(name='Local Force',
                parent='Point',
                local=True,
                force=(0, 0, -10),
                moment=(0, 0, 0) )

    # code for Global Force
    s.new_force(name='Global Force',
                parent='Point2',
                force=(0, 0, -10),
                moment=(0, 0, 0) )

    s['Point']._visible = False

    s['Point2']._visible = False

    s.solve_statics()


