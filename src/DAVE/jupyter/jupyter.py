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


def show(
    scene,
    camera_pos=(50, -25, 10),
    lookat=(0, 0, 0),
    width=1024,
    height=600,
    show_force: bool = True,  # show forces
    show_meshes: bool = True,  # show meshes and connectors
    show_global: bool = False,  # show or hide the environment (sea)
    show_cog: bool = True,
    cog_do_normalize: bool = False,
    cog_scale: float = 1.0,
    force_do_normalize: bool = True,  # Normalize force size to 1.0 for plotting
    force_scale: float = 1.6,  # Scale to be applied on (normalized) force magnitude
    geometry_scale: float = 1.0,  # poi radius of the pois
    painters="Construction",
    additional_actors=(),
    projection="3d",
    zoom_fit=False,
    scale=None,
):

    """
    Creates a 3d view of the scene and shows it as a static image.

    Args:
        scene: the scene
        sea:   plot sea [bool]
        camera_pos: camera position [x,y,z]
        lookat:  camera focal point [x,y,z] OR 'y','-y','x','-x','z','-z' to go to 2D mode
        show_force: bool = True  # show forces
        show_meshes: bool = True  # show meshes and connectors
        show_global: bool = False  # show or hide the environment (sea)
        show_cog: bool = True
        cog_do_normalize: bool = False
        cog_scale: float = 1.0
        force_do_normalize: bool = True  # Normalize force size to 1.0 for plotting
        force_scale: float = 1.6  # Scale to be applied on (normalized) force magnitude
        geometry_scale: float = 1.0  # poi radius of the pois
        painters : str with key of painters dict, or a painters instance
        additional_actors : list or tuple of actors that need to be added to the view,
        projection: '2d' or '3d'
        zoom_fit: True/False - adjust camera to view full scene
        scale : parallel scale for 2d views

    Returns:
        A 3d view

    """

    vedo.embedWindow(backend='2d', verbose=False)  # screenshot
    vedo.settings.usingQt = False

    vp = Viewport(scene, jupyter=True)

    if painters is None:
        from DAVE.settings_visuals import PAINTERS

        painters = PAINTERS["Construction"]
    elif isinstance(painters, str):
        from DAVE.settings_visuals import PAINTERS

        try:
            painters = PAINTERS[painters]
        except KeyError as E:
            print(f"Available painters are: {PAINTERS.keys()}")
            raise E

    vp.settings.painter_settings = painters

    vp.settings.show_force = show_force
    vp.settings.show_meshes = show_meshes
    vp.settings.show_global = show_global

    vp.settings.show_cog = show_cog
    vp.settings.cog_do_normalize = cog_do_normalize
    vp.settings.cog_scale = cog_scale

    vp.settings.force_do_normalize = force_do_normalize
    vp.settings.force_scale = force_scale

    vp.settings.geometry_scale = geometry_scale

    vp.setup_screen(offscreen=True, size=(width, height))

    vp.create_node_visuals(recreate=True)
    vp.position_visuals()

    for a in additional_actors:
        vp.add_temporary_actor(actor=a)

    c = vp.screen.camera

    if isinstance(lookat, str):  # go to 2d mode
        c.SetPosition(*camera_pos)

        if lookat == "x":
            c.SetViewUp(0, 0, 1)
            c.SetFocalPoint(camera_pos[0] + 1, camera_pos[1], camera_pos[2])
        elif lookat == "-x":
            c.SetViewUp(0, 0, 1)
            c.SetFocalPoint(camera_pos[0] - 1, camera_pos[1], camera_pos[2])
        elif lookat == "y":
            c.SetViewUp(0, 0, 1)
            c.SetFocalPoint(camera_pos[0], camera_pos[1] + 1, camera_pos[2])
        elif lookat == "-y":
            c.SetViewUp(0, 0, 1)
            c.SetFocalPoint(camera_pos[0], camera_pos[1] - 1, camera_pos[2])
        elif lookat == "z":
            c.SetViewUp(0, -1, 0)
            c.SetFocalPoint(camera_pos[0], camera_pos[1], camera_pos[2] + 1)
        elif lookat == "-z":
            c.SetViewUp(0, 1, 0)
            c.SetFocalPoint(camera_pos[0], camera_pos[1], camera_pos[2] - 1)
        else:
            raise ValueError('Value for "lookat" shall be x, -x, y, -y, z, -z')

        projection = "2d"

    else:

        c.SetPosition(*camera_pos)
        c.SetFocalPoint(*lookat)
        c.SetViewUp(0, 0, 1)

    if projection == "2d":
        from vedo import settings

        settings.useParallelProjection = True
        c.ParallelProjectionOn()
        if scale is not None:
            c.SetParallelScale(scale)
    else:
        from vedo import settings

        settings.useParallelProjection = False

        if scale is not None:
            warnings.warn("Scale parameter is only used for 2d projections")

    # vp.update_outlines()  # no need to update outlines. The actors are not yet in the scene, so no outlines to add

    vp.update_visibility()

    if zoom_fit and scale is not None:
        warnings.warn(
            "Both scale and zoom_fit have been defined. Scale will be ignored"
        )

    return vp.show(zoom_fit=zoom_fit)
