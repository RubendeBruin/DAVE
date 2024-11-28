from DAVE import *

if __name__ == '__main__':
    s = Scene()

    point = s.new_point(name='Point')
    s.new_circle(name='Circle', parent=point, axis=(0, 1, 0), radius=1)
    s.new_circle(name='Circle2', parent='Point', axis=(0, 1, 0), radius=1)
    point = s.new_point(name='Point2')
    s.new_circle(name='Circle3', parent=point, axis=(0, 1, 0), radius=1)
    s.delete('Circle2')
    s.delete('Point2')
    point = s.new_point(name='Point2')
    s.new_circle(name='Circle2', parent=point, axis=(0, 1, 0), radius=1)
    s.new_circle(name='Circle3', parent='Point2', axis=(0, 1, 0), radius=1)
    s.delete('Circle3')
    point = s.new_point(name='Point3')
    s.new_circle(name='Circle3', parent=point, axis=(0, 1, 0), radius=1)

    s['Point'].position = (-4.0, 3.0, 0.0)
    s['Point3'].global_position = (5.290, -0.113, 3.982)

    s.new_cable("Cable", endA="Circle", endB="Circle3", sheaves=["Circle2"])

    # DG(s)