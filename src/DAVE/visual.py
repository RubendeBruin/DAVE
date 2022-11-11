"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Ruben de Bruin - 2019

"""
import datetime
import logging
from copy import copy
from pathlib import Path
from typing import List
from warnings import warn

import numpy as np
from enum import Enum

from scipy.spatial import ConvexHull

import vtkmodules.qt
vtkmodules.qt.PyQtImpl = "PySide2"

import vedo as vp  # ref: https://github.com/marcomusy/vedo
import vtk

import vedo.settings
from DAVE.visual_helpers.vtkBlenderLikeInteractionStyle import BlenderStyle
from DAVE.visual_helpers.vtkHelpers import create_shearline_actors, create_momentline_actors


# vedo.settings.renderLinesAsTubes = True

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
    COLOR_SELECT_255,
    UC_CMAP,
)

import DAVE.scene as vf
import DAVE.scene as dn
import DAVE.settings_visuals


"""
visual visualizes a scene using vtk and vedo helpers

Basic data structure:

Viewport
 - node_visuals (VisualActors)
    - [node] -> reference to corresponding node 
    - actors [dict]
        - [ActorType]
        
        <the appearance of these visuals is determined by painters which are activated by update_visibility>
        
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
is updated or can be removed manually be calling remove_temporary_actors


Outlines
=========
Outlines are individual actors. They attach to a actor and do not have a reference to the node or the other actors
of the node.
They copy the data of the actor that they outline when they are created. They update based on the global-transform of
the referenced actor.

If the geometry of the referenced actor (ie the vertices) have changed then the outline needs to be re-created.
In that case the ._vertices_changed = True flag of the outlined actor should be set. 

