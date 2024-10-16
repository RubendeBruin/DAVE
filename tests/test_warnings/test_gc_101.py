from DAVE import *

def test_gc101():

    s = Scene()

    # code for Frame2
    s.new_frame(name='Frame2',
                position=(0,
                          0,
                          0),
                rotation=(0,
                          0,
                          0),
                fixed=(True, True, True, True, True, True),
                )

    # code for Frame3
    s.new_frame(name='Frame3',
                position=(-0,
                          -0,
                          -0),
                rotation=(-0,
                          -0,
                          -0),
                fixed=(True, True, True, True, True, True),
                )

    # code for Point3
    s.new_point(name='Point3',
                parent='Frame2',
                position=(0,
                          0,
                          0))

    # code for Point4
    s.new_point(name='Point4',
                parent='Frame3',
                position=(0,
                          0,
                          0))

    # code for Circle2
    c = s.new_circle(name='Circle2',
                     parent='Point3',
                     axis=(0, 1, 0),
                     radius=0.4)

    # code for Circle3
    c = s.new_circle(name='Circle3',
                     parent='Point4',
                     axis=(0, 1, 0),
                     radius=0.5)

    s.new_geometriccontact(name='Geometric_connection of Circle3 on Circle2',
                           child='Circle3',
                           parent='Circle2',
                           inside=True,
                           rotation_on_parent=0.0,
                           child_rotation=0.0)


    s.update()

    assert len(s.warnings) >= 1
    assert s.warnings[0][0].name == 'Geometric_connection of Circle3 on Circle2'


    # DG(s, autosave=False)