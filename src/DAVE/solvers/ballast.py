"""
Ballasting
"""
import numpy as np
from scipy.optimize import minimize, minimize_scalar
import matplotlib.pyplot as plt

from DAVE.scene import *
import DAVE.settings as ds

# ================== local ballast system class =========
# This is an extract of the class that used to be in Scene

class OptBallastSystem():
    """A BallastSystem
    The position of the axis system is the reference position for the tanks.
    Tanks can be added using new_tank()
    technical notes:
    - System is similar to the setup of RigidBody, but without the Axis
    - The class extends Poi, but overrides some of its properties
    - Update nees to be called to update the weight and cog
    """

    # Tank is an inner class
    class Tank:

        def __init__(self):
            self.name = "noname"
            """Name of the tank"""

            self.max = 0
            """Maximum fill in [kN]"""

            self.pct = 0
            """Actual fill percentage in [%]"""

            self.position = np.array((0., 0., 0.))
            """Tank CoG position relative to ballast system origin [m,m,m]"""

            self.frozen = False
            """The fill of frozen tanks should not be altered"""

            self._pointmass = None
            """Optional reference to pointmass node - handled by ballastsystem node"""

        @property
        def inertia(self):
            return self.weight() / vfc.G

        def weight(self):
            """Returns the actual weight of tank contents in kN"""
            return self.max * self.pct / 100

        def is_full(self):
            """Returns True of tank is (almost) full"""
            return self.pct >= 100 - 1e-5

        def is_empty(self):
            """Returns True of tank is (almost) empty"""
            return self.pct <= 1e-5

        def is_partial(self):
            """Returns True of tank not full but also not empty"""
            return (not self.is_empty() and not self.is_full())

        def mxmymz(self):
            """Position times actual weight"""
            return self.position * self.weight()

        def make_empty(self):
            """Empties the tank"""
            self.pct = 0

        def make_full(self):
            """Fills the tank"""
            self.pct = 100

    def __init__(self):


        self._tanks = []
        """List of tank objects"""

        self._cog = (0., 0., 0.)
        """Position of the CoG of the ballast-tanks relative to self._position, calculated when calling update()"""

        self._weight = 0
        """Weight [kN] of the ballast-tanks , calculated when calling update()"""

        self.frozen = False
        """The contents of a frozen tank should not be changed"""

    def update(self):
        self._cog, self._weight, = self.xyzw()
        self._weight = np.around(self._weight, decimals=5)

        # we are rounding a bit here to avoid very small numbers
        # which would mess-up the solver
        pos = np.array(self._cog) + np.array(self.position)
        pos = np.around(pos, 5)

        self._vfNode.position = pos

        self._vfForce.force = (0, 0, -self._weight)

        for tank in self._tanks:
            I = tank.inertia
            pos = np.array(tank.position) + np.array(self.position)
            tank._pointmass.inertia = tank.inertia
            tank._pointmass.position = pos


    def new_tank(self, name, position, capacity_kN, actual_fill=0, frozen=False):
        """Creates a new tanks and adds it to the ballast-system

        Args:
            name: (str) name of the tanks
            position: (float[3]) position of the tank [m,m,m]
            capacity_kN: (float) Maximum capacity of the tank in [kN]
            actual_fill: (float) Optional, actual fill percentage of the tank [0] [%]
            frozen: (bool) Optional, the contents of frozen tanks should not be altered
        Returns:
            BallastSystem.Tank object
        """
        # asserts

        assert3f(position, "position")
        assert1f(capacity_kN, "Capacity in kN")
        assert1f(actual_fill, "Actual fill percentage")
        assertValidName(name)

        assert name not in [t.name for t in self._tanks], ValueError(
            'Double names are not allowed, {} already exists'.format(name))

        t = OptBallastSystem.Tank()
        t.name = name
        t.position = position
        t.max = capacity_kN
        t.pct = actual_fill
        t.frozen = frozen

        self._tanks.append(t)

        return t



    def tank_names(self):
        return [tank.name for tank in self._tanks]

    def fill_tank(self, name, fill):

        assert1f(fill, "tank fill")

        for tank in self._tanks:
            if tank.name == name:
                tank.pct = fill
                return
        raise ValueError('No tank with name {}'.format(name))

    def xyzw(self):
        """Gets the current ballast cog and weight from the tanks
                Returns:
                    (x,y,z), weight
                """
        """Calculates the weight and inertia properties of the tanks"""

        mxmymz = np.array((0., 0., 0.))
        wt = 0

        for tank in self._tanks:
            w = tank.weight()
            p = np.array(tank.position, dtype=float)
            mxmymz += p * w

            wt += w

        if wt == 0:
            xyz = np.array((0., 0., 0.))
        else:
            xyz = mxmymz / wt

        return xyz, wt


    def tank(self, name):

        for t in self._tanks:
            if t.name == name:
                return t
        raise ValueError('No tank with name {}'.format(name))

    def __getitem__(self, item):
        return self.tank(item)

    @property
    def cogx(self):
        """X position of combined CoG of all tank contents in the ballast-system. (local coordinate) [m]"""
        return self.cog[0]

    @property
    def cogy(self):
        """Y position of combined CoG of all tank contents in the ballast-system. (local coordinate) [m]"""
        return self.cog[1]

    @property
    def cogz(self):
        """Z position of combined CoG of all tank contents in the ballast-system. (local coordinate) [m]"""
        return self.cog[2]

    @property
    def cog(self):
        """Combined CoG of all tank contents in the ballast-system. (local coordinate) [m,m,m]"""
        self.update()
        return (self._cog[0], self._cog[1], self._cog[2])

    @property
    def weight(self):
        """Total weight of all tank fillings in the ballast system [kN]"""
        self.update()
        return self._weight


