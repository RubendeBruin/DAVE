
"""
    Using this module a scene can be exported to Blender.

    Blender is the free and open source 3D creation suite. It supports the entirety of the 3D pipeline—modeling, rigging, animation, simulation, rendering, compositing and motion tracking, video editing and 2D animation pipeline.
    It can be downloaded from https://www.blender.org

    Only visuals will be exported.

    For this to work every visual needs to have a corresponding .blend file. This file should be located in one of the resource-paths.
    The name of the .blend file should be the same as the name of the .obj file.

    The blender model
    - should have the same origin as the .obj file
    - should have all transformations applied (select object, control+A, all transformation)

    A base blender file needs to be provided. The visuals will be added to this model. It will then be saved under a different name.

    Requirements for the base blender file:
    - Shall have a material called "Cable", this material will be assigned to each created cable.

    All functions in this file one or more of the following arguments

    - camera : a dictionary with ['position'] and ['direction'] which specifies the camera position and look direction
    - python_file : location for the generated python file
    - blender_base_file : .blend file to be used a starting scene
    - blender_result_file : .blend file to write to
    - blender_exe_path : location of the blender executable. Defaults to DAVE.constants.BLENDER_EXEC
                       : probably r"C:\Program Files\Blender Foundation\Blender\\blender.exe"

    ---






"""

"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Ruben de Bruin - 2019
"""


import DAVE.scene as dc
import DAVE.settings as consts
from scipy.spatial.transform import Rotation  # for conversion from axis-angle to euler
from os.path import splitext, basename
# from os import system
from numpy import deg2rad
from pathlib import Path
import numpy as np

import subprocess

import vtk


# utility functions for our python scripts are hard-coded here

BFUNC = """

from mathutils import Vector, Quaternion
import numpy as np

# These functions are inserted by DAVE.io.blender.py

def get_context_area():
    areas = [area for area in bpy.context.window.screen.areas if area.type == 'VIEW_3D']
    if not areas:
        raise ('No suitable context found to execute rotation transform in')
    return areas[0]

def insert_objects(filepath,scale=(1,1,1),rotation=(0,0,0), offset=(0,0,0), orientation=(0,0,0,0), position=(0,0,0), orientations=[], positions=[], frames_per_dof = 1 ):
    \"\"\"
    All meshes shall be joined

    First rotate (rotation)
    Then scale (scale)
    Then move (offset)

    Then global apply rotation rotate (orientation)
    Then apply global move (position)

    rotations in radians

    \"\"\"
    print('Loading {}'.format(filepath))


    objects = []
    if filepath.endswith('.blend'):
        with bpy.data.libraries.load(filepath=filepath, relative=False) as (data_from, data_to):
            data_to.objects.extend(data_from.objects)

        for object in data_to.objects:

            if object.type == 'MESH':  # only add meshes, materials are automatically included
                bpy.ops.object.add_named(name=object.name)
                # When you use bpy.ops.object.add() the newly created object becomes the active object
                # bpy.context.active_object
                objects.append(bpy.context.view_layer.objects.active)


    elif filepath.endswith('.obj'):
        obj = bpy.ops.import_scene.obj(filepath=filepath)
        objects = []
        for obj in bpy.context.selected_objects:
            obj.rotation_euler[0] = 0
            objects.append(obj)


    elif filepath.endwith('.stl'):
        print('STL not yet implemented')

    view3d_area = get_context_area()

    for object in objects:
        print(object.name)

        # bpy.ops.object.add_named(name=object.name)
        # When you use bpy.ops.object.add() the newly created object becomes the active object
        # bpy.context.active_object
        #active_object = bpy.context.view_layer.objects.active

        # Select only object

        bpy.ops.object.select_all(action='DESELECT')
        object.select_set(True)
        active_object = object

        # apply local transform
        #
        # Rotation is applied on the original object
        # Scale is applied on the rotated object
        # Offset is applied on the rotated and scaled object
        # 

        context_override = {'active_object': object, 'area':view3d_area}

        bpy.ops.transform.rotate(context_override,value=rotation[0], orient_axis='Z') # blender rotates in opposite direction (2.80)... (2.83 this seems to be fixed)?
        bpy.ops.transform.rotate(context_override,value=rotation[1], orient_axis='Y')
        bpy.ops.transform.rotate(context_override,value=rotation[2], orient_axis='X')

        bpy.ops.object.transform_apply(context_override,location=False, rotation=True, scale=False)    

        bpy.ops.transform.resize(context_override,value=scale)
        bpy.ops.object.transform_apply(context_override,location=False, rotation=False, scale=True)

        bpy.ops.transform.translate(context_override,value=offset)  # translate
        bpy.ops.object.transform_apply(context_override,location=True, rotation=False, scale=False)    

        # apply global transforms

        active_object.location = position
        active_object.rotation_mode = 'QUATERNION'
        active_object.rotation_quaternion = (orientation[3], orientation[0], orientation[1],orientation[2])

        n_frame = 1
        for pos, orient in zip(positions, orientations):
            bpy.context.scene.frame_set(n_frame * frames_per_dof)
            n_frame += 1


            active_object.rotation_quaternion = (orient[3], orient[0], orient[1],orient[2])
            active_object.keyframe_insert(data_path="rotation_quaternion", index = -1)

            active_object.location = Vector(pos)
            active_object.keyframe_insert(data_path="location",index = -1)


        bpy.context.scene.frame_end = (n_frame-1) * frames_per_dof





