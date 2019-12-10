"""
Ballasting
"""
import numpy as np
from scipy.optimize import minimize, minimize_scalar
import matplotlib.pyplot as plt

from DAVE.scene import *


def visualize_optimiaztion(fun, xlim, ylim):
    step = 1
    x,y = np.meshgrid(np.arange(xlim[0], xlim[1] + step, step),
                      np.arange(ylim[0], ylim[1] + step, step))
    def fun2(x,y):
        return fun([x,y])

    funn = np.vectorize(fun2)
    z = funn(x,y)

    fig = plt.figure(figsize=(8, 5))

    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib.colors import LogNorm

    ax = plt.axes(projection='3d', elev=50, azim=-50)

    ax.plot_surface(x, y, z, norm=LogNorm(), rstride=1, cstride=1,
                    edgecolor='none', alpha=.8, cmap=plt.cm.jet)

    plt.show()





def force_vessel_to_evenkeel_and_draft(scene, vessel, z):
    """
    Calculates the required force to be applied to place the vessel even-keel at the given vertical position (-draft if origin is at keel).

    Args:
        scene:  Scene
        vessel: Vessel node or vessel node name
        draft:  requested vertical position of vessel axis system origin. If the vessel origin is at the keel than this is minus draft

    Returns:
        Required external force and position (F,x,y) to be applied to the the vessel to the given position
    """



    vessel = scene._node_from_node_or_str(vessel)

    # store old props
    # old_position = vessel.position
    # old_rotation = vessel.rotation
    old_parent = vessel.parent
    old_fixed = vessel.fixed

    if vessel.parent is not None:
        raise Exception('Vessel with parent : not yet implemented')

    # Create a dummy at the vessel origin
    dummy_name = scene.available_name_like(vessel.name + "dummy")
    dummy = scene.new_axis(dummy_name)
    dummy.change_parent_to(vessel)
    dummy.parent = None

    # set dummy to even-keel
    dummy.rx = 0
    dummy.ry = 0
    dummy.z = z
    fixed = [1,1,1,1,1,1]
    fixed[0] = old_fixed[0]  # allowed to surge
    fixed[1] = old_fixed[1]  # allowed to sway
    fixed[5] = old_fixed[5] # allowed to yaw

    dummy.fixed = fixed

    # Change vessel parent to dummy
    vessel.parent = dummy
    vessel.position = (0,0,0)
    vessel.rotation = (0,0,0)
    vessel.fixed = True

    # solve statics
    scene.solve_statics()

    force = vessel.connection_force

    vessel.parent = old_parent
    vessel.fixed = old_fixed
    scene.delete(dummy_name)

    F = -force[2]

    if abs(F)<1e-6:
        print('No force required to get to requested draft')
        return (0,0,0)

    x = -force[4] / force[2]
    y = force[3] / force[2]

    print('Required force of {} kN at position x={}m and y={}m'.format(F,x,y))

    return (F,x,y)



class Tank:
    def __init__(self):
        self.name = "noname"
        self.max = 0
        self.pct = 0
        self.position = np.array((0.,0.,0.))

    def weight(self):
        return self.max *  self.pct / 100

    def is_full(self):
        return self.pct>=100-1e-5

    def is_empty(self):
        return self.pct<=1e-5

    def is_partial(self):
        return (not self.is_empty() and not self.is_full())

    def mxmymz(self):
        return self.position * self.weight()

    def capacity(self):
        return self.max

    def fillpct(self):
        return self.pct

    def make_empty(self):
        self.pct = 0

    def make_full(self):
        self.pct = 100

    def is_frozen(self):
        return False

