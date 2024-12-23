"""
  Helper functions for Marine analysis

  Main functionality:

  - linearize_buoyancy
  - calculate_linearized_buoyancy_props
  - carene_table

  - GZcurve_DisplacementDriven
  - GZcurve_MomentDriven [TODO]

"""
import math

"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Ruben de Bruin - 2019
"""

from DAVE.scene import *
import matplotlib.pyplot as plt
from warnings import warn


def linearize_buoyancy(
    scene: Scene, node: Buoyancy = None, delta_draft=1e-3, delta_roll=1, delta_pitch=0.3
):
    """Replaces the given Buoyancy node with a HydSpring node using even-keel (rotation = (0,0,0) ) as reference.

    Args:
        scene : scene
        node : node to be converted, if omitted then all nodes will be converted
        delta_draft: draft difference used in linearization [m]
        delta_roll: roll difference used in linearization [deg]
        delta_pitch pitch difference used in linearization [deg]

    See Also: calculate_linearized_buoyancy_props

    Returns a reference to the newly created HydSpring node. If node is not specified and multiple buoyancy nodes are
    present then only a reference to the last converted node is returned
    """

    if node is None:
        r = None
        for node in scene.nodes_of_type(Buoyancy):
            r = linearize_buoyancy(scene, node, delta_draft, delta_roll, delta_pitch)
        return r

    props = calculate_linearized_buoyancy_props(
        scene,
        node,
        delta_draft=delta_draft,
        delta_roll=delta_roll,
        delta_pitch=delta_pitch,
    )

    parent = node.parent
    name = node.name

    scene.delete(node)  # remove buoyancy node

    return scene.new_hydspring(
        name=name,
        parent=parent,
        cob=props["cob"],
        BMT=props["BMT"],
        BML=props["BML"],
        COFX=props["COFX"] - props["cob"][0],  # relative to CoB!
        COFY=props["COFY"] - props["cob"][1],
        kHeave=props["kHeave"],
        waterline=props["waterline"],
        displacement_kN=props["displacement_kN"],
    )


def calculate_linearized_buoyancy_props(
    scene: Scene,
    nodes: Buoyancy or list[Buoyancy],
    delta_draft=1e-3,
    delta_roll=1,
    delta_pitch=0.3,
):
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

    if isinstance(nodes, Buoyancy):
        nodes = [nodes]

    for node in nodes:
        if not isinstance(node, Buoyancy):
            raise ValueError(
                f"Node {node.name} should be a 'buoyancy' type of node but is a {type(node)}."
            )

    s = Scene()
    s.resource_provider = scene.resource_provider

    # Note that parent is created at 0,0,0 and under zero rotations
    # that means that the global axis system is the local axis system at target draft and even keel

    a = s.new_frame(nodes[0].parent.name, fixed=True)
    a.z = nodes[0].parent.global_position[2]

    for node in nodes:
        exec(node.give_python_code())  # place a copy of the buoyancy node in scene "s"

    # get buoyancy
    s.update()

    n2 = [s[node.name] for node in nodes]  # nodes in new scene

    del nodes  # to make sure it is not used again

    displacement_m3 = np.sum([node.displacement for node in n2])
    cob_local = (
        np.sum([np.array(node.cob_local) * node.displacement for node in n2], axis=0)
        / displacement_m3
    )
    cob_global = (
        np.sum([np.array(node.cob) * node.displacement for node in n2], axis=0)
        / displacement_m3
    )

    # increase draft
    old_z = a.z

    a.z = a.z - delta_draft
    s.update()

    new_disp = np.sum([node.displacement for node in n2])
    delta_disp = new_disp - displacement_m3

    if abs(delta_disp) < 1e-6:
        warn(f"Zero displacement change detected for vertical position of {a.z}m")
        return None

    Awl = delta_disp / delta_draft
    kHeave = Awl * scene.g * scene.rho_water

    # calcualte cofx and cofy from change of cob position
    # x_old * x_disp + cofx * dis_change = x_new * dis_new

    new_cob_local = (
        np.sum([np.array(node.cob_local) * node.displacement for node in n2], axis=0)
        / new_disp
    )

    COFX = (new_cob_local[0] * new_disp - cob_local[0] * displacement_m3) / delta_disp
    COFY = (new_cob_local[1] * new_disp - cob_local[1] * displacement_m3) / delta_disp

    a.z = old_z  # restore draft

    # calculate BMT and BML by rotating about cob

    rot = s.new_frame("rot", position=cob_global)
    a.change_parent_to(rot)

    rot.rotation = (delta_roll, 0, 0)  # impose heel
    s.update()
    new_cob_global = np.sum(
        [np.array(node.cob) * node.displacement for node in n2], axis=0
    ) / np.sum([node.displacement for node in n2])

    delta_MT = (
        new_cob_global[1] - cob_global[1]
    )  # Note that we're working in a copy where the parent axis is under zero heading

    rot.rotation = (0, delta_pitch, 0)  # impose trim
    s.update()
    new_cob_global = np.sum(
        [np.array(node.cob) * node.displacement for node in n2], axis=0
    ) / np.sum([node.displacement for node in n2])

    delta_ML = new_cob_global[0] - cob_global[0]

    BMT = -delta_MT / np.sin(np.deg2rad(delta_roll))
    BML = delta_ML / np.sin(np.deg2rad(delta_pitch))

    # assemble resuls in a dict
    results = {
        "cob": cob_local,
        "BMT": BMT,
        "BML": BML,
        "COFX": COFX,
        "COFY": COFY,
        "kHeave": kHeave,
        "Awl": Awl,
        "displacement_kN": displacement_m3 * scene.g * scene.rho_water,
        "displacement": displacement_m3,
        "waterline": -cob_global[2],
    }

    del s

    return results


def carene_table(
    scene,
    buoyancy_nodes,
    stepsize=0.25,
    delta_draft=1e-3,
    delta_roll=1,
    delta_pitch=0.3,
):
    """Creates a carene table for buoyancy node.

    DRAFT refers the origin the buoyancy node. That is (0,0,0) the same as the origin of its parent.

    Args:
        scene: reference to Scene object
        buoyancy_node: reference to Buoyancy node in scene OR a Frame OR a list of Buoyancy nodes**
        draft_min,draft_max: Draft range
        stepsize: Stepsize for drafts

        delta_draft, delta_roll, delta_pitch: deltas used for derivation of linearized properties (see calculate_linearized_buoyancy_props)

    **
    - If Buoyancy is a list, then all buoyancy nodes shall have the same parent.

    - If Buoyancy is a Frame or RigidBody then all *direct* Buoyancy type children of that node are used. That means: all nodes of type
    Buoyancy that have the provided Frame as parent

    Returns:
        Pandas dataframe

        Information about nodes used and not-used is provided in df.attrs dictionary

    """

    if isinstance(buoyancy_nodes, Buoyancy):
        buoyancy_nodes = [buoyancy_nodes]

    not_included_bns = (
        []
    )  # childeren that are not included because they are not direct children

    if isinstance(buoyancy_nodes, Frame):
        scene = scene.copy()
        frame = scene[buoyancy_nodes.name]

        # Working in a copy from now on

        nodes = scene.nodes_with_parent(frame, recursive=True)

        bns = [node for node in nodes if isinstance(node, Buoyancy)]

        scene._godmode = True
        for node in bns:
            node.change_parent_to(frame)

        if not bns:
            raise ValueError(
                f"There are no Buoyancy Shapes with parent {buoyancy_nodes.name}"
            )

        buoyancy_nodes = bns

    # Create a new scene with only this buoyancy node and a frame that it is on
    for buoyancy_node in buoyancy_nodes:
        if isinstance(buoyancy_node, Frame):
            raise ValueError(
                "carene_table: If a Frame is provided then it should not be in a list"
            )
        if not isinstance(buoyancy_node, Buoyancy):
            raise ValueError(
                f"Node {buoyancy_node.name} should be a 'buoyancy' type of node but is a {type(buoyancy_node)}."
            )

    # Check that all have the same parent
    parent = buoyancy_nodes[0].parent
    for bn in buoyancy_nodes:
        assert bn.parent == parent, "All nodes need to have the same parent"

    s = Scene()
    s.resource_provider = scene.resource_provider
    parent_node = s.new_frame(buoyancy_nodes[0].parent.name, fixed=True)

    for buoyancy_node in buoyancy_nodes:
        s.run_code(
            buoyancy_node.give_python_code()
        )  # place a copy of the buoyancy node in scene "s"

    zn = 1e10
    zp = -1e10

    for bn in buoyancy_nodes:
        node = s[bn.name]

        # now we have a frame (a) at 0,0,0 / 0,0,0
        # with a buoyancy shape attached to it

        # determine range

        xn, xp, yn, yp, zzn, zzp = node.trimesh.get_extends()

        zn = min(zn, zzn)
        zp = max(zp, zzp)

    deepest_draft = -zp  # negative of the highest vertex
    shallowest_draft = -zn  # negative of the lowest vertex

    # make logical steps of stepsize
    maxf = deepest_draft / stepsize
    if maxf > 0:
        maxi = math.ceil(maxf)
    else:
        maxi = math.floor(maxf)

    minf = shallowest_draft / stepsize
    if minf > 0:
        mini = math.floor(minf)
    else:
        mini = math.ceil(minf)

    steps = np.arange(maxi, mini)
    drafts = stepsize * steps
    drafts[0] = deepest_draft
    drafts = [*drafts]
    drafts.append(shallowest_draft)

    import pandas as pd

    nodes = [s[node.name] for node in buoyancy_nodes]  # nodes in copy of s

    a = []
    for z in reversed(drafts):
        print(z)

        parent_node.z = z
        r = calculate_linearized_buoyancy_props(
            s,
            nodes,
            delta_roll=delta_roll,
            delta_pitch=delta_pitch,
            delta_draft=delta_draft,
        )

        if r is None:
            continue

        r["CoB x [m]"] = r["cob"][0]
        r["CoB y [m]"] = r["cob"][1]
        r["CoB z [m]"] = r["cob"][2]
        del r["cob"]
        r["draft"] = z
        a.append(r)

    df = pd.DataFrame(a)

    df = df.rename(
        columns={
            "draft": "Draft [m]",
            "BMT": "BM T [m]",
            "BML": "BM L [m]",
            "COFX": "CoF x [m]",
            "COFY": "CoF y [m]",
            "displacement": "Displacement [m3]",
            "Awl": "Awl [m2]",
        }
    )

    df = df.set_index("Draft [m]")
    df.attrs["shape_node_names"] = [node.name for node in nodes]

    return df.drop(columns=["waterline", "displacement_kN", "kHeave"])


def GZcurve_DisplacementDriven(
    scene: Scene,
    vessel_node: Frame,
    displacement_kN=None,
    minimum_heel=0,
    maximum_heel=90,
    steps=180,
    teardown=True,
    wind_velocity=0,
    allow_surge=False,
    allow_sway=False,
    allow_yaw=False,
    allow_trim=True,
    noplot=False,
    noshow=False,
    fig=None,
    feedback=None,
    check_terminate=None,
):
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
        wind_velocity:  wind-velocity in [m/s]
        [disabled] enforce_even_keel (True) Run the analysis relative to even-keel position; otherwise run relative to equilibrium position
        allow_surge:    (False)
        allow_sway:     (False)
        allow_yaw:      (False)
        allow_trim:     (True)
        noplot:         Do not plot results [False]
        noshow:         Do plot but do not do plt.show() [False]
        fig:            Figure instance to plot in

        feedback : func(str) for providing feedback during reporting
        check_terminate : func() -> bool : for providing a terminate signal

    Returns:
        dictionary with heel, moment, and GM

        Also, it teardown is not selected, the DOFs for each of the displacements are stored in scene._gui_stability_dofs
        This is used by the Gui to make a movie of the stability calculation

    """

    # Two quick helper functions for running in controlled mode
    def give_feedback(txt):
        if feedback is not None:
            feedback(txt)

    def should_terminate():
        if check_terminate is not None:
            return check_terminate()
        else:
            return False

    # --------- verify input -----------

    s = scene  # alias
    doflog = []

    if minimum_heel > maximum_heel:
        raise ValueError("Minimum heel should be smaller than maximum heel")

    # vessel_node should not have a parent
    vessel = s._node_from_node_or_str(vessel_node)
    if vessel.parent is not None:
        give_feedback(
            'Error: "Vessel should not have a parent. Got {} as vessel which has parent {}.".format(vessel.name, vessel.parent.name)'
        )
        raise ValueError(
            "Vessel should not have a parent. Got {} as vessel which has parent {}.".format(
                vessel.name, vessel.parent.name
            )
        )

    # ---- record actual wind settings ----

    do_wind = wind_velocity > 0

    old_wind_velocity = s.wind_velocity
    old_wind_direction = s.wind_direction

    # set wind to what we need
    s.wind_velocity = 0

    # make sure that we are in equilibrium before we start
    s.solve_statics()

    # the vessel will heel towards PS, set the wind-direction accordingly
    if do_wind:
        y = vessel.uy
        s.wind_direction = np.degrees(np.arctan2(y[1], y[0])) - 180

    initial_heel = vessel.heel
    initial_trim = vessel.trim

    no_displacement = False
    if displacement_kN is None:  # default value
        displacement_kN = 1

    if displacement_kN == 1:
        no_displacement = True

    if minimum_heel == maximum_heel and steps > 1:
        raise ValueError(
            "Can not take multiple steps of min and max value are identical"
        )

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
    global_motion = s.new_frame(
        name, parent=vessel
    )  # construct at vessel origin and orientation, then even-keel
    global_motion.change_parent_to(None)
    global_motion.fixed = (
        not allow_surge,
        not allow_sway,
        False,  # heave allowed
        True,
        True,
        not allow_yaw,
    )
    # set even keel
    global_motion.set_even_keel()  # <-- we need this so that the YAW axis is vertical. If the yaw axis is not vertical then
    # free yawing of the vessel may introduce high heeling loads

    trim_motion = s.new_frame(
        s.available_name_like(vessel.name + "_trim_motion"), parent=global_motion
    )

    if allow_trim:
        trim_motion.fixed = (
            True,
            True,
            True,
            True,
            False,
            True,
        )  # allow for trim (rotation about y)
    else:
        trim_motion.set_fixed()

    name = s.available_name_like(vessel.name + "_heel")
    heel_node = s.new_frame(name, parent=trim_motion)

    heel_node.set_fixed()
    vessel.change_parent_to(heel_node)
    vessel.set_fixed()

    # record dofs
    s._vfc.state_update()
    D0 = s._vfc.get_dofs()

    # ----------------- do the calcs ---------------

    heel = np.linspace(minimum_heel, maximum_heel, num=steps)
    moment = list()
    moment_wind = list()
    trim = list()

    for x in heel:
        give_feedback(f"Setting heel angle {x} deg")

        s._vfc.set_dofs(D0)
        heel_node.rx = x

        give_feedback(f"Solving without wind")
        s._solve_statics_with_optional_control(
            feedback_func=feedback, do_terminate_func=check_terminate
        )

        if should_terminate():
            return None

        # moment.append(-heel_node.applied_force[3])  # No, applied force is in global axis system
        moment.append(
            -vessel.connection_moment_x
        )  # this is the connection moment in the axis system of the heel node

        trim.append(trim_motion.ry)

        # activate wind
        if do_wind:
            s.wind_velocity = wind_velocity
            give_feedback(f"Solving with wind")

            # We need to solve, suspended cargo may change position. But fix the vessel such that is does not change position due to wind
            old_fixes = global_motion.fixed
            global_motion.fixed = True

            s._solve_statics_with_optional_control(
                feedback_func=feedback, do_terminate_func=check_terminate
            )

            # print(global_motion.rotation)

            moment_wind.append(-vessel.connection_moment_x)

            # restore
            s.wind_velocity = 0
            global_motion.fixed = old_fixes

            if should_terminate():
                return None

        # for movie replay (temporary add of dof to heel)
        heel_node.fixed = (True, True, True, False, True, True)
        s._vfc.state_update()
        dofs = s._vfc.get_dofs()
        doflog.append(dofs)
        heel_node.set_fixed()

    # --------- collect return values --------
    r = dict()
    r["heel"] = heel
    r["moment"] = moment

    if allow_trim:
        r["trim"] = trim

    if do_wind:
        wind_moment = np.array(moment_wind) - np.array(moment)
        r["wind_moment"] = wind_moment.tolist()

    if no_displacement:
        GM = np.nan

    else:
        GZ = np.array(moment, dtype=float) / displacement_kN
        r["GZ"] = GZ

        if do_wind:
            wind_heeling_arm = -wind_moment / displacement_kN
            r["wind_heeling_arm"] = wind_heeling_arm.tolist()

        # calculate GM, but only if zero is part of the heel curve and at least two points
        if np.max(heel) >= 0 and np.min(heel) <= 0 and len(heel) > 1:
            GMs = np.diff(GZ) / np.diff(np.deg2rad(heel))
            heels = 0.5 * (heel[:-1] + heel[1:])
            GM = np.interp(0, heels, GMs)

        else:
            GM = np.nan

        r["GM"] = GM

        # restore dofs
        s._vfc.set_dofs(D0)

    # ----------- plot the results -----------

    if not noplot:
        give_feedback("creating figures")

        if fig is None:
            fig = plt.figure()
        else:
            fig.clear()

        if allow_trim:
            ax_gz = fig.add_subplot(2, 1, 1, label="gz")
            ax_trim = fig.add_subplot(2, 1, 2, label="trim")
        else:
            ax_gz = fig.add_subplot(1, 1, 1, label="gz")

        if allow_trim:
            ax_trim.plot(
                heel + initial_heel, trim + initial_trim, color="black", marker="+"
            )
            ax_trim.set_xlabel("Heel angle [deg]")
            ax_trim.set_ylabel(
                "Solved trim angle [deg]\n(including initial trim of {:.2f} [deg])".format(
                    initial_trim
                )
            )
            ax_trim.set_title("Trim resulting from imposed heel")
            ax_trim.grid()

        ax_gz.set_xlabel(
            "Heel angle [deg] including initial heel of {:.2f} deg".format(initial_heel)
        )

        what = "moment"
        if no_displacement:
            ax_gz.plot(
                heel + initial_heel,
                moment,
                color="black",
                marker="+",
                label="Restoring",
            )

            if do_wind:
                ax_gz.plot(
                    heel + initial_heel,
                    -wind_moment,
                    color="gray",
                    marker=".",
                    label="Wind",
                )
                ax_gz.set_ylabel("Moment [kN.m]")
                ax_gz.legend()

            else:
                ax_gz.set_ylabel("Restoring moment [kN*m]")
        else:
            ax_gz.plot(
                heel + initial_heel, GZ, color="black", marker="+", label="Restoring"
            )

            if do_wind:
                ax_gz.plot(
                    heel + initial_heel,
                    wind_heeling_arm,
                    color="gray",
                    marker=".",
                    label="Wind",
                )
                ax_gz.legend()
                ax_gz.set_ylabel("Lever arm [m]")
            else:
                ax_gz.set_ylabel("GZ [m]")
            what = "arm"

            # plot the GM line
            yy = ax_gz.get_ylim()
            xmax = np.rad2deg(yy[1] / GM)
            xmin = np.rad2deg(yy[0] / GM)

            xmin = np.max([xmin, np.min(heel)])
            xmax = np.min([xmax, np.max(heel)])

            ax_gz.plot(
                [xmin + initial_heel, xmax + initial_heel],
                [np.deg2rad(xmin) * GM, np.deg2rad(xmax) * GM],
            )
            box_props = dict(boxstyle="round", facecolor="gold", alpha=1)
            ax_gz.text(
                xmax,
                np.deg2rad(xmax) * GM,
                "GM = {:.2f}".format(GM),
                horizontalalignment="left",
                bbox=box_props,
            )

        ax_gz.set_title(
            f"Restoring {what} curve for {vessel.name};\n Displacement = {displacement_kN:.2f} [kN]"
        )

        ax_gz.grid("on")

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

    s.wind_direction = old_wind_direction
    s.wind_velocity = old_wind_velocity

    s.verbose = _verbose

    return r


