

"""
    This is the main module of the engine. It contains both the nodes and the scene.
    For calculations, this, together with settings.py, are the only required files.

    If this is the first time you use DAVE, please use the Gui and youtube to experiment.

    The purpose of this part of the documentation is to explain the general principles of DAVE and to provide a reference.

    #General#

    ##Axis systems##

    Axis systems are right-handed.

    In the global axis system the Z-axis points up.

    The mean sea-surface is defined as Z=0

    ##Units##

    The default unit system is m, kN, mT (metric tonne).
    G and RHO are defined accordingly.

    ##Rotations##

    Unfortunately there is no standard way of defining rotations in 3D.

    DAVE uses a [rotation vector](https://en.wikipedia.org/wiki/Axis%E2%80%93angle_representation#Rotation_vector) to represent rotations.
    This means that the rotation is defined as a vector with three components (rx,ry,rz). The magnitude of the vector is the rotation in degrees.
    The axis of rotation is the direction of the vector.

    Some examples:

    - `(0,0,90)` : A rotation of 90 degrees about the Z-axis
    - `(0,-10,0)` : A rotation of -10 degrees about the Y-axis
    - `(10,10,0)` : A rotation of sqrt(10^2 + 10^2) about the (1,1,0) axis.

    Hint: If euler angles are needed then axis systems can be stacked to obtain the same result.


    ###2D rotations###

    The following 2D rotations are available: tilt_x, tilt_y, heel, trim, heading and heading_compass. These are derived from the
    projection of one of the local axis onto the global axis system.
    For example the tilt about the x-axis is derived from the z-component of the y-axis.

    Example:
        A 3d rotation of (5,0,0) will give a heel of 5 degrees and a tilt_x of 8.7%
        A 3d rotation of (0,0,120) will give a heading of 120 degrees and a heading_compass of 330.



    ##Filesystem and configuration##

    By default DAVE will try to create a subfolder "DAVE_models" in the users HOME folder (%homepath% in windows,  ~ in linux). This folder will be used for storing temporary files, the log file, and as default save location for assets and models.

    DAVE can be configured by changing the settings in the settings.py file or by manually overriding them after importing settings.py and before importing scene.py



        import DAVE.settings
        from DAVE.scene import *
        from pathlib import Path

        # override some of the settings
        DAVE.settings.RESOURCE_PATH = [Path(r'c:\data')]
        DAVE.settings.BLENDER_EXEC = r'C:\Program Files\Blender Foundation\Blender\2.82 alpha\blender.exe'

        # now create the scene
        s = Scene()

        print(s.resources_paths)

    All settings are defined in UPPERCASE.

    Note: Changing G or RHO has no effect at this moment as these values would also need to be changed in the equilibrium-core

    ###/ or \\ ###

    DAVE is multiplatform. It runs fine under windows as well as linux.
    Windows uses a \\ in path definitions while linux uses as /.
    The python standard [pathlib](https://docs.python.org/3/library/pathlib.html) library is used to deal with paths. In most situations however a string will work fine as well.


    ##File format##

    The standard file-format for saving DAVE scenes and nodes is [vanilla](https://en.wikipedia.org/wiki/Vanilla_software) python.

    When loading a model or asset from a file into a scene the contents of that file are executed in the python interpreter. In the interpreter a variable `s` is
    available which refers to the current scene.

    This makes it possible to define DAVE models in a very flexible way as arbitrary code can be executed when importing the model. Importing a model into DAVE is basically the same as running a file, so beware of the involed security implications.


    # Scene and nodes #
    A node is an item or element in a model. For example a ship or a force.
    A Scene is a collection of nodes.

    The common way of working is as follows:

    1. Create a scene
    2. Add nodes to it

    Nodes are added to the scene using .new_nodetype() where nodetype is the type of the node. Each node has a unique name. This is always needs to be provided to the .new_node function.
    A complete list of node types and corresponding functions is provided later.

    Example

        s = Scene()                               # create an empty scene
        s.new_poi('point 1')                      # creates a poi with name anchor
        s.new_poi('point 2', position = (10,0,0)) # create a second poi at x=10
        s.new_cable('line',poiA = 'point 1', poiB = 'point 2')
              # creates a cable between the two points
        s.save_scene(r'test.dave')              # save to file


    Nodes in a scene can be referenced by either name or by reference.
    The .new_nodetype() functions return a reference to the newly created node.

        s = Scene()
        a = s.new_axis('axis')
            # a is now a reference to node 'axis'

        p1 = s.new_poi('poi_1', parent = a )       # refer by reference
        p2 = s.new_poi('poi_2', parent = 'axis' )  # refer by name

    A reference to a node can also be obtained from the scene using square brackets:

        s = Scene()
        s.new_axis('axis')

        a = s['axis']
        print(a.position)


    #Nodes#

    The following node types can be used:

    ##Geometry##

    The geometry of a scene is setup using `Axis`, `Poi` and `Sheave` nodes.

    |  Type | Provides  | Create using |
    |:---------------- |:------------------------------- |:-----|
    | `DAVE.scene.Axis` | Axis system with position and orientation  |  `DAVE.scene.Scene.new_axis` |
    | `DAVE.scene.Poi` | A position  |  `DAVE.scene.Scene.new_poi` |
    | `DAVE.scene.Sheave` | A disk with a radius and axis direction  |  `DAVE.scene.Scene.new_sheave` |
    | `RigidBody` | Same as axis system, but provides a weight as well  |  `DAVE.scene.Scene.new_rigidbody` |

    A RigidBody is technically idential to an axis system. So everything that applies to Axis also applies to RigidBody
    and everywhere where an axis system is used a rigidbody can be used as well.

    - Axis can be placed on other axis systems.
    - Pois can be located on an axis system.
    - Sheaves need to be placed on a poi.

    If a node has a parent then this means that its position and orientation are expressed relative to that parent.
    For nodes without a parent everything is defined relative to the global axis system.


    ###Forces###

    Geometry nodes are also used to transfer forces.

    Axis and Poi type nodes can receive forces and moments and apply them to their parents. See `Poi.applied_force_and_moment_global`,
    `Axis.applied_force` and `Axis.connection_force`.
    Cables running over sheave type nodes will apply the forces directly to the parent node of the sheave.

    ###Degrees of freedom###

    Axis and RigidBodies can have all their six individual degrees of freedom either fixed or free. If a degree of freedom is free then this means that the
    node is able to move/rotate in this degree of freedom.



    ##Connectors##

    Connectors connect two or more nodes and can apply a force on them based on their positions and orientations.

    |  Type | Provides  | Create using |
    |:---------------- |:------------------------------- |:-----|
    | `Cable` | A finite length cable with linear stiffness. A cable runs between two Poi nodes and can run over multiple pois or sheaves. A cable may have a diameter.   |  `Scene.new_cable` |
    | `LinearBeam` | A beam connects two axis systems with a linear beam element   |  `Scene.new_linear_beam` |
    | `LC6d` | Connects two axis systems with six linear springs. Orientation of the springs is determined by the master axis system   |  `Scene.new_linear_connector_6d` |
    | `Connector2d` | Connects two axis systems with two linear springs. Orientation of the springs is determined by shortest distance between the two axis systems |  `Scene.new_connector2d` |


    ##Forces##

    Forces apply a force to a node. The magnitude of the force may depend on the position and/or orientation of the node.

    |  Type | Provides  | Create using |
    |:---------------- |:------------------------------- |:-----|
    | `Force` | An fixed force and/or moment applied on a Poi |  `Scene.new_force` |
    | `HydSpring` | A linear hydrostatic spring attached to an Axis  |  `Scene.new_hydspring` |
    | `Buoyancy` | A buoyancy mesh attached to an Axis  |  `Scene.new_buoyancy` |

    ##Visuals##

    (Almost) Everything gets better when visualized :-).

    |  Type | Provides  | Create using |
    |:---------------- |:------------------------------- |:-----|
    | `Visual` | Obj type 3D visuals can be attached to an Axis |  `Scene.new_visual` |

    ##Inertia##

    Inertia is included via PointMass nodes. There is no direct API interface for these elements. They are included under
    the hood in the Axis nodes (and this in the derived RigidBody node).
    Also the ballast-system node type employs them to add the inertia of the ballast tanks.


    ##Others###

    `TriMeshSource` is a node that defines a triangular mesh. It is not created directly but is created implicitly when
    creating a buoyuany node. It may be accessed via `Buoyancy.trimesh`. Multiple buoyancy nodes may share the same TriMeshSource.




    #Scene#
    
    Apart from methods to create nodes, Scene also harbours functionality to delete, import, re-order and export nodes.

    ##Creating scenes##

    A Scene is not a singleton. Multiple scenes can exist next to eachother.

    A new and empty Scene can be created as follows:

        s = Scene()

     where `s` can be anything, for example `my_scene` but s is nice and short which is usefull as it will be used a lot.

     Optionally a filename can be provided to the constructor. In that case that file will be imported.

        my_vessel = Scene('path/to/my_vessel.dave_asset')

    It is also possible to create a (deep) copy of a scene. This is done as follows:

        copy_of_scene = Scene(copy_from = other_scene)


    ##Adding content##

    Nodes can be added to the scene using the s.new_poi, s.new_axis, etc.. functions which were introduced in the previous section.


    Multiple nodes can be imported from file or directly from another Scene object using `Scene.load_scene()` or `Scene.import_scene()` respectively.

    Note: Beware of name-conflicts when importing. The `Scene.import_scene` provides the option to add a prefix to names of imported nodes.


    ##Access nodes##

    A list of nodes is maintained as the ._nodes property of a scene. It is advised not to use this directly.

    Obtaining a reference to a single node can be done using its name:

        node = s['node_name']

    This is the reason why all node names should be unique. To get a list of all available node names use `Scene.print_node_tree()`

    It is also possible to:

    - Get all nodes of a type, use : `Scene.nodes_of_type()`
    - Get all nodes that depend on a node : `Scene.nodes_depending_on()`
    - Get all child nodes : `Scene.nodes_with_parent()`

    ##Deleting nodes##

    Removing nodes can be tricky due to nodes depending on eachother. For example deleting a poi which is also used a endpoint for a cable will cause problems for that cable.
    The same applies to axis systems with nodes on it (children)

    `Scene.clear` can be used to delete all nodes from a scene.

    To delete a single node there are two options:

    1. `Scene.delete`. This deletes a node from the scene. All nodes that depend on this node will be deleted as well.
    2. `Scene.dissolve`. This "evaporates" the node. Attempts to maintain child nodes. Often used in combination with the containerize option of `Scene.import_scene`

    ##Saving or exporting##

    The standard file-format for saving DAVE scenes and nodes is [vanilla](https://en.wikipedia.org/wiki/Vanilla_software) python.

    The contents of a Scene can be save using `Scene.save_scene`. The python code to re-create the scene can be obtained using `Scene.give_python_code`.

    ##Solving##

    Solving static equilibrium is done using `Scene.solve_statics`. If there is a static equilibrium condition then this function will attempt to find it by changing the non-fixed degrees of freedom of the scene.

    ##Optimalizations##

    A goal-seek function is available: `Scene.goal_seek`.

    ##Resources##

    In the default resource system the resources may be located in any of the folders listed in `Scene.resources_paths`.
    The value of this property is initialized with `DAVE.settings.RESOURCE_PATH`.

    `Scene.get_resource_list` can be used to obtain a list of all available resources. `Scene.get_resource_path` can
    be used to obtain a full path to a resource with a known name.


"""