def add_line(points, diameter, name=None, ani_points = None, frames_per_entry=1):
    # Points should contain FOUR coordinates per point, the 4th one can be 1.0

    curve = bpy.data.curves.new("Curve", type='CURVE')
    polyline = curve.splines.new(type='POLY')

    n_points = len(points)
    if n_points > 1:  # by default a poly curve has one point
        polyline.points.add(n_points - 1)

    # set the points
    pts = np.ravel(points)
    polyline.points.foreach_set('co',pts)

    # add animation
    if ani_points is not None:

        points = curve.splines.data.splines[0].points  # need to be in splines[0]
        for i_frame, cur_points in enumerate(ani_points):
            n_frame = i_frame * frames_per_entry

            # set the data
            pts = np.ravel(cur_points)
            points.foreach_set("co", pts)

            # add the key-frames
            for point in points:
                point.keyframe_insert(data_path="co", frame = n_frame)


    # Create the object
    if name is None:
        name = "Line"
    curveObj = bpy.data.objects.new(name, curve)
    curveObj.data.dimensions = '3D'

    # attach to scene
    bpy.context.scene.collection.objects.link(curveObj)

    # add material
    curveObj.data.materials.append(bpy.data.materials['Cable'])
    curveObj.data.bevel_depth = diameter/2

def add_beam(points, diameter, name=None, ani_points = None, frames_per_entry=1):
    # Points should contain FOUR coordinates per point, the 4th one can be 1.0

    curve = bpy.data.curves.new("Curve", type='CURVE')
    polyline = curve.splines.new(type='POLY')

    n_points = len(points)
    if n_points > 1:  # by default a poly curve has one point
        polyline.points.add(n_points - 1)

    # set the points
    pts = np.ravel(points)
    polyline.points.foreach_set('co',pts)

    # add animation
    if ani_points is not None:

        points = curve.splines.data.splines[0].points  # need to be in splines[0]
        for i_frame, cur_points in enumerate(ani_points):
            n_frame = i_frame * frames_per_entry

            # set the data
            pts = np.ravel(cur_points)
            points.foreach_set("co", pts)

            # add the key-frames
            for point in points:
                point.keyframe_insert(data_path="co", frame = n_frame)


    # Create the object
    if name is None:
        name = "Line"
    curveObj = bpy.data.objects.new(name, curve)
    curveObj.data.dimensions = '3D'

    # attach to scene
    bpy.context.scene.collection.objects.link(curveObj)

    # add material
    curveObj.data.materials.append(bpy.data.materials['Cable'])
    curveObj.data.bevel_depth = diameter/2