def ballast_to_even_keel(
    bs: BallastSystem, delta_fill=1, tolerance=0.01, passive_only=False, deballast=False,
    feedback_func = None, do_terminate = None, solve_func = None
):
    """Adds `delta_fill` fill to the tank at the highest projected elevation until parent
    of ballast-system is within heel and trim tolerance.

    Warning: delta_fill should be matched to tolerance else the the algorithm will fail
    """
    if feedback_func is None:
        feedback_func = lambda x: None

    if do_terminate is None:
        do_terminate = lambda x: False

    if solve_func is None:
        solve_func = lambda: s.solve_statics()


    f = bs.parent
    s = f._scene

    solve_func()

    log = ["Staring ballast to even keel operation"]

    while True:
        # find highest tank
        highest = -1e6
        highest_tank = None
        lowest = 1e6
        lowest_tank = None

        for tank in bs.tanks:
            if bs.is_frozen(tank.name):
                continue

            if not passive_only or (tank.level_global < 0):  # only passive filling
                if tank.fill_pct <= 100 - (delta_fill + 1e-6):
                    gz = f.to_glob_position((*tank.cog_when_full[:2], 0))[
                        2
                    ]  # vertical position of tank if it was as zero local elevation

                    if gz > highest:
                        highest_tank = tank
                        highest = gz

            if not passive_only or (tank.level_global > 0):  # only passive emptying
                if tank.fill_pct >= (delta_fill + 1e-6):
                    gz = f.to_glob_position((*tank.cog_when_full[:2], 0))[
                        2
                    ]  # vertical position of tank if it was as zero local elevation

                    if gz < lowest:
                        lowest_tank = tank
                        lowest = gz

        if not deballast and highest_tank is None:
            raise ValueError("No fillable tanks found")

        if deballast and lowest_tank is None:
            raise ValueError("No drainable tanks found")

        if deballast:
            lowest_tank.fill_pct -= delta_fill
        else:
            highest_tank.fill_pct += delta_fill

        old_heel = f.heel
        old_trim = f.trim

        solve_func()

        feedback_func(f"heel: {f.heel:.2f} trim: {f.trim:.2f} - {log[-1]}")
        if do_terminate():
            return log

        if (f.heel * old_heel) < 0 and (f.trim * old_trim < 0):  # overshoot!
            # undo and lower fill_pct

            if deballast:
                lowest_tank.fill_pct += delta_fill
                delta_fill *= 0.8
                log.append(
                    f"Draining water from tank {lowest_tank.name} overshoots, reducing fill delta to {delta_fill}%"
                )
                continue
            else:
                highest_tank.fill_pct -= delta_fill
                delta_fill *= 0.8
                log.append(
                    f"Adding water to tank {highest_tank.name} overshoots, reducing fill delta to {delta_fill}%"
                )
                continue

        else:
            if deballast:
                log.append(
                    f"Draining water from tank {lowest_tank.name} with {lowest_tank.fill_pct}%"
                )
            else:
                log.append(
                    f"Adding water to tank {highest_tank.name} with {highest_tank.fill_pct}%"
                )

        if abs(f.heel) < tolerance:
            if abs(f.trim) < tolerance:
                break

        # did anything change?
        if abs(f.heel - old_heel) > 1e-6 or abs(f.trim - old_trim) > 1e-6:
            if abs(f.heel) > abs(old_heel) and abs(f.trim) > abs(old_trim):
                raise ValueError(
                    "Action did increase total absolute heel AND trim, stopping - use different tanks or change method?"
                )
        else:
            log.append("No change in heel and trim")

    return log
