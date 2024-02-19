from DAVE import *

s = Scene()
s.new_point(name="Point1", position=(-10, 0, 0))
s.new_circle(name="Circle1", parent="Point1", axis=(0, 1, 0), radius=1)

s.new_point(name="Point2", position=(0, 0, 10))
s.new_circle(name="Circle2", parent="Point2", axis=(0, 1, 0), radius=1)

s.new_point(name="Point3", position=(10, 0, 0))
s.new_circle(name="Circle3", parent="Point3", axis=(0, 1, 0), radius=1)

c = s.new_cable(name="Cable", connections=("Circle1", "Circle2", "Circle3"))

DG(s)
