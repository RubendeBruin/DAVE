"""
Simplify
=========

Not every program supports every feature of DAVE.
This module contains methods to simplify or re-write a scene such that these features are re-written into something
that can be exported.

All methods work in-place. That means that the scene that is passed to the function is modified. As most functions are
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
        if t.manager is not None:
            raise ValueError(f'Can not convert tank {t.name} with manager {t.manager.name} to rigid-body. Please dissolve first')
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


def connector6D_to_cables(s, L6D : LC6d, L=100):
    """Convert the 6D connector to cables. The 6D connector is deleted.

    This is not an exact replacement, but it is a good approximation for small angles.
    Increase the length L to get lower interference between the directions

    We make a cube of size 2*dx,2*dy,2*dz. On each corner we connect three cables
    outwards in x,y and z directions. The length of the cables is L.

    For linear motion four or the eight cables are activated. The others go slack.

    """

    kx = L6D.stiffness[0]
    ky = L6D.stiffness[1]
    kz = L6D.stiffness[2]
    mx = L6D.stiffness[3]  # kNm / rad
    my = L6D.stiffness[4]
    mz = L6D.stiffness[5]

    # now we can calculate dx, dy and dz
    #    dx, dy, dz

    # find dx, dy and dz such that
    #
    # mx = 2*0.5*(0.5dy)**2*kz + dz*ky
    # my = dz*kx + dx*kz
    # mz = dx*ky + dy*kx
    #
    # The solution may not exist, and may not be unique
    # so when solving algebraically we run into singular matrices and zero rows.

    def root_me(X):

        dx = X[0]
        dy = X[1]
        dz = X[2]

        return [(dy**2)*kz + (dz**2)*ky - mx,
                (dz**2)*kx + (dx**2)*kz - my,
                (dx**2)*ky + (dy**2)*kx - mz]

    from scipy.optimize import root
    sol = root(root_me, [1e-3,1e-3,1e-3])
    dx,dy,dz = sol.x
    dx=abs(dx)
    dy=abs(dy)
    dz=abs(dz)

    dx = max(dx, 1e-12)  # for the signs
    dy = max(dy, 1e-12)
    dz = max(dz, 1e-12)

    # Make points on the corners of the cube
    positions = [(dx,dy,dz), (-dx,dy,dz), (dx,-dy,dz), (-dx,-dy,dz),
                 (dx,dy,-dz), (-dx,dy,-dz), (dx,-dy,-dz), (-dx,-dy,-dz)]

    # names for points
    names_main = [f'{L6D.name}_maincorner{i+1}' for i in range(8)]
    names_secondary = [f'{L6D.name}_secondarycorner{i+1}' for i in range(8)]

    # create the nodes
    for pos, name_M, name_S in zip(positions, names_main, names_secondary):

        name_S = s.available_name_like(name_S)

        P = s.new_point(name_S, position = pos, parent = L6D.secondary)

        # make the three points and cables to connect to
        x,y,z = pos
        pos1 = (x+L*np.sign(x), y, z)
        pos2 = (x, y+L*np.sign(y), z)
        pos3 = (x, y, z+L*np.sign(z))

        # We need to define the cables such that they remain under tension when the target moves
        # So they need to be a lot shorter than the distance between the points
        #
        # But the total stiffness should be the same
        Lcable = L


        if kx > 0:
            px = s.new_point(s.available_name_like(name_M+"x"),
                        position = pos1,
                        parent = L6D.main)
            s.new_cable(s.available_name_like(name_M+"x"), endA = P, endB = px, EA =  Lcable * kx / 4, length = Lcable)

        if ky > 0:
            py = s.new_point(s.available_name_like(name_M+"y"),
                        position = pos2,
                        parent = L6D.main)
            s.new_cable(s.available_name_like(name_M+"y"), endA = P, endB = py, EA =  Lcable * ky / 4, length = Lcable)

        if kz > 0:
            pz = s.new_point(s.available_name_like(name_M+"z"),
                        position = pos3,
                        parent = L6D.main)
            s.new_cable(s.available_name_like(name_M+"z"), endA = P, endB = pz, EA =  Lcable * kz / 4, length = Lcable)

        # make the cables

    s.delete(L6D)