from DAVE import *
from DAVE.gui.dock_system.dockwidget import guiEventType

def model():
    s = Scene()

    # code for Frame
    f = s.new_frame(name='Frame',
                    position=(0,
                              0,
                              0),
                    rotation=(360,
                              0,
                              0),
                    fixed=(True, True, True, True, True, True),
                    )

    # code for Tank
    mesh = s.new_tank(name='Tank',
                      parent='Frame')
    mesh.trimesh.load_file(r'res: cube.obj', scale=(1.0, 1.0, 1.0), rotation=(0.0, 0.0, 0.0), offset=(0.0, 0.0, 0.0))
    s['Tank'].volume = 0.75  # first load mesh, then set volume

    t = s['Tank']

    return s, f, t

def test_tank_fluid_change_number_of_vertices():
    s,f,t = model()

    g = DG(s, block = False)

    for i in range(360):
        f.rx = i
        g.guiEmitEvent(guiEventType.MODEL_STATE_CHANGED)
        g.app.processEvents()

def test_fill_tank():

    s,f,t = model()

    g = DG(s, block = False)

    for i in range(101):
        t.fill_pct = i
        g.guiEmitEvent(guiEventType.MODEL_STATE_CHANGED)
        g.app.processEvents()

# if __name__ == '__main__':
#     s, f, t = model()
#
#     f.fill_pct = 10
#
#     g = DG(s, block=False)
#
#     f.rx = 90
#     g.guiEmitEvent(guiEventType.MODEL_STATE_CHANGED)
#     g.app.processEvents()
#
#     f.rx = 100
#     g.guiEmitEvent(guiEventType.MODEL_STATE_CHANGED)
#     g.app.processEvents()
#
#     f.rx = 110
#     g.guiEmitEvent(guiEventType.MODEL_STATE_CHANGED)
#     g.app.processEvents()
#
#
