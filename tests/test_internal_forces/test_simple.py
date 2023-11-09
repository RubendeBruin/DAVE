from DAVE import *
import numpy as np

def model():
    s = Scene()
    s.new_frame('bar')
    s.new_point('p', parent='bar', position = (10,0,1))
    f = s.new_force('F', parent='p', force = (10,0,0))

    return s


if __name__ == '__main__':
    s = model()

    # make 100 random numbers
    r = np.random.rand(100)


    for i,rn in enumerate(r):
        rn = rn-0.5
        p = s.new_point(f'p{i}', parent='bar', position = (20*rn,-np.sin(rn),np.cos(3*rn)))
        f = s.new_force(f'F{i}', parent=p, force = (np.sin(5*rn),np.cos(rn/2),np.sin(33*rn)))

    bar : Frame = s['bar']
    lsd = bar.give_load_shear_moment_diagram()

    lsd.plot_components()

    import matplotlib.pyplot as plt
    plt.show()

