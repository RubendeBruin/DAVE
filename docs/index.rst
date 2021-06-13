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

.. _toctree: http://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html
.. _reStructuredText: http://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html
.. _references: http://www.sphinx-doc.org/en/stable/markup/inline.html
.. _Python domain syntax: http://sphinx-doc.org/domains.html#the-python-domain
.. _Sphinx: http://www.sphinx-doc.org/
.. _Python: http://docs.python.org/
.. _Numpy: http://docs.scipy.org/doc/numpy
.. _SciPy: http://docs.scipy.org/doc/scipy/reference/
.. _matplotlib: https://matplotlib.org/contents.html#
.. _Pandas: http://pandas.pydata.org/pandas-docs/stable
.. _Scikit-Learn: http://scikit-learn.org/stable
.. _autodoc: http://www.sphinx-doc.org/en/stable/ext/autodoc.html
.. _Google style: https://github.com/google/styleguide/blob/gh-pages/pyguide.md#38-comments-and-docstrings
.. _NumPy style: https://numpydoc.readthedocs.io/en/latest/format.html
.. _classical style: http://www.sphinx-doc.org/en/stable/domains.html#info-field-lists
