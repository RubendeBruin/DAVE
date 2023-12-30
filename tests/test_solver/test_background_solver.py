from time import sleep

from DAVE import *
import DAVEcore as DC

def model():
    s = Scene()
    s.new_point("A", position=(0, 0, 10))
    s.new_rigidbody("B", mass=1, cog=(0.1, 0, 0.1), fixed= False)
    s.new_point("p1", "B")
    s.new_cable("c1", "A", "p1", EA=1)

    return s

def test():
    s = model()
    s.solve_statics()

def test_background():


    for i in range(1000):
        s = model()
        BackgroundSolver = DC.BackgroundSolver(s._vfc)

        BackgroundSolver.Start()

        while True:
            if not BackgroundSolver.Running:
                assert BackgroundSolver.Converged
                break

