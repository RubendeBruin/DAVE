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
s.new_rigidbody('test2', mass = 5, cog = (0,-1,0), parent = 'test', position = (5,0,0), fixed = (True,True,True,True,False,True))

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
constraints = []

for n in s._nodes:

    if isinstance(n, (RigidBody, Axis)):

        if isinstance(n, RigidBody):
            mass = max(n.mass, OFX_ZERO_MASS)
            I = (mass * n.inertia_radii ** 2).tolist()
            cog = [*n.cog]

        else:
            mass = OFX_ZERO_MASS
            I = [OFX_ZERO_MASS, OFX_ZERO_MASS, OFX_ZERO_MASS]
            cog = [0, 0, 0]



        # check the connection

        pos = [*n.position]
        rot = [*rotation_to_attitude(n.rotation)]

        if not any(n.fixed):
            connection = 'Free'

        elif np.all(n.fixed):
            if n.parent is None:
                connection = 'Fixed'
            else:
                connection = n.parent.name

        else:
            # Partially fixed - create constraint

            cname = n.name + ' [fixes]'

            if n.parent is None:
                connection = 'Fixed'
            else:
                connection = n.parent.name

            fixes = []
            for f in n.fixed:
                if f:
                    fixes.append('No')
                else:
                    fixes.append('Yes')

            c = {'Name': cname,
                 'Connection': connection,
                 'DOFFree': fixes,
                 'InitialPosition': pos,
                 'InitialAttitude': rot,
                 }

            constraints.append(c)

            # set the props for the 6d buoy
            connection = cname
            pos = [0,0,0]
            rot = [0,0,0]

        b = {'Name':n.name,
             'Connection': connection,
             'InitialPosition': pos,
             'InitialAttitude': rot,
             'Mass': mass,
             'MomentsOfInertia': I,
             'CentreOfMass': cog
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



data = dict()

if buoys:
    data['6DBuoys'] = buoys
if winches:
    data['Winches'] = winches
if constraints:
    data['Constraints'] = constraints



s = yaml.dump(data, explicit_start=True)

with open(f'c:\data\ofx.yml','w') as f:
    f.write(s)
