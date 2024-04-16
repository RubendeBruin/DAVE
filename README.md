![](docs/images/promo1.jpg)

# DAVE


DAVE is a software package designed to make engineering more fun. DAVE will take care of calculations and book-keeping so that you can focus on designing the best solution.

See https://open-ocean.org/dave
Documentation: https://usedave.nl

## Download the compiled GUI

A compiled version of the graphical user interface can be downloaded here: https://www.open-ocean.org/dave-gui-standalone-portable/

## Description

DAVE is a python package for bookkeeping and visualization of floating, suspended and/or mechanical systems. It provides a general coordinates based geometry module and a graphical user interface.

Assets are the main building blocks of a model. Assets are digital versions of physical objects and contain all information required to use the item in engineering.
Assets can be imported into a scene (a model). In a scene assets can be connected to eachother and external influences like wind and water can be added.

Various solvers can then be used to investigate how a model behaves.
Static equilibrium can be calculated via the EquilibriumCore plugin. This core supports buoyancy based on linear hydrostatics or an imported shape.
The static equilibrium conditions allows for stability checks, static load distributions in lifting ropes, internal loads, static clearance checks and much more.

Exporting to other software packages is possible. By default an export routine to Blender (3d visualization and animation) is included.
The design of DAVE is such that export to software such as dynamic simulation packages, simulation software or game engines can easily be added.

## Documentation

See https://usedave.nl

## Installation

At the moment DAVE only work under Windows. Linux can be made available on request. OSX only if you sponsor me a mac with more that 8Gb ram :-p

Quick instuctions:

    pip install useDAVE


## Note

This project relies on EquilibriumCore for geometry and force calculations. This compiled module is downloaded when starting the gui for the first time.
