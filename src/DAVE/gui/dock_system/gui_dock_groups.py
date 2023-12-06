"""Gui dock groups

Gui dock groups are used to group dock widgets together.

General:
Description,Icon:       Description and icon of the dock group
Dock widgets:           List of dock widgets that belong to the group, these are the IDs (str) of the dock widgets




"""

from dataclasses import dataclass
from DAVE.gui.dock_system.ads_helpers import *

@dataclass
class DaveDockGroup:

    ID : str # unique ID

    # General settings
    description: str
    icon: QIcon or str

    # Dock widgets, referenced by key (str) as defined in DAVE_GUI_DOCKS keys
    dock_widgets: list[str]

    # Settings for global docks
    # use None for no preference
    # use True / False for show to hide
    show_edit : bool or None = None
    show_tree : bool or None = None
    show_timeline : bool or None = None

    # open in new window
    new_window : bool = False
    new_window_copy = True          # as copy
    new_window_no_workspaces = True # do not show workspaces
    new_window_read_only = True
    init_actions : str = ""         # run this code (on the copy)




