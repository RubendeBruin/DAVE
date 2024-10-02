from PySide6.QtWidgets import QApplication, QWidget

from DAVE import *
from DAVE.visual_helpers.qt_embedded_renderer import QtEmbeddedSceneRenderer

def test_memleak_vtk_actor():

    s = Scene()
    #
    # # code for Frame
    f = s.new_frame(name='Frame',
               position=(0,
                         0,
                         0),
               rotation=(0,
                         0,
                         0),
               fixed =(True, True, True, True, True, True),
                )
    #
    # # code for Tank
    mesh = s.new_buoyancy(name='Tank',
              parent='Frame')
    mesh.trimesh.load_file(r'res: cube.obj', scale = (1.0,1.0,1.0), rotation = (0.0,0.0,0.0), offset = (0.0,0.0,0.0))

    app = QApplication([])

    widget = QWidget()

    viewer = QtEmbeddedSceneRenderer(s, widget)

    widget.show()
    viewer.interactor.Start()

    viewer.zoom_all()

    import psutil

    # Get the current process
    process = psutil.Process()

    mem = []

    def move():
        f.ry = f.ry + 1
        f.rx = f.rx + 3
        viewer.position_visuals()
        viewer.refresh_embeded_view()

        # Get the memory info
        memory_info = process.memory_info()
        print(f"Memory usage: {memory_info.rss} bytes")

        mem.append(memory_info.rss)


    for i in range(500):
        move()

    assert mem[-1] < 1.02 * mem[10]
