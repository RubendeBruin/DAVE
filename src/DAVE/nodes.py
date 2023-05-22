"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Ruben de Bruin - 2019
"""

"""

Wrapping all methods of DAVEcore such that:
- it is more user-friendly
- code-completion is more robust
- we can do some additional checks. DAVEcore is written for speed, not robustness.
- DAVEcore is not a hard dependency



In order of definition:

Abstracts --> abstract classes
Geometry --> core-geometry nodes
Mixins --> mixin classes

Core --> core-connected classes
Pure --> pure-python classes
GeometricContact --> deserves its own category
Base --> fully implemented base classes (RiggingBodyContainer)
SuperNodes --> nodes composed of other nodes 

Results --> classes that are used to return results from Nodes

Base class / super
--------------------

All classes use super().__init__(scene, node)
This errors out at object with an error that its init does not accept arguments.
This is worked-around by introducing a "black hole" in the constructor of class DAVENodeBase which is to be the base of
any branch of classes.

Example:

DAVENodeBase      DAVENodeBase       ABC
     |                 |              |    
    Node               └─ Some mixin ─┘      <-- everything in this layer and lower shall call super(scene, name)
     |                        |
     └────── your node ───────┘ 


Name
-----
The NAME property is used to identify nodes and is managed in different ways:
- For Core nodes, the names is stored in the DAVEcore object
- For Pure nodes, the name is stored in the node itself using the _name property

Both call the _on_name_changed method after changing the name.
To execute custom code after name change implement this method in the class and call super()._on_name_changed() in the implementation


notes and choices:
-------------------
- properties are returned as tuple to make sure they are not editable.
   --> node.position[2] = 5 is not allowed


Checklist for adding new node classes:
--------------------------------------

Node:
- If possible, derive directly from one of the core, pure or base classes

- If not:
    - Derive from one of the fully implemented node classes and one or more mixins
    - Create a constructor that calls super().__init__(scene, name)
    - Implement any DAVENodeBase methods that are not implemented in the superclasses
    - Shackle and Sling are good examples for containers
    - GeometricContact is a good example for something complex.

Mixin:
- Derive from DAVENodeBase