# ================== and tanks ==========================


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
    dummy = scene.new_frame(dummy_name, parent = vessel)
    dummy.change_parent_to(None)

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

    vessel.change_parent_to(old_parent)
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





class BallastSystemSolver:
    """
    Changes in ballast system are condidered ok if either

    the error reduced with at least min_error_reduction
    the system is a a better state (more filling in higher priority tank without increasing the error)

    """

    def __init__(self, ballast_system_node):

        self.ballast_system_node = ballast_system_node
        self.BallastSystem = None

        self._target_cog = np.array((0.,0.,0.))
        self._target_wt = 0
        self.tolerance = 1e-3
        self.silent = True
        self.min_error_reduction = self.tolerance/25

        self._no_single_optimization = False
        self._no_double_optimization = False


    def print(self, *kwarg):
        if not(self.silent):
            print(*kwarg)


    def xyzw(self):
        return self.BallastSystem.xyzw()

    def _error(self):
        (cog, wt) = self.xyzw()

        dx = cog[0] - self._target_cog[0]
        dy = cog[1] - self._target_cog[1]
        dw = wt - self._target_wt

        return dx**2 + dy**2 + 0.1*dw **2

    def optimize_tank(self, tank):
        """Optimizes a single tank

        the optimized value of a tank is the missing total mass.
        But only if it is at the other side of the target cog

        """
        if self._no_single_optimization:
            return False


        p0 = tank.pct
        E0 = self._error()

        tank.pct = 0

        [Ox, Oy, _], Om = self.xyzw()  # m,m,kN
        Tx = self._target_cog[0]
        Ty = self._target_cog[1]
        Tm = self._target_wt

        x = tank.position[0]
        y = tank.position[1]

        # tank position must be on the other side of the target

        # target to actual vector
        actual_pos = (Ox - Tx, Oy - Ty)
        tank_pos = (x-Tx, y - Ty)

        # tank is on the other side if dot-product is negative
        if np.dot(actual_pos, tank_pos) > 0:
            return False

        # missing weight  [kN]
        req_wt = Tm - Om

        if req_wt == 0:
            # already optimized
            return False

        max_wt = tank.max

        req_pct = 100*req_wt / max_wt

        print(f'Reqired mass  : {req_wt}')
        print(f'Optimum for tank {tank.name} : {req_pct}')

        req_pct = min(100, req_pct)
        req_pct = max(0, req_pct)

        if req_pct == p0:
            tank.pct = p0
            return False

        # calculate new error
        weight = req_pct * max_wt / 100

        xx = (Tx*Om + x * weight) / (Om + weight)
        yy = (Ty*Om + y * weight) / (Om + weight)


        E = (Tx-xx)**2 + (Ty-yy)**2
        if E < E0:
            tank.pct = req_pct

            print(f'Optimized tank {tank.name} to {req_pct}')

            return True

        tank.pct = p0
        return False
        #
        #
        #
        #
        #
        #
        #
        #
        #
        # self.print('-- optimize tank -- {}'.format(tank.name))
        #
        # p0 = tank.pct
        # E0 = self._error()
        #
        # tank.pct = 0
        #
        # [Ox, Oy, _], Om = self.xyzw()
        # Tx = self._target_cog[0]
        # Ty = self._target_cog[1]
        # Tm = self._target_wt
        #
        # x = tank.position[0]
        # y = tank.position[1]
        #
        # # Optimum fill for combined cog position
        # denom = (Om*Ox*Tx - Om*Ox*x - Om*Tx*x - Om*Ty*y + Om*Ty + Om*x**2 + Om*y**2 - Om*y + Oy*Ty - Oy*y)
        #
        # if denom != 0:
        #     opt_pos = (Om**2*Ox**2 - Om**2*Ox*Tx - Om**2*Ox*x + Om**2*Tx*x + Om**2*Ty*y - Om**2*Ty - Om**2*y + Om**2 - Om*Oy*Ty - Om*Oy*y + 2*Om*Oy + Oy**2)/denom
        # else:
        #     opt_pos = tank.max
        #
        # # Optimum fill for mass
        # opt_mass = Tm - Om
        #
        # # Tank in wrong quadrant (fill for mass and empty for position of vice versa)
        # if opt_mass * opt_pos < 0:
        #     tank.pct = 0
        #     return p0!=0
        #
        # opt = 0.7 * opt_pos + 0.3 * opt_mass # combine
        #
        # print(f'Optimum for tank {tank.name} = {100*opt / tank.max}')
        #
        # opt_pct = 100*opt / tank.max
        # if abs(opt_pct-p0) < 1e-3:
        #     tank.pct = p0
        #     return False
        #
        # if opt_pct>100:
        #     if p0 < 100:
        #         tank.pct=100
        #     else:
        #         tank.pct = p0
        #         return False
        # elif opt_pct <= 0:
        #     if p0 > 0:
        #         tank.pct = 0
        #     else:
        #         tank.pct = p0
        #         return False
        #
        # else:
        #     tank.pct = opt_pct
        #
        # if self._error() < E0:
        #     return True
        #
        # else:
        #     tank.pct = p0
        #     return False



    def optimize_multiple_partial(self, tanks):

        print([tank.name for tank in tanks])

        E0 = self._error()
        p0 = list()
        for tank in tanks:
            p0.append(tank.pct)

        n_tanks = len(tanks)

        self.print('Optimizing multiple ( n = {} ) tanks:'.format(n_tanks))
        self.print('Initial error {}'.format(E0))

        for tank in tanks:
            self.print('{} == {} '.format(tank.name, tank.pct))



        # See if it is possible to empty or fill one of the tanks and get an result that is at least as good
        # This does not need to decrease the error because it leads to a better state
        # Except if that tank was already empty or full

        if n_tanks == 2:

            store_tank1 = tanks[1].pct
            store_tank0 = tanks[0].pct

            # empty second tank and optimize first one
            if not tanks[1].is_empty():
                tanks[1].make_empty()
                self.optimize_tank(tanks[0])
                if self._error() <= E0:
                    return True
                tanks[1].pct = store_tank1

            # fill first tank and optimize second one
            if not tanks[0].is_full:
                tanks[0].make_full()
                self.optimize_tank(tanks[1])
                if self._error() <= E0:
                    return True
                tanks[0].pct = store_tank0

            # fill second tank and optimize first one
            if not tanks[1].is_full:
                tanks[1].make_full()
                self.optimize_tank(tanks[0])
                if self._error() <= E0:
                    return True
                tanks[1].pct = store_tank1

            # empty first tank and optimize second one
            if not tanks[0].is_empty:
                tanks[0].make_empty()
                self.optimize_tank(tanks[1])
                if self._error() <= E0:
                    return True
                tanks[0].pct = store_tank0


        # More than two tanks - make empty
        if n_tanks > 2:
            for i_empty in reversed(range(n_tanks)):

                # set original fillings
                for tank,fill in zip( tanks, p0):
                    tank.pct = fill

                if tanks[i_empty].is_empty(): # do not empty tanks that were already full
                    continue

                subset = []
                for i in range(n_tanks):
                    if i == i_empty:
                        tanks[i].pct = 0
                    else:
                        subset.append(tanks[i])

                if self.optimize_multiple_partial(subset):
                    if self._error() <= E0:
                        self.print('Removed one of the slack tanks')
                        for tank in tanks:
                            self.print('{} == {} '.format(tank.name, tank.pct))

                        return True

        #  More than two tanks - make full
        if n_tanks>2:
            for i_full in range(n_tanks):

                # set original fillings
                for tank, fill in zip(tanks,p0):
                    tank.pct = fill

                if tanks[i_full].is_full():  # do not fill tanks that were already full
                    continue

                subset = []
                for i in range(n_tanks):
                    if i==i_full:
                        tanks[i].pct=100
                    else:
                        subset.append(tanks[i])

                if self.optimize_multiple_partial(subset):
                    if self._error() <= E0:
                        self.print('Removed one of the slack tanks')
                        return True


        # =========== It was not possible to improve the state by filling or emptying one of the tanks partial completely ====
        #
        # Do an optimization over all the given tanks



        if n_tanks == 1:
            return self.optimize_tank(tank)

        self._no_single_optimization = True

        if n_tanks == 2:
            return self.optimize_two_tanks(tanks[0], tanks[1])

        self._no_double_optimization = True

        if n_tanks == 3:
            return self.optimize_three_tanks(tanks[0], tanks[1], tanks[2])

        # Get the combined properties off all other tanks together
        for tank in tanks:
            tank.pct = 0

        [Ox, Oy, _], Om = self.xyzw()
        Tx = self._target_cog[0]
        Ty = self._target_cog[1]
        Tm = self._target_wt

        # set original fillings
        for tank, fill in zip(tanks,p0):
            tank.pct = fill

        def fun(x):

            mm = Om
            xx = Ox * mm
            yy = Oy * mm

            for i,tank in enumerate(tanks):
                mass = x[i] * tank.max / 100
                mm += mass
                xx += mass * tank.position[0]
                yy += mass * tank.position[1]

            cogx = xx/mm
            cogy = yy/mm

            error = (Tx - cogx)** 2 + (Ty-cogy)**2 + 0.1 * (mm-Tm)**2

            return error

        x0 = []
        bnds = []

        for tank in tanks:
            x0.append(tank.pct)
            bnds.append((0., 100.))

        res = minimize(fun, x0=np.array(x0), bounds=bnds) # , method="trust-constr" is slowest but give best results?

        if not res.success:
            self.print('SUB-OPTIMIZATION FAILED FOR {} TANKS'.format(n_tanks))

            # Often it fails because the solution any point on a line.

            # raise ArithmeticError('Optimization failed')  # TODO: possible to use a more robust routine?
            # if n_tanks==2: # we can plot this!
            #     visualize_optimiaztion(fun, (0,100), (0,100))


        # apply the result
        for i, tank in enumerate(tanks):
            tank.pct = res.x[i]

        # Did the optimization result in a different tank fill
        if self._error() < E0-self.min_error_reduction:

            self.print('Before optimaliz = ', x0)
            self.print('multi-opt result = ', res.x)

            return True

        # set original fillings
        for tank, fill in zip(tanks, p0):
            tank.pct = fill
        return False

    def optimize_two_tanks(self, tank1, tank2):
        print(f'optimizing {tank1.name}, {tank2.name}')
        if self._no_double_optimization:
            return False

        p1 = tank1.pct
        p2 = tank2.pct

        E0 = self._error()

        tank1.pct = 0
        tank2.pct = 0

        [Ox, Oy, _], Om = self.xyzw()  # m,m,kN
        Tx = self._target_cog[0]
        Ty = self._target_cog[1]
        Tm = self._target_wt

        x1 = tank1.position[0]
        y1 = tank1.position[1]

        x2 = tank2.position[0]
        y2 = tank2.position[1]

        # analytical optimum for weight in tank1
        f1 = (-Om*Ox*x1 + Om*Ox*x2 + Om*x1*x2 - Om*x2**2 + Om*y1*y2 - Om*y1 - Om*y2**2 + Om*y2 - Oy*y1 + Oy*y2 + Tm*Tx*x1 - Tm*Tx*x2 + Tm*Ty*y1 - Tm*Ty*y2 - Tm*x1*x2 + Tm*x2**2 - Tm*y1*y2 + Tm*y2**2)/(x1**2 - 2*x1*x2 + x2**2 + y1**2 - 2*y1*y2 + y2**2)

        f1 = min(f1, tank1.max)
        f1 = max(f1, 0)

        f2 = Tm - Om - f1

        f2 = min(f2, tank2.max)
        f2 = max(f2, 0)

        # does this make things better?
        tank1.pct = 100*f1 / tank1.max
        tank2.pct = 100*f2 / tank2.max

        if self._error()<E0:
            print('worked!')
            return True
        else:
            tank1.pct=p1
            tank2.pct=p2
            return False

    def optimize_three_tanks(self, tank1, tank2, tank3):
        print(f'optimizing {tank1.name}, {tank2.name}, {tank3.name}')

        p1 = tank1.pct
        p2 = tank2.pct
        p3 = tank3.pct

        E0 = self._error()

        tank1.pct = 0
        tank2.pct = 0
        tank3.pct = 0

        [Ox, Oy, _], Om = self.xyzw()  # m,m,kN
        Tx = self._target_cog[0]
        Ty = self._target_cog[1]
        Tm = self._target_wt

        x1 = tank1.position[0]
        y1 = tank1.position[1]

        x2 = tank2.position[0]
        y2 = tank2.position[1]

        x3 = tank3.position[0]
        y3 = tank3.position[1]

        # analytical optimum
        denom = x1 * y2 - x1 * y3 - x2 * y1 + x2 * y3 + x3 * y1 - x3 * y2

        if abs(denom)<1e-6:
            tank1.pct = p1
            tank2.pct = p2
            tank3.pct = p3
            return False

        f1 = (-Om * Ox * y2 + Om * Ox * y3 - Om * x2 * y3 + Om * x2 + Om * x3 * y2 - Om * x3 + Oy * x2 - Oy * x3 + Tm * Tx * y2 - Tm * Tx * y3 - Tm * Ty * x2 + Tm * Ty * x3 + Tm * x2 * y3 - Tm * x3 * y2) / denom
        f2 = (Om * Ox * y1 - Om * Ox * y3 + Om * x1 * y3 - Om * x1 - Om * x3 * y1 + Om * x3 - Oy * x1 + Oy * x3 - Tm * Tx * y1 + Tm * Tx * y3 + Tm * Ty * x1 - Tm * Ty * x3 - Tm * x1 * y3 + Tm * x3 * y1) / denom

        f1 = min(f1, tank1.max)
        f1 = max(f1, 0)

        f2 = min(f2, tank2.max)
        f2 = max(f2, 0)

        f3 = Tm - Om - f1 - f2

        f3 = min(f3, tank3.max)
        f3 = max(f3, 0)

        # does this make things better?
        tank1.pct = 100*f1 / tank1.max
        tank2.pct = 100*f2 / tank2.max
        tank3.pct = 100*f3 / tank3.max

        if self._error()<E0:
            print('worked!')
            return True
        else:
            print('Could not find a better optimum than:')
            print(f'{tank1.name} : {tank1.pct}')
            print(f'{tank2.name} : {tank2.pct}')
            print(f'{tank3.name} : {tank3.pct}')

            tank1.pct=p1
            tank2.pct=p2
            tank3.pct=p3
            return False


    def optimize_using(self, tanks):
        """Optimize using the given tanks. No fancy combinations"""

        names = ''
        for t in tanks:
            names += ' ' + t.name + '(' + str(t.pct) + ')'
        print('Optimize using {} tanks: {}'.format(len(tanks), names))

        E0 = self._error()
        p0 = list()
        for tank in tanks:
            p0.append(tank.pct)

        def fun(x):
            for i, tank in enumerate(tanks):
                tank.pct = x[i]
            return self._error()

        x0 = []
        bnds = []

        for tank in tanks:
            x0.append(tank.pct)
            bnds.append((0., 100.))

        res = minimize(fun, x0=np.array(x0), bounds=bnds)

        if not res.success:
            self.print('SUB-OPTIMIZATION FAILED FOR {} TANKS'.format(len(tanks)))

        # apply the result
        fun(res.x)

        # Did the optimization result in a different tank fill
        if self._error() < E0:
            self.print('Before optimaliz = ', x0)
            self.print('multi-opt result = ', res.x)
            return True
        else:
            self.print('multi-opt result = ', res.x)

        # set original fillings
        for tank, fill in zip(tanks, p0):
            tank.pct = fill
        return False

    def get_tank_to_optimize_with(self, optTanks, do_plot = False):

        [Ox, Oy, _], Om = self.xyzw()  # m,m,kN
        Tx = self._target_cog[0]
        Ty = self._target_cog[1]

        chk = abs(self._target_wt - Om)
        if chk > 1:
            raise ValueError("Only call this function when all fluid is already in")

        # target to actual vector
        actual_pos = (Ox - Tx, Oy - Ty)

        if do_plot:
            self.plot(optTanks)
            plt.axis('equal')
            plt.plot(Ox,Oy, 'rx')
            plt.plot(Tx,Ty, 'go')


        # try to find a full tank to optimize with

        # tank to drain
        for tank in reversed(optTanks):
            if tank.is_empty():
                continue
            if tank.is_partial():
                continue

            x = tank.position[0]
            y = tank.position[1]
            tank_pos = (x - Tx, y - Ty)

            # this is a tank that is going be emptied, so it needs to be on the same side as the actual cog

            # tank is on the other side if dot-product is negative
            if np.dot(actual_pos, tank_pos) > 0:
                print(f'tank to drain {tank.name}')
                if do_plot:
                    plt.plot(x,y,'y*')
                return tank

        # Tank to fill

        for tank in optTanks:
            if tank.is_full():
                continue
            if tank.is_partial():
                continue

            x = tank.position[0]
            y = tank.position[1]
            tank_pos = (x - Tx, y - Ty)

            # this is a tank that is going be filled, so it needs to be on the other side as the actual cog

            # tank is on the other side if dot-product is negative
            if np.dot(actual_pos, tank_pos) < 0:
                print(f'tank to fill {tank.name}')
                if do_plot:
                    plt.plot(x, y, 'y*')
                return tank

        print('No logical tank found, returning the first tank of the list')
        return optTanks[0]

    def ballast_to(self, cogx, cogy, weight):
        """cogx, cogy : local position relative to parent"""


        # create an own ballast-system based on the tanks of the node
        self.BallastSystem = OptBallastSystem()

        for tank in self.ballast_system_node.tanks:
            old_fill = tank.fill_pct
            if tank.fill_pct < 1:
                tank.fill_pct = 100
            self.BallastSystem.new_tank(tank.name, position=tank.cog_local, capacity_kN=tank.volume * tank.density * 9.81, actual_fill=old_fill, frozen=self.ballast_system_node.is_frozen(tank.name))
            tank.fill_pct = old_fill

        _log = []

        self._target_wt = weight
        self._target_cog[0] = cogx
        self._target_cog[1] = cogy

        # Get usable tanks
        optTanks = []
        for tank in self.BallastSystem._tanks:
            if not tank.frozen:
                optTanks.append(tank)



        # print log:
        print('ballasting to volume of {} kN'.format(self._target_wt ))
        print('at {} , {}'.format(self._target_cog[0],self._target_cog[1] ))

        print('using:')
        for tank in optTanks:
            print('{} of {} [ {}% full ]at {} {} {}'.format(tank.name, tank.max, tank.pct, *tank.position))
        print('-----------------------------')


        while True:

            if self._error() < self.tolerance:
                break

            [Ox, Oy, _], Om = self.xyzw()

            # if we do not have sufficient fluid yet, then add fluid
            if Om < self._target_wt:
                self.single_tanks_optimize(optTanks)  # add fluid somewhere where it is usefull until all fluid is used.

            [Ox, Oy, _], Om = self.xyzw()

            # get the number of partial tanks

            partials = []
            for tank in optTanks:
                if tank.is_partial():
                    partials.append(tank)

            self.plot(optTanks)
            for p in partials:
                plt.plot(p.position[0], p.position[1], 'yx')

            # plt.plot(self._target_cog[0], self._target_cog[1], 'gx')
            # plt.plot(Ox, Oy, 'ro')
            # plt.show()

            if len(partials)==1:
                # find a second tank and then optimize
                tanks = optTanks.copy()
                while True:
                    tank2 = self.get_tank_to_optimize_with(tanks)
                    if self.optimize_two_tanks(partials[0], tank2):
                        break
                    else:
                        tanks.remove(tank2)
                        if len(tanks) == 0:
                            raise ValueError('Could not perform two tank optimization with this slack tank in combination with any of the other tanks')
                continue


            elif len(partials)==2:
                # if self.optimize_two_tanks(*partials):
                #     continue

                tanks = optTanks.copy()
                while True:
                    tank3 = self.get_tank_to_optimize_with(tanks)
                    if self.optimize_three_tanks(*partials, tank3):
                        break
                    else:
                        print(f'removing tank {tank3.name}')
                        tanks.remove(tank3)
                        if len(tanks) == 0:
                            raise ValueError('Could not perform three tank optimization with these two tank in combination with any of the other tanks')

        #
        #
        # # display results of pass1
        # for tank in optTanks:
        #     print(f'{tank.name}: {tank.pct}')
        #
        # # pass 2
        # #
        # # select a second tank to use for the optimization
        # # there are two options: a tank that is now full or a tank that is now empty.
        # #
        # # pick one that is currently full
        # # do the same trick with the dot-product as before, but now the tank need to be on the same side as the actual
        # # because it is going to be emptied
        #
        #
        #
        #
        # while True:
        #
        #     tank2 = self.get_tank_to_optimize_with(optTanks)
        #
        #     print(tank2)
        #
        #     if self.optimize_two_tanks(partial, tank2):
        #         print('Optimized using two tanks:')
        #         print(f'{partial.name} : {partial.pct}')
        #         print(f'{tank2.name} : {tank2.pct}')
        #     else:
        #         raise ValueError('could not use that other tank to get to a better state - strange')
        #
        #
        #     if partial.is_partial() and tank2.is_partial():
        #         break
        #     elif tank2.is_partial:
        #         partial = tank2
        #     else:
        #         # could not use that other tank to get to a better state - strange
        #         raise ValueError('could not use that other tank to get to a better state - strange')
        #
        #
        # # pass 3
        # print('pass3')
        #
        # # we have the following partial tanks:
        # # partial
        # # tank2
        #
        # partials = [partial, tank2]
        #
        # tanks_to_optimize_with = optTanks.copy()
        #
        # while True:
        #
        #     # find a third tank to include in the optimization
        #     tank3 = self.get_tank_to_optimize_with(tanks_to_optimize_with, do_plot=True)
        #     tanks_to_optimize_with.remove(tank3)
        #     plt.show()
        #
        #     optimize_with = partials
        #     optimize_with.append(tank3)
        #
        #     if self.optimize_three_tanks(*partials):
        #         print('3 tank optimum')
        #         print(f'{partial.name} : {partial.pct}')
        #         print(f'{tank2.name} : {tank2.pct}')
        #         print(f'{tank3.name} : {tank3.pct}')
        #
        #     else:
        #         print('3 tank distribution')
        #         print(f'{partial.name} : {partial.pct}')
        #         print(f'{tank2.name} : {tank2.pct}')
        #         print(f'{tank3.name} : {tank3.pct}')
        #         # raise ValueError('Could not optimize further with these three tanks')
        #
        #     if partial.is_partial() and tank2.is_partial() and tank3.is_partial():
        #         break
        #     if self._error() < self.tolerance:
        #         break
        #
        #     partials = []
        #     for tank in optTanks:
        #         if tank.is_partial():
        #             partials.append(tank)
        #
        #     if len(partials)==2:
        #         continue
        #
        #     if len(partials)==1:
        #         tank2 = self.get_tank_to_optimize_with(optTanks, do_plot=True)
        #         partials.append(tank2)
        #         self.optimize_two_tanks(*partials)
        #         # raise ValueError('Only a single slack tank left....')
        #

        #
        #
        # maxit = 100
        # for it in range(maxit):
        #
        #     print('Iteration = {}, Error = {} with tanks:'.format(it, self._error()))
        #
        #     _log.append([tank.pct for tank in optTanks])
        #     print(_log[-1])
        #
        #     if self._error() < self.tolerance:
        #         break
        #
        #     # optimize partially filled tanks
        #     partials = []
        #     for tank in optTanks:
        #         if tank.is_partial():
        #             partials.append(tank)
        #
        #     # if not self._no_single_optimization:
        #     #     if len(partials) == 1:
        #     #         if self.optimize_tank(partials[0]):
        #     #             continue
        #
        #     if not self._no_double_optimization:
        #         if len(partials) == 2:
        #             if self.optimize_multiple_partial(partials):
        #                 continue
        #
        #     if len(partials) > 2:
        #         if self.optimize_multiple_partial(partials):
        #             continue
        #
        #     changed = False
        #
        #     # See if it gets better by filling or emptying _any_ of the other tanks
        #     if not self._no_single_optimization:
        #         for tank in optTanks:
        #             if self.optimize_tank(tank):
        #                 changed = True
        #                 break
        #
        #         if changed:
        #             continue
        #
        #     # optimizing the currently partial tanks failed
        #     # keeping the currently partial tanks and optimizing any one of the other tanks failed
        #
        #     # use the current partial tanks in combination with ONE of the other tanks
        #     for tank in optTanks:
        #         if tank not in partials:
        #             temp = partials.copy()
        #             temp.append(tank)
        #             if self.optimize_multiple_partial(temp):
        #
        #                 self.print('Optimized the following:')
        #                 for tank in temp:
        #                     self.print('{} --> {}'.format(tank.name, tank.pct))
        #
        #                 changed = True
        #                 break
        #
        #     if changed:
        #         continue
        #
        #     # use the current partial tanks in combination with TWO of the other tanks
        #     #
        #     # WARNING: This is very, very slow because there are many combinations
        #
        #     # do we need to fill or drain?
        #     _, wt = self.xyzw()
        #     if wt < self._target_wt:
        #         fill = False
        #     else:
        #         fill = True
        #
        #     for tank in optTanks:
        #
        #         # exclude full tanks if we need to fill
        #         if fill and tank.is_full():
        #             continue
        #         # exclude empty tanks if we need to drain
        #         if not fill and tank.is_empty():
        #             continue
        #
        #         for tank2 in optTanks:
        #
        #             # exclude full tanks if we need to fill
        #             if fill and tank2.is_full():
        #                 continue
        #             # exclude empty tanks if we need to drain
        #             if not fill and tank2.is_empty():
        #                 continue
        #
        #             # we now have tank and tank2
        #             # optimize using all partial tanks plus these two
        #
        #             if tank not in partials:
        #                 temp = partials.copy()
        #                 temp.append(tank)
        #                 if tank2 not in temp:
        #                     temp.append(tank2)
        #                     if self.optimize_using(temp):
        #
        #                         self.print('Optimized the following:')
        #                         for tank in temp:
        #                             self.print('{} --> {}'.format(tank.name, tank.pct))
        #
        #                         changed = True
        #                         break
        #
        #     if changed:
        #         continue
        #
        #     # No workable option to get to anything better
        #
        #
        #     print("Can not find a way to get closer to the intended solution. Giving up.")
        #     print([t.pct for t in optTanks])
        #     print(self._error())
        #     print(self.xyzw())
        #
        #     break



        self.print('Error = {}'.format(self._error()))

        if self._error() < self.tolerance:
            success = True
        else:
            success = False

        self.print(self.xyzw())
        print([t.pct for t in optTanks])

        s = self.ballast_system_node._scene
        for t in self.BallastSystem._tanks:
            s[t.name].fill_pct = t.pct

        if it == maxit-1:
            plt.plot(_log)
            print('Error = {}'.format(self._error()))
            plt.show()

        return success

#
    def plot(self, optTanks):

        plt.figure()

        x = [tank.position[0] for tank in optTanks]
        y = [tank.position[1] for tank in optTanks]
        pct = [tank.pct for tank in optTanks]

        plt.plot(x,y,'k.')

        plt.scatter(x,y,pct)

    def single_tanks_optimize(self, optTanks):
        """Keep filling tanks as until all water is used and a tank is partially filled"""

        # pass1, use single tank fills to get a good estimate with only a single slack tank

        for i in range(len(optTanks)):
            for tank in optTanks:
                if self.optimize_tank(tank):
                    if tank.is_partial():
                        print('single partial tank')
                        return tank

