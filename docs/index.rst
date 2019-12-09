============
DAVE
============

This is the documentation of **DAVE**.

For a general introduction and source-code see `GitHub <https://github.com/RubendeBruin/DAVE>`_

For documentation of the main module "Scene" see the pdoc generated documentation.

Other subjects:

*  Assets and resources <assets_and_resources.rst>
*  Source structure <package_structure.rst>
*  Settings :py:mod:`DAVE.constants` - For changing colors, paths, naming
*  Blender :py:mod:`DAVE.io.blender` - For exporting 3D scenes
*  Jupyter :py:mod:`DAVE.jupyter` - For using DAVE in a notebook
*  Marine :py:mod:`DAVE.marine` - For doing marine stuff

Reading the documentation is good. But your first steps will be much easier when you allow yourself to use the Gui:

::

    from DAVE.scene import Scene
    from DAVE.gui import Gui

    s = Scene()
    g = Gui(s)
    g.show()


Or run gui.py



Contents
========

.. toctree::
   :maxdepth: 2

   Assets and resources <assets_and_resources.rst>
   Scene and nodes <scene_and_nodes.rst>
   Source structure <package_structure.rst>
   License <license>
   Authors <authors>
   Changelog <changelog>
   Module Reference <api/modules>


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