"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Ruben de Bruin - 2019
"""

import pyo3d
import numpy as np
import DAVE.settings as vfc
from DAVE.tools import *
from os.path import isfile, split, dirname, exists
from os import listdir
from pathlib import Path
import datetime


# we are wrapping all methods of pyo3d such that:
# - code-completion is more robust
# - we can do some additional checks. pyo3d is written for speed, not robustness.
# - pyo3d is not a hard dependency
#
# notes and choices:
# - properties are returned as tuple to make sure they are not editable.
#    --> node.position[2] = 5 is not allowed



class Node:
    """ABSTRACT CLASS - Properties defined here are applicable to all derived classes
    Master class for all nodes"""

    def __init__(self, scene):
        self._scene = scene
        self._name = 'no name'

    def give_python_code(self):
        """Returns the python code that can be executed to re-create this node"""
        return "# No python code generated for element {}".format(self.name)

    @property
    def name(self):
        """Name of the node (str), must be unique"""
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    def _delete_vfc(self):
        pass

    def update(self):
        """Performs internal updates relevant for physics. Called before solving statics or getting results"""
        pass

class CoreConnectedNode(Node):
    """ABSTRACT CLASS - Properties defined here are applicable to all derived classes
    Master class for all nodes with a connected eqCore element"""

    def __init__(self, scene, vfNode):
        super().__init__(scene)
        self._vfNode = vfNode

    @property
    def name(self):
        """Name of the node (str), must be unique"""
        return self._vfNode.name

    @name.setter
    def name(self, name):
        if not name == self._vfNode.name:
            self._scene._verify_name_available(name)
            self._vfNode.name = name

    def _delete_vfc(self):
        self._scene._vfc.delete(self._vfNode.name)

class NodeWithParent(CoreConnectedNode):
    """
    NodeWithParent

    Do not use this class directly.
    This is a base-class for all nodes that have a "parent" property.
    """

    def __init__(self, scene, vfNode):
        super().__init__(scene, vfNode)
        self._parent = None
        self._None_parent_acceptable = False

    @property
    def parent(self):
        """Determines the parent of the node. Should be another axis or None"""
        if self._vfNode.parent is None:
            return None
        else:
            return self._parent
            # return Axis(self._scene, self._vfNode.parent)

    @parent.setter
    def parent(self, var):
        """Assigns a new parent. Keeps the local position and rotations the same

        See also: change_parent_to
        """

        if var is None:

            if not self._None_parent_acceptable:
                raise ValueError('None is not an acceptable parent for {} of {}'.format(self.name, type(self)))

            self._parent = None
            self._vfNode.parent = None
        else:
            if isinstance(var, Axis):
                self._parent = var
                self._vfNode.parent = var._vfNode
            elif isinstance(var, Poi):
                self._parent = var
                self._vfNode.parent = var._vfNode
            else:
                raise Exception('Parent can only be set to an instance of Axis or Poi, not to a {}'.format(type(var)))

    def change_parent_to(self, new_parent):
        """Assigns a new parent to the node but keeps the global position and rotation the same.

        See also: .parent (property)

        Args:
            new_parent: new parent node

        """

        try:
            self.rotation
            has_rotation = True
        except:
            has_rotation = False

        try:
            self.position
            has_position = True
        except:
            has_position = False

        # it is possible that this function is called on an object without position/rotation
        # in that case just fall-back to a change of parent
        if not has_position and not has_rotation:
            self.parent = new_parent
            return

        # check new_parent
        if new_parent is not None:

            if not isinstance(new_parent, Axis):
                if not has_rotation:
                    if not isinstance(new_parent, Poi):
                        raise TypeError(
                            'Only Poi-type nodes (or derived types) can be used as parent. You tried to use a {} as parent'.format(
                                type(new_parent)))
                else:
                    raise TypeError(
                        'Only None or Axis-type nodes (or derived types)  can be used as parent. You tried to use a {} as parent'.format(
                            type(new_parent)))

        glob_pos = self.global_position

        if has_rotation:
            glob_rot = self.global_rotation

        self.parent = new_parent

        if new_parent is None:
            self.position = glob_pos
            if has_rotation:
                self.rotation = glob_rot

        else:
            self.position = new_parent.to_loc_position(glob_pos)
            if has_rotation:
                self.rotation = new_parent.to_loc_direction(glob_rot)

class Visual(Node):
    """
    Visual

    .. image:: ./images/visual.png

    A Visual node contains a 3d visual, typically obtained from a .obj file.
    A visual node can be placed on an axis-type node.

    It is used for visualization. It does not affect the forces, dynamics or statics.

    The visual can be given an offset, rotation and scale. These are applied in the following order

    1. rotate
    2. scale
    3. offset

    Hint: To scale before rotation place the visual on a dedicated axis and rotate that axis.

    """

    def __init__(self, scene):

        super().__init__(scene)

        # Note: Visual does not have a corresponding vfCore element
        self.scene = scene

        self.offset = [0, 0, 0]
        """Offset (x,y,z) of the visual. Offset is applied after scaling"""
        self.rotation = [0, 0, 0]
        """Rotation (rx,ry,rz) of the visual"""

        self.scale = [1,1,1]
        """Scaling of the visual. Scaling is applied before offset."""

        self.path = ''
        """Filename of the visual"""

        self.parent = None
        """Parent : Axis-type"""

    def give_python_code(self):
        code = "# code for {}".format(self.name)


        code += "\ns.new_visual(name='{}',".format(self.name)
        code += "\n            parent='{}',".format(self.parent.name)
        code += "\n            path=r'{}',".format(self.path)
        code += "\n            offset=({}, {}, {}), ".format(*self.offset)
        code += "\n            rotation=({}, {}, {}), ".format(*self.rotation)
        code += "\n            scale=({}, {}, {}) )".format(*self.scale)

        return code

    def change_parent_to(self, new_parent):
        if not (isinstance(new_parent, Axis) or new_parent is None):
            raise ValueError('Visuals can only be attached to an axis (or derived) or None')

        # get current position and orientation
        if self.parent is not None:
            cur_position = self.parent.to_glob_position(self.offset)
            cur_rotation = self.parent.to_glob_direction(self.rotation)
        else:
            cur_position = self.offset
            cur_rotation = self.rotation

        self.parent = new_parent

        if new_parent is None:
            self.offset = cur_position
            self.rotation = cur_rotation
        else:
            self.offset = new_parent.to_loc_position(cur_position)
            self.rotation = new_parent.to_loc_direction(cur_rotation)

class Axis(NodeWithParent):
    """
    Axis

    Axes are the main building blocks of the geometry. They have a position and an rotation in space. Other nodes can be placed on them.
    Axes can be nested by parent/child relationships meaning that an axis can be placed on an other axis.
    The possible movements of an axis can be controlled in each degree of freedom using the "fixed" property.

    Axes are also the main building block of inertia.
    Dynamics are controlled using the inertia properties of an axis: inertia [mT], inertia_position[m,m,m] and inertia_radii [m,m,m]


    Notes:
         - circular references are not allowed: It is not allowed to place a on b and b on a

    """

    def __init__(self, scene, vfAxis):
        super().__init__(scene, vfAxis)
        self._None_parent_acceptable = True

        self._inertia = 0
        self._inertia_position = (0,0,0)
        self._inertia_radii = (0,0,0)

        self._pointmasses = list()
        for i in range(6):
            p = scene._vfc.new_pointmass(self.name + vfc.VF_NAME_SPLIT + 'pointmass_{}'.format(i))
            p.parent = vfAxis
            self._pointmasses.append(p)
        self._update_inertia()


    def _delete_vfc(self):
        for p in self._pointmasses:
            self._scene._vfc.delete(p.name)

        super()._delete_vfc()

    @property
    def inertia(self):
        return self._inertia

    @inertia.setter
    def inertia(self,val):
        assert1f(val,"Inertia")
        self._inertia = val
        self._update_inertia()

    @property
    def inertia_position(self):
        return np.array(self._inertia_position,dtype=float)

    @inertia_position.setter
    def inertia_position(self, val):
        assert3f(val, "Inertia position")
        self._inertia_position = tuple(val)
        self._update_inertia()

    @property
    def inertia_radii(self):
        return np.array(self._inertia_radii, dtype=float)

    @inertia_radii.setter
    def inertia_radii(self, val):
        assert3f_positive(val, "Inertia radii of gyration")
        self._inertia_radii = val
        self._update_inertia()


    def _update_inertia(self):
        # update mass
        for i in range(6):
            self._pointmasses[i].inertia = self._inertia / 6

        if self._inertia <= 0:
            return

        # update radii and position
        pos = radii_to_positions(*self._inertia_radii)
        for i in range(6):
            p = (pos[i][0] + self._inertia_position[0],
                 pos[i][1] + self._inertia_position[1],
                 pos[i][2] + self._inertia_position[2])
            self._pointmasses[i].position = p
            # print('{} at {} {} {}'.format(self._inertia/6, *p))



    @property
    def fixed(self):
        """Determines which of the six degrees of freedom are fixed, if any. (x,y,z,rx,ry,rz).
        True means that that degree of freedom will not change when solving statics.
        False means a that is may be changed in order to find equilibrium.

        These are the expressed on the coordinate system of the parent (if any) or the global axis system (if no parent)

        See Also: set_free, set_fixed
        """
        return self._vfNode.fixed

    @fixed.setter
    def fixed(self, var):
        if var == True:
            var = (True,True,True,True,True,True)
        if var == False:
            var = (False, False, False, False, False, False)

        self._vfNode.fixed = var

    def set_free(self):
        """Sets .fixed to (False,False,False,False,False,False)"""
        self._vfNode.set_free()

    def set_fixed(self):
        """Sets .fixed to (True,True,True,True,True,True)"""
        self._vfNode.set_fixed()

    @property
    def x(self):
        """The x-component of the position vector"""
        return self.position[0]

    @property
    def y(self):
        """The y-component of the position vector"""
        return self.position[1]

    @property
    def z(self):
        """The y-component of the position vector"""
        return self.position[2]

    @x.setter
    def x(self, var):
        a = self.position
        self.position = (var, a[1], a[2])

    @y.setter
    def y(self, var):
        a = self.position
        self.position = (a[0], var , a[2])

    @z.setter
    def z(self, var):
        a = self.position
        self.position = (a[0], a[1], var)



    @property
    def position(self):
        """Position of the axis (x,y,z)
        These are the expressed on the coordinate system of the parent (if any) or the global axis system (if no parent)"""
        return self._vfNode.position

    @position.setter
    def position(self, var):
        assert3f(var, "Position ")
        self._vfNode.position = var
        self._scene._geometry_changed()

    @property
    def rx(self):
        """The x-component of the rotation vector"""
        return self.rotation[0]

    @property
    def ry(self):
        """The y-component of the rotation vector"""
        return self.rotation[1]

    @property
    def rz(self):
        """The z-component of the rotation vector"""
        return self.rotation[2]

    @rx.setter
    def rx(self, var):
        a = self.rotation
        self.rotation = (var, a[1], a[2])

    @ry.setter
    def ry(self, var):
        a = self.rotation
        self.rotation = (a[0], var , a[2])

    @rz.setter
    def rz(self, var):
        a = self.rotation
        self.rotation = (a[0], a[1], var)

    @property
    def rotation(self):
        """Rotation of the axis about its origin (rx,ry,rz).
        Defined as a rotation about an axis where the direction of the axis is (rx,ry,rz) and the angle of rotation is |(rx,ry,rz| degrees.
        These are the expressed on the coordinate system of the parent (if any) or the global axis system (if no parent)"""
        return np.rad2deg(self._vfNode.rotation)

    @rotation.setter
    def rotation(self, var):
        # convert to degrees
        assert3f(var, "Rotation ")
        self._vfNode.rotation = np.deg2rad(var)
        self._scene._geometry_changed()

    # we need to over-ride the parent property to be able to call _geometry_changed afterwards
    @property
    def parent(self):
        """Determines the parent of the axis. Should either be another axis or 'None'"""
        return super().parent

    @parent.setter
    def parent(self, val):
        NodeWithParent.parent.fset(self, val)
        self._scene._geometry_changed()

    @property
    def gx(self):
        """The x-component of the global position vector"""
        return self.global_position[0]

    @property
    def gy(self):
        """The y-component of the global position vector"""
        return self.global_position[1]

    @property
    def gz(self):
        """The z-component of the global position vector"""
        return self.global_position[2]

    @gx.setter
    def gx(self, var):
        a = self.global_position
        self.global_position = (var, a[1], a[2])

    @gy.setter
    def gy(self, var):
        a = self.global_position
        self.global_position = (a[0], var, a[2])

    @gz.setter
    def gz(self, var):
        a = self.global_position
        self.global_position = (a[0], a[1], var)

    @property
    def global_position(self):
        """The global position of the origin."""
        return self._vfNode.global_position

    @global_position.setter
    def global_position(self, val):
        assert3f(val, "Global Position")
        if self.parent:
            self.position = self.parent.to_loc_position(val)
        else:
            self.position = val

    @property
    def grx(self):
        """The x-component of the global rotation vector"""
        return self.global_rotation[0]

    @property
    def gry(self):
        """The y-component of the global rotation vector"""
        return self.global_rotation[1]

    @property
    def grz(self):
        """The z-component of the global rotation vector"""
        return self.global_rotation[2]

    @grx.setter
    def grx(self, var):
        a = self.global_rotation
        self.global_rotation = (var, a[1], a[2])

    @gry.setter
    def gry(self, var):
        a = self.global_rotation
        self.global_rotation = (a[0], var, a[2])

    @grz.setter
    def grz(self, var):
        a = self.global_rotation
        self.global_rotation = (a[0], a[1], var)

    @property
    def tilt_x(self):
        """Returns the trim in [%]. This is the z-component of the unit y vector.

        See Also: heel
        """
        y = (0,1,0)
        uy = self.to_glob_direction(y)
        return 100*uy[2]

    @property
    def heel(self):
        """Returns the heel in [deg].  SB down is positive.
        This is the inverse sin of the unit y vector(This is the arcsin of the tiltx)

        See also: tilt_x
        """
        return np.rad2deg(np.arcsin(self.tilt_x/100))

    @property
    def tilt_y(self):
        """Returns the trim in [%]. This is the z-component of the unit -x vector. So a positive rotation about
        the y axis result in a positive tilt_y.

        See Also: heel
        """
        x = (-1, 0, 0)
        ux = self.to_glob_direction(x)
        return 100 * ux[2]

    @property
    def trim(self):
        """Returns the trim in [deg]. Bow-down is positive.

        This is the inverse sin of the unit -x vector(This is the arcsin of the tilt_y)

        See also: tilt_y
        """
        return np.rad2deg(np.arcsin(self.tilt_y / 100))

    @property
    def heading(self):
        """Returns the direction (0..360) [deg] of the local x-axis relative to the global x axis. Measured about the global z axis

        heading = atan(u_y,u_x)

        typically:
            heading 0  --> local axis align with global axis
            heading 90 --> local x-axis in direction of global y axis


        See also: heading_compass
        """
        x = (1, 0, 0)
        ux = self.to_glob_direction(x)
        heading = np.rad2deg(np.arctan2(ux[1],ux[0]))
        return np.mod(heading,360)

    @property
    def heading_compass(self):
        """The heading (0..360)[deg] assuming that the global y-axis is North and global x-axis is East and rotation accoring compass definition"""
        return np.mod(90-self.heading,360)

    @property
    def global_rotation(self):
        """The rotation of the axis in degrees. Expressed in the global axis system"""
        return tuple(np.rad2deg(self._vfNode.global_rotation))

    @global_rotation.setter
    def global_rotation(self, val):
        assert3f(val, "Global Rotation")
        if self.parent:
            self.rotation = self.parent.to_loc_rotation(val)
        else:
            self.rotation = val

    @property
    def global_transform(self):
        """Read-only: The global tranform of the axis system."""
        return self._vfNode.global_transform

    @property
    def connection_force(self):
        """Returns the force and moment that this axis applies on its parent [Parent axis system]"""
        return self._vfNode.connection_force

    @property
    def connection_force_x(self):
        """The x-component of the connection-force vector"""
        return self.connection_force[0]

    @property
    def connection_force_y(self):
        """The y-component of the connection-force vector"""
        return self.connection_force[1]

    @property
    def connection_force_z(self):
        """The z-component of the connection-force vector"""
        return self.connection_force[2]

    @property
    def connection_moment_x(self):
        """The mx-component of the connection-force vector"""
        return self.connection_force[3]

    @property
    def connection_moment_y(self):
        """The my-component of the connection-force vector"""
        return self.connection_force[4]

    @property
    def connection_moment_z(self):
        """The mx-component of the connection-force vector"""
        return self.connection_force[5]

    @property
    def applied_force(self):
        """Returns the force and moment that is applied on this axis [Global axis system]
        """
        return self._vfNode.applied_force

    @property
    def ux(self):
        """The unit x axis in global coordinates"""
        return self.to_glob_direction((1,0,0))

    @property
    def uy(self):
        """The unit y axis in global coordinates"""
        return self.to_glob_direction((0, 1, 0))

    @property
    def uz(self):
        """The unit z axis in global coordinates"""
        return self.to_glob_direction((0, 0, 1))

    @property
    def equilibrium_error(self):
        """Returns the force and moment that remains on this axis (applied-force minus connection force) [Parent axis system]
        """
        return self._vfNode.equilibrium_error

    def to_loc_position(self, value):
        """Returns the local position of a point in the global axis system.
        This considers the position and the rotation of the axis system.
        See Also: to_loc_direction
        """
        return self._vfNode.global_to_local_point(value)

    def to_glob_position(self, value):
        """Returns the global position of a point in the local axis system.
        This considers the position and the rotation of the axis system.
        See Also: to_glob_direction
        """
        return self._vfNode.local_to_global_point(value)

    def to_loc_direction(self, value):
        """Returns the local direction of a point in the global axis system.
        This considers only the rotation of the axis system.
        See Also: to_loc_position
        """
        return self._vfNode.global_to_local_vector(value)

    def to_glob_direction(self, value):
        """Returns the global direction of a point in the local axis system.
        This considers only the rotation of the axis system.
        See Also: to_glob_position"""
        return self._vfNode.local_to_global_vector(value)

    def to_loc_rotation(self, value):
        """Returns the local rotation. Used for rotating rotations.
            See Also: to_loc_position, to_loc_direction
             """
        return np.rad2deg(self._vfNode.global_to_local_rotation(np.deg2rad(value)))

    def to_glob_rotation(self, value):
        """Returns the global rotation. Used for rotating rotations.
            See Also: to_loc_position, to_loc_direction
             """
        return np.rad2deg(self._vfNode.local_to_global_rotation(np.deg2rad(value)))

    def change_parent_to(self, new_parent):
        """Assigns a new parent to the node but keeps the global position and rotation the same.

        See also: .parent (property)

        Args:
            new_parent: new parent node

        """

        # check new_parent
        if new_parent is not None:
            if not isinstance(new_parent, Axis):
                raise TypeError(
                    'Only None or Axis-type nodes (or derived types) can be used as parent. You tried to use a {} as parent'.format(
                    type(new_parent)))

        glob_pos = self.global_position
        glob_rot = self.global_rotation
        self.parent = new_parent
        self.global_position = glob_pos
        self.global_rotation = glob_rot



    def give_python_code(self):
        code = "# code for {}".format(self.name)
        code += "\ns.new_axis(name='{}',".format(self.name)
        if self.parent:
            code += "\n           parent='{}',".format(self.parent.name)

        # position

        if self.fixed[0]:
            code += "\n           position=({},".format(self.position[0])
        else:
            code += "\n           position=(solved({}),".format(self.position[0])
        if self.fixed[1]:
            code += "\n                     {},".format(self.position[1])
        else:
            code += "\n                     solved({}),".format(self.position[1])
        if self.fixed[2]:
            code += "\n                     {}),".format(self.position[2])
        else:
            code += "\n                     solved({})),".format(self.position[2])

        # rotation

        if self.fixed[3]:
            code += "\n           rotation=({},".format(self.rotation[0])
        else:
            code += "\n           rotation=(solved({}),".format(self.rotation[0])
        if self.fixed[4]:
            code += "\n                     {},".format(self.rotation[1])
        else:
            code += "\n                     solved({}),".format(self.rotation[1])
        if self.fixed[5]:
            code += "\n                     {}),".format(self.rotation[2])
        else:
            code += "\n                     solved({})),".format(self.rotation[2])

        # inertia and radii of gyration
        if self.inertia > 0:
            code += "\n                     inertia = {},".format(self.inertia)

        if np.any(self.inertia_radii > 0):
            code += "\n                     inertia_radii = ({}, {}, {}),".format(*self.inertia_radii)

        # fixeties
        code += "\n           fixed =({}, {}, {}, {}, {}, {}) )".format(*self.fixed)

        return code

class Poi(NodeWithParent):
    """A location on an axis"""

    # init parent and name are fully derived from NodeWithParent
    # _vfNode is a poi
    def __init__(self, scene, vfPoi):
        super().__init__(scene, vfPoi)
        self._None_parent_acceptable = True


    @property
    def x(self):
        """x component of local position"""
        return self.position[0]

    @property
    def y(self):
        """y component of local position"""
        return self.position[1]

    @property
    def z(self):
        return self.position[2]

    @x.setter
    def x(self, var):
        a = self.position
        self.position = (var, a[1], a[2])

    @y.setter
    def y(self, var):
        a = self.position
        self.position = (a[0], var, a[2])

    @z.setter
    def z(self, var):
        """z component of local position"""
        a = self.position
        self.position = (a[0], a[1], var)


    @property
    def position(self):
        """Local position"""
        return self._vfNode.position

    @position.setter
    def position(self, new_position):
        assert3f(new_position)
        self._vfNode.position = new_position

    @property
    def applied_force_and_moment_global(self):
        """Returns the applied force in the parent axis system"""
        return self._vfNode.applied_force

    @property
    def gx(self):
        """x component of global position"""
        return self.global_position[0]

    @property
    def gy(self):
        """y component of global position"""
        return self.global_position[1]

    @property
    def gz(self):
        """z component of global position"""
        return self.global_position[2]

    @gx.setter
    def gx(self, var):
        a = self.global_position
        self.global_position = (var, a[1], a[2])

    @gy.setter
    def gy(self, var):
        a = self.global_position
        self.global_position = (a[0], var, a[2])

    @gz.setter
    def gz(self, var):
        a = self.global_position
        self.global_position = (a[0], a[1], var)

    @property
    def global_position(self):
        """Global position"""
        return self._vfNode.global_position

    @global_position.setter
    def global_position(self, val):
        assert3f(val, "Global Position")
        if self.parent:
            self.position = self.parent.to_loc_position(val)
        else:
            self.position = val

    def give_python_code(self):
        code = "# code for {}".format(self.name)
        code += "\ns.new_poi(name='{}',".format(self.name)
        if self.parent:
            code += "\n          parent='{}',".format(self.parent.name)

        # position

        code += "\n          position=({},".format(self.position[0])
        code += "\n                    {},".format(self.position[1])
        code += "\n                    {}))".format(self.position[2])

        return code

class RigidBody(Axis):
    """A Rigid body, internally composed of an axis, a poi (cog) and a force (gravity)"""

    def __init__(self, scene, axis, poi, force):
        super().__init__(scene, axis)

        # The axis is the Node
        # poi and force are added separately

        self._vfPoi = poi
        self._vfForce = force

    # override the following properties
    # - name : sets the names of poi and force as well

    def _delete_vfc(self):
        super()._delete_vfc()
        self._scene._vfc.delete(self._vfPoi.name)
        self._scene._vfc.delete(self._vfForce.name)

    @property  # can not define a setter without a getter..?
    def name(self):
        return super().name

    @name.setter
    def name(self, newname):
        # super().name = newname
        super(RigidBody, self.__class__).name.fset(self, newname)
        self._vfPoi.name = newname + vfc.VF_NAME_SPLIT + "cog"
        self._vfForce.name = newname + vfc.VF_NAME_SPLIT + "gravity"

    @property
    def cogx(self):
        return self.cog[0]

    @property
    def cogy(self):
        return self.cog[1]

    @property
    def cogz(self):
        return self.cog[2]

    @property
    def cog(self):
        """Control the cog position of the body"""
        return self._vfPoi.position

    @cogx.setter
    def cogx(self, var):
        a = self.cog
        self.cog = (var, a[1], a[2])

    @cogy.setter
    def cogy(self, var):
        a = self.cog
        self.cog = (a[0], var, a[2])

    @cogz.setter
    def cogz(self, var):
        a = self.cog
        self.cog = (a[0], a[1], var)

    @cog.setter
    def cog(self, newcog):
        assert3f(newcog)
        self._vfPoi.position = newcog
        self.inertia_position = self.cog


    @property
    def mass(self):
        """Control the static mass of the body"""
        return self._vfForce.force[2] / -vfc.G

    @mass.setter
    def mass(self, newmass):
        assert1f(newmass)
        self.inertia = newmass
        self._vfForce.force = (0, 0, -vfc.G * newmass)

    def give_python_code(self):
        code = "# code for {}".format(self.name)
        code += "\ns.new_rigidbody(name='{}',".format(self.name)
        code += "\n                mass={},".format(self.mass)
        code += "\n                cog=({},".format(self.cog[0])
        code += "\n                     {},".format(self.cog[1])
        code += "\n                     {}),".format(self.cog[2])

        if self.parent:
            code += "\n                parent='{}',".format(self.parent.name)

        # position

        if self.fixed[0]:
            code += "\n                position=({},".format(self.position[0])
        else:
            code += "\n                position=(solved({}),".format(self.position[0])
        if self.fixed[1]:
            code += "\n                          {},".format(self.position[1])
        else:
            code += "\n                          solved({}),".format(self.position[1])
        if self.fixed[2]:
            code += "\n                          {}),".format(self.position[2])
        else:
            code += "\n                          solved({})),".format(self.position[2])

        # rotation

        if self.fixed[3]:
            code += "\n                rotation=({},".format(self.rotation[0])
        else:
            code += "\n                rotation=(solved({}),".format(self.rotation[0])
        if self.fixed[4]:
            code += "\n                          {},".format(self.rotation[1])
        else:
            code += "\n                          solved({}),".format(self.rotation[1])
        if self.fixed[5]:
            code += "\n                          {}),".format(self.rotation[2])
        else:
            code += "\n                          solved({})),".format(self.rotation[2])

        if np.any(self.inertia_radii > 0):
            code += "\n                     inertia_radii = ({}, {}, {}),".format(*self.inertia_radii)

        code += "\n                fixed =({}, {}, {}, {}, {}, {}) )".format(*self.fixed)

        return code

class Cable(CoreConnectedNode):
    """A Cable represents a linear elastic wire running from a Poi to another Poi.

    A cable has a un-stretched length [length] and a stiffness [EA] and may have a diameter [m]. The tension in the cable is calculated.

    Intermediate pois or sheaves may be added.

    - Pois are considered as sheaves with a zero diameter.
    - Sheaves are considered sheaves with the given geometry. If defined then the diameter of the cable is considered when calculating the geometry. The cable runs over the sheave in the positive direction (right hand rule) as defined by the axis of the sheave.

    For cables running over a sheave the friction in sideways direction is considered to be infinite. The geometry is calculated such that the
    cable section between sheaves is perpendicular to the vector from the axis of the sheave to the point where the cable leaves the sheave.

    This assumption results in undefined behaviour when the axis of the sheave is parallel to the cable direction.

    Notes:
        If pois or sheaves on a cable come too close together (<1mm) then they will be pushed away from eachother.
        This prevents the unwanted situation where multiple pois end up at the same location. In that case it can not be determined which amount of force should be applied to each of the pois.


    """

    def __init__(self, scene, node):
        super().__init__(scene, node)
        self._pois = list()

    @property
    def tension(self):
        """Tension in the cable in [kN] (Readonly, calculated)"""
        return self._vfNode.tension

    @property
    def stretch(self):
        """Stretch of the cable in [m] (Readonly, calculated)"""
        return self._vfNode.stretch

    @property
    def length(self):
        """Length in rest [m]"""
        return self._vfNode.Length

    @length.setter
    def length(self, val):
        if val < 1e-9:
            raise Exception('Length shall be more than 0 (otherwise stiffness EA/L becomes infinite)')
        self._vfNode.Length = val

    @property
    def EA(self):
        """Stiffness of the cable in [kN]"""
        return self._vfNode.EA

    @EA.setter
    def EA(self, ea):
        self._vfNode.EA = ea

    @property
    def diameter(self):
        """Diameter of the cable [m]"""
        return self._vfNode.diameter

    @diameter.setter
    def diameter(self, diameter):
        self._vfNode.diameter = diameter

    def get_points_for_visual(self):
        """Returns an list of 3D locations which can be used for visualization
        """
        return self._vfNode.global_points

    def check_endpoints(self):
        """Verifies that the endpoints are Pois"""
        if isinstance(self._pois[0], Sheave):
            raise ValueError(
                'First and last connection of a cable {} should be of type <Poi>. It is not allowed to use Sheave {} as start'.format(self.name, self._pois[0].name))

        if isinstance(self._pois[-1], Sheave):
            raise ValueError(
                'First and last connection of a cable {} should be of type <Poi>. It is not allowed to use Sheave {} as endpoint'.format(self.name, self._pois[-1].name))



    def _update_pois(self):
        self._vfNode.clear_connections()
        for point in self._pois:

            if isinstance(point, Poi):
                try:
                    self._vfNode.add_connection_poi(point._vfNode)
                except:
                    self._vfNode.add_connection(point._vfNode)
            if isinstance(point, Sheave):
                self._vfNode.add_connection_sheave(point._vfNode)

    def add_connection(self, apoi):
        """Adds a poi to the list of connection points"""

        if isinstance(apoi, str):
            apoi = self._scene[apoi]

        if not (isinstance(apoi, Poi) or isinstance(apoi, Sheave)):
            raise TypeError('Provided point should be a Poi')

        if self._pois:  # check for not empty
            if self._pois[-1] == apoi:
                raise Exception('The same poi can not be added directly after itself: {}'.format(apoi.name))

        self._pois.append(apoi)
        self._update_pois()

    def clear_connections(self):
        """Removes all connections"""
        self._pois.clear()
        self._update_pois()

    def give_poi_names(self):
        """Returns a list with the names of all the pois"""
        r = list()
        for p in self._pois:
            r.append(p.name)
        return r

    def give_python_code(self):
        code = "# code for {}".format(self.name)

        poi_names = self.give_poi_names()
        n_sheaves = len(poi_names)-2

        code += "\ns.new_cable(name='{}',".format(self.name)
        code += "\n            poiA='{}',".format(poi_names[0])
        code += "\n            poiB='{}',".format(poi_names[-1])
        code += "\n            length={},".format(self.length)

        if self.diameter != 0:
            code += "\n            diameter={},".format(self.diameter)

        if len(poi_names) <= 2:
            code += "\n            EA={})".format(self.EA)
        else:
            code += "\n            EA={},".format(self.EA)

            if n_sheaves == 1:
                code += "\n            sheaves = ['{}'])".format(poi_names[1])
            else:
                code += "\n            sheaves = ['{}',".format(poi_names[1])
                for i in range(n_sheaves-2):
                    code += "\n                       '{}',".format(poi_names[2+i])
                code += "\n                       '{}']),".format(poi_names[-2])


        return code

class Force(NodeWithParent):
    """A Force models a force and moment on a poi.

    Both are expressed in the global axis system.

    """

    @property
    def force(self):
        """
        Gets or sets the x,y and z force components.

        Example s['wind'].force = (12,34,56)
        """
        return self._vfNode.force

    @force.setter
    def force(self, val):
        assert3f(val)
        self._vfNode.force = val

    @property
    def moment(self):
        """
        Gets or sets the x,y and z moment components.

        Example s['wind'].moment = (12,34,56)
        """
        return self._vfNode.moment


    @moment.setter
    def moment(self, val):
        assert3f(val)
        self._vfNode.moment = val

    def give_python_code(self):
        code = "# code for {}".format(self.name)

        # new_force(self, name, parent=None, force=None, moment=None):

        code += "\ns.new_force(name='{}',".format(self.name)
        code += "\n            parent='{}',".format(self.parent.name)
        code += "\n            force=({}, {}, {}),".format(*self.force)
        code += "\n            moment=({}, {}, {}) )".format(*self.moment)
        return code

class Sheave(NodeWithParent):
    """A Sheave models sheave with axis and diameter.


    """

    @property
    def axis(self):
        """
        Gets or sets direction of the sheave axis
        """
        return self._vfNode.axis_direction

    @axis.setter
    def axis(self, val):
        assert3f(val)
        if np.linalg.norm(val) == 0:
            raise ValueError('Axis can not be 0,0,0')
        self._vfNode.axis_direction = val

    @property
    def radius(self):
        """
        Gets or sets radius of the sheave
        """
        return self._vfNode.radius


    @radius.setter
    def radius(self, val):
        assert1f(val)
        self._vfNode.radius = val

    def give_python_code(self):
        code = "# code for {}".format(self.name)
        code += "\ns.new_sheave(name='{}',".format(self.name)
        code += "\n            parent='{}',".format(self.parent.name)
        code += "\n            axis=({}, {}, {}),".format(*self.axis)
        code += "\n            radius={} )".format(self.radius)
        return code

class HydSpring(NodeWithParent):
    """A HydSpring models a linearized hydrostatic spring.

    The cob (center of buoyancy) is defined in the parent axis system.
    All other properties are defined relative to the cob.

    """

    @property
    def cob(self):
        """Center of buoyancy in parent axis system"""
        return self._vfNode.position

    @cob.setter
    def cob(self, val):
        assert3f(val)
        self._vfNode.position = val

    @property
    def BMT(self):
        """Vertical distance between cob and metacenter for roll"""
        return self._vfNode.BMT

    @BMT.setter
    def BMT(self, val):
        self._vfNode.BMT = val

    @property
    def BML(self):
        """Vertical distance between cob and metacenter for pitch"""
        return self._vfNode.BML

    @BML.setter
    def BML(self, val):
        self._vfNode.BML = val

    @property
    def COFX(self):
        """Horizontal x-position Center of Floatation (center of waterplane area), relative to cob"""
        return self._vfNode.COFX

    @COFX.setter
    def COFX(self, val):
        self._vfNode.COFX = val

    @property
    def COFY(self):
        """Horizontal y-position Center of Floatation (center of waterplane area), relative to cob"""
        return self._vfNode.COFY

    @COFY.setter
    def COFY(self, val):
        self._vfNode.COFY = val

    @property
    def kHeave(self):
        """Heave stiffness in kN/m"""
        return self._vfNode.kHeave

    @kHeave.setter
    def kHeave(self, val):
        self._vfNode.kHeave = val

    @property
    def waterline(self):
        """Waterline-elevation relative to cob for un-stretched heave-spring. Positive if cob is below the waterline (which is where is normally is)"""
        return self._vfNode.waterline

    @waterline.setter
    def waterline(self, val):
        self._vfNode.waterline = val

    @property
    def displacement_kN(self):
        """Displacement in [kN] when waterline is at waterline-elevation"""
        return self._vfNode.displacement_kN

    @displacement_kN.setter
    def displacement_kN(self, val):
        self._vfNode.displacement_kN = val

    def give_python_code(self):
        code = "# code for {}".format(self.name)

        # new_force(self, name, parent=None, force=None, moment=None):

        code += "\ns.new_hydspring(name='{}',".format(self.name)
        code += "\n            parent='{}',".format(self.parent.name)
        code += "\n            cob=({}, {}, {}),".format(*self.cob)
        code += "\n            BMT={},".format(self.BMT)
        code += "\n            BML={},".format(self.BML)
        code += "\n            COFX={},".format(self.COFX)
        code += "\n            COFY={},".format(self.COFY)
        code += "\n            kHeave={},".format(self.kHeave)
        code += "\n            waterline={},".format(self.waterline)
        code += "\n            displacement_kN={} )".format(self.displacement_kN)

        return code

class LC6d(CoreConnectedNode):
    """A LC6d models a Linear Connector with 6 dofs.

    It connects two Axis elements with six linear springs.
    The translational-springs are easy. The rotational springs may not be as intuitive. They are defined as:

      - rotation_x = arc-tan ( uy[0] / uy[1] )
      - rotation_y = arc-tan ( -ux[0] / ux[2] )
      - rotation_z = arc-tan ( ux[0] / ux [1] )

    which works fine for small rotations and rotations about only a single axis.

    Try to avoid using very high stiffness settings to create fixed connections. It is better to use use the "fixed"
    property of axis systems to create joints.

    """

    def __init__(self, scene, node):
        super().__init__(scene, node)
        self._master = None
        self._slave = None

    @property
    def stiffness(self):
        """Stiffness of the connector (kx, ky, kz, krx, kry, krz)"""
        return self._vfNode.stiffness

    @stiffness.setter
    def stiffness(self, val):
        self._vfNode.stiffness = val

    @property
    def master(self):
        """Master axis system"""
        return self._master

    @master.setter
    def master(self,val):
        if not isinstance(val, Axis):
            raise TypeError('Provided master should be a Axis')

        self._master = val
        self._vfNode.master = val._vfNode

    @property
    def slave(self):
        """Slave axis system"""
        return self._slave

    @slave.setter
    def slave(self, val):
        if not isinstance(val, Axis):
            raise TypeError('Provided master should be a Axis')

        self._slave = val
        self._vfNode.slave = val._vfNode


    def give_python_code(self):
        code = "# code for {}".format(self.name)


        code += "\ns.new_linear_connector_6d(name='{}',".format(self.name)
        code += "\n            master='{}',".format(self.master.name)
        code += "\n            slave='{}',".format(self.slave.name)
        code += "\n            stiffness=({}, {}, {}, ".format(*self.stiffness[:3])
        code += "\n                       {}, {}, {}) )".format(*self.stiffness[3:])

        return code

class Connector2d(CoreConnectedNode):
    """A Connector2d linear connector with acts both on linear displacement and angular displacement.

    * the linear stiffness is defined by k_linear and is defined over the actual shortest direction between master and slave.
    * the angular stiffness is defined by k_angular and is defined over the actual smallest angle between the two systems.
    """

    def __init__(self, scene, node):
        super().__init__(scene, node)
        self._master = None
        self._slave = None

    @property
    def angle(self):
        """Actual angle between master and slave [deg] (read-only)"""
        return np.rad2deg(self._vfNode.angle)

    @property
    def force(self):
        """Actual force between master and slave [kN] (read-only)"""
        return self._vfNode.force

    @property
    def moment(self):
        """Actual moment between master and slave [kN*m] (read-only)"""
        return self._vfNode.moment

    @property
    def axis(self):
        """Actual rotation axis between master and slave (read-only)"""
        return self._vfNode.axis

    @property
    def k_linear(self):
        """Linear stiffness [kN/m]"""
        return self._vfNode.k_linear

    @k_linear.setter
    def k_linear(self, value):
        self._vfNode.k_linear = value

    @property
    def k_angular(self):
        """Linear stiffness [kN*m/rad]"""
        return self._vfNode.k_angular

    @k_angular.setter
    def k_angular(self, value):
        self._vfNode.k_angular = value

    @property
    def master(self):
        """Master axis system"""
        return self._master

    @master.setter
    def master(self, val):
        if not isinstance(val, Axis):
            raise TypeError('Provided master should be a Axis')

        self._master = val
        self._vfNode.master = val._vfNode

    @property
    def slave(self):
        """Slave axis system"""
        return self._slave

    @slave.setter
    def slave(self, val):
        if not isinstance(val, Axis):
            raise TypeError('Provided master should be a Axis')

        self._slave = val
        self._vfNode.slave = val._vfNode

    def give_python_code(self):
        code = "# code for {}".format(self.name)

        code += "\ns.new_connector2d(name='{}',".format(self.name)
        code += "\n            master='{}',".format(self.master.name)
        code += "\n            slave='{}',".format(self.slave.name)
        code += "\n            k_linear ={},".format(self.k_linear)
        code += "\n            k_angular ={})".format(self.k_angular)

        return code

class LinearBeam(CoreConnectedNode):
    """A LinearBeam models a FEM-like linear beam element.

    A LinearBeam node connects two Axis elements with six linear springs.

    By definition the beam runs in the X-direction of the master axis system. So it may be needed to create a
    dedicated Axis element for the beam to control the orientation.

    The beam is defined using the following properties:

    *  EIy  - bending stiffness about y-axis
    *  EIz  - bending stiffness about z-axis
    *  GIp  - torsional stiffness about x-axis
    *  EA   - axis stiffness in x-direction
    *  L    - the un-stretched length of the beam

    The beam element is in rest if the slave axis system

    1. has the same global orientation as the master system
    2. is at global position equal to the global position of local point (L,0,0) of the master axis. (aka: the end of the beam)


    The scene.new_linearbeam automatically creates a dedicated axis system for each end of the beam. The orientation of this axis-system
    is determined as follows:

    First the direction from master to slave is determined: D
    The axis of rotation is the cross-product of the unit x-axis and D    AXIS = ux x D
    The angle of rotation is the angle between the master x-axis and D

    The rotation about the rotated X-axis is undefined.
    
    """

    def __init__(self, scene, node):
        super().__init__(scene, node)
        self._master = None
        self._slave = None

    @property
    def EIy(self):
        return self._vfNode.EIy
    @EIy.setter
    def EIy(self,value):
        self._vfNode.EIy = value

    @property
    def EIz(self):
        return self._vfNode.EIz

    @EIz.setter
    def EIz(self, value):
        self._vfNode.EIz = value

    @property
    def GIp(self):
        return self._vfNode.GIp

    @GIp.setter
    def GIp(self, value):
        self._vfNode.GIp = value

    @property
    def EA(self):
        return self._vfNode.EA

    @EA.setter
    def EA(self, value):
        self._vfNode.EA = value

    @property
    def master(self):
        return self._master

    @property
    def L(self):
        return self._vfNode.L

    @L.setter
    def L(self, value):
        self._vfNode.L = value

    @master.setter
    def master(self,val):
        if not isinstance(val, Axis):
            raise TypeError('Provided master should be a Axis')

        self._master = val
        self._vfNode.master = val._vfNode

    @property
    def slave(self):
        return self._slave

    @slave.setter
    def slave(self, val):
        if not isinstance(val, Axis):
            raise TypeError('Provided master should be a Axis')

        self._slave = val
        self._vfNode.slave = val._vfNode

    # read-only
    @property
    def moment_on_master(self):
        return self._vfNode.moment_on_master

    @property
    def moment_on_slave(self):
        return self._vfNode.moment_on_slave

    @property
    def tension(self):
        return self._vfNode.tension

    @property
    def torsion(self):
        return self._vfNode.torsion

    @property
    def torsion_angle(self):
        """Torsion angle in degrees"""
        return np.rad2deg(self._vfNode.torsion_angle)


def give_python_code(self):
        code = "# code for {}".format(self.name)

        code += "\ns.new_linear_beam(name='{}',".format(self.name)
        code += "\n            master='{}',".format(self.master.name)
        code += "\n            slave='{}',".format(self.slave.name)
        code += "\n            EIy ={},".format(self.EIy)
        code += "\n            EIz ={},".format(self.EIz)
        code += "\n            GIp ={},".format(self.GIp)
        code += "\n            EA ={},".format(self.EA)
        code += "\n            L ={}) # L can possibly be omitted".format(self.L)

        return code

class TriMeshSource(Node):
    """
    TriMesh

    A TriMesh node contains triangular mesh which can be used for buoyancy or contact

    """

    def __init__(self, scene, source):

        # Note: Visual does not have a corresponding vfCore Node in the scene but does have a vfCore
        self.scene = scene
        self._TriMesh = source
        self._new_mesh = True             # cheat for visuals

        self._path = ''                   # stores the data that was used to load the obj
        self._offset = (0,0,0)
        self._scale = (1,1,1)
        self._rotation = (0,0,0)

    def AddVertex(self, x,y,z):
        self._TriMesh.AddVertex(x,y,z)

    def AddFace(self, i,j,k):
        self._TriMesh.AddFace(i,j,k)

    def get_extends(self):
        """Returns the extends of the mesh in global coordinates

        Returns: (minimum_x, maximum_x, minimum_y, maximum_y, minimum_z, maximum_z)

        """

        t = self._TriMesh

        if t.nFaces == 0:
            return (0,0,0,0)

        v = t.GetVertex(0)
        xn = v[0]
        xp = v[0]
        yn = v[1]
        yp = v[1]
        zn = v[2]
        zp = v[2]

        for i in range(t.nVertices):
            v = t.GetVertex(i)
            x = v[0]
            y= v[1]
            z = v[2]

            if x<xn:
                xn = x
            if x>xp:
                xp = x
            if y < yn:
                yn = y
            if y > yp:
                yp = y
            if z < zn:
                zn = z
            if z > zp:
                zp = z

        return (xn,xp,yn,yp,zn, zp)





    def make_cube(self):
        """Sets the mesh to a cube"""

        from vtk import vtkCubeSource
        cube = vtkCubeSource()
        self.load_vtk_polydataSource(cube)

    def _fromVTKpolydata(self,polydata, offset = None, rotation = None, scale = None):

        import vtk

        tri = vtk.vtkTriangleFilter()

        tri.SetInputConnection(polydata)


        scaleFilter = vtk.vtkTransformPolyDataFilter()
        rotationFilter = vtk.vtkTransformPolyDataFilter()

        s = vtk.vtkTransform()
        s.Identity()
        r = vtk.vtkTransform()
        r.Identity()

        scaleFilter.SetInputConnection(tri.GetOutputPort())
        rotationFilter.SetInputConnection(scaleFilter.GetOutputPort())

        if scale is not None:
            s.Scale(*scale)

        if rotation is not None:
            q = rotation
            angle = (q[0] ** 2 + q[1] ** 2 + q[2] ** 2) ** (0.5)
            if angle > 0:
                r.RotateWXYZ(angle, q[0] / angle, q[1] / angle, q[2] / angle)

        if offset is None:
            offset = [0,0,0]

        scaleFilter.SetTransform(s)
        rotationFilter.SetTransform(r)
        rotationFilter.Update()

        data = rotationFilter.GetOutput()
        self._TriMesh.Clear()

        for i in range(data.GetNumberOfPoints()):
            point = data.GetPoint(i)
            self._TriMesh.AddVertex(point[0] + offset[0], point[1] + offset[1], point[2] + offset[2])

        for i in range(data.GetNumberOfCells()):
            cell = data.GetCell(i)

            if isinstance(cell,vtk.vtkLine):
                print("Cell nr {} is a line, not adding to mesh".format(i))
                continue

            id0 = cell.GetPointId(0)
            id1 = cell.GetPointId(1)
            id2 = cell.GetPointId(2)
            self._TriMesh.AddFace(id0, id1, id2)

        # check if anything was loaded
        if self._TriMesh.nFaces == 0:
            raise Exception('No faces in poly-data - no geometry added (hint: empty obj file?)')
        self._new_mesh = True

    def load_vtk_polydataSource(self, polydata):
        """Fills the triangle data from a vtk polydata such as a cubeSource.

        The vtk TriangleFilter is used to triangulate the source

        Examples:
            cube = vtk.vtkCubeSource()
            cube.SetXLength(122)
            cube.SetYLength(38)
            cube.SetZLength(10)
            trimesh.load_vtk_polydataSource(cube)
        """

        self._fromVTKpolydata(polydata.GetOutputPort())


    def load_obj(self, filename, offset = None, rotation = None, scale = None):
        """Loads an .obj file and and triangulates it.

        Order of modifications:

        1. rotate
        2. scale
        3. offset

        Args:
            filename: (str or path): file to load
            offset: : offset
            rotation:  : rotation
            scale:  scale

        """
        if not exists(filename):
            raise ValueError('File {} does not exit'.format(filename))

        filename = str(filename)

        import vtk
        obj = vtk.vtkOBJReader()
        obj.SetFileName(filename)

        # Add cleaning
        cln = vtk.vtkCleanPolyData()
        cln.SetInputConnection(obj.GetOutputPort())

        self._fromVTKpolydata(cln.GetOutputPort(), offset=offset, rotation=rotation, scale=scale)

        self._path = split(filename)[1]
        self._scale = scale
        self._offset = offset
        self._rotation = rotation

        if self._scale is None:
            self._scale = (1.0, 1.0, 1.0)
        if self._offset is None:
            self._offset = (0.0, 0.0, 0.0)
        if self._rotation is None:
            self._rotation = (0.0, 0.0, 0.0)

    def give_python_code(self):
        code = "# No code generated for TriMeshSource"
        return code

    def change_parent_to(self, new_parent):
        if not (isinstance(new_parent, Axis) or new_parent is None):
            raise ValueError('Visuals can only be attached to an axis (or derived) or None')

        # get current position and orientation
        if self.parent is not None:
            cur_position = self.parent.to_glob_position(self.offset)
            cur_rotation = self.parent.to_glob_direction(self.rotation)
        else:
            cur_position = self.offset
            cur_rotation = self.rotation

        self.parent = new_parent

        if new_parent is None:
            self.offset = cur_position
            self.rotation = cur_rotation
        else:
            self.offset = new_parent.to_loc_position(cur_position)
            self.rotation = new_parent.to_loc_direction(cur_rotation)

class Buoyancy(NodeWithParent):
    """Buoyancy provides a buoyancy force based on a buoyancy mesh. The mesh is triangulated and chopped at the instantaneous flat water surface. Buoyancy is applied as an upwards force that the center of buoyancy.
    The calculation of buoyancy is as accurate as the provided geometry.

    There as no restrictions to the size or aspect ratio of the panels. It is excellent to model as box using 6 faces. Using smaller panels has a negative effect on performance.

    The normals of the panels should point towards to water.
    """

    # init parent and name are fully derived from NodeWithParent
    # _vfNode is a buoyancy
    def __init__(self, scene, vfBuoyancy):
        super().__init__(scene, vfBuoyancy)
        self._None_parent_acceptable = True
        self._trimesh = TriMeshSource(self._scene, self._vfNode.trimesh) # the tri-mesh is wrapped in a custom object

    @property
    def trimesh(self):
        return self._trimesh

    @property
    def cob(self):
        """Returns the GLOBAL position of the center of buoyancy"""
        return self._vfNode.cob

    @property
    def cob_local(self):
        """Returns the local position of the center of buoyancy"""

        return self.parent.to_loc_position(self.cob)

    @property
    def displacement(self):
        """Returns displaced volume in m^3"""
        return self._vfNode.displacement

    # @trimesh.setter
    # def trimesh(self, new_mesh):
    #     raise Exception()
    #     if isinstance(new_mesh, TriMeshSource):
    #         self._vfNode.trimesh = new_mesh._TriMesh
    #         self._trimesh = new_mesh
    #     else:
    #         raise TypeError('new_mesh should be a TriMeshSource object but is a {}'.format(type(new_mesh)))

    def give_python_code(self):
        code = "# code for {}".format(self.name)
        code += "\nmesh = s.new_buoyancy(name='{}',".format(self.name)
        if self.parent:
            code += "\n          parent='{}')".format(self.parent.name)
        code += "\nmesh.trimesh.load_obj(s.get_resource_path(r'{}'), scale = ({},{},{}), rotation = ({},{},{}), offset = ({},{},{}))".format(self.trimesh._path, *self.trimesh._scale, *self.trimesh._rotation, *self.trimesh._offset)

        return code

class BallastSystem(Poi):
    """A BallastSystem

    The position of the axis system is the reference position for the tanks.

    Tanks can be added using new_tank()


    technical notes:
    - System is similar to the setup of RigidBody, but without the Axis
    - The class extends Poi, but overrides some of its properties
    - Update nees to be called to update the weight and cog

    TODO: Inertia

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

    def __init__(self, scene, poi, force):
        super().__init__(scene, poi)

        # The poi is the Node
        # force is added separately
        self._vfForce = force

        self._tanks = []
        """List of tank objects"""

        self._position = (0., 0., 0.)
        """Position is the origin of the ballast system"""

        self._cog = (0., 0., 0.)
        """Position of the CoG of the ballast-tanks relative to self._position, calculated when calling update()"""

        self._weight = 0
        """Weight [kN] of the ballast-tanks , calculated when calling update()"""

        self.frozen = False
        """The contents of a frozen tank should not be changed"""

    # override the following properties
    @Poi.parent.setter
    def parent(self, var):
        """Assigns a new parent. Keeps the local position and rotations the same

        See also: change_parent_to
        """

        super(Poi, type(self)).parent.fset(self, var)
        # update parent of other core nodes
        for tank in self._tanks:
            tank._vfNode.parent = self.parent._vfNode



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

        print('Weight {} cog {} {} {}'.format(self._weight, *self._cog))

    def _delete_vfc(self):
        super()._delete_vfc()
        self._scene._vfc.delete(self._vfForce.name)

        # delete the pointmasses (if any)
        for tank in self._tanks:
            if tank._pointmass is not None:
                self._scene._vfc.delete(tank._pointmass.name)

    @property
    def position(self):
        """Local position"""
        return self._position

    @position.setter
    def position(self, new_position):
        assert3f(new_position)
        self._position = new_position

    @property
    def name(self):
        return super().name

    @name.setter
    def name(self, newname):
        super(Poi, self.__class__).name.fset(self, newname)
        self._vfForce.name = newname + vfc.VF_NAME_SPLIT + "gravity"

    def new_tank(self, name, position, capacity_kN, actual_fill = 0, frozen = False) :
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

        assert name not in [t.name for t in self._tanks], ValueError('Double names are not allowed, {} already exists'.format(name))

        t = BallastSystem.Tank()
        t.name = name
        t.position = position
        t.max = capacity_kN
        t.pct = actual_fill
        t.frozen = frozen

        t._pointmass = \
            self._scene._vfc.new_pointmass(self.name + vfc.VF_NAME_SPLIT + '_pointmass_{}'.format(name))
        t._pointmass.parent = self.parent._vfNode # Axis

        self._tanks.append(t)

        return t

    def reorder_tanks(self, names):
        """Places tanks with given names at the top of the list. Other tanks are appended afterwards in original order.

        For a complete re-order give all tank names.

        Example:
            let tanks be 'a','b','c','d','e'

            then re_order_tanks(['e','b']) will result in ['e','b','a','c','d']
        """
        for name in names:
            if name not in self.tank_names():
                raise ValueError('No tank with name {}'.format(name))

        old_tanks = self._tanks.copy()
        self._tanks.clear()
        to_be_deleted = list()

        for name in names:
            for tank in old_tanks:
                if tank.name == name:
                    self._tanks.append(tank)
                    to_be_deleted.append(tank)

        for tank in to_be_deleted:
            old_tanks.remove(tank)

        for tank in old_tanks:
            self._tanks.append(tank)

    def order_tanks_by_elevation(self):
        """Re-orders the existing tanks such that the lowest tanks are higher in the list"""

        zs = [tank.position[2] for tank in self._tanks]
        inds = np.argsort(zs)
        self._tanks = [self._tanks[i] for i in inds]

    def order_tanks_by_distance_from_point(self, point, reverse=False):
        """Re-orders the existing tanks such that the tanks *furthest* from the point are first on the list

        Args:
            point : (x,y,z)  - reference point to determine the distance to
            reverse: (False) - order in reverse order: tanks nearest to the points first on list


        """
        pos = [tank.position for tank in self._tanks]
        pos = np.array(pos, dtype=float)
        pos -= np.array(point)

        dist = np.apply_along_axis(np.linalg.norm,1,pos)

        if reverse:
            inds = np.argsort(dist)
        else:
            inds = np.argsort(-dist)

        self._tanks = [self._tanks[i] for i in inds]

    def order_tanks_to_maximize_inertia_moment(self):
        """Re-order tanks such that tanks furthest from center of system are first on the list"""
        self._order_tanks_to_inertia_moment()

    def order_tanks_to_minimize_inertia_moment(self):
        """Re-order tanks such that tanks nearest to center of system are first on the list"""
        self._order_tanks_to_inertia_moment(maximize=False)

    def _order_tanks_to_inertia_moment(self, maximize = True):

        pos = [tank.position for tank in self._tanks]
        m = [tank.max for tank in self._tanks]
        pos = np.array(pos, dtype=float)
        mxmymz = np.vstack((m,m,m)).transpose() * pos
        total = np.sum(m)
        point = sum(mxmymz) / total

        if maximize:
            self.order_tanks_by_distance_from_point(point)
        else:
            self.order_tanks_by_distance_from_point(point, reverse=True)


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


    def empty_all_usable_tanks(self):
        for t in self._tanks:
            if not t.frozen:
                t.make_empty()

    def tank(self, name):
        for t in self._tanks:
            if t.name == name:
                return t
        raise ValueError('No tank with name {}'.format(name))

    def __getitem__(self, item):
        return self.tank(item)


    @property
    def cogx(self):
        return self.cog[0]

    @property
    def cogy(self):
        return self.cog[1]

    @property
    def cogz(self):
        return self.cog[2]

    @property
    def cog(self):
        """Returns the cog of the ballast-system"""
        self.update()
        return (self._cog[0], self._cog[1], self._cog[2])

    @property
    def weight(self):
        """Returns the cog of the ballast-system"""
        self.update()
        return self._weight


    @property
    def mass(self):
        """Control the static mass of the body"""
        return self._vfForce.force[2] / -vfc.G



    def give_python_code(self):
        code = "\n# code for {} and its tanks".format(self.name)

        code += "\nbs = s.new_ballastsystem('{}', parent = '{}',".format(self.name, self.parent.name)
        code += "\n                         position = ({},{},{}))".format(*self.position)

        for tank in self._tanks:
            code += "\nbs.new_tank('{}', position = ({},{},{}),".format(tank.name, *tank.position)
            code += "\n            capacity_kN = {}, frozen = {}, actual_fill = {})".format(tank.max, tank.frozen, tank.pct)

        return code

class WaveInteraction1(Node):
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

    def __init__(self, scene):

        super().__init__(scene)
        self.scene = scene

        self.offset = [0, 0, 0]
        """Offset (x,y,z) of the visual. Offset is applied after scaling"""

        self.parent = None
        """Parent : Axis-type"""

        self.path = None
        """Filename of a file that can be read by a Hyddb1 object"""

    def give_python_code(self):
        code = "# code for {}".format(self.name)

        code += "\ns.new_waveinteraction(name='{}',".format(self.name)
        code += "\n            parent='{}',".format(self.parent.name)
        code += "\n            path=r'{}',".format(self.path)
        code += "\n            offset=({}, {}, {}) )".format(*self.offset)

        return code

    def change_parent_to(self, new_parent):
        if not (isinstance(new_parent, Axis)):
            raise ValueError('Hydrodynamic databases can only be attached to an axis (or derived)')

        # get current position and orientation
        if self.parent is not None:
            cur_position = self.parent.to_glob_position(self.offset)
        else:
            cur_position = self.offset

        self.parent = new_parent
        self.offset = new_parent.to_loc_position(cur_position)




#

# ===============

class Scene:
    """
    A Scene is the main component of virtual-float.

    It provides a world to place nodes (elements) in.
    It interfaces with the virtual-float core for all calculations.

    _vfc : DAVE Core
    """

    def __init__(self, filename = None, copy_from = None):
        """Creates a new Scene

        Args:
            filename: (str or Path) Insert contents from this file into the newly created scene
            copy_from:  (Scene) Copy nodes from this other scene into the newly created scene
        """

        self.verbose = True
        """Report actions using print()"""

        self._vfc = pyo3d.Scene()
        """_vfc : DAVE Core, where the actual magic happens"""

        self._nodes = []
        """Contains a list of all nodes in the scene"""

        self.static_tolerance = 0.01
        """Desired tolerance when solving statics"""

        self.resources_paths = []
        """A list of paths where to look for resources such as .obj files. Priority is given to paths earlier in the list."""
        self.resources_paths.extend(vfc.RESOURCE_PATH)


        self._name_prefix = ""
        """An optional prefix to be applied to node names. Used when importing scenes."""

        if filename is not None:
            self.load_scene(filename)

        if copy_from is not None:
            self.import_scene(copy_from, containerize=False)

    def clear(self):
        """Deletes all nodes"""

        self._nodes = []
        del self._vfc
        self._vfc = pyo3d.Scene()


    # =========== private functions =============

    def _print_cpp(self):
        print(self._vfc.to_string())

    def _print(self,what):
        if self.verbose:
            print(what)

    def _prefix_name(self, name):
        return self._name_prefix + name

    def _verify_name_available(self, name):
        """Throws an error if a node with name 'name' already exists"""
        if name in self._vfc.names:
            raise Exception("The name '{}' is already in use. Pick a unique name".format(name))

    def _node_from_node_or_str(self, node):
        """If node is a string, then returns the node with that name,
        if node is a node, then returns that node

        Raises:
            ValueError if a string is passed with an non-existing node
        """

        if isinstance(node, Node):
            return node
        if isinstance(node, str):
            return self[node]
        raise ValueError('Node should be a Node or a string, not a {}'.format(type(node)))

    def _node_from_node(self, node, reqtype):
        """Gets a node from the specified type

        Returns None if node is None
        Returns node if node is already a reqtype type node
        Else returns the axis with the given name

        Raises Exception if a node with name is not found"""

        if node is None:
            return None

        # node is a string then get the node with this name
        if type(node) == str:
            node = self[self._name_prefix + node]

        reqtype = make_iterable(reqtype)

        for r in reqtype:
            if isinstance(node, r):
                return node

        if issubclass(type(node), Node):
            raise Exception(
                "Element with name {} can not be used , it should be a {} or derived type but is a {}.".format(
                    node.name, reqtype, type(node)))

        raise Exception('This is not an acceptable input argument {}'.format(node))

    def _parent_from_node(self, node):
        """Returns None if node is None
        Returns node if node is an axis type node
        Else returns the axis with the given name

        Raises Exception if a node with name is not found"""

        return self._node_from_node(node, Axis)

    def _poi_from_node(self, node):
        """Returns None if node is None
        Returns node if node is an poi type node
        Else returns the poi with the given name

        Raises Exception if anything is not ok"""

        return self._node_from_node(node, Poi)

    def _poi_or_sheave_from_node(self, node):
        """Returns None if node is None
        Returns node if node is an poi type node
        Else returns the poi with the given name

        Raises Exception if anything is not ok"""

        return self._node_from_node(node, [Poi, Sheave])

    def _geometry_changed(self):
        """Notify the scene that the geometry has changed and that the global transforms are invalid"""
        self._vfc.geometry_changed()

    # ======== resources =========

    def get_resource_path(self, name):
        """Looks for a file with "name" in the specified resource-paths and returns the full path to the the first one
        that is found.
        If name is a full path to an existing file, then that is returned.

        See Also:
            resource_paths


        Returns:
            Full path to resource

        Raises:
            FileExistsError if resource is not found

        """

        if isfile(name):
            return name

        for res in self.resources_paths:
            p = Path(res)

            full = p / name
            if isfile(full):
                return full

        # prepare feedback for error
        ext = str(name).split('.')[-1]  # everything after the last .

        print("The following resources with extension {} are available with ".format(ext))
        available = self.get_resource_list(ext)
        for a in available:
            print(a)

        raise FileExistsError('Resource "{}" not found in resource paths'.format(name))

    def get_resource_list(self, extension):
        """Returns a list of all file-paths (strings) given extension in any of the resource-paths"""

        r = []

        for dir in self.resources_paths:
            try:
                files = listdir(dir)
                for file in files:
                    if file.endswith(extension):
                        if file not in r:
                            r.append(file)
            except FileNotFoundError:
                pass

        return r



    # ======== element functions =========

    def node_by_name(self, node_name):
        for N in self._nodes:
            if N.name == node_name:
                return N

        self.print_node_tree()
        raise ValueError('No node with name "{}". Available names printed above.'.format(node_name))

    def __getitem__(self, node_name):
        """Returns a node with name"""
        return self.node_by_name(node_name)

    def nodes_of_type(self, node_class):
        """Returns all nodes of the specified or derived type

        Examples:
            pois = scene.nodes_of_type(DAVE.Poi)
            axis_and_bodies = scene.nodes_of_type(DAVE.Axis)
        """
        r = list()
        for n in self._nodes:
            if isinstance(n, node_class):
                r.append(n)
        return r

    def sort_nodes_by_dependency(self):
        """Sorts the nodes such that a node only depends on nodes earlier in the list."""

        scene_names = [n.name for n in self._nodes]

        self._vfc.state_update()  # use the function from the core.
        new_list = []
        for name in self._vfc.names:  # and then build a new list using the names
            if vfc.VF_NAME_SPLIT in name:
                continue

            if name not in scene_names:
                raise Exception('Something went wrong with sorting the the nodes by dependency. '
                                'Node naming between core and scene is inconsistent for node {}'.format(name))

            new_list.append(self[name])

        # and add the nodes without a vfc-core connection
        for node in self._nodes:
            if not node in new_list:
                new_list.append(node)

        self._nodes = new_list

    def name_available(self, name):
        """Returns True if the name is still available"""
        names = [n.name for n in self._nodes]
        names.extend(self._vfc.names)
        return not (name in names)

    def available_name_like(self, like):
        """Returns an available name like the one given, for example Axis23"""
        if self.name_available(like):
            return like
        counter = 1
        while True:
            name = like + '_' + str(counter)
            if self.name_available(name):
                return name
            counter += 1

    def nodes_depending_on(self, node):
        """Returns a list of nodes that physically depend on node. Only direct dependants are obtained with a connection to the core.
        This function should be used to determine dependencies of Core-connected elements.

        For making node-trees please use nodes_with_parent instead.

        Args:
            node : Node or node-name

        Returns:
            list of names

        See Also: nodes_with_parent
        """

        if isinstance(node, Node):
            node = node.name

        # check the node type
        _node = self[node]
        if not isinstance(_node, CoreConnectedNode):
            return []
        else:
            names =  self._vfc.elements_depending_on(node)

        r = []
        for name in names:
            try:
                r.append(self[name].name)
            except:
                pass

        # check visuals as well (which are not core-connected)
        for v in self.nodes_of_type(Visual):
            if v.parent is _node:
                r.append(v.name)

        return r

    def nodes_with_parent(self, node):
        """Returns a list of nodes that have given node as a parent. Good for making trees.
        For checking physical connections use nodes_depending_on instead.

        Args:
            node : Node or node-name

        Returns:
            list of names

        See Also: nodes_depending_on
        """

        if isinstance(node, str):
            node = self[node]

        r = []

        for n in self._nodes:

            try:
                parent = n.parent
            except AttributeError:
                continue

            if parent == node:
                r.append(n.name)

        return r



    def delete(self, node):
        """Deletes the given node from the scene as well as all nodes depending on it.

        See Also:
            dissolve
        """

        depending_nodes = self.nodes_depending_on(node)

        if isinstance(node, str):
            node = self[node]

        self._print('Deleting {} [{}]'.format(node.name, str(type(node)).split('.')[-1][:-2]))

        # First delete the dependencies
        for d in depending_nodes:
            if not self.name_available(d):  # element is still here
                self.delete(d)

        # then remove the vtk node itself
        self._print('removing vfc node')
        node._delete_vfc()
        self._nodes.remove(node)



    def dissolve(self, node):
        """Attempts to delete the given node without affecting the rest of the model.

        1. Look for nodes that have this node as parent
        2. Attach those nodes to the parent of this node.
        3. Delete this node.

        There are many situations in which this will fail because an it is impossible to dissolve
        the element. For example a poi can only be dissolved when nothing is attached to it.

        For now this function only works on AXIS

        """

        if isinstance(node, str):
            node=  self[node]

        if not type(node) == Axis:
            raise TypeError('Only nodes of type Axis can be dissolved at this moment')

        for d in self.nodes_depending_on(node):
            self[d].change_parent_to(node.parent)

        self.delete(node)



    # ========= The most important functions ========

    def update(self):
        """Updates the interface between the nodes and the core. This includes the re-calculation of all forces,
        buoyancy positions, ballast-system cogs etc.
        """
        for n in self._nodes:
            n.update()
        self._vfc.state_update()

    def solve_statics(self, silent=False, timeout = None):
        """Solves statics

        Args:
            silent: Do not print if successfully solved

        Returns:
            bool: True if successful, False otherwise.

        """
        self.update()
        if timeout is None:
            succes = self._vfc.state_solve_statics()
        else:
            succes = self._vfc.state_solve_statics_with_timeout(timeout, False)

        if self.verify_equilibrium():
            if not silent:
                self._print("Solved to {}.".format(self._vfc.Emaxabs))
            return True

        d = np.array(self._vfc.get_dofs())
        if np.any(np.abs(d)>2000):
            print("Error: One of the degrees of freedom exceeded the boundary of 2000 [m]/[rad].")
            return False

        return False

    def verify_equilibrium(self, tol = 1e-2):
        """Checks if the current state is an equilibrium

        Returns:
            bool: True if successful, False if not an equilibrium.

        """
        self.update()
        return (self._vfc.Emaxabs < tol)



    # ====== goal seek ========

    def goal_seek(self, evaluate, target, change_node, change_property, bracket=None, tol=1e-3):
        """goal_seek

        Goal seek is the classic goal-seek. It changes a single property of a single node in order to get
        some property of some node to a specified value. Just like excel.

        Args:
            evaluate : code to be evaluated to yield the value that is solved for. Eg: s['poi'].fx Scene is abbiviated as "s"
            target (number):       target value for that property
            change_node(Node or str):  node to be adjusted
            change_property (str): property of that node to be adjusted
            range(optional)  : specify the possible search-interval

        Returns:
            bool: True if successful, False otherwise.

        Examples:
            Change the y-position of the cog of a rigid body ('Barge')  in order to obtain zero roll (rx)
            >>> s.goal_seek("s['Barge'].fx",0,'Barge','cogy')

        """
        s = self

        change_node = self._node_from_node_or_str(change_node)

        # check that the attributes exist and are single numbers
        test = eval(evaluate)

        try:
            float(test)
        except:
            raise ValueError('Evaluation of {} does not result in a float')

        self._print('Attempting to evaluate {} to {} (now {})'.format(evaluate, target, test))

        initial = getattr(change_node, change_property)
        self._print('By changing the value of {}.{} (now {})'.format(change_node.name, change_property, initial))

        def set_and_get(x):
            setattr(change_node, change_property,x)
            self.solve_statics(silent=True)
            s = self
            result = eval(evaluate)
            self._print('setting {} results in {}'.format(x,result))
            return result-target

        from scipy.optimize import root_scalar
        x0 = initial
        x1 = initial+0.0001

        if bracket is not None:
            res = root_scalar(set_and_get, x0=x0, x1=x1, bracket=bracket,xtol = tol)
        else:
            res = root_scalar(set_and_get, x0=x0, x1=x1,xtol = tol)

        self._print(res)

        # evaluate result
        final_value = eval(evaluate)
        if abs(final_value-target) > 1e-3:
            raise ValueError("Target not reached. Target was {}, reached value is {}".format(target, final_value))


        return True


    def plot_effect(self, evaluate, change_node, change_property, start, to, steps):
        """Produces a 2D plot with the relation between two properties of the scene. For example the length of a cable
        versus the force in another cable.

        The evaluate argument is processed using "eval" and may contain python code. This may be used to combine multiple
        properties to one value. For example calculate the diagonal load distribution from four independent loads.

        The plot is produced using matplotlob. The plot is produced in the current figure (if any) and plt.show is not executed.

        Args:
            evaluate (str): code to be evaluated to yield the value on the y-axis. Eg: s['poi'].fx Scene is abbiviated as "s"
            change_node(Node or str):  node to be adjusted
            change_property (str): property of that node to be adjusted
            start : left side of the interval
            to : right side of the interval
            steps : number of steps in the interval

        Returns:
            Tuple (x,y) with x and y coordinates

        Examples:
            >>> s.plot_effect("s['cable'].tension", "cable", "length", 11, 14, 10)
            >>> import matplotlib.pyplot as plt
            >>> plt.show()

        """
        s=self
        change_node = self._node_from_node_or_str(change_node)

        # check that the attributes exist and are single numbers
        test = eval(evaluate)

        try:
            float(test)
        except:
            raise ValueError('Evaluation of {} does not result in a float')

        def set_and_get(x):
            setattr(change_node, change_property,x)
            self.solve_statics(silent=True)
            s = self
            result = eval(evaluate)
            self._print('setting {} results in {}'.format(x,result))
            return result

        xs = np.linspace(start,to,steps)
        y = []
        for x in xs:
            y.append(set_and_get(x))

        y = np.array(y)
        import matplotlib.pyplot as plt
        plt.plot(xs,y)
        plt.xlabel('{} of {}'.format(change_property, change_node.name))
        plt.ylabel(evaluate)

        return (xs,y)


    # ======== create functions =========

    def new_axis(self, name, parent=None, position=None, rotation=None, inertia=None, inertia_radii=None, fixed = True):
        """Creates a new *axis* node and adds it to the scene.

        Args:
            name: Name for the node, should be unique
            parent: optional, name of the parent of the node
            position: optional, position for the node (x,y,z)
            rotation: optional, rotation for the node (rx,ry,rz)
            fixed [True]: optional, determines whether the axis is fixed [True] or free [False]. May also be a sequence of 6 booleans.

        Returns:
            Reference to newly created axis

        """

        # apply prefixes
        name = self._prefix_name(name)

        # first check
        assertValidName(name)
        self._verify_name_available(name)
        b = self._parent_from_node(parent)

        if position is not None:
            assert3f(position, "Position ")
        if rotation is not None:
            assert3f(rotation, "Rotation ")

        if inertia is not None:
            assert1f_positive(inertia, "inertia ")

        if inertia_radii is not None:
            assert3f_positive(inertia_radii, "Radii of inertia")
            assert inertia is not None, ValueError("Can not set radii of gyration without specifying inertia")


        if not isinstance(fixed, bool):
            if len(fixed) != 6:
                raise Exception('"fixed" parameter should either be True/False or a 6x bool sequence such as (True,True,False,False,True,False)')



        # then create
        a = self._vfc.new_axis(name)

        new_node = Axis(self, a)

        # and set properties
        if b is not None:
            new_node.parent = b
        if position is not None:
            new_node.position = position
        if rotation is not None:
            new_node.rotation = rotation
        if inertia is not None:
            new_node.inertia = inertia
        if inertia_radii is not None:
            new_node.inertia_radii = inertia_radii


        if isinstance(fixed, bool):
            if fixed:
                new_node.set_fixed()
            else:
                new_node.set_free()
        else:
            new_node.fixed = fixed


        self._nodes.append(new_node)
        return new_node

    def new_waveinteraction(self, name, path, parent=None, offset=None,):
            """Creates a new *wave interaction* node and adds it to the scene.

            Args:
                name: Name for the node, should be unique
                path: Path to the hydrodynamic database
                parent: optional, name of the parent of the node
                offset: optional, position for the node (x,y,z)

            Returns:
                Reference to newly created wave-interaction object

            """

            if not parent:
                raise ValueError('Wave-interaction has to be located on an Axis')

            # apply prefixes
            name = self._prefix_name(name)

            # first check
            assertValidName(name)
            self._verify_name_available(name)
            b = self._parent_from_node(parent)

            if b is None:
                raise ValueError('Wave-interaction has to be located on an Axis')

            if offset is not None:
                assert3f(offset, "Offset ")

            self.get_resource_path(path)  # raises error when resource is not found

            # then create

            new_node = WaveInteraction1(self)

            new_node.name = name
            new_node.path = path
            new_node.parent = parent

            # and set properties
            new_node.parent = b
            if offset is not None:
                new_node.offset = offset

            self._nodes.append(new_node)
            return new_node

    def new_visual(self, name, path, parent=None, offset=None, rotation=None, scale = None):
        """Creates a new *Visual* node and adds it to the scene.

        Args:
            name: Name for the node, should be unique
            path: Path to the resource
            parent: optional, name of the parent of the node
            offset: optional, position for the node (x,y,z)
            rotation: optional, rotation for the node (rx,ry,rz)
            scale : optional, scale of the visual (x,y,z).

        Returns:
            Reference to newly created visual

        """

        # apply prefixes
        name = self._prefix_name(name)

        # first check
        assertValidName(name)
        self._verify_name_available(name)
        b = self._parent_from_node(parent)

        if offset is not None:
            assert3f(offset, "Offset ")
        if rotation is not None:
            assert3f(rotation, "Rotation ")

        self.get_resource_path(path) # raises error when resource is not found


        # then create

        new_node = Visual(self)

        new_node.name = name
        new_node.path = path
        new_node.parent = parent

        # and set properties
        if b is not None:
            new_node.parent = b
        if offset is not None:
            new_node.offset = offset
        if rotation is not None:
            new_node.rotation = rotation
        if scale is not None:
            new_node.scale = scale

        self._nodes.append(new_node)
        return new_node


    def new_poi(self, name, parent=None, position=None):
        """Creates a new *poi* node and adds it to the scene.

        Args:
            name: Name for the node, should be unique
            parent: optional, name of the parent of the node
            position: optional, position for the node (x,y,z)


        Returns:
            Reference to newly created poi

        """

        # apply prefixes
        name = self._prefix_name(name)

        # first check
        assertValidName(name)
        self._verify_name_available(name)
        b = self._parent_from_node(parent)

        if position is not None:
            assert3f(position, "Position ")

        # then create
        a = self._vfc.new_poi(name)

        new_node = Poi(self, a)

        # and set properties
        if b is not None:
            new_node.parent = b
        if position is not None:
            new_node.position = position

        self._nodes.append(new_node)
        return new_node

    def new_rigidbody(self, name, mass=0, cog=(0, 0, 0),
                      parent=None, position=None, rotation=None, inertia_radii=None, fixed = True ):
        """Creates a new *rigidbody* node and adds it to the scene.

        Args:
            name: Name for the node, should be unique
            mass: optional, [0] mass in mT
            cog: optional, (0,0,0) cog-position in (m,m,m)
            parent: optional, name of the parent of the node
            position: optional, position for the node (x,y,z)
            rotation: optional, rotation for the node (rx,ry,rz)
            inertia_radii : optional, radii of gyration (rxx,ryy,rzz); only used for dynamics
            fixed [True]: optional, determines whether the axis is fixed [True] or free [False]. May also be a sequence of 6 booleans.

        Examples:
            scene.new_rigidbody("heavy_thing", mass = 10000, cog = (1.45, 0, -0.7))

        Returns:
            Reference to newly created RigidBody

        """

        # apply prefixes
        name = self._prefix_name(name)

        # check input
        assertValidName(name)
        self._verify_name_available(name)
        b = self._parent_from_node(parent)

        if position is not None:
            assert3f(position, "Position ")
        if rotation is not None:
            assert3f(rotation, "Rotation ")
            
        if inertia_radii is not None:
            assert3f_positive(inertia_radii, "Radii of inertia")
            assert mass>0, ValueError("Can not set radii of gyration without specifying mass")

        if not isinstance(fixed, bool):
            if len(fixed) != 6:
                raise Exception('"fixed" parameter should either be True/False or a 6x bool sequence such as (True,True,False,False,True,False)')


        # make elements

        a = self._vfc.new_axis(name)

        p = self._vfc.new_poi(name + vfc.VF_NAME_SPLIT + "cog")
        p.parent = a
        p.position = cog

        g = self._vfc.new_force(name + vfc.VF_NAME_SPLIT + "gravity")
        g.parent = p
        g.force = (0, 0, -vfc.G * mass)

        r = RigidBody(self, a, p, g)

        r.cog = cog  # set inertia
        r.mass = mass

        # and set properties
        if b is not None:
            r.parent = b
        if position is not None:
            r.position = position
        if rotation is not None:
            r.rotation = rotation
            
        if inertia_radii is not None:
            r.inertia_radii = inertia_radii

        if isinstance(fixed, bool):
            if fixed:
                r.set_fixed()
            else:
                r.set_free()
        else:
            r.fixed = fixed

        self._nodes.append(r)
        return r

    def new_cable(self, name, poiA, poiB, length=-1, EA=0, diameter=0, sheaves=None):
        """Creates a new *cable* node and adds it to the scene.

        Args:
            name: Name for the node, should be unique
            poiA : A Poi element to connect the first end of the cable to
            poiB : A Poi element to connect the other end of the cable to
            length [-1] : un-stretched length of the cable in m; default [-1] create a cable with the current distance between the endpoints A and B
            EA [0] : stiffness of the cable in kN/m; default

            sheaves : [optional] A list of pois, these are sheaves that the cable runs over. Defined from poiA to poiB

        Examples:

            scene.new_cable('cable_name' poiA='poi_start', poiB = 'poi_end')  # minimal use

            scene.new_cable('cable_name', length=50, EA=1000, poiA=poi_start, poiB = poi_end, sheaves=[sheave1, sheave2])

            scene.new_cable('cable_name', length=50, EA=1000, poiA='poi_start', poiB = 'poi_end', sheaves=['single_sheave']) # also a single sheave needs to be provided as a list

        Notes:
            The default options for length and EA can be used to measure distances between points

        Returns:
            Reference to newly created Cable

        """

        # apply prefixes
        name = self._prefix_name(name)

        # first check
        assertValidName(name)
        self._verify_name_available(name)
        assert1f(length, 'length')
        assert1f(EA, 'EA')

        poiA = self._poi_from_node(poiA)
        poiB = self._poi_from_node(poiB)

        pois = [poiA]
        if sheaves is not None:

            if isinstance(sheaves, Poi): # single sheave as poi or string
                sheaves = [sheaves]

            if isinstance(sheaves, Sheave): # single sheave as poi or string
                sheaves = [sheaves]


            if isinstance(sheaves, str):
                sheaves = [sheaves]


            for s in sheaves:
                # s may be a poi or a sheave
                pois.append(self._poi_or_sheave_from_node(s))


        pois.append(poiB)

        # default options
        if length == -1:
            length = np.linalg.norm(np.array(poiA.global_position) - np.array(poiB.global_position))

            if length<1e-9:
                raise Exception('Length not provided and endpoints are at the same global position. Can not determine a suitable default length (>0)')



        # more checks
        if length<1e-9:
            raise Exception('Length should be more than 0')

        if EA<0:
            raise Exception('EA should be more than 0')

        assert1f(diameter, "Diameter should be a number >= 0")

        if diameter<0:
            raise Exception("Diameter should be >= 0")

        # then create
        a = self._vfc.new_cable(name)
        new_node = Cable(self, a)
        new_node.length = length
        new_node.EA = EA
        new_node.diameter = diameter

        for poi in pois:
            new_node.add_connection(poi)

        # and add to the scene
        self._nodes.append(new_node)
        return new_node

    def new_force(self, name, parent=None, force=None, moment=None):
        """Creates a new *force* node and adds it to the scene.

        Args:
            name: Name for the node, should be unique
            parent: name of the parent of the node [Poi]
            force: optional, global force on the node (x,y,z)
            moment: optional, global force on the node (x,y,z)


        Returns:
            Reference to newly created force

        """

        # apply prefixes
        name = self._prefix_name(name)

        # first check
        assertValidName(name)
        self._verify_name_available(name)
        b = self._poi_from_node(parent)

        if force is not None:
            assert3f(force, "Force ")

        if moment is not None:
            assert3f(moment, "Moment ")


        # then create
        a = self._vfc.new_force(name)

        new_node = Force(self, a)

        # and set properties
        if b is not None:
            new_node.parent = b
        if force is not None:
            new_node.force = force
        if moment is not None:
            new_node.moment = moment

        self._nodes.append(new_node)
        return new_node

    def new_sheave(self, name, parent, axis, radius=0):
        """Creates a new *sheave* node and adds it to the scene.

        Args:
            name: Name for the node, should be unique
            parent: name of the parent of the node [Poi]
            axis: direction of the axis of rotation (x,y,z)
            radius: optional, radius of the sheave


        Returns:
            Reference to newly created sheave

        """

        # apply prefixes
        name = self._prefix_name(name)

        # first check
        assertValidName(name)
        self._verify_name_available(name)
        b = self._poi_from_node(parent)

        assert3f(axis, "Axis of rotation ")

        assert1f(radius, "Radius of sheave")

        # then create
        a = self._vfc.new_sheave(name)

        new_node = Sheave(self, a)

        # and set properties
        new_node.parent = b
        new_node.axis = axis
        new_node.radius = radius

        self._nodes.append(new_node)
        return new_node

    def new_hydspring(self, name, parent, cob,
                      BMT, BML, COFX, COFY, kHeave, waterline, displacement_kN):
        """Creates a new *hydspring* node and adds it to the scene.

        Args:
            name: Name for the node, should be unique
            parent: name of the parent of the node [Axis]
            cob: position of the CoB (x,y,z) in the parent axis system
            BMT: Vertical distance between CoB and meta-center for roll
            BML: Vertical distance between CoB and meta-center for pitch
            COFX: X-location of center of flotation (center of waterplane) relative to CoB
            COFY: Y-location of center of flotation (center of waterplane) relative to CoB
            kHeave : heave stiffness (typically Awl * rho * g)
            waterline : Z-position (elevation) of the waterline relative to CoB
            displacement_kN : displacement (typically volume * rho * g)


        Returns:
            Reference to newly created hydrostatic spring

        """

        # apply prefixes
        name = self._prefix_name(name)

        # first check
        assertValidName(name)
        self._verify_name_available(name)
        b = self._parent_from_node(parent)
        assert3f(cob, "CoB ")
        assert1f(BMT, "BMT ")
        assert1f(BML, "BML ")
        assert1f(COFX, "COFX ")
        assert1f(COFY, "COFY ")
        assert1f(kHeave, "kHeave ")
        assert1f(waterline, "waterline ")
        assert1f(displacement_kN, "displacement_kN ")

        # then create
        a = self._vfc.new_hydspring(name)
        new_node = HydSpring(self, a)

        new_node.cob = cob
        new_node.parent = b
        new_node.BMT = BMT
        new_node.BML = BML
        new_node.COFX = COFX
        new_node.COFY = COFY
        new_node.kHeave = kHeave
        new_node.waterline = waterline
        new_node.displacement_kN = displacement_kN

        self._nodes.append(new_node)

        return new_node

    def new_linear_connector_6d(self, name, slave, master, stiffness = None):
        """Creates a new *linear connector 6d* node and adds it to the scene.

        Args:
            name: Name for the node, should be unique
            slave: Slaved axis system [Axis]
            master: Master axis system [Axis]
            stiffness: optional, connection stiffness (x,y,z, rx,ry,rz)

        See :py:class:`LC6d` for details

        Returns:
            Reference to newly created connector

        """

        # apply prefixes
        name = self._prefix_name(name)

        # first check
        assertValidName(name)
        self._verify_name_available(name)
        m = self._parent_from_node(master)
        s = self._parent_from_node(slave)

        if stiffness is not None:
            assert6f(stiffness, "Stiffness ")
        else:
            stiffness = (0,0,0,0,0,0)

        # then create
        a = self._vfc.new_linearconnector6d(name)

        new_node = LC6d(self, a)

        # and set properties
        new_node.master = m
        new_node.slave = s
        new_node.stiffness = stiffness

        self._nodes.append(new_node)
        return new_node

    def new_connector2d(self, name, master, slave, k_linear=0, k_angular=0):
        """Creates a new *new_connector2d* node and adds it to the scene.

        Args:
            name: Name for the node, should be unique
            slave: Slaved axis system [Axis]
            master: Master axis system [Axis]

            k_linear : linear stiffness in kN/m
            k_angular : angular stiffness in kN*m / rad

        Returns:
            Reference to newly created connector2d

        """

        # apply prefixes
        name = self._prefix_name(name)

        # first check
        assertValidName(name)
        self._verify_name_available(name)
        m = self._parent_from_node(master)
        s = self._parent_from_node(slave)

        assert1f(k_linear, "Linear stiffness")
        assert1f(k_angular, "Angular stiffness")

        # then create
        a = self._vfc.new_connector2d(name)

        new_node = Connector2d(self, a)

        # and set properties
        new_node.master = m
        new_node.slave = s
        new_node.k_linear = k_linear
        new_node.k_angular = k_angular

        self._nodes.append(new_node)
        return new_node

    def new_linear_beam(self, name, master, slave, EIy=0, EIz=0, GIp=0, EA=0, L=None):
        """Creates a new *linear beam* node and adds it to the scene.

        Args:
            name: Name for the node, should be unique
            slave: Slaved axis system [Axis]
            master: Master axis system [Axis]

            All stiffness terms default to 0
            The length defaults to the distance between master and slave


        See :py:class:`LinearBeam` for details

        Returns:
            Reference to newly created beam

        """

        # apply prefixes
        name = self._prefix_name(name)

        # first check
        assertValidName(name)
        self._verify_name_available(name)
        m = self._parent_from_node(master)
        s = self._parent_from_node(slave)

        if L is None:
            L = np.linalg.norm(np.array(m.global_position)- np.array(s.global_position))
        else:
            if L <= 0:
                raise ValueError('L should be > 0 as stiffness is defined per length.')


        # then create
        a = self._vfc.new_linearbeam(name)

        new_node = LinearBeam(self, a)

        # and set properties
        new_node.master = m
        new_node.slave = s
        new_node.EIy = EIy
        new_node.EIz = EIz
        new_node.GIp = GIp
        new_node.EA = EA
        new_node.L = L

        self._nodes.append(new_node)
        return new_node


    def new_buoyancy(self, name, parent=None):
        """Creates a new *poi* node and adds it to the scene.

        Args:
            name: Name for the node, should be unique
            parent: optional, name of the parent of the node
            trimesh: optional, TriMesh object


        Returns:
            Reference to newly created buoyancy

        """

        # apply prefixes
        name = self._prefix_name(name)

        # first check
        assertValidName(name)
        self._verify_name_available(name)
        b = self._parent_from_node(parent)

        # then create
        a = self._vfc.new_buoyancy(name)
        new_node = Buoyancy(self, a)

        # and set properties
        if b is not None:
            new_node.parent = b

        self._nodes.append(new_node)
        return new_node

    def new_ballastsystem(self, name, parent=None, position=None):
        """Creates a new *rigidbody* node and adds it to the scene.

        Args:
            name: Name for the node, should be unique
            parent: name of the parent of the ballast system (ie: the vessel axis system)
            position: the reference system in which the tanks are defined [0,0,0]

        Examples:
            scene.new_ballastsystem("cheetah_ballast", parent="Cheetah")

        Returns:
            Reference to newly created BallastSystem

        """

        # apply prefixes
        name = self._prefix_name(name)

        # check input
        assertValidName(name)
        self._verify_name_available(name)
        b = self._parent_from_node(parent)

        parent = self._parent_from_node(parent) # handles verification of type as well

        if position is not None:
            assert3f(position, "Position ")

        # make elements

        p = self._vfc.new_poi(name)

        g = self._vfc.new_force(name + vfc.VF_NAME_SPLIT + "gravity")
        g.parent = p
        g.force = (0, 0, 0)

        r = BallastSystem(self, p, g)

        # and set properties
        r.parent = parent

        if position is not None:
            r.position = position

        self._nodes.append(r)
        return r

    def print_python_code(self):
        """Prints the python code that generates the current scene

        See also: give_python_code
        """
        for line in self.give_python_code().split('\n'):
            print(line)

    def give_python_code(self):
        """Generates the python code that rebuilds the scene and elements in its current state."""

        import datetime
        import getpass

        self.sort_nodes_by_dependency()

        code = "# auto generated pyhton code"
        try:
            code += "\n# By {}".format(getpass.getuser())
        except:
            code += "\n# By an unknown"

        code += "\n# Time: {} UTC".format(str(datetime.datetime.now()).split('.')[0])

        code += "\n\n# To be able to distinguish the important number (eg: fixed positions) from"
        code += "\n# non-important numbers (eg: a position that is solved by the static solver) we use a dummy-function called 'solved'."
        code += "\n# For anything written as solved(number) that actual number does not influence the static solution"
        code += "\ndef solved(number):\n    return number\n"

        for n in self._nodes:
            code += '\n' + n.give_python_code()

        return code

    def save_scene(self, filename):
        """Saves the scene to a file

        This saves the scene in its current state to a file.
        Opening the saved file will reproduce exactly this scene.

        This sounds nice, but beware that it only saves the resulting model, not the process of creating the model.
        This means that if you created the model in a parametric fashion or assembled the model from other models then these are not re-evaluated when the model is openened again.
        So lets say this model uses a sub-model of a lifting hook which is imported from another file. If that other file is updated then
        the results of that update will not be reflected in the saved model.

        If no path is present in the file-name then the model will be saved in the last (lowest) resource-path (if any)

        Args:
            filename : filename or file-path to save the file. Default extension is .dave_asset

        Returns:
            the full path to the saved file

        """

        code = self.give_python_code()

        filename = Path(filename)

        # add .dave extension if needed
        if filename.suffix != '.dave':
            filename = Path(str(filename) + '.dave')

        # add path if not provided
        if not filename.is_absolute():
            try:
                filename = Path(self.resources_paths[-1]) / filename
            except:
                pass # save in current folder

        # make sure directory exists
        directory = filename.parent
        if not directory.exists():
            directory.mkdir()

        f = open(filename,'w+')
        f.write(code)
        f.close()

        self._print('Saved as {}'.format(filename))

        return filename

    def print_node_tree(self):

        self.sort_nodes_by_dependency()

        to_be_printed = []
        for n in self._nodes:
            to_be_printed.append(n.name)

        # to_be_printed.reverse()

        def print_deps(name, spaces):

            node = self[name]
            deps = self.nodes_with_parent(node)
            print(spaces + name + ' [' + str(type(node)).split('.')[-1][:-2] + ']')

            if deps is not None:
                for dep in deps:
                    if spaces == "":
                        spaces_plus = ' |-> '
                    else:
                        spaces_plus = ' |   ' + spaces
                    print_deps(dep, spaces_plus)

            to_be_printed.remove(name)

        while to_be_printed:
            name = to_be_printed[0]
            print_deps(name, '')

    def load_scene(self, filename = None):
        """Loads the contents of filename into the current scene.

        This function is typically used on an empty scene.

        Filename is appended with .dave if needed.
        File is searched for in the resource-paths.

        See also: import scene"""

        if filename is None:
            raise Exception('Please provide a file-name')

        filename = Path(filename)

        if filename.suffix != '.dave':
            filename = Path(str(filename) + '.dave')

        filename = self.get_resource_path(filename)

        print('Loading {}'.format(filename))

        f = open(file=filename, mode = 'r')
        s = self
        code = ''

        for line in f:
            code += line + '\n'

        exec(code, {}, {'s': s})

    def import_scene(self, other, prefix = "", containerize = True):
        """Copy-paste all nodes of scene "other" into current scene.

        To avoid double names it is recommended to use a prefix. This prefix will be added to all element names.

        Returns:
            Contained (Axis-type Node) : if the imported scene is containerized then a reference to the created container is returned.
        """

        if isinstance(other, Path):
            other = str(other)

        if isinstance(other, str):
            other = Scene(other)

        if not isinstance(other, Scene):
            raise TypeError('Other should be a Scene but is a ' + str(type(other)))

        old_prefix = self._name_prefix
        imported_element_names = []

        for n in other._nodes:
            imported_element_names.append(prefix + n.name)


        # check for double names

        for new_node_name in imported_element_names:
            if not self.name_available(new_node_name):
                raise NameError('An element with name "{}" is already present. Please use a prefix to avoid double names'.format(new_node_name))


        self._name_prefix = prefix

        code = other.give_python_code()

        s = self
        exec(code)

        self._name_prefix = old_prefix # restore

        # Move all imported elements without a parent into a newly created axis system
        if containerize:

            container_name = s.available_name_like('import_container')

            c = self.new_axis(prefix + container_name)

            for name in imported_element_names:

                node = self[name]
                if not isinstance(node, NodeWithParent):
                    continue

                if node.parent is None:
                    node.change_parent_to(c)

            return c

        return None

    def copy(self):
        """Creates a full and independent copy of the scene and returns it.

        Example:
            s = Scene()
            c = s.copy()
            c.new_axis('only in c')

        """

        c = Scene()
        c.import_scene(self)
        return c



    # =================== DYNAMICS ==================

    def dynamics_M(self,delta = 0.1):
        """Returns the mass matrix of the scene"""
        self.update()
        return self._vfc.M(delta)

    def dynamics_K(self, delta):
        """Returns the stiffness matrix of the scene for a perturbation of delta """
        self.update()
        return -self._vfc.K(delta)

    def dynamics_nodes(self):
        """Returns a list of nodes associated with the rows/columns of M and K"""
        self.update()
        nodes = self._vfc.get_dof_elements()
        r = [self[n.name] for n in nodes]
        return r

    def dynamics_modes(self):
        """Returns a list of nodes associated with the rows/columns of M and K"""
        self.update()
        return self._vfc.get_dof_modes()




