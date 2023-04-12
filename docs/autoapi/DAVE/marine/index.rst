:mod:`DAVE.marine`
==================

.. py:module:: DAVE.marine

.. autoapi-nested-parse::

   This Source Code Form is subject to the terms of the Mozilla Public
   License, v. 2.0. If a copy of the MPL was not distributed with this
   file, You can obtain one at http://mozilla.org/MPL/2.0/.

   Ruben de Bruin - 2019

   Helper functions for Marine analysis



Module Contents
---------------

.. function:: GZcurve_DisplacementDriven(scene, vessel_node, displacement_kN=None, minimum_heel=0, maximum_heel=90, steps=180, teardown=True, allow_surge=False, allow_sway=False, allow_yaw=False, allow_trim=True, noplot=False, noshow=False)

   This works for vessels without a parent.

   The vessels slaved to an axis system and its heel angle is fixed and enforced. After solving statics the GZ
   curve is derived from the resulting moment on the connection.

   The vessels heel and yaw are fixed.
   The vessel is free to heave, trim, and
   Only the vessels heel angle is fixed. The vessel is free to heave and trim.

   .. rubric:: Notes

   The reported heel is relative to the initial equilibrium position of the vessel. So if the initial heel
   of the vessel is not zero (vessel not even keel) then the reported heel is the heel relative to that
   initial heel.

   :param scene: the scene
   :param vessel_node: the vessel node or vessel node name
   :param displacement_kN: displacement to be used (default value of 1 results in moment in kN*m instead of arm in m)
   :param minimum_heel    minimum heel, begin of the curve:
   :type minimum_heel    minimum heel, begin of the curve: 0
   :param maximum_heel    maximum heel, end of the curve:
   :type maximum_heel    maximum heel, end of the curve: 90
   :param steps: number of steps (use un-even number to capture 0)
   :param teardown: remove the helper elements after the calculation
   :param allow_surge: (False)
   :param allow_sway: (False)
   :param allow_yaw: (False)
   :param allow_trim: (True)
   :param noplot: Do not plot results [False]
   :param noshow: Do plot but do not do plt.show() [False]

   :returns: dictionary with heel, moment, and GM

             Also, it teardown is not selected, the DOFs for each of the displacements are stored in scene._gui_stability_dofs
             This is used by the Gui to make a movie of the stability calculation


.. function:: GZcurve_MomentDriven()

   Calculates the GZ curve by applying a heeling moment and calculating the resulting heel angle. This method allows for
   accurate calculation of the curve up till approximately the maximum of the curve.

   - Where to apply moment (poi / body)
   - Where to obtain roll (body)
   - Where to get displacement from

   Returns:


