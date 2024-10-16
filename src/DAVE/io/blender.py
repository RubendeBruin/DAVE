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
import time

from vtkmodules.vtkCommonDataModel import vtkLine

from DAVE.tools import running_in_gui

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


def try_get_blender_executable():
    import platform

    if platform.system().lower().startswith("win"):
        # on windows we can possibly get blender from the registry
        import winreg
        import os

        def find_blender_from_reg(where, key):
            try:
                pt = winreg.QueryValue(where, key)
                if pt:
                    if "%1" in pt:
                        pt = pt[1:-6]  # strip the %1

                    if os.path.exists(pt):
                        return pt
                    else:
                        pass
                        # print(f'Blender NOT found here {pt} as listed in {key}')
            except Exception as E:
                # print(f'Error when looking for blender here: {key} - {str(E)}')
                raise ValueError("Not found here")

        where_is_blender_in_the_registry = [
            (winreg.HKEY_CLASSES_ROOT, r"Applications\blender.exe\shell\open\command"),
            (
                winreg.HKEY_CLASSES_ROOT,
                r"Applications\blender-launcher.exe\shell\open\command",
            ),
            (
                winreg.HKEY_CURRENT_USER,
                r"SOFTWARE\Classes\Applications\blender-launcher.exe\shell\open\command",
            ),
            (
                winreg.HKEY_CURRENT_USER,
                r"SOFTWARE\Classes\Applications\blender-launcher.exe\shell\open\command",
            ),
            (
                winreg.HKEY_CURRENT_USER,
                r"SOFTWARE\Classes\blendfile\shell\open\command",
            ),
            (
                winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\Classes\blendfile\shell\open\command",
            ),
        ]

        for possibility in where_is_blender_in_the_registry:
            try:
                BLENDER_EXEC = find_blender_from_reg(*possibility)
                if BLENDER_EXEC:
                    print('Blender found in registry at: {}'.format(BLENDER_EXEC))
                    return BLENDER_EXEC
            except:
                pass

        # find it in a path
        # by default the windows-store version seems to be installed in a location which is in the path


        paths = os.environ["PATH"].split(";")
        for pth in paths:
            test = pth + r"\\blender-launcher.exe"
            if os.path.exists(test):
                print("Blender found (using PATH variable) at: {}".format(test))
                return test

        # Getting quite desperate Do a GLOB search for blender-launcher.exe in C:\Program Files\Blender Foundation

        import glob
        for pth in glob.glob(r"C:\Program Files\Blender Foundation\*\blender-launcher.exe"):
            if os.path.exists(pth):
                print("Blender found (using GLOB search) at: {}".format(pth))
                return pth

        # Out of options


        print(
            "! Blender not found - Blender can be installed from the microsoft windows store."
            "   if you have blender already and want to be able to use blender then please either:\n"
            "   - configure windows to open .blend files with blender automatically \n"
            "   - add the folder containing blender-launcher.exe to the PATH variable."
        )

        return "Blender can not be found automatically"

        # print('\nLoading DAVE...')
    else:  # assume we're on linux
        BLENDER_EXEC = "blender"

    return BLENDER_EXEC


# utility functions for our python scripts are hard-coded here