# def add_beam(points, direction, diameter, name=None, ani_points=None, ani_directions=None, frames_per_entry=1):
#     # Beam is a bezier while lines are poly
#     bpy.ops.curve.primitive_bezier_curve_add(enter_editmode=True)
#     obj_data = bpy.context.active_object.data
#     obj_data.bevel_depth = diameter / 2
# 
#     n_points = len(points)
#     if n_points > 2:  # by default a curve has two points
#         obj_data.splines[0].bezier_points.add(n_points - 2)
# 
#     bpy.ops.object.mode_set(mode='OBJECT')  # back to object mode
# 
#     curve = bpy.context.active_object
#     bp = curve.data.splines[0].bezier_points
# 
#     def setpoints(pts, directions):
# 
#         L = 0.2*((pts[0][0]-pts[1][0])**2+(pts[0][1]-pts[1][1])**2+(pts[0][2]-pts[1][2])**2)**0.5
# 
#         end1 = bp[0]
#         end1.co = pts[0]
#         end1.handle_left = (pts[0][0]-L*directions[0][0], pts[0][1]-L*directions[0][1],pts[0][2]-L*directions[0][2])
#         end1.handle_right = (pts[0][0]+L*directions[0][0], pts[0][1]+L*directions[0][1],pts[0][2]+L*directions[0][2])
# 
#         end2 = bp[1]
#         end2.co = pts[1]
#         end2.handle_left = (pts[1][0]-L*directions[1][0], pts[1][1]-L*directions[1][1],pts[1][2]-L*directions[1][2])
#         end2.handle_right = (pts[1][0]+L*directions[1][0], pts[1][1]+L*directions[1][1],pts[1][2]+L*directions[1][2])
# 
#     if ani_points is not None:
#         for i_frame, (cur_points, cur_dir) in enumerate(zip(ani_points, ani_directions)):
# 
#             n_frame = i_frame * frames_per_entry
#             bpy.context.scene.frame_set(n_frame)
# 
#             setpoints(cur_points, cur_dir)
# 
#             # insert keyframes
#             for i_point in range(n_points):
#                 bp[i_point].keyframe_insert(data_path='handle_left', index=-1)
#                 bp[i_point].keyframe_insert(data_path='handle_right', index=-1)
#                 bp[i_point].keyframe_insert(data_path='co', index=-1)
# 
#     else:
#         setpoints(points, direction)
# 
#     if name is not None:
#         bpy.context.active_object.name = name
# 
#     bpy.context.active_object.data.materials.append(bpy.data.materials['Cable'])
#     bpy.ops.object.mode_set(mode='OBJECT')


"""

def _to_euler(rotation):
    r = Rotation.from_rotvec(deg2rad(rotation))
    return r.as_euler('zyx' ,degrees=False)

def _to_quaternion(rotation):
    r = Rotation.from_rotvec(deg2rad(rotation))
    return r.as_quat()


def _wavefield_to_blender(wavefield):
    """Returns blender python code to generate the wavefield in Blender

    Args:
        wavefield: DAVE.visual.wavefield object

    Returns:
        str
    """

    wavefield.update(0)

    wavefield.actor.GetMapper().Update()
    data = wavefield.actor.GetMapper().GetInputAsDataSet()

    code = '\n'
    code += '\nvertices = np.array(['

    for i in range(data.GetNumberOfPoints()):
        point = data.GetPoint(i)
        code += '\n    {}, {}, {},'.format(*point)

    code = code[:-1]  # remove the last ,

    code += """], dtype=np.float32)

num_vertices = vertices.shape[0] // 3

# Polygons are defined in loops. Here, we define one quad and two triangles
vertex_index = np.array(["""

    poly_length = []
    counter = 0
    poly_start = []

    for i in range(data.GetNumberOfCells()):
        cell = data.GetCell(i)

        if isinstance(cell, vtk.vtkLine):
            print("Cell nr {} is a line, not adding to mesh".format(i))
            continue

        code += '\n    '

        for ip in range(cell.GetNumberOfPoints()):
            code += '{},'.format(cell.GetPointId(ip))

        poly_length.append(cell.GetNumberOfPoints())
        poly_start.append(counter)
        counter += cell.GetNumberOfPoints()

    code = code[:-1]  # remove the last ,

    code += """], dtype=np.int32)

