from DAVE import *
def model():
    s = Scene()

    # code for Frame
    f = s.new_frame(name='Frame',
                    position=(0,
                              0,
                              0),
                    rotation=(0,
                              10,
                              0),
                    fixed=(True, True, True, True, True, True),
                    )

    # code for Tank
    mesh = s.new_buoyancy(name='Tank',
                      parent='Frame')
    mesh.trimesh.load_file(r'res: cube.obj', scale=(10.0, 10.0, 10.0), rotation=(0.0, 0.0, 0.0), offset=(0.0, 0.0, 0.0))
    t = s['Tank']

    return s, f, t

if __name__ == '__main__':
    s,f,t = model()
    DG(s, autosave=False)