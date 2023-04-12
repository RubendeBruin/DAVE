:mod:`DAVE.tools`
=================

.. py:module:: DAVE.tools

.. autoapi-nested-parse::

   This Source Code Form is subject to the terms of the Mozilla Public
   License, v. 2.0. If a copy of the MPL was not distributed with this
   file, You can obtain one at http://mozilla.org/MPL/2.0/.

   Ruben de Bruin - 2019


   Some tools



Module Contents
---------------

.. function:: assertBool(var, name='Variable')


.. function:: is_number(var)


.. function:: assert1f(var, name='Variable')


.. function:: assert1f_positive_or_zero(var, name='Variable')


.. function:: assert1f_positive(var, name='Variable')


.. function:: assert3f(var, name='Variable')

   Asserts that variable has length three and contains only numbers


.. function:: assert3f_positive(var, name='Variable')

   Asserts that variable has length three and contains only numbers


.. function:: assert6f(var, name='Variable')

   Asserts that variable has length six and contains only numbers


.. function:: assertValidName(var)


.. function:: assertPoi(var, name='Node')


.. function:: make_iterable(v)

   Makes an variable iterable by putting it in a list if needed


.. function:: radii_to_positions(rxx, ryy, rzz)

   decouple radii of gyration into six point discrete positions


.. function:: rotation_from_y_axis_direction(direction)

   Returns a rotation vector that rotates the Y-axis (0,1,0) into the given direction


