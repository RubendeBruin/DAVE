from DAVE import *
from DAVE.gui import Gui

if __name__ == '__main__':

    s = Scene()

    s.new_frame(name='Frame')
    s.new_tank(name='Tank', parent='Frame').trimesh.load_file('res: cube.obj')

    s['Tank'].fill_pct = 100.0

    g = Gui(s, block=False)
    g.app.exec()