class BallastSystemSolver:

    def __init__(self, ballast_system_node):

        self.BallastSystem = ballast_system_node

        self._target_cog = np.array((0.,0.,0.))
        self._target_wt = 0

    def xyzw(self):
        return self.BallastSystem.xyzw()

    def _error(self):
        (cog, wt) = self.xyzw()

        dx = cog[0] - self._target_cog[0]
        dy = cog[1] - self._target_cog[1]
        dw = wt - self._target_wt

        return dx**2 + dy**2 + dw **2

    def optimize_tank(self, tank):
        E0 = self._error()
        p0 = tank.pct

        # fill tank
        tank.pct = 100
        if self._error() < E0:
            return True

        # empty tank
        tank.pct = 0
        if self._error() < E0:
            return True

        # optimum must be somewhere in between

        def fun(x):
            if hasattr(x, "__len__"):
                tank.pct = x[0]
            else:
                tank.pct = x
            return self._error()


        res = minimize_scalar(fun, bounds=(0,100),method='Bounded')

        if not res.success:
            x = np.linspace(0,100,num=101)
            funn = np.vectorize(fun)
            y = funn(x)
            plt.plot(x,y)
            plt.show()
            print('SUB-OPTIMIZATION FAILED FOR ONE TANK!!!')
            # raise ArithmeticError('Optimization failed')

        if res.x > 100:
            print('error with bounds')

        # Did the optimization result in a different tank fill
        if abs(p0-res.x) > 0.0001:
            print('Tank {} set to {}'.format(tank.name, res.x))
            tank.pct = res.x
            return True

        return False

    def optimize_multiple_partial(self, tanks):

        E0 = self._error()


        n_tanks = len(tanks)

        # See if it is possible to empty one of the tanks and get an result that is at least as good
        if n_tanks == 2:

            store_tank1 = tanks[1].pct
            store_tank0 = tanks[0].pct

            # empty second tank and optimize first one
            tanks[1].make_empty()
            if self.optimize_tank(tanks[0]):
                if self._error() < E0:
                    return True
            tanks[1].pct = store_tank1

            # fill first tank and optimize second one
            tanks[0].make_full()
            if self.optimize_tank(tanks[1]):
                if self._error() < E0:
                    return True
            tanks[0].pct = store_tank0

            # fill second tank and optimize first one
            tanks[1].make_full()
            if self.optimize_tank(tanks[0]):
                if self._error() < E0:
                    return True
            tanks[1].pct = store_tank1

            # empty first tank and optimize second one
            tanks[0].make_empty()
            if self.optimize_tank(tanks[1]):
                if self._error() < E0:
                    return True
            tanks[0].pct = store_tank0


        # See if it is possible to empty one of the tanks and get an result that is at least as good
        if n_tanks > 2:
            # two slack tanks should be enough in most cases
            for i_empty in reversed(range(n_tanks)):
                subset = []
                for i in range(n_tanks):
                    if i == i_empty:
                        tanks[i].pct = 0
                    else:
                        subset.append(tanks[i])

                if self.optimize_multiple_partial(subset):
                    if self._error() <= E0:
                        print('Removed one of the slack tanks')
                        return True

        # See if it is possible to fill one of the tanks and get an result that is at least as good
        if n_tanks>2:
            # two slack tanks should be enough in most cases
            for i_full in range(n_tanks):
                subset = []
                for i in range(n_tanks):
                    if i==i_full:
                        tanks[i].pct=100
                    else:
                        subset.append(tanks[i])

                if self.optimize_multiple_partial(subset):
                    if self._error() <= E0:
                        print('Removed one of the slack tanks')
                        return True



        def fun(x):
            for i,tank in enumerate(tanks):
                tank.pct = x[i]
            return self._error()

        x0 = []
        bnds = []

        for tank in tanks:
            x0.append(tank.pct)
            bnds.append((0., 100.))

        res = minimize(fun, x0=np.array(x0), bounds=bnds)

        if not res.success:
            print('SUB-OPTIMIZATION FAILED FOR {} TANKS'.format(n_tanks))
            # raise ArithmeticError('Optimization failed')  # TODO: possible to use a more robust routine?
            if n_tanks==2: # we can plot this!
                visualize_optimiaztion(fun, (0,100), (0,100))


        # apply the result
        fun(res.x)

        # Did the optimization result in a different tank fill
        if self._error() < E0:
            print('multi-opt result = ', res.x)
            return True

        return False

    def ballast_to(self, cogx, cogy, weight):

        _log = []

        self._target_wt = weight
        self._target_cog[0] = cogx - self.BallastSystem.position[0]
        self._target_cog[1] = cogy- self.BallastSystem.position[1]


        # print log:
        print('ballasting to volume of {} kN'.format(self._target_wt ))
        print('at {} , {}'.format(self._target_cog[0],self._target_cog[1] ))

        print('using:')
        for tank in self.BallastSystem.tanks:
            print('{} of {} at {} {} {}'.format(tank.name, tank.capacity(), *tank.position))
        print('-----------------------------')


        while True:

            _log.append([tank.pct for tank in self.BallastSystem.tanks])
            print(_log[-1])

            if self._error() < 1e-5:
                break

            # optimize partially filled tanks
            partials = []
            for tank in self.BallastSystem.tanks:
                if tank.is_partial():
                    partials.append(tank)

            if len(partials) == 1:
                if self.optimize_tank(partials[0]):
                    continue


            if len(partials) > 1:
                if self.optimize_multiple_partial(partials):
                    continue

            changed = False

            for tank in self.BallastSystem.tanks:
                if self.optimize_tank(tank):
                    changed = True
                    break

            if changed:
                continue

            # optimizing the currently partial tanks failed
            # keeping the currently partial tanks and optimizing any one of the other tanks failed

            for tank in self.BallastSystem.tanks:
                if tank not in partials:
                    temp = partials.copy()
                    temp.append(tank)
                    if self.optimize_multiple_partial(temp):
                        changed = True
                        break

            if changed:
                continue

            print([t.pct for t in self.BallastSystem.tanks])
            print(self._error())
            print(self.xyzw())

            raise ArithmeticError('Optimization failed')


        print(self._error())
        print(self.xyzw())
        print([t.pct for t in self.BallastSystem.tanks])
        # plt.plot(_log)
        # plt.show()

# ====== main code ======

if __name__ == '__main__':

    # make four tanks
    t1 = Tank()
    t1.position = np.array((10.,10.,0))
    t1.max = 500


    t2 = Tank()
    t2.position = np.array((10., -10., 0))
    t2.max = 500

    t3 = Tank()
    t3.position = np.array((-10., -10., 0))
    t3.max = 500

    t4 = Tank()
    t4.position = np.array((-10., 10., 0))
    t4.max = 500

    t5 = Tank()
    t5.position = np.array((40., 10., 0))
    t5.max = 500

    t6 = Tank()
    t6.position = np.array((40., -10., 0))
    t6.max = 500

    t7 = Tank()
    t7.position = np.array((-40., -10., 0))
    t7.max = 500

    t8 = Tank()
    t8.position = np.array((-40., 10., 0))
    t8.max = 500

    t1.name = 't1'
    t2.name = 't2'
    t3.name = 't3'
    t4.name = 't4'
    t5.name = 't5'
    t6.name = 't6'
    t7.name = 't7'
    t8.name = 't8'

    # s = system()

    s = Scene()
    a = s.new_axis('as')

    bs = s.new_ballastsystem('bs',parent=a)

    bs.tanks.extend([t1,t2,t3,t4,t5,t6,t7,t8])

    bso = BallastSystemSolver(bs)

    s['Barge'].mass = 10000

    bso.ballast_to(0,5,2100)

"""
If more than three slack tanks

Fill the fullest one
or empty the emptiest one

and resolve

"""

