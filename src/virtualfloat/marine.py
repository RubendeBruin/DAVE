from virtualfloat.scene import *
import matplotlib.pyplot as plt


def GZcurve_DisplacementDriven(scene, vessel_node, displacement_kN=1, minimum_heel= 0, maximum_heel=90, steps=180, teardown=True, allow_surge=False, allow_sway=False, allow_yaw=False, allow_trim=True):
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

    Returns:


    """



    # verify input
    # vessel_node should not have a parent

    s = scene # lazy


    vessel = s._node_from_node_or_str(vessel_node)
    if vessel.parent is not None:
        raise ValueError("Vessel should not have a parent. Got {} as vessel which has parent {}.".format(vessel.name, vessel.parent.name))



    # store current vessel props
    _position = vessel.position
    _rotation = vessel.rotation
    _fixed = vessel.fixed
    _verbose = s.verbose
    s.verbose = False

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

    # do the calcs
    heel = np.linspace(minimum_heel,maximum_heel,num=steps)
    moment = list()
    trim = list()

    for x in heel:
        s._vfc.set_dofs(D0)
        heel_node.rx = x
        s.solve_statics(silent=True)
        moment.append(-heel_node.applied_force[3])
        trim.append(trim_motion.ry)

    s._vfc.set_dofs(D0)

    if allow_trim:
        plt.plot(heel, trim, color='black', marker='o')
        plt.xlabel('Imposed Heel angle [deg]')
        plt.ylabel('Solved trim angle [deg]')
        plt.title('Trim resulting from imposed heel')
        plt.grid()
        plt.figure()

    plt.plot(heel, moment, color='black', marker='o')

    plt.xlabel('Heel angle [deg]')
    what = 'moment'
    if (displacement_kN==1):
        plt.ylabel('Restoring moment [kN*m]')

    else:
        what = 'arm'
        plt.ylabel('GZ [m]')

    plt.title('Restoring {} curve for {}'.format(what, vessel.name))


    plt.grid()
    plt.show()

    if teardown:
        vessel.change_parent_to(None)
        s.delete(global_motion)

        # store current vessel props
        vessel.position = _position
        vessel.rotation = _rotation
        vessel.fixed = _fixed

    s.verbose = _verbose


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


