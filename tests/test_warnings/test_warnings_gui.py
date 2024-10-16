
from DAVE import *

if __name__ == '__main__':

    s = Scene()

    # code for Point
    s.new_point(name='Point',
                position=(2,
                          0,
                          0))

    # code for Point2
    s.new_point(name='Point2',
                position=(0,
                          6,
                          0))

    # code for Frame
    s.new_frame(name='Frame',
                position=(0,
                          0,
                          0),
                rotation=(0,
                          0,
                          0),
                fixed=(True, True, True, True, True, True),
                )

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

    # code for Circle
    c = s.new_circle(name='Circle',
                     parent='Point',
                     axis=(0, 1, 0),
                     radius=1)

    # code for Tank
    mesh = s.new_tank(name='Tank',
                      parent='Frame')
    mesh.trimesh.load_file(r'res: plane.obj', scale=(1.0, 1.0, 1.0), rotation=(0.0, 0.0, 0.0), offset=(0.0, 0.0, 0.0))
    s['Tank'].volume = 0  # first load mesh, then set volume

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

    # code for Cable
    s.new_cable(name='Cable',
                endA='Point2',
                endB='Point2',
                length=6.08276,
                EA=0.0,
                sheaves=['Circle'])

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
                           rotation_on_parent=0,
                           child_rotation=0)


    s.update()

    DG(s, autosave=False)