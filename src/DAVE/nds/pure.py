"""These are the pure-python classes for DAVE nodes"""
from pathlib import Path

from .abstracts import *
from .enums import *
from .helpers import *
from ..tools import *
from .mixins import HasParentPure
from .core import Frame


class Visual(NodePurePython, HasParentPure):
    """
    Visual

    .. image:: ./images/visual.png

    A Visual node contains a 3d visual, typically obtained from a .obj file.
    A visual node can be placed on an axis-type node.

    It is used for visualization. It does not affect the forces, dynamics or statics.

    The visual can be given an offset, rotation and scale. These are applied in the following order

    1. scale
    2. rotate
    3. offset

    """

    def __init__(self, scene, name: str):
        super().__init__(scene=scene, name=name)

        self.offset = [0, 0, 0]
        """Offset (x,y,z) of the visual. Offset is applied after scaling"""
        self.rotation = [0, 0, 0]
        """Rotation (rx,ry,rz) of the visual"""

        self.scale = [1, 1, 1]
        """Scaling of the visual. Scaling is applied before offset."""

        self._path = ""
        """Filename of the visual"""

        self.parent = None
        """Parent : Frame-type"""

        self.visual_outline = VisualOutlineType.FEATURE_AND_SILHOUETTE
        """For visualization"""

    @property
    def file_path(self) -> Path:
        """Resolved path of the visual [Path]
        #NOGUI"""
        return self._scene.get_resource_path(self._path)

    @property
    def path(self) -> str or Path:
        """Resource path or url to the visual (str)"""
        return self._path

    @path.setter
    def path(self, value):
        assert self._scene.get_resource_path(value, no_gui=True), "File not found"
        self._path = value

    def depends_on(self):
        if self.parent is None:
            return []
        else:
            return [self.parent]

    def give_python_code(self):
        code = "# code for {}".format(self.name)

        code += "\ns.new_visual(name='{}',".format(self.name)
        if self.parent is not None:
            code += "\n            parent='{}',".format(self.parent.name)
        code += "\n            path=r'{}',".format(self.path)
        code += "\n            offset=({:.6g}, {:.6g}, {:.6g}), ".format(*self.offset)
        code += "\n            rotation=({:.6g}, {:.6g}, {:.6g}), ".format(
            *self.rotation
        )
        code += "\n            scale=({:.6g}, {:.6g}, {:.6g}) )".format(*self.scale)
        if self.visual_outline != VisualOutlineType.FEATURE_AND_SILHOUETTE:
            code += f"\ns['{self.name}'].visual_outline = {self.visual_outline}"

        return code

    @node_setter_manageable
    def change_parent_to(self, new_parent):
        from .core import Frame

        if not (isinstance(new_parent, Frame) or new_parent is None):
            raise ValueError(
                "Visuals can only be attached to an axis (or derived) or None"
            )

        # get current position and orientation
        if self.parent is not None:
            cur_position = self.parent.to_glob_position(self.offset)
            cur_rotation = self.parent.to_glob_rotation(self.rotation)
        else:
            cur_position = self.offset
            cur_rotation = self.rotation

        self.parent = new_parent

        if new_parent is None:
            self.offset = cur_position
            self.rotation = cur_rotation
        else:
            self.offset = new_parent.to_loc_position(cur_position)
            self.rotation = new_parent.to_loc_rotation(cur_rotation)


