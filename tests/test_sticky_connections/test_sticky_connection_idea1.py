from DAVE import *

if __name__ == '__main__':

    s = Scene()


    # auto generated python code
    # By MS12H
    # Time: 2024-11-05 09:31:48 UTC

    # To be able to distinguish the important number (eg: fixed positions) from
    # non-important numbers (eg: a position that is solved by the static solver) we use a dummy-function called 'solved'.
    # For anything written as solved(number) that actual number does not influence the static solution

    def solved(number):
        return number


    # Environment settings
    s.g = 9.80665
    s.waterlevel = 0.0
    s.rho_air = 0.00126
    s.rho_water = 1.025
    s.wind_direction = 0.0
    s.wind_velocity = 0.0
    s.current_direction = 0.0
    s.current_velocity = 0.0

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

    # code for Sticky point
    s.new_point(name='Sticky point',
                parent='Frame',
                position=(0,
                          0,
                          -1.25))

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

    # code for Sticky cable part 1
    s.new_cable(name='Sticky cable part 1',
                endA='Point2',
                endB='Sticky point',
                length=10,
                diameter=0.5,
                EA=12345.0,
                sheaves=['Circle'])
    s['Sticky cable part 1'].reversed = (False, True, False)
    s['Sticky cable part 1'].max_winding_angles = [999.0, 270.0, 999.0]

    # code for Sticky cable part 2
    s.new_cable(name='Sticky cable part 2',
                endA='Sticky point',
                endB='Point3',
                length=10,
                diameter=0.5,
                EA=12345.0,
                sheaves=['Circle'])
    s['Sticky cable part 2'].reversed = (False, True, False)
    s['Sticky cable part 2'].max_winding_angles = [999.0, 270.0, 999.0]

    s['Normal cable']._visible = False

    # Limits

    # Watches
    s.try_add_watch('Sticky point', 'force')

    # Tags

    # - tags are added with 'try_add_tags' because the node may not exist anymore (eg changed components) wh

    # Colors
    s._try_add_color('Normal cable', (0, 255, 255))
    s._try_add_color('Sticky cable part 1', (255, 255, 24))
    s._try_add_color('Sticky cable part 2', (255, 164, 238))

    s['Sticky point'].z = -1.25000001 # work-around for solver geometry issue

    DG(s, autosave = False)