"""
from .nds.abstracts import *
from .nds.enums import *
from .nds.helpers import *
from .nds.mixins import *
from .nds.base import *
from .nds.pure import *
from .nds.core import *
from .nds.results import *
from .nds.geometry import *
from .nds.geometric_contact import *
from .nds.super_nodes import *



from DAVE.settings import DAVE_ADDITIONAL_RUNTIME_MODULES,RESOURCE_PATH

DAVE_ADDITIONAL_RUNTIME_MODULES['Watch'] = Watch
DAVE_ADDITIONAL_RUNTIME_MODULES['AreaKind'] = AreaKind
DAVE_ADDITIONAL_RUNTIME_MODULES['BallastSystem'] = BallastSystem
DAVE_ADDITIONAL_RUNTIME_MODULES['Beam'] = Beam
DAVE_ADDITIONAL_RUNTIME_MODULES['Buoyancy'] = Buoyancy
DAVE_ADDITIONAL_RUNTIME_MODULES['Cable'] = Cable
DAVE_ADDITIONAL_RUNTIME_MODULES['Circle'] = Circle
DAVE_ADDITIONAL_RUNTIME_MODULES['Component'] = Component
DAVE_ADDITIONAL_RUNTIME_MODULES['Connector2d'] = Connector2d
DAVE_ADDITIONAL_RUNTIME_MODULES['ContactBall'] = ContactBall
DAVE_ADDITIONAL_RUNTIME_MODULES['ContactMesh'] = ContactMesh
DAVE_ADDITIONAL_RUNTIME_MODULES['CurrentArea'] = CurrentArea
DAVE_ADDITIONAL_RUNTIME_MODULES['Force'] = Force
DAVE_ADDITIONAL_RUNTIME_MODULES['Frame'] = Frame
DAVE_ADDITIONAL_RUNTIME_MODULES['GeometricContact'] = GeometricContact
DAVE_ADDITIONAL_RUNTIME_MODULES['HydSpring'] = HydSpring
DAVE_ADDITIONAL_RUNTIME_MODULES['LC6d'] = LC6d
DAVE_ADDITIONAL_RUNTIME_MODULES['LoadShearMomentDiagram'] = LoadShearMomentDiagram
DAVE_ADDITIONAL_RUNTIME_MODULES['Point'] = Point
DAVE_ADDITIONAL_RUNTIME_MODULES['RigidBody'] = RigidBody
DAVE_ADDITIONAL_RUNTIME_MODULES['Shackle'] = Shackle
DAVE_ADDITIONAL_RUNTIME_MODULES['Sling'] = Sling
DAVE_ADDITIONAL_RUNTIME_MODULES['SPMT'] = SPMT
DAVE_ADDITIONAL_RUNTIME_MODULES['Tank'] = Tank
DAVE_ADDITIONAL_RUNTIME_MODULES['TriMeshSource'] = TriMeshSource
DAVE_ADDITIONAL_RUNTIME_MODULES['Visual'] = Visual
DAVE_ADDITIONAL_RUNTIME_MODULES['WaveInteraction1'] = WaveInteraction1
DAVE_ADDITIONAL_RUNTIME_MODULES['WindArea'] = WindArea
DAVE_ADDITIONAL_RUNTIME_MODULES['WindOrCurrentArea'] = WindOrCurrentArea

# ABSTRACTS and MIXINS
DAVE_ADDITIONAL_RUNTIME_MODULES['DAVENodeBase'] = DAVENodeBase
DAVE_ADDITIONAL_RUNTIME_MODULES['NodeCoreConnected'] = NodeCoreConnected
DAVE_ADDITIONAL_RUNTIME_MODULES['NodePurePython'] = NodePurePython

DAVE_ADDITIONAL_RUNTIME_MODULES['Manager'] = Manager
DAVE_ADDITIONAL_RUNTIME_MODULES['Node'] = Node
DAVE_ADDITIONAL_RUNTIME_MODULES['HasFootprint'] = HasFootprint
DAVE_ADDITIONAL_RUNTIME_MODULES['HasTrimesh'] = HasTrimesh
DAVE_ADDITIONAL_RUNTIME_MODULES['HasParent'] = HasParent
DAVE_ADDITIONAL_RUNTIME_MODULES['HasSubScene'] = HasSubScene


# Helpers
DAVE_ADDITIONAL_RUNTIME_MODULES['AreaKind'] = AreaKind
DAVE_ADDITIONAL_RUNTIME_MODULES['ClaimManagement'] = ClaimManagement
DAVE_ADDITIONAL_RUNTIME_MODULES['VisualOutlineType'] = VisualOutlineType


# Register the documentation
#
cdir = Path(dirname(__file__))
filename = cdir / './resources/node_prop_info.csv'
from DAVE.settings import DAVE_NODEPROP_INFO, NodePropertyInfo

if filename.exists():

    types = DAVE_ADDITIONAL_RUNTIME_MODULES.copy()
    types['tuple'] = tuple
    types['int'] = int
    types['float'] = float
    types['bool'] = bool
    types['str'] = str
    types['dict'] = type(dict)
    types['array'] = type(np.array)

    btypes = dict()
    btypes['True'] = True
    btypes['False'] = False
    btypes['true'] = True
    btypes['false'] = False


    with open(filename, newline='') as csvfile:
        prop_reader = csv.reader(csvfile)
        header = prop_reader.__next__()  # skip the header
        for row in prop_reader:
            cls_name = row[0]
            cls = DAVE_ADDITIONAL_RUNTIME_MODULES[cls_name]

            prop_name = row[1]
            val_type = types[row[2]]

            info = NodePropertyInfo(node_class=cls,
                                    property_name=row[1],
                                    property_type=val_type,
                                    doc_short=row[3],
                                    units=row[4],
                                    remarks=row[5],
                                    is_settable=btypes[row[6]],
                                    is_single_settable=btypes[row[7]],
                                    is_single_numeric=btypes[row[8]],
                                    doc_long=row[9])

            if cls not in DAVE_NODEPROP_INFO:
                DAVE_NODEPROP_INFO[cls] = dict()
            DAVE_NODEPROP_INFO[cls][prop_name]=info

else:
    print(f'Could not register node property info because {filename} does not exist')
