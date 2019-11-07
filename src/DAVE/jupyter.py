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
    Creates a 3d view of the scene.
    """
    vp = DAVE.visual.Viewport(scene)
    vp.Jupyter = True

    _setup_viewport(vp, what=what, sea=sea)

    return vp.show()

def screenshot(scene, what = 'all', sea=True, width=1024, height = 600, camera_pos=(50,-25,10), lookat = (0,0,0)):
    vp = DAVE.visual.Viewport(scene)

    _setup_viewport(vp, what=what, sea=sea)

    vp.screenshot(w=width, h=height, camera_pos=camera_pos, lookat=lookat)