#
#
class BallastSystem(NodePurePython, HasParentPure):
    """The BallastSystemNode is a non-physical node that marks a groups of Tank nodes as being the ballast system
    of a vessel.

    The BallastSystem node can interface with the ballast-solver to automatically determine a suitable ballast configuration.

    The tank objects are created separately and only their references are assigned to this ballast-system object.
    That is done using the .tanks property which is a list.
    The parent if this node is the vessel that the tanks belong to. The parent of the ballast system is expected to be
    a Frame or Rigidbody which can be ballasted (should not have a parent).

    Tanks can be excluded from the ballast algorithms by adding their names to the 'frozen' list.

    Typical use:
    - create vessel
    - create tanks
    - create ballast system
    - adds tanks to ballast system using ballast_system.tanks.append(tank node)
    - set the draft: ballast_system.target_elevation = -5.0 # note, typically negative
    - and solve the tank fills: ballast_system.solve_ballast


    """

    def __init__(self, scene, name):
        super().__init__(scene=scene, name=name)

        self.tanks = []
        """List of Tank objects"""

        self.frozen = []
        """List of names of frozen tanks - The contents of a frozen tank should not be changed"""

        self._target_elevation = None
        """Target elevation of the parent Frame (global, m)"""
        self._target_cog = None
        """Required cog of all the ballast tanks to reach the target z, calculated when setting target_elevation"""
        self._target_weight = None
        """Required total amount of water ballast to reach the target z, calculated when setting target_elevation"""

    @property
    def target_elevation(self) -> float:
        """The target elevation of the parent of the ballast system [m]"""
        return self._target_elevation

    @target_elevation.setter
    def target_elevation(self, value):
        assert1f(value, "target elevation")

        # empty all connected tanks
        fills = [tank.fill_pct for tank in self.tanks]
        for tank in self.tanks:
            tank.fill_pct = 0

        try:
            from DAVE.solvers.ballast import force_vessel_to_evenkeel_and_draft

            (F, x, y) = force_vessel_to_evenkeel_and_draft(
                self._scene, self.parent, value
            )
            self._target_elevation = value
            self._target_cog = (x, y)
            self._target_weight = -F

        finally:  # restore all connected tanks
            for tank, fill in zip(self.tanks, fills):
                tank.fill_pct = fill

    def solve_ballast(self, method=1, use_current_fill=False):
        """Attempts to find a suitable filling of the ballast tanks to position parent at even-keel and target-elevation

        Args:
            method: algorithm to use (named 1 and 2)
            use_current_fill: use current tank fill as start for the algorithm

        See Also: target_elevation"""

        if self._target_weight is None:
            raise ValueError(
                "Please set target_elevation first (eg: target_elevation = -5)"
            )

        from DAVE.solvers.ballast import BallastSystemSolver

        ballast_solver = BallastSystemSolver(self)

        assert method == 1 or method == 2, "Method shall be 1 or 2"

        if not ballast_solver.ballast_to(
            self._target_cog[0],
            self._target_cog[1],
            self._target_weight,
            start_empty=not use_current_fill,
            method=method,
        ):
            raise ValueError(
                "Could not obtain tank fillings to satisfy required condition - requesting a different draft may help"
            )

    def new_tank(
        self, name, position, capacity_kN, rho=1.025, frozen=False, actual_fill=0
    ):
        """Adds a new cubic shaped tank with the given volume as derived from capacity and rho

        Warning: provided for backwards compatibility only.
        """

        from warnings import warn

        warn(
            "BallastSystem.new_tank is outdated and may be removed in a future version."
        )

        tnk = self._scene.new_tank(name, parent=self.parent, density=rho)
        volume = capacity_kN / (9.81 * rho)
        side = volume ** (1 / 3)
        tnk.trimesh.load_file(
            "res: cube.obj",
            scale=(side, side, side),
            rotation=(0.0, 0.0, 0.0),
            offset=position,
        )
        if actual_fill > 0:
            tnk.fill_pct = actual_fill

        if frozen:
            tnk.frozen = frozen

        self.tanks.append(tnk)

        return tnk

    # for gui
    def change_parent_to(self, new_parent):
        if not (isinstance(new_parent, Frame) or new_parent is None):
            raise ValueError(
                "Visuals can only be attached to an axis (or derived) or None"
            )
        self.parent = new_parent

    # for node
    def depends_on(self):
        return [self.parent, *self.tanks]

    def is_frozen(self, name):
        """Returns True if the tank with this name if frozen"""
        return name in self.frozen

    def reorder_tanks(self, names):
        """Places tanks with given names at the top of the list. Other tanks are appended afterwards in original order.

        For a complete re-order give all tank names.

        Example:
            let tanks be 'a','b','c','d','e'

            then re_order_tanks(['e','b']) will result in ['e','b','a','c','d']
        """
        for name in names:
            if name not in self.tank_names():
                raise ValueError("No tank with name {}".format(name))

        old_tanks = self.tanks.copy()
        self.tanks.clear()
        to_be_deleted = list()

        for name in names:
            for tank in old_tanks:
                if tank.name == name:
                    self.tanks.append(tank)
                    to_be_deleted.append(tank)

        for tank in to_be_deleted:
            old_tanks.remove(tank)

        for tank in old_tanks:
            self.tanks.append(tank)

    def order_tanks_by_elevation(self):
        """Re-orders the existing tanks such that the lowest tanks are higher in the list"""

        zs = [tank.cog_when_full[2] for tank in self.tanks]
        inds = np.argsort(zs)
        self.tanks = [self.tanks[i] for i in inds]

    def order_tanks_by_distance_from_point(self, point, reverse=False):
        """Re-orders the existing tanks such that the tanks *furthest* from the point are first on the list

        Args:
            point : (x,y,z)  - reference point to determine the distance to
            reverse: (False) - order in reverse order: tanks nearest to the points first on list


        """
        pos = [tank.cog_when_full for tank in self.tanks]
        pos = np.array(pos, dtype=float)
        pos -= np.array(point)

        dist = np.apply_along_axis(np.linalg.norm, 1, pos)

        if reverse:
            inds = np.argsort(dist)
        else:
            inds = np.argsort(-dist)

        self.tanks = [self.tanks[i] for i in inds]

    def order_tanks_to_maximize_inertia_moment(self):
        """Re-order tanks such that tanks furthest from center of system are first on the list"""
        self._order_tanks_to_inertia_moment()

    def order_tanks_to_minimize_inertia_moment(self):
        """Re-order tanks such that tanks nearest to center of system are first on the list"""
        self._order_tanks_to_inertia_moment(maximize=False)

    def _order_tanks_to_inertia_moment(self, maximize=True):
        """Re-order tanks such that tanks furthest away from center of system are first on the list"""
        pos = [tank.cog_when_full for tank in self.tanks]
        m = [tank.capacity for tank in self.tanks]
        pos = np.array(pos, dtype=float)
        mxmymz = np.vstack((m, m, m)).transpose() * pos
        total = np.sum(m)
        point = sum(mxmymz) / total

        if maximize:
            self.order_tanks_by_distance_from_point(point)
        else:
            self.order_tanks_by_distance_from_point(point, reverse=True)

    def tank_names(self):
        return [tank.name for tank in self.tanks]

    def fill_tank(self, name, fill):
        assert1f(fill, "tank fill")

        for tank in self.tanks:
            if tank.name == name:
                tank.pct = fill
                return
        raise ValueError("No tank with name {}".format(name))

    def xyzw(self):
        """Gets the current ballast cog in GLOBAL axis system weight from the tanks

        Returns:
            (x,y,z), weight [mT]
        """
        """Calculates the weight and inertia properties of the tanks"""

        mxmymz = np.array((0.0, 0.0, 0.0))
        wt = 0

        for tank in self.tanks:
            w = tank.volume * tank.density
            p = np.array(tank.cog, dtype=float)
            mxmymz += p * w

            wt += w

        if wt == 0:
            xyz = np.array((0.0, 0.0, 0.0))
        else:
            xyz = mxmymz / wt

        return xyz, wt

    def empty_all_usable_tanks(self):
        """Empties all non-frozen tanks.
        Returns a list with tank number and fill percentage of all affected tanks. This can be used to restore the
        ballast situation as it was before emptying.

        See also: restore tank fillings
        """
        restore = []

        for i, t in enumerate(self.tanks):
            if not self.is_frozen(t.name):
                restore.append((i, t.fill_pct))
                t.fill_pct = 0

        return restore

    def restore_tank_fillings(self, restore):
        """Restores the tank fillings as per restore.

        Restore is typically obtained from the "empty_all_usable_tanks" function.

        See Also: empty_all_usable_tanks
        """

        for r in restore:
            i, pct = r
            self.tanks[i].fill_pct = pct

    def tank(self, name):
        for t in self.tanks:
            if t.name == name:
                return t
        raise ValueError("No tank with name {}".format(name))

    def __getitem__(self, item):
        return self.tank(item)

    @property
    def cogx(self) -> float:
        """X position of combined CoG of all tank contents in the ballast-system. (global coordinate) [m]"""
        return self.cog[0]

    @property
    def cogy(self) -> float:
        """Y position of combined CoG of all tank contents in the ballast-system. (global coordinate) [m]"""
        return self.cog[1]

    @property
    def cogz(self) -> float:
        """Z position of combined CoG of all tank contents in the ballast-system. (global coordinate) [m]"""
        return self.cog[2]

    @property
    def cog(self) -> tuple[float, float, float]:
        """Combined CoG of all tank contents in the ballast-system. (global coordinate) [m,m,m]"""
        cog, wt = self.xyzw()
        return (cog[0], cog[1], cog[2])

    @property
    def weight(self) -> float:
        """Total weight of all tank fillings in the ballast system [kN]"""
        cog, wt = self.xyzw()
        return wt * 9.81

    def give_python_code(self):
        code = "\n# code for {} and its tanks".format(self.name)

        code += "\nbs = s.new_ballastsystem('{}', parent = '{}')".format(
            self.name, self.parent.name
        )

        for tank in self.tanks:
            code += "\nbs.tanks.append(s['{}'])".format(tank.name)

        return code


