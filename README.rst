.. image:: docs/images/promo1.jpg

============
DAVE
============

DAVE is a software package designed to make engineering more fun. DAVE will take care of calculations and book-keeping so that you can focus on designing the best solution.

Description
===========

DAVE is a python package for bookkeeping and visualization of floating, suspended and/or mechanical systems. It provides a general coordinates based geometry module and a graphical user interface.

Assets are the main building blocks of a model. Assets are digital versions of physical objects and contain all information required to use the item in engineering.
Assets can be imported into a scene (a model). In a scene assets can be connected to eachother.

Various solvers can then be used to investigate how a model behaves.
Static equilibrium can be calculated via the EquilibriumCore plugin. This core supports buoyancy based on linear hydrostatics or an imported shape.
The static equilibrium conditions allows for stability checks, static load distributions in lifting ropes, internal loads, static clearance checks and much more.

Exporting to other software packages is possible. By default an export routine to Blender (3d visualization and animation) is included.
Export to engineering applications such a dynamic simulation packages, simulation software or game engines can easily be added.

.. image:: docs/images/twinny.jpg

Note
====

This project relies on EquilibriumCore for geometry and force calculations. Contact the author for a copy of EquilibriumCore (pyo3d.pyd).
