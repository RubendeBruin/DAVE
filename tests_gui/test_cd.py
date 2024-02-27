import tempfile
from pathlib import Path
from shutil import copy


from DAVE import *

s = Scene()
s.new_frame('Frame')
s.new_visual('Visual', parent='Frame', path='res: cube.obj')

# make a temporary folder
temp_folder = Path(tempfile.mkdtemp())
print('working in temp folder:', temp_folder)

file = s.get_resource_path('res: cube.obj')

# copy to the temporary folder
copy(file, temp_folder / 'cube_newstyle.obj')

from DAVE.gui import Gui
g = Gui(s, block=False)

g.get_folder_for_dialogs = lambda : temp_folder

g.menu_save_model_as()

g.app.exec()