BFUNC = """

from mathutils import Vector, Quaternion
import numpy as np

# These functions are inserted by DAVE.io.blender.py

def change_color_of_object(object, new_rgb):
    if new_rgb is None:
        return
    
    # copy material
    if object.active_material:
        material = object.active_material.copy()
        BSDF_node = material.node_tree.nodes['Principled BSDF']
        BSDF_node.inputs['Base Color'].default_value = (new_rgb[0]/255,new_rgb[1]/255,new_rgb[2]/255,1)
        
        print(f'Changing material to color {new_rgb}')
        object.active_material = material
    

def get_context_area():
    areas = [area for area in bpy.context.window.screen.areas if area.type == 'VIEW_3D']
    if not areas:
        raise ('No suitable context found to execute rotation transform in')
    return areas[0]

def insert_objects(filepath,scale=(1,1,1),rotation=(0,0,0,0), offset=(0,0,0), orientation=(0,0,0,0), position=(0,0,0), orientations=[], positions=[], frames_per_dof = 1, color=None ):
    \"\"\"
    All meshes shall be joined

    First scale
    then rotate
    then move

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

    elif filepath.endswith('.obj') or filepath.endswith('.stl') or filepath.endswith('.glb') or filepath.endswith('.gltf'):
        if filepath.endswith('.obj'):
            obj = bpy.ops.wm.obj_import(filepath=filepath)
        elif filepath.endswith('.stl'):
            obj = bpy.ops.import_mesh.stl(filepath=filepath)
        elif filepath.endswith('.glb') or filepath.endswith('.gltf'):
            obj = bpy.ops.import_scene.gltf(filepath=filepath)
        else:
            raise ValueError(f'Unknown file format for {filepath}')

        objects = []
        for obj in bpy.context.selected_objects:
            obj.rotation_euler[0] = 0
            objects.append(obj)


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

        # context_override = {'active_object': object, 'area':view3d_area}

        # bpy.ops.transform.rotate(context_override,value=rotation[0], orient_axis='Z') # blender rotates in opposite direction (2.80)... (2.83 this seems to be fixed)?
        # bpy.ops.transform.rotate(context_override,value=rotation[1], orient_axis='Y')
        # bpy.ops.transform.rotate(context_override,value=rotation[2], orient_axis='X')
 
        # bpy.ops.transform.resize(context_override,value=scale)
        bpy.ops.transform.resize(value=scale)
        # bpy.ops.object.transform_apply(context_override,location=False, rotation=False, scale=True)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        
        active_object.rotation_mode = 'QUATERNION'
        active_object.rotation_quaternion = (rotation[3], rotation[0], rotation[1],rotation[2])

        # bpy.ops.object.transform_apply(context_override,location=False, rotation=True, scale=False)    
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)    

        # bpy.ops.transform.translate(context_override,value=offset)  # translate
        bpy.ops.transform.translate(value=offset)  # translate
        # bpy.ops.object.transform_apply(context_override,location=True, rotation=False, scale=False)    
        bpy.ops.object.transform_apply(location=True, rotation=False, scale=False)    

        # apply global transforms

        active_object.location = position
        active_object.rotation_mode = 'QUATERNION'
        active_object.rotation_quaternion = (orientation[3], orientation[0], orientation[1],orientation[2])
        
        # Set color
        change_color_of_object(active_object, color)
        

        n_frame = 0
        for pos, orient in zip(positions, orientations):
            bpy.context.scene.frame_set(n_frame * frames_per_dof)
            n_frame += 1


            active_object.rotation_quaternion = (orient[3], orient[0], orient[1],orient[2])
            active_object.keyframe_insert(data_path="rotation_quaternion", index = -1)

            active_object.location = Vector(pos)
            active_object.keyframe_insert(data_path="location",index = -1)


        bpy.context.scene.frame_end = (n_frame-1) * frames_per_dof
        # bpy.context.scene.frame_start = 0
        
        # bpy.context.area.ui_type = 'FCURVES'   # need to set context back to original afterwards
        # bpy.ops.graph.select_all(action='SELECT')
        # bpy.ops.graph.handle_type(type='VECTOR')






def add_line(points, diameter, name=None, ani_points = None, frames_per_entry=1, color=None):
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
    
    # set color (if needed)
    change_color_of_object(curveObj, color)

def add_beam(points, diameter, name=None, ani_points = None, frames_per_entry=1, color=None):
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
    
    # set color (if needed)
    change_color_of_object(curveObj, color)

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
    return r.as_euler("zyx", degrees=False)


def _to_quaternion(rotation):
    r = Rotation.from_rotvec(deg2rad(rotation))
    return r.as_quat()


def _wavefield_to_blender(wavefield, frames_per_step=1, export_only_1_in_x_frames=1):
    """Returns blender python code to generate the wavefield in Blender

    Args:
        wavefield: DAVE.visual.wavefield object

    Returns:
        str
    """

    wavefield.update(0)

    wavefield.actor.GetMapper().Update()
    data = wavefield.actor.GetMapper().GetInputAsDataSet()

    code = "\n"
    code += "\nvertices = np.array(["

    for i in range(data.GetNumberOfPoints()):
        point = data.GetPoint(i)
        code += "\n    {}, {}, {},".format(*point)

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

        if isinstance(cell, vtkLine):
            # print("Cell nr {} is a line, not adding to mesh".format(i))
            continue

        code += "\n    "

        for ip in range(cell.GetNumberOfPoints()):
            code += "{},".format(cell.GetPointId(ip))

        poly_length.append(cell.GetNumberOfPoints())
        poly_start.append(counter)
        counter += cell.GetNumberOfPoints()

    code = code[:-1]  # remove the last ,

    code += """], dtype=np.int32)

