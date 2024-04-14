from DAVE import *
from DAVE.gui import Gui
from DAVE.gui.dock_system.dockwidget import guiEventType

if __name__ == '__main__':
    s = Scene()
    f = s.new_frame('Frame')

    g = Gui(s, block = False)

    g.run_code("s.new_buoyancy('Buoyancy mesh', parent='Frame')", event=guiEventType.MODEL_STRUCTURE_CHANGED)

    g.run_code("s['Buoyancy mesh'].trimesh.load_file(r'res: plane.obj', scale=(1.0, 1.0, 1.0), rotation=(0.0, 0.0, 0.0), offset=(0.0, 0.0, 0.0))",  event=guiEventType.MODEL_STRUCTURE_CHANGED)

    g.guiSelectNode('Buoyancy mesh')

    g.app.exec()

    g.MainWindow.close()