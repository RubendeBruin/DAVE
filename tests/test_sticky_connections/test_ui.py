from DAVE import *

if __name__ == '__main__':

    s = Scene()

    # auto generated python code
    # By MS12H
    # Time: 2024-11-27 13:50:26 UTC

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



    # code for Point
    s.new_point(name='Point',
              position=(0,
                        0,
                        0))

    # code for Point2
    s.new_point(name='Point2',
              position=(0,
                        0,
                        5))

    # code for Point3
    s.new_point(name='Point3',
              position=(4.932,
                        -0.319,
                        3.867))

    # code for Bottom
    c = s.new_circle(name='Bottom',
                parent='Point',
                axis=(0, 1, 0),
                radius=1 )

    # code for Top
    c = s.new_circle(name='Top',
                parent='Point2',
                axis=(0, 1, 0),
                radius=1 )

    # code for Cable
    s.new_cable(name='Cable',
                endA='Top',
                endB='Top',
                length=16.2832,
                diameter=0.5,
                EA=12345.0,
                sheaves = ['Point3',
                           'Bottom'])
    # friction, first set values, then enable
    s['Cable'].friction_force_factor = [None, 0.0, None]
    s['Cable'].pin_position_cable = [None, None, 0.0]
    s['Cable'].pin_position_circle = [None, None, 210.0]
    s['Cable'].friction_type = [FrictionType.No, FrictionType.Force, FrictionType.Pinned]

    # Limits

    # Watches

    # Tags

    # - tags are added with 'try_add_tags' because the node may not exist anymore (eg changed components) wh

    # Colors

    DG(s)