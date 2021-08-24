"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Ruben de Bruin - 2019


  Helper functions for running DAVE from jupyter

"""

# # setup headless rendering if running in linux
# from platform import system
# if system() == 'Linux':
#     import os
#     os.system('/usr/bin/Xvfb :99 -screen 0 1024x768x24 &')
#     os.environ['DISPLAY'] = ':99'
import warnings

from ..visual import Viewport
import vedo

"""
visuals [true/false]
geometry_size
normalize_force [true/false]
force_size
normalize_cog [true/false]
cog_size
orthographic [true/false]
"""

def view(scene, sea=True,camera_pos=(50,-25,10), lookat = (0,0,0),
         visual_alpha = 1.0,
         do_meshes = True,
         geometry_size=1,
         force_normalize=False,
         force_scale=1,
         cog_normalize=False,
         cog_scale=1,
         ):
    """
    Creates a 3d view of the scene and shows in using panel.


    Args:
        scene: the scene
        sea:   plot sea [bool]
        camera_pos: camera position [x,y,z]
        lookat:  camera focal point [x,y,z]
        do_visuals:  plot visuals
        geometry_size: overall geometry size (set 0 for no geometry)
        force_normalize: plot all forces at same scale [False]
        force_scale: overall force scale (set 0 for no forces)
        cog_normalize: plot all cogs at same scale [False]
        cog_scale: overall cog scale (set 0 for no cog)

    Returns:
        A 3d view

    """
    return _view(scene, 'panel', sea=sea, width = 1024, height = 800, camera_pos=camera_pos, lookat=lookat,
          geometry_size = geometry_size,
          force_normalize = force_normalize,
          force_scale = force_scale,
          cog_normalize=cog_normalize,
          cog_scale = cog_scale)

def show(scene, sea=False,camera_pos=(50,-25,10), lookat = (0,0,0),width=1024, height = 600,
         geometry_size=1,
         force_normalize=False,
         force_scale=1,
         cog_normalize=False,
         cog_scale=1,
         painters = 'Construction',
         additional_actors = [],
         projection = '3d',
         zoom_fit = False,
         scale = None):

    """
    Creates a 3d view of the scene and shows it as a static image.

    Args:
        scene: the scene
        sea:   plot sea [bool]
        camera_pos: camera position [x,y,z]
        lookat:  camera focal point [x,y,z] OR 'y','-y','x','-x','z','-z' to go to 2D mode
        geometry_size: overall geometry size (set 0 for no geometry)
        force_normalize: plot all forces at same scale [False]
        force_scale: overall force scale (set 0 for no forces)
        cog_normalize: plot all cogs at same scale [False]
        cog_scale: overall cog scale (set 0 for no cog)
        painters : str with key of painters dict, or a painters instance
        projection: '2d' or '3d'
        zoom_fit: True/False - adjust camera to view full scene
        scale : parallel scale for 2d views

    Returns:
        A 3d view

    """

    return _view(scene, backend= '2d', sea=sea, width = width, height = height, camera_pos=camera_pos, lookat=lookat,
                geometry_size = geometry_size,
                force_normalize = force_normalize,
                force_scale = force_scale,
                cog_normalize=cog_normalize,
                cog_scale = cog_scale,
                painters=painters,
                additional_actors = additional_actors,
                zoom_fit=zoom_fit,
                projection=projection,
                scale = scale)

def _view(scene, backend = '2d', sea=True, width=1024, height = 600, camera_pos=(50,-25,10), lookat = (0,0,0),
          geometry_size = 1,
          force_normalize = False,
          force_scale = 1,
          cog_normalize=False,
          cog_scale = 1,
          painters = None,
          additional_actors = (),
          zoom_fit = True,
          projection = '3d',
          scale=None):


    vedo.embedWindow(backend=backend, verbose=False)  # screenshot
    vedo.settings.usingQt = False

    vp = Viewport(scene, jupyter=True)

    if painters is None:
        from DAVE.settings_visuals import PAINTERS
        painters = PAINTERS['Construction']
    elif isinstance(painters, str):
        from DAVE.settings_visuals import PAINTERS

        try:
            painters = PAINTERS[painters]
        except KeyError as E:
            print(f'Available painters are: {PAINTERS.keys()}')
            raise E

    vp.settings.painter_settings = painters

    vp.show_geometry = (geometry_size > 0)
    vp.geometry_scale = geometry_size
    vp.force_do_normalize = force_normalize
    vp.show_force = (force_scale > 0)
    vp.force_scale = force_scale
    vp.cog_scale = cog_scale
    vp.cog_do_normalize = cog_normalize

    vp.settings.show_global = sea
    vp.setup_screen(offscreen=True, size=(width,height))

    vp.create_node_visuals(recreate=True)
    vp.position_visuals()

    vp.update_visibility()

    for a in additional_actors:
        vp.add_temporary_actor(actor=a)

    # warningshown = False

    # for va in vp.node_visuals:
    #     for a in va.actors.values():
    #         if a.GetVisibility():
    #             if backend == 'panel':
    #                 # Work-around for panel
    #                 tr = vtk.vtkTransform()
    #                 tr.SetMatrix(a.GetMatrix())
    #
    #                 a.SetScale(tr.GetScale())
    #                 a.SetPosition(tr.GetPosition())
    #                 a.SetOrientation(tr.GetOrientation())
    #
    #                 scale = tr.GetScale()
    #                 orientation = tr.GetOrientation()
    #
    #                 if not warningshown:
    #                     if isinstance(va.node, DAVE.Visual):
    #                         if scale != (1, 1, 1):
    #                             if orientation != (0, 0, 0):
    #                                 print(
    #                                     'WARNING: THIS INTERACTIVE VIEWER WRONGLY HANDLES SCALE IN COMBINATION WITH ORIENTATION.')
    #                                 if va.node is not None:
    #                                     print(f'VISUAL FOR {va.node.name} IS NOT DISPLAYED CORRECTLY.')
    #                                 print('USE show(...) or Gui for correct visualization')
    #                                 warningshown = True
    #
    #                 tr0 = vtk.vtkTransform()
    #                 tr0.Identity()
    #                 a.SetUserTransform(tr0)
    #
    #             offscreen.add(a)

    c = vp.screen.camera

    if isinstance(lookat, str):  # go to 2d mode
        c.SetPosition(*camera_pos)

        if lookat == 'x':
            c.SetViewUp(0,0,1)
            c.SetFocalPoint(camera_pos[0]+1, camera_pos[1], camera_pos[2])
        elif lookat == '-x':
            c.SetViewUp(0, 0, 1)
            c.SetFocalPoint(camera_pos[0]-1, camera_pos[1], camera_pos[2])
        elif lookat == 'y':
            c.SetViewUp(0, 0, 1)
            c.SetFocalPoint(camera_pos[0], camera_pos[1]+1, camera_pos[2])
        elif lookat == '-y':
            c.SetViewUp(0, 0, 1)
            c.SetFocalPoint(camera_pos[0], camera_pos[1]-1, camera_pos[2])
        elif lookat == 'z':
            c.SetViewUp(0, -1, 0)
            c.SetFocalPoint(camera_pos[0], camera_pos[1], camera_pos[2]+1)
        elif lookat == '-z':
            c.SetViewUp(0, 1, 0)
            c.SetFocalPoint(camera_pos[0], camera_pos[1], camera_pos[2]-1)
        else:
            raise ValueError('Value for "lookat" shall be x, -x, y, -y, z, -z')

        projection='2d'

    else:

        c.SetPosition(*camera_pos)
        c.SetFocalPoint(*lookat)
        c.SetViewUp(0, 0, 1)

    if projection=='2d':
        from vedo import settings
        settings.useParallelProjection = True
        c.ParallelProjectionOn()
        if scale is not None:
            c.SetParallelScale(scale)
    else:
        from vedo import settings
        settings.useParallelProjection = False

        if scale is not None:
            warnings.warn('Scale parameter is only used for 2d projections')

    vp.update_outlines()

    if zoom_fit and scale is not None:
        warnings.warn('Both scale and zoom_fit have been defined. Scale will be ignored')

    return vp.show(zoom_fit=zoom_fit)


