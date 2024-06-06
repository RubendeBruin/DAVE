"""A VisualActor is the visual representation of a node or the global environment
node is a reference to the node it represents. If node is None then this is the global environment ("scenery")
a VisualActor can contain a number of vtk actors or vedo-actors. These are stored in a dictionary
An visualActor may have a label_actor. This is a 2D annotation
The appearance of a visual may change when it is selected. This is handled by select and deselect
"""

from copy import copy
import logging

import numpy as np

from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkRenderingCore import vtkActor

import DAVE.nodes as dn
from DAVE.visual_helpers.constants import *

from DAVE.settings_visuals import ViewportSettings, COLOR_SELECT_255
from DAVE.visual_helpers.vtkActorMakers import (
    Cylinder,
    Sphere,
    Arrow,
    ArrowHead,
    actor_from_trimesh,
    Mesh,
)
from DAVE.visual_helpers.vtkHelpers import (
    apply_parent_translation_on_transform,
    SetTransformIfDifferent,
    create_tube_data,
    update_line_to_points,
    SetMatrixIfDifferent,
    mat4x4_from_point_on_frame,
    SetScaleIfDifferent,
    transform_to_mat4x4,
    transform_from_point,
    update_vertices,
    update_mesh_from,
    add_lid_to_open_mesh,
    update_mesh,
    update_mesh_to_empty,
    update_mesh_polydata,
)


