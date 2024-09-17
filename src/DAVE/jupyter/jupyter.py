"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Ruben de Bruin - 2019


  Helper functions for running DAVE from jupyter or generating reports in PDF

"""

# # setup headless rendering if running in linux
# from platform import system
# if system() == 'Linux':
#     import os
#     os.system('/usr/bin/Xvfb :99 -screen 0 1024x768x24 &')
#     os.environ['DISPLAY'] = ':99'
import warnings

# from ..visual import Viewport

import PIL
from vtkmodules.util.numpy_support import vtk_to_numpy
import numpy as np
from vtkmodules.vtkCommonCore import vtkUnsignedCharArray

from DAVE.settings import DAVE_ANNOTATION_LAYERS


def show(
    scene,
    camera_pos=None,  #
    lookat=None,
    width=1024,
    height=600,
    show_force: bool = True,  # show forces
    show_meshes: bool = True,  # show meshes and connectors
    show_sea: bool = False,
    show_origin=True,
    show_cog: bool = True,
    cog_do_normalize: bool = False,
    cog_scale: float = 1.0,
    force_do_normalize: bool = True,  # Normalize force size to 1.0 for plotting
    force_scale: float = 1.6,  # Scale to be applied on (normalized) force magnitude
    geometry_scale: float = 1.0,  # poi radius of the pois
    painters="Construction",
    additional_actors=(),
    paint_uc=False,
    projection="3d",
    zoom_fit=False,
    scale=None,
    transparent=False,
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
        show_sea: bool = False,
        show_origin = True,
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
        paint_uc: Paint unity-checks using colors
        scale : parallel scale for 2d views

    Returns:
        A 3d view

    """

    image = pil_image(
        scene=scene,
        camera_pos=camera_pos,  #
        lookat=lookat,
        width=width,
        height=height,
        show_force=show_force,  # show forces
        show_meshes=show_meshes,  # show meshes and connectors
        show_sea=show_sea,
        show_origin=show_origin,
        show_cog=show_cog,
        cog_do_normalize=cog_do_normalize,
        cog_scale=cog_scale,
        force_do_normalize=force_do_normalize,  # Normalize force size to 1.0 for plotting
        force_scale=force_scale,  # Scale to be applied on (normalized) force magnitude
        geometry_scale=geometry_scale,  # poi radius of the pois
        painters=painters,
        additional_actors=additional_actors,
        paint_uc=paint_uc,
        projection=projection,
        zoom_fit=zoom_fit,
        scale=scale,
        transparent=transparent,
    )

    return image


