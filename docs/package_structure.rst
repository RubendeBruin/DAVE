Structure of the python package
=================================

This help shows the setup of the source-code and informs where to add new components.

The source-code is outlined as follows:

Core elements
~~~~~~~~~~~~~~
Core elements are independent of any user interaction or visualization.

Import using


    from DAVE import *


- scene.py    , :py:mod:`DAVE.scene` main unit. Contains all scene and all nodes. Communication with pyo3d
- constants.py, :py:mod:`DAVE.constants` package-wide settings. Including settings for input/output packages
- tools.py    , :py:mod:`DAVE.tools` small helper functions for scene or constants
- / resources , standard resources (.obj) and assets

GUI components
~~~~~~~~~~~~~~~
Everything for the QT-based graphical user interface.

Import using

    from DAVE.gui import *

- gui.py , :py:mod:`DAVE.gui` contains the main window and dialogs
- element_widgets.py , :py:mod:`DAVE.element_widgets` contains the node-edit widgets
- standard_assets.py , :py:mod:`DAVE.standard_assets` this is the asset browser
- visuals.py :py:mod:`DAVE.visuals` (shared with jupyter)
- /forms , produced gui code - auto-generated
- ../guis , .ui files (qt designer)

Jupyter components
~~~~~~~~~~~~~~~~~~~
Everything for the Jupyter-based user interface

Import using

    from DAVE.jupyter import *

- /jupyter

- jupyer.py :py:mod:`DAVE.jupyter` Jupyter helper functions. Also contains the code for headless server config.
- reporting.py :py:mod:`DAVE.jupyter` Reporting nodes
- visuals.py :py:mod:`DAVE.visuals` (shared with gui)


Input/output
~~~~~~~~~~~~~
Import from and export to 3rd party packages

- io/blender.py , :py:mod:`DAVE.io.blender` blender output
- constants.py  , :py:mod:`DAVE.constants` constants for blender



Adding additional input/output functionality
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- add main unit to /io subdir
- add configuration to constants.py
- add gui interfaces to gui.py

Adding additional solvers or optimizers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- generic: add to scene.py --> use as s.solve_this()
- typical: add as separate file. --> use as special_solver(s)