# For each polygon the start of its vertex indices in the vertex_index array
loop_start = np.array([
        """

    for p in poly_start:
        code += "{}, ".format(p)

    code = code[:-1]  # remove the last ,

    code += """], dtype=np.int32)

# Length of each polygon in number of vertices
loop_total = np.array([
        """

    for p in poly_length:
        code += "{}, ".format(p)

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

    for i_source_frame in range(wavefield.nt):
        # skip some of the frames, but not the fist or last
        if (
            i_source_frame != wavefield.nt - 1
            and i_source_frame != 0
            and i_source_frame % export_only_1_in_x_frames != 0
        ):
            continue  # skip this frame

        # print('exporting wave-frame {} of {}'.format(i_frame ,wavefield.nt))

        # update wave-field

        t = i_source_frame * wavefield.dt
        i_frame = int(t * frames_per_step)

        wavefield.update(t)
        wavefield.actor.GetMapper().Update()

        filename = consts.PATH_TEMP / "waves_frame{}.npy".format(i_frame)
        # data = v.actor.GetMapper().GetInputAsDataSet()

        # pre-allocate data
        n_points = data.GetNumberOfPoints()
        points = np.zeros((n_points, 3))

        for i in range(n_points):
            point = data.GetPoint(i)
            points[i, :] = point

        np.save(filename, np.ravel(points))

        code += '\nprint("Importing wave-frame {} / {}")'.format(i_frame, wavefield.nt)

        code += '\nvertices = np.load(r"{}")'.format(str(filename))
        code += """
print("applying vertices")        
mesh.vertices.foreach_set("co", vertices)
print("creating keyframes")
for vertex in mesh.vertices:
    """
        code += 'vertex.keyframe_insert(data_path="co", frame = {})'.format(i_frame)

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


def nearest_rotation_vector(v0, v1):
    """Rotation vectors are not unique. This function determines the rotation vector
    describing rotation v1 (in degrees) nearest to rotation vector v0 and return that
    vector
    """
    v1 = np.array(v1)

    if np.linalg.norm(v1) < 1e-6:
        if np.linalg.norm(v0) < 1e-6:
            # two zero rotations
            return (0, 0, 0)
        else:
            n = v0 / np.linalg.norm(v0)  # change-vector in v0 direction

    else:
        n = v1 / np.linalg.norm(v1)  # normal in v1

    v0_proj = np.dot(v0, n) * n

    d = np.dot(v1 - v0_proj, n)  # signed distance in direction of n

    i = round(d / 360)  # integer number of 360*n lengths that v1 is past v0_proj

    return v1 - 360 * i * n


def create_blend_and_open(
    scene,
    blender_result_file=None,
    blender_base_file=None,
    blender_exe_path=None,
    camera=None,
    animation_dofs=None,
    wavefield=None,
    frames_per_step=1,
    tempfile = None
):
    create_blend(
        scene,
        blender_base_file,
        blender_result_file,
        blender_exe_path=blender_exe_path,
        camera=camera,
        animation_dofs=animation_dofs,
        wavefield=wavefield,
        frames_per_step=frames_per_step,
        tempfile = tempfile
    )

    # check that blender has started and has opened the file
    # if not then wait for that to happen because the temporary file
    # will be deleted when the script ends

    # command = 'explorer "{}"'.format(str(blender_result_file))
    # subprocess.call(command, creationflags=subprocess.DETACHED_PROCESS)


def create_blend(
    scene,
    blender_base_file,
    blender_result_file,
    blender_exe_path=None,
    camera=None,
    animation_dofs=None,
    wavefield=None,
    frames_per_step=1,
    tempfile = None
):
    # Can not use real temp files as those may be deleted before Blender can open them
    if tempfile is None:
        tempfile = Path(consts.PATH_TEMP) / "blender.py"

    if blender_base_file is None:
        blender_base_file = consts.BLENDER_BASE_SCENE

    if blender_result_file is None:
        i = 0
        while True:
            blender_result_file = consts.PATH_TEMP / f"result{i}.blend"
            if not blender_result_file.exists():
                break
            i += 1

    blender_py_file(
        scene,
        tempfile,
        blender_base_file=blender_base_file,
        blender_result_file=blender_result_file,
        camera=camera,
        animation_dofs=animation_dofs,
        wavefield=wavefield,
        frames_per_step=frames_per_step,
    )

    if blender_exe_path is None:
        raise ValueError(
            "Path of Blender executable needs to be specified (in create_blend)"
        )

    command_run = [blender_exe_path, "-b", "--python", tempfile]
    command_open = [blender_exe_path, blender_result_file]

    assert Path(
        blender_base_file
    ).exists(), f"Blender base file {blender_base_file} not found"
    assert not Path(blender_result_file).exists(), "Blender result file already exists"

    if running_in_gui():
        command_run = [blender_exe_path, "-b", "--python", str(tempfile)]
        command_open = [blender_exe_path, str(blender_result_file)]
        command_wait = "SLEEP 5"

        from DAVE.gui.helpers.background_runner import BackgroundRunnerGui

        BackgroundRunnerGui([command_run, command_open, command_wait])

    else:
        print(f"Creating Blender file here: {tempfile}")
        print("Producing Blender file using:")
        print(command_run)
        result = subprocess.run(command_run)
        if result.returncode == 0:
            print("done, opening the file")
            assert Path(blender_result_file).exists(), "Blender file not created :-("
            subprocess.Popen(command_open)
            time.sleep(5)
        else:
            print("Blender file creation failed")
            return


def blender_py_file(
    scene,
    python_file,
    blender_base_file,
    blender_result_file,
    camera=None,
    animation_dofs=None,
    wavefield=None,
    frames_per_step=24,
):
    # If animation dofs are not provided, and the scene has a timeline with a non-zero range, then use that
    timeline = None
    if animation_dofs is None:
        t = getattr(scene, "t", None)
        if t:
            if t.range() is not None:
                timeline = t

    code = '# Auto-generated python file for blender\n# Execute using blender.exe -b --python "{}"\n\n'.format(
        python_file
    )
    code += "import bpy\n"
    code += 'bpy.ops.wm.open_mainfile(filepath=r"{}")\n'.format(blender_base_file)
    code += "\n"
    code += BFUNC
    code += "\n# Set 3d cursor to origin"
    code += "\nbpy.context.scene.cursor.location = (0.0, 0.0, 0.0)"

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

        code += "\n# Exporting {}".format(visual.name)

        # look for the file
        # try to find a .blend file

        try:
            name = visual.path.split(".")[0]
            filename = scene.get_resource_path(
                name + ".blend", error_interaction = None
            )  # raises exception if file is not found
        except:
            filename = scene.get_resource_path(visual.path)  # fall-back to .obj

        # the offset needs to be rotated.

        has_parent = visual.parent is not None

        # if has_parent is None:
        #     rot = Rotation.from_rotvec(deg2rad(visual.parent.global_rotation))
        # else:
        #     rot = (0, 0, 0)

        # rotated_offset = rot.apply(visual.offset)

        if animation_dofs and has_parent:
            code += "\npositions = []"
            code += "\norientations = []"
            for dof in animation_dofs:
                scene._vfc.set_dofs(dof)
                scene.update()

                code += "\norientations.append([{},{},{},{}])".format(
                    *_to_quaternion(visual.parent.global_rotation)
                )

                position = visual.parent.global_position
                # global_offset = visual.parent.to_glob_direction(visual.offset)

                glob_position = np.array(position)  # + np.array(global_offset)

                code += "\npositions.append([{},{},{}])".format(*glob_position)

            code += '\ninsert_objects(filepath=r"{}", scale=({},{},{}), rotation=({},{},{},{}), offset=({},{},{}), orientation=({},{},{},{}), position=({},{},{}), positions=positions, orientations=orientations, color={},frames_per_dof={})'.format(
                filename,
                *visual.scale,
                *_to_quaternion(visual.rotation),
                *visual.offset,
                *_to_quaternion(visual.parent.global_rotation),
                *visual.parent.global_position,
                visual.color,
                frames_per_step,
            )

        elif timeline and has_parent:
            code += "\npositions = []"
            code += "\norientations = []"

            time_start, time_end = timeline.range()

            past_rotvec = (0, 0, 0)

            for i_time in range(time_end - time_start + 1):
                timeline.activate_time(i_time + time_start)
                scene.update()

                # get the rotation vector nearest to the pervious one (unwinding)
                rotvec = visual.parent.global_rotation  # (degrees)

                # the rotvec can be changed in length by any multiple of 360
                # it should be as close to the past_rotvec as possible
                #
                # to the difference between the current rotation vector and the
                # previous one projected onto the current one should be <=180

                rotvec = nearest_rotation_vector(past_rotvec, rotvec)

                code += "\norientations.append([{},{},{},{}])".format(
                    *_to_quaternion(rotvec)
                )
                past_rotvec = rotvec

                position = visual.parent.global_position
                # global_offset = visual.parent.to_glob_direction(visual.offset)

                glob_position = np.array(position)  # + np.array(global_offset)

                code += "\npositions.append([{},{},{}])".format(*glob_position)

            code += '\ninsert_objects(filepath=r"{}", scale=({},{},{}), rotation=({},{},{},{}), offset=({},{},{}), orientation=({},{},{},{}), position=({},{},{}), positions=positions, orientations=orientations, color={}, frames_per_dof={})'.format(
                filename,
                *visual.scale,
                *_to_quaternion(visual.rotation),
                *visual.offset,
                *_to_quaternion(visual.parent.global_rotation),
                *visual.parent.global_position,
                visual.color,
                frames_per_step,
            )

        else:
            if has_parent:
                parent_global_position = visual.parent.global_position
                parent_global_rotation = visual.parent.global_rotation
            else:
                parent_global_position = (0, 0, 0)
                parent_global_rotation = (0, 0, 0)

            code += '\ninsert_objects(filepath=r"{}", scale=({},{},{}), rotation=({},{},{},{}), offset=({},{},{}), orientation=({},{},{},{}), position=({},{},{}), color={})'.format(
                filename,
                *visual.scale,
                *_to_quaternion(visual.rotation),
                *visual.offset,
                *_to_quaternion(parent_global_rotation),
                *parent_global_position,
                visual.color,
            )

    for cable in scene.nodes_of_type(dc.Cable):
        points = cable.get_points_for_visual_blender()
        dia = cable.diameter

        if dia < consts.BLENDER_CABLE_DIA:
            dia = consts.BLENDER_CABLE_DIA

        code += "\npoints=["
        for p in points:
            code += "({},{},{},1.0),".format(*p)
        code = code[:-1]
        code += "]"

        if animation_dofs:
            code += "\nani_points = []"
            for dof in animation_dofs:
                scene._vfc.set_dofs(dof)
                scene.update()
                points = cable.get_points_for_visual_blender()
                code += "\nframe_points=["
                for p in points:
                    code += "({},{},{},1.0),".format(*p)
                code = code[:-1]
                code += "]"
                code += "\nani_points.append(frame_points)"

            code += '\nadd_line(points, diameter={}, name = "{}", ani_points = ani_points, color = {},frames_per_entry = {})'.format(
                dia, cable.name, cable.color, frames_per_step
            )

        elif timeline:
            code += "\nani_points = []"
            time_start, time_end = timeline.range()

            for i_time in range(time_end - time_start + 1):
                timeline.activate_time(i_time + time_start)
                scene.update()
                points = cable.get_points_for_visual_blender()
                code += "\nframe_points=["
                for p in points:
                    code += "({},{},{},1.0),".format(*p)
                code = code[:-1]
                code += "]"
                code += "\nani_points.append(frame_points)"

            code += '\nadd_line(points, diameter={}, name = "{}", ani_points = ani_points, color = {}, frames_per_entry = {})'.format(
                dia, cable.name, cable.color, frames_per_step
            )

        else:
            code += '\nadd_line(points, diameter={}, name = "{}", color = {})'.format(
                dia, cable.name, cable.color
            )

    for beam in scene.nodes_of_type(dc.Beam):
        points = beam.global_positions

        dia = consts.BLENDER_BEAM_DIA

        code += "\npoints=["
        for p in points:
            code += "({},{},{},1.0),".format(*p)
        code = code[:-1]
        code += "]"

        if animation_dofs:
            code += "\nani_points = []"
            for dof in animation_dofs:
                scene._vfc.set_dofs(dof)
                scene.update()
                points = beam.global_positions
                code += "\nframe_points=["
                for p in points:
                    code += "({},{},{},1.0),".format(*p)
                code = code[:-1]
                code += "]"
                code += "\nani_points.append(frame_points)"

            code += '\nadd_beam(points, diameter={}, name = "{}", ani_points = ani_points, color = {})'.format(
                dia, beam.name, beam.color
            )

        elif timeline:
            code += "\nani_points = []"
            time_start, time_end = timeline.range()
            for i_time in range(time_end - time_start + 1):
                timeline.activate_time(i_time + time_start)
                scene.update()
                points = beam.global_positions
                code += "\nframe_points=["
                for p in points:
                    code += "({},{},{},1.0),".format(*p)
                code = code[:-1]
                code += "]"
                code += "\nani_points.append(frame_points)"

            code += '\nadd_beam(points, diameter={}, name = "{}", ani_points = ani_points, color = {}, frames_per_entry = {})'.format(
                dia, beam.name, beam.color, frames_per_step
            )

        else:
            code += '\nadd_beam(points, diameter={}, name = "{}", color = {})'.format(
                dia, beam.name, beam.color
            )

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
        code += "\nbpy.ops.mesh.primitive_uv_sphere_add(radius={}, enter_editmode=False, location=({}, {}, {}))".format(
            contactball.radius, *contactball.parent.global_position
        )

    if camera is not None:
        pos = camera["position"]
        dir = camera["direction"]

        code += "\n\n# Set the active camera"
        code += "\nobj_camera = bpy.context.scene.camera"
        code += "\nobj_camera.location = ({},{},{})".format(*pos)
        code += "\ndir = Vector(({},{},{}))\n".format(*dir)
        code += "\nq = dir.to_track_quat('-Z','Y')\nobj_camera.rotation_euler = q.to_euler()"

    # Add the wave-plane
    if wavefield is not None:
        code += "\n# wavefield"
        code += _wavefield_to_blender(wavefield, frames_per_step=frames_per_step)

    code += '\nbpy.ops.wm.save_mainfile(filepath=r"{}")'.format(blender_result_file)
    # bpy.ops.wm.quit_blender() # not needed

    print(code)

    file = open(python_file, "w+")
    file.write(code)
    file.close()


if __name__ == "__main__":
    from DAVE import *

    s = Scene()

    # auto generated python code
    # By beneden
    # Time: 2022-03-02 18:53:10 UTC

    # To be able to distinguish the important number (eg: fixed positions) from
    # non-important numbers (eg: a position that is solved by the static solver) we use a dummy-function called 'solved'.
    # For anything written as solved(number) that actual number does not influence the static solution

    def solved(number):
        return number

    # Environment settings
    s.g = 9.80665
    s.waterlevel = 0.0
    s.rho_air = 0.00126
    s.rho_water = 1.025
    s.wind_direction = 0.0
    s.wind_velocity = 0.0
    s.current_direction = 0.0
    s.current_velocity = 0.0

    # code for Frame
    s.new_frame(
        name="Frame",
        position=(0.0, 0.0, 4.0),
        rotation=(0.0, 0.0, 0.0),
        fixed=(True, True, True, True, True, True),
    )

    # code for Frame_1
    s.new_frame(
        name="Frame_1",
        parent="Frame",
        position=(15.0, 0.0, -6.0),
        rotation=(0.0, 0.0, 0.0),
        fixed=(True, True, True, True, True, True),
    )

    # code for Visual
    s.new_visual(
        name="Visual",
        parent="Frame",
        path=r"wirecube.obj",
        offset=(0, 0, 0),
        rotation=(0, 0, 0),
        scale=(1, 1, 1),
    )
    s.new_visual(
        name="Visual2",
        parent="Frame",
        path=r"wirecube.obj",
        offset=(10, 0, 0),
        rotation=(0, 0, 0),
        scale=(1, 1, 1),
    )

    # code for beam Beam
    s.new_beam(
        name="Beam",
        nodeA="Frame_1",
        nodeB="Frame",
        n_segments=6.0,
        tension_only=False,
        EIy=0.0,
        EIz=0.0,
        GIp=0.0,
        EA=1000.0,
        mass=0.7,
        L=19.0,
    )  # L can possibly be omitted

    # Limits of un-managed nodes

    # Tags

    # Colors
    s["Visual"].color = (23, 255, 23)
    s["Visual2"].color = (254, 0, 0)
    s["Beam"].color = (0, 100, 254)

    from DAVE.gui.dialog_blender import try_get_blender_executable

    blender_executable = try_get_blender_executable()

    create_blend_and_open(s, blender_exe_path=blender_executable)
