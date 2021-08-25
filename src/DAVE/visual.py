"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Ruben de Bruin - 2019

"""
from copy import copy
from typing import List

import numpy as np
from enum import Enum
from scipy.spatial import ConvexHull

import vtkmodules.qt
vtkmodules.qt.PyQtImpl = "PySide2"

import vedo as vp  # ref: https://github.com/marcomusy/vedo
import vtk

from DAVE.settings_visuals import (
    ViewportSettings,
    ActorSettings,
    RESOLUTION_SPHERE,
    RESOLUTION_ARROW,
    COLOR_BG1,
    COLOR_BG2,
    COLOR_WATER,
    TEXTURE_SEA,
    VISUAL_BUOYANCY_PLANE_EXTEND,
    COLOR_SELECT,
    LIGHT_TEXTURE_SKYBOX,
    ALPHA_SEA,
    COLOR_SELECT_255
)


# vp.settings.renderLinesAsTubes = True

import DAVE.scene as vf
import DAVE.scene as dn



"""
visual visualizes a scene using vtk and vedo helpers

Basic data structure:

Viewport
 - node_visuals (VisualActors)
    - [node] -> reference to corresponding node 
    - actors [dict]
        - [ActorType]
        
        <the appearance of these visuals is determined by painers which are activated by update_visibility>
        
 - temporary_visuals (VisualActors)
    These are visuals that are temporary added to the viewport. For example a moment-line or boundary edges of a mesh
    these are automatically deleted when the viewport is updated (position_visuals) 
        
 - private visuals (wave-plane, etc)
 
       <the appearance of these visuals is determined by Viewport>
       <set by update_global_visibility which is called bt update_visibility>




Viewport
============

Viewport is the main class which handles the viewport (ie: Plotter).
It supports embedded plotting (in a qt application) as well as stand-alone or via Jupyter or Renders (offscreen renderer)

A viewport contains VisualActors.


Visual-Actors
------------------

this class contains a reference to a Node (optional) and a dict of actors

Dict of actors: On of them is always called "main". This is used, among others, to determine the position of the label (if any) 
    

a visual actor can be hidden by setting visible to False

each of the individual vtk-plotter actors has a "actor_type" property which is a enum ActorType.

ActorType is used for general control of these actors. At the moment this is only Scaling which is implemented in "position visuals"


VISUALS FOR NODES
==================



     each actor:
       - may have an ActorType property. This is yet another way to tell what kind of feature the visual represents
    - has a property "node"
   


- A visual representing a Node has its node property set to a node (not None).
  appearance of these nodes is controlled by Painters.
- The visibility of these nodes may be overridden by the .visible setting of the node.
  
  
   
    Updates the visibility settings for all of the actors
    A visual can be hidden completely by setting visible to false
    An actor can be hidden depending on the actor-type using ????  <-- obsolete
        
        


Creating and updating actors
-----------------------------

Creating and updating of actors is done by Viewport:

When a new viewport has been created:
- create_world_actors : Creates the global scenery

When new nodes are added to the screen:
- create_visuals      : Creates actors for nodes in the scene that do not yet have one

When the nodes in the scene have moved:
- position_visuals    : Updates the positions of existing visuals
                        Removes visuals for which the node is no longer present in the scene
                        Applies scaling for non-physical actors
                        Updates the geometry for visuals where needed (meshes)
                        Updates the "paint_state" property for tanks and contact nodes (see paint)
                        
When the nodes in the screen have changed:                    
- add_new_actors_to_screen:
                        Checks all visuals for actors that are not yet added to the screen. Adds them
                        Checks for Visual and Mesh nodes that need to be reloaded by checking _new_mesh
                            if so then only reloads the main component; the other components are handled by (position_visuals)                                                    
  
Painting

-  update_painting : paints all actors of a visual according to the node-type
                     and paint-definition in VieportSettings (called internally when needed)
-  update_visibility : updates the paint for all non-selected nodes
                       updates the outlines
-  update_outlines : Updates the outlines of all actors
                     Hides outlines for invisible actors, except if they are xray

Painting definition

Paint is stored in a nested dictionary.

painters['node-class']['actor_key']

- Some actors may change paint based on their state. This state gets post-fixed to the node-class
    - Tanks will change color based on their fill
        empty
        partial
        full
        freeflooding
    - Contact-balls will change color based on contact or not 
        free
        contact
  
  for these nodes the entry becomes:
    painters['node-class:paint_state']['actor_key']
  
Temporary actors
-----------------
Actors (anything derived from vtkActor) can be added to the viewport by calling
add_temporary_actor. Temporary actors are automatically removed when the viewport
is updated or can be removed manaully be calling remove_temporary_actors

