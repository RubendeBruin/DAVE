

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
from os import system
from numpy import deg2rad
from pathlib import Path
import numpy as np


# utility functions for our python scripts are hard-coded here

BFUNC = """

from mathutils import Vector, Quaternion
import numpy as np

# These functions are inserted by DAVE.io.blender.py

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
        obj = bpy.context.selected_objects[0]
        obj.rotation_euler[0] = 0
        objects = [obj]
        
    elif filepath.endwith('.stl'):
        print('STL not yet implemented')
        

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

        bpy.ops.transform.translate(value=offset)  # translate

        bpy.ops.transform.rotate(value=-rotation[0], orient_axis='Z') # blender rotates in opposite direction (2.80)
        bpy.ops.transform.rotate(value=-rotation[1], orient_axis='Y')
        bpy.ops.transform.rotate(value=-rotation[2], orient_axis='X')
        bpy.ops.transform.resize(value=scale)

        # bpy.ops.transform.translate(value=(-offset[0], -offset[1], -offset[2])) # and translate back
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        # bpy.ops.transform.translate(value=offset)  # translate    

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
    if n_points > 2:  # by default a curve has one points
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

    # attach to scene
    bpy.context.scene.collection.objects.link(curveObj)

    # add material
    curveObj.data.materials.append(bpy.data.materials['Cable'])
    curveObj.data.bevel_depth = diameter/2

def add_beam(points, direction, diameter, name=None, ani_points=None, ani_directions=None, frames_per_entry=1):
    # Beam is a bezier while lines are poly
    bpy.ops.curve.primitive_bezier_curve_add(enter_editmode=True)
    obj_data = bpy.context.active_object.data
    obj_data.bevel_depth = diameter / 2

    n_points = len(points)
    if n_points > 2:  # by default a curve has two points
        obj_data.splines[0].bezier_points.add(n_points - 2)

    bpy.ops.object.mode_set(mode='OBJECT')  # back to object mode

    curve = bpy.context.active_object
    bp = curve.data.splines[0].bezier_points

    def setpoints(pts, directions):

        L = 0.2*((pts[0][0]-pts[1][0])**2+(pts[0][1]-pts[1][1])**2+(pts[0][2]-pts[1][2])**2)**0.5

        end1 = bp[0]
        end1.co = pts[0]
        end1.handle_left = (pts[0][0]-L*directions[0][0], pts[0][1]-L*directions[0][1],pts[0][2]-L*directions[0][2])
        end1.handle_right = (pts[0][0]+L*directions[0][0], pts[0][1]+L*directions[0][1],pts[0][2]+L*directions[0][2])

        end2 = bp[1]
        end2.co = pts[1]
        end2.handle_left = (pts[1][0]-L*directions[1][0], pts[1][1]-L*directions[1][1],pts[1][2]-L*directions[1][2])
        end2.handle_right = (pts[1][0]+L*directions[1][0], pts[1][1]+L*directions[1][1],pts[1][2]+L*directions[1][2])

    if ani_points is not None:
        for i_frame, (cur_points, cur_dir) in enumerate(zip(ani_points, ani_directions)):

            n_frame = i_frame * frames_per_entry
            bpy.context.scene.frame_set(n_frame)

            setpoints(cur_points, cur_dir)

            # insert keyframes
            for i_point in range(n_points):
                bp[i_point].keyframe_insert(data_path='handle_left', index=-1)
                bp[i_point].keyframe_insert(data_path='handle_right', index=-1)
                bp[i_point].keyframe_insert(data_path='co', index=-1)

    else:
        setpoints(points, direction)

    if name is not None:
        bpy.context.active_object.name = name

    bpy.context.active_object.data.materials.append(bpy.data.materials['Cable'])
    bpy.ops.object.mode_set(mode='OBJECT')


"""


def _to_euler(rotation):
    r = Rotation.from_rotvec(deg2rad(rotation))
    return r.as_euler('zyx',degrees=False)

