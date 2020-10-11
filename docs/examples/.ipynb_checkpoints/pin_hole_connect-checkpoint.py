from DAVE.scene import *
from DAVE.tools import rotation_from_y_axis_direction

s = Scene()

# code for A1
s.new_axis(name='A1',
           position=(0.0,
                     1.0,
                     3.0),
           rotation=(10.0,
                     0.0,
                     30.0),
           fixed =(True, True, True, True, True, True) )
s.new_point(name='P1',
            parent='A1',
            position=(2.0,
                    0.0,
                    0.0))
s.new_circle(name='hole',
             parent='P1',
             axis=(1.0, 1.0, 0.0),
             radius=3)


# code for A2
s.new_rigidbody(name='A2',
           position=(0.0,
                     0.0,
                     0.0),
           rotation=(0.0,
                     0.0,
                     0.0),
           fixed =False,
                mass=1)
s.new_point(name='P2',
            parent='A2',
            position=(10.0,
                    0.0,
                    0.0))
s.new_circle(name='pin',
             parent='P2',
             axis=(0.0, 1.0, 0.0),
             radius=0.5)


# Connect pin to hole


# step1: create an axis at the centerline of the hole

hole = s['hole']
pin = s['pin']

# --------- prepare hole

hole_axis = s.new_axis('hole_axis')
hole_axis.parent = hole.parent.parent
hole_axis.position = hole.parent.position

# orient the axis such that the Y-direction is the axis direction of the hole
y = np.array((0,1,0))
hole_axis.rotation = rotation_from_y_axis_direction(hole.axis)

print(s['A1'].to_glob_direction(hole.axis))
print(hole_axis.to_glob_direction((0,1,0)))

# rotation about Y-axis is allowed
hole_axis.fixed = True

hole_axis_rotation = s.new_axis('hole_axis_rotation')
hole_axis_rotation.parent = hole_axis
hole_axis_rotation.fixed = (True, True, True,
                            True, False, True)

# ----------- prepare pin

pin_axis = s.new_axis('pin_axis')
pin_axis.position = pin.parent.global_position
pin_axis.parent = pin.parent.parent
pin_axis.rotation = rotation_from_y_axis_direction(pin.axis)
pin_axis.fixed = (True, True, True,
                            True, False, True)

pin.parent.parent.change_parent_to(pin_axis)
pin.parent.parent.fixed = True

pin_axis.parent = hole_axis_rotation
pin_axis.rotation = (0,0,0)

pin_axis.position = (hole.radius - pin.radius,0,0)


print(s._vfc.to_string())

from DAVE.gui.main import Gui
Gui(s)

