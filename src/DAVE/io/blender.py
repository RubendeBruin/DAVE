

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
import DAVE.constants as consts
from scipy.spatial.transform import Rotation  # for conversion from axis-angle to euler
from os.path import splitext, basename
from os import system
from numpy import deg2rad


# utility functions for our python scripts are hard-coded here

BFUNC = """

from mathutils import Vector

# These functions are inserted by DAVE.io.blender.py

def insert_objects(filepath,scale=(1,1,1),rotation=(0,0,0), offset=(0,0,0), orientation=(0,0,0), position=(0,0,0) ):
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

	with bpy.data.libraries.load(filepath=filepath, relative=False) as (data_from, data_to):
		data_to.objects.extend(data_from.objects)
	
	for object in data_to.objects:
		print(object.name)

		if object.type == 'MESH':    # only add meshes, materials are automatically included
			bpy.ops.object.add_named(name=object.name)
			# When you use bpy.ops.object.add() the newly created object becomes the active object
			# bpy.context.active_object
			active_object = bpy.context.view_layer.objects.active
			bpy.ops.object.select_all(action='DESELECT')
			active_object.select_set(True)
			# set absolute
			# active_object.location = (0,0,5)
			# active_object.rotation_euler = (1,2,3)
			# active_object.scale = (2,1,1)
			# apply transform
			bpy.ops.transform.translate(value=offset)
			bpy.ops.transform.rotate(value=-rotation[0], orient_axis='Z') # blender rotates in opposite direction (2.80)
			bpy.ops.transform.rotate(value=-rotation[1], orient_axis='Y')
			bpy.ops.transform.rotate(value=-rotation[2], orient_axis='X')
			bpy.ops.transform.resize(value=scale)
			# apply global transforms
			bpy.ops.transform.rotate(value=-orientation[0], orient_axis='Z')
			bpy.ops.transform.rotate(value=-orientation[1], orient_axis='Y')
			bpy.ops.transform.rotate(value=-orientation[2], orient_axis='X')
			bpy.ops.transform.translate(value=position)

def add_line(p1, p2, diameter, name=None):

    bpy.ops.curve.primitive_bezier_curve_add(enter_editmode=True)
    obj_data = bpy.context.active_object.data
    obj_data.bevel_depth = diameter

    end1 = obj_data.splines[0].bezier_points[0]
    end1.co = p1
    end1.handle_left = p1
    end1.handle_right = p1

    end2 = obj_data.splines[0].bezier_points[1]
    end2.co = p2
    end2.handle_left = p2
    end2.handle_right = p2

    if name is not None:
        bpy.context.active_object.name = name

    bpy.ops.object.mode_set(mode='OBJECT')
"""



def _to_euler(rotation):
    r = Rotation.from_rotvec(deg2rad(rotation))
    return r.as_euler('zyx',degrees=False)




def create_blend_and_open(scene, blender_base_file, blender_result_file, blender_exe_path=None, camera=None):
    create_blend(scene, blender_base_file, blender_result_file, blender_exe_path=blender_exe_path,camera=camera)
    command = '"{}"'.format(blender_result_file)
    system(command)

def create_blend(scene, blender_base_file, blender_result_file, blender_exe_path=None, camera=None):
    tempfile = consts.PATH_TEMP + 'blender.py'

    blender_py_file(scene, tempfile, blender_base_file, blender_result_file,camera=camera)

    if blender_exe_path is None:
        blender_exe_path = consts.BLENDER_EXEC

    command = '""{}" -b --python "{}""'.format(blender_exe_path, tempfile)
    print(command)
    system(command)

def blender_py_file(scene, python_file, blender_base_file, blender_result_file, camera = None):

    code = '# Auto-generated python file for blender\n# Execute using blender.exe -b --python "{}"\n\n'.format(python_file)
    code += 'import bpy\n'
    code += 'bpy.ops.wm.open_mainfile(filepath=r"{}")\n'.format(blender_base_file)
    code += '\n'
    code += BFUNC
    code += '\n'

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

        filename = scene.get_resource_path(name + '.blend')  # raises exception if file is not found

        # the offset needs to be rotated.

        rot = Rotation.from_rotvec(deg2rad(visual.parent.global_rotation))
        rotated_offset = rot.apply(visual.offset)

        code += '\ninsert_objects(filepath=r"{}", scale=({},{},{}), rotation=({},{},{}), offset=({},{},{}), orientation=({},{},{}), position=({},{},{}))'.format(
	                filename,
                    *visual.scale,
                    *_to_euler(visual.rotation),
                    *rotated_offset,
                    *_to_euler(visual.parent.global_rotation),
                    *visual.parent.global_position)


    for cable in scene.nodes_of_type(dc.Cable):
        points = []
        for p in cable._pois:
            points.append(p.global_position)

        n = len(points)
        for i in range(n-1):
            p1 = points[i]
            p2 = points[i+1]
            code += '\nadd_line(({},{},{}),({},{},{}), diameter={}, name = "{}_{}")'.format(*p1, *p2, consts.BLENDER_CABLE_DIA, cable.name, i)

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




