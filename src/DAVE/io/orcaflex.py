"""
DAVE to ORCAFLEX yaml

This is an incomplete export from DAVE to Orcaflex.

We are using the yaml format instead of the orcaflex API because writing to yaml does not require an orcaflex license.

Supported are:

- Rigid bodies without parent --> 6D buoys
- Cables --> winches

"""

import yaml
from scipy.spatial.transform import Rotation

OFX_ZERO_MASS = 1e-6


def rotation_to_attitude(rotation):
    """Convers a rotation vector to orcaflex attitudes"""
    r = Rotation.from_rotvec(np.deg2rad(rotation))
    eu = r.as_euler(seq='zyx',degrees=True).tolist()
    return [eu[2], eu[1], eu[0]]


from DAVE import *

s = Scene()
b = s.new_rigidbody('test', rotation = (10,10,0), mass = 5, fixed=False, cog = (0,-1,0))

s.new_point('p', position = (0,0,20))
s.new_point('p2', parent = 'test', position = (1,1,1))
s.new_point('p3', parent = 'test', position = (-1,-1,-1))
s.new_cable('line','p3','p2', sheaves=['p'],length=10,EA=100)
s.solve_statics()

# from DAVE.gui import *
# Gui(s)

data = dict()

s.sort_nodes_by_dependency()

buoys = []
winches = []

for n in s._nodes:

    if isinstance(n, RigidBody):

        mass = max(n.mass, OFX_ZERO_MASS)
        I = (mass * n.inertia_radii**2)

        b = {'Name':n.name,
             'Connection': 'Free',
             'InitialPosition': [*n.position],
             'InitialAttitude': [*rotation_to_attitude(n.rotation)],
             'Mass': mass,
             'MomentsOfInertia': I.tolist(),
             'CentreOfMass': [*n.cog]
             }
        buoys.append(b)

    if isinstance(n, Cable):

        connection = []
        connectionX = []
        connectionY = []
        connectionZ = []

        for c in n.connections:
            # either a point or a circle
            # for now only points are supported

            if isinstance(c, Circle):
                raise ValueError('Circles not yet supported')

            if c.parent is None:
                connection.append('Fixed')
            else:
                connection.append(c.parent.name)
            connectionX.append(c.position[0])
            connectionY.append(c.position[1])
            connectionZ.append(c.position[2])

        w = { 'Name': n.name,
              'Connection': connection,
              'ConnectionX': connectionX,
              'ConnectionY': connectionY,
              'ConnectionZ': connectionZ,
              'Stiffness': n.EA,
              'NumberOfConnections': len(n.connections),
              'WinchControlType': 'By Stage',
              'StageMode': ['Specified Length','Specified Payout','Specified Payout'],
              'StageValue': [n.length,0,0]
              }

        winches.append(w)


data = {'6DBuoys': buoys,
        'Winches': winches}

s = yaml.dump(data, explicit_start=True)

with open(f'c:\data\ofx.yml','w') as f:
    f.write(s)
