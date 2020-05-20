from DAVE.scene import *
from DAVE.rigging import create_shackle_gphd
# from DAVE.tools import rotation_from_y_axis_direction

s = Scene()

sizes = (120,150,200,250,300,400,500,600,700,800,900,1000,1250,1500)

for gp in sizes:
    b = create_shackle_gphd(s, f'sh{gp}', gp)
    b.x = gp / 100

s.new_geometriccontact("quick_action", "sh1500pin", "sh1250inside")

s.new_geometriccontact("quick_action_1", "sh1000inside", "sh1500bow")
s.new_geometriccontact("quick_action_2", "sh1000pin", "sh900inside")
s.new_geometriccontact("quick_action_3", "sh900inside", "sh1500bow")

s['sh1250'].fixed = (True, True, True, False, True, True)
s['sh1250'].mass = 1.99

s['sh1250'].rotation = (5.0, 0.0, 0.0)
s['sh1250'].mass = 1.99

s['sh1250'].rotation = (10.0, 0.0, 0.0)
s['sh1250'].mass = 1.99

s['sh1250'].rotation = (180.0, -5.0, 0.0)
s['sh1250'].mass = 1.99

s['sh1250'].rotation = (180.0, -10.0, 0.0)
s['sh1250'].mass = 1.99

s['sh1250'].rotation = (180.0, -15.0, 0.0)
s['sh1250'].mass = 1.99

s['sh1250'].rotation = (180.0, -20.0, 0.0)
s['sh1250'].mass = 1.99

s['sh1250'].rotation = (180.0, -10.0, 0.0)
s['sh1250'].mass = 1.99

s['sh1250'].rotation = (175.0, -10.0, 0.0)
s['sh1250'].mass = 1.99

s['sh1250'].rotation = (170.0, -10.0, 0.0)
s['sh1250'].mass = 1.99

s['sh1250'].rotation = (165.0, -10.0, 0.0)
s['sh1250'].mass = 1.99

s['sh1250'].rotation = (160.0, -10.0, 0.0)
s['sh1250'].mass = 1.99

s['sh1250'].rotation = (150.0, -10.0, 0.0)
s['sh1250'].mass = 1.99

s['sh1250'].rotation = (140.0, -10.0, 0.0)
s['sh1250'].mass = 1.99

s['quick_action_1'].flipped = True

s['quick_action_1'].flipped = False

s['quick_action_1'].flipped = True

s['quick_action_1'].flipped = False

s['quick_action_1'].flipped = True

s['quick_action_1'].flipped = False

s['quick_action_1'].flipped = True

s['quick_action_1'].flipped = False

s['quick_action_1'].flipped = True
s.delete("quick_action_1")

s['quick_action_3'].flipped = True

s['quick_action_3'].flipped = False

s['quick_action_3'].flipped = True

s['quick_action_3'].flipped = False

s['sh1000'].position = (12.5, -0.0, -3.021)
s['sh1000'].rotation = (127.279, 127.279, -0.0)
s['sh1000'].cog = (0.0, 0.0, 0.359)

s['sh1000'].position = (12.5, -0.0, -5.021)
s['sh1000'].rotation = (127.279, 127.279, -0.0)

s['sh1000'].position = (12.5, -0.0, -6.021)
s['sh1000'].rotation = (127.279, 127.279, -0.0)

s['sh1000'].position = (12.5, -0.0, -7.021)
s['sh1000'].rotation = (127.279, 127.279, -0.0)
s.new_geometriccontact("quick_action_1", "sh1000inside", "sh900pin")
s.new_geometriccontact("quick_action_4", "sh800inside", "sh1000pin")
s.new_geometriccontact("quick_action_5", "sh700inside", "sh800pin")
s.new_geometriccontact("quick_action_6", "sh600inside", "sh700pin")
s.new_cable("quick_action_7", poiA="sh600pin", poiB = "sh500inside")

s['quick_action_7'].length = 6.0
s['quick_action_7'].connections = ('sh600pin','sh500inside')

s['quick_action_7'].EA = 1.0
s['quick_action_7'].connections = ('sh600pin','sh500inside')

s['quick_action_7'].EA = 10.0
s['quick_action_7'].connections = ('sh600pin','sh500inside')

s['quick_action_7'].EA = 100.0
s['quick_action_7'].connections = ('sh600pin','sh500inside')

s['quick_action_7'].EA = 1000.0
s['quick_action_7'].connections = ('sh600pin','sh500inside')

from DAVE.gui.main import Gui
Gui(s, geometry_scale=0.001, cog_scale=0.001)
