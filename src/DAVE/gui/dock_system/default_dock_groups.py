from DAVE.gui.dock_system.gui_dock_groups import DaveDockGroup
from DAVE.gui.settings import DOCK_GROUPS


# ['Watches',
# 'Properties',
# 'DOF Editor',
# 'Node Tree',
# 'Quick actions',
# 'Derived Properties',
# 'Properties - dynamic',
# 'Mode-shapes',
# 'Environment',
# 'Stability',
# 'Limits and UCs',
# 'Tags',
# 'Airy waves',
# 'Footprints',
# 'Graph',
# 'vanGogh',
# 'DOF editor',
# 'Explore 1-to-1']

# Construct the basic dock groups
construct = DaveDockGroup(
    ID="Build",
    description="Build",
    icon=":v2/icons/design.svg",
    dock_widgets=["Quick actions"],
    show_edit=True,
    show_tree=True,
    show_timeline=None,
)

DOCK_GROUPS.append(construct)

explore = DaveDockGroup(
    ID="Explore",
    description="Explore",
    icon=":v2/icons/explore.svg",
    dock_widgets=["Explore 1-to-1"],
    show_edit=None,
    show_tree=False,
    show_timeline=None,
)

DOCK_GROUPS.append(explore)


limits = DaveDockGroup(
    ID="Limits",
    description="Limits",
    icon=":v2/icons/limits.svg",
    dock_widgets=["Limits and UCs"],
    show_edit=None,
    show_tree=True,
    show_timeline=None,
)

DOCK_GROUPS.append(limits)


ballast = DaveDockGroup(
    ID="Ballast",
    description="Ballast",
    icon=":v2/icons/ballast.svg",
    dock_widgets=["Ballast Solver", "Tanks", "BallastSystemSelect","TankReOrder"],
    show_edit=None,
    show_tree=False,
    show_timeline=None,
)

DOCK_GROUPS.append(ballast)

shear_and_bending = DaveDockGroup(
    ID="Shear and Bending",
    description="Shear and Bending",
    icon=":v2/icons/shearandbending.svg",
    dock_widgets=["Footprints","Graph"],
    show_edit=False,
    show_tree=False,
    show_timeline=None,)
DOCK_GROUPS.append(shear_and_bending)

modeshapes = DaveDockGroup(
    ID="Modeshapes",
    description="Motion",
    icon=":v2/icons/motion.svg",
    dock_widgets=["Mode-shapes","Properties - dynamic"],
    show_edit=False,
    show_tree=False,
    show_timeline=None,)
DOCK_GROUPS.append(modeshapes)