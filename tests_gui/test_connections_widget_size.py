"""The widget showing the connections of a cable can get too small on small screens.
Enforce a minimum height for the widget.
"""

from DAVE import *
from DAVE.gui import Gui

s = Scene()
for i in range(30):
    s.new_point(f"p{i}", position=(i, 0, 0))

s.new_cable('cable', connections=('p0','p1'))

Gui(s)