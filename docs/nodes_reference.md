#### BallastSystem
The BallastSystemNode is a non-physical node that marks a groups of Tank nodes as being the ballast system
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


    

|  Property | Read-Only  | Documentation 
|:---------------- |:------------------------------- |:---------------- |
target_elevation |  | The target elevation of the parent of the ballast system.|
cogx | Read-only | X position of combined CoG of all tank contents in the ballast-system. (global coordinate) [m]|
cogy | Read-only | Y position of combined CoG of all tank contents in the ballast-system. (global coordinate) [m]|
cogz | Read-only | Z position of combined CoG of all tank contents in the ballast-system. (global coordinate) [m]|
cog | Read-only | Combined CoG of all tank contents in the ballast-system. (global coordinate) [m,m,m]|
weight | Read-only | Total weight of all tank fillings in the ballast system [kN]|
#### Beam
A LinearBeam models a FEM-like linear beam element.

    A LinearBeam node connects two Axis elements

    By definition the beam runs in the X-direction of the nodeA axis system. So it may be needed to create a
    dedicated Axis element for the beam to control the orientation.

    The beam is defined using the following properties:

    *  EIy  - bending stiffness about y-axis
    *  EIz  - bending stiffness about z-axis
    *  GIp  - torsional stiffness about x-axis
    *  EA   - axis stiffness in x-direction
    *  L    - the un-stretched length of the beam
    *  mass - mass of the beam in [mT]

    The beam element is in rest if the nodeB axis system

    1. has the same global orientation as the nodeA system
    2. is at global position equal to the global position of local point (L,0,0) of the nodeA axis. (aka: the end of the beam)

    The scene.new_linearbeam automatically creates a dedicated axis system for each end of the beam. The orientation of this axis-system
    is determined as follows:

    First the direction from nodeA to nodeB is determined: D
    The axis of rotation is the cross-product of the unit x-axis and D    AXIS = ux x D
    The angle of rotation is the angle between the nodeA x-axis and D
    The rotation about the rotated X-axis is undefined.

    

|  Property | Read-Only  | Documentation 
|:---------------- |:------------------------------- |:---------------- |
n_segments |  | Number of segments used in beam [-]|
EIy |  | E * Iyy : bending stiffness in the XZ plane [kN m2]<br><br>        E is the modulus of elasticity; for steel 190-210 GPa (10^6 kN/m2)<br>        Iyy is the cross section moment of inertia [m4]<br>        |
EIz |  | E * Izz : bending stiffness in the XY plane [kN m2]<br><br>        E is the modulus of elasticity; for steel 190-210 GPa (10^6 kN/m2)<br>        Iyy is the cross section moment of inertia [m4]<br>        |
GIp |  | G * Ipp : torsional stiffness about the X (length) axis [kN m2]<br><br>        G is the shear-modulus of elasticity; for steel 75-80 GPa (10^6 kN/m2)<br>        Ip is the cross section polar moment of inertia [m4]<br>        |
EA |  | E * A : stiffness in the length direction [kN]<br><br>        E is the modulus of elasticity; for steel 190-210 GPa (10^6 kN/m2)<br>        A is the cross-section area in [m2]<br>        |
tension_only |  | axial stiffness (EA) only applicable to tension [True/False]|
mass |  | Mass of the beam in [mT]|
L |  | Length of the beam in unloaded condition [m]|
nodeA |  | The axis system that the A-end of the beam is connected to. The beam leaves this axis system along the X-axis<br>        |
nodeB |  | The axis system that the B-end of the beam is connected to. The beam arrives at this axis system along the X-axis<br>        |
moment_A | Read-only | Moment on beam at node A (kNm, kNm, kNm) , axis system of node A|
moment_B | Read-only | Moment on beam at node B (kNm, kNm, kNm) , axis system of node B|
tension | Read-only | Tension in the beam [kN], negative for compression<br><br>        tension is calculated at the midpoints of the beam segments.<br>        |
torsion | Read-only | Torsion moment [kNm]. Positive if end B has a positive rotation about the x-axis of end A<br><br>        torsion is calculated at the midpoints of the beam segments.<br>        |
X_nodes | Read-only | Returns the x-positions of the end nodes and internal nodes along the length of the beam [m]|
X_midpoints | Read-only | X-positions of the beam centers measured along the length of the beam [m]|
global_positions | Read-only | Global-positions of the end nodes and internal nodes [m,m,m]|
global_orientations | Read-only | Global-orientations of the end nodes and internal nodes [deg,deg,deg]|
bending | Read-only | Bending forces of the end nodes and internal nodes [0, kNm, kNm]|
#### Buoyancy
Buoyancy provides a buoyancy force based on a buoyancy mesh. The mesh is triangulated and chopped at the instantaneous flat water surface. Buoyancy is applied as an upwards force that the center of buoyancy.
    The calculation of buoyancy is as accurate as the provided geometry.

    There as no restrictions to the size or aspect ratio of the panels. It is excellent to model as box using 6 faces. Using smaller panels has a negative effect on performance.

    The normals of the panels should point towards to water.
    

