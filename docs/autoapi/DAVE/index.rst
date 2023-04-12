:mod:`DAVE`
===========

.. py:module:: DAVE


Subpackages
-----------
.. toctree::
   :titlesonly:
   :maxdepth: 3

   gui/index.rst
   jupyter/index.rst


Submodules
----------
.. toctree::
   :titlesonly:
   :maxdepth: 1

   auto_download/index.rst
   frequency_domain/index.rst
   marine/index.rst
   rigging/index.rst
   run_gui/index.rst
   scene/index.rst
   settings/index.rst
   tools/index.rst
   visual/index.rst


Package Contents
----------------

.. data:: dist_name
   

   

.. py:class:: Node(scene)

   ABSTRACT CLASS - Properties defined here are applicable to all derived classes
   Master class for all nodes

   .. attribute:: _scene
      :annotation: :Scene

      reference to the scene that the node lives is


   .. attribute:: _name
      :annotation: :str = no name

      Unique name of the node


   .. attribute:: _manager
      :annotation: :Node or None

      Reference to a node that controls this node


   .. method:: __repr__(self)



   .. method:: __str__(self)



   .. method:: depends_on(self)


      Returns a list of nodes that need to be available before the node can be created


   .. method:: give_python_code(self)


      Returns the python code that can be executed to re-create this node


   .. method:: manager(self)
      :property:



   .. method:: _verify_change_allowed(self)


      Changing the state of a node is only allowed if either:
      1. the node is not manages (node._manager is None)
      2. the manager of the node is identical to scene.current_manager


   .. method:: name(self)
      :property:


      Name of the node (str), must be unique


   .. method:: _delete_vfc(self)



   .. method:: update(self)


      Performs internal updates relevant for physics. Called before solving statics or getting results



.. py:class:: CoreConnectedNode(scene, vfNode)

   Bases: :class:`DAVE.scene.Node`

   ABSTRACT CLASS - Properties defined here are applicable to all derived classes
   Master class for all nodes with a connected eqCore element

   .. method:: name(self)
      :property:


      Name of the node (str), must be unique


   .. method:: _delete_vfc(self)




.. py:class:: NodeWithParent(scene, vfNode)

   Bases: :class:`DAVE.scene.CoreConnectedNode`

   NodeWithParent

   Do not use this class directly.
   This is a base-class for all nodes that have a "parent" property.

   .. method:: depends_on(self)



   .. method:: parent(self)
      :property:


      Determines the parent of the node. Should be another axis or None


   .. method:: change_parent_to(self, new_parent)


      Assigns a new parent to the node but keeps the global position and rotation the same.

      See also: .parent (property)

      :param new_parent: new parent node



.. py:class:: Visual(scene)

   Bases: :class:`DAVE.scene.Node`

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

   .. attribute:: offset
      :annotation: = [0, 0, 0]

      Offset (x,y,z) of the visual. Offset is applied after scaling


   .. attribute:: rotation
      :annotation: = [0, 0, 0]

      Rotation (rx,ry,rz) of the visual


   .. attribute:: scale
      :annotation: = [1, 1, 1]

      Scaling of the visual. Scaling is applied before offset.


   .. attribute:: path
      :annotation: = 

      Filename of the visual


   .. attribute:: parent
      

      Axis-type

      :type: Parent


   .. method:: depends_on(self)



   .. method:: give_python_code(self)



   .. method:: change_parent_to(self, new_parent)




