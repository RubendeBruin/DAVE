Scene and nodes
================

How to set-up a scene using code
---------------------------------

This is the main module of the engine. It contains both the nodes and the scene.

    A node is an item or element in a model. For example a ship or a force.
    A Scene is a collection of nodes.

    The common way of working is as follows:

    1. Create a scene
    2. Add nodes to it

    Example:

    ::

        s = Scene()                               # create an empty scene
        s.new_poi('point 1')                      # creates a poi with name anchor
        s.new_poi('point 2', position = (10,0,0)) # create a second poi at x=10
        s.new_cable('line',poiA = 'point 1', poiB = 'point 2') # creates a cable between the two points
        s.save_scene(r'test.dave')                # save to file


    Nodes in a scene can be referenced by either name or by reference.
    The new_some_node_type functions return a reference to the newly created node.

    ::

        s = Scene()
        a = s.new_axis('axis')                     # a is now a reference to node 'axis'

        p1 = s.new_poi('poi_1', parent = a )       # refer by reference
        p2 = s.new_poi('poi_2', parent = 'axis' )  # refer by name


    A reference to a node can also be obtained from the scene using square brackets:

    ::

        s = Scene()
        s.new_axis('axis')

        a = s['axis']
        print(a.position)




Node types
------------

The following node types can be used:

.. list-table:: Node-types
   :widths: 10 20 70
   :header-rows: 1

   * - Icon
     - Type
     - Description

   * - **Geometry**
     -
     -

   * - .. image:: ../images/axis.png
          :width: 28 px
          :height: 28 px
     - :py:class:`Axis`  :py:func:`Scene.new_axis`
     - Axis is an local axis system.
       This is the main building block of the geometry.

   * - .. image:: ../images/poi.png
          :width: 28 px
          :height: 28 px
     - :py:class:`Poi`
       :py:func:`Scene.new_poi`
     - Point of interest is a position on an axis system.
       Used as connection point or reference point for other nodes.

   * - .. image:: ../images/cube.png
          :width: 28 px
          :height: 28 px
     - :py:class:`RigidBody`
       :py:func:`Scene.new_rigidbody`
     - This is a rigid body with a mass and cog.It creates its own axis system (it is a super-set of Axis)

   * - **Connections**
     -
     -

   * - .. image:: ../images/cable.png
          :width: 28 px
          :height: 28 px
     - :py:class:`DAVE.Scene.Cable`
       :py:func:`Scene.new_cable`
     - Linear elastic cable between two or more pois

   * - .. image:: ../images/beam.png
          :width: 28 px
          :height: 28 px
     - :py:class:`LinearBeam`
       :py:func:`Scene.new_linear_beam`
     - Linear elastic beam between two or more pois

   * - .. image:: ../images/lincon6.png
          :width: 28 px
          :height: 28 px
     - :py:class:`LC6d`
       :py:func:`Scene.new_linear_connector_6d`
     - Connects two axis systems with six linear springs

   * - .. image:: ../images/con2d.png
          :width: 28 px
          :height: 28 px
     - :py:class:`Connector2d`
       :py:func:`Scene.new_connector2d`
     - Connects two axis systems with one rotational and one translational spring

   * - **Forces**
     -
     -

   * - .. image:: ../images/force.png
          :width: 28 px
          :height: 28 px
     - :py:class:`Force`
       :py:func:`Scene.new_force`
     - This is a force/moment. If is defined in the global axis system and acts on a poi

   * - .. image:: ../images/linhyd.png
          :width: 28 px
          :height: 28 px
     - :py:class:`HydSpring`
       :py:func:`Scene.new_hydspring`
     - Create linear springs to model linearized hydrostatics

   * - .. image:: ../images/trimesh.png
          :width: 28 px
          :height: 28 px
     - :py:class:`Buoyancy`
       :py:func:`Scene.new_buoyancy`
     - Buoyancy mesh for non-linear, shape-based hydrostatics

   * - **Other**
     -
     -

   * - .. image:: ../images/visual.png
          :width: 28 px
          :height: 28 px
     - :py:class:`Visual`
       :py:func:`Scene.new_visual`
     - 3D visual to spice-up the looks of the scene

   * - .. image:: ../images/trimesh.png
          :width: 28 px
          :height: 28 px
     - :py:class:`TriMeshSource`
       :py:func:`Buoyancy.trimesh`
     - 3D triangulated mesh for buoyancy calculations. Automatically created when a Bouyancy node is added.


Geometry is build using Axis systems, Rigid bodies and Pois.

Axis systems and rigid bodies have a position and an orientation.
Pois only have a position

All can be positioned on a parent. If a node has a parent then this means that its position and orientation are expressed relative to that parent.

Axis and RigidBodies can have all their six individual degrees of freedom either fixed or free. If a degree of freedom is free then this means that the
node is able to move/rotate in this degree of freedom.

If this is the first time you read this then please use the Gui to experiment.


Scene functions
----------------

Apart from methods to create nodes, Scene also harbours functionality to delete, import, re-order and export nodes.


.. list-table:: Scene functions
   :widths: 30 20 40
   :header-rows: 1

   * - Action
     - How
     - Description

   * - Create a new scene
     - `s = Scene()`
     - Creates a new scene "s". Optionally a file-name can be provided to load the contents of that file directly into the scene

   * - **Adding content**
     -
     -

   * - Adding a node
     - `s.new_poi, s.new_axis, etc..`
     - See list of node types and new_ functions in the next table.

   * - Import nodes (1)
     - :py:func:`Scene.import_scene`
     - Imports all nodes from an other scene and places them as a group in the current scene.

   * - Import nodes (2)
     - :py:func:`Scene.load_scene`
     - Imports all nodes from an other scene and adds them to the current scene. Beware of name-conflicts.

   * - **Access nodes**
     -
     -

   * - Get a node
     - `s['node_name']`
     - gets a reference to a node with name "node_name".

   * - Get all nodes of a type
     - :py:func:`Scene.nodes_of_type`
     - gets a list of reference to all nodes with this type

   * - Get all nodes that depend on
     - :py:func:`Scene.nodes_depending_on`
     - gets a list of reference to all nodes with this type

   * - Get all child nodes
     - :py:func:`Scene.nodes_with_parent`
     - gets a list of reference to all nodes with this type


   * - **Deleting content**
     -
     -

   * - clear
     - :py:func:`Scene.clear`
     - Deletes all nodes from the scene

   * - delete
     - :py:func:`Scene.delete`
     - Deletes a node from the scene. All nodes that depend on this node will be deleted as well.

   * - dissolve
     - :py:func:`Scene.dissolve`
     - Removes a single node from the scene. Attempts to maintain child nodes. Often used in combination with import

   * - **Saving or exporting**
     -
     -

   * - Save to file
     - :py:func:`Scene.save_scene`
     - Saves the content of the scene to a file

   * - Get as python code
     - :py:func:`Scene.give_python_code`
     - Returns python to re-create the scene in its current state.

   * - Print node-tree
     - :py:func:`Scene.print_node_tree`
     - Prints a node-tree

   * - **Solving**
     -
     -

   * - Solve statics
     - :py:func:`Scene.solve_statics`
     - Brings the nodes in the scene to a static equilibrium

   * - Goal seek
     - :py:func:`Scene.goal_seek`
     - Iteratively changes a property to set another property to some specified value.


Notes:
rotations are defined as https://en.wikipedia.org/wiki/Axis%E2%80%93angle_representation#Rotation_vector