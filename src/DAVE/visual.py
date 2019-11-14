"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Ruben de Bruin - 2019


  Some tools

"""

"""
visual visualizes a scene using vtkplotter


main class is VisualActor
this class contains a reference to a Node and a list of actors

a visual actor can be hidden by setting visible to False

each of the individual vtk-plotter actors has a "actor_type" property which is a enum ActorType

Note:
at this moment the outlines of the actors are created using a outline filter. This is expensive.
Probably more efficient to implement this using shaders. But only once VTK 9.0+ becomes standard as the shader
code will change.

"""

import vtkmodules.qt
vtkmodules.qt.PyQtImpl = 'PySide2'

import vtkplotter as vp   # ref: https://github.com/marcomusy/vtkplotter
import DAVE.scene as vf
import DAVE.constants as vc
import vtk
import numpy as np
from enum import Enum

def transform_to_mat4x4(transform):
    mat4x4 = vtk.vtkMatrix4x4()
    for i in range(4):
        for j in range(4):
            mat4x4.SetElement(i, j, transform[j * 4 + i])
    return mat4x4

def transform_from_point(x,y,z):
    mat4x4 = vtk.vtkMatrix4x4()
    mat4x4.SetElement(0, 3, x)
    mat4x4.SetElement(1, 3, y)
    mat4x4.SetElement(2, 3, z)
    return mat4x4

def actor_from_trimesh(trimesh):
    """Creates a vtkplotter.Actor from a pyo3d.TriMesh"""

    if trimesh.nFaces == 0:
        return None

    vertices = []
    for i in range(trimesh.nVertices):
        vertices.append(trimesh.GetVertex(i))

    faces = []
    for i in range(trimesh.nFaces):
        faces.append(trimesh.GetFace(i))

    return vp.actors.Actor([vertices, faces]).alpha(vc.ALPHA_BUOYANCY)

def vp_actor_from_obj(filename):
    # load the data
    filename = str(filename)
    source = vtk.vtkOBJReader()
    source.SetFileName(filename)
    #clean the data
    con = vtk.vtkCleanPolyData()
    con.SetInputConnection(source.GetOutputPort())
    con.Update()
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(con.GetOutputPort())
    mapper.Update()
    # actor = vtk.vtkActor()
    # actor.SetMapper(mapper)
    vpa = vp.actors.Actor(mapper.GetInputAsDataSet())
    vpa.flat()
    return vpa

class ActorType(Enum):
    FORCE = 1
    VISUAL = 2
    GEOMETRY = 3
    GLOBAL = 4
    CABLE = 5
    NOT_GLOBAL = 6

class VisualOutline:
    parent_vp_actor = None
    outline_actor = None
    outline_transform = None

class VisualActor:

    def __init__(self, actors, node):
        self.actors = actors  # vtkplotter actors
        self.node = node      # Node
        self.visible = True
        self._original_colors = list()
        self._original_alpha = list()    # used by select
        self._original_opacity = list()  # overwritten by set-alpha

    def select(self):

        self._original_colors = list()
        self._original_alpha = list()

        if self.node is not None:
            print('storing ' + str(self.node.name))
        else:
            print('storing properties')

        for actor in self.actors:
            self._original_colors.append(actor.color())
            self._original_alpha.append(actor.alpha())
            actor.color(vc.COLOR_SELECT)


    def deselect(self):

        if self._original_colors:

            if self.node is not None:
                print('setting ' + str(self.node.name))
            else:
                print('setting properties')


            for actor, color, alpha in zip(self.actors, self._original_colors, self._original_alpha):
                actor.color(color)
                actor.alpha(alpha)

            self._original_colors = list()
            self._original_alpha = list()

        else:
            for a in self.actors:
                if a.actor_type == ActorType.GLOBAL:
                    a.alpha(0.4)
                else:
                    a.alpha(1)


    def make_transparent(self):

        self._original_opacity = []
        for a in self.actors:
            self._original_opacity.append(a.alpha())
            a.alpha(0.4)

    def reset_opacity(self):

        if self._original_opacity:
            for a,alp in zip(self.actors, self._original_opacity):
                a.alpha(alp)
            self._original_opacity = []
        else:
            for a in self.actors:
                if a.actor_type == ActorType.GLOBAL:
                    a.alpha(0.4)
                else:
                    a.alpha(1)

    def set_dsa(self, d,s,a):
        for act in self.actors:
            act.lighting(diffuse=vc.VISUAL_DIFFUSE, ambient=vc.VISUAL_AMBIENT, specular=vc.VISUAL_SPECULAR, enabled=True)


class Viewport:

    def __init__(self, scene, jupyter = False):
        self.scene = scene
        self.visuals = []
        self.outlines = []
        self.screen = None
        """Becomes assigned when a screen is active (or was active...)"""

        self.mouseLeftEvent = None
        self.mouseRightEvent = None

        self.Jupyter = jupyter

        # Settings
        self.show_geometry = True     # show or hide geometry objects (axis, pois, etc)
        self.show_force = True        # show or hide forces and connectors
        self.show_visual = True       # show or hide visuals
        self.show_global = False      # show or hide the environment (sea)
        self.force_do_normalize = True # Normalize force size to 1.0 for plotting
        self.force_scale = 1.6        # Scale to be applied on (normalized) force magnitude
        self.geometry_scale = 1.0          # poi radius of the pois
        self.outline_width = vc.OUTLINE_WIDTH      # line-width of the outlines (cell-like shading)
        self.cable_line_width = 3.0   # line-width used for cable elements

        self.quick_updates_only = False # Do not perform slow updates ( make animations quicker)


    def update_outlines(self):
        if self.screen is None:
            return

        if self.quick_updates_only:
            for outline in self.outlines:
                outline.outline_actor.SetVisibility(False)
            return

        # list of already existing outlines
        _outlines = [a.parent_vp_actor for a in self.outlines]

        # loop over actors, add outlines if needed
        for vp_actor in self.screen.actors:
            data = vp_actor.GetMapper().GetInputAsDataSet()
            if isinstance(data, vtk.vtkPolyData):
                # this actor can have an outline
                if vp_actor not in _outlines:
                    # create outline and add to self.outlines

                    tr = vtk.vtkTransformPolyDataFilter()

                    tr.SetInputData(data) # can we make a connection using port? (maintain the pipeline : see issue vtkplotter #48)
                                          # remark: Better to implement using shaders, but wait till VTK 9 because this will change the shader code.
                    temp = vtk.vtkTransform()
                    temp.Identity()
                    tr.SetTransform(temp)
                    tr.Update()

                    ol = vtk.vtkPolyDataSilhouette()
                    ol.SetInputConnection(tr.GetOutputPort())
                    ol.SetEnableFeatureAngle(True)
                    ol.SetCamera(self.screen.renderer.GetActiveCamera())
                    ol.SetBorderEdges(True)

                    mapper = vtk.vtkPolyDataMapper()
                    mapper.SetInputConnection(ol.GetOutputPort())

                    actor = vtk.vtkActor()
                    actor.SetMapper(mapper)
                    actor.GetProperty().SetColor(0, 0, 0)
                    actor.GetProperty().SetLineWidth(self.outline_width)

                    self.screen.renderer.AddActor(actor)  # vtk actor

                    # store
                    record = VisualOutline()
                    record.outline_actor = actor
                    record.outline_transform = tr
                    record.parent_vp_actor = vp_actor
                    self.outlines.append(record)

        # Update transforms for outlines
        to_be_deleted = []
        for record in self.outlines:
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

                record.outline_actor.SetVisibility(record.parent_vp_actor.GetVisibility())

            else:
                # mark for deletion
                to_be_deleted.append(record)

        # Remove obsolete outlines

        for record in to_be_deleted:
            # remove actor
            self.screen.renderer.RemoveActor(record.outline_actor)
            self.outlines.remove(record)



    def create_world_actors(self):

        world_actors = []

        plane = vp.Plane(pos=(0,0,0), normal=(0,0,1), sx=1000, sy=1000).c(vc.COLOR_WATER)
        plane.texture('blue') # vc.TEXTURE_SEA)
        plane.lighting(ambient=1.0, diffuse=0.0, specular=0.0)
        plane.alpha(0.4)

        world_actors.append(plane)
        world_actors[0].actor_type = ActorType.GLOBAL

        if self.show_global:
            world_actors[0].on()
        else:
            world_actors[0].off()

        v = VisualActor(world_actors, None)
        self.visuals.append(v)

    def deselect_all(self):
        for v in self.visuals:
            v.deselect()



    # def set_alpha(self, alpha_nodes, alpha_visuals):
    #     """Sets the alpha (transparency) of element-type nodes and visual-type nodes to the given values"""
    #
    #     for V in self.visuals:
    #         if isinstance(V.node, vf.Visual):
    #             a = alpha_visuals
    #         else:
    #             a = alpha_nodes
    #
    #         for A in V.actors:
    #             A.alpha(a)


    def level_camera(self):
        self.vtkWidget.GetRenderWindow().GetRenderers().GetFirstRenderer().GetActiveCamera().SetViewUp([0, 0, 1])
        self.refresh_embeded_view()


    def toggle_2D(self):
        camera = self.renderer.GetActiveCamera()
        if camera.GetParallelProjection():
            camera.ParallelProjectionOff()
        else:
            camera.ParallelProjectionOn()


    def _scaled_force_vector(self, vector):

        r = np.array(vector)
        len = np.linalg.norm(r)
        if len == 0:
            return r
        if self.force_do_normalize:
            r *= (1000/len)
        r *= (self.force_scale / 1000)
        return r



    def create_visuals(self, recreate = False):
        """Visuals are created in their parent axis system

        Attributes:
            recreate : re-create already exisiting visuals
        """

        for N in self.scene.nodes:

            if not recreate:
                try:            # if we already have a visual, then no need to create another one
                    N.visual
                    if N.visual is not None:
                        continue
                except:
                    pass

            actors = []

            if isinstance(N, vf.Buoyancy):

                # 0 : source-mesh
                # 1 : cob
                # 2 : water-plane
                # 3 : sumberged mesh

                # This is the source-mesh. Connect it to the parent
                vis = actor_from_trimesh(N.trimesh._TriMesh)

                if vc.COLOR_BUOYANCY_MESH_FILL is None:
                    vis = vp.Cube(side=0.00001)
                else:
                    vis.c(vc.COLOR_BUOYANCY_MESH_FILL)

                vis.actor_type = ActorType.FORCE

                if vc.COLOR_BUOYANCY_MESH_FILL is None:
                    vis.wireframe()

                if vis is not None:
                    actors.append(vis)

                # cob
                c = vp.Sphere(r=0.5, res = vc.RESOLUTION_SPHERE).c(vc.COLOR_WATER)
                c.actor_type = ActorType.FORCE
                actors.append(c)

                # waterplane
                exts = N.trimesh.get_extends()

                cx = 0.5 * (exts[0] + exts[1])
                dx = exts[1] - exts[0]
                cy = 0.5 * (exts[3] + exts[2])
                dy = exts[3] - exts[2]

                p = vp.Plane(pos = (cx,cy,0), normal = (0,0,1), sx = dx*1.1, sy = dy*1.1).c(vc.COLOR_WATER)
                p.actor_type = ActorType.NOT_GLOBAL
                actors.append(p)


            if isinstance(N, vf.Visual):
                file = self.scene.get_resource_path(N.path)
                # visual = vp.vtkio.load(file)
                visual = vp_actor_from_obj(file)
                visual.color(vc.COLOR_VISUAL)
                visual.loaded_obj = file
                visual.actor_type = ActorType.VISUAL
                actors.append(visual)


            if isinstance(N, vf.Axis):
                size = 1
                ar = vp.Arrow((0,0,0),(size,0,0), res=vc.RESOLUTION_ARROW).c(vc.COLOR_X)
                ag = vp.Arrow((0, 0, 0), (0, size, 0), res=vc.RESOLUTION_ARROW).c(vc.COLOR_Y)
                ab = vp.Arrow((0, 0, 0), (0, 0, size), res=vc.RESOLUTION_ARROW).c(vc.COLOR_Z)

                ar.actor_type = ActorType.GEOMETRY
                ag.actor_type = ActorType.GEOMETRY
                ab.actor_type = ActorType.GEOMETRY

                actors.append(ar)
                actors.append(ag)
                actors.append(ab)

            if isinstance(N, vf.RigidBody):
                size = 1
                # box = vp.Box(pos=(0,0,0), length=size, width=size, height= size).c(vc.COLOR_COG)

                box = vp_actor_from_obj(self.scene.get_resource_path('cog.obj'))
                box.color(vc.COLOR_COG)

                box.actor_type = ActorType.FORCE
                actors.append(box)

            if isinstance(N, vf.Poi):
                size = 1
                p = vp.Sphere(pos=(0,0,0), r=size/2, res = vc.RESOLUTION_SPHERE)
                p.c(vc.COLOR_POI)
                p.actor_type = ActorType.GEOMETRY
                actors.append(p)

            if isinstance(N, vf.Force):

                endpoint = self._scaled_force_vector(N.force)
                p = vp.Arrow(startPoint=(0,0,0), endPoint=endpoint, res=vc.RESOLUTION_ARROW)
                p.c(vc.COLOR_FORCE)
                p.actor_type = ActorType.FORCE
                p._force = endpoint

                actors.append(p)

                endpoint = self._scaled_force_vector(N.moment)
                p = vp.Arrow(startPoint=(0, 0, 0), endPoint=endpoint, res=vc.RESOLUTION_ARROW)
                p.actor_type = ActorType.FORCE
                p._moment = endpoint
                p.c(vc.COLOR_FORCE)
                actors.append(p)

                p = vp.Arrow(startPoint = 0.2 * endpoint, endPoint= 1.2 * endpoint, res=vc.RESOLUTION_ARROW)
                p.actor_type = ActorType.FORCE
                p.c(vc.COLOR_FORCE)
                actors.append(p)

            if isinstance(N, vf.Cable):

                # points = list()
                # for p in N._pois:
                #     points.append(p.global_position)
                # if N._vfNode.global_points:
                #     a = vp.Line(N._vfNode.global_points, lw=3).c(vc.COLOR_CABLE)
                # else:
                a = vp.Line([(0,0,0),(0,0,10),(-5,0,0)], lw=3).c(vc.COLOR_CABLE)

                a.actor_type = ActorType.CABLE
                actors.append(a)

            if isinstance(N, vf.LinearBeam):

                points = list()

                for i in range(4):
                    points.append((0,0,0))

                a = vp.Line(points, lw=5).c(vc.COLOR_VISUAL)
                a.actor_type = ActorType.CABLE

                actors.append(a)

            if isinstance(N, vf.Connector2d):

                points = list()

                for i in range(2):
                    points.append((0,0,0))

                a = vp.Line(points, lw=5).c(vc.COLOR_FORCE)
                a.actor_type = ActorType.CABLE

                actors.append(a)

            if isinstance(N, vf.LC6d):

                points = list()

                for i in range(2):
                    points.append((0,0,0))

                a = vp.Line(points, lw=5).c(vc.COLOR_FORCE)
                a.actor_type = ActorType.CABLE

                actors.append(a)



            va = VisualActor(actors, N)
            N.visual = va
            self.visuals.append(va)

            self.set_default_dsa()

    def position_visuals(self):
        """All visuals are aligned with their node"""

        to_be_removed = []
        to_be_removed_actors = []

        for V in self.visuals:

            # check if the node still exists
            # if not, then remove the visual

            node = V.node
            if node not in self.scene.nodes:
                if len(V.actors) > 0:  # not all nodes have an actor
                    if V.actors[0].actor_type != ActorType.GLOBAL:  # global visuals do not have a corresponding node
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

            if isinstance(V.node, vf.Visual):
                A = V.actors[0]

                # get the local (user set) transform
                t = vtk.vtkTransform()
                t.Identity()
                t.Translate(V.node.offset)
                t.Scale(V.node.scale)

                # # scale offset
                # scaled_offset = [V.node.offset[i] / V.node.scale[i] for i in range(3)]


                # calculate wxys from node.rotation
                r= V.node.rotation
                angle = (r[0]**2 + r[1]**2 + r[2]**2)**(0.5)
                if angle > 0:
                    t.RotateWXYZ(angle, r[0]/angle, r[1]/angle, r[2]/angle)

                # elm_matrix = t.GetMatrix()

                # Get the parent matrix (if any)
                if V.node.parent is not None:
                    tr = V.node.parent.global_transform

                    mat4x4 = vtk.vtkMatrix4x4()
                    for i in range(4):
                        for j in range(4):
                            mat4x4.SetElement(i, j, tr[j * 4 + i])

                    t.PostMultiply()
                    t.Concatenate(mat4x4)

                A.setTransform(t.GetMatrix())
                continue



            if isinstance(V.node, vf.Cable):

                # # check the number of points
                A = V.actors[0]

                # points = list()
                # for p in V.node._pois:
                #     points.append(p.global_position)

                points = V.node._vfNode.global_points
                
                if len(points)==0:  # not yet created
                    continue

                n_points = A.NPoints()
                A.setPoints(points)   # points can be set without allocation

                if n_points != len(points): # equal number of points
                    # different number of points in line
                    # (re-create the poly-line)
                    lines = vtk.vtkCellArray()  # Create the polyline.
                    lines.InsertNextCell(len(points))
                    for i in range(len(points)):
                        # print('inserting point {} {} {}'.format(*i))
                        lines.InsertCellPoint(i)
                    A.poly.SetLines(lines)

                continue

            if isinstance(V.node, vf.LinearBeam):

                # Each beam is visualized using FOUR points being
                # 0. Endpoint A
                # 1. local position (0.1*L,0,0) on endpoint A
                # 2. local position (-0.1*L,0,0) on endpoint B
                # 3. Endpoint B

                A = V.actors[0]

                points = list()
                points.append(node.master.to_glob_position((0,0,0)))
                points.append(node.master.to_glob_position((0.1*node.L, 0, 0)))
                points.append(node.slave.to_glob_position((-0.1 * node.L, 0, 0)))
                points.append(node.slave.to_glob_position((0, 0, 0)))


                A.setPoints(points)

                # work-around
                # (re-create the poly-line)
                # if n_points != len(points):

                n_points = A.NPoints()

                lines = vtk.vtkCellArray()  # Create the polyline.
                lines.InsertNextCell(n_points)
                for i in range(len(points)):
                    lines.InsertCellPoint(i)
                A.poly.SetLines(lines)

                continue

            if isinstance(V.node, vf.Connector2d):
                A = V.actors[0]

                points = list()
                points.append(node.master.to_glob_position((0,0,0)))
                points.append(node.slave.to_glob_position((0, 0, 0)))

                A.setPoints(points)

                # work-around
                # (re-create the poly-line)
                # if n_points != len(points):

                n_points = A.NPoints()

                lines = vtk.vtkCellArray()  # Create the polyline.
                lines.InsertNextCell(n_points)
                for i in range(len(points)):
                    lines.InsertCellPoint(i)
                A.poly.SetLines(lines)

                continue

            if isinstance(V.node, vf.LC6d):
                A = V.actors[0]

                points = list()
                points.append(node.master.to_glob_position((0,0,0)))
                points.append(node.slave.to_glob_position((0, 0, 0)))

                A.setPoints(points)

                # work-around
                # (re-create the poly-line)
                # if n_points != len(points):

                n_points = A.NPoints()

                lines = vtk.vtkCellArray()  # Create the polyline.
                lines.InsertNextCell(n_points)
                for i in range(len(points)):
                    lines.InsertCellPoint(i)
                A.poly.SetLines(lines)

                continue


            if isinstance(V.node, vf.Poi):
                t = V.actors[0].getTransform()
                t.Identity()
                t.Translate(V.node.global_position)
                V.actors[0].setTransform(t)

                V.actors[0].SetScale(self.geometry_scale)

                continue


            if isinstance(V.node, vf.Force):

                # check is the arrows are still what they should be
                if not np.all(V.actors[0]._force == self._scaled_force_vector(V.node.force)):

                    self.screen.remove(V.actors[0])

                    endpoint = self._scaled_force_vector(V.node.force)


                    p = vp.Arrow(startPoint=(0, 0, 0), endPoint=endpoint, res=vc.RESOLUTION_ARROW)
                    p.actor_type = ActorType.FORCE
                    p._force = endpoint
                    p.c(vc.COLOR_FORCE)

                    V.actors[0] = p
                    self.screen.add(V.actors[0])

                # check is the arrows are still what they should be
                if not np.all(np.array(V.actors[1]._moment) == self._scaled_force_vector(V.node.moment)):
                    self.screen.remove(V.actors[1])
                    self.screen.remove(V.actors[2])

                    endpoint = self._scaled_force_vector(V.node.moment)
                    p = vp.Arrow(startPoint=(0, 0, 0), endPoint=endpoint, res=vc.RESOLUTION_ARROW)
                    p.actor_type = ActorType.FORCE
                    p._moment = endpoint
                    p.c(vc.COLOR_FORCE)
                    V.actors[1] = p

                    p = vp.Arrow(startPoint=0.2 * endpoint, endPoint=1.2 * endpoint, res=vc.RESOLUTION_ARROW)
                    p.actor_type = ActorType.FORCE
                    p.c(vc.COLOR_FORCE)
                    V.actors[2] = p
                    self.screen.add(V.actors[1])
                    self.screen.add(V.actors[2])

                t = V.actors[0].getTransform()
                t.Identity()
                t.Translate(V.node.parent.global_position)
                for a in V.actors:
                    a.setTransform(t)

                continue

            if isinstance(V.node, vf.RigidBody):

                # Some custom code to place and scale the Actor[3] of the body.
                # This actor should be placed at the CoG position and scaled to a solid steel block

                t = vtk.vtkTransform()
                t.Identity()

                scale = V.node.mass / 8050  # density of steel

                if scale < 0.8:
                    scale = 0.8

                t.Translate(V.node.cog)
                mat4x4 = transform_to_mat4x4(V.node.global_transform)

                for A in V.actors:
                    A.setTransform(mat4x4)

                t.PostMultiply()
                t.Concatenate(mat4x4)

                V.actors[3].SetScale(scale)
                V.actors[3].setTransform(t)

                # scale the arrows
                V.actors[0].SetScale(self.geometry_scale)
                V.actors[1].SetScale(self.geometry_scale)
                V.actors[2].SetScale(self.geometry_scale)

                continue

            if isinstance(V.node, vf.Buoyancy):

                # move the full mesh with the parent
                mat4x4 = transform_to_mat4x4(V.node.parent.global_transform)
                current_transform = V.actors[0].getTransform().GetMatrix()

                # if the current transform is identical to the new one,
                # then we do not need to change anything (creating the mesh is slow)

                changed = False
                for i in range(4):
                    for j in range(4):
                        if current_transform.GetElement(i,j) != mat4x4.GetElement(i,j):
                            changed = True

                if not changed:
                    continue

                V.actors[0].setTransform(mat4x4)
                V.actors[0].alpha(vc.ALPHA_BUOYANCY)

                if vc.COLOR_BUOYANCY_MESH_FILL is None:
                    V.actors[0].c(vc.COLOR_BUOYANCY_MESH_LINES)
                    V.actors[0].wireframe()

                if self.quick_updates_only:
                    continue

                # move the CoB to the new (global!) position
                cob = V.node.cob
                V.actors[1].setTransform(transform_from_point(*cob))
                if V.node.displacement == 0:
                    V.actors[1].off()
                else:
                    V.actors[1].on()

                # update water-plane
                x1,x2,y1,y2,_,_ = V.node.trimesh.get_extends()
                x1 -= vc.VISUAL_BUOYANCY_PLANE_EXTEND
                x2 += vc.VISUAL_BUOYANCY_PLANE_EXTEND
                y1 -= vc.VISUAL_BUOYANCY_PLANE_EXTEND
                y2 += vc.VISUAL_BUOYANCY_PLANE_EXTEND
                p1 = V.node.parent.to_glob_position((x1,y1,0))
                p2 = V.node.parent.to_glob_position((x2, y1, 0))
                p3 = V.node.parent.to_glob_position((x2, y2, 0))
                p4 = V.node.parent.to_glob_position((x1, y2, 0))

                V.actors[2].setPoint(0,(p1[0],p1[1], 0))
                V.actors[2].setPoint(1,(p2[0],p2[1], 0))
                V.actors[2].setPoint(2,(p4[0],p4[1], 0))
                V.actors[2].setPoint(3,(p3[0],p3[1], 0))

                # create the actual buoyancy mesh as a new actor

                if len(V.actors) > 3:
                    if self.screen is not None:
                        self.screen.remove(V.actors[3])
                        V.actors.remove(V.actors[3])

                mesh = V.node._vfNode.current_mesh

                if mesh.nVertices > 0:  # only add when available

                    vertices = []
                    for i in range(mesh.nVertices):
                        vertices.append(mesh.GetVertex(i))

                    faces = []
                    for i in range(mesh.nFaces):
                        faces.append(mesh.GetFace(i))

                    # vis = vp.actors.Actor([vertices, faces], wire=True).c((0, 0, 1))
                    vis = vp.actors.Actor([vertices, faces]).c(vc.COLOR_BUOYANCY_MESH_LINES)
                    vis.actor_type = ActorType.FORCE
                    vis.wireframe()
                    vis.lw(vc.LINEWIDTH_SUBMERGED_MESH)
                    V.actors.append(vis)
                    if self.screen is not None:
                        self.screen.add(vis)

                continue

            if isinstance(V.node, vf.Axis):
                tr = transform_to_mat4x4(V.node.global_transform)
                for a in V.actors:
                    a.SetScale(self.geometry_scale)
                    a.setTransform(tr)

                continue

            # --- default ---

            try:
                tr = V.node.global_transform
            except AttributeError:
                try:
                    tr = V.node.parent.global_transform
                except AttributeError:
                    continue

            mat4x4 = transform_to_mat4x4(tr)

            for A in V.actors:
                A.setTransform(mat4x4)


        for V in to_be_removed:
            self.visuals.remove(V)
            self.screen.remove(V.actors)



        self.update_outlines()

    def add_new_actors_to_screen(self):
        """Updates the screen with added actors"""

        to_be_added = []

        if self.screen:

            actors = self.screen.getActors()
            for va in self.visuals:
                for a in va.actors:
                    if not (a in actors):
                        to_be_added.append(a)
                        # self.screen.add(a)   # do not add directly to avoid frequent updates
                        #print('adding actor for {}'.format(va.node.name))
            self.screen.add(to_be_added)

            # check if objs need to be re-loaded
            for va in self.visuals:
                if isinstance(va.node, vf.Visual):

                    try:
                        file = self.scene.get_resource_path(va.node.path)
                    except FileExistsError:
                        continue

                    if file == va.actors[0].loaded_obj:
                        continue

                    self.screen.clear(va.actors[0])

                    # update the obj
                    va.actors[0] = vp_actor_from_obj(file)
                    va.actors[0].loaded_obj = file
                    va.actors[0].color(vc.COLOR_VISUAL)
                    va.actors[0].actor_type = ActorType.VISUAL

                    self.screen.add(va.actors[0])

                if isinstance(va.node, vf.Buoyancy):
                    if va.node.trimesh._new_mesh:

                        new_mesh = actor_from_trimesh(va.node.trimesh._TriMesh)
                        if new_mesh is not None:
                            self.screen.clear(va.actors[0])
                            va.actors[0] = new_mesh
                            va.actors[0].actor_type = ActorType.FORCE
                            self.screen.add(va.actors[0])
                            va.node.trimesh._new_mesh = False


            self.set_default_dsa()



    def shutdown_qt(self):
        """Stops the renderer such that the application can close without issues"""

        if self.vtkWidget:
            ren = self.vtkWidget.GetRenderWindow()
            iren = ren.GetInteractor()
            ren.Finalize()
            iren.TerminateApp()


    def screenshot(self, w=800, h=600,camera_pos=(50,-25,10), lookat = (0,0,0)):
        vp.settings.lightFollowsCamera = True

        _notebook = vp.settings.notebookBackend
        vp.settings.notebookBackend = False
        vp.settings.screeshotScale = 2

        self.create_world_actors()

        camera = dict()
        camera['viewup'] = [0, 0, 1]
        camera['pos'] = camera_pos
        camera['focalPoint'] = lookat



        offscreen = vp.Plotter(axes=0, offscreen=True, size=(h,w))

        for va in self.visuals:
            for a in va.actors:
                if a.GetVisibility():
                    offscreen.add(a)

        offscreen.show(camera=camera)

        for r in offscreen.renderers:
            r.SetBackground(1,1,1)
            r.UseFXAAOn()

        self.update_outlines()

        filename = str(vc.PATH_TEMP_SCREENSHOT)

        vp.screenshot(filename)

        vp.settings.notebookBackend = _notebook

        from IPython.display import Image, display
        display(Image(filename))

        # import matplotlib.pyplot as plt
        # plt.figure(figsize=(w/300,h/300), dpi=300)
        # plt.imshow(plt.imread(filename))
        #
        # plt.axis(False)
        # plt.show()

    def show(self, qtWidget = None):

        vp.settings.lightFollowsCamera = True

        self.create_world_actors()

        camera = dict()
        camera['viewup'] = [0, 0, 1]
        camera['pos'] = [10, -10, 5]
        camera['focalPoint'] = [0, 0, 0]

        if self.Jupyter:
            vp.settings.embedWindow()
            screen = vp.Plotter(axes = 4, bg=vc.COLOR_BG1, bg2=vc.COLOR_BG2)

            # screen.add(self.create_world_actors())
            # self.create_world_actors()

            for va in self.visuals:
                for a in va.actors:
                    if a.GetVisibility():
                        screen.add(a)

            self.screen = screen
            return screen.show(camera=camera)

        else:

            if qtWidget is None:
                screen = vp.plotter.Plotter(interactive=True, offscreen=False,
                    axes=4, bg=vc.COLOR_BG1, bg2=vc.COLOR_BG2)
            else:
                screen = vp.plotter.Plotter(qtWidget=qtWidget,
                                            axes=4, bg=vc.COLOR_BG1, bg2=vc.COLOR_BG2)

            for va in self.visuals:
                for a in va.actors:
                    screen.add(a)

        screen.show(camera=camera, verbose = False)

        self.screen = screen

        for r in screen.renderers:
            r.ResetCamera()

        self.update_outlines()

        return screen

    def onMouseLeft(self, info):
        if self.mouseLeftEvent is not None:
            self.mouseLeftEvent(info)

    def zoom_all(self):
        for r in self.screen.renderers:
            r.ResetCamera()



    def onMouseRight(self, info):
        if self.mouseRightEvent is not None:
            self.mouseRightEvent(info)

    def make_lighter(self):
        """Increase light intensity for embedded mode"""
        C = self.light.GetIntensity()
        C += 0.05
        self.light.SetIntensity(C)
        print('Light intensity = {}'.format(C))
        self.refresh_embeded_view()

    def make_darker(self):
        """Decrease light intensity for embedded mode"""
        C = self.light.GetIntensity()
        C -= 0.05
        if C <= 0:
            C = 0
        self.light.SetIntensity(C)
        print('Light intensity = {}'.format(C))
        self.refresh_embeded_view()

    def show_embedded(self, target_frame):
        """target frame : QFrame """

        from PySide2.QtWidgets import QVBoxLayout
        from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

        # add a widget to gui
        vl = QVBoxLayout()
        self.target_frame = target_frame
        self.vtkWidget = QVTKRenderWindowInteractor(target_frame)

        vl.addWidget(self.vtkWidget)
        target_frame.setLayout(vl)

        screen = self.show(qtWidget=self.vtkWidget)

        self.renwin = self.vtkWidget.GetRenderWindow()
        self.renderer = screen.renderers[0]

        self.renwin.AddRenderer(self.renderer)

        # for r in screen.renderers:
        #     self.renwin.AddRenderer(r)

        iren = self.renwin.GetInteractor()
        iren.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())

        iren.AddObserver("LeftButtonPressEvent", screen._mouseleft)
        iren.AddObserver("RightButtonPressEvent", screen._mouseright)
        iren.AddObserver("MiddleButtonPressEvent", screen._mousemiddle)

        for r in screen.renderers:
            r.ResetCamera()

        iren.Start()

        screen.mouseLeftClickFunction = self.onMouseLeft
        screen.mouseRightClickFunction = self.onMouseRight

        # Add some lights


        light1 = vtk.vtkLight()

        light1.SetIntensity(0.3)
        light1.SetLightTypeToCameraLight()
        light1.SetPosition(100, 100, 100)

        self.renderer.AddLight(light1)

        self.light = light1


    def refresh_embeded_view(self):
        self.vtkWidget.update()

    def update_visibility(self):
        """Updates the visibility settings for all of the actors

        A visual can be hidden completely by setting visible to false
        An actor can be hidden depending on the actor-type using

        self.show_geometry = True
        self.show_force = True
        self.show_visual = True
        self.show_global = False

        """

        for v in self.visuals:
            for i,a in enumerate(v.actors):

                try:
                    a.actor_type
                except:
                    raise AttributeError('Missing actor_type for actor nr {} on node {}'.format(i, v.node.name))

                if a.actor_type == ActorType.FORCE:
                    if self.show_force:
                        a.on()
                    else:
                        a.off()

                elif a.actor_type == ActorType.VISUAL:
                    if self.show_visual:
                        a.on()
                    else:
                        a.off()

                elif a.actor_type == ActorType.GEOMETRY:
                    if self.show_geometry:
                        a.on()
                    else:
                        a.off()

                elif a.actor_type == ActorType.GLOBAL:
                    if self.show_global:
                        a.on()
                    else:
                        a.off()

                elif a.actor_type == ActorType.NOT_GLOBAL:
                    if self.show_global:
                        a.off()
                    else:
                        a.on()



                # Cables are a separate class

                elif a.actor_type == ActorType.CABLE:
                    if self.show_visual or self.show_force:
                        a.on()
                    else:
                        a.off()

        self.update_outlines()


    def set_dsa(self, d,s,a):
        for v in self.visuals:
            v.set_dsa(d,s,a)

    def set_default_dsa(self):
        self.set_dsa(vc.VISUAL_DIFFUSE, vc.VISUAL_SPECULAR, vc.VISUAL_AMBIENT)