"""



class DelayRenderingTillDone():
    """Little helper class to pause rendering and refresh using with(...)

    with(DelayRenderingTillDone(Viewport):
        do_updates


    Creates an attribute _DelayRenderingTillDone_lock on the parent viewport to
    keep this action exclusive to the first caller.

    """
    def __init__(self, viewport):
        self.viewport = viewport
        self.inactive = False

    def __enter__(self):
        try:
            if self.viewport._DelayRenderingTillDone_lock:
                self.inactive = True
                return
        except:
            pass

        self.viewport._DelayRenderingTillDone_lock = True # keep others from gaining control
        self.viewport.screen.interactor.EnableRenderOff()
        for r in self.viewport.screen.renderers:
            r.DrawOff()


    def __exit__(self, *args, **kwargs):
        if self.inactive:
            return
        self.viewport.screen.interactor.EnableRenderOn()
        self.viewport.refresh_embeded_view()
        for r in self.viewport.screen.renderers:
            r.DrawOn()
        self.viewport._DelayRenderingTillDone_lock = False # release lock



def transform_to_mat4x4(transform):
    mat4x4 = vtk.vtkMatrix4x4()
    for i in range(4):
        for j in range(4):
            mat4x4.SetElement(i, j, transform[j * 4 + i])
    return mat4x4


def transform_from_point(x, y, z):
    mat4x4 = vtk.vtkMatrix4x4()
    mat4x4.SetElement(0, 3, x)
    mat4x4.SetElement(1, 3, y)
    mat4x4.SetElement(2, 3, z)
    return mat4x4

def transform_from_node(node):
    """Returns the vtkTransform that can be used to align the actor
    to the node.

    Actor.SetUserTransform(....)
    """
    t = vtk.vtkTransform()
    t.Identity()
    tr = node.global_transform

    mat4x4 = vtk.vtkMatrix4x4()
    for i in range(4):
        for j in range(4):
            mat4x4.SetElement(i, j, tr[j * 4 + i])

    t.PostMultiply()
    t.Concatenate(mat4x4)

    return t




def transform_from_direction(axis):
    """
    Creates a transform that rotates the X-axis to the given direction
    Args:
        axis: requested direction

    Returns:
        vtk.vtkTransform
    """
    theta = np.arcsin(axis[2])
    phi = np.arctan2(axis[1], axis[0])
    t = vtk.vtkTransform()
    t.PostMultiply()
    # t.RotateX(90)  # put it along Z
    t.RotateY(np.rad2deg(theta))
    t.RotateZ(np.rad2deg(phi))

    return t


def update_line_to_points(line_actor, points):
    """Updates the points of a line-actor"""

    source = line_actor.GetMapper().GetInput()

    pts = source.GetPoints()

    npt = len(points)

    # check for number of points
    if pts.GetNumberOfPoints() == npt:
        line_actor.points(points)
        return
    else:

        _points = vtk.vtkPoints()
        _points.SetNumberOfPoints(npt)
        for i, pt in enumerate(points):
            _points.SetPoint(i, pt)

        _lines = vtk.vtkCellArray()
        _lines.InsertNextCell(npt)
        for i in range(npt):
            _lines.InsertCellPoint(i)
        source.SetLines(_lines)
        source.SetPoints(_points)

        source.Modified()


def apply_parent_translation_on_transform(parent, t):

    if parent is None:
        return

    tr = parent.global_transform

    mat4x4 = vtk.vtkMatrix4x4()
    for i in range(4):
        for j in range(4):
            mat4x4.SetElement(i, j, tr[j * 4 + i])

    t.PostMultiply()
    t.Concatenate(mat4x4)


def actor_from_trimesh(trimesh):
    """Creates a vedo.Mesh from a pyo3d.TriMesh"""

    if trimesh.nFaces == 0:
        return vp.Cube(side=0.00001)

    vertices = [trimesh.GetVertex(i) for i in range(trimesh.nVertices)]
    # are the vertices unique?

    faces = [trimesh.GetFace(i) for i in range(trimesh.nFaces)]

    return actor_from_vertices_and_faces(vertices, faces)


def actor_from_vertices_and_faces(vertices, faces):
    """Creates a mesh based on the given vertices and faces. Cleans up
    the structure before creating by removing duplicate vertices"""
    unique_vertices = np.unique(vertices, axis=0)

    if len(unique_vertices) != len(vertices):  # reconstruct faces and vertices
        unique_vertices, indices = np.unique(vertices, axis=0, return_inverse=True)
        f = np.array(faces)
        better_faces = indices[f]
        actor = vp.Mesh([unique_vertices, better_faces])
    else:
        actor = vp.Mesh([vertices, faces])

    return actor


def vp_actor_from_obj(filename):
    # load the data
    filename = str(filename)
    source = vtk.vtkOBJReader()
    source.SetFileName(filename)

    # # clean the data
    # con = vtk.vtkCleanPolyData()
    # con.SetInputConnection(source.GetOutputPort())
    # con.Update()
    # #
    #
    # # data = normals.GetOutput()
    # # for i in range(data.GetNumberOfPoints()):
    # #     point = data.GetPoint(i)
    # #     print(point)
    #
    # normals = vtk.vtkPolyDataNormals()
    # normals.SetInputConnection(con.GetOutputPort())
    # normals.ConsistencyOn()
    # normals.AutoOrientNormalsOn()

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(source.GetOutputPort())
    mapper.Update()
    #
    # # We are not importing textures and materials.
    # # Set color to 'w' to enforce an uniform color
    vpa = vp.Mesh(mapper.GetInputAsDataSet(), c="w")  # need to set color here

    # vpa = vp.Mesh(filename, c="w")

    return vpa

def _create_moment_or_shear_line(what, frame : dn.Frame, scale_to = 2, at=None):
    """see create_momentline_actors, create_shearline_actors
    """

    if at is None:
        at = frame

    lsm = frame.give_load_shear_moment_diagram(at)

    x, Fz, My = lsm.give_shear_and_moment()

    report_axis = at

    start = report_axis.to_glob_position((x[0], 0, 0))
    end = report_axis.to_glob_position((x[-1], 0, 0))

    n = len(x)
    scale = scale_to

    if what=='Moment':
        value = My
        color = 'green'
    elif what=='Shear':
        value = Fz
        color = 'blue'
    else:
        raise ValueError(f'What should be Moment or Shear, not {what}')

    if np.max(np.abs(value))<1e-6:
        scale = 0
    else:
        scale = scale / np.max(np.abs(value))
    line = [report_axis.to_glob_position((x[i], 0, scale * value[i])) for i in range(n)]

    actor_axis = vp.Line((start, end)).c('black').lw(3)
    actor_graph = vp.Line(line).c(color).lw(3)

    return (actor_axis, actor_graph)

def create_momentline_actors(frame : dn.Frame, scale_to = 2, at=None):
    """Returns an actor that visualizes the moment-line for the given frame.

    Args:
        frame : Frame node to report the momentline for
        scale_to : absolute maximum of the line [m]
        at : Optional: [Frame] to report the momentline in
        """
    return _create_moment_or_shear_line('Moment', frame, scale_to, at)

def create_shearline_actors(frame : dn.Frame, scale_to = 2, at=None):
    """Returns an actor that visualizes the shear-line for the given frame.

    Args:
        frame : Frame node to report the shearline for
        scale_to : absolute maximum of the line [m]
        at : Optional: [Frame] to report the shearline in
        """
    return _create_moment_or_shear_line('Shear', frame, scale_to, at)

class ActorType(Enum):
    FORCE = 1
    VISUAL = 2
    GEOMETRY = 3
    GLOBAL = 4
    CABLE = 5
    NOT_GLOBAL = 6
    BALLASTTANK = 7
    MESH_OR_CONNECTOR = 8
    COG = 9


class VisualOutline:
    parent_vp_actor = None
    outline_actor = None
    outline_transform = None


class VisualActor:
    """A VisualActor is the visual representation of a node or the global environment

    node is a reference to the node it represents. If node is None then this is the global environment ("scenery")

    a VisualActor can contain a number of vtk actors or vedo-actors. These are stored in a dictionary

    An visualActor may have a label_actor. This is a 2D annotation

    The appearance of a visual may change when it is selected. This is handled by select and deselect



    """

    def __init__(self, actors: dict, node):

        # check if 'main' is available
        if "main" not in actors:
            raise ValueError(
                f"one of the actors shall be called main, but got only keys: {actors.keys()}"
            )

        self.actors = actors  # dict of vedo actors. There shall be one called 'main'
        self.node = node  # Node
        self.label_actor = None

        self.paint_state = ""  # some nodes change paint depending on their state

        self._is_selected = False
        self._is_sub_selected = (
            False  # parent of this object is selected - render transparent
        )

    def select(self):
        self._is_selected = True

    def on(self):
        for a in self.actors.values():
            a.on()

    def off(self):
        for a in self.actors.values():
            a.off()

    @property
    def visible(self):
        return self.actors["main"].GetVisibility()

    def setLabelPosition(self, position):

        if len(position) != 3:
            raise ValueError('Position should have length 3')

        if self.label_actor is not None:
            self.label_actor.SetAttachmentPoint(*position)


    def labelCreate(self, txt):
        la = vtk.vtkCaptionActor2D()
        la.SetCaption(txt)

        position = self.actors["main"].GetPosition()

        la.SetAttachmentPoint(*position)

        la.SetPickable(True)

        cap = la.GetTextActor().GetTextProperty()
        la.GetTextActor().SetPickable(True)

        size = 0.02

        cap.SetColor(0, 0, 0)
        la.SetWidth(100 * size)
        la.SetHeight(size)
        la.SetPosition(-size / 2, -size / 2)
        la.SetBorder(False)
        cap.SetBold(True)
        cap.SetItalic(False)

        la.no_outline = True

        self.label_actor = la


    def labelUpdate(self, txt):
        if self.label_actor is None:
            self.labelCreate(txt)
        else:
            if self.label_actor.GetCaption() != txt:
                self.label_actor.SetCaption(txt)

        return self.label_actor

    def update_paint(self, ps):
        """Updates the painting for this visual

            Painting depends on the node type of this visual.
            The properties for the individual actors of this visual are
            stored in

            ps is the painter_settings dictionary

            """

        if ps is None:
            print("No painter settings, ugly world :(")
            return

        if self.node is None:
            node_class = "global"
        else:
            if isinstance(self.node, dn.ContactBall):
                node_class = f"ContactBall:{self.paint_state}"
            elif isinstance(self.node, dn.Tank):
                node_class = f"Tank:{self.paint_state}"
            elif isinstance(self.node, dn.Shackle):
                node_class = "RigidBody"
            else:
                node_class = self.node.class_name

        if node_class in ps:
            node_painter_settings = ps[node_class]
        else:
            print(f"No paint for {node_class}")
            return  # no settings available

        # Override paint settings if node is selected or sub-selected

        if self._is_selected:
            new_painter_settings = dict()
            for k,value in node_painter_settings.items():
                v = copy(value)
                v.surfaceColor = COLOR_SELECT_255
                v.lineColor = COLOR_SELECT_255
                new_painter_settings[k] = v

            new_painter_settings['main'].labelShow = True

            node_painter_settings = new_painter_settings

        if self._is_sub_selected:
            new_painter_settings = dict()

            for k, value in node_painter_settings.items():
                v = copy(value)
                v.alpha = min(v.alpha, 0.4)
                new_painter_settings[k] = v
            node_painter_settings = new_painter_settings

        # label
        self.label_actor.SetVisibility(node_painter_settings['main'].labelShow)

        for key, actor in self.actors.items():

            if key in node_painter_settings:
                actor_settings = node_painter_settings[key]
            else:
                print(f"No paint for actor {node_class} {key}")
                continue

            # set the "xray" property of the actor
            actor.xray = actor_settings.xray
            actor._outline_color = actor_settings.outlineColor

            # on or off
            if actor_settings.surfaceShow or actor_settings.lineWidth > 0:
                actor.on()
            else:
                actor.off()
                continue

            if actor_settings.surfaceShow:

                props = actor.GetProperty()
                props.SetInterpolationToPBR()
                props.SetRepresentationToSurface()
                props.SetColor(
                    (
                        actor_settings.surfaceColor[0] / 255,
                        actor_settings.surfaceColor[1] / 255,
                        actor_settings.surfaceColor[2] / 255,
                    )
                )
                props.SetOpacity(actor_settings.alpha)
                props.SetMetallic(actor_settings.metallic)
                props.SetRoughness(actor_settings.roughness)
            else:
                actor.GetProperty().SetRepresentationToWireframe()

            actor.lineWidth(actor_settings.lineWidth)

            if actor_settings.lineWidth > 0:
                actor.lineColor(
                    (
                        actor_settings.lineColor[0] / 255,
                        actor_settings.lineColor[1] / 255,
                        actor_settings.lineColor[2] / 255,
                    )
                )
            else:
                actor.GetProperty().SetLineWidth(0)



    def update_geometry(self, viewport):
        """Updates the geometry of the actors to the current state of the node.
        This includes moving as well as changing meshes and volumes"""

        # update label name if needed
        self.labelUpdate(self.node.name) # does not do anything if the label-name is unchanged

        # the following ifs all end with Return, so only a single one is executed

        if isinstance(self.node, vf.Visual):
            A = self.actors["main"]

            # get the local (user set) transform
            t = vtk.vtkTransform()
            t.Identity()
            t.Translate(self.node.offset)
            t.Scale(self.node.scale)

            # # scale offset
            # scaled_offset = [V.node.offset[i] / V.node.scale[i] for i in range(3)]

            # calculate wxys from node.rotation
            r = self.node.rotation
            angle = (r[0] ** 2 + r[1] ** 2 + r[2] ** 2) ** (0.5)
            if angle > 0:
                t.RotateWXYZ(angle, r[0] / angle, r[1] / angle, r[2] / angle)

            # elm_matrix = t.GetMatrix()

            # Get the parent matrix (if any)
            if self.node.parent is not None:
                apply_parent_translation_on_transform(self.node.parent, t)

            A.SetUserTransform(t)
            return

        if isinstance(self.node, vf.Circle):
            A = self.actors["main"]

            # get the local (user set) transform
            t = vtk.vtkTransform()
            t.Identity()

            # scale to flat disk
            t.Scale(self.node.radius, self.node.radius, 0.1)

            # rotate z-axis (length axis is cylinder) is direction of axis
            axis = self.node.axis / np.linalg.norm(self.node.axis)
            z = (0, 0, 1)
            rot_axis = np.cross(z, axis)
            rot_dot = np.dot(z, axis)
            if rot_dot > 1:
                rot_dot = 1
            if rot_dot < -1:
                rot_dot = -1

            angle = np.arccos(rot_dot)

            t.PostMultiply()
            t.RotateWXYZ(np.rad2deg(angle), rot_axis)

            t.Translate(self.node.parent.position)

            # Get the parent matrix (if any)
            if self.node.parent.parent is not None:
                apply_parent_translation_on_transform(self.node.parent.parent, t)

            A.SetUserTransform(t)
            return

        if isinstance(self.node, vf.Cable):

            # # check the number of points
            A = self.actors["main"]

            points = self.node.get_points_for_visual()

            if len(points) == 0:  # not yet created
                return

            update_line_to_points(A, points)

            self.setLabelPosition(np.mean(points, axis=0))

            return

        if isinstance(self.node, vf.SPMT):

            A = self.actors["main"]

            pts = self.node.get_actual_global_points()
            if len(pts) == 0:
                return

            update_line_to_points(A, pts)

            return

        if isinstance(self.node, vf.Beam):
            points = self.node.global_positions
            A = self.actors["main"]
            update_line_to_points(A, points)

            self.setLabelPosition(np.mean(points, axis=0))

            return

        if isinstance(self.node, vf.Connector2d):
            A = self.actors["main"]

            points = list()
            points.append(self.node.nodeA.to_glob_position((0, 0, 0)))
            points.append(self.node.nodeB.to_glob_position((0, 0, 0)))

            A.points(points)

            return

        if isinstance(self.node, vf.LC6d):
            A = self.actors["main"]

            points = list()
            points.append(self.node.main.to_glob_position((0, 0, 0)))
            points.append(self.node.secondary.to_glob_position((0, 0, 0)))

            A.points(points)

            return

        if isinstance(self.node, vf.BallastSystem):
            return

        # footprints
        if isinstance(self.node, vf.NodeWithParentAndFootprint):

            fp = self.node.footprint
            if fp:
                n_points = len(fp)
                current_n_points = self.actors["footprint"]._mapper.GetInput().GetNumberOfPoints()

                if isinstance(self.node, vf.Point):
                    p = self.node.position
                    local_position = [(v[0]+p[0], v[1]+p[1], v[2]+p[2]) for v in fp]
                    if self.node.parent:
                        fp = [self.node.parent.to_glob_position(loc) for loc in local_position]
                    else:
                        fp = local_position


                if n_points == current_n_points:
                    self.actors["footprint"].points(fp)
                else:
                    # create a new actor
                    new_actor = actor_from_vertices_and_faces(vertices=fp, faces=[range(n_points)])

                    print('number of points changed, creating new')

                    if viewport.screen is not None:
                        viewport.screen.remove(self.actors["footprint"])
                        self.actors["footprint"] = new_actor
                        viewport.screen.add(self.actors["footprint"], render=True)

        if isinstance(self.node, vf.Point):
            t = vtk.vtkTransform()
            t.Identity()
            t.Translate(self.node.global_position)
            self.actors["main"].SetUserTransform(t)
            self.actors["main"].SetScale(viewport.settings.geometry_scale)

            self.setLabelPosition(self.node.global_position)
            return

        if isinstance(self.node, vf.ContactBall):

            self.node.update()

            t = vtk.vtkTransform()
            t.Identity()
            t.Translate(self.node.parent.global_position)

            # check radius
            if self.actors["main"]._r != self.node.radius:
                temp = vp.Sphere(
                    pos=(0, 0, 0), r=self.node.radius, res=RESOLUTION_SPHERE
                )
                self.actors["main"].points(temp.points())
                self.actors["main"]._r = self.node.radius

            self.actors["main"].SetUserTransform(t)
            # V.actors["main"].wireframe(V.node.contact_force_magnitude > 0)

            if self.node.can_contact:
                point1 = self.node.parent.global_position
                point2 = self.node.contactpoint
                self.actors["contact"].points([point1, point2])
                self.actors["contact"].on()
            else:
                self.actors["contact"].off()

            # update paint settings
            if self.node.contact_force_magnitude > 0:  # do we have contact?
                self.paint_state = "contact"
            else:
                self.paint_state = "free"

            self.update_paint(viewport.settings.painter_settings)

            return

        if isinstance(self.node, vf.WaveInteraction1):
            t = vtk.vtkTransform()
            t.Identity()
            t.Translate(self.node.parent.to_glob_position(self.node.offset))
            self.actors["main"].SetUserTransform(t)
            self.actors["main"].SetScale(viewport.settings.geometry_scale)
            return

        if isinstance(self.node, vf.Force):

            # check is the arrows are still what they should be
            if not np.all(
                    self.actors["main"]._force == viewport._scaled_force_vector(self.node.force)
            ):
                viewport.screen.remove(self.actors["main"])

                endpoint = viewport._scaled_force_vector(self.node.force)

                p = vp.Arrow(
                    startPoint=(0, 0, 0), endPoint=endpoint, res=RESOLUTION_ARROW
                )
                p.PickableOn()
                p.actor_type = ActorType.FORCE
                p._force = endpoint

                self.actors["main"] = p
                viewport.screen.add(self.actors["main"])

            # check is the arrows are still what they should be
            if not np.all(
                    np.array(self.actors["moment1"]._moment)
                    == viewport._scaled_force_vector(self.node.moment)
            ):
                viewport.screen.remove(self.actors["moment1"])
                viewport.screen.remove(self.actors["moment2"])

                endpoint = viewport._scaled_force_vector(self.node.moment)
                p = vp.Arrow(
                    startPoint=(0, 0, 0), endPoint=endpoint, res=RESOLUTION_ARROW
                )
                p.PickableOn()
                p.actor_type = ActorType.FORCE
                p._moment = endpoint
                self.actors["moment1"] = p

                p = vp.Arrow(
                    startPoint=0.2 * endpoint,
                    endPoint=1.2 * endpoint,
                    res=RESOLUTION_ARROW,
                )
                p.PickableOn()
                p.actor_type = ActorType.FORCE
                self.actors["moment2"] = p
                viewport.screen.add(self.actors["moment1"])
                viewport.screen.add(self.actors["moment2"])

            t = self.actors["main"].getTransform()
            t.Identity()
            t.Translate(self.node.parent.global_position)
            for a in self.actors.values():
                a.SetUserTransform(t)

            return

        if isinstance(self.node, vf.RigidBody):

            # Some custom code to place and scale the Actor[3] of the body.
            # This actor should be placed at the CoG position and scaled to a solid steel block

            t = vtk.vtkTransform()
            t.Identity()

            if viewport.settings.cog_do_normalize:
                scale = 1
            else:
                scale = (self.node.mass / 8.050) ** (1 / 3)  # density of steel

            t.Translate(self.node.cog)
            mat4x4 = transform_to_mat4x4(self.node.global_transform)

            for A in self.actors.values():
                A.SetUserMatrix(mat4x4)

            t.PostMultiply()
            t.Concatenate(mat4x4)

            scale = scale * viewport.settings.cog_scale

            self.actors["main"].SetScale(scale)
            self.actors["main"].SetUserTransform(t)

            # scale the arrows
            self.actors["x"].SetScale(viewport.settings.geometry_scale)
            self.actors["y"].SetScale(viewport.settings.geometry_scale)
            self.actors["z"].SetScale(viewport.settings.geometry_scale)

            return

        if (
                isinstance(self.node, vf.Buoyancy)
                or isinstance(self.node, vf.ContactMesh)
                or isinstance(self.node, vf.Tank)
        ):
            # Source mesh update is common for all mesh-like nodes
            #

            # print(f'Updating source mesh for {V.node.name}')

            changed = False  # anything changed?

            if self.node.trimesh._new_mesh:
                changed = True  # yes, mesh has changed
                self.node.trimesh._new_mesh = False  # one time only

            # move the full mesh with the parent

            if self.node.parent is not None:
                mat4x4 = transform_to_mat4x4(self.node.parent.global_transform)
                current_transform = self.actors["main"].getTransform().GetMatrix()

                # if the current transform is identical to the new one,
                # then we do not need to change anything (creating the mesh is slow)

                for i in range(4):
                    for j in range(4):
                        if current_transform.GetElement(i, j) != mat4x4.GetElement(
                                i, j
                        ):
                            changed = True  # yes, transform has changed
                            break

                # Update the source-mesh position
                #
                # the source-mesh itself is updated in "add_new_actors_to_screen"
                if changed:
                    self.actors["main"].SetUserMatrix(mat4x4)

            if not changed:
                if isinstance(self.node, vf.Tank):
                    # the tank fill may have changed,
                    # only skip if fill percentage has changed with less than 1e-3%
                    vfp = getattr(self, '_visualized_fill_percentage', -1)
                    if abs(self.node.fill_pct - vfp) < 1e-3:
                        return

                else:
                    return  # skip the other update functions

        if isinstance(self.node, vf.Buoyancy):

            ## Buoyancy has multiple actors
            #
            # actor 0 : the source mesh :: main
            # actor 1 : the CoB
            # actor 2 : the waterplane
            # actor 3 : the submerged part of the source mesh
            #

            # If we are here then either the source-mesh has been updated or the position has changed

            if viewport.quick_updates_only:
                for a in self.actors.values():
                    a.off()
                return

            # Update the CoB
            # move the CoB to the new (global!) position
            cob = self.node.cob
            self.actors["cob"].SetUserMatrix(transform_from_point(*cob))

            # update water-plane
            x1, x2, y1, y2, _, _ = self.node.trimesh.get_extends()
            x1 -= VISUAL_BUOYANCY_PLANE_EXTEND
            x2 += VISUAL_BUOYANCY_PLANE_EXTEND
            y1 -= VISUAL_BUOYANCY_PLANE_EXTEND
            y2 += VISUAL_BUOYANCY_PLANE_EXTEND
            p1 = self.node.parent.to_glob_position((x1, y1, 0))
            p2 = self.node.parent.to_glob_position((x2, y1, 0))
            p3 = self.node.parent.to_glob_position((x2, y2, 0))
            p4 = self.node.parent.to_glob_position((x1, y2, 0))

            corners = [
                (p1[0], p1[1], 0),
                (p2[0], p2[1], 0),
                (p3[0], p3[1], 0),
                (p4[0], p4[1], 0),
            ]
            self.actors["waterplane"].points(corners)

            # Instead of updating, remove the old actor and create a new one

            # remove already existing submerged mesh (if any)
            if "submerged_mesh" in self.actors:
                if viewport.screen is not None:
                    viewport.screen.remove(self.actors["submerged_mesh"])
                    del self.actors["submerged_mesh"]

            mesh = self.node._vfNode.current_mesh

            if mesh.nVertices > 0:  # only add when available

                vis = actor_from_trimesh(mesh)

                vis.actor_type = ActorType.MESH_OR_CONNECTOR
                self.actors["submerged_mesh"] = vis
                self.update_paint(viewport.settings.painter_settings)

                if viewport.screen is not None:
                    viewport.screen.add(vis)

            return

        if isinstance(self.node, vf.ContactMesh):
            return

        if isinstance(self.node, vf.Tank):

            ## Tank has multiple actors
            #
            # main : source-mesh
            # cog : cog
            # fluid : filled part of mesh

            # If the source mesh has been updated, then V.node.trimesh._new_mesh is True
            just_created = getattr(self, '__just_created', True)
            if just_created:
                self._visual_volume = -1

            if viewport.quick_updates_only:
                for a in self.actors.values():
                    a.off()
                return
            else:
                if self.node.visible:
                    for a in self.actors.values():
                        a.on()

            # Update the actors
            self.node.update()

            points = self.actors["main"].points(True)
            self.setLabelPosition(np.mean(points, axis=1).flatten())

            # Update the CoG
            # move the CoG to the new (global!) position
            self.actors["cog"].SetUserMatrix(transform_from_point(*self.node.cog))

            if self.node.volume <= 1:  # the "cog node" has a volume of
                self.actors["cog"].off()
            else:
                self.actors["cog"].on()

            # Fluid in tank

            # Construct a visual:
            #   - vertices
            #   - faces

            # If tank is full, then simply copy the mesh from the tank itself

            if self.node.fill_pct > 99.99 and not self.node.free_flooding:

                # tank is full
                vertices = points[0]
                faces = self.actors['main'].faces()

            else:

                mesh = self.node._vfNode.current_mesh

                if mesh.nVertices > 0:  # only add when available

                    vertices = []
                    for i in range(mesh.nVertices):
                        vertices.append(mesh.GetVertex(i))

                    faces = []
                    for i in range(mesh.nFaces):
                        faces.append(mesh.GetFace(i))

                    # create the lid using a convex hull
                    thickness_tolerance = 1e-4  # for numerical accuracy

                    verts = np.array(vertices)
                    z = verts[:, 2]
                    maxz = np.max(z)
                    top_plane_verts = verts[z >= maxz - thickness_tolerance]

                    # make convex hull
                    d2 = top_plane_verts[:, 0:2]

                    try:

                        hull = ConvexHull(d2)

                        points = top_plane_verts[
                                 hull.vertices, :
                                 ]  # for 2-D the vertices are guaranteed to be in counterclockwise order

                        nVerts = len(vertices)

                        for point in points:
                            vertices.append([*point])

                        # construct faces
                        for i in range(len(points) - 2):
                            faces.append([nVerts, nVerts + i + 2, nVerts + i + 1])
                    except:
                        pass

                else:
                    vertices = []
                # -------------------

            # paint settings
            if self.node.free_flooding:
                self.paint_state = "freeflooding"
            else:
                if self.node.fill_pct >= 95:
                    self.paint_state = "full"
                elif self.node.fill_pct <= 5:
                    self.paint_state = "empty"
                else:
                    self.paint_state = "partial"

            # we now have vertices and points and faces

            # do we already have an actor?
            need_new = False
            if "fluid" in self.actors:
                # print(f'Already have an actor for {V.node.name}')

                self._visualized_fill_percentage = self.node.fill_pct  # store for "need_update" check

                vis = self.actors["fluid"]
                pts = vis.GetMapper().GetInput().GetPoints()
                npt = len(vertices)

                # Update the existing actor if the number of vertices stay the same
                # If not then delete the actor

                # check for number of points
                if pts.GetNumberOfPoints() == npt:
                    # print(f'setting points for {V.node.name}')
                    vis.points(vertices)

                else:

                    if viewport.screen is not None:
                        viewport.screen.remove(self.actors["fluid"])
                        del self.actors["fluid"]
                        need_new = True
            else:
                need_new = True

            if len(vertices) > 0:  # if we have an actor

                if need_new:

                    # print(f'Creating new actor for for {V.node.name}')

                    vis = actor_from_vertices_and_faces(vertices, faces)

                    vis.actor_type = ActorType.MESH_OR_CONNECTOR

                    self.actors["fluid"] = vis

                    if viewport.screen is not None:
                        viewport.screen.add(vis, render=True)

                if not self.node.visible:
                    vis.off()

            self._visual_volume = self.node.volume

            # viewport.update_painting(self)
            self.update_paint(viewport.settings.painter_settings)

            return



        if isinstance(self.node, vf.Frame):
            m44 = transform_to_mat4x4(self.node.global_transform)
            for a in self.actors.values():
                a.SetScale(viewport.settings.geometry_scale)
                a.SetUserMatrix(m44)

            return

        # --- default ---

        try:
            tr = self.node.global_transform
        except AttributeError:
            try:
                tr = self.node.parent.global_transform
            except AttributeError:
                return

        mat4x4 = transform_to_mat4x4(tr)

        for A in self.actors.values():
            A.SetUserMatrix(mat4x4)


class Viewport:
    """
    Viewport provides a view of a Scene.

    Use:
    v = Viewport(scene)
    v.show()


    """

    def __init__(self, scene, jupyter=False):
        self.scene = scene

        """These are the visuals for the nodes"""
        self.node_visuals: List[VisualActor] = list()
        self.node_outlines: List[VisualOutline] = list()

        """These are the temporary visuals"""
        self.temporary_actors: List[vtk.vtkActor] = list()

        """These are all non-node-bound visuals , visuals for the global environment"""
        self.global_visuals = dict()

        self.screen = None
        """Becomes assigned when a screen is active (or was active...)"""

        self.vtkWidget = None
        """Qt viewport, if any"""

        self.mouseLeftEvent = None
        self.mouseRightEvent = None
        self.onEscapeKey = None
        "Function handles"

        self.Jupyter = jupyter

        self.settings = ViewportSettings()

        self.quick_updates_only = (
            False  # Do not perform slow updates ( make animations quicker)
        )

        self._wavefield = None
        """WaveField object"""

    @staticmethod
    def show_as_qt_app(s, painters = None, sea=False, boundary_edges = False):
        from PySide2.QtWidgets import QWidget, QApplication

        app = QApplication()
        widget = QWidget()
        widget.show()

        if painters is None:
            from DAVE.settings_visuals import PAINTERS
            painters = PAINTERS['Construction']

        v = Viewport(scene=s)

        v.settings.painter_settings = painters

        v.settings.show_global = sea

        v.show_embedded(widget)
        v.quick_updates_only = False

        v.create_node_visuals()
        # v.add_new_node_actors_to_screen()

        v.position_visuals()
        v.add_new_node_actors_to_screen() # position visuals may create new actors
        v.update_visibility()

        v.zoom_all()

        app.exec_()


    def add_temporary_actor(self, actor : vtk.vtkActor):
        self.temporary_actors.append(actor)
        if self.screen:
            self.screen.add(actor)

    def remove_temporary_actors(self):
        if self.temporary_actors:
            if self.screen:
                self.screen.remove(self.temporary_actors)
        self.temporary_actors.clear()


    def update_outlines(self):
        """Updates the outlines of all actors in the viewport

        Update comprises
        - setting the visibility
            An outline copies the visibility of its parent actor.
            Except if the parent actor has a property "xray" which is set to true
        - removing obsolete outlines
        - adding new outlines
        - updating the transforms

        """
        if self.screen is None:
            return

        camera = self.screen.camera

        # Hide and quit if only doing quick updates
        if self.quick_updates_only:
            for outline in self.node_outlines:
                outline.outline_actor.SetVisibility(False)
            return

        # Control outline visibility
        for outline in self.node_outlines:
            if getattr(outline.parent_vp_actor, "xray", False):
                outline.outline_actor.SetVisibility(True)
            else:
                if outline.parent_vp_actor.GetVisibility():
                    outline.outline_actor.SetVisibility(True)
                else:
                    outline.outline_actor.SetVisibility(False)



        # list of already existing outlines
        _outlines = [a.parent_vp_actor for a in self.node_outlines]

        # loop over actors, add outlines if needed
        for vp_actor in self.screen.actors:

            if isinstance(
                vp_actor.GetProperty(), vtkmodules.vtkRenderingCore.vtkProperty2D
            ):  # annotations
                continue

            if vp_actor.GetProperty().GetRepresentation() == 1:  # wireframe
                continue

            if getattr(vp_actor, "no_outline", False):
                continue

            data = vp_actor.GetMapper().GetInputAsDataSet()
            if isinstance(data, vtk.vtkPolyData):
                # this actor can have an outline
                if vp_actor not in _outlines:
                    # create outline and add to self.outlines

                    # clean the input data to ensure continuous faces
                    # # clean the data

                    con = vtk.vtkCleanPolyData()
                    con.SetInputData(data)
                    con.Update()

                    tr = vtk.vtkTransformPolyDataFilter()

                    tr.SetInputData(con.GetOutput())

                    temp = vtk.vtkTransform()
                    temp.Identity()
                    tr.SetTransform(temp)
                    tr.Update()

                    ol = vtk.vtkPolyDataSilhouette()
                    ol.SetInputConnection(tr.GetOutputPort())
                    ol.SetEnableFeatureAngle(True)
                    ol.SetCamera(camera)
                    ol.SetBorderEdges(True)

                    mapper = vtk.vtkPolyDataMapper()
                    mapper.SetInputConnection(ol.GetOutputPort())

                    actor = vtk.vtkActor()
                    actor.SetMapper(mapper)
                    actor.GetProperty().SetColor(0, 0, 0)
                    actor.GetProperty().SetLineWidth(self.settings.outline_width)

                    self.screen.renderer.AddActor(actor)  # vtk actor

                    # store
                    record = VisualOutline()
                    record.outline_actor = actor
                    record.outline_transform = tr
                    record.parent_vp_actor = vp_actor
                    self.node_outlines.append(record)

        # Update transforms for outlines
        to_be_deleted = []
        for record in self.node_outlines:
            # is the parent actor still present?
            if record.parent_vp_actor in self.screen.actors:
                # update transform
                userTransform = record.parent_vp_actor.GetUserTransform()

                if userTransform is not None:
                    matrix = userTransform.GetMatrix()
                else:
                    matrix = vtk.vtkMatrix4x4()

                trans = vtk.vtkTransform()
                trans.Identity()
                trans.Concatenate(matrix)
                trans.Scale(record.parent_vp_actor.GetScale())

                record.outline_transform.SetTransform(trans)

                record.outline_actor.SetVisibility(
                    getattr(record.parent_vp_actor, "xray", False)
                    or record.parent_vp_actor.GetVisibility()
                )

                # get color
                color = getattr(record.parent_vp_actor, "_outline_color", (0,0,0))
                record.outline_actor.GetProperty().SetColor(color[0]/255, color[1]/255, color[2]/255)

            else:
                # mark for deletion
                to_be_deleted.append(record)

        # Remove obsolete outlines
        to_be_deleted_actors = [oa.outline_actor for oa in to_be_deleted]
        self.screen.remove(to_be_deleted_actors)

        for record in to_be_deleted:
            self.node_outlines.remove(record)

    def create_world_actors(self):
        """Creates the sea and global axes"""

        if 'sea' in self.global_visuals:
            raise ValueError('Global visuals already created - can not create again')

        plane = vp.Plane(pos=(0, 0, 0), normal=(0, 0, 1), sx=1000, sy=1000).c(
            COLOR_WATER
        )
        plane.texture(TEXTURE_SEA)
        plane.lighting(ambient=1.0, diffuse=0.0, specular=0.0)
        plane.alpha(0.4)

        self.global_visuals["sea"] = plane
        self.global_visuals["sea"].actor_type = ActorType.GLOBAL
        self.global_visuals["sea"].no_outline = True

        self.global_visuals["main"] = vp.Line((0, 0, 0), (10, 0, 0)).c("red")
        self.global_visuals["main"].actor_type = ActorType.GEOMETRY

        self.global_visuals["y"] = vp.Line((0, 0, 0), (0, 10, 0)).c("green")
        self.global_visuals["y"].actor_type = ActorType.GEOMETRY

        self.global_visuals["z"] = vp.Line((0, 0, 0), (0, 0, 10)).c("blue")
        self.global_visuals["z"].actor_type = ActorType.GEOMETRY

        for actor in self.global_visuals.values():
            self.screen.add(actor)


    def deselect_all(self):

        for v in self.node_visuals:
            v._is_selected = False
            self.update_painting()

    def node_from_vtk_actor(self, actor):
        """
        Given a vkt actor, find the corresponding node
        Args:
            actor: vtkActor

        Returns:

        """
        for v in self.node_visuals:
            for a in v.actors.values():
                if a == actor:
                    return v.node
            if v.label_actor == actor:
                return v.node

        return None

    def actor_from_node(self, node):
        """Finds the VisualActor belonging to node"""
        for v in self.node_visuals:
            if v.node is node:
                return v
        return None

    def add_dynamic_wave_plane(self, waveplane):
        self.remove_dynamic_wave_plane()
        self.screen.renderer.AddActor(waveplane.actor)
        self._wavefield = waveplane

        self.settings.show_global = False
        #
        # if self.settings.show_global = False:
        #     self._staticwaveplane = True
        #     self.global_visual.off()
        # else:
        #     self._staticwaveplane = False

    def remove_dynamic_wave_plane(self):
        if self._wavefield is not None:
            self.screen.renderer.RemoveActor(self._wavefield.actor)
            self._wavefield = None

            # if self._staticwaveplane:
            #     self.global_visual.on()

    def update_dynamic_waveplane(self, t):
        if self._wavefield is not None:
            self._wavefield.update(t)

    def hide_actors_of_type(self, types):
        for V in self.node_visuals:
            for A in V.actors.values():
                if A.actor_type in types:
                    A.off()

    def show_actors_of_type(self, types):
        for V in self.node_visuals:
            for A in V.actors.values():
                if A.actor_type in types:
                    A.on()

    def set_alpha(self, alpha, exclude_nodes=None):
        """Sets the alpha (transparency) of for ALL actors in all visuals except the GLOBAL actors or visuals belonging to a node in exclude_nodes"""

        if exclude_nodes is None:
            exclude_nodes = []
        for V in self.node_visuals:
            for A in V.actors.values():

                if V.node in exclude_nodes:
                    continue

                if A.actor_type == ActorType.GLOBAL:
                    continue
                A.alpha(alpha)

    def level_camera(self):
        self.vtkWidget.GetRenderWindow().GetRenderers().GetFirstRenderer().GetActiveCamera().SetViewUp(
            [0, 0, 1]
        )
        self.refresh_embeded_view()

    def camera_reset(self):
        self.vtkWidget.GetRenderWindow().GetRenderers().GetFirstRenderer().ResetCamera()

    def toggle_2D(self):
        """Toggles between 2d and 3d mode. Returns True if mode is 2d after toggling"""
        camera = self.renderer.GetActiveCamera()
        if camera.GetParallelProjection():
            camera.ParallelProjectionOff()
            return False
        else:
            camera.ParallelProjectionOn()
            return True

    def set_camera_direction(self, vector):
        # Points the camera in the given direction
        camera = (
            self.vtkWidget.GetRenderWindow()
            .GetRenderers()
            .GetFirstRenderer()
            .GetActiveCamera()
        )
        vector = np.array(vector)
        vector = vector / np.linalg.norm(vector)

        if np.linalg.norm(np.cross(vector, (0, 0, 1))) < 1e-8:
            up = (0, -1, 0)
        else:
            up = (0, 0, 1)

        camera.SetViewUp(up)
        tar = np.array(camera.GetFocalPoint())
        pos = np.array(camera.GetPosition())
        dist = np.linalg.norm(tar - pos)

        camera_position = tar - dist * vector

        camera.SetPosition(camera_position)

    def _scaled_force_vector(self, vector):

        r = np.array(vector)
        len = np.linalg.norm(r)
        if len == 0:
            return r
        if self.settings.force_do_normalize:
            r *= 1000 / len
        r *= self.settings.force_scale / 1000
        return r

    def create_node_visuals(self, recreate=False):
        """Creates actors for nodes in the scene that do not yet have one

        Visuals are created in their parent axis system


        Attributes:
            recreate : re-create already exisiting visuals
        """

        for N in self.scene._nodes:

            if not recreate:
                try:  # if we already have a visual, then no need to create another one
                    N.visual
                    if N.visual is not None:
                        continue
                except:
                    pass

            actors = dict()

            if isinstance(N, vf.Buoyancy):

                # source-mesh : main
                # cob
                # water-plane
                # sumberged mesh

                # This is the source-mesh. Connect it to the parent
                vis = actor_from_trimesh(
                    N.trimesh._TriMesh
                )  # returns a small cube if no trimesh is defined

                vis.actor_type = ActorType.MESH_OR_CONNECTOR

                actors["main"] = vis

                # cob
                c = vp.Sphere(r=0.5, res=RESOLUTION_SPHERE)
                c.actor_type = ActorType.MESH_OR_CONNECTOR
                actors["cob"] = c

                # waterplane
                #
                (
                    minimum_x,
                    maximum_x,
                    minimum_y,
                    maximum_y,
                    minimum_z,
                    maximum_z,
                ) = N.trimesh.get_extends()

                vertices = [
                    (minimum_x, minimum_y, 0),
                    (maximum_x, minimum_y, 0),
                    (maximum_x, maximum_y, 0),
                    (minimum_x, maximum_y, 0),
                ]
                faces = [(0, 1, 2, 3)]

                p = vp.Mesh([vertices, faces])  # waterplane, ok to create like this

                p.actor_type = ActorType.NOT_GLOBAL
                actors["waterplane"] = p

            if isinstance(N, vf.Tank):

                # source-mesh
                # cog
                # filled part of mesh (added later)

                # This is the source-mesh. Connect it to the parent
                vis = actor_from_trimesh(N.trimesh._TriMesh)

                vis.actor_type = ActorType.MESH_OR_CONNECTOR

                actors["main"] = vis

                # cog
                c = vp.Sphere(r=0.1, res=RESOLUTION_SPHERE)
                c.actor_type = ActorType.MESH_OR_CONNECTOR
                actors["cog"] = c


            if isinstance(N, vf.ContactMesh):

                # 0 : source-mesh

                # This is the source-mesh. Connect it to the parent

                vis = actor_from_trimesh(N.trimesh._TriMesh)
                if not vis:
                    vis = vp.Cube(side=0.00001)

                vis.actor_type = ActorType.MESH_OR_CONNECTOR

                vis.loaded_obj = True

                actors["main"] = vis

            if isinstance(N, vf.Visual):
                file = self.scene.get_resource_path(N.path)
                # visual = vp.vtkio.load(file)
                visual = vp_actor_from_obj(file)
                visual.loaded_obj = file
                visual.actor_type = ActorType.VISUAL
                actors["main"] = visual

            if isinstance(N, vf.Frame):
                size = 1
                ar = vp.Arrow((0, 0, 0), (size, 0, 0), res=RESOLUTION_ARROW)
                ag = vp.Arrow((0, 0, 0), (0, size, 0), res=RESOLUTION_ARROW)
                ab = vp.Arrow((0, 0, 0), (0, 0, size), res=RESOLUTION_ARROW)

                ar.actor_type = ActorType.GEOMETRY
                ag.actor_type = ActorType.GEOMETRY
                ab.actor_type = ActorType.GEOMETRY

                ar.PickableOn()
                ag.PickableOn()
                ab.PickableOn()

                actors["main"] = ar
                actors["y"] = ag
                actors["z"] = ab

                # footprint
                actors["footprint"] = vp.Cube(side=0.00001) # dummy


            if isinstance(N, vf.RigidBody):
                size = 1

                # a rigidbody is also an axis

                box = vp_actor_from_obj(self.scene.get_resource_path("res: cog.obj"))

                box.actor_type = ActorType.COG
                actors["x"] = actors["main"]
                actors["main"] = box

            if isinstance(N, vf.Point):
                size = 0.5
                p = vp.Sphere(pos=(0, 0, 0), r=size / 2, res=RESOLUTION_SPHERE)
                p.actor_type = ActorType.GEOMETRY
                actors["main"] = p

                # footprint
                actors["footprint"] = vp.Cube(side=0.00001) # dummy

            if isinstance(N, vf.ContactBall):
                p = vp.Sphere(pos=(0, 0, 0), r=N.radius, res=RESOLUTION_SPHERE)
                p.actor_type = ActorType.MESH_OR_CONNECTOR
                p._r = N.radius
                actors["main"] = p

                point1 = (0, 0, 0)
                a = vp.Line([point1, point1], lw=5)
                a.actor_type = ActorType.MESH_OR_CONNECTOR

                actors["contact"] = a

            if isinstance(N, vf.WaveInteraction1):
                size = 2
                p = vp.Sphere(pos=(0, 0, 0), r=size / 2, res=RESOLUTION_SPHERE)
                p.actor_type = ActorType.FORCE
                actors["main"] = p

            if isinstance(N, vf.Force):

                endpoint = self._scaled_force_vector(N.force)
                p = vp.Arrow(
                    startPoint=(0, 0, 0), endPoint=endpoint, res=RESOLUTION_ARROW
                )
                p.PickableOn()
                p.actor_type = ActorType.FORCE
                p._force = endpoint

                actors["main"] = p

                endpoint = self._scaled_force_vector(N.moment)
                p = vp.Arrow(
                    startPoint=(0, 0, 0), endPoint=endpoint, res=RESOLUTION_ARROW
                )
                p.PickableOn()
                p.actor_type = ActorType.FORCE
                p._moment = endpoint
                actors["moment1"] = p

                p = vp.Arrow(
                    startPoint=0.2 * endpoint,
                    endPoint=1.2 * endpoint,
                    res=RESOLUTION_ARROW,
                )
                p.PickableOn()
                p.actor_type = ActorType.FORCE
                actors["moment2"] = p

            if isinstance(N, vf.Circle):
                axis = np.array(N.axis)
                axis /= np.linalg.norm(axis)
                p = vp.Cylinder(r=1)
                p.actor_type = ActorType.GEOMETRY

                actors["main"] = p

            if isinstance(N, vf.Cable):

                if N._vfNode.global_points:
                    a = vp.Line(N._vfNode.global_points)
                else:
                    a = vp.Line([(0, 0, 0), (0, 0, 0.1), (0, 0, 0)])

                a.PickableOn()

                a.actor_type = ActorType.CABLE
                actors["main"] = a

            if isinstance(N, vf.SPMT):

                gp = N.get_actual_global_points()
                if gp:
                    a = vp.Line(gp, lw=3)
                else:
                    a = vp.Line([(0, 0, 0), (0, 0, 0.1), (0, 0, 0)], lw=3)

                a.actor_type = ActorType.CABLE
                actors["main"] = a

            if isinstance(N, vf.Beam):

                gp = N.global_positions

                if len(gp) > 0:
                    a = vp.Line(gp)
                else:
                    a = vp.Line([(0, 0, 0), (0, 0, 0.1), (0, 0, 0)])

                a.actor_type = ActorType.CABLE
                actors["main"] = a

            if isinstance(N, vf.Connector2d):

                points = list()

                for i in range(2):
                    points.append((0, 0, 0))

                a = vp.Line(points)
                a.actor_type = ActorType.CABLE

                actors["main"] = a

            if isinstance(N, vf.LC6d):

                points = list()

                for i in range(2):
                    points.append((0, 0, 0))

                a = vp.Line(points)
                a.actor_type = ActorType.CABLE

                actors["main"] = a



            if not actors:  # no actors created
                print(f"No actors created for node {N.name}")
                continue

            va = VisualActor(actors, N)
            va.labelUpdate(N.name)
            N.visual = va
            N.visual.__just_created = True

            self.node_visuals.append(va)


    def position_visuals(self):
        """When the nodes in the scene have moved:
        Updates the positions of existing visuals
        Removes visuals for which the node is no longer present in the scene
        Applies scaling for non-physical actors
        Updates the geometry for visuals where needed (meshes)
        Updates the "paint_state" property for tanks and contact nodes (see paint)"""

        to_be_removed = []

        for V in self.node_visuals:

            # check if the node still exists
            # if not, then remove the visual

            node = V.node
            if node not in self.scene._nodes:
                if V.actors:  # not all nodes have an actor
                    if (
                        V.actors["main"].actor_type != ActorType.GLOBAL
                    ):  # global visuals do not have a corresponding node
                        to_be_removed.append(V)
                        continue
                else:
                    to_be_removed.append(V)
                    continue  # node does not have an actor

            # create a transform from the Node
            # or the parent of the Node
            # or skip (for example a poi without a parent)

            if V.node is None:
                continue

            V.update_geometry(viewport=self)

        acs = list()
        for V in to_be_removed:
            self.node_visuals.remove(V)
            acs.extend(list(V.actors.values()))
            if V.label_actor is not None:
                acs.append(V.label_actor)

        acs.extend(self.temporary_actors)

        if acs:
            self.screen.remove(acs)

        self.update_outlines()

    def add_new_node_actors_to_screen(self):
        """Updates the screen with added actors"""

        to_be_added = []

        if self.screen:

            actors = self.screen.getMeshes()
            for va in self.node_visuals:
                for a in va.actors.values():
                    if not (a in actors):
                        to_be_added.append(a)

                if va.label_actor is not None:
                    if va.label_actor not in actors:
                        to_be_added.append(va.label_actor)

            if to_be_added:
                self.screen.add(to_be_added)

            # check if objs or meshes need to be re-loaded
            for va in self.node_visuals:
                if isinstance(va.node, vf.Visual):

                    try:
                        file = self.scene.get_resource_path(va.node.path)
                    except FileExistsError:
                        continue

                    if file == va.actors["main"].loaded_obj:
                        continue

                    self.screen.clear(va.actors["main"])

                    # update the obj
                    va.actors["main"] = vp_actor_from_obj(file)
                    va.actors["main"].loaded_obj = file
                    va.actors["main"].actor_type = ActorType.VISUAL

                    if not va.node.visible:
                        va.actors["main"].off()

                    self.screen.add(va.actors["main"])

                if (
                    isinstance(va.node, vf.Buoyancy)
                    or isinstance(va.node, vf.ContactMesh)
                    or isinstance(va.node, vf.Tank)
                ):
                    if va.node.trimesh._new_mesh:

                        # va.node.update() # the whole scene is already updated when executing code

                        new_mesh = actor_from_trimesh(va.node.trimesh._TriMesh)
                        new_mesh.no_outline = True

                        if new_mesh is not None:
                            self.screen.clear(va.actors["main"])

                            va.actors["main"] = new_mesh
                            va.actors["main"].actor_type = ActorType.MESH_OR_CONNECTOR

                            if va.node.parent is not None:
                                tr = va.node.parent.global_transform
                                mat4x4 = transform_to_mat4x4(tr)
                                va.actors["main"].SetUserMatrix(mat4x4)

                            else:
                                print("Trimesh without a parent")

                            if not va.node.visible:
                                va.actors["main"].off()

                            self.screen.add(va.actors["main"])  # add after positioning

                            # va.node.trimesh._new_mesh = False  # is set to False by position_visuals

            # self.set_default_dsa()

    def shutdown_qt(self):
        """Stops the renderer such that the application can close without issues"""

        if self.vtkWidget:
            ren = self.vtkWidget.GetRenderWindow()
            iren = ren.GetInteractor()
            ren.Finalize()
            iren.TerminateApp()

    def setup_screen(self, offscreen = False, size = (800,500)):
        """Creates the plotter instance and stores it in self.screen

        If offscreen = True then an offscreen plotter is made
        """

        if offscreen:
            self.screen = vp.Plotter(axes=0, offscreen=True, size=size)

        else:

            if (
                self.Jupyter and self.vtkWidget is None
            ):  # it is possible to launch the Gui from jupyter, so check for both

                # create embedded notebook (k3d) view
                import vedo as vtkp

                vtkp.settings.embedWindow(backend="k3d")
                self.screen = vp.Plotter(axes=4, bg=COLOR_BG1, bg2=COLOR_BG2)

            else:

                if self.vtkWidget is None:

                    # create stand-alone interactive view
                    import vedo as vtkp

                    vtkp.settings.embedWindow(backend=None)

                    self.screen = vp.plotter.Plotter(
                        interactive=True,
                        offscreen=False,
                        axes=4,
                        bg=COLOR_BG1,
                        bg2=COLOR_BG2,
                    )

                else:

                    # create embedded Qt view
                    import vedo as vtkp

                    vtkp.settings.embedWindow(backend=None)

                    self.screen = vp.plotter.Plotter(
                        qtWidget=self.vtkWidget, axes=4, bg=COLOR_BG1, bg2=COLOR_BG2
                    )

        """ For reference: this is how to load an cubemap texture

            Problem is that the default VTK orientation is not with the Z-axis up. So some magic needs to be done
            to have the cubemap and environmental light texture in the right orientation

            # load env texture
            cubemap_path_root = r'C:\\datapath\\skybox2-'

            files = [cubemap_path_root + name + '.jpg' for name in ['posx', 'negx', 'posy', 'negy', 'posz', 'negz']]

            cubemap = vtk.vtkTexture()
            cubemap.SetCubeMap(True)

            for i,file in enumerate(files):
                readerFactory = vtk.vtkImageReader2Factory()
                # textureFile = readerFactory.CreateImageReader2(file)
                textureFile = readerFactory.CreateImageReader2(r'c:\data\white.png')
                textureFile.SetFileName(r'c:\data\white.png')
                textureFile.Update()

                cubemap.SetInputDataObject(i, textureFile.GetOutput())

            # make skybox actor
            skybox = vtk.vtkSkybox()
            skybox.SetTexture(cubemap)

            self.screen.add(skybox)"""

        # Make a white skybox texture for light emission
        # cubemap = vtk.vtkTexture()
        # cubemap.SetCubeMap(True)
        #
        readerFactory = vtk.vtkImageReader2Factory()

        from pathlib import Path

        if not Path.exists(LIGHT_TEXTURE_SKYBOX):
            raise ValueError(f"No image found here: {LIGHT_TEXTURE_SKYBOX}")

        textureFile = readerFactory.CreateImageReader2(str(LIGHT_TEXTURE_SKYBOX))
        textureFile.SetFileName(str(LIGHT_TEXTURE_SKYBOX))
        textureFile.Update()
        texture = vtk.vtkTexture()
        texture.SetInputDataObject(textureFile.GetOutput())
        #
        # for i in range(6):
        #     cubemap.SetInputDataObject(i, textureFile.GetOutput())
        #

        # self.screen.show(camera=camera)

        # texture = vtk.vtkTexture()
        # input = vtk.vtkPNGReader()
        # input.SetFileName(str(LIGHT_TEXTURE_SKYBOX))
        # input.Modified()
        # texture.SetInputDataObject(input.GetOutput())

        # # Add SSAO
        # # see: https://blog.kitware.com/ssao/
        basicPasses = vtk.vtkRenderStepsPass()
        self.ssao = vtk.vtkSSAOPass()

        # Radius 10, Kernel 500 gives nice result - but slow
        # Kernel size 50 less accurate bus faster
        self.ssao.SetRadius(10)
        self.ssao.SetDelegatePass(basicPasses)
        self.ssao.SetKernelSize(50)
        self.ssao.SetBlur(True)

        for r in self.screen.renderers:
            r.ResetCamera()

            r.UseImageBasedLightingOn()
            r.SetEnvironmentTexture(texture)

            r.SetUseDepthPeeling(True)

            r.Modified()

    def show(self, include_outlines=True, zoom_fit = False):
        """Add actors to screen and show

        If purpose is to show embedded, then call show_embedded instead
        """
        if self.screen is None:
            raise Exception("Please call setup_screen first")

        # vp.settings.lightFollowsCamera = True

        self.create_world_actors()

        # if camera is None:
        #     camera = dict()
        #     camera["viewup"] = [0, 0, 1]
        #     camera["pos"] = [10, -10, 5]
        #     camera["focalPoint"] = [0, 0, 0]


        if self.Jupyter and self.vtkWidget is None:

            # show embedded
            for va in self.node_visuals:
                for a in va.actors.values():
                    # if a.GetVisibility():  # also invisible nodes need to be added because they may be x-rayed
                    self.screen.add(a)

            self.update_visibility()  # needs to be called after actors have been added to screen
            self.update_global_visibility()

            self.screen.resetcam = False


            for outline in self.node_outlines:
                self.screen.add(outline.outline_actor)

            return self.screen.show(resetcam=zoom_fit)

        else:

            screen = self.screen

            for va in self.node_visuals:
                for a in va.actors.values():
                    screen.add(a)

            if include_outlines:
                for outline in self.node_outlines:
                    screen.add(outline.outline_actor)

            screen.resetcam = False

            camera = dict()
            camera["viewup"] = [0, 0, 1]
            camera["pos"] = [10, -10, 5]
            camera["focalPoint"] = [0, 0, 0]

            screen.show(camera=camera)

            return screen

    def EnableSSAO(self):

        # from documentation:
        # virtual void 	UseSSAOOn ()
        # virtual void 	UseSSAOOff ()
        #
        # but does not work

        for r in self.screen.renderers:
            r.SetPass(self.ssao)
            r.Modified()

    def DisableSSAO(self):
        for r in self.screen.renderers:
            r.SetPass(None)
            r.Modified()

    def onMouseLeft(self, info):

        if self.mouseLeftEvent is not None:
            self.mouseLeftEvent(info)

    def zoom_all(self):
        """Set camera to view the whole scene (ignoring the sea)"""

        store = self.settings.show_global
        self.settings.show_global = False
        self.update_global_visibility()

        for r in self.screen.renderers:
            r.ResetCamera()

        self.settings.show_global = store
        self.update_global_visibility()

    def onMouseRight(self, info):
        if self.mouseRightEvent is not None:
            self.mouseRightEvent(info)

    def show_embedded(self, target_frame):
        """target frame : QFrame """

        from PySide2.QtWidgets import QVBoxLayout
        from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

        # add a widget to gui
        vl = QVBoxLayout()
        vl.setContentsMargins(0, 0, 0, 0)
        self.target_frame = target_frame
        self.vtkWidget = QVTKRenderWindowInteractor(target_frame)

        vl.addWidget(self.vtkWidget)
        target_frame.setLayout(vl)

        self.setup_screen()
        screen = self.show()

        self.renwin = self.vtkWidget.GetRenderWindow()
        self.renderer = screen.renderers[0]

        self.renwin.AddRenderer(self.renderer)

        iren = self.renwin.GetInteractor()
        iren.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())

        iren.AddObserver("LeftButtonPressEvent", self._leftmousepress)
        iren.AddObserver("RightButtonPressEvent", screen._mouseright)
        iren.AddObserver("MiddleButtonPressEvent", screen._mousemiddle)
        iren.AddObserver("KeyPressEvent", self.keyPressFunction)
        iren.AddObserver(vtk.vtkCommand.InteractionEvent, self.keep_up_up)

        for r in screen.renderers:
            r.ResetCamera()

        iren.Start()

        screen.mouseRightClickFunction = self.onMouseRight

    def _leftmousepress(self, iren, event):
        """Implements a "fuzzy" mouse pick function"""

        if self.mouseLeftEvent is not None:

            pos = self.screen.interactor.GetEventPosition()

            picker = vtk.vtkPropPicker()

            for j in range(5):

                if j == 0:
                    x, y = 0, 0
                elif j == 1:
                    x, y = -1, 1
                elif j == 2:
                    x, y = -1, -1
                elif j == 3:
                    x, y = 1, 1
                else:
                    x, y = 1, -1

                if picker.Pick(pos[0] + 2 * x, pos[1] + 2 * y, 0, self.screen.renderer):
                    actor = picker.GetActor()  # gives an Actor
                    if actor is not None:
                        self.mouseLeftEvent(actor)
                        return

                    actor = picker.GetActor2D()
                    if actor is not None:
                        self.mouseLeftEvent(actor)
                        return

    def keep_up_up(self, obj, event_type):
        """Force z-axis up"""

        camera = self.screen.camera

        up = camera.GetViewUp()
        if abs(up[2]) < 0.2:
            factor = 1 - (5 * abs(up[2]))
            camera.SetViewUp(
                factor * up[0], factor * up[1], (1 - factor) + factor * up[2]
            )
        else:
            camera.SetViewUp(0, 0, 1)

        z = camera.GetPosition()[2]
        alpha = 1
        if z < 0:

            dz = camera.GetDirectionOfProjection()[2]

            # alpha = (z + 10)/10
            alpha = 1 - (10 * dz)
            if alpha < 0:
                alpha = 0
        self.global_visuals["sea"].alpha(ALPHA_SEA * alpha)

    def keyPressFunction(self, obj, event):
        key = obj.GetKeySym()
        if key == "Escape":
            if self.onEscapeKey is not None:
                self.onEscapeKey()

    def refresh_embeded_view(self):
        self.vtkWidget.update()

    def update_visibility(self):
        """Updates the settings of the viewport to reflect the settings in self.settings.painter_settings"""

        for v in self.node_visuals:

            # on-off from node overrides everything
            if v.node is not None:
                for a in v.actors.values():
                    a.SetVisibility(v.node.visible)
                    a.xray = v.node.visible
                v.label_actor.SetVisibility(v.node.visible)

                if not v.node.visible:
                    continue # no need to update paint on invisible actor

            v.update_paint(self.settings.painter_settings)

            if v._is_selected:
                v.labelUpdate(v.node.name)

        self.update_global_visibility()
        self.update_outlines()

    def update_global_visibility(self):
        """Syncs the visibility of the global actors to Viewport-settings"""

        if self.settings.show_global:
            for actor in self.global_visuals.values():
                actor.on()
        else:
            for actor in self.global_visuals.values():
                actor.off()


class WaveField:
    def __init__(self):
        self.actor = None
        self.pts = None
        self.nt = 0
        self.elevation = None

        self.texture = vtk.vtkTexture()
        input = vtk.vtkJPEGReader()
        input.SetFileName(TEXTURE_SEA)
        self.texture.SetInputConnection(input.GetOutputPort())
        self.ttp = vtk.vtkTextureMapToPlane()

    def update(self, t):
        t = np.mod(t, self.period)
        i = int(self.nt * t / self.period)

        count = 0
        for ix, xx in enumerate(self.x):
            for iy, yy in enumerate(self.y):
                self.pts.SetPoint(count, xx, yy, self.elevation[iy, ix, i])
                count += 1
        self.pts.Modified()

    def create_waveplane(
        self,
        wave_direction,
        wave_amplitude,
        wave_length,
        wave_period,
        nt,
        nx,
        ny,
        dx,
        dy,
    ):

        x = np.linspace(-dx, dx, nx)
        y = np.linspace(-dy, dy, ny)
        xv, yv = np.meshgrid(x, y)

        u = np.array(
            (np.cos(np.deg2rad(wave_direction)), np.sin(np.deg2rad(wave_direction)))
        )

        dist_phasor = np.exp(1j * (xv * u[0] + yv * u[1]) * (2 * np.pi / wave_length))

        t = np.linspace(0, wave_period, nt)
        time_phasor = np.exp(-1j * (2 * np.pi * t / wave_period))

        elevation = np.zeros((*xv.shape, nt))

        for i in range(nt):
            elevation[:, :, i] = wave_amplitude * np.real(time_phasor[i] * dist_phasor)

        # the vtk stuff

        # make grid
        pts = vtk.vtkPoints()
        for ix, xx in enumerate(x):
            for iy, yy in enumerate(y):
                pts.InsertNextPoint(yy, xx, elevation[iy, ix, 1])

        grid = vtk.vtkStructuredGrid()
        grid.SetDimensions(ny, nx, 1)
        grid.SetPoints(pts)

        # make mapper
        filter = vtk.vtkStructuredGridGeometryFilter()
        filter.SetInputData(grid)

        # texture stuff
        self.ttp.SetInputConnection(filter.GetOutputPort())

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(self.ttp.GetOutputPort())

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        #
        #
        actor.GetProperty().SetAmbient(1.0)
        actor.GetProperty().SetDiffuse(0.0)
        actor.GetProperty().SetSpecular(0.0)
        actor.SetTexture(self.texture)

        # alternative: use PBR
        #
        # Does not render nicely: wave grid clearly visible
        #
        # props = actor.GetProperty()
        # props.SetInterpolationToPBR()
        # props.SetMetallic(0.8)
        # props.SetRoughness(0.1)

        self.pts = pts
        self.actor = actor
        self.elevation = elevation
        self.nt = nt
        self.period = wave_period
        self.x = x
        self.y = y