def _to_quaternion(rotation):
    r = Rotation.from_rotvec(deg2rad(rotation))
    return r.as_quat()


def create_blend_and_open(scene, blender_result_file = None, blender_base_file=None, blender_exe_path=None, camera=None, animation_dofs=None):

    if blender_base_file is None:
        blender_base_file = consts.BLENDER_BASE_SCENE

    if blender_result_file is None:
        blender_result_file = consts.BLENDER_DEFAULT_OUTFILE

    create_blend(scene, blender_base_file, blender_result_file, blender_exe_path=blender_exe_path,camera=camera, animation_dofs=animation_dofs)
    command = '"{}"'.format(str(blender_result_file))
    system(command)

def create_blend(scene, blender_base_file, blender_result_file, blender_exe_path=None, camera=None,animation_dofs=None):
    tempfile = Path(consts.PATH_TEMP) / 'blender.py'

    blender_py_file(scene, tempfile, blender_base_file, blender_result_file,camera=camera,animation_dofs=animation_dofs)

    if blender_exe_path is None:
        blender_exe_path = consts.BLENDER_EXEC

    command = '""{}" -b --python "{}""'.format(blender_exe_path, tempfile)
    print(command)
    system(command)

def blender_py_file(scene, python_file, blender_base_file, blender_result_file, camera = None, animation_dofs=None):

    code = '# Auto-generated python file for blender\n# Execute using blender.exe -b --python "{}"\n\n'.format(python_file)
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

        name,_ = splitext(basename(visual.path))

        try:
            filename = scene.get_resource_path(name + '.blend')  # raises exception if file is not found
        except:
            filename = scene.get_resource_path(visual.path) # fall-back to .obj

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

                glob_position = np.array(position) # + np.array(global_offset)

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


    for beam in scene.nodes_of_type(dc.LinearBeam):
        pa = beam.master.global_position
        pb = beam.slave.global_position

        code += '\npoints=['
        code += '({},{},{}),'.format(*pa)
        code += '({},{},{})]'.format(*pb)

        code += '\ndirections=['
        code += '({},{},{}),'.format(*beam.master.ux)
        code += '({},{},{})]'.format(*beam.slave.ux)

        dia = consts.BLENDER_BEAM_DIA

        if animation_dofs:
            code += '\nani_points = []'
            code += '\nani_dirs = []'

            for dof in animation_dofs:
                scene._vfc.set_dofs(dof)
                scene.update()
                pa = beam.master.global_position
                pb = beam.slave.global_position

                code += '\nf_points=['
                code += '({},{},{}),'.format(*pa)
                code += '({},{},{})]'.format(*pb)

                code += '\nf_directions=['
                code += '({},{},{}),'.format(*beam.master.ux)
                code += '({},{},{})]'.format(*beam.slave.ux)

                code += '\nani_points.append(f_points)'
                code += '\nani_dirs.append(f_directions)'



            code += '\nadd_beam(points, directions, diameter={}, name = "{}", ani_points = ani_points,ani_directions = ani_dirs)'.format(dia, beam.name)
        else:
            code += '\nadd_beam(points, directions, diameter={}, name = "{}")'.format(dia, beam.name)



    if camera is not None:
        pos = camera['position']
        dir = camera['direction']

        code += '\n\n# Set the active camera'
        code += '\nobj_camera = bpy.context.scene.camera'
        code += '\nobj_camera.location = ({},{},{})'.format(*pos)
        code += '\ndir = Vector(({},{},{}))\n'.format(*dir)
        code += "\nq = dir.to_track_quat('-Z','Y')\nobj_camera.rotation_euler = q.to_euler()"

    code += '\nbpy.ops.wm.save_mainfile(filepath=r"{}")'.format(blender_result_file)
    # bpy.ops.wm.quit_blender() # not needed

    print(code)

    file = open(python_file, 'w+')
    file.write(code)
    file.close()




