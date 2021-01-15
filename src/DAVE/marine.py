"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Ruben de Bruin - 2019

  Helper functions for Marine analysis



  Main functionality:

  - linearize_buoyancy
  - calculate_linearized_buoyancy_props
  - carene_table

  - GZcurve_DisplacementDriven
  - GZcurve_MomentDriven [TODO]

"""

from DAVE.scene import *
import matplotlib.pyplot as plt
from warnings import warn

def linearize_buoyancy(scene : Scene, node : Buoyancy, delta_draft=1e-3, delta_roll = 1, delta_pitch = 0.3):
    """Replaces the given Buoyancy node with a HydSpring node using even-keel (rotation = (0,0,0) ) as reference.

    Args:
        delta_draft: draft difference used in linearization [m]
        delta_roll: roll difference used in linearization [deg]
        delta_pitch pitch difference used in linearization [deg]

    See Also: calculate_linearized_buoyancy_props

    Returns a reference to the newly created HydSpring node
    """

    props = calculate_linearized_buoyancy_props(scene, node,
                                                delta_draft=delta_draft, delta_roll = delta_roll, delta_pitch = delta_pitch)

    parent = node.parent
    name = node.name

    scene.delete(node)  # remove buoyancy node

    return scene.new_hydspring(name = name,
                        parent = parent,
                        cob = props['cob'],
                        BMT = props['BMT'],
                        BML = props['BML'],
                        COFX = props['COFX'] - props['cob'][0],  # relative to CoB!
                        COFY = props['COFY'] - props['cob'][1],
                        kHeave=props['kHeave'],
                        waterline=props['waterline'],
                        displacement_kN=props['displacement_kN'])





def calculate_linearized_buoyancy_props(scene : Scene, node : Buoyancy, delta_draft=1e-3, delta_roll = 1, delta_pitch = 0.3):
    """Obtains the linearized buoyancy properties of a buoyant shape. The properties are derived for the current
    vertical position of the parent body (draft at origin) and even-keel.

    COFX, COFY and kHeave are evaluated by increasing the draft by delta_draft.
    BMT, BML are evaluated by increasing the roll/pitch by delta_roll/delta_pitch [deg]. So roll to sb, pitch to bow.
    Note: negative values are allowed. Zero is not allowed and will result in division by zero.

        cob,"Center of buoyancy in parent axis system (m,m,m)"
        BMT,Vertical distance between cob and metacenter for roll [m]
        BML,Vertical distance between cob and metacenter for pitch [m]
        COFX,"Horizontal x-position Center of Floatation (center of waterplane area), parent axis system [m]"
        COFY,"Horizontal y-position Center of Floatation (center of waterplane area), parent axis system [m]"
        kHeave,Heave stiffness in [kN/m]
        waterline,Waterline-elevation relative to cob for un-stretched heave-spring. Positive if cob is below the waterline (which is where is normally is) [m]
        displacement_kN,False,Displacement in [kN] when waterline is at waterline-elevation
    """

    if not isinstance(node, Buoyancy):
        raise ValueError(f"Node {node.name} should be a 'buoyancy' type of node but is a {type(node)}.")



    s = Scene()
    s.resources_paths = scene.resources_paths
    a = s.new_axis(node.parent.name, fixed=True)
    a.z = node.parent.global_position[2]

    exec(node.give_python_code())  # place a copy of the buoyancy node in scene "s"

    node = s[node.name]

    # get buoyancy
    s.update()

    displacement_m3 = node.displacement
    cob = node.cob_local
    cob_global = node.cob

    # increase draft
    old_z = a.z

    a.z = a.z - delta_draft
    s.update()

    new_disp =  node.displacement
    delta_disp = new_disp - displacement_m3

    if abs(delta_disp) < 1e-6:
        warn(f'Zero displacement change detected for vertical position of {a.z}m')
        return None


    Awl = delta_disp / delta_draft
    kHeave = Awl * 9.81 * node.density

    # calcualte cofx and cofy from change of cob position
    # x_old * x_disp + cofx * dis_change = x_new * dis_new

    COFX = (node.cob_local[0] * new_disp - cob[0] * displacement_m3) / delta_disp
    COFY = (node.cob_local[1] * new_disp - cob[1] * displacement_m3) / delta_disp

    a.z = old_z # restore draft

    # calculate BMT and BML by rotating about cob

    rot = s.new_axis('rot', position = cob_global)
    a.change_parent_to(rot)

    rot.rotation = (delta_roll, 0,0) # impose heel
    s.update()

    delta_MT = node.cob[1] - cob_global[1]

    rot.rotation = (0, delta_pitch, 0)  # impose trim
    s.update()

    delta_ML = node.cob[0] - cob_global[0]

    BMT = -delta_MT / np.sin(np.deg2rad(delta_roll))
    BML = delta_ML / np.sin(np.deg2rad(delta_pitch))

    # assemble resuls in a dict
    results = {'cob': cob,
               'BMT': BMT,
               'BML': BML,
               'COFX' : COFX,
               'COFY' : COFY,
               'kHeave': kHeave,
               'Awl': Awl,
               'displacement_kN': displacement_m3 * 9.81 * node.density,
               'displacement' : displacement_m3 ,
               'waterline': -cob_global[2]}

    del s

    return results

def carene_table(scene, buoyancy_node, draft_min, draft_max,
                 stepsize=0.25,
                 delta_draft=1e-3, delta_roll = 1, delta_pitch = 0.3):

    """Creates a carene table for buoyancy node.

    DRAFT refers the origin of the parent of the buoyancy node.

    Args:
        scene: reference to Scene object
        buoyancy_node: reference to Buoyancy node in scene
        draft_min,draft_max: Draft range
        stepsize: Stepsize for drafts

        delta_draft, delta_roll, delta_pitch: deltas used for derivation of linearized properties (see calculate_linearized_buoyancy_props)

    Returns:
        Pandas dataframe

    """

    zs = np.arange(draft_min, draft_max, stepsize )
    if max(zs) < draft_max:
        zs = np.append(zs,draft_max)
    import pandas as pd

    a = []

    for z in zs:
        buoyancy_node.parent.z = -z
        r = calculate_linearized_buoyancy_props(scene, buoyancy_node, delta_roll=delta_roll, delta_pitch=delta_pitch, delta_draft=delta_draft)

        if r is None:
            break

        r['CoB x [m]'] = r['cob'][0]
        r['CoB y [m]'] = r['cob'][1]
        r['CoB z [m]'] = r['cob'][2]
        del r['cob']
        r['draft'] = z
        a.append(r)

    df = pd.DataFrame(a)

    df = df.rename(columns={'draft':'Draft [m]',
                            'BMT': 'BM T [m]',
                            'BML': 'BM L [m]',
                            'COFX': 'CoF x [m]',
                            'COFY': 'CoF y [m]',
                            'displacement': 'Displacement [m3]',
                            'Awl': 'Awl [m2]'})

    df = df.set_index('Draft [m]')

    return df.drop(columns=['waterline', 'displacement_kN','kHeave'])




def GZcurve_DisplacementDriven(scene, vessel_node, displacement_kN=None, minimum_heel= 0, maximum_heel=90, steps=180,
                               teardown=True,
                               allow_surge=False, allow_sway=False, allow_yaw=False, allow_trim=True,
                               noplot = False, noshow = False,
                               fig = None):
    """This works for vessels without a parent.

    The vessels slaved to an axis system and its heel angle is fixed and enforced. After solving statics the GZ
    curve is derived from the resulting moment on the connection.

    The vessels heel and yaw are fixed.
    The vessel is free to heave, trim, and
    Only the vessels heel angle is fixed. The vessel is free to heave and trim.

    Notes:
        The reported heel is relative to the initial equilibrium position of the vessel. So if the initial heel
        of the vessel is not zero (vessel not even keel) then the reported heel is the heel relative to that
        initial heel.

    Args:
        scene:          the scene
        vessel_node:    the vessel node or vessel node name
        displacement_kN: displacement to be used (default value of 1 results in moment in kN*m instead of arm in m)
        minimum_heel    minimum heel, begin of the curve (0)
        maximum_heel    maximum heel, end of the curve (90)
        steps:          number of steps (use un-even number to capture 0)
        teardown:       remove the helper elements after the calculation
        [disabled] enforce_even_keel (True) Run the analysis relative to even-keel position; otherwise run relative to equilibrium position
        allow_surge:    (False)
        allow_sway:     (False)
        allow_yaw:      (False)
        allow_trim:     (True)
        noplot:         Do not plot results [False]
        noshow:         Do plot but do not do plt.show() [False]
        axes:           Axes instance to plot in

    Returns:
        dictionary with heel, moment, and GM

        Also, it teardown is not selected, the DOFs for each of the displacements are stored in scene._gui_stability_dofs
        This is used by the Gui to make a movie of the stability calculation

    """



    # --------- verify input -----------

    s = scene # lazy
    doflog = []

    if minimum_heel > maximum_heel:
        raise ValueError('Minimum heel should be smaller than maximum heel')

    # vessel_node should not have a parent
    vessel = s._node_from_node_or_str(vessel_node)
    if vessel.parent is not None:
        raise ValueError("Vessel should not have a parent. Got {} as vessel which has parent {}.".format(vessel.name, vessel.parent.name))

    # make sure that we are in equilibrium before we start
    s.solve_statics()

    initial_heel = vessel.heel
    initial_trim = vessel.trim

    no_displacement = False
    if displacement_kN is None: # default value
        displacement_kN = 1

    if displacement_kN == 1:
        no_displacement = True

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

    # # check initial heel
    #
    # if enforce_even_keel:
    #
    #     # equilibrium_rotation = global_motion.rotation
    #
    #     # force global motion trim and heel to be zero but maintain heading
    #     dx = global_motion.to_glob_direction((1,0,0))
    #     yaw = np.arctan2(dx[1],dx[0])
    #     global_motion.rotation = (0,0, np.rad2deg(yaw))

    initial_rotation = global_motion.rotation

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

        # for movie replay
        heel_node.fixed = (True,True,True,False,True,True)
        s._vfc.state_update()
        dofs = s._vfc.get_dofs()
        doflog.append(dofs)
        heel_node.set_fixed()

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

        # if np.max(np.abs(initial_rotation)) > 0.01:
        #     lbl = "Equilibrium heel = {:.2f} deg, trim = {:.2f} deg".format(initial_heel, initial_trim)
        # else:
        #     lbl = None

        if fig is None:
            fig = plt.figure()
        else:
            fig.clear()

        if allow_trim:

            ax_gz = fig.add_subplot(2,1,1,label='gz')
            ax_trim = fig.add_subplot(2,1,2,label='trim')
        else:
            ax_gz = fig.add_subplot(1,1,1, label='gz')


        if allow_trim:
            ax_trim.plot(heel + initial_heel, trim + initial_trim, color='black', marker='+')
            ax_trim.set_xlabel('Heel angle [deg]')
            ax_trim.set_ylabel('Solved trim angle [deg]\n(including initial trim of {:.2f} [deg])'.format(initial_trim))
            ax_trim.set_title('Trim resulting from imposed heel')
            ax_trim.grid()

        ax_gz.set_xlabel('Heel angle [deg] including initial heel of {:.2f} deg'.format(initial_heel))

        what = 'moment'
        if no_displacement:
            ax_gz.plot(heel + initial_heel, moment, color='black', marker='+')
            ax_gz.set_ylabel('Restoring moment [kN*m]')
        else:
            ax_gz.plot(heel + initial_heel, GZ, color='black', marker='+')
            what = 'arm'
            ax_gz.set_ylabel('GZ [m]')

            # plot the GM line
            yy = ax_gz.get_ylim()
            xmax = np.rad2deg(yy[1] / GM)
            xmin = np.rad2deg(yy[0] / GM)

            xmin = np.max([xmin, np.min(heel)])
            xmax = np.min([xmax, np.max(heel)])


            ax_gz.plot([xmin + initial_heel, xmax+ initial_heel], [np.deg2rad(xmin)*GM, np.deg2rad(xmax)*GM])
            box_props = dict(boxstyle='round', facecolor='gold', alpha=1)
            ax_gz.text(xmax,np.deg2rad(xmax)*GM,'GM = {:.2f}'.format(GM),horizontalalignment='left',bbox=box_props)

        ax_gz.set_title('Restoring {} curve for {};\n Displacement = {} [kN]'.format(what, vessel.name, round(100*displacement_kN)/100))

        ax_gz.grid('on')
        # if lbl:
        #     plt.legend(facecolor='gold')
        if not noshow:
            plt.show()

    # -------- clean up -----------

    if teardown:
        vessel.change_parent_to(None)
        s.delete(global_motion)

        # restore current vessel props
        vessel.position = _position
        vessel.rotation = _rotation
        vessel.fixed = _fixed
        s.solve_statics()
    else:
        heel_node.fixed = (True, True, True, False, True, True)
        s._gui_stability_dofs = doflog

    s.verbose = _verbose

    # --------- collect return values --------
    r = dict()
    r['heel'] = heel

    if allow_trim:
        r['trim'] = trim

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


