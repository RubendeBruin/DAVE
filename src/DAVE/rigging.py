"""
rigging.py

This module supplies additional functionality for working with rigging.



"""

"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Ruben de Bruin - 2019
"""

def create_sling(s, name, Ltotal, LeyeA, LeyeB, LspliceA, LspliceB, diameter, EA, mass, endA = None, endB=None, sheave=None):
    """
    Creates a new sling and adds it to scene s.

    endA
    eyeA (cable)
    splice (body , mass/2)
    main (cable)     [optional: runs over sheave]
    splice (body, mass/2)
    eyeB (cable)
    endB

    Args:
        s:     The scene in which the sling should be created
        name:  Name prefix
        Ltotal: Total length measured between the inside of the eyes of the sling is pulled straight.
        LeyeA: Total inside length in eye A if stretched flat
        LeyeB: Total inside length in eye B if stretched flat
        LspliceA: Length of the splice at end A
        LspliceB: Length of the splice at end B
        diameter: Diameter of the sling
        EA: EA of the wire
        mass: total mass
        endA : Sheave or poi to fix end A of the sling to [optional]
        endB : Sheave or poi to fix end A of the sling to [optional]
        sheave : Sheave or poi for the main part of the sling

    Returns:

    """

    # create the two splices

    sa = s.new_rigidbody(name + '_spliceA', mass = mass/2, fixed=False)
    a1= s.new_poi(name + '_spliceA1', parent=sa, position = (LspliceA/2, diameter/2, 0))
    a2 = s.new_poi(name + '_spliceA2', parent=sa, position=(LspliceA / 2, -diameter / 2, 0))
    am = s.new_poi(name + '_spliceAM', parent=sa, position=(-LspliceA / 2, 0, 0))

    s.new_visual(name + '_spliceA_visual', parent=sa,  path=r'cylinder 1x1x1 lowres.obj',
                 offset=(-LspliceA/2, 0.0, 0.0),
                 rotation=(0.0, 90.0, 0.0),
                 scale=(LspliceA, 2*diameter, diameter))

    sb = s.new_rigidbody(name + '_spliceB', mass = mass/2, rotation = (0,0,180),fixed=False)
    b1 = s.new_poi(name + '_spliceB1', parent=sb, position = (LspliceB/2, diameter/2, 0))
    b2 = s.new_poi(name + '_spliceB2', parent=sb, position=(LspliceB / 2, -diameter / 2, 0))
    bm = s.new_poi(name + '_spliceBM', parent=sb, position=(-LspliceB / 2, 0, 0))

    s.new_visual(name + '_spliceB_visual', parent=sb, path=r'cylinder 1x1x1 lowres.obj',
                 offset=(-LspliceB / 2, 0.0, 0.0),
                 rotation=(0.0, 90.0, 0.0),
                 scale=(LspliceB, 2 * diameter, diameter))

    # main part

    # The stiffness of the main part is corrected to account for the stiffness of the splices.
    # It is considered that the stiffness of the splices is two times that of the wire.
    #
    # Springs in series: 1/Ktotal = 1/k1 + 1/k2 + 1/k3

    Lmain = Ltotal-LspliceA-LspliceB-LeyeA-LeyeB
    ka = (2*EA / LspliceA)
    kb = (2*EA / LspliceB)
    kmain = (EA / Lmain)
    k_total = 1 / ((1/ka) + (1/kmain) + (1/kb))

    EAmain = k_total * Lmain

    s.new_cable(name, poiA = am, poiB = bm, length=Lmain, EA=EAmain, diameter=diameter, sheaves=sheave)

    # eyes
    if endA is None:
        endA = []
    if endB is None:
        endB = []

    s.new_cable(name + '_eyeA', poiA = a1, poiB=a2, length = LeyeA * 2 - diameter, EA=EA, diameter=diameter, sheaves = endA)
    s.new_cable(name + '_eyeB', poiA=b1, poiB=b2, length=LeyeB * 2 - diameter, EA = EA, diameter=diameter, sheaves = endB)

