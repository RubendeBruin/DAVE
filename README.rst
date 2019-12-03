.. image:: docs/images/promo1.jpg

============
DAVE
============

DAVE is a software package designed to make engineering more fun. DAVE will take care of calculations and book-keeping so that you can focus on designing the best solution.

Description
===========

DAVE is a python package for bookkeeping and visualization of floating, suspended and/or mechanical systems. It provides a general coordinates based geometry module and a graphical user interface.

Assets are the main building blocks of a model. Assets are digital versions of physical objects and contain all information required to use the item in engineering.
Assets can be imported into a scene (a model). In a scene assets can be connected to eachother and external influences like wind and water can be added.

Various solvers can then be used to investigate how a model behaves.
Static equilibrium can be calculated via the EquilibriumCore plugin. This core supports buoyancy based on linear hydrostatics or an imported shape.
The static equilibrium conditions allows for stability checks, static load distributions in lifting ropes, internal loads, static clearance checks and much more.

Exporting to other software packages is possible. By default an export routine to Blender (3d visualization and animation) is included.
The design of DAVE is such that export to software such as dynamic simulation packages, simulation software or game engines can easily be added.


.. image:: docs/images/twinlift.jpg

TUTORIAL
=========

A first video tutorial is available at: https://youtu.be/f-dQaaepsrk

.. raw:: html
   
   <iframe width="560" height="315" src="https://www.youtube.com/embed/f-dQaaepsrk" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>


Installation
============

Download and install python and required packages.

Download and install miniconda for x64

install packages
----------------

The following packages are required:
 - vtk version 8.2 or up (the version 8.1.2 that pip installs does not work with pyside2m so use conda instead)
 - pyside2 (installs qt)
 - IPython
 - vtkplotter
 - numpy
 - scipy
 - matplotlib
 - pyo3d (see note)
 
 
You can use the following environement yml file to create a new conda enviroment with these packages: <https://github.com/RubendeBruin/DAVE/blob/master/dave.yml>

Then do:

::

    conda env create -f dave.yml
    
to create a dedicated environment for DAVE

To activate this environment do

::

    activate dave


Clone DAVE from github:
------------------------

Go to the folder where you want to store dave and related files.

::

   git clone https://github.com/RubendeBruin/DAVE.git


Start DAVE
-----------

To start DAVE, the following needs to be run in python.

Add the "src" subfolder to the python path

::

    import sys
    sys.path.extend(r"c:\here\installed\DAVE\src"
    
import Scene and Gui

::

     from DAVE.scene import *
     from DAVE.gui import Gui

     s = Scene()
     
     # build your scene here
     # for example
     # s.new_axis('global_axis_system')
     
     Gui(s).show()

     
enjoy!
    
    

Future developments
===================

DAVE is still growing. At this moment DAVE only supports static calculations and visuals. This may sound a little disappointing but many engineering problems are actually governed by statics. Being able to accurately calculate the static loads is very valuable. Think about skew-loads on a lifting hook, barge heel change when removing weights, static load distribution changes as effect cog changes or length differences in lifting ropes, etc.

*Dynamics*

At this moment dynamics are not yet included. To incorporate these the following will be added:

  * Moments of intertia (Ixx,Iyy,Izz) for RigidBodies
  * Modal analysis for simplification of models

in the more distant future:

  * Hydrodynamic databases for vessels
  * Frequency domain responses

*Exports*

  * Exports to engineering and simulation packages

*Rigging*

For the design of rigging it is planned to add sheaves and cables with non-zero diameter.

*Other*

  * Automatic Solving of ballast configurations for vessels
  * Carene tables from buoyancy shapes
  * Contact points and planes
  * Blender rendering to Jupyter

References and credits
======================

DAVE hates re-inventing the wheel. Therefore DAVE uses the following already available software:

- Python, QT, numpy, scipy, matplotlib
- Blender <http://www.blender.org>
- vtkplotter <https://github.com/marcomusy/vtkplotter>
- vtk <http://www.vtk.org>


Note
====

This project relies on EquilibriumCore for geometry and force calculations. Contact the author for a copy of EquilibriumCore (pyo3d.pyd).