# For each polygon the start of its vertex indices in the vertex_index array
loop_start = np.array([
        """

    for p in poly_start:
        code += '{}, '.format(p)

    code = code[:-1]  # remove the last ,

    code += """], dtype=np.int32)

# Length of each polygon in number of vertices
loop_total = np.array([
        """

    for p in poly_length:
        code += '{}, '.format(p)

    code = code[:-1]  # remove the last ,

    code += """], dtype=np.int32)

num_vertex_indices = vertex_index.shape[0]
num_loops = loop_start.shape[0]

# Create mesh object based on the arrays above

mesh = bpy.data.meshes.new(name='created mesh')

mesh.vertices.add(num_vertices)
mesh.vertices.foreach_set("co", vertices)

mesh.loops.add(num_vertex_indices)
mesh.loops.foreach_set("vertex_index", vertex_index)

mesh.polygons.add(num_loops)
mesh.polygons.foreach_set("loop_start", loop_start)
mesh.polygons.foreach_set("loop_total", loop_total)

"""

    wavefield.nt  # number of key-frames

    last_frame_nr = 0

    for i_source_frame in range(wavefield.nt):
        t = wavefield.period * i_source_frame / wavefield.nt

        n_frame = consts.BLENDER_FPS * t

        if i_source_frame != wavefield.nt -1:
            if i_source_frame != 0:
                if n_frame - last_frame_nr < 5:
                    continue

        last_frame_nr = n_frame

        print('exporting wave-frame {} of {}'.format(n_frame ,wavefield.nt))

        # update wave-field
        wavefield.update(t)
        wavefield.actor.GetMapper().Update()

        filename = consts.PATH_TEMP / 'waves_frame{}.npy'.format(n_frame)
        # data = v.actor.GetMapper().GetInputAsDataSet()

        # pre-allocate data
        n_points = data.GetNumberOfPoints()
        points = np.zeros((n_points, 3))

        for i in range(n_points):
            point = data.GetPoint(i)
            points[i ,:] = point

        np.save(filename ,np.ravel(points))

        code += '\nprint("Importing wave-frame {} / {}")'.format(n_frame, wavefield.nt)

        code += '\nvertices = np.load(r"{}")'.format(str(filename))
        code += """
print("applying vertices")        
mesh.vertices.foreach_set("co", vertices)
print("creating keyframes")
for vertex in mesh.vertices:
    """
        code += 'vertex.keyframe_insert(data_path="co", frame = {})'.format(np.round(n_frame))

        # ============= END OF THE LOOP

    code += """
# We're done setting up the mesh values, update mesh object and 
# let Blender do some checks on it
mesh.update()
mesh.validate()

# Create Object whose Object Data is our new mesh
obj = bpy.data.objects.new('created object', mesh)

