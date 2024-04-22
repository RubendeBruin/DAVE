"""Issue 115

Importing scenes fails if importing a model with a node named "import_container" #115
"""

import tempfile
from DAVE import *

def test_issue_115():
    s = Scene()
    f = s.new_frame('import_container')

    # save the scene using a temp name
    filename = tempfile.mktemp(suffix='.dave')
    s.save_scene(filename)

    s = Scene()
    s.import_scene(filename, containerize=True)