.. py:class:: Axis(scene, vfAxis)

   Bases: :class:`DAVE.scene.NodeWithParent`

   Axis

   Axes are the main building blocks of the geometry. They have a position and an rotation in space. Other nodes can be placed on them.
   Axes can be nested by parent/child relationships meaning that an axis can be placed on an other axis.
   The possible movements of an axis can be controlled in each degree of freedom using the "fixed" property.

   Axes are also the main building block of inertia.
   Dynamics are controlled using the inertia properties of an axis: inertia [mT], inertia_position[m,m,m] and inertia_radii [m,m,m]


   .. rubric:: Notes

   - circular references are not allowed: It is not allowed to place a on b and b on a

   .. method:: depends_on(self)



   .. method:: _delete_vfc(self)



   .. method:: inertia(self)
      :property:



   .. method:: inertia_position(self)
      :property:



   .. method:: inertia_radii(self)
      :property:



   .. method:: _update_inertia(self)



   .. method:: fixed(self)
      :property:


      Determines which of the six degrees of freedom are fixed, if any. (x,y,z,rx,ry,rz).
      True means that that degree of freedom will not change when solving statics.
      False means a that is may be changed in order to find equilibrium.

      These are the expressed on the coordinate system of the parent (if any) or the global axis system (if no parent)

      See Also: set_free, set_fixed


   .. method:: set_free(self)


      Sets .fixed to (False,False,False,False,False,False)


   .. method:: set_fixed(self)


      Sets .fixed to (True,True,True,True,True,True)


   .. method:: x(self)
      :property:


      The x-component of the position vector


   .. method:: y(self)
      :property:


      The y-component of the position vector


   .. method:: z(self)
      :property:


      The y-component of the position vector


   .. method:: position(self)
      :property:


      Position of the axis (x,y,z)
      These are the expressed on the coordinate system of the parent (if any) or the global axis system (if no parent)


   .. method:: rx(self)
      :property:


      The x-component of the rotation vector


   .. method:: ry(self)
      :property:


      The y-component of the rotation vector


   .. method:: rz(self)
      :property:


      The z-component of the rotation vector


   .. method:: rotation(self)
      :property:


      Rotation of the axis about its origin (rx,ry,rz).
      Defined as a rotation about an axis where the direction of the axis is (rx,ry,rz) and the angle of rotation is |(rx,ry,rz| degrees.
      These are the expressed on the coordinate system of the parent (if any) or the global axis system (if no parent)


   .. method:: parent(self)
      :property:


      Determines the parent of the axis. Should either be another axis or 'None'


   .. method:: gx(self)
      :property:


      The x-component of the global position vector


   .. method:: gy(self)
      :property:


      The y-component of the global position vector


   .. method:: gz(self)
      :property:


      The z-component of the global position vector


   .. method:: global_position(self)
      :property:


      The global position of the origin.


   .. method:: grx(self)
      :property:


      The x-component of the global rotation vector


   .. method:: gry(self)
      :property:


      The y-component of the global rotation vector


   .. method:: grz(self)
      :property:


      The z-component of the global rotation vector


   .. method:: tilt_x(self)
      :property:


      Returns the trim in [%]. This is the z-component of the unit y vector.

      See Also: heel


   .. method:: heel(self)
      :property:


      Returns the heel in [deg].  SB down is positive.
      This is the inverse sin of the unit y vector(This is the arcsin of the tiltx)

      See also: tilt_x


   .. method:: tilt_y(self)
      :property:


      Returns the trim in [%]. This is the z-component of the unit -x vector. So a positive rotation about
      the y axis result in a positive tilt_y.

      See Also: heel


   .. method:: trim(self)
      :property:


      Returns the trim in [deg]. Bow-down is positive.

      This is the inverse sin of the unit -x vector(This is the arcsin of the tilt_y)

      See also: tilt_y


   .. method:: heading(self)
      :property:


      Returns the direction (0..360) [deg] of the local x-axis relative to the global x axis. Measured about the global z axis

      heading = atan(u_y,u_x)

      typically:
          heading 0  --> local axis align with global axis
          heading 90 --> local x-axis in direction of global y axis


      See also: heading_compass


   .. method:: heading_compass(self)
      :property:


      The heading (0..360)[deg] assuming that the global y-axis is North and global x-axis is East and rotation accoring compass definition


   .. method:: global_rotation(self)
      :property:


      The rotation of the axis in degrees. Expressed in the global axis system


   .. method:: global_transform(self)
      :property:


      Read-only: The global tranform of the axis system.


   .. method:: connection_force(self)
      :property:


      Returns the force and moment that this axis applies on its parent [Parent axis system]


   .. method:: connection_force_x(self)
      :property:


      The x-component of the connection-force vector


   .. method:: connection_force_y(self)
      :property:


      The y-component of the connection-force vector


   .. method:: connection_force_z(self)
      :property:


      The z-component of the connection-force vector


   .. method:: connection_moment_x(self)
      :property:


      The mx-component of the connection-force vector


   .. method:: connection_moment_y(self)
      :property:


      The my-component of the connection-force vector


   .. method:: connection_moment_z(self)
      :property:


      The mx-component of the connection-force vector


   .. method:: applied_force(self)
      :property:


      Returns the force and moment that is applied on this axis [Global axis system]


   .. method:: ux(self)
      :property:


      The unit x axis in global coordinates


   .. method:: uy(self)
      :property:


      The unit y axis in global coordinates


   .. method:: uz(self)
      :property:


      The unit z axis in global coordinates


   .. method:: equilibrium_error(self)
      :property:


      Returns the force and moment that remains on this axis (applied-force minus connection force) [Parent axis system]


   .. method:: to_loc_position(self, value)


      Returns the local position of a point in the global axis system.
      This considers the position and the rotation of the axis system.
      See Also: to_loc_direction


   .. method:: to_glob_position(self, value)


      Returns the global position of a point in the local axis system.
      This considers the position and the rotation of the axis system.
      See Also: to_glob_direction


   .. method:: to_loc_direction(self, value)


      Returns the local direction of a point in the global axis system.
      This considers only the rotation of the axis system.
      See Also: to_loc_position


   .. method:: to_glob_direction(self, value)


      Returns the global direction of a point in the local axis system.
      This considers only the rotation of the axis system.
      See Also: to_glob_position


   .. method:: to_loc_rotation(self, value)


      Returns the local rotation. Used for rotating rotations.
      See Also: to_loc_position, to_loc_direction


   .. method:: to_glob_rotation(self, value)


      Returns the global rotation. Used for rotating rotations.
      See Also: to_loc_position, to_loc_direction


   .. method:: change_parent_to(self, new_parent)


      Assigns a new parent to the node but keeps the global position and rotation the same.

      See also: .parent (property)

      :param new_parent: new parent node


   .. method:: give_python_code(self)




.. py:class:: Poi(scene, vfPoi)

   Bases: :class:`DAVE.scene.NodeWithParent`

   A location on an axis

   .. method:: x(self)
      :property:


      x component of local position


   .. method:: y(self)
      :property:


      y component of local position


   .. method:: z(self)
      :property:



   .. method:: position(self)
      :property:


      Local position


   .. method:: applied_force_and_moment_global(self)
      :property:


      Returns the applied force in the parent axis system


   .. method:: gx(self)
      :property:


      x component of global position


   .. method:: gy(self)
      :property:


      y component of global position


   .. method:: gz(self)
      :property:


      z component of global position


   .. method:: global_position(self)
      :property:


      Global position


   .. method:: give_python_code(self)




.. py:class:: RigidBody(scene, axis, poi, force)

   Bases: :class:`DAVE.scene.Axis`

   A Rigid body, internally composed of an axis, a poi (cog) and a force (gravity)

   .. method:: _delete_vfc(self)



   .. method:: name(self)
      :property:



   .. method:: cogx(self)
      :property:



   .. method:: cogy(self)
      :property:



   .. method:: cogz(self)
      :property:



   .. method:: cog(self)
      :property:


      Control the cog position of the body


   .. method:: mass(self)
      :property:


      Control the static mass of the body


   .. method:: give_python_code(self)




.. py:class:: Cable(scene, node)

   Bases: :class:`DAVE.scene.CoreConnectedNode`

   A Cable represents a linear elastic wire running from a Poi or sheave to another Poi of sheave.

   A cable has a un-stretched length [length] and a stiffness [EA] and may have a diameter [m]. The tension in the cable is calculated.

   Intermediate pois or sheaves may be added.

   - Pois are considered as sheaves with a zero diameter.
   - Sheaves are considered sheaves with the given geometry. If defined then the diameter of the cable is considered when calculating the geometry. The cable runs over the sheave in the positive direction (right hand rule) as defined by the axis of the sheave.

   For cables running over a sheave the friction in sideways direction is considered to be infinite. The geometry is calculated such that the
   cable section between sheaves is perpendicular to the vector from the axis of the sheave to the point where the cable leaves the sheave.

   This assumption results in undefined behaviour when the axis of the sheave is parallel to the cable direction.

   .. rubric:: Notes

   If pois or sheaves on a cable come too close together (<1mm) then they will be pushed away from eachother.
   This prevents the unwanted situation where multiple pois end up at the same location. In that case it can not be determined which amount of force should be applied to each of the pois.

   .. method:: depends_on(self)



   .. method:: tension(self)
      :property:


      Tension in the cable in [kN] (Readonly, calculated)


   .. method:: stretch(self)
      :property:


      Stretch of the cable in [m] (Readonly, calculated)


   .. method:: length(self)
      :property:


      Length in rest [m]


   .. method:: EA(self)
      :property:


      Stiffness of the cable in [kN]


   .. method:: diameter(self)
      :property:


      Diameter of the cable [m]


   .. method:: connections(self)
      :property:



   .. method:: get_points_for_visual(self)


      Returns an list of 3D locations which can be used for visualization


   .. method:: _add_connection_to_core(self, connection)



   .. method:: _update_pois(self)



   .. method:: _give_poi_names(self)


      Returns a list with the names of all the pois


   .. method:: give_python_code(self)




.. py:class:: Force

   Bases: :class:`DAVE.scene.NodeWithParent`

   A Force models a force and moment on a poi.

   Both are expressed in the global axis system.

   .. method:: force(self)
      :property:


      Gets or sets the x,y and z force components.

      Example s['wind'].force = (12,34,56)


   .. method:: fx(self)
      :property:


      The global x-component of the force


   .. method:: fy(self)
      :property:


      The global y-component of the force


   .. method:: fz(self)
      :property:


      The global z-component of the force


   .. method:: moment(self)
      :property:


      Gets or sets the x,y and z moment components.

      Example s['wind'].moment = (12,34,56)


   .. method:: mx(self)
      :property:


      The global x-component of the force


   .. method:: my(self)
      :property:


      The global y-component of the force


   .. method:: mz(self)
      :property:


      The global z-component of the force


   .. method:: give_python_code(self)




.. py:class:: ContactMesh(scene, vfContactMesh)

   Bases: :class:`DAVE.scene.NodeWithParent`

   A ContactMesh is a tri-mesh with an axis parent

   .. method:: trimesh(self)
      :property:



   .. method:: give_python_code(self)




.. py:class:: ContactBall(scene, node)

   Bases: :class:`DAVE.scene.NodeWithParent`

   A ContactBall is a linear elastic ball which can contact with ContactMeshes.

   It is modelled as a sphere around a Poi. Radius and stiffness can be controlled using radius and k.

   The force is applied on the Poi and it not registered separately.

   .. method:: has_contact(self)
      :property:



   .. method:: contactpoint(self)
      :property:



   .. method:: add_contactmesh(self, mesh)



   .. method:: clear_contactmeshes(self)



   .. method:: meshes_names(self)
      :property:


      returns a list with the names of the meshes


   .. method:: force(self)
      :property:



   .. method:: radius(self)
      :property:



   .. method:: k(self)
      :property:



   .. method:: give_python_code(self)




.. py:class:: Sheave

   Bases: :class:`DAVE.scene.NodeWithParent`

   A Sheave models sheave with axis and diameter.



   .. method:: axis(self)
      :property:


      Gets or sets direction of the sheave axis


   .. method:: radius(self)
      :property:


      Gets or sets radius of the sheave


   .. method:: give_python_code(self)



   .. method:: global_position(self)
      :property:


      Returns the global position of the center of the sheave



.. py:class:: HydSpring

   Bases: :class:`DAVE.scene.NodeWithParent`

   A HydSpring models a linearized hydrostatic spring.

   The cob (center of buoyancy) is defined in the parent axis system.
   All other properties are defined relative to the cob.

   .. method:: cob(self)
      :property:


      Center of buoyancy in parent axis system


   .. method:: BMT(self)
      :property:


      Vertical distance between cob and metacenter for roll


   .. method:: BML(self)
      :property:


      Vertical distance between cob and metacenter for pitch


   .. method:: COFX(self)
      :property:


      Horizontal x-position Center of Floatation (center of waterplane area), relative to cob


   .. method:: COFY(self)
      :property:


      Horizontal y-position Center of Floatation (center of waterplane area), relative to cob


   .. method:: kHeave(self)
      :property:


      Heave stiffness in kN/m


   .. method:: waterline(self)
      :property:


      Waterline-elevation relative to cob for un-stretched heave-spring. Positive if cob is below the waterline (which is where is normally is)


   .. method:: displacement_kN(self)
      :property:


      Displacement in [kN] when waterline is at waterline-elevation


   .. method:: give_python_code(self)




.. py:class:: LC6d(scene, node)

   Bases: :class:`DAVE.scene.CoreConnectedNode`

   A LC6d models a Linear Connector with 6 dofs.

   It connects two Axis elements with six linear springs.
   The translational-springs are easy. The rotational springs may not be as intuitive. They are defined as:

     - rotation_x = arc-tan ( uy[0] / uy[1] )
     - rotation_y = arc-tan ( -ux[0] / ux[2] )
     - rotation_z = arc-tan ( ux[0] / ux [1] )

   which works fine for small rotations and rotations about only a single axis.

   Try to avoid using very high stiffness settings to create fixed connections. It is better to use use the "fixed"
   property of axis systems to create joints.

   .. method:: depends_on(self)



   .. method:: stiffness(self)
      :property:


      Stiffness of the connector (kx, ky, kz, krx, kry, krz)


   .. method:: master(self)
      :property:


      Master axis system


   .. method:: slave(self)
      :property:


      Slave axis system


   .. method:: give_python_code(self)




.. py:class:: Connector2d(scene, node)

   Bases: :class:`DAVE.scene.CoreConnectedNode`

   A Connector2d linear connector with acts both on linear displacement and angular displacement.

   * the linear stiffness is defined by k_linear and is defined over the actual shortest direction between master and slave.
   * the angular stiffness is defined by k_angular and is defined over the actual smallest angle between the two systems.

   .. method:: depends_on(self)



   .. method:: angle(self)
      :property:


      Actual angle between master and slave [deg] (read-only)


   .. method:: force(self)
      :property:


      Actual force between master and slave [kN] (read-only)


   .. method:: moment(self)
      :property:


      Actual moment between master and slave [kN*m] (read-only)


   .. method:: axis(self)
      :property:


      Actual rotation axis between master and slave (read-only)


   .. method:: ax(self)
      :property:


      X component of actual rotation axis between master and slave (read-only)


   .. method:: ay(self)
      :property:


      Y component of actual rotation axis between master and slave (read-only)


   .. method:: az(self)
      :property:


      Z component of actual rotation axis between master and slave (read-only)


   .. method:: k_linear(self)
      :property:


      Linear stiffness [kN/m]


   .. method:: k_angular(self)
      :property:


      Linear stiffness [kN*m/rad]


   .. method:: master(self)
      :property:


      Master axis system


   .. method:: slave(self)
      :property:


      Slave axis system


   .. method:: give_python_code(self)




.. py:class:: LinearBeam(scene, node)

   Bases: :class:`DAVE.scene.CoreConnectedNode`

   A LinearBeam models a FEM-like linear beam element.

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

   .. method:: depends_on(self)



   .. method:: EIy(self)
      :property:



   .. method:: EIz(self)
      :property:



   .. method:: GIp(self)
      :property:



   .. method:: EA(self)
      :property:



   .. method:: master(self)
      :property:



   .. method:: L(self)
      :property:



   .. method:: slave(self)
      :property:



   .. method:: moment_on_master(self)
      :property:



   .. method:: moment_on_slave(self)
      :property:



   .. method:: tension(self)
      :property:



   .. method:: torsion(self)
      :property:



   .. method:: torsion_angle(self)
      :property:


      Torsion angle in degrees


   .. method:: give_python_code(self)




.. py:class:: TriMeshSource(scene, source)

   Bases: :class:`DAVE.scene.Node`

   TriMesh

   A TriMesh node contains triangular mesh which can be used for buoyancy or contact

   .. method:: AddVertex(self, x, y, z)



   .. method:: AddFace(self, i, j, k)



   .. method:: get_extends(self)


      Returns the extends of the mesh in global coordinates

      Returns: (minimum_x, maximum_x, minimum_y, maximum_y, minimum_z, maximum_z)


   .. method:: make_cube(self)


      Sets the mesh to a cube


   .. method:: _fromVTKpolydata(self, polydata, offset=None, rotation=None, scale=None)



   .. method:: load_vtk_polydataSource(self, polydata)


      Fills the triangle data from a vtk polydata such as a cubeSource.

      The vtk TriangleFilter is used to triangulate the source

      .. rubric:: Examples

      cube = vtk.vtkCubeSource()
      cube.SetXLength(122)
      cube.SetYLength(38)
      cube.SetZLength(10)
      trimesh.load_vtk_polydataSource(cube)


   .. method:: load_obj(self, filename, offset=None, rotation=None, scale=None)


      Loads an .obj file and and triangulates it.

      Order of modifications:

      1. rotate
      2. scale
      3. offset

      :param filename: (str or path): file to load
      :param offset: : offset
      :param rotation: : rotation
      :param scale: scale


   .. method:: give_python_code(self)



   .. method:: change_parent_to(self, new_parent)




.. py:class:: Buoyancy(scene, vfBuoyancy)

   Bases: :class:`DAVE.scene.NodeWithParent`

   Buoyancy provides a buoyancy force based on a buoyancy mesh. The mesh is triangulated and chopped at the instantaneous flat water surface. Buoyancy is applied as an upwards force that the center of buoyancy.
   The calculation of buoyancy is as accurate as the provided geometry.

   There as no restrictions to the size or aspect ratio of the panels. It is excellent to model as box using 6 faces. Using smaller panels has a negative effect on performance.

   The normals of the panels should point towards to water.

   .. method:: trimesh(self)
      :property:



   .. method:: cob(self)
      :property:


      Returns the GLOBAL position of the center of buoyancy


   .. method:: cob_local(self)
      :property:


      Returns the local position of the center of buoyancy


   .. method:: displacement(self)
      :property:


      Returns displaced volume in m^3


   .. method:: give_python_code(self)




.. py:class:: BallastSystem(scene, poi, force)

   Bases: :class:`DAVE.scene.Poi`

   A BallastSystem

   The position of the axis system is the reference position for the tanks.

   Tanks can be added using new_tank()


   technical notes:
   - System is similar to the setup of RigidBody, but without the Axis
   - The class extends Poi, but overrides some of its properties
   - Update nees to be called to update the weight and cog

   TODO: Inertia

   .. py:class:: Tank

      .. attribute:: name
         :annotation: = noname

         Name of the tank


      .. attribute:: max
         :annotation: = 0

         Maximum fill in [kN]


      .. attribute:: pct
         :annotation: = 0

         Actual fill percentage in [%]


      .. attribute:: position
         

         Tank CoG position relative to ballast system origin [m,m,m]


      .. attribute:: frozen
         :annotation: = False

         The fill of frozen tanks should not be altered


      .. attribute:: _pointmass
         

         Optional reference to pointmass node - handled by ballastsystem node


      .. method:: inertia(self)
         :property:



      .. method:: weight(self)


         Returns the actual weight of tank contents in kN


      .. method:: is_full(self)


         Returns True of tank is (almost) full


      .. method:: is_empty(self)


         Returns True of tank is (almost) empty


      .. method:: is_partial(self)


         Returns True of tank not full but also not empty


      .. method:: mxmymz(self)


         Position times actual weight


      .. method:: make_empty(self)


         Empties the tank


      .. method:: make_full(self)


         Fills the tank



   .. attribute:: _tanks
      :annotation: = []

      List of tank objects


   .. attribute:: _position
      :annotation: = [0.0, 0.0, 0.0]

      Position is the origin of the ballast system


   .. attribute:: _cog
      :annotation: = [0.0, 0.0, 0.0]

      Position of the CoG of the ballast-tanks relative to self._position, calculated when calling update()


   .. attribute:: _weight
      :annotation: = 0

      Weight [kN] of the ballast-tanks , calculated when calling update()


   .. attribute:: frozen
      :annotation: = False

      The contents of a frozen tank should not be changed


   .. method:: update(self)



   .. method:: _delete_vfc(self)



   .. method:: position(self)
      :property:


      Local position


   .. method:: name(self)
      :property:



   .. method:: new_tank(self, name, position, capacity_kN, actual_fill=0, frozen=False)


      Creates a new tanks and adds it to the ballast-system

      :param name: (str) name of the tanks
      :param position: (float[3]) position of the tank [m,m,m]
      :param capacity_kN: (float) Maximum capacity of the tank in [kN]
      :param actual_fill: (float) Optional, actual fill percentage of the tank [0] [%]
      :param frozen: (bool) Optional, the contents of frozen tanks should not be altered

      :returns: BallastSystem.Tank object


   .. method:: reorder_tanks(self, names)


      Places tanks with given names at the top of the list. Other tanks are appended afterwards in original order.

      For a complete re-order give all tank names.

      .. rubric:: Example

      let tanks be 'a','b','c','d','e'

      then re_order_tanks(['e','b']) will result in ['e','b','a','c','d']


   .. method:: order_tanks_by_elevation(self)


      Re-orders the existing tanks such that the lowest tanks are higher in the list


   .. method:: order_tanks_by_distance_from_point(self, point, reverse=False)


      Re-orders the existing tanks such that the tanks *furthest* from the point are first on the list

      :param point: (x,y,z)  - reference point to determine the distance to
      :param reverse: (False) - order in reverse order: tanks nearest to the points first on list


   .. method:: order_tanks_to_maximize_inertia_moment(self)


      Re-order tanks such that tanks furthest from center of system are first on the list


   .. method:: order_tanks_to_minimize_inertia_moment(self)


      Re-order tanks such that tanks nearest to center of system are first on the list


   .. method:: _order_tanks_to_inertia_moment(self, maximize=True)



   .. method:: tank_names(self)



   .. method:: fill_tank(self, name, fill)



   .. method:: xyzw(self)


      Gets the current ballast cog and weight from the tanks

      :returns: (x,y,z), weight


   .. method:: empty_all_usable_tanks(self)



   .. method:: tank(self, name)



   .. method:: __getitem__(self, item)



   .. method:: cogx(self)
      :property:



   .. method:: cogy(self)
      :property:



   .. method:: cogz(self)
      :property:



   .. method:: cog(self)
      :property:


      Returns the cog of the ballast-system


   .. method:: weight(self)
      :property:


      Returns the cog of the ballast-system


   .. method:: mass(self)
      :property:


      Control the static mass of the body


   .. method:: give_python_code(self)




.. py:class:: WaveInteraction1(scene)

   Bases: :class:`DAVE.scene.Node`

   WaveInteraction

   Wave-interaction-1 couples a first-order hydrodynamic database to an axis.

   This adds:
   - wave-forces
   - damping
   - added mass

   The data is provided by a Hyddb1 object which is defined in the MaFreDo package. The contents are not embedded
   but are to be provided separately in a file. This node contains only the file-name.

   .. attribute:: offset
      :annotation: = [0, 0, 0]

      Offset (x,y,z) of the visual. Offset is applied after scaling


   .. attribute:: parent
      

      Axis-type

      :type: Parent


   .. attribute:: path
      

      Filename of a file that can be read by a Hyddb1 object


   .. method:: depends_on(self)



   .. method:: give_python_code(self)



   .. method:: change_parent_to(self, new_parent)




.. py:class:: Manager

   .. method:: managed_nodes(self)


      Returns a list of managed nodes


   .. method:: delete(self)


      Carefully remove the manager, reinstate situation as before



.. py:class:: GeometricContact(scene, circle1, circle2, name)

   Bases: :class:`DAVE.scene.Node`, :class:`DAVE.scene.Manager`

   GeometricContact

   A GeometricContact can be used to construct geometric connections between circular members:
       -       steel bars and holes, such as a shackle pin in a padeye (pin-hole)
       -       steel bars and steel bars, such as a shackle-shackle connection


   parent_parent_of_circle2 [axis]  <-- not managed
      - parent_of_circle2 [poi]
          - circle2 [circle]        <--- input for creation

          - SELF_master_axis           <--- created
               - SELF_pin_hole_connection  <--- created
                 -SELF_connection_axial_rotation
                   - SELF_slaved_axis       <--- created

                      - parent_of_parent_of_circle1 [axis]
                        - parent_of_circle_1 [poi]
                          - circle1 [circle]               <--- input for creation




   .. attribute:: _master_axis
      

      Axis on the master axis at the location of the center of hole or pin


   .. attribute:: _pin_hole_connection
      

      axis between the center of the hole and the center of the pin. Free to rotate about the center of the hole as well as the pin


   .. attribute:: _slaved_axis
      

      axis to which the slaved body is connected. Either the center of the hole or the center of the pin


   .. method:: parent(self)
      :property:



   .. method:: change_parent_to(self, new_parent)



   .. method:: delete(self)



   .. method:: _make_connection(self)



   .. method:: set_pin_pin_connection(self)


      Sets the connection to be of type pin-pin


   .. method:: set_pin_in_hole_connection(self)


      Sets the connection to be of type pin-in-hole

      The axes of the two sheaves are aligned by rotating the slaved body
      The axes of the two sheaves are placed at a distance hole_dia - pin_dia apart, perpendicular to the axis direction
      An axes is created at the centers of the two sheaves
      These axes are connected with a shore axis which is allowed to rotate relative to the master axis
      the slave axis is fixed to this rotating axis


   .. method:: managed_nodes(self)


      Returns a list of managed nodes


   .. method:: depends_on(self)



   .. method:: flip(self)



   .. method:: change_side(self)



   .. method:: swivel(self)
      :property:



   .. method:: swivel_fixed(self)
      :property:



   .. method:: master_rotation(self)
      :property:



   .. method:: master_fixed(self)
      :property:



   .. method:: slave_rotation(self)
      :property:



   .. method:: slave_fixed(self)
      :property:



   .. method:: inside(self)
      :property:



   .. method:: give_python_code(self)




.. py:class:: Sling(scene, name, length, LeyeA, LeyeB, LspliceA, LspliceB, diameter, EA, mass, endA=None, endB=None, sheaves=None)

   Bases: :class:`DAVE.scene.Node`, :class:`DAVE.scene.Manager`

   A Sling is a single wire with an eye on each end. The eyes are created by splicing the end of the sling back
   into the itself.

   The geometry of a sling is defined as follows:

   diameter : diameter of the wire
   LeyeA, LeyeB : inside lengths of the eyes
   LsplicaA, LspliceB : the length of the splices
   Total : the distance between the insides of ends of the eyes A and B when pulled straight.

   Stiffness:
   The stiffness of the sling is specified by a single value: EA
   This determines the stiffnesses of the individual parts as follows:
   Wire in the eyes: EA
   Splices: Infinity (rigid)
   Main part: determined such that total stiffness (k) of the sling is EA/L


     Eye A           Splice A             main part                   Splice B          Eye B

   /---------------\                                                                /---------------    |                =============-------------------------------------===============                |
   \---------------/                                                                \---------------/

   See Also: Grommet

   .. method:: _update_properties(self)



   .. method:: depends_on(self)


      Endpoints and sheaves are managed, so no dependency on those

      however we do depend on their parents (if any)


   .. method:: managed_nodes(self)



   .. method:: delete(self)



   .. method:: give_python_code(self)



   .. method:: length(self)
      :property:



   .. method:: LeyeA(self)
      :property:



   .. method:: LeyeB(self)
      :property:



   .. method:: LspliceA(self)
      :property:



   .. method:: LspliceB(self)
      :property:



   .. method:: diameter(self)
      :property:



   .. method:: EA(self)
      :property:



   .. method:: mass(self)
      :property:



   .. method:: endA(self)
      :property:



   .. method:: endB(self)
      :property:



   .. method:: sheaves(self)
      :property:




.. py:class:: Scene(filename=None, copy_from=None)

   A Scene is the main component of DAVE.

   It provides a world to place nodes (elements) in.
   It interfaces with the equilibrium core for all calculations.

   By convention a Scene element is created with the name s, but create as many scenes as you want.

   .. rubric:: Examples

   s = Scene()
   s.new_axis('my_axis', position = (0,0,1))

   a = Scene() # another world
   a.new_poi('a point')

   .. attribute:: verbose
      :annotation: = True

      Report actions using print()


   .. attribute:: _vfc
      

      DAVE Core, where the actual magic happens

      :type: _vfc


   .. attribute:: _nodes
      :annotation: = []

      Contains a list of all nodes in the scene


   .. attribute:: static_tolerance
      :annotation: = 0.01

      Desired tolerance when solving statics


   .. attribute:: resources_paths
      :annotation: = []

      A list of paths where to look for resources such as .obj files. Priority is given to paths earlier in the list.


   .. attribute:: _savepoint
      

      Python code to re-create the scene, see savepoint_make()


   .. attribute:: _name_prefix
      :annotation: = 

      An optional prefix to be applied to node names. Used when importing scenes.


   .. attribute:: current_manager
      

      Setting this to an instance of a Manager allows nodes with that manager to be changed


   .. attribute:: _godmode
      :annotation: = False

      Icarus warning, wear proper PPE


   .. method:: clear(self)


      Deletes all nodes


   .. method:: _print_cpp(self)



   .. method:: _print(self, what)



   .. method:: _prefix_name(self, name)



   .. method:: _verify_name_available(self, name)


      Throws an error if a node with name 'name' already exists


   .. method:: _node_from_node_or_str(self, node)


      If node is a string, then returns the node with that name,
      if node is a node, then returns that node

      :raises ValueError if a string is passed with an non-existing node:


   .. method:: _node_from_node(self, node, reqtype)


      Gets a node from the specified type

      Returns None if node is None
      Returns node if node is already a reqtype type node
      Else returns the axis with the given name

      Raises Exception if a node with name is not found


   .. method:: _parent_from_node(self, node)


      Returns None if node is None
      Returns node if node is an axis type node
      Else returns the axis with the given name

      Raises Exception if a node with name is not found


   .. method:: _poi_from_node(self, node)


      Returns None if node is None
      Returns node if node is an poi type node
      Else returns the poi with the given name

      Raises Exception if anything is not ok


   .. method:: _poi_or_sheave_from_node(self, node)


      Returns None if node is None
      Returns node if node is an poi type node
      Else returns the poi with the given name

      Raises Exception if anything is not ok


   .. method:: _sheave_from_node(self, node)


      Returns None if node is None
      Returns node if node is an poi type node
      Else returns the poi with the given name

      Raises Exception if anything is not ok


   .. method:: _geometry_changed(self)


      Notify the scene that the geometry has changed and that the global transforms are invalid


   .. method:: _fix_vessel_heel_trim(self)


      Fixes the heel and trim of each node that has a buoyancy or linear hydrostatics node attached.

      :returns: Dictionary with original fixed properties as dict({'node name',fixed[6]}) which can be passed to _restore_original_fixes


   .. method:: _restore_original_fixes(self, original_fixes)


      Restores the fixes as in original_fixes

      See also: _fix_vessel_heel_trim

      :param original_fixes: dict with {'node name',fixes[6] }

      :returns: None


   .. method:: get_resource_path(self, name)


      Looks for a file with "name" in the specified resource-paths and returns the full path to the the first one
      that is found.
      If name is a full path to an existing file, then that is returned.

      .. seealso:: resource_paths

      :returns: Full path to resource

      :raises FileExistsError if resource is not found:


   .. method:: get_resource_list(self, extension)


      Returns a list of all file-paths (strings) given extension in any of the resource-paths


   .. method:: node_by_name(self, node_name, silent=False)



   .. method:: __getitem__(self, node_name)


      Returns a node with name


   .. method:: nodes_of_type(self, node_class)


      Returns all nodes of the specified or derived type

      .. rubric:: Examples

      pois = scene.nodes_of_type(DAVE.Poi)
      axis_and_bodies = scene.nodes_of_type(DAVE.Axis)


   .. method:: assert_unique_names(self)


      Asserts that all names are unique


   .. method:: sort_nodes_by_parent(self)


      Sorts the nodes such that the parent of this node (if any) occurs earlier in the list.

      .. seealso:: sort_nodes_by_dependency


   .. method:: sort_nodes_by_dependency(self)


      Sorts the nodes such that a node only depends on nodes earlier in the list.

      .. seealso:: sort_nodes_by_parent


   .. method:: name_available(self, name)


      Returns True if the name is still available


   .. method:: available_name_like(self, like)


      Returns an available name like the one given, for example Axis23


   .. method:: node_A_core_depends_on_B_core(self, A, B)


      Returns True if the node core of node A depends on the core node of node B


   .. method:: nodes_depending_on(self, node)


      Returns a list of nodes that physically depend on node. Only direct dependants are obtained with a connection to the core.
      This function should be used to determine dependencies of Core-connected elements.

      For making node-trees please use nodes_with_parent instead.

      :param node: Node or node-name

      :returns: list of names

      See Also: nodes_with_parent


   .. method:: nodes_with_parent(self, node)


      Returns a list of nodes that have given node as a parent. Good for making trees.
      For checking physical connections use nodes_depending_on instead.

      :param node: Node or node-name

      :returns: list of names

      See Also: nodes_depending_on


   .. method:: delete(self, node)


      Deletes the given node from the scene as well as all nodes depending on it.

      .. seealso:: dissolve


   .. method:: dissolve(self, node)


      Attempts to delete the given node without affecting the rest of the model.

      1. Look for nodes that have this node as parent
      2. Attach those nodes to the parent of this node.
      3. Delete this node.

      There are many situations in which this will fail because an it is impossible to dissolve
      the element. For example a poi can only be dissolved when nothing is attached to it.

      For now this function only works on AXIS


   .. method:: savepoint_make(self)



   .. method:: savepoint_restore(self)



   .. method:: update(self)


      Updates the interface between the nodes and the core. This includes the re-calculation of all forces,
      buoyancy positions, ballast-system cogs etc.


   .. method:: solve_statics(self, silent=False, timeout=None)


      Solves statics

      :param silent: Do not print if successfully solved

      :returns: True if successful, False otherwise.
      :rtype: bool


   .. method:: verify_equilibrium(self, tol=0.01)


      Checks if the current state is an equilibrium

      :returns: True if successful, False if not an equilibrium.
      :rtype: bool


   .. method:: goal_seek(self, evaluate, target, change_node, change_property, bracket=None, tol=0.001)


      goal_seek

      Goal seek is the classic goal-seek. It changes a single property of a single node in order to get
      some property of some node to a specified value. Just like excel.

      :param evaluate: code to be evaluated to yield the value that is solved for. Eg: s['poi'].fx Scene is abbiviated as "s"
      :param target: target value for that property
      :type target: number
      :param change_node: node to be adjusted
      :type change_node: Node or str
      :param change_property: property of that node to be adjusted
      :type change_property: str
      :param range: specify the possible search-interval
      :type range: optional

      :returns: True if successful, False otherwise.
      :rtype: bool

      .. rubric:: Examples

      Change the y-position of the cog of a rigid body ('Barge')  in order to obtain zero roll (rx)
      >>> s.goal_seek("s['Barge'].fx",0,'Barge','cogy')


   .. method:: plot_effect(self, evaluate, change_node, change_property, start, to, steps)


      Produces a 2D plot with the relation between two properties of the scene. For example the length of a cable
      versus the force in another cable.

      The evaluate argument is processed using "eval" and may contain python code. This may be used to combine multiple
      properties to one value. For example calculate the diagonal load distribution from four independent loads.

      The plot is produced using matplotlob. The plot is produced in the current figure (if any) and plt.show is not executed.

      :param evaluate: code to be evaluated to yield the value on the y-axis. Eg: s['poi'].fx Scene is abbiviated as "s"
      :type evaluate: str
      :param change_node: node to be adjusted
      :type change_node: Node or str
      :param change_property: property of that node to be adjusted
      :type change_property: str
      :param start: left side of the interval
      :param to: right side of the interval
      :param steps: number of steps in the interval

      :returns: Tuple (x,y) with x and y coordinates

      .. rubric:: Examples

      >>> s.plot_effect("s['cable'].tension", "cable", "length", 11, 14, 10)
      >>> import matplotlib.pyplot as plt
      >>> plt.show()


   .. method:: new_axis(self, name, parent=None, position=None, rotation=None, inertia=None, inertia_radii=None, fixed=True)


      Creates a new *axis* node and adds it to the scene.

      :param name: Name for the node, should be unique
      :param parent: optional, name of the parent of the node
      :param position: optional, position for the node (x,y,z)
      :param rotation: optional, rotation for the node (rx,ry,rz)
      :param fixed [True]: optional, determines whether the axis is fixed [True] or free [False]. May also be a sequence of 6 booleans.

      :returns: Reference to newly created axis


   .. method:: new_geometriccontact(self, name, slave_item, master_item, inside=False, swivel=None, master_rotation=None, slave_rotation=None, swivel_fixed=True, master_fixed=False, slave_fixed=False)


      Creates a new *new_geometriccontact* node and adds it to the scene.

      Geometric contact connects two circular elements and can be used to model bar-bar connections or pin-in-hole connections.

      By default a bar-bar connection is created between item1 and item2.

      :param name: Name for the node, should be unique
      :param slave_item: [Sheave] will be the master of the connection
      :param master_item: [Sheave] will be the slave of the connection
      :param inside: [False] False creates a pinpin connection. True creates a pin-hole type of connection
      :param swivel: Rotation angle between the two items. Defaults to 90 for pinpin and 0 for pin-hole
      :param master_rotation: Angle of the connecting hinge relative to master or None for default
      :param slave_rotation: Angle of the slave relative to the connecting hinge or None for default
      :param swivel_fixed: Fix swivel [True]
      :param master_fixed: Fix connecting hinge to master [False]
      :param slave_fixed: Fix slave to connecting hinge [False]

      .. note::

         For pin-hole connections there is no geometrical difference between the pin and the hole. Therefore it is not needed to specify
         which is the pin and which is the hole

      :returns: Reference to newly created new_geometriccontact


   .. method:: new_waveinteraction(self, name, path, parent=None, offset=None)


      Creates a new *wave interaction* node and adds it to the scene.

      :param name: Name for the node, should be unique
      :param path: Path to the hydrodynamic database
      :param parent: optional, name of the parent of the node
      :param offset: optional, position for the node (x,y,z)

      :returns: Reference to newly created wave-interaction object


   .. method:: new_visual(self, name, path, parent=None, offset=None, rotation=None, scale=None)


      Creates a new *Visual* node and adds it to the scene.

      :param name: Name for the node, should be unique
      :param path: Path to the resource
      :param parent: optional, name of the parent of the node
      :param offset: optional, position for the node (x,y,z)
      :param rotation: optional, rotation for the node (rx,ry,rz)
      :param scale: optional, scale of the visual (x,y,z).

      :returns: Reference to newly created visual


   .. method:: new_poi(self, name, parent=None, position=None)


      Creates a new *poi* node and adds it to the scene.

      :param name: Name for the node, should be unique
      :param parent: optional, name of the parent of the node
      :param position: optional, position for the node (x,y,z)

      :returns: Reference to newly created poi


   .. method:: new_rigidbody(self, name, mass=0, cog=(0, 0, 0), parent=None, position=None, rotation=None, inertia_radii=None, fixed=True)


      Creates a new *rigidbody* node and adds it to the scene.

      :param name: Name for the node, should be unique
      :param mass: optional, [0] mass in mT
      :param cog: optional, (0,0,0) cog-position in (m,m,m)
      :param parent: optional, name of the parent of the node
      :param position: optional, position for the node (x,y,z)
      :param rotation: optional, rotation for the node (rx,ry,rz)
      :param inertia_radii: optional, radii of gyration (rxx,ryy,rzz); only used for dynamics
      :param fixed [True]: optional, determines whether the axis is fixed [True] or free [False]. May also be a sequence of 6 booleans.

      .. rubric:: Examples

      scene.new_rigidbody("heavy_thing", mass = 10000, cog = (1.45, 0, -0.7))

      :returns: Reference to newly created RigidBody


   .. method:: new_cable(self, name, endA, endB, length=-1, EA=0, diameter=0, sheaves=None)


      Creates a new *cable* node and adds it to the scene.

      :param name: Name for the node, should be unique
      :param endA: A Poi element to connect the first end of the cable to
      :param endB: A Poi element to connect the other end of the cable to
      :param length [-1]: un-stretched length of the cable in m; default [-1] create a cable with the current distance between the endpoints A and B
      :param EA [0]: stiffness of the cable in kN/m; default
      :param sheaves: [optional] A list of pois, these are sheaves that the cable runs over. Defined from endA to endB

      .. rubric:: Examples

      scene.new_cable('cable_name' endA='poi_start', endB = 'poi_end')  # minimal use

      scene.new_cable('cable_name', length=50, EA=1000, endA=poi_start, endB = poi_end, sheaves=[sheave1, sheave2])

      scene.new_cable('cable_name', length=50, EA=1000, endA='poi_start', endB = 'poi_end', sheaves=['single_sheave']) # also a single sheave needs to be provided as a list

      .. rubric:: Notes

      The default options for length and EA can be used to measure distances between points

      :returns: Reference to newly created Cable


   .. method:: new_force(self, name, parent=None, force=None, moment=None)


      Creates a new *force* node and adds it to the scene.

      :param name: Name for the node, should be unique
      :param parent: name of the parent of the node [Poi]
      :param force: optional, global force on the node (x,y,z)
      :param moment: optional, global force on the node (x,y,z)

      :returns: Reference to newly created force


   .. method:: new_sheave(self, name, parent, axis, radius=0.0)


      Creates a new *sheave* node and adds it to the scene.

      :param name: Name for the node, should be unique
      :param parent: name of the parent of the node [Poi]
      :param axis: direction of the axis of rotation (x,y,z)
      :param radius: optional, radius of the sheave

      :returns: Reference to newly created sheave


   .. method:: new_hydspring(self, name, parent, cob, BMT, BML, COFX, COFY, kHeave, waterline, displacement_kN)


      Creates a new *hydspring* node and adds it to the scene.

      :param name: Name for the node, should be unique
      :param parent: name of the parent of the node [Axis]
      :param cob: position of the CoB (x,y,z) in the parent axis system
      :param BMT: Vertical distance between CoB and meta-center for roll
      :param BML: Vertical distance between CoB and meta-center for pitch
      :param COFX: X-location of center of flotation (center of waterplane) relative to CoB
      :param COFY: Y-location of center of flotation (center of waterplane) relative to CoB
      :param kHeave: heave stiffness (typically Awl * rho * g)
      :param waterline: Z-position (elevation) of the waterline relative to CoB
      :param displacement_kN: displacement (typically volume * rho * g)

      :returns: Reference to newly created hydrostatic spring


   .. method:: new_linear_connector_6d(self, name, slave, master, stiffness=None)


      Creates a new *linear connector 6d* node and adds it to the scene.

      :param name: Name for the node, should be unique
      :param slave: Slaved axis system [Axis]
      :param master: Master axis system [Axis]
      :param stiffness: optional, connection stiffness (x,y,z, rx,ry,rz)

      See :py:class:`LC6d` for details

      :returns: Reference to newly created connector


   .. method:: new_connector2d(self, name, master, slave, k_linear=0, k_angular=0)


      Creates a new *new_connector2d* node and adds it to the scene.

      :param name: Name for the node, should be unique
      :param slave: Slaved axis system [Axis]
      :param master: Master axis system [Axis]
      :param k_linear: linear stiffness in kN/m
      :param k_angular: angular stiffness in kN*m / rad

      :returns: Reference to newly created connector2d


   .. method:: new_linear_beam(self, name, master, slave, EIy=0, EIz=0, GIp=0, EA=0, L=None)


      Creates a new *linear beam* node and adds it to the scene.

      :param name: Name for the node, should be unique
      :param slave: Slaved axis system [Axis]
      :param master: Master axis system [Axis]
      :param All stiffness terms default to 0:
      :param The length defaults to the distance between master and slave:

      See :py:class:`LinearBeam` for details

      :returns: Reference to newly created beam


   .. method:: new_buoyancy(self, name, parent=None)


      Creates a new *buoyancy* node and adds it to the scene.

      :param name: Name for the node, should be unique
      :param parent: optional, name of the parent of the node

      :returns: Reference to newly created buoyancy


   .. method:: new_contactmesh(self, name, parent=None)


      Creates a new *contactmesh* node and adds it to the scene.

      :param name: Name for the node, should be unique
      :param parent: optional, name of the parent of the node

      :returns: Reference to newly created contact mesh


   .. method:: new_contactball(self, name, parent=None, radius=1, k=9999, meshes=None)


      Creates a new *force* node and adds it to the scene.

      :param name: Name for the node, should be unique
      :param parent: name of the parent of the node [Poi]
      :param force: optional, global force on the node (x,y,z)
      :param moment: optional, global force on the node (x,y,z)

      :returns: Reference to newly created force


   .. method:: new_ballastsystem(self, name, parent=None, position=None)


      Creates a new *rigidbody* node and adds it to the scene.

      :param name: Name for the node, should be unique
      :param parent: name of the parent of the ballast system (ie: the vessel axis system)
      :param position: the reference system in which the tanks are defined [0,0,0]

      .. rubric:: Examples

      scene.new_ballastsystem("cheetah_ballast", parent="Cheetah")

      :returns: Reference to newly created BallastSystem


   .. method:: new_sling(self, name, length=-1, EA=1.0, mass=0.1, endA=None, endB=None, LeyeA=None, LeyeB=None, LspliceA=None, LspliceB=None, diameter=0.1, sheaves=None)


      Creates a new sling, adds it to the scene and returns a reference to the newly created object.

      .. seealso:: Sling

      :param name: name
      :param length: length of the sling [m], defaults to distance between endpoints
      :param EA: stiffness in kN, default: 1.0 (note: equilibrium will fail if mass >0 and EA=0)
      :param mass: mass in mT, default  0.1
      :param endA: element to connect end A to [poi, circle]
      :param endB: element to connect end B to [poi, circle]
      :param LeyeA: inside eye on side A length [m], defaults to 1/6th of length
      :param LeyeB: inside eye on side B length [m], defaults to 1/6th of length
      :param LspliceA: splice length on side A [m] (the part where the cable is connected to itself)
      :param LspliceB: splice length on side B [m] (the part where the cable is connected to itself)
      :param diameter: cable diameter in m, defaul to 0.1
      :param sheaves: optional: list of sheaves/pois that the sling runs over

      :returns: a reference to the newly created Sling object.


   .. method:: print_python_code(self)


      Prints the python code that generates the current scene

      See also: give_python_code


   .. method:: give_python_code(self)


      Generates the python code that rebuilds the scene and elements in its current state.


   .. method:: save_scene(self, filename)


      Saves the scene to a file

      This saves the scene in its current state to a file.
      Opening the saved file will reproduce exactly this scene.

      This sounds nice, but beware that it only saves the resulting model, not the process of creating the model.
      This means that if you created the model in a parametric fashion or assembled the model from other models then these are not re-evaluated when the model is openened again.
      So lets say this model uses a sub-model of a lifting hook which is imported from another file. If that other file is updated then
      the results of that update will not be reflected in the saved model.

      If no path is present in the file-name then the model will be saved in the last (lowest) resource-path (if any)

      :param filename: filename or file-path to save the file. Default extension is .dave_asset

      :returns: the full path to the saved file


   .. method:: print_node_tree(self)



   .. method:: load_scene(self, filename=None)


      Loads the contents of filename into the current scene.

      This function is typically used on an empty scene.

      Filename is appended with .dave if needed.
      File is searched for in the resource-paths.

      See also: import scene


   .. method:: import_scene(self, other, prefix='', containerize=True)


      Copy-paste all nodes of scene "other" into current scene.

      To avoid double names it is recommended to use a prefix. This prefix will be added to all element names.

      :returns: if the imported scene is containerized then a reference to the created container is returned.
      :rtype: Contained (Axis-type Node)


   .. method:: copy(self)


      Creates a full and independent copy of the scene and returns it.

      .. rubric:: Example

      s = Scene()
      c = s.copy()
      c.new_axis('only in c')


   .. method:: dynamics_M(self, delta=1e-06)


      Returns the mass matrix of the scene


   .. method:: dynamics_K(self, delta=1e-06)


      Returns the stiffness matrix of the scene for a perturbation of delta

      A component is positive if a displacement introduces an reaction force in the opposite direction.
      or:
      A component is positive if a positive force is needed to introduce a positive displacement.


   .. method:: dynamics_nodes(self)


      Returns a list of nodes associated with the rows/columns of M and K


   .. method:: dynamics_modes(self)


      Returns a list of modes (0=x ... 5=rotation z) associated with the rows/columns of M and K



.. function:: assertBool(var, name='Variable')


.. function:: is_number(var)


.. function:: assert1f(var, name='Variable')


.. function:: assert1f_positive_or_zero(var, name='Variable')


.. function:: assert1f_positive(var, name='Variable')


.. function:: assert3f(var, name='Variable')

   Asserts that variable has length three and contains only numbers


.. function:: assert3f_positive(var, name='Variable')

   Asserts that variable has length three and contains only numbers


.. function:: assert6f(var, name='Variable')

   Asserts that variable has length six and contains only numbers


.. function:: assertValidName(var)


.. function:: assertPoi(var, name='Node')


.. function:: make_iterable(v)

   Makes an variable iterable by putting it in a list if needed


.. function:: radii_to_positions(rxx, ryy, rzz)

   decouple radii of gyration into six point discrete positions


.. function:: rotation_from_y_axis_direction(direction)

   Returns a rotation vector that rotates the Y-axis (0,1,0) into the given direction


.. function:: create_shackle_gphd(s, name, wll)

   Green-Pin Heavy Duty Bow Shackle BN

   visual from: https://www.traceparts.com/en/product/green-pinr-p-6036-green-pinr-heavy-duty-bow-shackle-bn-hdgphm0800-mm?CatalogPath=TRACEPARTS%3ATP04001002006&Product=10-04072013-086517&PartNumber=HDGPHM0800
   details from: https://www.greenpin.com/sites/default/files/2019-04/brochure-april-2019.pdf

   wll a b c d e f g h i j k weight
   [t] [mm]  [kg]
   120 95 95 208 95 147 400 238 647 453 428 50 110
   150 105 108 238 105 169 410 275 688 496 485 50 160
   200 120 130 279 120 179 513 290 838 564 530 70 235
   250 130 140 299 130 205 554 305 904 614 565 70 295
   300 140 150 325 140 205 618 305 996 644 585 80 368
   400 170 175 376 164 231 668 325 1114 690 665 70 560
   500 180 185 398 164 256 718 350 1190 720 710 70 685
   600 200 205 444 189 282 718 375 1243 810 775 70 880
   700 210 215 454 204 308 718 400 1263 870 820 70 980
   800 210 220 464 204 308 718 400 1270 870 820 70 1100
   900 220 230 485 215 328 718 420 1296 920 860 70 1280
   1000 240 240 515 215 349 718 420 1336 940 900 70 1460
   1250 260 270 585 230 369 768 450 1456 1025 970 70 1990
   1500 280 290 625 230 369 818 450 1556 1025 1010 70 2400

   Returns:


