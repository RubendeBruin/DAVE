"""These are the settings for the GUI"""

from os import mkdir

# ======= Animate after solving =========

GUI_DO_ANIMATE = True
GUI_SOLVER_ANIMATION_DURATION = 0.5  # S
GUI_ANIMATION_FPS = 60

# ======= Autosave ========

from DAVE.settings import default_user_dir

autosave_dir = default_user_dir / ".autosave"
if not autosave_dir.exists():
    mkdir(autosave_dir)

AUTOSAVE_INTERVAL_S = 60  # save every 60 seconds

QUICK_ACTION_REGISTER = []
"""Functions in this list are called by the Quick Action widget in the gui and can be used to add buttons to the
quick-action widget. 

QUICK_ACTION_REGISTER demo:

def qa_demo(scene, selection, *args):
    if any([isinstance(node, Point) for node in selection]):
        btn = QPushButton('Good point!')
        btn.setIcon(QIcon(":/icons/circle.png"))
        return [(btn,"print('Told ya')")]
    return []

QUICK_ACTION_REGISTER.append(qa_demo)
"""

# ======= Dock system =========


DAVE_GUI_DOCKS = dict()


from DAVE.gui.dock_system.gui_dock_groups import DaveDockGroup


"""This dictionary contains all dock widgets that are available in the gui. The key is the ID of the dock widget, the value is the class of the dock widget.

from DAVE.gui.dock_system.gui_dock_groups import DockGroup
"""

DOCK_GROUPS = []




