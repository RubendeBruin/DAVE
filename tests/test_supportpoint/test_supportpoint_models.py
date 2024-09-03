from DAVE import *

def model():
    s = Scene()
    f = s.new_frame('frame')

    rb = s.new_rigidbody('rb', mass = 100, fixed = False)
    p = s.new_point('point', parent = rb, position = (1,2,3))

    # sp = SupportPoint(s, 'sp')
    sp = s.new_supportpoint('sp', 'frame','point',kz=1000, kx = 1, ky = 1)

    return s

if __name__ == '__main__':
    s = model()

    # s.solve_statics()

    DG(s)