class WaveInteraction1(NodePurePython, HasParentPure):
    """
    WaveInteraction

    Wave-interaction-1 couples a first-order hydrodynamic database to an axis.

    This adds:
    - wave-forces
    - damping
    - added mass

    The data is provided by a Hyddb1 object which is defined in the MaFreDo package. The contents are not embedded
    but are to be provided separately in a file. This node contains only the file-name.

    """

    def __init__(self, scene, name: str):
        super().__init__(scene=scene, name=name)

        self.offset = [0, 0, 0]
        """Position (x,y,z) of the hydrodynamic origin in its parents axis system"""

        self.path = None
        """Filename of a file that can be read by a Hyddb1 object"""

    @property
    def file_path(self) -> str:
        """Resolved path of the visual (str)
        #NOGUI"""
        return self._scene.get_resource_path(self.path)

    def depends_on(self):
        return [self.parent]

    def give_python_code(self):
        code = "# code for {}".format(self.name)

        code += "\ns.new_waveinteraction(name='{}',".format(self.name)
        code += "\n            parent='{}',".format(self.parent.name)
        code += "\n            path=r'{}',".format(self.path)
        code += "\n            offset=({}, {}, {}) )".format(*self.offset)

        return code

    @node_setter_manageable
    def change_parent_to(self, new_parent):
        if not (isinstance(new_parent, Frame)):
            raise ValueError(
                "Hydrodynamic databases can only be attached to an axis (or derived)"
            )

        # get current position and orientation
        if self.parent is not None:
            cur_position = self.parent.to_glob_position(self.offset)
        else:
            cur_position = self.offset

        self.parent = new_parent
        self.offset = new_parent.to_loc_position(cur_position)