"""

from DAVE.visual_helpers.vtkHelpers import *

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
    """

    Actor.Data -> TransformFilter -> EdgeDetection -> Actor
                   ^^^^^^^^^^^^^
                   this shall match the transform of the outlined actor

    This is set-up in this way to have the correct camera angle for the silhouette.

    If not used silhoutte but outlines only, then the transform filter can be set to identity
    and the transform can be applied on the actor instead. This saves re-computation in the
    edge detection

    """
    parent_vp_actor = None
    outline_actor = None
    outline_transform = None

    def update(self):

        # update transform

        do_silhouette = getattr(self.parent_vp_actor, "do_silhouette", True)
        I = vtk.vtkTransform()
        I.Identity()

        if do_silhouette:
            SetTransformIfDifferent(self.outline_actor, I) # outline actor shall have identity

            new_matrix = self.parent_vp_actor.GetMatrix()

            current_matrix = self.outline_transform.GetTransform().GetMatrix()

            if not vtkMatricesAlmostEqual(new_matrix, current_matrix):
                self.outline_transform.GetTransform().SetMatrix(new_matrix)

        else:

            if not vtkMatricesAlmostEqual(I.GetMatrix(), self.outline_transform.GetTransform().GetMatrix()):
                self.outline_transform.SetTransform(I)

            SetMatrixIfDifferent(self.outline_actor, self.parent_vp_actor.GetMatrix())  # outline transform shall have identity


        self.outline_actor.SetVisibility(
            getattr(self.parent_vp_actor, "xray", False)
            or self.parent_vp_actor.GetVisibility()
        )

        # get color
        color = getattr(self.parent_vp_actor, "_outline_color", (0, 0, 0))
        self.outline_actor.GetProperty().SetColor(
            color[0] / 255, color[1] / 255, color[2] / 255
        )
        self.outline_actor.GetProperty().SetLineWidth(2)





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


    @property
    def center_position(self):
        return self.actors["main"].GetCenter()

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
            raise ValueError("Position should have length 3")

        if self.label_actor is not None:
            self.label_actor.SetAttachmentPoint(*position)

    def labelCreate(self, txt):
        la = vtk.vtkCaptionActor2D()
        la.SetCaption(txt)

        position = self.center_position

        # print(f'{txt} : at {position}')

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

            self.label_actor.SetAttachmentPoint(*self.center_position)

        return self.label_actor

    def update_paint(self, settings: ViewportSettings):
        """Updates the painting for this visual

        Painting depends on the node type of this visual.
        The properties for the individual actors of this visual are
        stored in

        ps is the painter_settings dictionary

        """

        ps = settings.painter_settings

        if ps is None:
            print("No painter settings, ugly world :(")
            return

        # Get the class of the node,
        # this includes custom states for multi-state nodes

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

        # Get the corresponding paint

        if node_class in ps:
            node_painter_settings = ps[node_class]
        else:
            print(f"No paint for {node_class}")
            return  # no settings available

        # Override paint if a color is defined for the node
        if self.node.color is not None:
            new_painter_settings = dict()
            for k, value in node_painter_settings.items():
                v = copy(value)
                v.surfaceColor = self.node.color
                v.lineColor = self.node.color
                new_painter_settings[k] = v

            node_painter_settings = new_painter_settings

        # Override paint settings if node is selected or sub-selected

        if self._is_selected:
            new_painter_settings = dict()
            for k, value in node_painter_settings.items():
                v = copy(value)
                v.surfaceColor = COLOR_SELECT_255
                v.lineColor = COLOR_SELECT_255
                new_painter_settings[k] = v

            new_painter_settings["main"].labelShow = True

            node_painter_settings = new_painter_settings

        if self._is_sub_selected:
            new_painter_settings = dict()

            for k, value in node_painter_settings.items():
                v = copy(value)
                v.alpha = min(v.alpha, 0.4)
                new_painter_settings[k] = v
            node_painter_settings = new_painter_settings

        # label
        if settings.label_scale > 0:
            self.label_actor.SetVisibility(node_painter_settings["main"].labelShow)
        else:
            self.label_actor.SetVisibility(False)

        # check for UCs, create uc_paint accordingly
        uc_paint = None
        if settings.paint_uc:

            uc_node = self.node
            if isinstance(
                self.node, DAVE.Visual
            ):  # Visuals adopt the color of their parent
                if self.node.parent is not None:
                    uc_node = self.node.parent

            uc = uc_node.UC
            if uc is not None:
                if uc > 1:
                    uc_paint = (1, 0, 1)  # ugly pink
                else:
                    uc_paint = UC_CMAP(round(100 * uc))

        # Loop over the individual actors in the node
        # and apply their paint or the uc_paint

        for key, actor in self.actors.items():

            # start_time = actor.GetMTime()

            if '#' in key:
                key = key.split('#')[0]

            if key in node_painter_settings:
                actor_settings = node_painter_settings[key]
            else:
                print(f"No paint for actor {node_class} {key}")
                continue

            # ****** Some very-custom code ********
            if settings.show_global:
                if node_class == "Buoyancy":
                    if key == "waterplane":
                        actor.off()
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

                if uc_paint is None:

                    props.SetColor(
                        (
                            actor_settings.surfaceColor[0] / 255,
                            actor_settings.surfaceColor[1] / 255,
                            actor_settings.surfaceColor[2] / 255,
                        )
                    )
                else:
                    props.SetColor(uc_paint[:3])

                if self._is_selected:
                    props.SetOpacity(actor_settings.alpha)
                    props.SetMetallic(1.0)
                    props.SetRoughness(0.3)
                else:
                    props.SetOpacity(actor_settings.alpha)
                    props.SetMetallic(actor_settings.metallic)
                    props.SetRoughness(actor_settings.roughness)

            else:
                actor.GetProperty().SetRepresentationToWireframe()

            if getattr(self.node, '_draw_fat', False):
                actor.linewidth(2*actor_settings.lineWidth)
            else:
                actor.linewidth(actor_settings.lineWidth)

            if actor_settings.lineWidth > 0:
                if uc_paint is None:
                    # actor.lineColor(   # See vedo Issue https://github.com/marcomusy/vedo/issues/583
                    #     (
                    #         actor_settings.lineColor[0] / 255,
                    #         actor_settings.lineColor[1] / 255,
                    #         actor_settings.lineColor[2] / 255,
                    #     )
                    # )
                    actor.GetProperty().SetColor( (
                            actor_settings.lineColor[0] / 255,
                            actor_settings.lineColor[1] / 255,
                            actor_settings.lineColor[2] / 255,
                        ))
                else:
                    actor.GetProperty().SetColor(uc_paint[:3])
            else:
                actor.GetProperty().SetLineWidth(0)

            # if actor.GetMTime() == start_time:
            #     print('Nothing changed')

    def update_geometry(self, viewport):
        """Updates the geometry of the actors to the current state of the node.
        This includes moving as well as changing meshes and volumes"""

        # update label name if needed
        self.labelUpdate(
            self.node.name
        )  # does not do anything if the label-name is unchanged

        # the following ifs all end with Return, so only a single one is executed

        if isinstance(self.node, vf.Visual):
            A = self.actors["main"]

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


            # Get the parent matrix (if any)
            if self.node.parent is not None:
                apply_parent_translation_on_transform(self.node.parent, t)

            SetTransformIfDifferent(A, t)


            return

        if isinstance(self.node, vf.Circle):
            A = self.actors["main"]


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

            SetTransformIfDifferent(A, t)

            return

        if isinstance(self.node, vf._Area):
            self.actors["main"].SetScale(np.sqrt(self.node.A))
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
            # 'main' is a cube spanning the upper surface of the SPMT
            # the center is at the center
            # the length extents half the distance between the axles
            # the width extents half the wheel_width

            N= self.node
            N.update()

            # The deck
            WHEEL_WIDTH = 1.0  # [m, a wheel is actually a pair of wheels]
            TOP_THICKNESS = 0.5  # m
            WHEEL_RADIUS = 0.3 # [m]#

            top_length = N.n_length * N.spacing_length
            top_width = (N.n_width - 1) * N.spacing_width + WHEEL_WIDTH

            top_deck = self.actors['main']
            top_deck.SetScale(top_length, top_width, TOP_THICKNESS)
            SetMatrixIfDifferent(top_deck, mat4x4_from_point_on_frame(N.parent, (0,0,-0.5*TOP_THICKNESS)))

            # The wheels
            #
            # sync the number of wheels
            n_wheels = N.n_length * N.n_width
            n_wheel_actors = len(self.actors) - 2 # 2 other actors

            #    wheel actors are named wheel#xx

            if n_wheel_actors > n_wheels:  # remove actors
                for i in range(n_wheel_actors-n_wheels):
                    name = f'wheel#{n_wheels + i}'
                    viewport.screen.remove(self.actors[name], render = False)
                    del self.actors[name]
            if n_wheel_actors < n_wheels: # add actors
                for i in range(n_wheels-n_wheel_actors):
                    actor = vp.Cylinder(pos = (0,0,0), r = WHEEL_RADIUS, height = WHEEL_WIDTH, axis = (0,1,0), res=24)
                    self.actors[f'wheel#{n_wheel_actors+i}'] = actor
                    viewport.screen.add(actor, render = False)

            # position the wheels
            axle_positions = N.axles
            extensions = N.extensions

            for i in range(n_wheels):
                actor = self.actors[f'wheel#{i}']
                pos = axle_positions[i]

                m44 = mat4x4_from_point_on_frame(self.node.parent, (pos[0],pos[1],-extensions[i] + WHEEL_RADIUS))
                SetMatrixIfDifferent(actor, m44)



            # The lines
            A = self.actors["line"]

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
                current_n_points = (
                    self.actors["footprint"]._mapper.GetInput().GetNumberOfPoints()
                )

                if isinstance(self.node, vf.Point):
                    p = self.node.position
                    local_position = [
                        (v[0] + p[0], v[1] + p[1], v[2] + p[2]) for v in fp
                    ]
                    if self.node.parent:
                        fp = [
                            self.node.parent.to_glob_position(loc)
                            for loc in local_position
                        ]
                    else:
                        fp = local_position

                elif isinstance(self.node, vf.Frame):
                    fp = [
                        self.node.to_glob_position(loc)
                        for loc in fp
                    ]

                else:
                    raise Exception('Footprint on node which is not a Point or Frame -- unexpected')

                if n_points == current_n_points:
                    self.actors["footprint"].points(fp)
                    self.actors["footprint"]._vertices_changed = True
                else:
                    # create a new actor
                    new_actor = actor_from_vertices_and_faces(
                        vertices=fp, faces=[range(n_points)]
                    )

                    print("number of points changed, creating new")

                    if viewport.screen is not None:
                        viewport.screen.remove(self.actors["footprint"])
                        # remove outline as well
                        self.actors["footprint"] = new_actor
                        viewport.screen.add(self.actors["footprint"], render=False)

        if isinstance(self.node, vf.Point):
            t = vtk.vtkTransform()
            t.Identity()

            t.Translate(self.node.global_position)


            SetTransformIfDifferent(self.actors["main"], t)
            SetScaleIfDifferent(self.actors["main"],viewport.settings.geometry_scale)

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

            SetTransformIfDifferent(self.actors["main"], t)
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

            self.update_paint(viewport.settings)

            return

        if isinstance(self.node, vf.WaveInteraction1):
            t = vtk.vtkTransform()
            t.Identity()
            t.Translate(self.node.parent.to_glob_position(self.node.offset))
            SetTransformIfDifferent(self.actors["main"], t)
            SetScaleIfDifferent(self.actors["main"], viewport.settings.geometry_scale)
            return

        if isinstance(self.node, vf.Force):

            # check is the arrows are still what they should be
            if not np.all(
                self.actors["main"]._force
                == viewport._scaled_force_vector(self.node.force)
            ):
                viewport.screen.remove(self.actors["main"], render=False)

                endpoint = viewport._scaled_force_vector(self.node.force)

                p = vtkArrowActor(
                    startPoint=(0, 0, 0), endPoint=endpoint, res=RESOLUTION_ARROW
                )
                p.PickableOn()
                p.actor_type = ActorType.FORCE
                p._force = endpoint

                self.actors["main"] = p
                viewport.screen.add(self.actors["main"], render=False)

            # check is the arrows are still what they should be
            if not np.all(
                np.array(self.actors["moment1"]._moment)
                == viewport._scaled_force_vector(self.node.moment)
            ):
                viewport.screen.remove(self.actors["moment1"], render=False)
                viewport.screen.remove(self.actors["moment2"], render=False)

                endpoint = viewport._scaled_force_vector(self.node.moment)
                p = vtkArrowActor(
                    startPoint=(0, 0, 0), endPoint=endpoint, res=RESOLUTION_ARROW
                )
                p.PickableOn()
                p.actor_type = ActorType.FORCE
                p._moment = endpoint
                self.actors["moment1"] = p

                p = vtkArrowHeadActor(startPoint=0.96*endpoint, endPoint=1.36*endpoint,res=RESOLUTION_ARROW)
                p.PickableOn()
                p.actor_type = ActorType.FORCE

                p.actor_type = ActorType.FORCE
                self.actors["moment2"] = p

                viewport.screen.add(self.actors["moment1"], render=False)
                viewport.screen.add(self.actors["moment2"], render=False)

            t = self.actors["main"].get_transform()
            t.Identity()
            t.Translate(self.node.parent.global_position)
            for a in self.actors.values():
                SetTransformIfDifferent(a, t)

            return

        if isinstance(self.node, vf.RigidBody):

            # Some custom code to place and scale the Actor[3] of the body.
            # This actor should be placed at the CoG position and scaled to a solid steel block

            # The CoG
            if viewport.settings.cog_do_normalize:
                scale = 1
            else:
                scale = (self.node.mass / 8.050) ** (1 / 3)  # density of steel
            scale = scale * viewport.settings.cog_scale

            t = vtk.vtkTransform()
            t.Identity()

            t.Translate(self.node.cog)    # the set to local cog position
            t.Scale(scale, scale, scale)  # then scale

            # apply parent transform
            mat4x4 = transform_to_mat4x4(self.node.global_transform)
            t.PostMultiply()
            t.Concatenate(mat4x4)

            SetTransformIfDifferent(self.actors["main"], t)

            # The arrows
            t = vtk.vtkTransform()
            t.Identity()
            t.Scale(viewport.settings.geometry_scale,
                    viewport.settings.geometry_scale,
                    viewport.settings.geometry_scale)  # scale first

            t.PostMultiply()
            t.Concatenate(mat4x4)  # apply position and orientatation

            for key in ('x','y','z'):
                SetTransformIfDifferent(self.actors[key], t)


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
                current_transform = self.actors["main"].get_transform().GetMatrix()

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
                    SetMatrixIfDifferent(self.actors["main"],mat4x4)

            if not changed:
                if isinstance(self.node, vf.Tank):
                    # the tank fill may have changed,
                    # only skip if fill percentage has changed with less than 1e-3%
                    vfp = getattr(self, "_visualized_fill_percentage", -1)
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
            SetMatrixIfDifferent(self.actors["cob"],transform_from_point(*cob))

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
            self.actors["waterplane"]._vertices_changed = True

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
                self.update_paint(viewport.settings)

                if viewport.screen is not None:
                    viewport.screen.add(vis, render=False)

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
            just_created = getattr(self, "__just_created", True)
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

            # Points are the vertices in global axis system (transforms applied)
            points = self.actors["main"].points(True)
            self.setLabelPosition(np.mean(points, axis=1).flatten())

            # Update the CoG
            # move the CoG to the new (global!) position
            SetMatrixIfDifferent(self.actors["cog"],transform_from_point(*self.node.cog))

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
                faces = self.actors["main"].faces()

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

                self._visualized_fill_percentage = (
                    self.node.fill_pct
                )  # store for "need_update" check

                vis = self.actors["fluid"]
                pts = vis.GetMapper().GetInput().GetPoints()
                npt = len(vertices)

                # Update the existing actor if the number of vertices stay the same
                # If not then delete the actor

                # check for number of points
                if pts.GetNumberOfPoints() == npt:
                    # print(f'setting points for {V.node.name}')
                    vis.points(vertices)

                    logging.info(
                        f"Updated global vertex postions for fluid visuals {self.node.name}"
                    )
                    vis._vertices_changed = True

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

                    logging.info(f"Creating new fluid actor for {self.node.name}")

                    if viewport.screen is not None:
                        viewport.screen.add(vis, render=False)

                if not self.node.visible:
                    vis.off()

            self._visual_volume = self.node.volume

            # viewport.update_painting(self)
            self.update_paint(viewport.settings)

            return

        if isinstance(self.node, vf.Frame):

            # The arrows
            t = vtk.vtkTransform()
            t.Identity()
            t.Scale(viewport.settings.geometry_scale,
                    viewport.settings.geometry_scale,
                    viewport.settings.geometry_scale)  # scale first


            mat4x4 = transform_to_mat4x4(self.node.global_transform)
            t.PostMultiply()
            t.Concatenate(mat4x4)  # apply position and orientatation

            for a in self.actors.values():
                SetTransformIfDifferent(a, t)


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
            SetMatrixIfDifferent(A, mat4x4)



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

        self.Jupyter = jupyter

        self.settings = ViewportSettings()

        self.quick_updates_only = (
            False  # Do not perform slow updates ( make animations quicker)
        )

        self._wavefield = None
        """WaveField object"""

        # colorbar image
        png = vtk.vtkPNGReader()
        png.SetFileName(
            str(Path(__file__).parent / "resources" / "uc_colorbar_smaller.png")
        )
        png.Update()

        imagemapper = vtk.vtkImageMapper()
        imagemapper.SetInputData(png.GetOutput())
        imagemapper.SetColorWindow(255)
        imagemapper.SetColorLevel(127.5)

        image = vtk.vtkActor2D()
        image.SetMapper(imagemapper)
        image.SetPosition(0, 0.95)

        self.colorbar_actor = image
        """The colorbar for UCs is a static image"""

        self.Style = BlenderStyle()
        self.Style.callbackCameraDirectionChanged = self._rotate_actors_due_to_camera_movement
        self.Style.callbackAnyKey = self.keyPressFunction

    @staticmethod
    def show_as_qt_app(s, painters=None, sea=False, boundary_edges=False):
        from PySide2.QtWidgets import QWidget, QApplication

        app = QApplication()
        widget = QWidget()
        widget.show()

        if painters is None:
            from DAVE.settings_visuals import PAINTERS

            painters = PAINTERS["Construction"]

        v = Viewport(scene=s)

        v.settings.painter_settings = painters

        v.settings.show_global = sea

        v.show_embedded(widget)
        v.quick_updates_only = False

        v.create_node_visuals()
        # v.add_new_node_actors_to_screen()

        v.position_visuals()
        v.add_new_node_actors_to_screen()  # position visuals may create new actors
        v.update_visibility()

        v.zoom_all()

        app.exec_()

    def initialize_node_drag(self, nodes):
        # Initialize dragging on selected node

        actors = []
        outlines = []

        for node in nodes:
            actors.extend([*self.actor_from_node(node).actors.values()])
            outlines.extend([ol.outline_actor for ol in self.node_outlines if ol.parent_vp_actor in actors])


        self.Style.StartDragOnProps([*actors, *outlines])


    def add_temporary_actor(self, actor: vtk.vtkActor):
        self.temporary_actors.append(actor)
        if self.screen:
            self.screen.add(actor, render=False)

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

        # Remove outlines of nodes for which the input data has changed
        # such that they can be re-created

        to_be_deleted = []

        for ol in self.node_outlines:
            if getattr(ol.parent_vp_actor,'_vertices_changed', False):
                logging.info('Force-recreating outline due to vertices_changed flag on outlined actor')
                to_be_deleted.append(ol)
                _outlines.remove(ol.parent_vp_actor)
                ol.parent_vp_actor._vertices_changed = False


        # loop over actors, add outlines if needed
        for vp_actor in self.screen.actors:

            if isinstance(
                vp_actor.GetProperty(), vtkmodules.vtkRenderingCore.vtkProperty2D
            ):  # annotations
                continue

            try:
                if vp_actor.GetProperty().GetRepresentation() == 1:  # wireframe
                    continue
            except:
                continue

            if getattr(vp_actor, "no_outline", False):
                continue

            do_silhouette = getattr(vp_actor, "do_silhouette", True)

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

                    if do_silhouette:

                        ol = vtk.vtkPolyDataSilhouette()
                        ol.SetInputConnection(tr.GetOutputPort())
                        ol.SetEnableFeatureAngle(True)
                        ol.SetCamera(camera)
                        ol.SetBorderEdges(True)
                    else:
                        ol = vtk.vtkFeatureEdges()
                        ol.SetColoring(False)  # does not seem to do anything
                        ol.SetInputConnection(tr.GetOutputPort())

                        ol.ExtractAllEdgeTypesOff()
                        ol.BoundaryEdgesOn()
                        ol.SetFeatureAngle(25)
                        ol.FeatureEdgesOn()

                    mapper = vtk.vtkPolyDataMapper()
                    mapper.SetInputConnection(ol.GetOutputPort())
                    mapper.ScalarVisibilityOff()  # No colors!

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
                    vp_actor._outline = record
                    self.node_outlines.append(record)

                    record.outline_actor.outlined_actor = vp_actor  # insert a ref to the original actor, used when clicking

        # Update transforms for outlines

        for record in self.node_outlines:
            # is the parent actor still present?
            if record.parent_vp_actor in self.screen.actors:

                record.update()

            else:
                # mark for deletion
                to_be_deleted.append(record)

        # Remove obsolete outlines
        to_be_deleted_actors = [oa.outline_actor for oa in to_be_deleted]
        self.screen.remove(to_be_deleted_actors)

        for record in to_be_deleted:
            self.node_outlines.remove(record)

    def focus_on(self, position):
        """Places the camera focus on position"""

        c = self.screen.camera

        cur_focus = np.array(c.GetFocalPoint())

        if np.linalg.norm(cur_focus - np.array(position)) < 1e-3:
            # already has focus, zoom in
            distance = np.array(c.GetPosition()) - cur_focus
            c.SetPosition(cur_focus + 0.9 * distance)
            self.screen.renderer.ResetCameraClippingRange()

        else:
            self.screen.camera.SetFocalPoint(position)

    def create_world_actors(self):
        """Creates the sea and global axes"""

        if "sea" in self.global_visuals:
            raise ValueError("Global visuals already created - can not create again")

        plane = vp.Plane(pos=(0, 0, 0), normal=(0, 0, 1), s =(1000, 1000)).c(
            COLOR_WATER
        )
        plane.texture(TEXTURE_SEA)
        plane.lighting(ambient=1.0, diffuse=0.0, specular=0.0, specular_power=1e-7)
        plane.alpha(0.4)

        self.global_visuals["sea"] = plane
        self.global_visuals["sea"].actor_type = ActorType.GLOBAL
        self.global_visuals["sea"].no_outline = False  # If outlines are used, then they need to be disabled
                                                       # when performing a zoom-fit (see zoom-all)
        self.global_visuals["sea"].negative = False

        self.global_visuals["main"] = vp.Line((0, 0, 0), (10, 0, 0)).c("red")
        self.global_visuals["main"].actor_type = ActorType.GEOMETRY
        self.global_visuals["main"].negative = True

        self.global_visuals["y"] = vp.Line((0, 0, 0), (0, 10, 0)).c("green")
        self.global_visuals["y"].actor_type = ActorType.GEOMETRY
        self.global_visuals["y"].negative = True

        self.global_visuals["z"] = vp.Line((0, 0, 0), (0, 0, 10)).c("blue")
        self.global_visuals["z"].actor_type = ActorType.GEOMETRY
        self.global_visuals["z"].negative = True

        for actor in self.global_visuals.values():
            self.screen.add(actor, render=False)

        wind_actor = vp.Lines(
            start_pts=[(0, 0, 0), (0, 0, 0)], end_pts=[(10, 0, 0), (-0.5, 1, 0)]
        )
        wind_actor.c(DAVE.settings_visuals._DARK_GRAY)
        wind_actor.lw(1)

        points = [(3 + 4 * i / 36, 0.4 * np.cos(i / 4), 0) for i in range(36)]

        current_actor = vp.Lines(
            start_pts=[(0, 0, 0), (10, 0, 0), (10, 0, 0), *points[:-1]],
            end_pts=[(10, 0, 0), (9, 0.3, 0), (9, -0.3, 0), *points[1:]],
        )
        current_actor.c(DAVE.settings_visuals._BLUE_DARK)
        current_actor.lw(1)

        self.current_actor = current_actor
        self.wind_actor = wind_actor

        self.screen.add(self.colorbar_actor, render=False)

    def add_wind_and_current_actors(self):
        self.screen.add_icon(self.wind_actor, pos=2, size=0.06)
        self.screen.add_icon(self.current_actor, pos=4, size=0.06)

    def deselect_all(self):

        for v in self.node_visuals:
            if v._is_selected:
                v._is_selected = False
                v.update_paint(self.settings)

    def node_from_vtk_actor(self, actor):
        """
        Given a vkt actor, find the corresponding node
        Args:
            actor: vtkActor

        Returns:

        """
        # print(actor)

        outlined_actor = getattr(actor,'outlined_actor',None)
        if outlined_actor is not None:
            return self.node_from_vtk_actor(outlined_actor)

        for v in self.node_visuals:
            for a in v.actors.values():
                if a == actor:
                    return v.node
            if v.label_actor == actor:
                return v.node

        return None

    def actor_from_node(self, node) -> VisualActor or None:
        """Finds the VisualActor belonging to node"""
        for v in self.node_visuals:
            if v.node is node:
                return v
        return None

    def outline_from_actor(self, actor):
        """Return the actor that outlines actor if any, else returns None"""
        for a in self.node_outlines:
            if a.parent_vp_actor == actor:
                return a.outline_actor
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



    def toggle_2D(self):
        """Toggles between 2d and 3d mode. Returns True if mode is 2d after toggling"""
        self.Style.ToggleParallelProjection()
        return bool(self.renderer.GetActiveCamera().GetParallelProjection())


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
                    N._visualObject
                    if N._visualObject is not None:
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

                # disable backface
                backProp = vtk.vtkProperty()
                backProp.SetOpacity(0)
                vis.SetBackfaceProperty(backProp)

                actors["main"] = vis

            if isinstance(N, vf.Visual):
                file = self.scene.get_resource_path(N.path)
                visual = vp_actor_from_file(file)

                if N.visual_outline == dn.VisualOutlineType.NONE:
                    visual.no_outline = True
                    visual.do_silhouette = False
                elif N.visual_outline == dn.VisualOutlineType.FEATURE:
                    visual.do_silhouette = False
                    visual.no_outline = False
                else:
                    visual.do_silhouette = True
                    visual.no_outline = False

                visual.loaded_obj = file
                visual.actor_type = ActorType.VISUAL
                actors["main"] = visual

            if isinstance(N, vf.Frame):
                size = 1
                ar = vtkArrowActor((0, 0, 0), (size, 0, 0), res=RESOLUTION_ARROW)
                ag = vtkArrowActor((0, 0, 0), (0, size, 0), res=RESOLUTION_ARROW)
                ab = vtkArrowActor((0, 0, 0), (0, 0, size), res=RESOLUTION_ARROW)

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
                actors["footprint"] = vp.Cube(side=0.00001)  # dummy

            if isinstance(N, vf._Area):  # wind or current area
                # circle with area 1m2
                # and then scale with sqrt(A)
                # A = pi * r**2 --> r = sqrt(1/pi)
                actors["main"] = vp.Circle(res=36, r=np.sqrt(1 / np.pi))
                actors["main"].SetScale(np.sqrt(N.A))

            if isinstance(N, vf.RigidBody):
                # a rigidbody is also an axis

                cog = vp_actor_from_file(self.scene.get_resource_path("res: cog.obj"))
                cog.actor_type = ActorType.COG

                # switch the CoG to be the main actor
                actors["x"] = actors["main"]
                actors["main"] = cog

            if isinstance(N, vf.Point):
                size = 0.5
                p = vp.Sphere(pos=(0, 0, 0), r=size / 2, res=RESOLUTION_SPHERE)
                p.actor_type = ActorType.GEOMETRY
                actors["main"] = p

                # footprint
                actors["footprint"] = vp.Cube(side=0.00001)  # dummy

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
                p = vtkArrowActor(
                    startPoint=(0, 0, 0), endPoint=endpoint, res=RESOLUTION_ARROW
                )
                p.PickableOn()
                p.actor_type = ActorType.FORCE
                p._force = endpoint

                actors["main"] = p

                endpoint = self._scaled_force_vector(N.moment)
                p = vtkArrowActor(
                    startPoint=(0, 0, 0), endPoint=endpoint, res=RESOLUTION_ARROW
                )
                p.PickableOn()
                p.actor_type = ActorType.FORCE
                p._moment = endpoint
                actors["moment1"] = p

                p = vtkArrowHeadActor(startPoint=0.96*endpoint, endPoint=1.36*endpoint,
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

                # SPMT
                #
                # 'main' is a cube spanning the upper surface of the SPMT
                # the center is at the center
                # the length extents half the distance between the axles
                # the width extents half the wheel_width

                WHEEL_WIDTH = 1.0 # [m, a wheel is actually a pair of wheels]
                TOP_THICKNESS = 0.5 # m

                top_length = N.n_length * N.spacing_length
                top_width = (N.n_width-1) * N.spacing_width + WHEEL_WIDTH

                actors["main"] = vp.Cube(side=1)

                gp = N.get_actual_global_points()
                if gp:
                    a = vp.Line(gp, lw=3)
                else:
                    a = vp.Line([(0, 0, 0), (0, 0, 0.1), (0, 0, 0)], lw=3)

                a.actor_type = ActorType.CABLE
                a.SetPickable(True)
                actors["line"] = a

            if isinstance(N, vf.Beam):

                gp = N.global_positions

                if len(gp) > 0:
                    a = vp.Line(gp)
                else:
                    a = vp.Line([(0, 0, 0), (0, 0, 0.1), (0, 0, 0)])

                a.SetPickable(True)

                a.actor_type = ActorType.CABLE
                actors["main"] = a

            if isinstance(N, vf.Connector2d):

                points = list()

                for i in range(2):
                    points.append((0, 0, 0))

                a = vp.Line(points)
                a.actor_type = ActorType.CABLE

                a.SetPickable(True)

                actors["main"] = a

            if isinstance(N, vf.LC6d):

                points = list()

                for i in range(2):
                    points.append((0, 0, 0))

                a = vp.Line(points)
                a.actor_type = ActorType.CABLE

                a.SetPickable(True)

                actors["main"] = a

            if not actors:  # no actors created
                if not isinstance(N, dn.Manager):
                    print(f"No actors created for node {N.name}")
                continue

            va = VisualActor(actors, N)
            va.labelUpdate(N.name)
            N._visualObject = va
            N._visualObject.__just_created = True

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
                        getattr(V.actors["main"], "actor_type", None)
                        != ActorType.GLOBAL
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

        self._rotate_actors_due_to_camera_movement()

        self.update_outlines()

        # update wind and current actors
        transform = vtk.vtkTransform()
        transform.Identity()
        transform.RotateZ(self.scene.wind_direction)

        SetTransformIfDifferent(self.wind_actor, transform)

        transform = vtk.vtkTransform()
        transform.Identity()
        transform.RotateZ(self.scene.current_direction)

        SetTransformIfDifferent(self.current_actor, transform)

        if self.scene.wind_velocity > 0:
            self.wind_actor.SetScale(1.0)
        else:
            self.wind_actor.SetScale(0.0)

        if self.scene.current_velocity > 0:
            self.current_actor.SetScale(1.0)
        else:
            self.current_actor.SetScale(0.0)

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
                self.screen.add(to_be_added, render=False)

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
                    va.actors["main"] = vp_actor_from_file(file)
                    va.actors["main"].loaded_obj = file
                    va.actors["main"].actor_type = ActorType.VISUAL

                    # set the outline visibility (copy from "create")

                    if va.node.visual_outline == dn.VisualOutlineType.NONE:
                        va.actors["main"].no_outline = True
                        va.actors["main"].do_silhouette = False
                    elif va.node.visual_outline == dn.VisualOutlineType.FEATURE:
                        va.actors["main"].do_silhouette = False
                        va.actors["main"].no_outline = False
                    else:
                        va.actors["main"].do_silhouette = True
                        va.actors["main"].no_outline = False

                    if not va.node.visible:
                        va.actors["main"].off()

                    self.screen.add(va.actors["main"], render=False)

                if (
                    isinstance(va.node, vf.Buoyancy)
                    or isinstance(va.node, vf.ContactMesh)
                    or isinstance(va.node, vf.Tank)
                ):
                    if va.node.trimesh._new_mesh:

                        # va.node.update() # the whole scene is already updated when executing code

                        new_mesh = actor_from_trimesh(va.node.trimesh._TriMesh)
                        new_mesh.no_outline = True

                        if isinstance(va.node, vf.ContactMesh):
                            backProp = vtk.vtkProperty()
                            backProp.SetOpacity(0)
                            new_mesh.SetBackfaceProperty(backProp)

                        if new_mesh is not None:
                            self.screen.clear(va.actors["main"])

                            va.actors["main"] = new_mesh
                            va.actors["main"].actor_type = ActorType.MESH_OR_CONNECTOR

                            if va.node.parent is not None:
                                tr = va.node.parent.global_transform
                                mat4x4 = transform_to_mat4x4(tr)
                                SetMatrixIfDifferent(va.actors["main"],mat4x4)

                            else:
                                print("Trimesh without a parent")

                            if not va.node.visible:
                                va.actors["main"].off()

                            self.screen.add(va.actors["main"], render=False)  # add after positioning

                            # va.node.trimesh._new_mesh = False  # is set to False by position_visuals

            # self.set_default_dsa()

    def shutdown_qt(self):
        """Stops the renderer such that the application can close without issues"""

        if self.vtkWidget:
            ren = self.vtkWidget.GetRenderWindow()
            iren = ren.GetInteractor()
            ren.Finalize()
            iren.TerminateApp()

    def setup_screen(self, offscreen=False, size=(800, 500)):
        """Creates the plotter instance and stores it in self.screen

        If offscreen = True then an offscreen plotter is made
        """

        if offscreen:
            self.screen = vp.Plotter(axes=0, offscreen=True, size=size, backend='2d')

        else:

            if (
                self.Jupyter and self.vtkWidget is None
            ):  # it is possible to launch the Gui from jupyter, so check for both

                # create embedded notebook (k3d) view
                import vedo as vtkp

                # vtkp.settings.embedWindow(backend="k3d")
                self.screen = vp.Plotter(axes=4, bg=COLOR_BG1, bg2=COLOR_BG2,backend="k3d")

            else:

                if self.vtkWidget is None:

                    # create stand-alone interactive view
                    import vedo as vtkp

                    # vtkp.settings.embedWindow(

                    self.screen = vp.plotter.Plotter(
                        interactive=True,
                        offscreen=False,
                        axes=4,
                        bg=COLOR_BG1,
                        bg2=COLOR_BG2,
                        backend=None
                    )

                else:

                    # create embedded Qt view
                    import vedo as vtkp

                    # vtkp.settings.embedWindow(backend=None)

                    self.screen = vp.plotter.Plotter(
                        qt_widget=self.vtkWidget, axes=4, bg=COLOR_BG1, bg2=COLOR_BG2, backend=None
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
        self.ssao.SetRadius(5)
        self.ssao.SetDelegatePass(basicPasses)
        self.ssao.SetKernelSize(50)
        self.ssao.SetBlur(True)

        # light = vtk.vtkLight()
        # light.SetLightTypeToCameraLight()
        # light.SetIntensity(10)

        for r in self.screen.renderers:
            r.ResetCamera()
            # r.AddLight(light)

            r.UseImageBasedLightingOn()
            r.SetEnvironmentTexture(texture)

            r.SetUseDepthPeeling(True)

            # r.SetLightFollowCamera(True)

            r.Modified()

    def show(self, include_outlines=True, zoom_fit=False):
        """Add actors to screen and show

        If purpose is to show embedded, then call show_embedded instead
        """
        if self.screen is None:
            raise Exception("Please call setup_screen first")

        # vp.settings.lightFollowsCamera = True

        # self.create_world_actors()

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
                    self.screen.add(a, render=False)

            self.update_visibility()  # needs to be called after actors have been added to screen
            self.update_global_visibility()

            self.screen.resetcam = False

            for outline in self.node_outlines:
                self.screen.add(outline.outline_actor, render=False)

            return self.screen.show(resetcam=zoom_fit)

        else:

            screen = self.screen

            for va in self.node_visuals:
                for a in va.actors.values():
                    screen.add(a, render=False)

            if include_outlines:
                for outline in self.node_outlines:
                    screen.add(outline.outline_actor, render=False)

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

    def zoom_all(self):
        """Set camera to view the whole scene (ignoring the sea)"""
        sea_actor = self.global_visuals["sea"]
        sea_actor.SetUseBounds(False)

        # find outline actor for sea
        outline_node = self.outline_from_actor(sea_actor)
        if outline_node is not None:
            outline_node.SetUseBounds(False)  # and keep at False

        # check if style can be used
        if self.Style.GetCurrentRenderer():
            self.Style.ZoomFit()
        else:
            try:
                self.renderer.ResetCamera()  # try to use the current renderer
            except:
                warn('Can not perform zoom-all, no active renderer/camera')

        sea_actor.SetUseBounds(True)

    def onMouseRight(self, info):
        if self.mouseRightEvent is not None:
            self.mouseRightEvent(info)

    def show_embedded(self, target_frame):
        """target frame : QFrame"""

        from PySide2.QtWidgets import QVBoxLayout
        from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

        # add a widget to gui
        vl = QVBoxLayout()
        vl.setContentsMargins(0, 0, 0, 0)
        self.target_frame = target_frame
        self.vtkWidget = QVTKRenderWindowInteractor(target_frame)

        vl.addWidget(self.vtkWidget)
        target_frame.setLayout(vl)

        # self.vtkWidget.setMouseTracking(True)

        self.setup_screen()
        screen = self.show()

        self.renwin = self.vtkWidget.GetRenderWindow()
        self.renderer = screen.renderers[0]

        self.renwin.AddRenderer(self.renderer)

        iren = self.renwin.GetInteractor()

        style = self.Style


        iren.SetInteractorStyle(style)

        # iren.AddObserver("LeftButtonPressEvent", self._leftmousepress)
        # iren.AddObserver("RightButtonPressEvent", screen._mouseright)
        # iren.AddObserver("MiddleButtonPressEvent", screen._mousemiddle)
        # iren.AddObserver("MouseMoveEvent", self.mouseMoveFunction)
        # iren.AddObserver("KeyPressEvent", self.keyPressFunction)
        # iren.AddObserver(vtk.vtkCommand.InteractionEvent, self.keep_up_up)

        iren.SetNumberOfFlyFrames(2)

        for r in screen.renderers:
            r.ResetCamera()

        iren.Start()

        # screen.mouseRightClickFunction = self.onMouseRight

        self.create_world_actors()
        self.add_wind_and_current_actors()




    def keyPressFunction(self, key):
        """Most key-pressed are handled by the Style,

        here we override some specific ones.

        Returning True make the style ignore the key-press

        """
        KEY = key.upper()

        if KEY == "A":
            self.zoom_all()
            self.refresh_embeded_view()
            return True


    def refresh_embeded_view(self):
        if self.vtkWidget is not None:
            self.vtkWidget.update()

    def update_visibility(self):
        """Updates the settings of the viewport to reflect the settings in self.settings.painter_settings"""

        for v in self.node_visuals:

            # on-off from node overrides everything
            if v.node is not None:
                for a in v.actors.values():
                    a.SetVisibility(v.node.visible)
                    if not v.node.visible:  # only disable xray, never enable
                        a.xray = False

                v.label_actor.SetVisibility(v.node.visible)

                if not v.node.visible:
                    continue  # no need to update paint on invisible actor

            v.update_paint(self.settings)

            if v._is_selected:
                v.labelUpdate(v.node.name)

        self.update_global_visibility()
        self.update_outlines()


    def update_global_visibility(self):
        """Syncs the visibility of the global actors to Viewport-settings"""

        if self.settings.show_global:
            for actor in self.global_visuals.values():
                if actor.negative:
                    actor.off()
                else:
                    actor.on()
        else:
            for actor in self.global_visuals.values():
                if actor.negative:
                    actor.on()
                else:
                    actor.off()

        self.colorbar_actor.SetVisibility(self.settings.paint_uc)

    def _rotate_actors_due_to_camera_movement(self):
        """Gets called when the camera has moved"""

        for V in self.node_visuals:
            node = V.node

            if isinstance(node, dn._Area):
                actor = V.actors["main"]

                # calculate scale
                scale = np.sqrt(node.A)

                if node.areakind == dn.AreaKind.SPHERE:
                    direction = self.screen.camera.GetDirectionOfProjection()
                elif node.areakind == dn.AreaKind.PLANE:
                    direction = node.direction
                    if node.parent.parent is not None:
                        direction = node.parent.parent.to_glob_direction(direction)
                else:
                    axis_direction = node.direction
                    if node.parent.parent is not None:
                        axis_direction = node.parent.parent.to_glob_direction(
                            axis_direction
                        )
                    camera_direction = self.screen.camera.GetDirectionOfProjection()

                    # the normal of the plane need to be
                    # 1. perpendicular to "direction"
                    # 2. in the same plane as "camera direction" and "direction"

                    temp = np.cross(axis_direction, camera_direction)
                    if np.linalg.norm(temp) < 1e-6:  # axis and camera are perpendicular
                        direction = self.screen.camera.GetViewUp()
                    else:
                        direction = np.cross(temp, axis_direction)
                        direction = direction / np.linalg.norm(direction)

                transform = transform_from_direction(
                    direction, position=node.parent.global_position, scale = scale
                )

                SetMatrixIfDifferent(actor,transform)
                if hasattr(actor, "_outline"):
                    actor._outline.update()


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