class VisualActor:
    def __init__(self, actors: dict, node):
        # check if 'main' is available
        if "main" not in actors:
            raise ValueError(
                f"one of the actors shall be called main, but got only keys: {actors.keys()}"
            )

        for k, v in actors.items():
            if not isinstance(v, vtkActor):
                raise ValueError(f"Actor {k} is not a vtkActor, but {type(v)}")

        self.actors = actors  # dict vtk actors. There shall be one called 'main'
        self.node = node  # Node
        # self.label_actor = None

        self.paint_state = ""  # some nodes change paint depending on their state

        self._is_selected = False
        self._is_sub_selected = (
            False  # parent of this object is selected - render transparent
        )

        self.info = None  # Holder for additional info

    @property
    def center_position(self):
        return self.actors["main"].GetCenter()

    def get_annotation_position(self, pos3d, pos1f: float or None):
        """Gets the position of the annotation in 3D space

        pos3d is the 3D position of the annotation
        pos1f is the 1D position of the annotation, None if not provided
        """

        # This is the fall-back option if the node does not have a get_annotation_position method

        if isinstance(self.node, dn.Point):
            return self.node.global_position

        if isinstance(self.node, dn.Cable):
            return self.node.get_point_along_cable(pos1f)

        if isinstance(self.node, dn.Beam):
            return self.node.get_point_along_beam(pos1f)

        if isinstance(self.node, dn.Frame):
            return self.node.to_glob_position(pos3d)

        return self.center_position

    def select(self):
        self._is_selected = True

    def on(self):
        for a in self.actors.values():
            a.SetVisibility(True)

    def off(self):
        for a in self.actors.values():
            a.SetVisibility(False)

    @property
    def visible(self):
        return self.actors["main"].GetVisibility()

    #
    # def setLabelPosition(self, position):
    #     if len(position) != 3:
    #         raise ValueError("Position should have length 3")
    #
    #     if self.label_actor is not None:
    #         self.label_actor.SetAttachmentPoint(*position)
    #
    # def labelCreate(self, txt):
    #     la = vtkCaptionActor2D()
    #     la.SetCaption(txt)
    #
    #     position = self.center_position
    #
    #     # print(f'{txt} : at {position}')
    #     la.GetProperty().SetColor(0, 0, 0)
    #     la.SetAttachmentPoint(*position)
    #
    #     la.SetPickable(True)
    #
    #     cap = la.GetTextActor().GetTextProperty()
    #
    #     la.GetTextActor().SetTextScaleModeToNone()
    #     la.GetTextActor().SetPickable(True)
    #
    #     tp = la.GetCaptionTextProperty()
    #     tp.SetBackgroundOpacity(1.0)
    #     tp.SetBackgroundColor(1.0, 1.0, 1.0)
    #     tp.FrameOn()
    #     tp.SetFrameColor(0, 0, 0)
    #     tp.SetFrameWidth(1)
    #
    #     cap.SetColor(0, 0, 0)
    #     la.SetBorder(False)
    #     cap.SetBold(False)
    #     cap.SetItalic(False)
    #
    #     cap.SetFontFamilyToArial()
    #
    #     la.no_outline = True
    #
    #     self.label_actor = la
    #
    # def labelUpdate(self, txt):
    #     if txt == "":
    #         if self.label_actor is not None:
    #             self.label_actor.SetVisibility(False)
    #             if self.label_actor.GetCaption() != txt:
    #                 self.label_actor.SetCaption(txt)
    #         return
    #
    #     if self.label_actor is None:
    #         self.labelCreate(txt)
    #     else:
    #         if self.label_actor.GetCaption() != txt:
    #             self.label_actor.SetCaption(txt)
    #
    #         self.label_actor.SetAttachmentPoint(*self.center_position)
    #
    #     return self.label_actor

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
            # check is node is still valid (not deleted). If not then return
            if not self.node.is_valid:
                return

            if isinstance(self.node, dn.ContactBall):
                node_class = f"ContactBall:{self.paint_state}"
            elif isinstance(self.node, dn.Tank):
                node_class = f"Tank:{self.paint_state}"
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

        if isinstance(self.node, dn.Cable):
            actor = self.actors["main"]
            mapper = actor.GetMapper()

            if (
                self.node.do_color_by_tension
                and not settings.paint_uc
                and self.node.color is None
            ):
                mapper.SetScalarModeToUsePointFieldData()
                mapper.ScalarVisibilityOn()
                mapper.SelectColorArray("TubeColors")
                mapper.Modified()
            else:
                mapper.ScalarVisibilityOff()

        if self._is_selected:
            new_painter_settings = dict()
            for k, value in node_painter_settings.items():
                v = copy(value)
                v.surfaceColor = COLOR_SELECT_255
                v.lineColor = COLOR_SELECT_255
                new_painter_settings[k] = v

            node_painter_settings = new_painter_settings

        if self._is_sub_selected:
            new_painter_settings = dict()

            for k, value in node_painter_settings.items():
                v = copy(value)
                v.alpha = min(v.alpha, 0.4)
                new_painter_settings[k] = v
            node_painter_settings = new_painter_settings

        # # label
        # if settings.label_scale > 0 and self.label_actor.GetCaption() != "":
        #     if (
        #         self.label_actor.GetVisibility()
        #         != node_painter_settings["main"].labelShow
        #     ):
        #         self.label_actor.SetVisibility(node_painter_settings["main"].labelShow)
        #
        #     ta = self.label_actor.GetTextActor()
        #
        #     txtprop = ta.GetTextProperty()
        #
        #     if txtprop.GetFontSize() != int(settings.label_scale * 10):
        #         txtprop.SetFontSize(int(settings.label_scale * 10))
        # else:
        #     self.label_actor.SetVisibility(False)

        # check for UCs, create uc_paint accordingly
        uc_paint = None
        if settings.paint_uc:
            uc_node = self.node
            if isinstance(
                self.node, dn.Visual
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
            props = actor.GetProperty()

            if "#" in key:
                key = key.split("#")[0]

            if key in node_painter_settings:
                actor_settings = node_painter_settings[key]
            else:
                print(f"No paint for actor {node_class} {key}")
                continue

            # ****** Some very-custom code for Buoyancy ********

            if node_class == "Buoyancy":
                if key == "waterplane":
                    if settings.show_sea or self.node.displacement <= 1e-6:
                        actor.SetVisibility(False)
                        continue
                if key == "cob":
                    # check if we have displacement
                    if self.node.displacement <= 1e-6:
                        actor.SetVisibility(False)
                        continue

            # set the "xray" property of the actor
            actor.xray = actor_settings.xray
            actor._outline_color = actor_settings.outlineColor

            # on or off
            if actor_settings.surfaceShow or actor_settings.lineWidth > 0:
                actor.SetVisibility(True)
            else:
                actor.SetVisibility(False)
                continue

            if actor_settings.surfaceShow:
                # props.SetInterpolationToPBR()
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
                    # props.SetMetallic(1.0)
                    # props.SetRoughness(0.3)
                else:
                    props.SetOpacity(actor_settings.alpha)
                    # props.SetMetallic(actor_settings.metallic)
                    # props.SetRoughness(actor_settings.roughness)

            else:
                props.SetRepresentationToWireframe()

            if getattr(self.node, "_draw_fat", False):
                props.SetLineWidth(2 * actor_settings.lineWidth)
            else:
                props.SetLineWidth(actor_settings.lineWidth)

            if actor_settings.lineWidth > 0:
                if uc_paint is None:
                    # actor.lineColor(   # See vedo Issue https://github.com/marcomusy/vedo/issues/583
                    #     (
                    #         actor_settings.lineColor[0] / 255,
                    #         actor_settings.lineColor[1] / 255,
                    #         actor_settings.lineColor[2] / 255,
                    #     )
                    # )
                    props.SetColor(
                        (
                            actor_settings.lineColor[0] / 255,
                            actor_settings.lineColor[1] / 255,
                            actor_settings.lineColor[2] / 255,
                        )
                    )
                else:
                    props.SetColor(uc_paint[:3])
            else:
                props.SetLineWidth(0)

            # if actor.GetMTime() == start_time:
            #     print('Nothing changed')

    def update_geometry(self, viewport):
        """Updates the geometry of the actors to the current state of the node.
        This includes moving as well as changing meshes and volumes"""

        # # update label name if needed
        # label_text = getattr(self.node, viewport.settings.label_property, "")

        # self.labelUpdate(
        #     label_text
        # )  # does not do anything if the label-name is unchanged

        # the following ifs all end with Return, so only a single one is executed

        if isinstance(self.node, dn.Visual):
            # A = self.actors["main"]
            for A in self.actors.values():

                t = vtkTransform()
                t.Identity()
                t.PostMultiply()

                t.Scale(self.node.scale)

                # calculate wxys from node.rotation
                r = self.node.rotation
                angle = (r[0] ** 2 + r[1] ** 2 + r[2] ** 2) ** (0.5)
                if angle > 0:
                    t.RotateWXYZ(angle, r[0] / angle, r[1] / angle, r[2] / angle)

                t.Translate(self.node.offset)

                # Get the parent matrix (if any)
                if self.node.parent is not None:
                    apply_parent_translation_on_transform(self.node.parent, t)

                SetTransformIfDifferent(A, t)

            return

        if isinstance(self.node, dn.Circle):
            A = self.actors["main"]

            t = vtkTransform()
            t.Identity()

            # scale to flat disk
            thickness = (
                (self.node.draw_stop - self.node.draw_start) / 2
                if self.node.is_roundbar
                else 0.1
            )

            if self.node.is_roundbar:
                move = (self.node.draw_start + self.node.draw_stop) / 2
                t.Translate(0, 0, move)

            t.Scale(self.node.radius, self.node.radius, thickness)

            # rotate z-axis (length axis of cylinder) is direction of axis
            axis = np.asarray(self.node.axis) / np.linalg.norm(self.node.axis)
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

        if isinstance(self.node, dn.WindOrCurrentArea):
            self.actors["main"].SetScale(np.sqrt(self.node.A))
            return

        if isinstance(self.node, dn.Cable):
            # # check the number of points
            A = self.actors["main"]

            points, tensions = self.node.get_points_and_tensions_for_visual()

            # get cable scale from painter settings
            ps = viewport.settings.painter_settings
            min_dia = ps["Cable"]["main"].optionalScale

            diameter = self.node.diameter
            diameter = max(diameter, min_dia)

            # check if anything has changed before updating
            old_points = getattr(A, "_actual_points", None)
            old_diameter = getattr(A, "_actual_diameter", None)
            old_tensions = getattr(A, "_actual_tensions", None)

            if old_points is not None:
                if len(old_points) == len(points):
                    if np.allclose(old_points, points):
                        if old_diameter == diameter:
                            if old_tensions is not None:
                                if np.allclose(old_tensions, tensions):
                                    print("Not updating cable visual")
                                    return

            A._actual_points = points
            A._actual_diameter = diameter
            A._actual_tensions = tensions

            if self.node._render_as_tube:
                new_data = create_tube_data(points, diameter, colors=tensions)
                update_mesh_polydata(A, new_data)
            else:
                if len(points) == 0:  # not yet created
                    return

                update_line_to_points(A, points)

            # self.setLabelPosition(np.mean(points, axis=0))

            return

        if isinstance(self.node, dn.SPMT):
            # 'main' is a cube spanning the upper surface of the SPMT
            # the center is at the center
            # the length extents half the distance between the axles
            # the width extents half the wheel_width

            N = self.node
            N.update()

            # The deck
            WHEEL_WIDTH = 1.0  # [m, a wheel is actually a pair of wheels]
            TOP_THICKNESS = 0.5  # m
            WHEEL_RADIUS = 0.3  # [m]#

            top_length = N.n_length * N.spacing_length
            top_width = (N.n_width - 1) * N.spacing_width + WHEEL_WIDTH

            top_deck = self.actors["main"]
            top_deck.SetScale(top_length, top_width, TOP_THICKNESS)
            SetMatrixIfDifferent(
                top_deck,
                mat4x4_from_point_on_frame(N.parent, (0, 0, -0.5 * TOP_THICKNESS)),
            )

            # The wheels
            #
            # sync the number of wheels
            n_wheels = N.n_length * N.n_width
            n_wheel_actors = len(self.actors) - 2  # 2 other actors

            #    wheel actors are named wheel#xx

            if n_wheel_actors > n_wheels:  # remove actors
                for i in range(n_wheel_actors - n_wheels):
                    name = f"wheel#{n_wheels + i}"
                    viewport.remove(self.actors[name])
                    del self.actors[name]
            if n_wheel_actors < n_wheels:  # add actors
                for i in range(n_wheels - n_wheel_actors):
                    actor = Cylinder(
                        pos=(0, 0, 0),
                        r=WHEEL_RADIUS,
                        height=WHEEL_WIDTH,
                        axis=(0, 1, 0),
                        res=24,
                    )
                    self.actors[f"wheel#{n_wheel_actors+i}"] = actor
                    viewport.add(actor)

            # position the wheels
            axle_positions = N.axles
            extensions = N.extensions

            for i in range(n_wheels):
                actor = self.actors[f"wheel#{i}"]
                pos = axle_positions[i]

                m44 = mat4x4_from_point_on_frame(
                    self.node.parent, (pos[0], pos[1], -extensions[i] + WHEEL_RADIUS)
                )
                SetMatrixIfDifferent(actor, m44)

            # The lines
            A = self.actors["line"]

            pts = self.node.get_actual_global_points()
            if len(pts) == 0:
                return

            update_line_to_points(A, pts)

            return

        if isinstance(self.node, dn.Beam):
            points = self.node.global_positions
            A = self.actors["main"]
            update_line_to_points(A, points)

            # self.setLabelPosition(np.mean(points, axis=0))

            return

        if isinstance(self.node, dn.Connector2d):
            A = self.actors["main"]

            points = list()
            points.append(self.node.nodeA.to_glob_position((0, 0, 0)))
            points.append(self.node.nodeB.to_glob_position((0, 0, 0)))

            # A.points(points)
            update_vertices(self.actors["main"], points)

            return

        if isinstance(self.node, dn.LC6d):
            A = self.actors["main"]

            points = list()
            points.append(self.node.main.to_glob_position((0, 0, 0)))
            points.append(self.node.secondary.to_glob_position((0, 0, 0)))

            # A.points(points)
            update_vertices(self.actors["main"], points)

            return

        if isinstance(self.node, dn.BallastSystem):
            return

        # footprints
        if isinstance(self.node, dn.HasFootprint):
            fp = self.node.footprint
            if fp:
                n_points = len(fp)
                current_n_points = (
                    self.actors["footprint"].GetMapper().GetInput().GetNumberOfPoints()
                )

                if isinstance(self.node, dn.Point):
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

                elif isinstance(self.node, dn.Frame):
                    fp = [self.node.to_glob_position(loc) for loc in fp]

                else:
                    raise Exception(
                        "Footprint on node which is not a Point or Frame -- unexpected"
                    )

                if n_points == current_n_points:
                    # self.actors["footprint"].points(fp)
                    actor = self.actors["footprint"]
                    update_vertices(actor, fp)
                    actor._vertices_changed = True

                else:
                    # create a new actor
                    new_actor = Mesh(
                        vertices=fp,
                        faces=[range(n_points)],
                        do_clean=True,
                    )

                    # print("number of points changed, creating new")

                    if viewport.renderer is not None:
                        viewport.remove(self.actors["footprint"])
                        # remove outline as well
                        self.actors["footprint"] = new_actor
                        viewport.add(self.actors["footprint"])

        if isinstance(self.node, dn.Point):
            t = vtkTransform()
            t.Identity()

            t.Translate(self.node.global_position)

            SetTransformIfDifferent(self.actors["main"], t)
            SetScaleIfDifferent(self.actors["main"], viewport.settings.geometry_scale)

            # self.setLabelPosition(self.node.global_position)
            return

        if isinstance(self.node, dn.ContactBall):
            self.node.update()

            t = vtkTransform()
            t.Identity()
            t.Translate(self.node.parent.global_position)

            # check radius
            if self.actors["main"]._r != self.node.radius:
                # Update radius by re-creating the polydata
                temp = Sphere(r=self.node.radius, res=RESOLUTION_SPHERE)
                update_mesh_from(self.actors["main"], temp)

                self.actors["main"]._r = self.node.radius

            SetTransformIfDifferent(self.actors["main"], t)
            # V.actors["main"].wireframe(V.node.contact_force_magnitude > 0)

            if self.node.can_contact:
                point1 = self.node.parent.global_position
                point2 = self.node.contactpoint

                update_line_to_points(self.actors["contact"], [point1, point2])

                self.actors["contact"].SetVisibility(True)
            else:
                self.actors["contact"].SetVisibility(False)

            # update paint settings
            if self.node.contact_force_magnitude > 0:  # do we have contact?
                self.paint_state = "contact"
            else:
                self.paint_state = "free"

            self.update_paint(viewport.settings)

            return

        if isinstance(self.node, dn.WaveInteraction1):
            t = vtkTransform()
            t.Identity()
            t.Translate(self.node.parent.to_glob_position(self.node.offset))
            SetTransformIfDifferent(self.actors["main"], t)
            SetScaleIfDifferent(self.actors["main"], viewport.settings.geometry_scale)
            return

        if isinstance(self.node, dn.Force):
            # check is the arrows are still what they should be
            if not np.all(
                self.actors["main"]._force
                == viewport._scaled_force_vector(self.node.global_force)
            ):
                viewport.remove(self.actors["main"])

                endpoint = viewport._scaled_force_vector(self.node.global_force)

                p = Arrow(startPoint=(0, 0, 0), endPoint=endpoint, res=RESOLUTION_ARROW)
                p.SetPickable(True)
                p.actor_type = ActorType.FORCE
                p._force = endpoint

                self.actors["main"] = p
                viewport.add(self.actors["main"])

            # check is the arrows are still what they should be
            if not np.all(
                np.array(self.actors["moment1"]._moment)
                == viewport._scaled_force_vector(self.node.global_moment)
            ):
                viewport.remove(self.actors["moment1"])
                viewport.remove(self.actors["moment2"])

                endpoint = viewport._scaled_force_vector(self.node.global_moment)
                p = Arrow(startPoint=(0, 0, 0), endPoint=endpoint, res=RESOLUTION_ARROW)
                p.SetPickable(True)
                p.actor_type = ActorType.FORCE
                p._moment = endpoint
                self.actors["moment1"] = p

                p = ArrowHead(
                    startPoint=0.96 * endpoint,
                    endPoint=1.36 * endpoint,
                    res=RESOLUTION_ARROW,
                )
                p.SetPickable(True)
                p.actor_type = ActorType.FORCE

                p.actor_type = ActorType.FORCE
                self.actors["moment2"] = p

                viewport.add(self.actors["moment1"])
                viewport.add(self.actors["moment2"])

            t = vtkTransform()
            t.Identity()
            t.Translate(self.node.parent.global_position)
            for a in self.actors.values():
                SetTransformIfDifferent(a, t)

            return

        if isinstance(self.node, dn.RigidBody):
            # Some custom code to place and scale the Actor[3] of the body.
            # This actor should be placed at the CoG position and scaled to a solid steel block

            # The CoG
            if viewport.settings.cog_do_normalize:
                scale = 1
            else:
                scale = (self.node.mass / 8.050) ** (1 / 3)  # density of steel
            scale = scale * viewport.settings.cog_scale

            t = vtkTransform()
            t.Identity()

            t.Translate(self.node.cog)  # the set to local cog position
            t.Scale(scale, scale, scale)  # then scale

            # apply parent transform
            mat4x4 = transform_to_mat4x4(self.node.global_transform)
            t.PostMultiply()
            t.Concatenate(mat4x4)

            SetTransformIfDifferent(self.actors["main"], t)

            # The arrows
            t = vtkTransform()
            t.Identity()
            t.Scale(
                viewport.settings.geometry_scale,
                viewport.settings.geometry_scale,
                viewport.settings.geometry_scale,
            )  # scale first

            t.PostMultiply()
            t.Concatenate(mat4x4)  # apply position and orientatation

            for key in ("x", "y", "z"):
                SetTransformIfDifferent(self.actors[key], t)

            return

        if (
            isinstance(self.node, dn.Buoyancy)
            or isinstance(self.node, dn.ContactMesh)
            or isinstance(self.node, dn.Tank)
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
                current_transform = self.actors[
                    "main"
                ].GetMatrix()  # current transform matrix

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
                    SetMatrixIfDifferent(self.actors["main"], mat4x4)

            if not changed:
                if isinstance(self.node, dn.Tank):
                    # the tank fill may have changed,
                    # only skip if fill percentage has changed with less than 1e-3%
                    vfp = getattr(self, "_visualized_fill_percentage", -1)
                    if abs(self.node.fill_pct - vfp) < 1e-3:
                        return

                else:
                    return  # skip the other update functions

        if isinstance(self.node, dn.Buoyancy):
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
                    a.SetVisibility(False)
                return

            # Update the CoB
            # move the CoB to the new (global!) position
            cob = self.node.cob
            SetMatrixIfDifferent(self.actors["cob"], transform_from_point(*cob))

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
            # self.actors["waterplane"].points(corners)
            update_vertices(self.actors["waterplane"], corners)

            self.actors["waterplane"]._vertices_changed = True

            # Instead of updating, remove the old actor and create a new one

            # remove already existing submerged mesh (if any)
            if "submerged_mesh" in self.actors:
                viewport.remove(self.actors["submerged_mesh"])
                del self.actors["submerged_mesh"]

            mesh = self.node._vfNode.current_mesh

            if mesh.nVertices > 0:  # only add when available
                vis = actor_from_trimesh(mesh)

                vis.actor_type = ActorType.MESH_OR_CONNECTOR
                self.actors["submerged_mesh"] = vis

                viewport.add(vis)

            self.update_paint(
                viewport.settings
            )  # needed to make the CoB and WaterPlane actors visible / invisible

            return

        if isinstance(self.node, dn.ContactMesh):
            return

        if isinstance(self.node, dn.Tank):
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
                    a.SetVisibility(False)
                return
            else:
                if self.node.visible:
                    for a in self.actors.values():
                        a.SetVisibility(True)

            # Update the actors
            self.node.update()

            # Update the CoG
            # move the CoG to the new (global!) position
            SetMatrixIfDifferent(
                self.actors["cog"], transform_from_point(*self.node.cog)
            )

            if self.node.volume <= 1:  # the "cog node" has a volume of
                self.actors["cog"].SetVisibility(False)
            else:
                self.actors["cog"].SetVisibility(True)

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

            # Fluid in tank

            # Construct a visual:
            #   - vertices
            #   - faces

            # There are the following options:
            # - tank is empty : no fluid
            # - tank is full  : use mesh from tank as input for fluid mesh
            # - in between

            fill_pct = self.node.fill_pct  # this also accounts for free-flooding

            if fill_pct <= 0:
                # self.actors["fluid"].SetVisibility(False)  # overridden elsewhere
                update_mesh_to_empty(self.actors["fluid"])
            elif fill_pct > 99.99:  # full
                update_mesh_from(
                    self.actors["fluid"],
                    self.actors["main"],
                    apply_soure_transform=True,
                )
            else:
                # get the mesh and vertices from the node, and update actor accordingly

                mesh = self.node._vfNode.current_mesh

                if mesh.nVertices == 0:
                    raise ValueError(f"No mesh returned for fluid in {self.node.name}")

                vertices = []
                for i in range(mesh.nVertices):
                    vertices.append(mesh.GetVertex(i))

                faces = []
                for i in range(mesh.nFaces):
                    faces.append(mesh.GetFace(i))

                add_lid_to_open_mesh(
                    vertices=vertices, faces=faces
                )  # results stored in-place

                update_mesh(self.actors["fluid"], vertices, faces)

            self._visual_volume = self.node.volume

            # viewport.update_painting(self)
            self.update_paint(viewport.settings)

            return

        if isinstance(self.node, dn.Frame):
            # The arrows
            t = vtkTransform()
            t.Identity()
            t.Scale(
                viewport.settings.geometry_scale,
                viewport.settings.geometry_scale,
                viewport.settings.geometry_scale,
            )  # scale first

            mat4x4 = transform_to_mat4x4(self.node.global_transform)
            t.PostMultiply()
            t.Concatenate(mat4x4)  # apply position and orientatation

            for a in self.actors.values():
                SetTransformIfDifferent(a, t)

            return

        # --- default ---
