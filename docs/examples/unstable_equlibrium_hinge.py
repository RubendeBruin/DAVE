from DAVE.scene import *


s = Scene()

s.new_axis('Axis')
s.new_axis('Axis_1', parent = 'Axis')

s['Axis_1'].position = (0.0, 0.0, 2.0)
s.new_rigidbody('Body', parent = 'Axis_1')

s['Body'].position = (0.0, 0.0, -5.0)

s['Body'].mass = 1.0

s['Axis'].fixed = (True, True, True, True, False, True)
s['Axis_1'].fixed = (True, True, True, True, False, True)

s.delete('Axis')

print(s._vfc.to_string())

# s.solve_statics()

from DAVE.gui.main import Gui
Gui(s)
