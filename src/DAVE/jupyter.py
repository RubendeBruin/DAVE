"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Ruben de Bruin - 2019


  Helper functions for running virtual-float from jupyter

"""

import os

# setup headless rendering
os.system('/usr/bin/Xvfb :99 -screen 0 1024x768x24 &')
os.environ['DISPLAY'] = ':99'

import DAVE.visual
import vtkplotter as vtkp
import DAVE.settings as vc

def _setup_viewport(vp, what = 'all', sea=True):

    what = what.upper()

    vp.show_global = sea

    if what == 'ALL':
        pass
        # default
    elif what == 'VISUALS':
        vp.show_visual = True
        vp.show_geometry = False
        vp.show_force = False
    elif True:
        print('Unexpected what: {} '.format(what))
        print('What should be "all","visuals"')

    vp.create_visuals(recreate=True)
    vp.position_visuals()
    vp.update_visibility()

    return vp

def show(scene, what = 'all', sea=True):
    """
    Creates a 3d view of the scene and shows in using k3d.
    """

    vtkp.settings.embedWindow(backend='panel')

    vp = DAVE.visual.Viewport(scene, jupyter=True)
    vp.screen = vtkp.Plotter(axes=4, bg=vc.COLOR_BG1, bg2=vc.COLOR_BG2)

    _setup_viewport(vp, what=what, sea=sea)

    camera = dict()
    camera['viewup'] = [0, 0, 1]
    camera['pos'] = [10, -10, 5]
    camera['focalPoint'] = [0, 0, 0]

    # show embedded
    for va in vp.visuals:
        for a in va.actors:
            if a.GetVisibility():
                vp.screen.add(a)

    # vp.screen.camera.Reset()

    return vp.show(camera=camera)

def screenshot(scene, what = 'all', sea=True, width=1024, height = 600, camera_pos=(50,-25,10), lookat = (0,0,0)):

    vp = DAVE.visual.Viewport(scene)

    _setup_viewport(vp, what=what, sea=sea)

    vtkp.settings.embedWindow(backend=None)
    vtkp.settings.screeshotScale = 2
    vtkp.settings.screeshotLargeImage = False
    vtkp.settings.usingQt = False

    vtkp.settings.lightFollowsCamera = True

    vp.create_world_actors()

    camera = dict()
    camera['viewup'] = [0, 0, 1]
    camera['pos'] = camera_pos
    camera['focalPoint'] = lookat

    offscreen = vtkp.Plotter(axes=0, offscreen=True, size=(width, height))

    for va in vp.visuals:
        for a in va.actors:
            if a.GetVisibility():
                offscreen.add(a)

    offscreen.show(camera=camera)

    for r in offscreen.renderers:
        r.SetBackground(1, 1, 1)
        r.UseFXAAOn()

    vp.position_visuals()
    vp.update_outlines()

    filename = str(vc.PATH_TEMP_SCREENSHOT)

    print('export')
    # array = vp.screenshot(filename, returnNumpy=False)
    vtkp.screenshot(filename, returnNumpy=False)

    # import matplotlib.pyplot as plt
    #
    # plt.figure(figsize=(w/300,h/300), dpi=300)
    # plt.axis(False)
    # plt.imshow(array)
    # plt.show()

    from IPython.display import Image, display
    display(Image(filename))


