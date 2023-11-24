import numpy as np
from DAVE.settings import NodePropertyInfo, DAVE_ADDITIONAL_RUNTIME_MODULES, DAVE_NODEPROP_INFO
# ===================== Auto-generated documentation registration for BallastSystem
cls = DAVE_ADDITIONAL_RUNTIME_MODULES["BallastSystem"]
DAVE_NODEPROP_INFO[cls] = dict()

# Property: target_elevation
info = NodePropertyInfo(node_class=cls,
                        property_name="target_elevation",
                        property_type=float,
                        doc_short="""The target elevation of the parent of the ballast system """,
                        doc_long = """The target elevation of the parent of the ballast system [m]""",
                        units = """[m]""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["target_elevation"] = info


# Property: cogx
info = NodePropertyInfo(node_class=cls,
                        property_name="cogx",
                        property_type=float,
                        doc_short="""X position of combined CoG of all tank contents in the ballast-system.  """,
                        doc_long = """X position of combined CoG of all tank contents in the ballast-system. (global coordinate) [m]""",
                        units = """[m]""",
                        remarks="""global coordinate""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["cogx"] = info


# Property: cogy
info = NodePropertyInfo(node_class=cls,
                        property_name="cogy",
                        property_type=float,
                        doc_short="""Y position of combined CoG of all tank contents in the ballast-system.  """,
                        doc_long = """Y position of combined CoG of all tank contents in the ballast-system. (global coordinate) [m]""",
                        units = """[m]""",
                        remarks="""global coordinate""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["cogy"] = info


# Property: cogz
info = NodePropertyInfo(node_class=cls,
                        property_name="cogz",
                        property_type=float,
                        doc_short="""Z position of combined CoG of all tank contents in the ballast-system.  """,
                        doc_long = """Z position of combined CoG of all tank contents in the ballast-system. (global coordinate) [m]""",
                        units = """[m]""",
                        remarks="""global coordinate""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["cogz"] = info


# Property: cog
info = NodePropertyInfo(node_class=cls,
                        property_name="cog",
                        property_type=tuple,
                        doc_short="""Combined CoG of all tank contents in the ballast-system.  """,
                        doc_long = """Combined CoG of all tank contents in the ballast-system. (global coordinate) [m,m,m]""",
                        units = """[m,m,m]""",
                        remarks="""global coordinate""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["cog"] = info


# Property: weight
info = NodePropertyInfo(node_class=cls,
                        property_name="weight",
                        property_type=float,
                        doc_short="""Total weight of all tank fillings in the ballast system """,
                        doc_long = """Total weight of all tank fillings in the ballast system [kN]""",
                        units = """[kN]""",
                        remarks="""""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["weight"] = info

# ===================== Auto-generated documentation registration for Beam
cls = DAVE_ADDITIONAL_RUNTIME_MODULES["Beam"]
DAVE_NODEPROP_INFO[cls] = dict()

# Property: n_segments
info = NodePropertyInfo(node_class=cls,
                        property_name="n_segments",
                        property_type=int,
                        doc_short="""Number of segments used in beam """,
                        doc_long = """Number of segments used in beam [-]""",
                        units = """[-]""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["n_segments"] = info


# Property: EIy
info = NodePropertyInfo(node_class=cls,
                        property_name="EIy",
                        property_type=float,
                        doc_short="""E * Iyy : bending stiffness in the XZ plane """,
                        doc_long = """E * Iyy : bending stiffness in the XZ plane [kN m2]

        E is the modulus of elasticity; for steel 190-210 GPa (10^6 kN/m2)
        Iyy is the cross section moment of inertia [m4]
        """,
                        units = """[kN m2]""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["EIy"] = info


# Property: EIz
info = NodePropertyInfo(node_class=cls,
                        property_name="EIz",
                        property_type=float,
                        doc_short="""E * Izz : bending stiffness in the XY plane """,
                        doc_long = """E * Izz : bending stiffness in the XY plane [kN m2]

        E is the modulus of elasticity; for steel 190-210 GPa (10^6 kN/m2)
        Iyy is the cross section moment of inertia [m4]
        """,
                        units = """[kN m2]""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["EIz"] = info


# Property: GIp
info = NodePropertyInfo(node_class=cls,
                        property_name="GIp",
                        property_type=float,
                        doc_short="""G * Ipp : torsional stiffness about the X (length) axis """,
                        doc_long = """G * Ipp : torsional stiffness about the X (length) axis [kN m2]

        G is the shear-modulus of elasticity; for steel 75-80 GPa (10^6 kN/m2)
        Ip is the cross section polar moment of inertia [m4]
        """,
                        units = """[kN m2]""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["GIp"] = info


# Property: EA
info = NodePropertyInfo(node_class=cls,
                        property_name="EA",
                        property_type=float,
                        doc_short="""E * A : stiffness in the length direction """,
                        doc_long = """E * A : stiffness in the length direction [kN]

        E is the modulus of elasticity; for steel 190-210 GPa (10^6 kN/m2)
        A is the cross-section area in [m2]
        """,
                        units = """[kN]""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["EA"] = info


# Property: tension_only
info = NodePropertyInfo(node_class=cls,
                        property_name="tension_only",
                        property_type=bool,
                        doc_short="""axial stiffness (EA) only applicable to tension """,
                        doc_long = """axial stiffness (EA) only applicable to tension [True/False]""",
                        units = """[True/False]""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["tension_only"] = info


# Property: mass
info = NodePropertyInfo(node_class=cls,
                        property_name="mass",
                        property_type=float,
                        doc_short="""Mass of the beam in """,
                        doc_long = """Mass of the beam in [mT]""",
                        units = """[mT]""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["mass"] = info


# Property: L
info = NodePropertyInfo(node_class=cls,
                        property_name="L",
                        property_type=float,
                        doc_short="""Length of the beam in unloaded condition """,
                        doc_long = """Length of the beam in unloaded condition [m]""",
                        units = """[m]""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["L"] = info


# Property: nodeA
info = NodePropertyInfo(node_class=cls,
                        property_name="nodeA",
                        property_type=DAVE_ADDITIONAL_RUNTIME_MODULES["Frame"],
                        doc_short="""The axis system that the A-end of the beam is connected to. The beam leaves this axis system along the X-axis """,
                        doc_long = """The axis system that the A-end of the beam is connected to. The beam leaves this axis system along the X-axis [Frame]""",
                        units = """[Frame]""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["nodeA"] = info


# Property: nodeB
info = NodePropertyInfo(node_class=cls,
                        property_name="nodeB",
                        property_type=DAVE_ADDITIONAL_RUNTIME_MODULES["Frame"],
                        doc_short="""The axis system that the B-end of the beam is connected to. The beam arrives at this axis system along the X-axis """,
                        doc_long = """The axis system that the B-end of the beam is connected to. The beam arrives at this axis system along the X-axis [Frame]""",
                        units = """[Frame]""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["nodeB"] = info


# Property: moment_A
info = NodePropertyInfo(node_class=cls,
                        property_name="moment_A",
                        property_type=tuple,
                        doc_short="""Moment on beam at node A  """,
                        doc_long = """Moment on beam at node A [kNm, kNm, kNm] (axis system of node A)""",
                        units = """[kNm, kNm, kNm]""",
                        remarks="""axis system of node A""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["moment_A"] = info


# Property: moment_B
info = NodePropertyInfo(node_class=cls,
                        property_name="moment_B",
                        property_type=tuple,
                        doc_short="""Moment on beam at node B  """,
                        doc_long = """Moment on beam at node B [kNm, kNm, kNm] (axis system of node B)""",
                        units = """[kNm, kNm, kNm]""",
                        remarks="""axis system of node B""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["moment_B"] = info


# Property: tension
info = NodePropertyInfo(node_class=cls,
                        property_name="tension",
                        property_type=float,
                        doc_short="""Tension in the beam , negative for compression""",
                        doc_long = """Tension in the beam [kN], negative for compression

        tension is calculated at the midpoints of the beam segments.
        """,
                        units = """[kN]""",
                        remarks="""""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["tension"] = info


# Property: torsion
info = NodePropertyInfo(node_class=cls,
                        property_name="torsion",
                        property_type=float,
                        doc_short="""Torsion moment . Positive if end B has a positive rotation about the x-axis of end A""",
                        doc_long = """Torsion moment [kNm]. Positive if end B has a positive rotation about the x-axis of end A

        torsion is calculated at the midpoints of the beam segments.
        """,
                        units = """[kNm]""",
                        remarks="""""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["torsion"] = info


# Property: X_nodes
info = NodePropertyInfo(node_class=cls,
                        property_name="X_nodes",
                        property_type=tuple,
                        doc_short="""Returns the x-positions of the end nodes and internal nodes along the length of the beam """,
                        doc_long = """Returns the x-positions of the end nodes and internal nodes along the length of the beam [m]""",
                        units = """[m]""",
                        remarks="""""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["X_nodes"] = info


# Property: X_midpoints
info = NodePropertyInfo(node_class=cls,
                        property_name="X_midpoints",
                        property_type=tuple,
                        doc_short="""X-positions of the beam centers measured along the length of the beam """,
                        doc_long = """X-positions of the beam centers measured along the length of the beam [m]""",
                        units = """[m]""",
                        remarks="""""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["X_midpoints"] = info


# Property: bending
info = NodePropertyInfo(node_class=cls,
                        property_name="bending",
                        property_type=np.array,
                        doc_short="""Bending forces of the end nodes and internal nodes """,
                        doc_long = """Bending forces of the end nodes and internal nodes [0, kNm, kNm]""",
                        units = """[0, kNm, kNm]""",
                        remarks="""""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["bending"] = info

# ===================== Auto-generated documentation registration for Buoyancy
cls = DAVE_ADDITIONAL_RUNTIME_MODULES["Buoyancy"]
DAVE_NODEPROP_INFO[cls] = dict()

# Property: cob
info = NodePropertyInfo(node_class=cls,
                        property_name="cob",
                        property_type=tuple,
                        doc_short="""GLOBAL position of the center of buoyancy  """,
                        doc_long = """GLOBAL position of the center of buoyancy [m,m,m] (global axis)""",
                        units = """[m,m,m]""",
                        remarks="""global axis""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["cob"] = info


# Property: cob_local
info = NodePropertyInfo(node_class=cls,
                        property_name="cob_local",
                        property_type=tuple,
                        doc_short="""Position of the center of buoyancy  """,
                        doc_long = """Position of the center of buoyancy [m,m,m] (local axis)""",
                        units = """[m,m,m]""",
                        remarks="""local axis""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["cob_local"] = info


# Property: displacement
info = NodePropertyInfo(node_class=cls,
                        property_name="displacement",
                        property_type=float,
                        doc_short="""Displaced volume of fluid """,
                        doc_long = """Displaced volume of fluid [m^3]""",
                        units = """[m^3]""",
                        remarks="""""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["displacement"] = info

# ===================== Auto-generated documentation registration for Cable
cls = DAVE_ADDITIONAL_RUNTIME_MODULES["Cable"]
DAVE_NODEPROP_INFO[cls] = dict()

# Property: tension
info = NodePropertyInfo(node_class=cls,
                        property_name="tension",
                        property_type=float,
                        doc_short="""Tension in the cable """,
                        doc_long = """Tension in the cable [kN]""",
                        units = """[kN]""",
                        remarks="""""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["tension"] = info


# Property: stretch
info = NodePropertyInfo(node_class=cls,
                        property_name="stretch",
                        property_type=float,
                        doc_short="""Stretch of the cable """,
                        doc_long = """Stretch of the cable [m]""",
                        units = """[m]""",
                        remarks="""""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["stretch"] = info


# Property: actual_length
info = NodePropertyInfo(node_class=cls,
                        property_name="actual_length",
                        property_type=float,
                        doc_short="""Current length of the cable: length + stretch """,
                        doc_long = """Current length of the cable: length + stretch [m]""",
                        units = """[m]""",
                        remarks="""""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["actual_length"] = info


# Property: length
info = NodePropertyInfo(node_class=cls,
                        property_name="length",
                        property_type=float,
                        doc_short="""Length of the cable when in rest """,
                        doc_long = """Length of the cable when in rest [m]""",
                        units = """[m]""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["length"] = info


# Property: EA
info = NodePropertyInfo(node_class=cls,
                        property_name="EA",
                        property_type=float,
                        doc_short="""Stiffness of the cable """,
                        doc_long = """Stiffness of the cable [kN]""",
                        units = """[kN]""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["EA"] = info


# Property: diameter
info = NodePropertyInfo(node_class=cls,
                        property_name="diameter",
                        property_type=float,
                        doc_short="""Diameter of the cable. Used when a cable runs over a circle. """,
                        doc_long = """Diameter of the cable. Used when a cable runs over a circle. [m]""",
                        units = """[m]""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["diameter"] = info


# Property: mass_per_length
info = NodePropertyInfo(node_class=cls,
                        property_name="mass_per_length",
                        property_type=float,
                        doc_short="""Mass per length of the cable """,
                        doc_long = """Mass per length of the cable [mT/m]""",
                        units = """[mT/m]""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["mass_per_length"] = info


# Property: mass
info = NodePropertyInfo(node_class=cls,
                        property_name="mass",
                        property_type=float,
                        doc_short="""Mass of the cable  """,
                        doc_long = """Mass of the cable (derived from length and mass-per-length) [mT]""",
                        units = """[mT]""",
                        remarks="""derived from length and mass-per-length""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["mass"] = info


# Property: reversed
info = NodePropertyInfo(node_class=cls,
                        property_name="reversed",
                        property_type=tuple,
                        doc_short="""Diameter of the cable. Used when a cable runs over a circle. """,
                        doc_long = """Diameter of the cable. Used when a cable runs over a circle. [m]""",
                        units = """[m]""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["reversed"] = info


# Property: solve_segment_lengths
info = NodePropertyInfo(node_class=cls,
                        property_name="solve_segment_lengths",
                        property_type=bool,
                        doc_short="""If True then lengths of the segment are solved for a continuous tension distribution including weight. If false then the segment lengths are determined only on the geometry """,
                        doc_long = """If True then lengths of the segment are solved for a continuous tension distribution including weight. If false then the segment lengths are determined only on the geometry [bool]
        Note that the solution is typically not unique!""",
                        units = """[bool]""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["solve_segment_lengths"] = info


# Property: friction
info = NodePropertyInfo(node_class=cls,
                        property_name="friction",
                        property_type=tuple,
                        doc_short="""Friction factors at the connections """,
                        doc_long = """Friction factors at the connections [-]""",
                        units = """[-]""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["friction"] = info


# Property: angles_at_connections
info = NodePropertyInfo(node_class=cls,
                        property_name="angles_at_connections",
                        property_type=tuple,
                        doc_short="""Change in cable direction at each of the connections """,
                        doc_long = """Change in cable direction at each of the connections [deg]""",
                        units = """[deg]""",
                        remarks="""""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["angles_at_connections"] = info


# Property: max_winding_angles
info = NodePropertyInfo(node_class=cls,
                        property_name="max_winding_angles",
                        property_type=tuple,
                        doc_short="""Maximum winding angles at the connections """,
                        doc_long = """Maximum winding angles at the connections [deg]""",
                        units = """[deg]""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["max_winding_angles"] = info


# Property: friction_forces
info = NodePropertyInfo(node_class=cls,
                        property_name="friction_forces",
                        property_type=tuple,
                        doc_short="""Forces at the connections due to friction """,
                        doc_long = """Forces at the connections due to friction [kN]""",
                        units = """[kN]""",
                        remarks="""""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["friction_forces"] = info


# Property: calculated_friction_factor
info = NodePropertyInfo(node_class=cls,
                        property_name="calculated_friction_factor",
                        property_type=float,
                        doc_short="""The friction factor that was left for DAVE to calculate , only applicable to loops""",
                        doc_long = """The friction factor that was left for DAVE to calculate [-], only applicable to loops""",
                        units = """[-]""",
                        remarks="""""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["calculated_friction_factor"] = info


# Property: friction_factors_as_calculated
info = NodePropertyInfo(node_class=cls,
                        property_name="friction_factors_as_calculated",
                        property_type=tuple,
                        doc_short="""The friction factors as calculated by DAVE , only applicable to loops""",
                        doc_long = """The friction factors as calculated by DAVE [-], only applicable to loops""",
                        units = """[-]""",
                        remarks="""""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["friction_factors_as_calculated"] = info


# Property: segment_end_tensions
info = NodePropertyInfo(node_class=cls,
                        property_name="segment_end_tensions",
                        property_type=tuple,
                        doc_short="""Tensions at the ends of each of the cable segments """,
                        doc_long = """Tensions at the ends of each of the cable segments [kN, kN]
        These are identical if the cable weight is zero.
        """,
                        units = """[kN, kN]""",
                        remarks="""""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["segment_end_tensions"] = info


# Property: segment_mean_tensions
info = NodePropertyInfo(node_class=cls,
                        property_name="segment_mean_tensions",
                        property_type=tuple,
                        doc_short="""Mean tensions in the free segments of the cable """,
                        doc_long = """Mean tensions in the free segments of the cable [kN]
        Note that the tension in a segment is constant if the cable weight is zero.
        """,
                        units = """[kN]""",
                        remarks="""""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["segment_mean_tensions"] = info

# ===================== Auto-generated documentation registration for Circle
cls = DAVE_ADDITIONAL_RUNTIME_MODULES["Circle"]
DAVE_NODEPROP_INFO[cls] = dict()

# Property: axis
info = NodePropertyInfo(node_class=cls,
                        property_name="axis",
                        property_type=tuple,
                        doc_short="""Direction of the sheave axis  """,
                        doc_long = """Direction of the sheave axis (parent axis system) [m,m,m]

        Note:
            The direction of the axis is also used to determine the positive direction over the circumference of the
            circle. This is then used when cables run over the circle or the circle is used for geometric contacts. So
            if a cable runs over the circle in the wrong direction then a solution is to change the axis direction to
            its opposite:  circle.axis =- circle.axis. (another solution in that case is to define the connections of
            the cable in the reverse order)
        """,
                        units = """[m,m,m]""",
                        remarks="""parent axis system""",
                        is_settable=True,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["axis"] = info


# Property: radius
info = NodePropertyInfo(node_class=cls,
                        property_name="radius",
                        property_type=float,
                        doc_short="""Radius of the circle """,
                        doc_long = """Radius of the circle [m]""",
                        units = """[m]""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["radius"] = info


# Property: is_roundbar
info = NodePropertyInfo(node_class=cls,
                        property_name="is_roundbar",
                        property_type=bool,
                        doc_short="""Flag to indicate that the circle should be treated as round-bar """,
                        doc_long = """Flag to indicate that the circle should be treated as round-bar [true/false]""",
                        units = """[true/false]""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["is_roundbar"] = info


# Property: global_position
info = NodePropertyInfo(node_class=cls,
                        property_name="global_position",
                        property_type=tuple,
                        doc_short="""Global position of the center of the sheave """,
                        doc_long = """Global position of the center of the sheave [m,m,m]

        Note: this is the same as the global position of the parent point.
        """,
                        units = """[m,m,m]""",
                        remarks="""""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["global_position"] = info


# Property: global_axis
info = NodePropertyInfo(node_class=cls,
                        property_name="global_axis",
                        property_type=tuple,
                        doc_short="""Global axis direction """,
                        doc_long = """Global axis direction [m,m,m]""",
                        units = """[m,m,m]""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["global_axis"] = info


# Property: position
info = NodePropertyInfo(node_class=cls,
                        property_name="position",
                        property_type=tuple,
                        doc_short="""Local position of the center of the sheave  (parent axis).""",
                        doc_long = """Local position of the center of the sheave [m,m,m] (parent axis).

        Note: this is the same as the local position of the parent point.
        """,
                        units = """[m,m,m]""",
                        remarks="""""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["position"] = info

# ===================== Auto-generated documentation registration for Component
cls = DAVE_ADDITIONAL_RUNTIME_MODULES["Component"]
DAVE_NODEPROP_INFO[cls] = dict()
# ===================== Auto-generated documentation registration for Connector2d
cls = DAVE_ADDITIONAL_RUNTIME_MODULES["Connector2d"]
DAVE_NODEPROP_INFO[cls] = dict()

# Property: angle
info = NodePropertyInfo(node_class=cls,
                        property_name="angle",
                        property_type=float,
                        doc_short="""Actual angle between nodeA and nodeB  """,
                        doc_long = """Actual angle between nodeA and nodeB [deg] (read-only)""",
                        units = """[deg]""",
                        remarks="""read-only""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["angle"] = info


# Property: force
info = NodePropertyInfo(node_class=cls,
                        property_name="force",
                        property_type=float,
                        doc_short="""Actual force between nodeA and nodeB  """,
                        doc_long = """Actual force between nodeA and nodeB [kN] (read-only)""",
                        units = """[kN]""",
                        remarks="""read-only""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["force"] = info


# Property: moment
info = NodePropertyInfo(node_class=cls,
                        property_name="moment",
                        property_type=float,
                        doc_short="""Actual moment between nodeA and nodeB  """,
                        doc_long = """Actual moment between nodeA and nodeB [kNm] (read-only)""",
                        units = """[kNm]""",
                        remarks="""read-only""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["moment"] = info


# Property: axis
info = NodePropertyInfo(node_class=cls,
                        property_name="axis",
                        property_type=tuple,
                        doc_short="""Actual rotation axis between nodeA and nodeB """,
                        doc_long = """Actual rotation axis between nodeA and nodeB [m,m,m](read-only)""",
                        units = """[m,m,m]""",
                        remarks="""read-only""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["axis"] = info


# Property: ax
info = NodePropertyInfo(node_class=cls,
                        property_name="ax",
                        property_type=float,
                        doc_short="""X component of actual rotation axis between nodeA and nodeB """,
                        doc_long = """X component of actual rotation axis between nodeA and nodeB [deg](read-only)""",
                        units = """[deg]""",
                        remarks="""read-only""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["ax"] = info


# Property: ay
info = NodePropertyInfo(node_class=cls,
                        property_name="ay",
                        property_type=float,
                        doc_short="""Y component of actual rotation axis between nodeA and nodeB  """,
                        doc_long = """Y component of actual rotation axis between nodeA and nodeB [deg] (read-only)""",
                        units = """[deg]""",
                        remarks="""read-only""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["ay"] = info


# Property: az
info = NodePropertyInfo(node_class=cls,
                        property_name="az",
                        property_type=float,
                        doc_short="""Z component of actual rotation axis between nodeA and nodeB  """,
                        doc_long = """Z component of actual rotation axis between nodeA and nodeB [deg] (read-only)""",
                        units = """[deg]""",
                        remarks="""read-only""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["az"] = info


# Property: k_linear
info = NodePropertyInfo(node_class=cls,
                        property_name="k_linear",
                        property_type=float,
                        doc_short="""Linear stiffness """,
                        doc_long = """Linear stiffness [kN/m]""",
                        units = """[kN/m]""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["k_linear"] = info


# Property: k_angular
info = NodePropertyInfo(node_class=cls,
                        property_name="k_angular",
                        property_type=float,
                        doc_short="""Angular stiffness """,
                        doc_long = """Angular stiffness [kNm/rad]""",
                        units = """[kNm/rad]""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["k_angular"] = info

# ===================== Auto-generated documentation registration for ContactBall
cls = DAVE_ADDITIONAL_RUNTIME_MODULES["ContactBall"]
DAVE_NODEPROP_INFO[cls] = dict()

# Property: can_contact
info = NodePropertyInfo(node_class=cls,
                        property_name="can_contact",
                        property_type=bool,
                        doc_short="""True if the ball is currently perpendicular to at least one of the faces of one of the meshes. So when contact is possible. To check if there is contact use "force".""",
                        doc_long = """True if the ball is currently perpendicular to at least one of the faces of one of the meshes. So when contact is possible. To check if there is contact use "force".
        See Also: Force
        """,
                        units = """""",
                        remarks="""""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["can_contact"] = info


# Property: contact_force
info = NodePropertyInfo(node_class=cls,
                        property_name="contact_force",
                        property_type=tuple,
                        doc_short="""Returns the force on the ball  """,
                        doc_long = """Returns the force on the ball [kN, kN, kN] (global axis)

        The force is applied at the center of the ball

        See Also: contact_force_magnitude
        """,
                        units = """[kN, kN, kN]""",
                        remarks="""global axis""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["contact_force"] = info


# Property: contact_force_magnitude
info = NodePropertyInfo(node_class=cls,
                        property_name="contact_force_magnitude",
                        property_type=float,
                        doc_short="""Returns the absolute force on the ball, if any """,
                        doc_long = """Returns the absolute force on the ball, if any [kN]

        The force is applied on the center of the ball

        See Also: contact_force
        """,
                        units = """[kN]""",
                        remarks="""""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["contact_force_magnitude"] = info


# Property: compression
info = NodePropertyInfo(node_class=cls,
                        property_name="compression",
                        property_type=float,
                        doc_short="""Returns the absolute compression of the ball, if any """,
                        doc_long = """Returns the absolute compression of the ball, if any [m]""",
                        units = """[m]""",
                        remarks="""""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["compression"] = info


# Property: contactpoint
info = NodePropertyInfo(node_class=cls,
                        property_name="contactpoint",
                        property_type=tuple,
                        doc_short="""Nearest point on the nearest mesh, if contact  """,
                        doc_long = """Nearest point on the nearest mesh, if contact [m,m,m] (global)""",
                        units = """[m,m,m]""",
                        remarks="""global""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["contactpoint"] = info


# Property: meshes
info = NodePropertyInfo(node_class=cls,
                        property_name="meshes",
                        property_type=tuple,
                        doc_short="""List of contact-mesh nodes.""",
                        doc_long = """List of contact-mesh nodes.
        When getting this will yield a list of node references.
        When setting node references and node-names may be used.

        eg: ball.meshes = [mesh1, 'mesh2']
        """,
                        units = """""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["meshes"] = info


# Property: meshes_names
info = NodePropertyInfo(node_class=cls,
                        property_name="meshes_names",
                        property_type=tuple,
                        doc_short="""List with the names of the meshes""",
                        doc_long = """List with the names of the meshes""",
                        units = """""",
                        remarks="""""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["meshes_names"] = info


# Property: radius
info = NodePropertyInfo(node_class=cls,
                        property_name="radius",
                        property_type=float,
                        doc_short="""Radius of the contact-ball """,
                        doc_long = """Radius of the contact-ball [m]""",
                        units = """[m]""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["radius"] = info


# Property: k
info = NodePropertyInfo(node_class=cls,
                        property_name="k",
                        property_type=float,
                        doc_short="""Compression stiffness of the ball in force per meter of compression """,
                        doc_long = """Compression stiffness of the ball in force per meter of compression [kN/m]""",
                        units = """[kN/m]""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["k"] = info

# ===================== Auto-generated documentation registration for ContactMesh
cls = DAVE_ADDITIONAL_RUNTIME_MODULES["ContactMesh"]
DAVE_NODEPROP_INFO[cls] = dict()
# ===================== Auto-generated documentation registration for CurrentArea
cls = DAVE_ADDITIONAL_RUNTIME_MODULES["CurrentArea"]
DAVE_NODEPROP_INFO[cls] = dict()
# ===================== Auto-generated documentation registration for DAVENodeBase
cls = DAVE_ADDITIONAL_RUNTIME_MODULES["DAVENodeBase"]
DAVE_NODEPROP_INFO[cls] = dict()
# ===================== Auto-generated documentation registration for Force
cls = DAVE_ADDITIONAL_RUNTIME_MODULES["Force"]
DAVE_NODEPROP_INFO[cls] = dict()

# Property: force
info = NodePropertyInfo(node_class=cls,
                        property_name="force",
                        property_type=tuple,
                        doc_short="""The x,y and z components of the force  """,
                        doc_long = """The x,y and z components of the force [kN,kN,kN] (global axis)

        Example s['wind'].force = (12,34,56)
        """,
                        units = """[kN,kN,kN]""",
                        remarks="""global axis""",
                        is_settable=True,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["force"] = info


# Property: fx
info = NodePropertyInfo(node_class=cls,
                        property_name="fx",
                        property_type=float,
                        doc_short="""The global x-component of the force  """,
                        doc_long = """The global x-component of the force [kN] (global axis)""",
                        units = """[kN]""",
                        remarks="""global axis""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["fx"] = info


# Property: fy
info = NodePropertyInfo(node_class=cls,
                        property_name="fy",
                        property_type=float,
                        doc_short="""The global y-component of the force   """,
                        doc_long = """The global y-component of the force [kN]  (global axis)""",
                        units = """[kN]""",
                        remarks="""global axis""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["fy"] = info


# Property: fz
info = NodePropertyInfo(node_class=cls,
                        property_name="fz",
                        property_type=float,
                        doc_short="""The global z-component of the force   """,
                        doc_long = """The global z-component of the force [kN]  (global axis)""",
                        units = """[kN]""",
                        remarks="""global axis""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["fz"] = info


# Property: moment
info = NodePropertyInfo(node_class=cls,
                        property_name="moment",
                        property_type=tuple,
                        doc_short="""Moment  (global).""",
                        doc_long = """Moment [kNm,kNm,kNm] (global).

        Example s['wind'].moment = (12,34,56)
        """,
                        units = """[kNm,kNm,kNm]""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["moment"] = info


# Property: mx
info = NodePropertyInfo(node_class=cls,
                        property_name="mx",
                        property_type=float,
                        doc_short="""The global x-component of the moment   """,
                        doc_long = """The global x-component of the moment [kNm]  (global axis)""",
                        units = """[kNm]""",
                        remarks="""global axis""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["mx"] = info


# Property: my
info = NodePropertyInfo(node_class=cls,
                        property_name="my",
                        property_type=float,
                        doc_short="""The global y-component of the moment   """,
                        doc_long = """The global y-component of the moment [kNm]  (global axis)""",
                        units = """[kNm]""",
                        remarks="""global axis""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["my"] = info


# Property: mz
info = NodePropertyInfo(node_class=cls,
                        property_name="mz",
                        property_type=float,
                        doc_short="""The global z-component of the moment   """,
                        doc_long = """The global z-component of the moment [kNm]  (global axis)""",
                        units = """[kNm]""",
                        remarks="""global axis""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["mz"] = info


# Property: is_global
info = NodePropertyInfo(node_class=cls,
                        property_name="is_global",
                        property_type=bool,
                        doc_short="""True if the force and moment are expressed in the global axis system. False if they are expressed in the local axis system, aka followers """,
                        doc_long = """True if the force and moment are expressed in the global axis system. False if they are expressed in the local axis system, aka followers [-]""",
                        units = """[-]""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["is_global"] = info


# Property: global_force
info = NodePropertyInfo(node_class=cls,
                        property_name="global_force",
                        property_type=tuple,
                        doc_short="""The force in the global axis system """,
                        doc_long = """The force in the global axis system [kN,kN,kN]""",
                        units = """[kN,kN,kN]""",
                        remarks="""""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["global_force"] = info


# Property: global_moment
info = NodePropertyInfo(node_class=cls,
                        property_name="global_moment",
                        property_type=tuple,
                        doc_short="""The moment in the global axis system """,
                        doc_long = """The moment in the global axis system [kNm,kNm,kNm]""",
                        units = """[kNm,kNm,kNm]""",
                        remarks="""""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["global_moment"] = info

# ===================== Auto-generated documentation registration for Frame
cls = DAVE_ADDITIONAL_RUNTIME_MODULES["Frame"]
DAVE_NODEPROP_INFO[cls] = dict()

# Property: inertia
info = NodePropertyInfo(node_class=cls,
                        property_name="inertia",
                        property_type=float,
                        doc_short="""The linear inertia or 'mass' of the axis """,
                        doc_long = """The linear inertia or 'mass' of the axis [mT]
        - used only for dynamics""",
                        units = """[mT]""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["inertia"] = info


# Property: inertia_position
info = NodePropertyInfo(node_class=cls,
                        property_name="inertia_position",
                        property_type=tuple,
                        doc_short="""The position of the center of inertia. Aka: "cog"  """,
                        doc_long = """The position of the center of inertia. Aka: "cog" [m,m,m] (local axis)
        - used only for dynamics
        - defined in local axis system""",
                        units = """[m,m,m]""",
                        remarks="""local axis""",
                        is_settable=True,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["inertia_position"] = info


# Property: inertia_radii
info = NodePropertyInfo(node_class=cls,
                        property_name="inertia_radii",
                        property_type=tuple,
                        doc_short="""The radii of gyration of the inertia  """,
                        doc_long = """The radii of gyration of the inertia [m,m,m] (local axis)

        Used to calculate the mass moments of inertia via

        Ixx = rxx^2 * inertia
        Iyy = rxx^2 * inertia
        Izz = rxx^2 * inertia

        Note that DAVE does not directly support cross terms in the interia matrix of an axis system. If you want to
        use cross terms then combine multiple axis system to reach the same result. This is because inertia matrices with
        diagonal terms can not be translated.
        """,
                        units = """[m,m,m]""",
                        remarks="""local axis""",
                        is_settable=True,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["inertia_radii"] = info


# Property: fixed
info = NodePropertyInfo(node_class=cls,
                        property_name="fixed",
                        property_type=tuple,
                        doc_short="""Determines which of the six degrees of freedom are fixed, if any. (x,y,z,rx,ry,rz).""",
                        doc_long = """Determines which of the six degrees of freedom are fixed, if any. (x,y,z,rx,ry,rz).
        True means that that degree of freedom will not change when solving statics.
        False means a that is may be changed in order to find equilibrium.

        These are the expressed on the coordinate system of the parent (if any) or the global axis system (if no parent)

        See Also: set_free, set_fixed
        """,
                        units = """""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["fixed"] = info


# Property: fixed_x
info = NodePropertyInfo(node_class=cls,
                        property_name="fixed_x",
                        property_type=bool,
                        doc_short="""Restricts/allows movement in x direction of parent""",
                        doc_long = """Restricts/allows movement in x direction of parent""",
                        units = """""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["fixed_x"] = info


# Property: fixed_y
info = NodePropertyInfo(node_class=cls,
                        property_name="fixed_y",
                        property_type=bool,
                        doc_short="""Restricts/allows movement in y direction of parent""",
                        doc_long = """Restricts/allows movement in y direction of parent""",
                        units = """""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["fixed_y"] = info


# Property: fixed_z
info = NodePropertyInfo(node_class=cls,
                        property_name="fixed_z",
                        property_type=bool,
                        doc_short="""Restricts/allows movement in z direction of parent""",
                        doc_long = """Restricts/allows movement in z direction of parent""",
                        units = """""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["fixed_z"] = info


# Property: fixed_rx
info = NodePropertyInfo(node_class=cls,
                        property_name="fixed_rx",
                        property_type=bool,
                        doc_short="""Restricts/allows movement about x direction of parent""",
                        doc_long = """Restricts/allows movement about x direction of parent""",
                        units = """""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["fixed_rx"] = info


# Property: fixed_ry
info = NodePropertyInfo(node_class=cls,
                        property_name="fixed_ry",
                        property_type=bool,
                        doc_short="""Restricts/allows movement about y direction of parent""",
                        doc_long = """Restricts/allows movement about y direction of parent""",
                        units = """""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["fixed_ry"] = info


# Property: fixed_rz
info = NodePropertyInfo(node_class=cls,
                        property_name="fixed_rz",
                        property_type=bool,
                        doc_short="""Restricts/allows movement about z direction of parent""",
                        doc_long = """Restricts/allows movement about z direction of parent""",
                        units = """""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["fixed_rz"] = info


# Property: x
info = NodePropertyInfo(node_class=cls,
                        property_name="x",
                        property_type=float,
                        doc_short="""The x-component of the position vector  """,
                        doc_long = """The x-component of the position vector (parent axis) [m]""",
                        units = """[m]""",
                        remarks="""parent axis""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["x"] = info


# Property: y
info = NodePropertyInfo(node_class=cls,
                        property_name="y",
                        property_type=float,
                        doc_short="""The y-component of the position vector  """,
                        doc_long = """The y-component of the position vector (parent axis) [m]""",
                        units = """[m]""",
                        remarks="""parent axis""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["y"] = info


# Property: z
info = NodePropertyInfo(node_class=cls,
                        property_name="z",
                        property_type=float,
                        doc_short="""The z-component of the position vector  """,
                        doc_long = """The z-component of the position vector (parent axis) [m]""",
                        units = """[m]""",
                        remarks="""parent axis""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["z"] = info


# Property: position
info = NodePropertyInfo(node_class=cls,
                        property_name="position",
                        property_type=tuple,
                        doc_short="""Position of the axis  """,
                        doc_long = """Position of the axis (parent axis) [m,m,m]

        These are the expressed on the coordinate system of the parent (if any) or the global axis system (if no parent)
        """,
                        units = """[m,m,m]""",
                        remarks="""parent axis""",
                        is_settable=True,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["position"] = info


# Property: rx
info = NodePropertyInfo(node_class=cls,
                        property_name="rx",
                        property_type=float,
                        doc_short="""The x-component of the rotation vector  """,
                        doc_long = """The x-component of the rotation vector [degrees] (parent axis)""",
                        units = """[degrees]""",
                        remarks="""parent axis""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["rx"] = info


# Property: ry
info = NodePropertyInfo(node_class=cls,
                        property_name="ry",
                        property_type=float,
                        doc_short="""The y-component of the rotation vector  """,
                        doc_long = """The y-component of the rotation vector [degrees] (parent axis)""",
                        units = """[degrees]""",
                        remarks="""parent axis""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["ry"] = info


# Property: rz
info = NodePropertyInfo(node_class=cls,
                        property_name="rz",
                        property_type=float,
                        doc_short="""The z-component of the rotation vector , """,
                        doc_long = """The z-component of the rotation vector [degrees], (parent axis)""",
                        units = """[degrees]""",
                        remarks="""parent axis""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["rz"] = info


# Property: rotation
info = NodePropertyInfo(node_class=cls,
                        property_name="rotation",
                        property_type=tuple,
                        doc_short="""Rotation of the frame about its origin as rotation-vector (rx,ry,rz) .""",
                        doc_long = """Rotation of the frame about its origin as rotation-vector (rx,ry,rz) [degrees].
        Defined as a rotation about an axis where the direction of the axis is (rx,ry,rz) and the angle of rotation is |(rx,ry,rz| degrees.
        These are the expressed on the coordinate system of the parent (if any) or the global axis system (if no parent)
        """,
                        units = """[degrees]""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["rotation"] = info


# Property: parent
info = NodePropertyInfo(node_class=cls,
                        property_name="parent",
                        property_type=DAVE_ADDITIONAL_RUNTIME_MODULES["Frame"],
                        doc_short="""Determines the parent of the axis. Should either be another axis or 'None'""",
                        doc_long = """Determines the parent of the axis. Should either be another axis or 'None'

        Other axis may be refered to by reference or by name (str). So the following are identical

            p = s.new_frame('parent_axis')
            c = s.new_frame('child axis')

            c.parent = p
            c.parent = 'parent_axis'

        To define that an axis does not have a parent use

            c.parent = None

        """,
                        units = """""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["parent"] = info


# Property: gx
info = NodePropertyInfo(node_class=cls,
                        property_name="gx",
                        property_type=float,
                        doc_short="""The x-component of the global position vector  """,
                        doc_long = """The x-component of the global position vector [m] (global axis )""",
                        units = """[m]""",
                        remarks="""global axis""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["gx"] = info


# Property: gy
info = NodePropertyInfo(node_class=cls,
                        property_name="gy",
                        property_type=float,
                        doc_short="""The y-component of the global position vector  """,
                        doc_long = """The y-component of the global position vector [m] (global axis )""",
                        units = """[m]""",
                        remarks="""global axis""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["gy"] = info


# Property: gz
info = NodePropertyInfo(node_class=cls,
                        property_name="gz",
                        property_type=float,
                        doc_short="""The z-component of the global position vector  """,
                        doc_long = """The z-component of the global position vector [m] (global axis )""",
                        units = """[m]""",
                        remarks="""global axis""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["gz"] = info


# Property: global_position
info = NodePropertyInfo(node_class=cls,
                        property_name="global_position",
                        property_type=tuple,
                        doc_short="""The global position of the origin of the axis system   """,
                        doc_long = """The global position of the origin of the axis system  [m,m,m] (global axis)""",
                        units = """[m,m,m]""",
                        remarks="""global axis""",
                        is_settable=True,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["global_position"] = info


# Property: grx
info = NodePropertyInfo(node_class=cls,
                        property_name="grx",
                        property_type=float,
                        doc_short="""The x-component of the global rotation vector  """,
                        doc_long = """The x-component of the global rotation vector [degrees] (global axis)""",
                        units = """[degrees]""",
                        remarks="""global axis""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["grx"] = info


# Property: gry
info = NodePropertyInfo(node_class=cls,
                        property_name="gry",
                        property_type=float,
                        doc_short="""The y-component of the global rotation vector  """,
                        doc_long = """The y-component of the global rotation vector [degrees] (global axis)""",
                        units = """[degrees]""",
                        remarks="""global axis""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["gry"] = info


# Property: grz
info = NodePropertyInfo(node_class=cls,
                        property_name="grz",
                        property_type=float,
                        doc_short="""The z-component of the global rotation vector  """,
                        doc_long = """The z-component of the global rotation vector [degrees] (global axis)""",
                        units = """[degrees]""",
                        remarks="""global axis""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["grz"] = info


# Property: tilt_x
info = NodePropertyInfo(node_class=cls,
                        property_name="tilt_x",
                        property_type=float,
                        doc_short="""Tilt about local x-axis """,
                        doc_long = """Tilt about local x-axis [deg]
        This is the arc-sin of the z-component of the unit y vector.

        See Also: heel, tilt_y
        """,
                        units = """[deg]""",
                        remarks="""""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["tilt_x"] = info


# Property: tilt_x_opposite
info = NodePropertyInfo(node_class=cls,
                        property_name="tilt_x_opposite",
                        property_type=float,
                        doc_short="""Tilt about local NEGATIVE x-axis """,
                        doc_long = """Tilt about local NEGATIVE x-axis [deg]

        See Also: heel, tilt_y, tilt_x
        """,
                        units = """[deg]""",
                        remarks="""""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["tilt_x_opposite"] = info


# Property: tilt_y_opposite
info = NodePropertyInfo(node_class=cls,
                        property_name="tilt_y_opposite",
                        property_type=float,
                        doc_short="""Tilt about local NEGATIVE y-axis """,
                        doc_long = """Tilt about local NEGATIVE y-axis [deg]

        See Also: heel, tilt_y, tilt_x
        """,
                        units = """[deg]""",
                        remarks="""""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["tilt_y_opposite"] = info


# Property: heel
info = NodePropertyInfo(node_class=cls,
                        property_name="heel",
                        property_type=float,
                        doc_short="""Heel in degrees. SB down is positive """,
                        doc_long = """Heel in degrees. SB down is positive [deg]
        This is the inverse sin of the unit y vector(= tiltx)

        See also: tilt_x
        """,
                        units = """[deg]""",
                        remarks="""""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["heel"] = info


# Property: tilt_y
info = NodePropertyInfo(node_class=cls,
                        property_name="tilt_y",
                        property_type=float,
                        doc_short="""Tilt about local y-axis """,
                        doc_long = """Tilt about local y-axis [deg]

        This is arc-sin of the z-component of the unit -x vector.
        So a positive rotation about the y axis results in a positive tilt_y.

        See Also: trim
        """,
                        units = """[deg]""",
                        remarks="""""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["tilt_y"] = info


# Property: trim
info = NodePropertyInfo(node_class=cls,
                        property_name="trim",
                        property_type=float,
                        doc_short="""Trim in degrees. Bow-down is positive """,
                        doc_long = """Trim in degrees. Bow-down is positive [deg]

        This is the inverse sin of the unit -x vector(= tilt_y)

        See also: tilt_y
        """,
                        units = """[deg]""",
                        remarks="""""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["trim"] = info


# Property: heading
info = NodePropertyInfo(node_class=cls,
                        property_name="heading",
                        property_type=float,
                        doc_short="""Direction (0..360)  of the local x-axis relative to the global x axis. Measured about the global z axis""",
                        doc_long = """Direction (0..360) [deg] of the local x-axis relative to the global x axis. Measured about the global z axis

        heading = atan(u_y,u_x)

        typically:
            heading 0  --> local axis align with global axis
            heading 90 --> local x-axis in direction of global y axis


        See also: heading_compass
        """,
                        units = """[deg]""",
                        remarks="""""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["heading"] = info


# Property: heading_compass
info = NodePropertyInfo(node_class=cls,
                        property_name="heading_compass",
                        property_type=float,
                        doc_short="""The heading (0..360) assuming that the global y-axis is North and global x-axis is East and rotation according compass definition""",
                        doc_long = """The heading (0..360)[deg] assuming that the global y-axis is North and global x-axis is East and rotation according compass definition""",
                        units = """[deg]""",
                        remarks="""""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["heading_compass"] = info


# Property: global_rotation
info = NodePropertyInfo(node_class=cls,
                        property_name="global_rotation",
                        property_type=tuple,
                        doc_short="""Rotation vector  """,
                        doc_long = """Rotation vector [deg,deg,deg] (global axis)""",
                        units = """[deg,deg,deg]""",
                        remarks="""global axis""",
                        is_settable=True,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["global_rotation"] = info


# Property: connection_force
info = NodePropertyInfo(node_class=cls,
                        property_name="connection_force",
                        property_type=tuple,
                        doc_short="""The forces and moments that this axis applies on its parent at the origin of this axis system.  """,
                        doc_long = """The forces and moments that this axis applies on its parent at the origin of this axis system. [kN, kN, kN, kNm, kNm, kNm] (Parent axis)

        If this axis would be connected to a point on its parent, and that point would be located at the location of the origin of this axis system
        then the connection force equals the force and moment applied on that point.

        Example:
            parent axis with name A
            this axis with name B
            this axis is located on A at position (10,0,0)
            there is a Point at the center of this axis system.
            A force with Fz = -10 acts on the Point.

            The connection_force is (-10,0,0,0,0,0)

            This is the force and moment as applied on A at point (10,0,0)


        """,
                        units = """[kN, kN, kN, kNm, kNm, kNm]""",
                        remarks="""Parent axis""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["connection_force"] = info


# Property: connection_force_x
info = NodePropertyInfo(node_class=cls,
                        property_name="connection_force_x",
                        property_type=float,
                        doc_short="""The x-component of the connection-force vector  """,
                        doc_long = """The x-component of the connection-force vector [kN] (Parent axis)""",
                        units = """[kN]""",
                        remarks="""Parent axis""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["connection_force_x"] = info


# Property: connection_force_y
info = NodePropertyInfo(node_class=cls,
                        property_name="connection_force_y",
                        property_type=float,
                        doc_short="""The y-component of the connection-force vector  """,
                        doc_long = """The y-component of the connection-force vector [kN] (Parent axis)""",
                        units = """[kN]""",
                        remarks="""Parent axis""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["connection_force_y"] = info


# Property: connection_force_z
info = NodePropertyInfo(node_class=cls,
                        property_name="connection_force_z",
                        property_type=float,
                        doc_short="""The z-component of the connection-force vector  """,
                        doc_long = """The z-component of the connection-force vector [kN] (Parent axis)""",
                        units = """[kN]""",
                        remarks="""Parent axis""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["connection_force_z"] = info


# Property: connection_moment_x
info = NodePropertyInfo(node_class=cls,
                        property_name="connection_moment_x",
                        property_type=float,
                        doc_short="""The mx-component of the connection-force vector  """,
                        doc_long = """The mx-component of the connection-force vector [kNm] (Parent axis)""",
                        units = """[kNm]""",
                        remarks="""Parent axis""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["connection_moment_x"] = info


# Property: connection_moment_y
info = NodePropertyInfo(node_class=cls,
                        property_name="connection_moment_y",
                        property_type=float,
                        doc_short="""The my-component of the connection-force vector  """,
                        doc_long = """The my-component of the connection-force vector [kNm] (Parent axis)""",
                        units = """[kNm]""",
                        remarks="""Parent axis""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["connection_moment_y"] = info


# Property: connection_moment_z
info = NodePropertyInfo(node_class=cls,
                        property_name="connection_moment_z",
                        property_type=float,
                        doc_short="""The mx-component of the connection-force vector  """,
                        doc_long = """The mx-component of the connection-force vector [kNm] (Parent axis)""",
                        units = """[kNm]""",
                        remarks="""Parent axis""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["connection_moment_z"] = info


# Property: applied_force
info = NodePropertyInfo(node_class=cls,
                        property_name="applied_force",
                        property_type=tuple,
                        doc_short="""The force and moment that is applied on origin of this axis  """,
                        doc_long = """The force and moment that is applied on origin of this axis [kN, kN, kN, kNm, kNm, kNm] (Global axis)""",
                        units = """[kN, kN, kN, kNm, kNm, kNm]""",
                        remarks="""Global axis""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["applied_force"] = info


# Property: ux
info = NodePropertyInfo(node_class=cls,
                        property_name="ux",
                        property_type=tuple,
                        doc_short="""The unit x axis  """,
                        doc_long = """The unit x axis [m,m,m] (Global axis)""",
                        units = """[m,m,m]""",
                        remarks="""Global axis""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["ux"] = info


# Property: uy
info = NodePropertyInfo(node_class=cls,
                        property_name="uy",
                        property_type=tuple,
                        doc_short="""The unit y axis  """,
                        doc_long = """The unit y axis [m,m,m] (Global axis)""",
                        units = """[m,m,m]""",
                        remarks="""Global axis""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["uy"] = info


# Property: uz
info = NodePropertyInfo(node_class=cls,
                        property_name="uz",
                        property_type=tuple,
                        doc_short="""The unit z axis  """,
                        doc_long = """The unit z axis [m,m,m] (Global axis)""",
                        units = """[m,m,m]""",
                        remarks="""Global axis""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["uz"] = info


# Property: equilibrium_error
info = NodePropertyInfo(node_class=cls,
                        property_name="equilibrium_error",
                        property_type=tuple,
                        doc_short="""The remaining force and moment on this axis. Should be zero when in equilibrium  """,
                        doc_long = """The remaining force and moment on this axis. Should be zero when in equilibrium [kN,kN,kN,kNm,kNm,kNm] (applied-force minus connection force, Parent axis)""",
                        units = """[kN,kN,kN,kNm,kNm,kNm]""",
                        remarks="""applied-force minus connection force, Parent axis""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["equilibrium_error"] = info

# ===================== Auto-generated documentation registration for GeometricContact
cls = DAVE_ADDITIONAL_RUNTIME_MODULES["GeometricContact"]
DAVE_NODEPROP_INFO[cls] = dict()

# Property: swivel
info = NodePropertyInfo(node_class=cls,
                        property_name="swivel",
                        property_type=float,
                        doc_short="""Swivel angle between parent and child objects """,
                        doc_long = """Swivel angle between parent and child objects [degrees]""",
                        units = """[degrees]""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["swivel"] = info


# Property: swivel_fixed
info = NodePropertyInfo(node_class=cls,
                        property_name="swivel_fixed",
                        property_type=bool,
                        doc_short="""Allow parent and child to swivel relative to eachother """,
                        doc_long = """Allow parent and child to swivel relative to eachother [boolean]""",
                        units = """[boolean]""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["swivel_fixed"] = info


# Property: rotation_on_parent
info = NodePropertyInfo(node_class=cls,
                        property_name="rotation_on_parent",
                        property_type=float,
                        doc_short="""Angle between the line connecting the centers of the circles and the axis system of the parent node """,
                        doc_long = """Angle between the line connecting the centers of the circles and the axis system of the parent node [degrees]""",
                        units = """[degrees]""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["rotation_on_parent"] = info


# Property: fixed_to_parent
info = NodePropertyInfo(node_class=cls,
                        property_name="fixed_to_parent",
                        property_type=bool,
                        doc_short="""Allow rotation around parent """,
                        doc_long = """Allow rotation around parent [boolean]

        see also: rotation_on_parent""",
                        units = """[boolean]""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["fixed_to_parent"] = info


# Property: child_rotation
info = NodePropertyInfo(node_class=cls,
                        property_name="child_rotation",
                        property_type=float,
                        doc_short="""Angle between the line connecting the centers of the circles and the axis system of the child node """,
                        doc_long = """Angle between the line connecting the centers of the circles and the axis system of the child node [degrees]""",
                        units = """[degrees]""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["child_rotation"] = info


# Property: child_fixed
info = NodePropertyInfo(node_class=cls,
                        property_name="child_fixed",
                        property_type=bool,
                        doc_short="""Allow rotation of child relative to connection, see also: child_rotation """,
                        doc_long = """Allow rotation of child relative to connection, see also: child_rotation [boolean]""",
                        units = """[boolean]""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["child_fixed"] = info


# Property: inside
info = NodePropertyInfo(node_class=cls,
                        property_name="inside",
                        property_type=bool,
                        doc_short="""Type of connection: True means child circle is inside parent circle, False means the child circle is outside but the circumferences contact """,
                        doc_long = """Type of connection: True means child circle is inside parent circle, False means the child circle is outside but the circumferences contact [boolean]""",
                        units = """[boolean]""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["inside"] = info

# ===================== Auto-generated documentation registration for HasContainer
cls = DAVE_ADDITIONAL_RUNTIME_MODULES["HasContainer"]
DAVE_NODEPROP_INFO[cls] = dict()
# ===================== Auto-generated documentation registration for HasFootprint
cls = DAVE_ADDITIONAL_RUNTIME_MODULES["HasFootprint"]
DAVE_NODEPROP_INFO[cls] = dict()

# Property: footprint
info = NodePropertyInfo(node_class=cls,
                        property_name="footprint",
                        property_type=tuple,
                        doc_short="""Determines where on its parent the force of this node is applied.""",
                        doc_long = """Determines where on its parent the force of this node is applied.
        Tuple of tuples ((x1,y1,z1), (x2,y2,z2), .... (xn,yn,zn))""",
                        units = """""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["footprint"] = info

# ===================== Auto-generated documentation registration for HasParent
cls = DAVE_ADDITIONAL_RUNTIME_MODULES["HasParent"]
DAVE_NODEPROP_INFO[cls] = dict()

# Property: parents
info = NodePropertyInfo(node_class=cls,
                        property_name="parents",
                        property_type=tuple,
                        doc_short="""Returns a tuple of all parents of this node""",
                        doc_long = """Returns a tuple of all parents of this node""",
                        units = """""",
                        remarks="""""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["parents"] = info


# Property: parent
info = NodePropertyInfo(node_class=cls,
                        property_name="parent",
                        property_type=DAVE_ADDITIONAL_RUNTIME_MODULES["Node"],
                        doc_short="""The node that this node is located on, if any """,
                        doc_long = """The node that this node is located on, if any [Node]""",
                        units = """[Node]""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["parent"] = info

# ===================== Auto-generated documentation registration for HasSubScene
cls = DAVE_ADDITIONAL_RUNTIME_MODULES["HasSubScene"]
DAVE_NODEPROP_INFO[cls] = dict()

# Property: path
info = NodePropertyInfo(node_class=cls,
                        property_name="path",
                        property_type=str,
                        doc_short="""Path of the model-file. For example res: padeye.dave""",
                        doc_long = """Path of the model-file. For example res: padeye.dave""",
                        units = """""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["path"] = info


# Property: exposed_properties
info = NodePropertyInfo(node_class=cls,
                        property_name="exposed_properties",
                        property_type=tuple,
                        doc_short="""Names of exposed properties""",
                        doc_long = """Names of exposed properties""",
                        units = """""",
                        remarks="""""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["exposed_properties"] = info

# ===================== Auto-generated documentation registration for HasTrimesh
cls = DAVE_ADDITIONAL_RUNTIME_MODULES["HasTrimesh"]
DAVE_NODEPROP_INFO[cls] = dict()
# ===================== Auto-generated documentation registration for HydSpring
cls = DAVE_ADDITIONAL_RUNTIME_MODULES["HydSpring"]
DAVE_NODEPROP_INFO[cls] = dict()

# Property: cob
info = NodePropertyInfo(node_class=cls,
                        property_name="cob",
                        property_type=tuple,
                        doc_short="""Center of buoyancy in  """,
                        doc_long = """Center of buoyancy in (parent axis) [m,m,m]""",
                        units = """[m,m,m]""",
                        remarks="""parent axis""",
                        is_settable=True,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["cob"] = info


# Property: BMT
info = NodePropertyInfo(node_class=cls,
                        property_name="BMT",
                        property_type=float,
                        doc_short="""Vertical distance between cob and metacenter for roll """,
                        doc_long = """Vertical distance between cob and metacenter for roll [m]""",
                        units = """[m]""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["BMT"] = info


# Property: BML
info = NodePropertyInfo(node_class=cls,
                        property_name="BML",
                        property_type=float,
                        doc_short="""Vertical distance between cob and metacenter for pitch """,
                        doc_long = """Vertical distance between cob and metacenter for pitch [m]""",
                        units = """[m]""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["BML"] = info


# Property: COFX
info = NodePropertyInfo(node_class=cls,
                        property_name="COFX",
                        property_type=float,
                        doc_short="""Horizontal x-position Center of Floatation (center of waterplane area), relative to cob """,
                        doc_long = """Horizontal x-position Center of Floatation (center of waterplane area), relative to cob [m]""",
                        units = """[m]""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["COFX"] = info


# Property: COFY
info = NodePropertyInfo(node_class=cls,
                        property_name="COFY",
                        property_type=float,
                        doc_short="""Horizontal y-position Center of Floatation (center of waterplane area), relative to cob """,
                        doc_long = """Horizontal y-position Center of Floatation (center of waterplane area), relative to cob [m]""",
                        units = """[m]""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["COFY"] = info


# Property: kHeave
info = NodePropertyInfo(node_class=cls,
                        property_name="kHeave",
                        property_type=float,
                        doc_short="""Heave stiffness """,
                        doc_long = """Heave stiffness [kN/m]""",
                        units = """[kN/m]""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["kHeave"] = info


# Property: waterline
info = NodePropertyInfo(node_class=cls,
                        property_name="waterline",
                        property_type=float,
                        doc_short="""Waterline-elevation relative to cob for un-stretched heave-spring. Positive if cob is below the waterline  """,
                        doc_long = """Waterline-elevation relative to cob for un-stretched heave-spring. Positive if cob is below the waterline (which is where is normally is) [m]""",
                        units = """[m]""",
                        remarks="""which is where is normally is""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["waterline"] = info


# Property: displacement_kN
info = NodePropertyInfo(node_class=cls,
                        property_name="displacement_kN",
                        property_type=float,
                        doc_short="""Displacement when waterline is at waterline-elevation """,
                        doc_long = """Displacement when waterline is at waterline-elevation [kN]""",
                        units = """[kN]""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["displacement_kN"] = info

# ===================== Auto-generated documentation registration for LC6d
cls = DAVE_ADDITIONAL_RUNTIME_MODULES["LC6d"]
DAVE_NODEPROP_INFO[cls] = dict()

# Property: stiffness
info = NodePropertyInfo(node_class=cls,
                        property_name="stiffness",
                        property_type=tuple,
                        doc_short="""Stiffness of the connector: kx, ky, kz, krx, kry, krz in  """,
                        doc_long = """Stiffness of the connector: kx, ky, kz, krx, kry, krz in [kN/m and kNm/rad] (axis system of the main axis)""",
                        units = """[kN/m and kNm/rad]""",
                        remarks="""axis system of the main axis""",
                        is_settable=True,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["stiffness"] = info


# Property: fgx
info = NodePropertyInfo(node_class=cls,
                        property_name="fgx",
                        property_type=float,
                        doc_short="""Force on main in global coordinate frame """,
                        doc_long = """Force on main in global coordinate frame [kN]""",
                        units = """[kN]""",
                        remarks="""""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["fgx"] = info


# Property: fgy
info = NodePropertyInfo(node_class=cls,
                        property_name="fgy",
                        property_type=float,
                        doc_short="""Force on main in global coordinate frame """,
                        doc_long = """Force on main in global coordinate frame [kN]""",
                        units = """[kN]""",
                        remarks="""""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["fgy"] = info


# Property: fgz
info = NodePropertyInfo(node_class=cls,
                        property_name="fgz",
                        property_type=float,
                        doc_short="""Force on main in global coordinate frame """,
                        doc_long = """Force on main in global coordinate frame [kN]""",
                        units = """[kN]""",
                        remarks="""""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["fgz"] = info


# Property: force_global
info = NodePropertyInfo(node_class=cls,
                        property_name="force_global",
                        property_type=tuple,
                        doc_short="""Force on main in global coordinate frame """,
                        doc_long = """Force on main in global coordinate frame [kN,kN,kN,kNm,kNm,kNm]""",
                        units = """[kN,kN,kN,kNm,kNm,kNm]""",
                        remarks="""""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["force_global"] = info


# Property: mgx
info = NodePropertyInfo(node_class=cls,
                        property_name="mgx",
                        property_type=float,
                        doc_short="""Moment on main in global coordinate frame """,
                        doc_long = """Moment on main in global coordinate frame [kNm]""",
                        units = """[kNm]""",
                        remarks="""""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["mgx"] = info


# Property: mgy
info = NodePropertyInfo(node_class=cls,
                        property_name="mgy",
                        property_type=float,
                        doc_short="""Moment on main in global coordinate frame """,
                        doc_long = """Moment on main in global coordinate frame [kNm]""",
                        units = """[kNm]""",
                        remarks="""""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["mgy"] = info


# Property: mgz
info = NodePropertyInfo(node_class=cls,
                        property_name="mgz",
                        property_type=float,
                        doc_short="""Moment on main in global coordinate frame """,
                        doc_long = """Moment on main in global coordinate frame [kNm]""",
                        units = """[kNm]""",
                        remarks="""""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["mgz"] = info


# Property: moment_global
info = NodePropertyInfo(node_class=cls,
                        property_name="moment_global",
                        property_type=tuple,
                        doc_short="""Moment on main in global coordinate frame """,
                        doc_long = """Moment on main in global coordinate frame [kNm, kNm, kNm]""",
                        units = """[kNm, kNm, kNm]""",
                        remarks="""""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["moment_global"] = info

# ===================== Auto-generated documentation registration for Manager
cls = DAVE_ADDITIONAL_RUNTIME_MODULES["Manager"]
DAVE_NODEPROP_INFO[cls] = dict()
# ===================== Auto-generated documentation registration for Node
cls = DAVE_ADDITIONAL_RUNTIME_MODULES["Node"]
DAVE_NODEPROP_INFO[cls] = dict()

# Property: name
info = NodePropertyInfo(node_class=cls,
                        property_name="name",
                        property_type=str,
                        doc_short="""Name of the node """,
                        doc_long = """Name of the node [str]""",
                        units = """[str]""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["name"] = info


# Property: visible
info = NodePropertyInfo(node_class=cls,
                        property_name="visible",
                        property_type=bool,
                        doc_short="""Determines if this node is visible in the viewport """,
                        doc_long = """Determines if this node is visible in the viewport [bool]""",
                        units = """[bool]""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["visible"] = info


# Property: UC
info = NodePropertyInfo(node_class=cls,
                        property_name="UC",
                        property_type=float,
                        doc_short="""Returns the governing UC of the node, returns None is no limits are defined """,
                        doc_long = """Returns the governing UC of the node, returns None is no limits are defined [-]

        See Also: give_UC, UC_governing_details
        """,
                        units = """[-]""",
                        remarks="""""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["UC"] = info


# Property: UC_governing_details
info = NodePropertyInfo(node_class=cls,
                        property_name="UC_governing_details",
                        property_type=tuple,
                        doc_short="""Returns the details of the governing UC for this node :""",
                        doc_long = """Returns the details of the governing UC for this node [-, name, limit value, actual value]:
        0: UC,
        1: property-name,
        2: property-limits
        3: property value

        Returns (None, None, None, None) if no limits are supplied
        """,
                        units = """[-, name, limit value, actual value]""",
                        remarks="""""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["UC_governing_details"] = info


# Property: tags
info = NodePropertyInfo(node_class=cls,
                        property_name="tags",
                        property_type=tuple,
                        doc_short="""All tags of this node """,
                        doc_long = """All tags of this node (tuple of str)""",
                        units = """""",
                        remarks="""tuple of str""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["tags"] = info

# ===================== Auto-generated documentation registration for NodeCoreConnected
cls = DAVE_ADDITIONAL_RUNTIME_MODULES["NodeCoreConnected"]
DAVE_NODEPROP_INFO[cls] = dict()

# Property: name
info = NodePropertyInfo(node_class=cls,
                        property_name="name",
                        property_type=str,
                        doc_short="""Name of the node (str), must be unique""",
                        doc_long = """Name of the node (str), must be unique""",
                        units = """""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["name"] = info

# ===================== Auto-generated documentation registration for NodePurePython
cls = DAVE_ADDITIONAL_RUNTIME_MODULES["NodePurePython"]
DAVE_NODEPROP_INFO[cls] = dict()

# Property: name
info = NodePropertyInfo(node_class=cls,
                        property_name="name",
                        property_type=str,
                        doc_short="""Name of the node (str), must be unique """,
                        doc_long = """Name of the node (str), must be unique [str]""",
                        units = """[str]""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["name"] = info

# ===================== Auto-generated documentation registration for Point
cls = DAVE_ADDITIONAL_RUNTIME_MODULES["Point"]
DAVE_NODEPROP_INFO[cls] = dict()

# Property: x
info = NodePropertyInfo(node_class=cls,
                        property_name="x",
                        property_type=float,
                        doc_short="""x component of local position  """,
                        doc_long = """x component of local position [m] (parent axis)""",
                        units = """[m]""",
                        remarks="""parent axis""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["x"] = info


# Property: y
info = NodePropertyInfo(node_class=cls,
                        property_name="y",
                        property_type=float,
                        doc_short="""y component of local position  """,
                        doc_long = """y component of local position [m] (parent axis)""",
                        units = """[m]""",
                        remarks="""parent axis""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["y"] = info


# Property: z
info = NodePropertyInfo(node_class=cls,
                        property_name="z",
                        property_type=float,
                        doc_short="""z component of local position  """,
                        doc_long = """z component of local position [m] (parent axis)""",
                        units = """[m]""",
                        remarks="""parent axis""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["z"] = info


# Property: applied_force
info = NodePropertyInfo(node_class=cls,
                        property_name="applied_force",
                        property_type=tuple,
                        doc_short="""Applied force  """,
                        doc_long = """Applied force [kN,kN,kN] (parent axis)""",
                        units = """[kN,kN,kN]""",
                        remarks="""parent axis""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["applied_force"] = info


# Property: force
info = NodePropertyInfo(node_class=cls,
                        property_name="force",
                        property_type=float,
                        doc_short="""total force magnitude as applied on the point """,
                        doc_long = """total force magnitude as applied on the point [kN]""",
                        units = """[kN]""",
                        remarks="""""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["force"] = info


# Property: fx
info = NodePropertyInfo(node_class=cls,
                        property_name="fx",
                        property_type=float,
                        doc_short="""x component of applied force  """,
                        doc_long = """x component of applied force [kN] (parent axis)""",
                        units = """[kN]""",
                        remarks="""parent axis""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["fx"] = info


# Property: fy
info = NodePropertyInfo(node_class=cls,
                        property_name="fy",
                        property_type=float,
                        doc_short="""y component of applied force  """,
                        doc_long = """y component of applied force [kN] (parent axis)""",
                        units = """[kN]""",
                        remarks="""parent axis""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["fy"] = info


# Property: fz
info = NodePropertyInfo(node_class=cls,
                        property_name="fz",
                        property_type=float,
                        doc_short="""z component of applied force  """,
                        doc_long = """z component of applied force [kN] (parent axis)""",
                        units = """[kN]""",
                        remarks="""parent axis""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["fz"] = info


# Property: applied_moment
info = NodePropertyInfo(node_class=cls,
                        property_name="applied_moment",
                        property_type=tuple,
                        doc_short="""Applied moment  """,
                        doc_long = """Applied moment [kNm,kNm,kNm] (parent axis)""",
                        units = """[kNm,kNm,kNm]""",
                        remarks="""parent axis""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["applied_moment"] = info


# Property: moment
info = NodePropertyInfo(node_class=cls,
                        property_name="moment",
                        property_type=float,
                        doc_short="""total moment magnitude as applied on the point """,
                        doc_long = """total moment magnitude as applied on the point [kNm]""",
                        units = """[kNm]""",
                        remarks="""""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["moment"] = info


# Property: mx
info = NodePropertyInfo(node_class=cls,
                        property_name="mx",
                        property_type=float,
                        doc_short="""x component of applied moment  """,
                        doc_long = """x component of applied moment [kNm] (parent axis)""",
                        units = """[kNm]""",
                        remarks="""parent axis""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["mx"] = info


# Property: my
info = NodePropertyInfo(node_class=cls,
                        property_name="my",
                        property_type=float,
                        doc_short="""y component of applied moment  """,
                        doc_long = """y component of applied moment [kNm] (parent axis)""",
                        units = """[kNm]""",
                        remarks="""parent axis""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["my"] = info


# Property: mz
info = NodePropertyInfo(node_class=cls,
                        property_name="mz",
                        property_type=float,
                        doc_short="""z component of applied moment  """,
                        doc_long = """z component of applied moment [kNm] (parent axis)""",
                        units = """[kNm]""",
                        remarks="""parent axis""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["mz"] = info


# Property: position
info = NodePropertyInfo(node_class=cls,
                        property_name="position",
                        property_type=tuple,
                        doc_short="""Local position  """,
                        doc_long = """Local position [m,m,m] (parent axis)""",
                        units = """[m,m,m]""",
                        remarks="""parent axis""",
                        is_settable=True,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["position"] = info


# Property: applied_force_and_moment_global
info = NodePropertyInfo(node_class=cls,
                        property_name="applied_force_and_moment_global",
                        property_type=tuple,
                        doc_short="""Applied force and moment on this point  """,
                        doc_long = """Applied force and moment on this point [kN, kN, kN, kNm, kNm, kNm] (Global axis)""",
                        units = """[kN, kN, kN, kNm, kNm, kNm]""",
                        remarks="""Global axis""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["applied_force_and_moment_global"] = info


# Property: gx
info = NodePropertyInfo(node_class=cls,
                        property_name="gx",
                        property_type=float,
                        doc_short="""x component of position  """,
                        doc_long = """x component of position [m] (global axis)""",
                        units = """[m]""",
                        remarks="""global axis""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["gx"] = info


# Property: gy
info = NodePropertyInfo(node_class=cls,
                        property_name="gy",
                        property_type=float,
                        doc_short="""y component of position  """,
                        doc_long = """y component of position [m] (global axis)""",
                        units = """[m]""",
                        remarks="""global axis""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["gy"] = info


# Property: gz
info = NodePropertyInfo(node_class=cls,
                        property_name="gz",
                        property_type=float,
                        doc_short="""z component of position  """,
                        doc_long = """z component of position [m] (global axis)""",
                        units = """[m]""",
                        remarks="""global axis""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["gz"] = info


# Property: global_position
info = NodePropertyInfo(node_class=cls,
                        property_name="global_position",
                        property_type=tuple,
                        doc_short="""Global position  """,
                        doc_long = """Global position [m,m,m] (global axis)""",
                        units = """[m,m,m]""",
                        remarks="""global axis""",
                        is_settable=True,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["global_position"] = info

# ===================== Auto-generated documentation registration for RigidBody
cls = DAVE_ADDITIONAL_RUNTIME_MODULES["RigidBody"]
DAVE_NODEPROP_INFO[cls] = dict()

# Property: footprint
info = NodePropertyInfo(node_class=cls,
                        property_name="footprint",
                        property_type=tuple,
                        doc_short="""Sets the footprint vertices. Supply as an iterable with each element containing three floats""",
                        doc_long = """Sets the footprint vertices. Supply as an iterable with each element containing three floats""",
                        units = """""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["footprint"] = info


# Property: cogx
info = NodePropertyInfo(node_class=cls,
                        property_name="cogx",
                        property_type=float,
                        doc_short="""x-component of cog position  """,
                        doc_long = """x-component of cog position [m] (local axis)""",
                        units = """[m]""",
                        remarks="""local axis""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["cogx"] = info


# Property: cogy
info = NodePropertyInfo(node_class=cls,
                        property_name="cogy",
                        property_type=float,
                        doc_short="""y-component of cog position  """,
                        doc_long = """y-component of cog position [m] (local axis)""",
                        units = """[m]""",
                        remarks="""local axis""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["cogy"] = info


# Property: cogz
info = NodePropertyInfo(node_class=cls,
                        property_name="cogz",
                        property_type=float,
                        doc_short="""z-component of cog position  """,
                        doc_long = """z-component of cog position [m] (local axis)""",
                        units = """[m]""",
                        remarks="""local axis""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["cogz"] = info


# Property: cog
info = NodePropertyInfo(node_class=cls,
                        property_name="cog",
                        property_type=tuple,
                        doc_short="""Center of Gravity position  """,
                        doc_long = """Center of Gravity position [m,m,m] (local axis)""",
                        units = """[m,m,m]""",
                        remarks="""local axis""",
                        is_settable=True,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["cog"] = info


# Property: mass
info = NodePropertyInfo(node_class=cls,
                        property_name="mass",
                        property_type=float,
                        doc_short="""Static mass of the body """,
                        doc_long = """Static mass of the body [mT]

        See Also: inertia
        """,
                        units = """[mT]""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["mass"] = info

# ===================== Auto-generated documentation registration for RigidBodyContainer
cls = DAVE_ADDITIONAL_RUNTIME_MODULES["RigidBodyContainer"]
DAVE_NODEPROP_INFO[cls] = dict()
# ===================== Auto-generated documentation registration for SPMT
cls = DAVE_ADDITIONAL_RUNTIME_MODULES["SPMT"]
DAVE_NODEPROP_INFO[cls] = dict()

# Property: force
info = NodePropertyInfo(node_class=cls,
                        property_name="force",
                        property_type=tuple,
                        doc_short="""Returns the force component perpendicular to the SPMT in each of the axles  """,
                        doc_long = """Returns the force component perpendicular to the SPMT in each of the axles (negative mean uplift) [kN]""",
                        units = """[kN]""",
                        remarks="""negative mean uplift""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["force"] = info


# Property: contact_force
info = NodePropertyInfo(node_class=cls,
                        property_name="contact_force",
                        property_type=tuple,
                        doc_short="""Returns the contact force in each of the axles  """,
                        doc_long = """Returns the contact force in each of the axles (global) [kN,kN,kN]""",
                        units = """[kN,kN,kN]""",
                        remarks="""global""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["contact_force"] = info


# Property: compression
info = NodePropertyInfo(node_class=cls,
                        property_name="compression",
                        property_type=float,
                        doc_short="""Returns the total compression  """,
                        doc_long = """Returns the total compression (negative means uplift) [m]""",
                        units = """[m]""",
                        remarks="""negative means uplift""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["compression"] = info


# Property: extensions
info = NodePropertyInfo(node_class=cls,
                        property_name="extensions",
                        property_type=tuple,
                        doc_short="""Returns the extension of each of the axles  """,
                        doc_long = """Returns the extension of each of the axles (bottom of wheel to top of spmt) [m]""",
                        units = """[m]""",
                        remarks="""bottom of wheel to top of spmt""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["extensions"] = info


# Property: max_extension
info = NodePropertyInfo(node_class=cls,
                        property_name="max_extension",
                        property_type=float,
                        doc_short="""Maximum extension of the axles """,
                        doc_long = """Maximum extension of the axles [m]
        See Also: extensions""",
                        units = """[m]""",
                        remarks="""""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["max_extension"] = info


# Property: min_extension
info = NodePropertyInfo(node_class=cls,
                        property_name="min_extension",
                        property_type=float,
                        doc_short="""Minimum extension of the axles """,
                        doc_long = """Minimum extension of the axles [m]
        See Also: extensions""",
                        units = """[m]""",
                        remarks="""""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["min_extension"] = info


# Property: n_width
info = NodePropertyInfo(node_class=cls,
                        property_name="n_width",
                        property_type=int,
                        doc_short="""number of axles in transverse direction """,
                        doc_long = """number of axles in transverse direction [-]""",
                        units = """[-]""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["n_width"] = info


# Property: n_length
info = NodePropertyInfo(node_class=cls,
                        property_name="n_length",
                        property_type=int,
                        doc_short="""number of axles in length direction """,
                        doc_long = """number of axles in length direction [-]""",
                        units = """[-]""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["n_length"] = info


# Property: spacing_width
info = NodePropertyInfo(node_class=cls,
                        property_name="spacing_width",
                        property_type=float,
                        doc_short="""distance between axles in transverse direction """,
                        doc_long = """distance between axles in transverse direction [m]""",
                        units = """[m]""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["spacing_width"] = info


# Property: spacing_length
info = NodePropertyInfo(node_class=cls,
                        property_name="spacing_length",
                        property_type=float,
                        doc_short="""distance between axles in length direction """,
                        doc_long = """distance between axles in length direction [m]""",
                        units = """[m]""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["spacing_length"] = info


# Property: reference_force
info = NodePropertyInfo(node_class=cls,
                        property_name="reference_force",
                        property_type=float,
                        doc_short="""total force (sum of all axles) when at reference extension """,
                        doc_long = """total force (sum of all axles) when at reference extension [kN]""",
                        units = """[kN]""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["reference_force"] = info


# Property: reference_extension
info = NodePropertyInfo(node_class=cls,
                        property_name="reference_extension",
                        property_type=float,
                        doc_short="""Distance between top of SPMT and bottom of wheel at which compression is zero """,
                        doc_long = """Distance between top of SPMT and bottom of wheel at which compression is zero [m]""",
                        units = """[m]""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["reference_extension"] = info


# Property: k
info = NodePropertyInfo(node_class=cls,
                        property_name="k",
                        property_type=float,
                        doc_short="""Vertical stiffness of all axles together """,
                        doc_long = """Vertical stiffness of all axles together [kN/m]""",
                        units = """[kN/m]""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["k"] = info


# Property: use_friction
info = NodePropertyInfo(node_class=cls,
                        property_name="use_friction",
                        property_type=bool,
                        doc_short="""Apply friction between wheel and surface such that resulting force is vertical """,
                        doc_long = """Apply friction between wheel and surface such that resulting force is vertical [True/False]
        False: Force is perpendicular to the surface
        True: Force is vertical
        """,
                        units = """[True/False]""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["use_friction"] = info


# Property: meshes
info = NodePropertyInfo(node_class=cls,
                        property_name="meshes",
                        property_type=tuple,
                        doc_short="""List of contact-mesh nodes. If empty list then the SPMT can contact all contact meshes.""",
                        doc_long = """List of contact-mesh nodes. If empty list then the SPMT can contact all contact meshes.
        When getting this will yield a list of node references.
        When setting node references and node-names may be used.

        eg: ball.meshes = [mesh1, 'mesh2']
        """,
                        units = """""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["meshes"] = info


# Property: meshes_names
info = NodePropertyInfo(node_class=cls,
                        property_name="meshes_names",
                        property_type=tuple,
                        doc_short="""List with the names of the meshes""",
                        doc_long = """List with the names of the meshes""",
                        units = """""",
                        remarks="""""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["meshes_names"] = info


# Property: axles
info = NodePropertyInfo(node_class=cls,
                        property_name="axles",
                        property_type=tuple,
                        doc_short="""Axles is a list axle positions  """,
                        doc_long = """Axles is a list axle positions [m,m,m] (parent axis)
        Each entry is a (x,y,z) entry which determines the location of the axle on SPMT. This is relative to the parent of the SPMT.

        Example:
            [(-10,0,0),(-5,0,0),(0,0,0)] for three axles
        """,
                        units = """[m,m,m]""",
                        remarks="""parent axis""",
                        is_settable=True,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["axles"] = info

# ===================== Auto-generated documentation registration for Tank
cls = DAVE_ADDITIONAL_RUNTIME_MODULES["Tank"]
DAVE_NODEPROP_INFO[cls] = dict()

# Property: free_flooding
info = NodePropertyInfo(node_class=cls,
                        property_name="free_flooding",
                        property_type=bool,
                        doc_short="""Tank is filled till global waterline  """,
                        doc_long = """Tank is filled till global waterline (aka: damaged) [bool]""",
                        units = """[bool]""",
                        remarks="""aka: damaged""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["free_flooding"] = info


# Property: permeability
info = NodePropertyInfo(node_class=cls,
                        property_name="permeability",
                        property_type=float,
                        doc_short="""Permeability is the fraction of the meshed volume that can be filled with fluid """,
                        doc_long = """Permeability is the fraction of the meshed volume that can be filled with fluid [-]""",
                        units = """[-]""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["permeability"] = info


# Property: cog
info = NodePropertyInfo(node_class=cls,
                        property_name="cog",
                        property_type=tuple,
                        doc_short="""Global position of the center of volume / gravity  """,
                        doc_long = """Global position of the center of volume / gravity [m,m,m] (global)""",
                        units = """[m,m,m]""",
                        remarks="""global""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["cog"] = info


# Property: cog_local
info = NodePropertyInfo(node_class=cls,
                        property_name="cog_local",
                        property_type=tuple,
                        doc_short="""Center of gravity  """,
                        doc_long = """Center of gravity [m,m,m] (parent axis)""",
                        units = """[m,m,m]""",
                        remarks="""parent axis""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["cog_local"] = info


# Property: cog_when_full_global
info = NodePropertyInfo(node_class=cls,
                        property_name="cog_when_full_global",
                        property_type=tuple,
                        doc_short="""Global position of the center of volume / gravity of the tank when it is filled  """,
                        doc_long = """Global position of the center of volume / gravity of the tank when it is filled [m,m,m] (global)""",
                        units = """[m,m,m]""",
                        remarks="""global""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["cog_when_full_global"] = info


# Property: cog_when_full
info = NodePropertyInfo(node_class=cls,
                        property_name="cog_when_full",
                        property_type=tuple,
                        doc_short="""LOCAL position of the center of volume / gravity of the tank when it is filled  """,
                        doc_long = """LOCAL position of the center of volume / gravity of the tank when it is filled [m,m,m] (parent axis)""",
                        units = """[m,m,m]""",
                        remarks="""parent axis""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["cog_when_full"] = info


# Property: cogx_when_full
info = NodePropertyInfo(node_class=cls,
                        property_name="cogx_when_full",
                        property_type=float,
                        doc_short="""x position of the center of volume / gravity of the tank when it is filled  """,
                        doc_long = """x position of the center of volume / gravity of the tank when it is filled [m] (parent axis)""",
                        units = """[m]""",
                        remarks="""parent axis""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["cogx_when_full"] = info


# Property: cogy_when_full
info = NodePropertyInfo(node_class=cls,
                        property_name="cogy_when_full",
                        property_type=float,
                        doc_short="""y position of the center of volume / gravity of the tank when it is filled  """,
                        doc_long = """y position of the center of volume / gravity of the tank when it is filled [m] (parent axis)""",
                        units = """[m]""",
                        remarks="""parent axis""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["cogy_when_full"] = info


# Property: cogz_when_full
info = NodePropertyInfo(node_class=cls,
                        property_name="cogz_when_full",
                        property_type=float,
                        doc_short="""z position of the center of volume / gravity of the tank when it is filled  """,
                        doc_long = """z position of the center of volume / gravity of the tank when it is filled [m] (parent axis)""",
                        units = """[m]""",
                        remarks="""parent axis""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["cogz_when_full"] = info


# Property: fill_pct
info = NodePropertyInfo(node_class=cls,
                        property_name="fill_pct",
                        property_type=float,
                        doc_short="""Amount of volume in tank as percentage of capacity """,
                        doc_long = """Amount of volume in tank as percentage of capacity [%]""",
                        units = """[%]""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["fill_pct"] = info


# Property: level_global
info = NodePropertyInfo(node_class=cls,
                        property_name="level_global",
                        property_type=float,
                        doc_short="""The fluid plane elevation in the global axis system """,
                        doc_long = """The fluid plane elevation in the global axis system [m]
        Setting this adjusts the volume""",
                        units = """[m]""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["level_global"] = info


# Property: volume
info = NodePropertyInfo(node_class=cls,
                        property_name="volume",
                        property_type=float,
                        doc_short="""The actual volume of fluid in the tank """,
                        doc_long = """The actual volume of fluid in the tank [m3]
        Setting this adjusts the fluid level""",
                        units = """[m3]""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["volume"] = info


# Property: used_density
info = NodePropertyInfo(node_class=cls,
                        property_name="used_density",
                        property_type=float,
                        doc_short="""Density of the fluid in the tank """,
                        doc_long = """Density of the fluid in the tank [mT/m3]""",
                        units = """[mT/m3]""",
                        remarks="""""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["used_density"] = info


# Property: density
info = NodePropertyInfo(node_class=cls,
                        property_name="density",
                        property_type=float,
                        doc_short="""Density of the fluid in the tank. Density < 0 means use outside water density. See also used_density """,
                        doc_long = """Density of the fluid in the tank. Density < 0 means use outside water density. See also used_density [mT/m3]""",
                        units = """[mT/m3]""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["density"] = info


# Property: capacity
info = NodePropertyInfo(node_class=cls,
                        property_name="capacity",
                        property_type=float,
                        doc_short="""Fillable volume of the tank calcualted as mesh volume times permeability """,
                        doc_long = """Fillable volume of the tank calcualted as mesh volume times permeability [m3]
        This is calculated from the defined geometry and permeability.
        See also: mesh_volume""",
                        units = """[m3]""",
                        remarks="""""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["capacity"] = info


# Property: mesh_volume
info = NodePropertyInfo(node_class=cls,
                        property_name="mesh_volume",
                        property_type=float,
                        doc_short="""Volume enclosed by the mesh the tank """,
                        doc_long = """Volume enclosed by the mesh the tank [m3]
        This is calculated from the defined geometry and does not account for permeability.
        See also: capacity""",
                        units = """[m3]""",
                        remarks="""""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["mesh_volume"] = info


# Property: ullage
info = NodePropertyInfo(node_class=cls,
                        property_name="ullage",
                        property_type=float,
                        doc_short="""Ullage of the tank """,
                        doc_long = """Ullage of the tank [m]
        The ullage is the distance between a measurement point and the fluid surface. The point is [xf,yf,zv] where
        xf and yf are the x and y coordinates (local) of the center of fluid when the tank is full. zv is the largest z value
        of all the vertices of the tank.
        The measurement direction is in local z-direction. If the tank is under an angle then this is not perpendicular to the fluid.
        It is possible that this definition results in an ullage larger than the physical tank depth. In that case the physical depth of
        the tank is returned instead.
        """,
                        units = """[m]""",
                        remarks="""""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["ullage"] = info


# Property: sounding
info = NodePropertyInfo(node_class=cls,
                        property_name="sounding",
                        property_type=float,
                        doc_short="""Sounding of the tank """,
                        doc_long = """Sounding of the tank [m]
        The sounding is the distance between a measurement point and the fluid surface. The point is [xf,yf,zv] where
        xf and yf are the x and y coordinates (local) of the center of fluid when the tank is full. zv is the lowest z value
        of all the vertices of the tank.
        The measurement direction is in local z-direction. If the tank is under an angle then this is not perpendicular to the fluid.
        It is possible that this definition results in a sounding larger than the physical tank depth. In that case the physical depth of
        the tank is returned instead.
        """,
                        units = """[m]""",
                        remarks="""""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["sounding"] = info

# ===================== Auto-generated documentation registration for Visual
cls = DAVE_ADDITIONAL_RUNTIME_MODULES["Visual"]
DAVE_NODEPROP_INFO[cls] = dict()

# Property: path
info = NodePropertyInfo(node_class=cls,
                        property_name="path",
                        property_type=str,
                        doc_short="""Resource path or url to the visual """,
                        doc_long = """Resource path or url to the visual (str)""",
                        units = """""",
                        remarks="""str""",
                        is_settable=True,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["path"] = info

# ===================== Auto-generated documentation registration for WaveInteraction1
cls = DAVE_ADDITIONAL_RUNTIME_MODULES["WaveInteraction1"]
DAVE_NODEPROP_INFO[cls] = dict()
# ===================== Auto-generated documentation registration for WindArea
cls = DAVE_ADDITIONAL_RUNTIME_MODULES["WindArea"]
DAVE_NODEPROP_INFO[cls] = dict()
# ===================== Auto-generated documentation registration for WindOrCurrentArea
cls = DAVE_ADDITIONAL_RUNTIME_MODULES["WindOrCurrentArea"]
DAVE_NODEPROP_INFO[cls] = dict()

# Property: force
info = NodePropertyInfo(node_class=cls,
                        property_name="force",
                        property_type=tuple,
                        doc_short="""The x,y and z components of the force  """,
                        doc_long = """The x,y and z components of the force [kN,kN,kN] (global axis)""",
                        units = """[kN,kN,kN]""",
                        remarks="""global axis""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["force"] = info


# Property: fx
info = NodePropertyInfo(node_class=cls,
                        property_name="fx",
                        property_type=float,
                        doc_short="""The global x-component of the force  """,
                        doc_long = """The global x-component of the force [kN] (global axis)""",
                        units = """[kN]""",
                        remarks="""global axis""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["fx"] = info


# Property: fy
info = NodePropertyInfo(node_class=cls,
                        property_name="fy",
                        property_type=float,
                        doc_short="""The global y-component of the force   """,
                        doc_long = """The global y-component of the force [kN]  (global axis)""",
                        units = """[kN]""",
                        remarks="""global axis""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["fy"] = info


# Property: fz
info = NodePropertyInfo(node_class=cls,
                        property_name="fz",
                        property_type=float,
                        doc_short="""The global z-component of the force   """,
                        doc_long = """The global z-component of the force [kN]  (global axis)""",
                        units = """[kN]""",
                        remarks="""global axis""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["fz"] = info


# Property: A
info = NodePropertyInfo(node_class=cls,
                        property_name="A",
                        property_type=float,
                        doc_short="""Total area . See also Ae""",
                        doc_long = """Total area [m2]. See also Ae""",
                        units = """[m2]""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["A"] = info


# Property: Ae
info = NodePropertyInfo(node_class=cls,
                        property_name="Ae",
                        property_type=float,
                        doc_short="""Effective area . This is the projection of the total to the actual wind/current direction. Read only.""",
                        doc_long = """Effective area [m2]. This is the projection of the total to the actual wind/current direction. Read only.""",
                        units = """[m2]""",
                        remarks="""""",
                        is_settable=False,
                        is_single_settable = False,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["Ae"] = info


# Property: Cd
info = NodePropertyInfo(node_class=cls,
                        property_name="Cd",
                        property_type=float,
                        doc_short="""Cd coefficient """,
                        doc_long = """Cd coefficient [-]""",
                        units = """[-]""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = True
                        )
DAVE_NODEPROP_INFO[cls]["Cd"] = info


# Property: direction
info = NodePropertyInfo(node_class=cls,
                        property_name="direction",
                        property_type=tuple,
                        doc_short="""Depends on 'areakind'. For 'plane' this is the direction of the normal of the plane, for 'cylindrical' this is""",
                        doc_long = """Depends on 'areakind'. For 'plane' this is the direction of the normal of the plane, for 'cylindrical' this is
        the direction of the axis and for 'sphere' this is not used [m,m,m]""",
                        units = """""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = False,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["direction"] = info


# Property: areakind
info = NodePropertyInfo(node_class=cls,
                        property_name="areakind",
                        property_type=DAVE_ADDITIONAL_RUNTIME_MODULES["AreaKind"],
                        doc_short="""Defines how to interpret the area.""",
                        doc_long = """Defines how to interpret the area.
        See also: `direction`""",
                        units = """""",
                        remarks="""""",
                        is_settable=True,
                        is_single_settable = True,
                        is_single_numeric = False
                        )
DAVE_NODEPROP_INFO[cls]["areakind"] = info
