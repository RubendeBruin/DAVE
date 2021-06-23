"""
Simplify
=========

Not every program supports every feature of DAVE.
This module contains methods to simplify or re-write a scene such that these features are re-written into something
that can be exported.

All methods work in-place. That means that the scene that is passed to the function it modified. As must functions are
"destructive" it is recommended to run these on a copy of the original model.

Methods

- .. method:: split_cables   Splits cables into sections without sheaves

- .. method:: tanks_to_bodies   Converts tanks to rigidbodies

See also:
    DAVE.marine.linearize_buoyancy


"""

"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Ruben de Bruin - 2019

"""

from DAVE import *
import numpy as np
from numpy.linalg import norm

def tanks_to_bodies(s : Scene):
    """Converts tanks with fluid to rigid-bodies. Tanks without fluid are deleted. Rotational inertia of the
    fluid in the tanks (whatever that may be) is fixed to radii of gyration of 0.1m.

    Free-fluid surface is ignored

    Name will be re-used
    """

    tanks = s.nodes_of_type(Tank)

    for t in tanks:
        parent = t.parent
        cog_local = t.cog_local
        mass = t.volume * t.density
        name = t.name

        s.delete(t)

        if mass>1e-6:
            s.new_rigidbody(name, parent=parent, position=cog_local, cog = (0,0,0), mass=mass, inertia_radii=(0.1,0.1,0.1))



def split_cables(s : Scene):
    """Splits cables that run over intermediate points (sheaves) into separate cables. Cables running over
    circles are split into cables connected to the centers of the circles.

    Warning: this function does not compensate for the length of the cable on a circle. Circles are reduced to points.
    """

    cables = s.nodes_of_type(Cable)

    for c in cables:
        if len(c.connections) == 2:
            continue

        # cable with more than 2 connection points
        #
        # Get the points over which the cable runs. For circles get the centerpoint
        points = []
        for p in c.connections:
            if isinstance(p, Point):
                points.append(p)
            elif isinstance(p, Circle):
                points.append(p.parent)

        # calculate the actual length of the cable
        l_segments = []
        for i in range(1,len(points)):
            d = np.array(points[i].global_position) - np.array(points[i-1].global_position)
            l_segments.append(norm(d))

        l_actual = np.sum(l_segments)

        # create new cables
        for i, l_seg in enumerate(l_segments):
            name = s.available_name_like(f'{c.name}_part_{i+1}')
            s.new_cable(name,
                        endA = points[i],
                        endB = points[i+1],
                        EA = c.EA,
                        length = l_seg * c.length / l_actual)  # distribute stretch length evenly

        s.delete(c)



