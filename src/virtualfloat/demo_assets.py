

def solved(v):
    return v


def hook4p(s):

    # code for hook4p
    s.new_rigidbody(name='hook4p',
               position=(0.0,
                         0.0,
                         0.0),
               rotation=(0.0,
                         0.0,
                         0.0),
               mass = 80,
               cog = (0,0, -1.3),
               fixed =(True, True, True, True, False, True) )
    # code for Visual
    s.new_visual(name='Visual',
                parent='hook4p',
                path='hook4p.obj',
                offset=(0, 0, 0),
                rotation=(0, 0, 0),
                scale=(1, 1, 1) )

    s.new_poi(name='prong1',
              parent='hook4p',
              position=(1.2,
                        0.0,
                        -1.3))
    s.new_poi(name='prong2',
              parent='hook4p',
              position=(0.0,
                        1.2,
                        -1.3))
    s.new_poi(name='prong3',
              parent='hook4p',
              position=(-1.2,
                        0.0,
                        -1.3))
    s.new_poi(name='prong4',
              parent='hook4p',
              position=(0.0,
                        -1.2,
                        -1.3))

def hook2p(s):
    s.new_rigidbody(name='hook2p',
               position=(0.0,
                         0.0,
                         8.0),
               rotation=(0.0,
                         solved(0.0),
                         0.0),
               mass = 60,
               cog = (0,0,-1.1),
               fixed=(True, True, True, True, False, True))
    # code for prong1
    s.new_poi(name='prong1',
              parent='hook4p',
              position=(1.2,
                        0.0,
                        -1.3))
    # code for prong2
    s.new_poi(name='prong2',
              parent='hook4p',
              position=(-1.2,
                        0.0,
                        -1.3))
    # code for Visual
    s.new_visual(name='Visual',
                 parent='hook4p',
                 path='hook2p.obj',
                 offset=(0, 0, 0),
                 rotation=(0, 0, 0),
                 scale=(1, 1, 1))