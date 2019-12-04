"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Ruben de Bruin - 2019

  Helper functions for Marine analysis

"""

from DAVE.scene import *
import matplotlib.pyplot as plt


def GZcurve_DisplacementDriven(scene, vessel_node, displacement_kN=None, minimum_heel= 0, maximum_heel=90, steps=180, teardown=True, allow_surge=False, allow_sway=False, allow_yaw=False, allow_trim=True, noplot = False, noshow = False):
    """This works for vessels without a parent.

    The vessels slaved to an axis system and its heel angle is fixed and enforced. After solving statics the GZ
    curve is derived from the resulting moment on the connection.

    The vessels heel and yaw are fixed.
    The vessel is free to heave, trim, and
    Only the vessels heel angle is fixed. The vessel is free to heave and trim.

    Args:
        scene:          the scene
        vessel_node:    the vessel node or vessel node name
        displacement_kN: displacement to be used (default value of 1 results in moment in kN*m instead of arm in m)
        minimum_heel    minimum heel, begin of the curve (0)
        maximum_heel    maximum heel, end of the curve (90)
        steps:          number of steps (use un-even number to capture 0)
        teardown:       remove the helper elements after the calculation
        allow_surge:    (False)
        allow_sway:     (False)
        allow_yaw:      (False)
        allow_trim:     (True)
        noplot:         Do not plot results [False]
        noshow:         Do plot but do not do plt.show() [False]

    Returns:
        dictionary with heel, moment, and GM

    """



    # --------- verify input -----------


    s = scene # lazy

    if minimum_heel > maximum_heel:
        raise ValueError('Minimum heel should be smaller than maximum heel')

    # vessel_node should not have a parent
    vessel = s._node_from_node_or_str(vessel_node)
    if vessel.parent is not None:
        raise ValueError("Vessel should not have a parent. Got {} as vessel which has parent {}.".format(vessel.name, vessel.parent.name))

    no_displacement = False
    if displacement_kN is None: # default value
        no_displacement = True
        displacement_kN = 1

    if minimum_heel == maximum_heel and steps>1:
        raise ValueError("Can not take multiple steps of min and max value are identical")

    # --------------- store current state -------

    # store current vessel props
    _position = vessel.position
    _rotation = vessel.rotation
    _fixed = vessel.fixed
    _verbose = s.verbose
    s.verbose = False

    # --------- construct system to impose heel ---------

    # construct axis system at vessel origin
    name = s.available_name_like(vessel.name + "_global_motion")
    global_motion = s.new_axis(name, parent=vessel) # construct at vessel origin
    global_motion.change_parent_to(None)
    global_motion.fixed = (not allow_surge,
                           not allow_sway,
                           False,               # heave allowed
                           True, True,
                           not allow_yaw)

    trim_motion = s.new_axis(s.available_name_like(vessel.name + "_trim_motion"), parent=global_motion)

    if allow_trim:
        trim_motion.fixed = (True,True,True,
                             True,False,True) # allow for trim (rotation about y)
    else:
        trim_motion.set_fixed()

    name = s.available_name_like(vessel.name + "_heel")
    heel_node = s.new_axis(name, parent=trim_motion)

    heel_node.set_fixed()
    vessel.change_parent_to(heel_node)
    vessel.set_fixed()

    # record dofs
    s._vfc.state_update()
    D0 = s._vfc.get_dofs()

    # ----------------- do the calcs ---------------

    heel = np.linspace(minimum_heel,maximum_heel,num=steps)
    moment = list()
    trim = list()

    for x in heel:
        s._vfc.set_dofs(D0)
        heel_node.rx = x
        s.solve_statics(silent=True)
        moment.append(-heel_node.applied_force[3])
        trim.append(trim_motion.ry)

    if no_displacement:
        GM = np.nan
    else:
        GZ = np.array(moment, dtype=float) / displacement_kN
        # calculate GM, but only if zero is part of the heel curve and at least two points
        if (np.max(heel)>=0 and np.min(heel)<=0 and len(heel)>1):
            GMs = np.diff(GZ) / np.diff(np.deg2rad(heel))
            heels = 0.5*(heel[:-1] + heel[1:])
            GM = np.interp(0,heels, GMs)
        else:
            GM = np.nan

        # restore dofs
        s._vfc.set_dofs(D0)

    # ----------- plot the results -----------

    if not noplot:

        if allow_trim:
            plt.plot(heel, trim, color='black', marker='+')
            plt.xlabel('Imposed Heel angle [deg]')
            plt.ylabel('Solved trim angle [deg]')
            plt.title('Trim resulting from imposed heel')
            plt.grid()
            plt.figure()

        plt.xlabel('Heel angle [deg]')
        what = 'moment'
        if no_displacement:
            plt.plot(heel, moment, color='black', marker='+')
            plt.ylabel('Restoring moment [kN*m]')
        else:
            plt.plot(heel, GZ, color='black', marker='+')
            what = 'arm'
            plt.ylabel('GZ [m]')

            # plot the GM line
            yy = plt.ylim()
            xmax = np.rad2deg(yy[1] / GM)
            xmin = np.rad2deg(yy[0] / GM)

            xmin = np.max([xmin, np.min(heel)])
            xmax = np.min([xmax, np.max(heel)])


            plt.plot([xmin, xmax], [np.deg2rad(xmin)*GM, np.deg2rad(xmax)*GM])
            box_props = dict(boxstyle='round', facecolor='gold', alpha=1)
            plt.text(xmax,np.deg2rad(xmax)*GM,'GM = {:.2f}'.format(GM),horizontalalignment='left',bbox=box_props)

        plt.title('Restoring {} curve for {}'.format(what, vessel.name))

        plt.grid()
        if not noshow:
            plt.show()

    # -------- clean up -----------

    if teardown:
        vessel.change_parent_to(None)
        s.delete(global_motion)

        # store current vessel props
        vessel.position = _position
        vessel.rotation = _rotation
        vessel.fixed = _fixed

    s.verbose = _verbose

    # --------- collect return values --------
    r = dict()
    r['heel'] = heel

    if not no_displacement:
        r['GM'] = GM
        r['GZ'] = moment
    else:
        r['moment'] = moment

    return r


def GZcurve_MomentDriven():

    """Calculates the GZ curve by applying a heeling moment and calculating the resulting heel angle. This method allows for
    accurate calculation of the curve up till approximately the maximum of the curve.

    - Where to apply moment (poi / body)
    - Where to obtain roll (body)
    - Where to get displacement from

    Returns:

    """

    # Store the current DOFs of the model
    # start with a moment (can not be obtained from the GM as more than one buoyancy object may be present)
    #


