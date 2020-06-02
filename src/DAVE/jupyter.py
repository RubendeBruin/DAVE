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
import vtk

def show(scene, what = 'all', sea=True,camera_pos=(50,-25,10), lookat = (0,0,0)):
    """
    Creates a 3d view of the scene and shows in using k3d.
    """
    return _view(scene, 'panel', what=what, sea=sea, width = 1024, height = 800, camera_pos=camera_pos, lookat=lookat)

def screenshot(scene, what = 'all', sea=True,camera_pos=(50,-25,10), lookat = (0,0,0),width=1024, height = 600):
    return _view(scene, backend= '2d', what=what, sea=sea, width = width, height = height, camera_pos=camera_pos, lookat=lookat)

def _view(scene, backend = '2d', what = 'all', sea=True, width=1024, height = 600, camera_pos=(50,-25,10), lookat = (0,0,0)):
    camera = dict()
    camera['viewup'] = [0, 0, 1]
    camera['pos'] = camera_pos
    camera['focalPoint'] = lookat

    vtkp.embedWindow(backend=backend)  # screenshot
    vtkp.settings.usingQt = False

    vp = DAVE.visual.Viewport(scene)

    vtkp.settings.lightFollowsCamera = True

    offscreen = vtkp.Plotter(axes=0, offscreen=True, size=(width, height))

    what = what.upper()

    vp.show_global = sea

    if what == 'ALL':
        pass
        # default
    elif what == 'VISUALS':
        vp.show_visual = True
        vp.show_geometry = False
        vp.show_force = False
    else:
        print('Unexpected what: {} '.format(what))
        print('What should be "all","visuals"')

    vp.create_visuals(recreate=True)
    vp.position_visuals()
    vp.update_visibility()

    for va in vp.visuals:
        print(va.node.name)
        for a in va.actors:
            if a.GetVisibility():

                if backend == 'panel':

                    # Work-around for panel
                    tr = vtk.vtkTransform()
                    tr.SetMatrix(a.GetMatrix())

                    a.SetPosition(tr.GetPosition())
                    a.SetOrientation(tr.GetOrientation())

                    tr0 = vtk.vtkTransform()
                    tr0.Identity()
                    a.SetUserTransform(tr0)

                offscreen.add(a)

    return offscreen.show(camera=camera)