# Add *Object* to the scene, not the mesh
scene = bpy.context.scene
scene.collection.objects.link(obj)"""

    return code



def create_blend_and_open(scene, blender_result_file = None, blender_base_file=None, blender_exe_path=None, camera=None, animation_dofs=None, wavefield=None):

    create_blend(scene, blender_base_file, blender_result_file, blender_exe_path=blender_exe_path ,camera=camera, animation_dofs=animation_dofs, wavefield=wavefield, open_gui=True)
    # command = 'explorer "{}"'.format(str(blender_result_file))
    # subprocess.call(command, creationflags=subprocess.DETACHED_PROCESS)

def create_blend(scene, blender_base_file, blender_result_file, blender_exe_path=None, camera=None ,animation_dofs=None, wavefield=None, open_gui = False):
    tempfile = Path(consts.PATH_TEMP) / 'blender.py'

    if blender_base_file is None:
        blender_base_file = consts.BLENDER_BASE_SCENE

    if blender_result_file is None:
        blender_result_file = consts.BLENDER_DEFAULT_OUTFILE

    blender_py_file(scene, tempfile, blender_base_file = blender_base_file , blender_result_file = blender_result_file
                    ,camera=camera, animation_dofs=animation_dofs, wavefield=wavefield)

    if blender_exe_path is None:
        blender_exe_path = consts.BLENDER_EXEC

    command = '"{}" -b --python "{}"'.format(blender_exe_path, tempfile)

    print(command)

    pid = subprocess.Popen(command)
    pid.wait()

    command = 'explorer "{}"'.format(blender_result_file)
    subprocess.Popen(command)


def blender_py_file(scene, python_file, blender_base_file, blender_result_file, camera=None, animation_dofs=None,
                    wavefield=None):
    code = '# Auto-generated python file for blender\n# Execute using blender.exe -b --python "{}"\n\n'.format(
        python_file)
    code += 'import bpy\n'
    code += 'bpy.ops.wm.open_mainfile(filepath=r"{}")\n'.format(blender_base_file)
    code += '\n'
    code += BFUNC
    code += '\n# Set 3d cursor to origin'
    code += '\nbpy.context.scene.cursor.location = (0.0, 0.0, 0.0)'

    for visual in scene.nodes_of_type(dc.Visual):

        """
        A Visual node contains a 3d visual, typically obtained from a .obj file.
        A visual node can be placed on an axis-type node.

        It is used for visualization. It does not affect the forces, dynamics or statics.

            visual.offset = [0, 0, 0] :: Offset (x,y,z) of the visual. Offset is applied after scaling
            visual.rotation = :: Rotation (rx,ry,rz) of the visual
            visual.scale :: Scaling of the visual. Scaling is applied before offset.
            visual.path :: Filename of the visual

            visual.parent :: Parent : Axis-type

            parent is an axis type and has .global_position and .global_rotation
        """

        code += '\n# Exporting {}'.format(visual.name)

        # look for the file

        name, _ = splitext(basename(visual.path))

        try:
            filename = scene.get_resource_path(name + '.blend')  # raises exception if file is not found
        except:
            filename = scene.get_resource_path(visual.path)  # fall-back to .obj

        # the offset needs to be rotated.

        rot = Rotation.from_rotvec(deg2rad(visual.parent.global_rotation))
        # rotated_offset = rot.apply(visual.offset)

        if animation_dofs:
            code += '\npositions = []'
            code += '\norientations = []'
            for dof in animation_dofs:
                scene._vfc.set_dofs(dof)
                scene.update()

                code += '\norientations.append([{},{},{},{}])'.format(*_to_quaternion(visual.parent.global_rotation))

                position = visual.parent.global_position
                # global_offset = visual.parent.to_glob_direction(visual.offset)

                glob_position = np.array(position)  # + np.array(global_offset)

                code += '\npositions.append([{},{},{}])'.format(*glob_position)

            code += '\ninsert_objects(filepath=r"{}", scale=({},{},{}), rotation=({},{},{}), offset=({},{},{}), orientation=({},{},{},{}), position=({},{},{}), positions=positions, orientations=orientations)'.format(
                filename,
                *visual.scale,
                *_to_euler(visual.rotation),
                *visual.offset,
                *_to_quaternion(visual.parent.global_rotation),
                *visual.parent.global_position)


        else:
            code += '\ninsert_objects(filepath=r"{}", scale=({},{},{}), rotation=({},{},{}), offset=({},{},{}), orientation=({},{},{},{}), position=({},{},{}))'.format(
                filename,
                *visual.scale,
                *_to_euler(visual.rotation),
                *visual.offset,
                *_to_quaternion(visual.parent.global_rotation),
                *visual.parent.global_position)

    for cable in scene.nodes_of_type(dc.Cable):

        points = cable.get_points_for_visual()
        dia = cable.diameter

        if dia < consts.BLENDER_CABLE_DIA:
            dia = consts.BLENDER_CABLE_DIA

        code += '\npoints=['
        for p in points:
            code += '({},{},{},1.0),'.format(*p)
        code = code[:-1]
        code += ']'

        if animation_dofs:
            code += '\nani_points = []'
            for dof in animation_dofs:
                scene._vfc.set_dofs(dof)
                scene.update()
                points = cable.get_points_for_visual()
                code += '\nframe_points=['
                for p in points:
                    code += '({},{},{},1.0),'.format(*p)
                code = code[:-1]
                code += ']'
                code += '\nani_points.append(frame_points)'

            code += '\nadd_line(points, diameter={}, name = "{}", ani_points = ani_points)'.format(dia, cable.name)

        else:

            code += '\nadd_line(points, diameter={}, name = "{}")'.format(dia, cable.name)

    for beam in scene.nodes_of_type(dc.Beam):

        points = beam.global_positions

        dia = consts.BLENDER_BEAM_DIA

        code += '\npoints=['
        for p in points:
            code += '({},{},{},1.0),'.format(*p)
        code = code[:-1]
        code += ']'

        if animation_dofs:
            code += '\nani_points = []'
            for dof in animation_dofs:
                scene._vfc.set_dofs(dof)
                scene.update()
                points = beam.global_positions
                code += '\nframe_points=['
                for p in points:
                    code += '({},{},{},1.0),'.format(*p)
                code = code[:-1]
                code += ']'
                code += '\nani_points.append(frame_points)'

            code += '\nadd_beam(points, diameter={}, name = "{}", ani_points = ani_points)'.format(dia, beam.name)

        else:

            code += '\nadd_beam(points, diameter={}, name = "{}")'.format(dia, beam.name)

    # for beam in scene.nodes_of_type(dc.LinearBeam):
    #     pa = beam.nodeA.global_position
    #     pb = beam.nodeB.global_position
    #
    #     code += '\npoints=['
    #     code += '({},{},{}),'.format(*pa)
    #     code += '({},{},{})]'.format(*pb)
    #
    #     code += '\ndirections=['
    #     code += '({},{},{}),'.format(*beam.nodeA.ux)
    #     code += '({},{},{})]'.format(*beam.nodeB.ux)
    #
    #     dia = consts.BLENDER_BEAM_DIA
    #
    #     if animation_dofs:
    #         code += '\nani_points = []'
    #         code += '\nani_dirs = []'
    #
    #         for dof in animation_dofs:
    #             scene._vfc.set_dofs(dof)
    #             scene.update()
    #             pa = beam.nodeA.global_position
    #             pb = beam.nodeB.global_position
    #
    #             code += '\nf_points=['
    #             code += '({},{},{}),'.format(*pa)
    #             code += '({},{},{})]'.format(*pb)
    #
    #             code += '\nf_directions=['
    #             code += '({},{},{}),'.format(*beam.nodeA.ux)
    #             code += '({},{},{})]'.format(*beam.nodeB.ux)
    #
    #             code += '\nani_points.append(f_points)'
    #             code += '\nani_dirs.append(f_directions)'
    #
    #
    #
    #         code += '\nadd_beam(points, directions, diameter={}, name = "{}", ani_points = ani_points,ani_directions = ani_dirs)'.format(dia, beam.name)
    #     else:
    #         code += '\nadd_beam(points, directions, diameter={}, name = "{}")'.format(dia, beam.name)

    for contactball in scene.nodes_of_type(dc.ContactBall):
        code += '\nbpy.ops.mesh.primitive_uv_sphere_add(radius={}, enter_editmode=False, location=({}, {}, {}))'.format(
            contactball.radius, *contactball.parent.global_position)

    if camera is not None:
        pos = camera['position']
        dir = camera['direction']

        code += '\n\n# Set the active camera'
        code += '\nobj_camera = bpy.context.scene.camera'
        code += '\nobj_camera.location = ({},{},{})'.format(*pos)
        code += '\ndir = Vector(({},{},{}))\n'.format(*dir)
        code += "\nq = dir.to_track_quat('-Z','Y')\nobj_camera.rotation_euler = q.to_euler()"

    # Add the wave-plane
    if wavefield is not None:
        code += '\n# wavefield'
        code += _wavefield_to_blender(wavefield)

    code += '\nbpy.ops.wm.save_mainfile(filepath=r"{}")'.format(blender_result_file)
    # bpy.ops.wm.quit_blender() # not needed

    print(code)

    file = open(python_file, 'w+')
    file.write(code)
    file.close()
