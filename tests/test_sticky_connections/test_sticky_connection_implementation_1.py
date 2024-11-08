from DAVE import *

if __name__ == '__main__':

    s = Scene()

    # code for Frame
    s.new_frame(name='Frame',
                position=(0,
                          0,
                          0),
                rotation=(0,
                          -5,
                          0),
                fixed=(True, True, True, True, True, True),
                )

    # code for Point2
    s.new_point(name='Point2',
                position=(-5,
                          0,
                          9.5))

    # code for Point3
    s.new_point(name='Point3',
                position=(5,
                          0,
                          9.5))

    # code for Point
    s.new_point(name='Point',
                parent='Frame',
                position=(0,
                          0,
                          0))

    # code for Circle
    c = s.new_circle(name='Circle',
                     parent='Point',
                     axis=(0, 1, 0),
                     radius=1)

    # code for Normal cable
    s.new_cable(name='Normal cable',
                endA='Point2',
                endB='Point3',
                length=20,
                diameter=0.5,
                EA=12345.0,
                sheaves=['Circle'])
    s['Normal cable'].reversed = (False, True, False)

    s['Normal cable']._visible = True

    nc : Cable = s['Normal cable']

    print(nc.name)

    nc.sticky = (None, (0.5, (0,0,-1.250000001)), None)

    DG(s)


