
from DAVE import *


def test_model_documentation_circle_geometry():

    s = Scene()

    dy = 2

    # code for Load
    s.new_rigidbody(name='Load',
                    mass=10,
                    fixed=(False,False,False,True,True,True),
                    )

    # code for point_left
    s.new_point(name='point_left',
              position=(-5,
                        0,
                        0))

    # code for point_right
    s.new_point(name='point_right',
              position=(5,
                        dy,
                        0))

    # code for point_right2
    s.new_point(name='point_right2',
              position=(5,
                        -dy,
                        0))

    # code for Pnt
    s.new_point(name='Pnt',
              parent='Load',
              position=(0,
                        0,
                        0))

    # code for sheave
    c = s.new_circle(name='sheave',
                parent='Pnt',
                axis=(0, 1, 0),
                radius=5 )

    # code for Grommet/_grommet
    cab = s.new_cable(name='Cable',
                endA='point_left',
                endB='point_left',
                length=98.583,
                diameter=0,
                EA=10000,
                sheaves = ['sheave',
                           'point_right',
                           'point_right2',
                           'sheave'])
    s['Cable'].reversed = (False, True, False, False, False, False)


    s.solve_statics()

    points, tensions = cab._vfNode.get_drawing_data(
                0,0, False
            )


    for i, p in enumerate(points):
        s.new_point(name=f'points{i}',position=p)


    mt = s.new_cable(name='measuring_tape',EA=0, length=0, connections = ['Pnt','points7','points6'])
    angles = mt.angles_at_connections

    # gui(s)