|  Property | Read-Only  | Documentation 
|:---------------- |:------------------------------- |:---------------- |
trimesh | Read-only | Reference to TriMeshSource object<br>        |
cob | Read-only | GLOBAL position of the center of buoyancy [m,m,m] (global axis)|
cob_local | Read-only | Position of the center of buoyancy [m,m,m] (local axis)|
displacement | Read-only | Displaced volume of fluid [m^3]|
#### Cable
A Cable represents a linear elastic wire running from a Poi or sheave to another Poi of sheave.

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


    

|  Property | Read-Only  | Documentation 
|:---------------- |:------------------------------- |:---------------- |
tension | Read-only | Tension in the cable [kN]|
stretch | Read-only | Stretch of the cable [m]<br><br>        Tension [kN] = EA [kN] * stretch [m] / length [m]<br>        |
actual_length | Read-only | Current length of the cable: length + stretch [m]|
length |  | Length of the cable when in rest [m]<br><br>        Tension [kN] = EA [kN] * stretch [m] / length [m]<br>        |
EA |  | Stiffness of the cable [kN]<br><br>        Tension [kN] = EA [kN] * stretch [m] / length [m]<br>        |
diameter |  | Diameter of the cable. Used when a cable runs over a circle. [m]|
connections |  | List or Tuple of nodes that this cable is connected to. Nodes may be passed by name (string) or by reference.<br><br>        Example:<br>            p1 = s.new_point('point 1')<br>            p2 = s.new_point('point 2', position = (0,0,10)<br>            p3 = s.new_point('point 3', position = (10,0,10)<br>            c1 = s.new_circle('circle 1',parent = p3, axis = (0,1,0), radius = 1)<br>            c = s.new_cable("cable_1", endA="Point", endB = "Circle", length = 1.2, EA = 10000)<br><br>            c.connections = ('point 1', 'point 2', 'point 3')<br>            # or<br>            c.connections = (p1, p2,p3)<br>            # or<br>            c.connections = [p1, 'point 2', p3]  # all the same<br><br>        Notes:<br>            1. Circles can not be used as endpoins. If one of the endpoints is a Circle then the Point that that circle<br>            is located on is used instead.<br>            2. Points should not be repeated directly.<br><br>        The following will fail:<br>        c.connections = ('point 1', 'point 3', 'circle 1')<br><br>        because the last point is a circle. So circle 1 will be replaced with the point that the circle is on: point 3.<br><br>        so this becomes<br>        ('point 1','point 3','point 3')<br><br>        this is invalid because point 3 is repeated.<br>        <br>        |
#### Circle
A Circle models a circle shape based on a diameter and an axis direction

|  Property | Read-Only  | Documentation 
|:---------------- |:------------------------------- |:---------------- |
axis |  | Direction of the sheave axis (x,y,z) in parent axis system.<br><br>        Note:<br>            The direction of the axis is also used to determine the positive direction over the circumference of the<br>            circle. This is then used when cables run over the circle or the circle is used for geometric contacts. So<br>            if a cable runs over the circle in the wrong direction then a solution is to change the axis direction to<br>            its opposite:  circle.axis =- circle.axis. (another solution in that case is to define the connections of<br>            the cable in the reverse order)<br>        |
radius |  | Radius of the circle [m]|
global_position | Read-only | Returns the global position of the center of the sheave.<br><br>        Note: this is the same as the global position of the parent point.<br>        |
position | Read-only | Returns the local position of the center of the sheave.<br><br>        Note: this is the same as the local position of the parent point.<br>        |
#### Component
Components are frame-nodes containing a scene. The imported scene is referenced by a file-name. All impored nodes
    are placed in the components frame.
    

|  Property | Read-Only  | Documentation 
|:---------------- |:------------------------------- |:---------------- |
name |  | Name of the node (str), must be unique<br>        |
path |  | Path of the model-file. For example res: padeye.dave|
#### Connector2d
A Connector2d linear connector with acts both on linear displacement and angular displacement.

    * the linear stiffness is defined by k_linear and is defined over the actual shortest direction between nodeA and nodeB.
    * the angular stiffness is defined by k_angular and is defined over the actual smallest angle between the two systems.
    

|  Property | Read-Only  | Documentation 
|:---------------- |:------------------------------- |:---------------- |
angle | Read-only | Actual angle between nodeA and nodeB [deg] (read-only)|
force | Read-only | Actual force between nodeA and nodeB [kN] (read-only)|
moment | Read-only | Actual moment between nodeA and nodeB [kNm] (read-only)|
axis | Read-only | Actual rotation axis between nodeA and nodeB (read-only)|
ax | Read-only | X component of actual rotation axis between nodeA and nodeB (read-only)|
ay | Read-only | Y component of actual rotation axis between nodeA and nodeB (read-only)|
az | Read-only | Z component of actual rotation axis between nodeA and nodeB (read-only)|
k_linear |  | Linear stiffness [kN/m]|
k_angular |  | Angular stiffness [kNm/rad]|
nodeA |  | Connected axis system A<br>        |
nodeB |  | Connected axis system B<br>        |
#### ContactBall
A ContactBall is a linear elastic ball which can contact with ContactMeshes.

    It is modelled as a sphere around a Poi. Radius and stiffness can be controlled using radius and k.

    The force is applied on the Poi and it not registered separately.
    

|  Property | Read-Only  | Documentation 
|:---------------- |:------------------------------- |:---------------- |
can_contact | Read-only | True if the ball is currently perpendicular to at least one of the faces of one of the meshes. So when contact is possible. To check if there is contact use "force".<br>        See Also: Force<br>        |
contact_force | Read-only | Returns the force on the ball [kN, kN, kN] (global axis)<br><br>        The force is applied at the center of the ball<br><br>        See Also: contact_force_magnitude<br>        |
contact_force_magnitude | Read-only | Returns the absolute force on the ball, if any [kN]<br><br>        The force is applied on the center of the ball<br><br>        See Also: contact_force<br>        |
compression | Read-only | Returns the absolute compression of the ball, if any [m]|
contactpoint | Read-only | The nearest point on the nearest mesh. Only defined|
meshes |  | List of contact-mesh nodes.<br>        When getting this will yield a list of node references.<br>        When setting node references and node-names may be used.<br><br>        eg: ball.meshes = [mesh1, 'mesh2']<br>        |
meshes_names | Read-only | List with the names of the meshes|
radius |  | Radius of the contact-ball [m]|
k |  | Compression stiffness of the ball in force per meter of compression [kN/m]|
#### ContactMesh
A ContactMesh is a tri-mesh with an axis parent

|  Property | Read-Only  | Documentation 
|:---------------- |:------------------------------- |:---------------- |
trimesh | Read-only | The TriMeshSource object which can be used to change the mesh<br><br>        Example:<br>            s['Contactmesh'].trimesh.load_file('cube.obj', scale = (1.0,1.0,1.0), rotation = (0.0,0.0,0.0), offset = (0.0,0.0,0.0))<br>        |
#### CurrentArea
Abstract Based class for wind and current areas.

|  Property | Read-Only  | Documentation 
|:---------------- |:------------------------------- |:---------------- |
force | Read-only | The x,y and z components of the force [kN,kN,kN] (global axis)|
fx | Read-only | The global x-component of the force [kN] (global axis)|
fy | Read-only | The global y-component of the force [kN]  (global axis)|
fz | Read-only | The global z-component of the force [kN]  (global axis)|
A |  | Total area [m2]. See also Ae|
Ae | Read-only | Effective area [m2]. This is the projection of the total to the actual wind/current direction. Read only.|
Cd |  | Cd coefficient [-]|
direction |  | Depends on 'areakind'. For 'plane' this is the direction of the normal of the plane, for 'cylindrical' this is<br>        the direction of the axis and for 'sphere' this is not used [m,m,m]|
areakind |  | Defines how to interpret the area.<br>        See also: `direction`|
#### Force
A Force models a force and moment on a poi.

    Both are expressed in the global axis system.

    

|  Property | Read-Only  | Documentation 
|:---------------- |:------------------------------- |:---------------- |
force |  | The x,y and z components of the force [kN,kN,kN] (global axis)<br><br>        Example s['wind'].force = (12,34,56)<br>        |
fx |  | The global x-component of the force [kN] (global axis)|
fy |  | The global y-component of the force [kN]  (global axis)|
fz |  | The global z-component of the force [kN]  (global axis)|
moment |  | The x,y and z components of the moment (kNm,kNm,kNm) in the global axis system.<br><br>        Example s['wind'].moment = (12,34,56)<br>        |
mx |  | The global x-component of the moment [kNm]  (global axis)|
my |  | The global y-component of the moment [kNm]  (global axis)|
mz |  | The global z-component of the moment [kNm]  (global axis)|
#### Frame

    Axis

    Axes are the main building blocks of the geometry. They have a position and an rotation in space. Other nodes can be placed on them.
    Axes can be nested by parent/child relationships meaning that an axis can be placed on an other axis.
    The possible movements of an axis can be controlled in each degree of freedom using the "fixed" property.

    Axes are also the main building block of inertia.
    Dynamics are controlled using the inertia properties of an axis: inertia [mT], inertia_position[m,m,m] and inertia_radii [m,m,m]


    Notes:
         - circular references are not allowed: It is not allowed to place a on b and b on a

    

|  Property | Read-Only  | Documentation 
|:---------------- |:------------------------------- |:---------------- |
inertia |  | The linear inertia of the axis in [mT] Aka: "Mass"<br>        - used only for dynamics|
inertia_position |  | The position of the center of inertia. Aka: "cog" [m,m,m] (local axis)<br>        - used only for dynamics<br>        - defined in local axis system|
inertia_radii |  | The radii of gyration of the inertia [m,m,m] (local axis)<br><br>        Used to calculate the mass moments of inertia via<br><br>        Ixx = rxx^2 * inertia<br>        Iyy = rxx^2 * inertia<br>        Izz = rxx^2 * inertia<br><br>        Note that DAVE does not directly support cross terms in the interia matrix of an axis system. If you want to<br>        use cross terms then combine multiple axis system to reach the same result. This is because inertia matrices with<br>        diagonal terms can not be translated.<br>        |
fixed |  | Determines which of the six degrees of freedom are fixed, if any. (x,y,z,rx,ry,rz).<br>        True means that that degree of freedom will not change when solving statics.<br>        False means a that is may be changed in order to find equilibrium.<br><br>        These are the expressed on the coordinate system of the parent (if any) or the global axis system (if no parent)<br><br>        See Also: set_free, set_fixed<br>        |
fixed_x |  | Restricts/allows movement in x direction of parent|
fixed_y |  | Restricts/allows movement in y direction of parent|
fixed_z |  | Restricts/allows movement in z direction of parent|
fixed_rx |  | Restricts/allows movement about x direction of parent|
fixed_ry |  | Restricts/allows movement about y direction of parent|
fixed_rz |  | Restricts/allows movement about z direction of parent|
x |  | The x-component of the position vector (parent axis) [m]|
y |  | The y-component of the position vector (parent axis) [m]|
z |  | The z-component of the position vector (parent axis) [m]|
position |  | Position of the axis (parent axis) [m,m,m]<br><br>        These are the expressed on the coordinate system of the parent (if any) or the global axis system (if no parent)|
rx |  | The x-component of the rotation vector [degrees] (parent axis)|
ry |  | The y-component of the rotation vector [degrees] (parent axis)|
rz |  | The z-component of the rotation vector [degrees], (parent axis)|
rotation |  | Rotation of the axis about its origin (rx,ry,rz).<br>        Defined as a rotation about an axis where the direction of the axis is (rx,ry,rz) and the angle of rotation is |(rx,ry,rz| degrees.<br>        These are the expressed on the coordinate system of the parent (if any) or the global axis system (if no parent)|
parent |  | Determines the parent of the axis. Should either be another axis or 'None'<br><br>        Other axis may be refered to by reference or by name (str). So the following are identical<br><br>            p = s.new_frame('parent_axis')<br>            c = s.new_frame('child axis')<br><br>            c.parent = p<br>            c.parent = 'parent_axis'<br><br>        To define that an axis does not have a parent use<br><br>            c.parent = None<br><br>        |
gx |  | The x-component of the global position vector [m] (global axis )|
gy |  | The y-component of the global position vector [m] (global axis )|
gz |  | The z-component of the global position vector [m] (global axis )|
global_position |  | The global position of the origin of the axis system  [m,m,m] (global axis)|
grx |  | The x-component of the global rotation vector [degrees] (global axis)|
gry |  | The y-component of the global rotation vector [degrees] (global axis)|
grz |  | The z-component of the global rotation vector [degrees] (global axis)|
tilt_x | Read-only | Tilt percentage about local x-axis [%]<br>        This is the z-component of the unit y vector.<br><br>        See Also: heel, tilt_y<br>        |
heel | Read-only | Heel in degrees. SB down is positive [deg]<br>        This is the inverse sin of the unit y vector(This is the arcsin of the tiltx)<br><br>        See also: tilt_x<br>        |
tilt_y | Read-only | Tilt percentage about local y-axis [%]<br><br>        This is the z-component of the unit -x vector.<br>        So a positive rotation about the y axis results in a positive tilt_y.<br><br>        See Also: trim<br>        |
trim | Read-only | Trim in degrees. Bow-down is positive [deg]<br><br>        This is the inverse sin of the unit -x vector(This is the arcsin of the tilt_y)<br><br>        See also: tilt_y<br>        |
heading | Read-only | Direction (0..360) [deg] of the local x-axis relative to the global x axis. Measured about the global z axis<br><br>        heading = atan(u_y,u_x)<br><br>        typically:<br>            heading 0  --> local axis align with global axis<br>            heading 90 --> local x-axis in direction of global y axis<br><br><br>        See also: heading_compass<br>        |
heading_compass | Read-only | The heading (0..360)[deg] assuming that the global y-axis is North and global x-axis is East and rotation accoring compass definition|
global_rotation |  | Rotation [deg,deg,deg] (global axis)|
global_transform | Read-only | Read-only: The global transform of the axis system [matrix]<br>        |
connection_force | Read-only | The forces and moments that this axis applies on its parent at the origin of this axis system. [kN, kN, kN, kNm, kNm, kNm] (Parent axis)<br><br>        If this axis would be connected to a point on its parent, and that point would be located at the location of the origin of this axis system<br>        then the connection force equals the force and moment applied on that point.<br><br>        Example:<br>            parent axis with name A<br>            this axis with name B<br>            this axis is located on A at position (10,0,0)<br>            there is a Point at the center of this axis system.<br>            A force with Fz = -10 acts on the Point.<br><br>            The connection_force is (-10,0,0,0,0,0)<br><br>            This is the force and moment as applied on A at point (10,0,0)<br><br><br>        |
connection_force_x | Read-only | The x-component of the connection-force vector [kN] (Parent axis)|
connection_force_y | Read-only | The y-component of the connection-force vector [kN] (Parent axis)|
connection_force_z | Read-only | The z-component of the connection-force vector [kN] (Parent axis)|
connection_moment_x | Read-only | The mx-component of the connection-force vector [kNm] (Parent axis)|
connection_moment_y | Read-only | The my-component of the connection-force vector [kNm] (Parent axis)|
connection_moment_z | Read-only | The mx-component of the connection-force vector [kNm] (Parent axis)|
applied_force | Read-only | The force and moment that is applied on origin of this axis [kN, kN, kN, kNm, kNm, kNm] (Global axis)|
ux | Read-only | The unit x axis [m,m,m] (Global axis)|
uy | Read-only | The unit y axis [m,m,m] (Global axis)|
uz | Read-only | The unit z axis [m,m,m] (Global axis)|
equilibrium_error | Read-only | The remaining force and moment on this axis. Should be zero when in equilibrium  (applied-force minus connection force, Parent axis)|
#### GeometricContact

    GeometricContact

    A GeometricContact can be used to construct geometric connections between circular members:
        - 	steel bars and holes, such as a shackle pin in a padeye (pin-hole)
        -	steel bars and steel bars, such as a shackle-shackle connection


    Situation before creation of geometric contact:

    Axis1
        Point1
            Circle1
    Axis2
        Point2
            Circle2

    Create a geometric contact with Circle1 and parent and Circle2 as child

    Axis1
        Point1              : observed, referenced as parent_circle_parent
            Circle1         : observed, referenced as parent_circle

        _axis_on_parent                 : managed
            _pin_hole_connection        : managed
                _connection_axial_rotation : managed
                    _axis_on_child      : managed
                        Axis2           : managed    , referenced as child_circle_parent_parent
                            Point2      : observed   , referenced as child_circle_parent
                                Circle2 : observed   , referenced as child_circle







    

|  Property | Read-Only  | Documentation 
|:---------------- |:------------------------------- |:---------------- |
name |  | Name of the node (str), must be unique<br>        |
child |  | The Circle that is connected to the GeometricContact [Node]<br><br>        See Also: parent<br>        <br>        |
parent |  | The Circle that the GeometricConnection is connected to [Node]<br><br>        See Also: child<br>        <br>        |
swivel |  | Swivel angle between parent and child objects [degrees]|
swivel_fixed |  | Allow parent and child to swivel relative to eachother [boolean]|
rotation_on_parent |  | Angle between the line connecting the centers of the circles and the axis system of the parent node [degrees]|
fixed_to_parent |  | Allow rotation around parent [boolean]<br><br>        see also: rotation_on_parent|
child_rotation |  | Angle between the line connecting the centers of the circles and the axis system of the child node [degrees]|
child_fixed |  | Allow rotation of child relative to connection, see also: child_rotation [boolean]|
inside |  | Type of connection: True means child circle is inside parent circle, False means the child circle is outside but the circumferences contact [boolean]|
#### HydSpring
A HydSpring models a linearized hydrostatic spring.

    The cob (center of buoyancy) is defined in the parent axis system.
    All other properties are defined relative to the cob.

    

|  Property | Read-Only  | Documentation 
|:---------------- |:------------------------------- |:---------------- |
cob |  | Center of buoyancy in parent axis system (m,m,m)|
BMT |  | Vertical distance between cob and metacenter for roll [m]|
BML |  | Vertical distance between cob and metacenter for pitch [m]|
COFX |  | Horizontal x-position Center of Floatation (center of waterplane area), relative to cob [m]|
COFY |  | Horizontal y-position Center of Floatation (center of waterplane area), relative to cob [m]|
kHeave |  | Heave stiffness [kN/m]|
waterline |  | Waterline-elevation relative to cob for un-stretched heave-spring. Positive if cob is below the waterline (which is where is normally is) [m]|
displacement_kN |  | Displacement when waterline is at waterline-elevation [kN]|
#### LC6d
A LC6d models a Linear Connector with 6 dofs.

    It connects two Axis elements with six linear springs.

    The first axis system is called "main", the second is called "secondary". The difference is that
    the "main" axis system is used for the definition of the stiffness values.

    The translational-springs are easy. The rotational springs may not be as intuitive. They are defined as:

      - rotation_x = arc-tan ( uy[0] / uy[1] )
      - rotation_y = arc-tan ( -ux[0] / ux[2] )
      - rotation_z = arc-tan ( ux[0] / ux [1] )

    which works fine for small rotations and rotations about only a single axis.

    Tip:
    It is better to use use the "fixed" property of axis systems to create joints.

    

|  Property | Read-Only  | Documentation 
|:---------------- |:------------------------------- |:---------------- |
stiffness |  | Stiffness of the connector: kx, ky, kz, krx, kry, krz in [kN/m and kNm/rad] (axis system of the main axis)|
main |  | Main axis system. This axis system dictates the axis system that the stiffness is expressed in<br>        |
secondary |  | Secondary (connected) axis system<br>        |
fgx | Read-only | Force on main in global coordinate frame [kN]|
fgy | Read-only | Force on main in global coordinate frame [kN]|
fgz | Read-only | Force on main in global coordinate frame [kN]|
force_global | Read-only | Force on main in global coordinate frame [kN]|
mgx | Read-only | Moment on main in global coordinate frame [kNm]|
mgy | Read-only | Moment on main in global coordinate frame [kNm]|
mgz | Read-only | Moment on main in global coordinate frame [kNm]|
moment_global | Read-only | Moment on main in global coordinate frame [kNm]|
#### Point
A location on an axis

|  Property | Read-Only  | Documentation 
|:---------------- |:------------------------------- |:---------------- |
x |  | x component of local position [m] (parent axis)|
y |  | y component of local position [m] (parent axis)|
z |  | z component of local position [m] (parent axis)|
applied_force | Read-only | Applied force [kN,kN,kN] (parent axis)|
force | Read-only | total force magnitude as applied on the point [kN]|
fx | Read-only | x component of applied force [kN] (parent axis)|
fy | Read-only | y component of applied force [kN] (parent axis)|
fz | Read-only | z component of applied force [kN] (parent axis)|
applied_moment | Read-only | Applied moment [kNm,kNm,kNm] (parent axis)|
moment | Read-only | total moment magnitude as applied on the point [kNm]|
mx | Read-only | x component of applied moment [kNm] (parent axis)|
my | Read-only | y component of applied moment [kNm] (parent axis)|
mz | Read-only | z component of applied moment [kNm] (parent axis)|
position |  | Local position [m,m,m] (parent axis)|
applied_force_and_moment_global | Read-only | Applied force and moment on this point [kN, kN, kN, kNm, kNm, kNm] (Global axis)|
gx |  | x component of position [m] (global axis)|
gy |  | y component of position [m] (global axis)|
gz |  | z component of position [m] (global axis)|
global_position |  | Global position [m,m,m] (global axis)|
#### RigidBody
A Rigid body, internally composed of an axis, a point (cog) and a force (gravity)

|  Property | Read-Only  | Documentation 
|:---------------- |:------------------------------- |:---------------- |
name |  | Name of the node (str), must be unique<br>        |
footprint |  | Sets the footprint vertices. Supply as an iterable with each element containing three floats|
cogx |  | x-component of cog position [m] (local axis)|
cogy |  | y-component of cog position [m] (local axis)|
cogz |  | z-component of cog position [m] (local axis)|
cog |  | Center of Gravity position [m,m,m] (local axis)|
mass |  | Static mass of the body [mT]<br><br>        See Also: inertia<br>        |
#### SPMT
An SPMT is a Self-propelled modular transporter

    These are platform vehicles

    ============  =======
    0 0 0 0 0 0   0 0 0 0

    This SPMT node models the wheels and hydraulics of a single suspension system.

    A set of wheels is called an "axle". The hydraulics are modelled as a linear spring.
    The axles can make contact with a contact shape.

    The positions of the axles are controlled by n_length, n_width, spacing_length and spacing_width.
    The hydraulics are controlled by reference_extension, reference_force and k.

    Setting use_friction to True (default) adds friction such that all contact-forces are purely vertical.
    Setting use_friction to False will make contact-forces perpendicular to the contacted surface.

    

|  Property | Read-Only  | Documentation 
|:---------------- |:------------------------------- |:---------------- |
force | Read-only | Returns the force component perpendicular to the SPMT in each of the axles (negative mean uplift) [kN]|
contact_force | Read-only | Returns the contact force in each of the axles (global) [kN,kN,kN]|
compression | Read-only | Returns the total compression (negative means uplift) [m]|
extensions | Read-only | Returns the extension of each of the axles (bottom of wheel to top of spmt) [m]|
max_extension | Read-only | Maximum extension of the axles [m]<br>        See Also: extensions|
min_extension | Read-only | Minimum extension of the axles [m]<br>        See Also: extensions|
n_width |  | number of axles in transverse direction|
n_length |  | number of axles in length direction|
spacing_width |  | distance between axles in transverse direction [m]|
spacing_length |  | distance between axles in length direction [m]|
reference_force |  | total force (sum of all axles) when at reference extension [kN]|
reference_extension |  | Distance between top of SPMT and bottom of wheel at which compression is zero [m]|
k |  | Vertical stiffness of all axles together [kN/m]|
use_friction |  | Apply friction between wheel and surface such that resulting force is vertical [True/False]<br>        False: Force is perpendicular to the surface<br>        True: Force is vertical<br>        |
meshes |  | List of contact-mesh nodes.<br>        When getting this will yield a list of node references.<br>        When setting node references and node-names may be used.<br><br>        eg: ball.meshes = [mesh1, 'mesh2']<br>        |
meshes_names | Read-only | List with the names of the meshes|
axles |  | Axles is a list axle positions. Each entry is a (x,y,z) entry which determines the location of the axle on<br>        SPMT. This is relative to the parent of the SPMT.<br><br>        Example:<br>            [(-10,0,0),(-5,0,0),(0,0,0)] for three axles<br>        |
#### Shackle

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

    

|  Property | Read-Only  | Documentation 
|:---------------- |:------------------------------- |:---------------- |
kind |  | Type of shackle, for example GP800 [text]|
name |  | Name of the node (str), must be unique<br>        |
#### Sling
A Sling is a single wire with an eye on each end. The eyes are created by splicing the end of the sling back
    into the itself.

    The geometry of a sling is defined as follows:

    diameter : diameter of the wire
    LeyeA, LeyeB : inside lengths of the eyes
    LsplicaA, LspliceB : the length of the splices
    Ultimate length : the distance between the insides of ends of the eyes A and B when pulled straight (= Ultimate Length).

    Stiffness:
    The stiffness of the sling is specified by a single value: EA. EA can be set directly or by providing a k_total
    This determines the stiffnesses of the individual parts as follows:
    Wire in the eyes: EA
    Splices: Infinity (rigid)

    See Also: Grommet

    

|  Property | Read-Only  | Documentation 
|:---------------- |:------------------------------- |:---------------- |
name |  | Name of the node (str), must be unique<br>        |
k_total |  | Total stiffness of the sling in kN/m|
length |  | Total length measured between the INSIDE of the eyes of the sling is pulled straight. [m]|
LeyeA |  | Total length inside eye A if stretched flat [m]|
LeyeB |  | Total length inside eye B if stretched flat [m]|
LspliceA |  | Length of the splice at end A [m]|
LspliceB |  | Length of the splice at end B [m]|
diameter |  | Diameter of the sling (except the splices) [m]|
EA |  | EA of the wire of the sling. See also: k_total|
mass |  | Mass and weight of the sling. This mass is discretized  distributed over the two splices [mT]|
endA |  | End A [circle or point node]<br>        |
endB |  | End B [circle or point node]<br>        |
sheaves |  | List of sheaves (circles, points) that the sling runs over between the two ends.<br><br>        May be provided as list of nodes or node-names.<br>        <br>        |
#### Tank
Tank provides a fillable tank based on a mesh. The mesh is triangulated and chopped at the instantaneous flat fluid surface. Gravity is applied as an downwards force that the center of fluid.
    The calculation of fluid volume and center is as accurate as the provided geometry.

    There as no restrictions to the size or aspect ratio of the panels. It is excellent to model as box using 6 faces. Using smaller panels has a negative effect on performance.

    The normals of the panels should point *away* from the fluid. This means that the same basic shapes can be used for both buoyancy and tanks.
    

|  Property | Read-Only  | Documentation 
|:---------------- |:------------------------------- |:---------------- |
trimesh | Read-only | The TriMeshSource object which can be used to change the mesh<br><br>            Example:<br>                s['Contactmesh'].trimesh.load_file('cube.obj', scale = (1.0,1.0,1.0), rotation = (0.0,0.0,0.0), offset = (0.0,0.0,0.0))<br>        |
free_flooding |  | Tank is filled till global waterline (aka: damaged) [bool]|
permeability |  | Permeability is the fraction of the enclosed volume that can be filled with fluid [-]|
cog | Read-only | Returns the GLOBAL position of the center of volume / gravity|
cog_local | Read-only | Returns the local position of the center of gravity|
cog_when_full | Read-only | Returns the LOCAL position of the center of volume / gravity of the tank when it is filled|
fill_pct |  | Amount of volume in tank as percentage of capacity [%]|
level_global |  | The fluid plane elevation in the global axis system. Setting this adjusts the volume|
volume |  | The actual volume of fluid in the tank in m3. Setting this adjusts the fluid level|
density |  | Density of the fluid in the tank in mT/m3|
capacity | Read-only | Returns the capacity of the tank in m3. This is calculated from the defined geometry and permeability.|
ullage | Read-only | Ullage of the tank [m].<br>        The ullage is the distance between a measurement point and the fluid surface. The point is [xf,yf,zv] where<br>        xf and yf are the x and y coordinates (local) of the center of fluid when the tank is full. zv is the largest z value<br>        of all the vertices of the tank.<br>        The measurement direction is in local z-direction. If the tank is under an angle then this is not perpendicular to the fluid.<br>        It is possible that this definition returns an ullage larger than the physical tank depth. In that case the physical depth of<br>        the tank is returned instead.<br>        |
#### TriMeshSource

    TriMesh

    A TriMesh node contains triangular mesh which can be used for buoyancy or contact

    

|  Property | Read-Only  | Documentation 
|:---------------- |:------------------------------- |:---------------- |
#### Visual

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

    

|  Property | Read-Only  | Documentation 
|:---------------- |:------------------------------- |:---------------- |
file_path | Read-only | Resolved path of the visual (str)<br>        |
#### WaveInteraction1

    WaveInteraction

    Wave-interaction-1 couples a first-order hydrodynamic database to an axis.

    This adds:
    - wave-forces
    - damping
    - added mass

    The data is provided by a Hyddb1 object which is defined in the MaFreDo package. The contents are not embedded
    but are to be provided separately in a file. This node contains only the file-name.

    

|  Property | Read-Only  | Documentation 
|:---------------- |:------------------------------- |:---------------- |
file_path | Read-only | Resolved path of the visual (str)<br>        |
#### WindArea
Abstract Based class for wind and current areas.

|  Property | Read-Only  | Documentation 
|:---------------- |:------------------------------- |:---------------- |
force | Read-only | The x,y and z components of the force [kN,kN,kN] (global axis)|
fx | Read-only | The global x-component of the force [kN] (global axis)|
fy | Read-only | The global y-component of the force [kN]  (global axis)|
fz | Read-only | The global z-component of the force [kN]  (global axis)|
A |  | Total area [m2]. See also Ae|
Ae | Read-only | Effective area [m2]. This is the projection of the total to the actual wind/current direction. Read only.|
Cd |  | Cd coefficient [-]|
direction |  | Depends on 'areakind'. For 'plane' this is the direction of the normal of the plane, for 'cylindrical' this is<br>        the direction of the axis and for 'sphere' this is not used [m,m,m]|
areakind |  | Defines how to interpret the area.<br>        See also: `direction`|