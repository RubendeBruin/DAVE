:mod:`DAVE.settings`
====================

.. py:module:: DAVE.settings

.. autoapi-nested-parse::

   settings.py

   This is the global configuration file.

   This file defines constants and settings used throughout the package.
   Among which:
   - paths,
   - filenames,
   - environmental constants and
   - colors

   ALL PROGRAM WIDE VARIABLES ARE DEFINED IN UPPERCASE



Module Contents
---------------

.. data:: G
   :annotation: = 9.81

   

.. data:: RHO
   :annotation: = 1.025

   

.. data:: FD_GLOBAL_MIN_DAMPING_FRACTION
   :annotation: = 0.005

   

.. data:: home
   

   

.. data:: default_user_dir
   

   

.. data:: cdir
   

   

.. data:: RESOURCE_PATH
   :annotation: = []

   

.. data:: PATH_TEMP
   

   

.. data:: PATH_TEMP_SCREENSHOT
   

   Debugging/logging

   By default a file "log.txt" is saved in the users temporary folder


.. data:: LOGFILE
   

   Node-name settings


.. data:: VF_NAME_SPLIT
   :annotation: = -->

   

.. data:: MANAGED_NODE_IDENTIFIER
   :annotation: = >>>

   =========== Visuals ==================

   This section defines color and geometry options for visualization in VTK


.. data:: VISUAL_BUOYANCY_PLANE_EXTEND
   :annotation: = 5

   

.. data:: TEXTURE_SEA
   

   

.. data:: ALPHA_SEA
   :annotation: = 0.8

   

.. data:: RESOLUTION_SPHERE
   :annotation: = 12

   

.. data:: RESOLUTION_ARROW
   :annotation: = 12

   

.. data:: _BLACK
   :annotation: = [0, 0, 0]

   

.. data:: _RED
   :annotation: = [144, 33, 30]

   

.. data:: _ORANGE
   :annotation: = [200, 80, 33]

   

.. data:: _BROWN
   :annotation: = [187, 134, 41]

   

.. data:: _GREEN
   :annotation: = [0, 127, 14]

   

.. data:: _YELLOW
   :annotation: = [255, 216, 0]

   

.. data:: _PURPLE
   :annotation: = [87, 0, 127]

   

.. data:: _WHITE
   :annotation: = [255, 255, 255]

   

.. data:: _BLUE
   :annotation: = [12, 106, 146]

   

.. data:: _BLUE_LIGHT
   :annotation: = [203, 224, 239]

   

.. data:: _BLUE_DARK
   :annotation: = [57, 76, 90]

   

.. data:: _PINK
   :annotation: = [247, 17, 228]

   

.. data:: _DARK_GRAY
   :annotation: = [45, 45, 48]

   

.. data:: _LIGHT_GRAY
   :annotation: = [200, 200, 200]

   

.. data:: _MEDIUM_GRAY
   :annotation: = [145, 145, 145]

   

.. function:: rgb(col)


.. data:: COLOR_SELECT
   

   

.. data:: COLOR_VISUAL
   

   

.. data:: COLOR_CABLE
   

   

.. data:: COLOR_POI
   

   

.. data:: COLOR_WAVEINTERACTION
   

   

.. data:: COLOR_FORCE
   

   

.. data:: COLOR_SHEAVE
   

   

.. data:: COLOR_COG
   

   

.. data:: COLOR_BEAM
   

   

.. data:: COLOR_BUOYANCY_MESH_FILL
   

   

.. data:: COLOR_BUOYANCY_MESH_LINES
   

   

.. data:: LINEWIDTH_SUBMERGED_MESH
   :annotation: = 3

   

.. data:: COLOR_X
   

   

.. data:: COLOR_Y
   

   

.. data:: COLOR_Z
   

   

.. data:: COLOR_WATER
   

   

.. data:: COLOR_BG2
   

   

.. data:: COLOR_BG1
   

   

.. data:: COLOR_BG2_ENV
   

   

.. data:: COLOR_BG1_ENV
   

   

.. data:: ALPHA_VISUAL
   :annotation: = 0.3

   

.. data:: ALPHA_BUOYANCY
   :annotation: = 1.0

   

.. data:: OUTLINE_WIDTH
   :annotation: = 1

   

.. data:: VISUAL_DIFFUSE
   :annotation: = 0.4

   

.. data:: VISUAL_SPECULAR
   :annotation: = 0.05

   

.. data:: VISUAL_AMBIENT
   :annotation: = 0.5

   ========= GUI =================

   Gui specific settings


.. data:: PROPS_NODE
   :annotation: = ['name']

   

.. data:: PROPS_AXIS
   :annotation: = ['global_position', 'global_rotation', 'applied_force', 'connection_force', 'equilibrium_error', 'x', 'y', 'z', 'gz', 'gy', 'gz', 'rx', 'ry', 'rz', 'grx', 'gry', 'grz', 'ux', 'uy', 'uz', 'connection_force_x', 'connection_force_y', 'connection_force_z', 'connection_moment_x', 'connection_moment_y', 'connection_moment_z', 'tilt_x', 'heel', 'tilt_y', 'trim', 'heading', 'heading_compass']

   

.. data:: PROPS_POI
   :annotation: = ['global_position', 'applied_force_and_moment_global', 'x', 'y', 'z', 'gx', 'gy', 'gz']

   

.. data:: PROPS_CABLE
   :annotation: = ['tension', 'stretch']

   

.. data:: PROPS_FORCE
   :annotation: = ['force', 'fx', 'fy', 'fz', 'moment', 'mx', 'my', 'mz']

   

.. data:: PROPS_CON2D
   :annotation: = ['angle', 'moment', 'force', 'ax', 'ay', 'az']

   

.. data:: PROPS_BODY
   :annotation: = ['cog', 'cogx', 'cogy', 'cogz', 'mass']

   

.. data:: PROPS_BUOY_MESH
   :annotation: = ['cob', 'displacement', 'cob_local']

   

.. data:: PROPS_LINEARBEAM
   :annotation: = ['tension', 'torsion', 'moment_on_master', 'moment_on_slave']

   

.. data:: PROPS_CONTACTBALL
   :annotation: = ['has_contact', 'contactpoint', 'force']

   

.. data:: GUI_DO_ANIMATE
   :annotation: = True

   

.. data:: GUI_SOLVER_ANIMATION_DURATION
   :annotation: = 0.5

   

.. data:: GUI_ANIMATION_FPS
   :annotation: = 60

   

.. data:: BLENDER_EXEC_DEFAULT_WIN
   :annotation: = C:\Program Files\Blender Foundation\Blender\blender.exe

   

.. data:: pt
   :annotation: = 

   

.. data:: BLENDER_BASE_SCENE
   

   

.. data:: BLENDER_DEFAULT_OUTFILE
   

   

.. data:: BLENDER_CABLE_DIA
   :annotation: = 0.1

   

.. data:: BLENDER_BEAM_DIA
   :annotation: = 0.5

   

.. data:: BLENDER_FPS
   :annotation: = 30

   

