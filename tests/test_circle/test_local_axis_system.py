from DAVE import *

if __name__ == '__main__':
    s  = Scene()
    p1 = s.new_point(name='Point1', position=(0, 0, 0))

    c = s.new_circle(name='Circle', parent=p1, axis=(0, 1, 0), radius=1)


    for axis in [(0,0,1),(0,1,0),(1,0,0)]:
        c.axis = axis
        print(f"{axis} -> {c._local_y_axis} and {c._local_x_axis}")

    DG(s, autosave=False)