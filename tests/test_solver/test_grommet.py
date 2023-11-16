from DAVE import *

# this test fails in versions before build 20231116

def test_grommet():
    s = Scene()

    # code for Point
    s.new_point(name='Point',
                position=(0,
                          0,
                          0))

    # code for Body
    s.new_rigidbody(name='Body',
                    mass=300,
                    position=(0, 0, -17.110),
                    fixed= (True, True, True, True, False, True),
                    )


    # code for Circle
    c = s.new_circle(name='Circle',
                     parent='Point',
                     axis=(0, 1, 0),
                     radius=1)

    # code for Point_1
    s.new_point(name='Point_1',
                parent='Body',
                position=(0,
                          0,
                          0))

    # code for Circle_1
    c = s.new_circle(name='Circle_1',
                     parent='Point_1',
                     axis=(0, 1, 0),
                     radius=1)

    # code for sling_grommet/_grommet
    s.new_cable(name='loop',
                endA='Circle_1',
                endB='Circle_1',
                length=40.6822,
                mass_per_length=0.0381334,
                diameter=0.108141,
                EA=373076.15760407416,
                sheaves=['Circle'])

    # Watches
    s['Point'].watches['Momnet on upper sheave'] = Watch(evaluate='self.applied_moment', decimals=3, condition='')
    s['Body'].watches['Moment on body'] = Watch(evaluate='self.applied_force[4]', decimals=3, condition='')
    s['Point_1'].watches['Momemt on point'] = Watch(evaluate='self.applied_moment[1]', decimals=3, condition='')
    s['loop'].watches['loop.segment_end_tensions'] = Watch(evaluate='self.segment_end_tensions', decimals=3,
                                                           condition='')

    s.solve_statics()  # this fails in versions before build 20231116