def pil_image(
    scene,
    do_sequence=True,
    use_step0_as_background=True,
    use_only_steps_with_labels=False,
    camera_pos=None,  #
    lookat=None,
    width=1024,
    height=600,
    show_force: bool = True,  # show forces
    show_meshes: bool = True,  # show meshes and connectors
    show_origin: bool = True,
    show_sea: bool = False,
    show_cog: bool = False,
    cog_do_normalize: bool = False,
    cog_scale: float = 1.0,
    force_do_normalize: bool = True,  # Normalize force size to 1.0 for plotting
    force_scale: float = 1.6,  # Scale to be applied on (normalized) force magnitude
    geometry_scale: float = 1.0,  # poi radius of the pois
    painters="Construction",
    additional_actors=(),
    paint_uc=False,
    projection="3d",
    zoom_fit=False,
    scale=None,
    transparent=True,  # render using a transparent background
    layers="",
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
        show_origin : bool = True : show the origin
        show_sea : bool = False : show the sea
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
        paint_uc: Paint unity-checks using colors
        transparent : If one image: render image transparent. Multiple images: Renders the first image with solid background and the rest with transparent background
        scale : parallel scale for 2d views
        layers : str : name of the layer(s) to be included in the image. Separate multiple layers with a newline \n

    Returns:
        A 3d view

    """

    if lookat is None and camera_pos is None:
        zoom_fit = True

    if lookat is None:
        lookat = (0, 0, 0)
    if camera_pos is None:
        camera_pos = (50, -25, 10)

    from DAVE.visual_helpers.image_screen_renderer import ImageRenderer

    vp = ImageRenderer(scene)

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

    # Feed all the settings

    vp.settings.painter_settings = painters

    vp.settings.show_force = show_force
    vp.settings.show_meshes = show_meshes
    vp.settings.show_sea = show_sea
    vp.settings.show_origin = show_origin

    vp.settings.show_cog = show_cog
    vp.settings.cog_do_normalize = cog_do_normalize
    vp.settings.cog_scale = cog_scale

    vp.settings.paint_uc = paint_uc

    vp.settings.force_do_normalize = force_do_normalize
    vp.settings.force_scale = force_scale

    vp.settings.geometry_scale = geometry_scale

    # # Create screen and add visuals
    #
    # vp.create_node_visuals(recreate=True)
    # vp.create_world_actors()
    #
    # vp.position_visuals()
    #
    # for a in additional_actors:
    #     vp.add_temporary_actor(actor=a)
    #
    # # Set-up the camera

    c = vp.camera

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
        c.ParallelProjectionOn()
        if scale is not None:
            c.SetParallelScale(scale)
    else:
        if scale is not None:
            warnings.warn("Scale parameter is only used for 2d projections")

    vp.update_visibility()

    if zoom_fit and scale is not None:
        warnings.warn(
            "Both scale and zoom_fit have been defined. Scale will be ignored"
        )

    # Activate layers (if any)
    if layers:
        for layer_key in layers.split("\n"):

            if layer_key not in DAVE_ANNOTATION_LAYERS:
                raise ValueError(
                    f"Layer {layer_key} not found, available layers are: {DAVE_ANNOTATION_LAYERS.keys()}"
                )

            layer = DAVE_ANNOTATION_LAYERS[layer_key](
                scene,
                scene_renderer=vp,
                do_not_update_yet=False,
            )

            vp.layers.append(layer)

    # rotate actors to camera orientation (WindArea)
    vp._camera_direction_changed()

    # zoom-fit
    if zoom_fit:
        vp.zoom_all()

    # Now we finally have everything setup the way we want
    # time to render to an image
    #
    # This can be done by Vedo, but just as easy (and robust) to do directly

    vp.renderer.ResetCameraClippingRange()
    near, far = c.GetClippingRange()
    c.SetClippingRange((1 / 100) * far, far)

    do_timeline = do_sequence
    timeline = getattr(scene, "t")

    win = vp.window
    win.SetSize(int(width), int(height))

    if timeline is None or not do_timeline:
        # render a single image
        return vp.produce_pil_image(width=width, height=height, transparent=transparent)

    else:
        # render a sequence of images
        times = [tt for tt in timeline.times()]

        images = list()
        _transparent = False  # first image transparent

        for time in times:
            timeline.activate_time(time)

            caption = timeline.get_label(time)

            if use_only_steps_with_labels and caption is None:
                continue

            vp.position_visuals()
            vp._camera_direction_changed()
            vp.update_visibility()  # UC paint

            if use_step0_as_background and len(images) > 1:
                # we need to clean the background as the previous image is still there
                nx, ny = win.GetSize()
                arr = vtkUnsignedCharArray()
                win.GetRGBACharPixelData(0, 0, nx - 1, ny - 1, 0, arr)
                arr.Fill(0)
                win.SetRGBACharPixelData(0, 0, nx - 1, ny - 1, arr, 0)

                win.Frame()

            if use_step0_as_background and len(images) == 1:
                _transparent = True

            pil_img = vp.produce_pil_image(
                width=width, height=height, transparent=_transparent
            )

            pil_img.DAVE_caption = caption

            images.append(pil_img)

        return images


if __name__ == "__main__":
    from DAVE import Scene

    s = Scene()

    # code for Point
    s.new_point(name="Point", position=(10, 0, 0))

    # code for Frame
    s.new_frame(
        name="Frame",
        position=(0, 0, 0),
        rotation=(0, 0, 0),
        fixed=(True, True, True, True, True, True),
    )

    # code for Visual
    s.new_visual(
        name="Visual",
        parent="Frame",
        path=r"res: cube_with_bevel.obj",
        offset=(0, 0, 0),
        rotation=(0, 0, 0),
        scale=(1, 1, 1),
    )

    image = show(s, width=800.1, height=400)

    image.show()
