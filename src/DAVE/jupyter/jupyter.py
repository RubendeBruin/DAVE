"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Ruben de Bruin - 2019


  Helper functions for running DAVE from jupyter

"""



# setup headless rendering if running in linux
from platform import system
if system() == 'Linux':
    import os
    os.system('/usr/bin/Xvfb :99 -screen 0 1024x768x24 &')
    os.environ['DISPLAY'] = ':99'

import DAVE.visual
import vedo as vtkp
import vtk

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
          visual_alpha = visual_alpha,
          do_meshes = do_meshes,
          geometry_size = geometry_size,
          force_normalize = force_normalize,
          force_scale = force_scale,
          cog_normalize=cog_normalize,
          cog_scale = cog_scale)

def show(scene, sea=True,camera_pos=(50,-25,10), lookat = (0,0,0),width=1024, height = 600,
         visual_alpha=1.0,
         do_meshes = True,
         geometry_size=1,
         force_normalize=False,
         force_scale=1,
         cog_normalize=False,
         cog_scale=1):

    """
    Creates a 3d view of the scene and shows it as a static image.

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

    return _view(scene, backend= '2d', sea=sea, width = width, height = height, camera_pos=camera_pos, lookat=lookat,
          visual_alpha = visual_alpha,
          do_meshes = do_meshes,
          geometry_size = geometry_size,
          force_normalize = force_normalize,
          force_scale = force_scale,
          cog_normalize=cog_normalize,
          cog_scale = cog_scale)

def _view(scene, backend = '2d', sea=True, width=1024, height = 600, camera_pos=(50,-25,10), lookat = (0,0,0),
          visual_alpha = 1.0,
          do_meshes = True,
          geometry_size = 1,
          force_normalize = False,
          force_scale = 1,
          cog_normalize=False,
          cog_scale = 1):

    camera = dict()
    camera['viewup'] = [0, 0, 1]
    camera['pos'] = camera_pos
    camera['focalPoint'] = lookat

    vtkp.embedWindow(backend=backend)  # screenshot
    vtkp.settings.usingQt = False

    vp = DAVE.visual.Viewport(scene)

    vp.visual_alpha = visual_alpha
    vp.show_meshes = do_meshes
    vp.show_geometry = (geometry_size > 0)
    vp.geometry_scale = geometry_size
    vp.force_do_normalize = force_normalize
    vp.show_force = (force_scale > 0)
    vp.force_scale = force_scale
    vp.cog_scale = cog_scale
    vp.cog_do_normalize = cog_normalize

    vtkp.settings.lightFollowsCamera = True

    offscreen = vtkp.Plotter(axes=0, offscreen=True, size=(width, height))

    vp.show_global = sea

    vp.create_world_actors()
    vp.create_visuals(recreate=True)
    vp.position_visuals()
    vp.update_visibility()

    warningshown = False

    for va in vp.visuals:
        for a in va.actors:
            if a.GetVisibility():
                if backend == 'panel':
                    # Work-around for panel
                    tr = vtk.vtkTransform()
                    tr.SetMatrix(a.GetMatrix())

                    a.SetScale(tr.GetScale())
                    a.SetPosition(tr.GetPosition())
                    a.SetOrientation(tr.GetOrientation())

                    scale = tr.GetScale()
                    orientation = tr.GetOrientation()

                    if not warningshown:
                        if isinstance(va.node, DAVE.Visual):
                            if scale != (1, 1, 1):
                                if orientation != (0, 0, 0):
                                    print(
                                        'WARNING: THIS INTERACTIVE VIEWER WRONGLY HANDLES SCALE IN COMBINATION WITH ORIENTATION.')
                                    if va.node is not None:
                                        print(f'VISUAL FOR {va.node.name} IS NOT DISPLAYED CORRECTLY.')
                                    print('USE show(...) or Gui for correct visualization')
                                    warningshown = True

                    tr0 = vtk.vtkTransform()
                    tr0.Identity()
                    a.SetUserTransform(tr0)

                offscreen.add(a)

    return offscreen.show(camera=camera)


