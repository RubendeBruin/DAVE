from pathlib import Path

from DAVE import *
from DAVE.gui import Gui
from DAVE.gui.dock_system.dockwidget import guiEventType


"""Issue description: a visual is made unavailable by changing the cd.

Cause:
Updating the visuals after clearing the scene raised an issue because the 
visuals were updated before they were removed. 
Solution is was to remove redundant visuals before updating them.
"""

def test_issue179():


    import tempfile
    import shutil


    # Step 1: Create two temporary directories
    temp_dir1 = tempfile.TemporaryDirectory()
    temp_dir2 = tempfile.TemporaryDirectory()

    # make an empty DAVE file in the second temporary directory
    s = Scene()
    filename2 = f'{temp_dir2.name}/davefile.dave'
    s.save_scene(filename2)




    # Step 2: Copy the default cube.obj file to the first temporary directory
    s = Scene()
    filename = s.resource_provider.get_resource_path('res: cube.obj')
    shutil.copy2(filename, temp_dir1.name)

    # Step 3: Create a new DAVE model with a visual
    g = Gui(s, block = False)

    filename = f'{temp_dir1.name}/davefile.dave'
    code = 's.save_scene(r"{}")'.format(filename)
    g.run_code(code, guiEventType.NOTHING)

    g.scene.current_directory = Path(temp_dir1.name)


    g.run_code("s.new_visual('Visual', path ='cd: cube.obj')", event=guiEventType.MODEL_STRUCTURE_CHANGED)

    # Now open the file in the second temporary directory
    g.open_file(filename2)

    g.app.processEvents()

    g.MainWindow.close()
