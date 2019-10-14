from DAVE.scene import *
import numpy as np

def single_dof_hinge(s):
    b = s.new_rigidbody('block', mass = 1, cog = (10,0,0), fixed=(True,True,True,True,False, True))
    return [np.pi / 2]

def single_dof_hinge_eq(s):
    b = s.new_rigidbody('block', mass = 1, cog = (10,0,0), rotation = (0,-90,0), fixed=(True,True,True,True,False, True))
    return [np.pi / 2]


def dual_dof_hinge(s):
    b = s.new_rigidbody('block', mass = 1, cog = (10,0,0), fixed=(True,True,True,False,False, True))
    return [0, np.pi / 2]

def tripple_dof_hinge(s):
    b = s.new_rigidbody('block', mass = 1, cog = (10,0,0), fixed=(True,True,True,False,False, False))
    return [0, np.pi / 2,0]

def single_dof_hinge_plus_cable(s):
    b = s.new_rigidbody('block', mass = 1, cog = (10,0,0), fixed=(True,True,True,True,False, True))
    p1 = s.new_poi('p1', position = (10,0,10))
    p2 = s.new_poi('p2', parent='block', position = (20,0,0))
    s.new_cable('cable','p1','p2', length = 8, EA=1000)
    return [-0.454547]

def demo_cable(s):
    b = s.new_rigidbody('block', mass=1, cog=(10, 0, 0))
    b.set_free()
    p1 = s.new_poi('p1', position=(10, 0, 10))
    p2 = s.new_poi('p2', parent='block', position=(0, 0, 0))
    s.new_cable('cable', 'p1', 'p2', length=15, EA=1000)

    k = 1000 / 15
    F = 1 * 9.81
    stretch = F / k
    z = -5 - stretch

    return [10,0,z,0,np.pi/2,0]


def demo_two_cable(s):
    b = s.new_rigidbody('block', mass=20, cog=(0, 0, 0))
    b.set_free()
    s.new_poi('p1a', position=(1, 0, 10))
    s.new_poi('p1b', position=(-1, 0, 10))
    s.new_poi('p2a', parent='block', position=(1, 0, 0))
    s.new_poi('p2b', parent='block', position=(-1, 0, 0))

    s.new_cable('cable_a', 'p1a', 'p2a', length=15, EA=1000)
    s.new_cable('cable_b', 'p1b', 'p2b', length=15, EA=1000)

    k = 2*1000/15
    F = 20 * 9.81
    stretch = F / k
    z = -5 - stretch

    return [0, 0, z, 0.0, 0.0, 0.0]

def demo_two_cable_twisted(s):
    b = s.new_rigidbody('block', mass=20, cog=(0, 0, 0), rotation=(0,0,180))
    b.set_free()
    s.new_poi('p1a', position=(1, 0, 10))
    s.new_poi('p1b', position=(-1, 0, 10))
    s.new_poi('p2a', parent='block', position=(1, 0, 0))
    s.new_poi('p2b', parent='block', position=(-1, 0, 0))

    s.new_cable('cable_a', 'p1a', 'p2a', length=15, EA=1000)
    s.new_cable('cable_b', 'p1b', 'p2b', length=15, EA=1000)

    k = 2*1000/15
    F = 20 * 9.81
    stretch = F / k
    z = -5 - stretch

    return [0, 0, z, 0.0, 0.0, 0.0]

def demo_snake(s, n=20):
    s.new_axis('base0')
    for i in range(n):  # 20
        s.new_rigidbody(name = 'base{}'.format(i+1),
                        parent = 'base{}'.format(i),
                        mass = 1,
                        position = (2,0,0),
                        cog = (1,0,0),
                        fixed = (True,True,True,True, False, True))

    s.new_poi('Poi', parent='base{}'.format(n), position = (2,0,0))
    s.new_poi('Poi_1')
    s['Poi_1'].position = (10.0, 0.0, 0.0)
    s.new_cable('Cable', poiA = 'Poi_1', poiB= 'Poi', length=7.000, EA=100000)

    print('for n=20 the expected tension in cable is 81.385')

def all_elements():
    s = Scene()
    a = s.new_axis('test', position = (10,20,0))
    b = s.new_rigidbody('rigidbody', mass=10)
    b.set_free()
    pa = s.new_poi('poi on rigidbody', parent = 'rigidbody', position = (2,2,2))
    pt = s.new_poi('poi on test', parent='test', position = (5,7,-2))
    pb = s.new_poi('global poi', position=(0, 0, 1))
    s.new_cable('cable', length=50, EA=1000, poiA=pa, poiB = pt, sheaves=[pb])
    # s.new_cable('cable', length=1, EA=1000, poiA=pa, poiB=pb)

    return s

def grid(s, n=5):


    for i in range(n):
        for j in range(n):
            b = s.new_rigidbody(name = 'body {} {}'.format(i,j), mass = 1, position = (4*i, 4*j, 0))
            s.new_poi(name = 'poi {} {}'.format(i,j), parent = b)

    for i in range(n-1):
        for j in range(n-1):
            p1 = 'poi {} {}'.format(i,j)
            p2 = 'poi {} {}'.format(i, j+1)
            p3 = 'poi {} {}'.format(i+1, j)

            s.new_cable(name = 'cable {} {} a'.format(i,j), poiA = p1, poiB = p2, length = 5, EA = 1000)
            s.new_cable(name='cable {} {} b'.format(i, j), poiA=p1, poiB=p3, length=5, EA=1000)

            s['body {} {}'.format(i,j)].set_free()

    return s

def barge(s):

    def solved(v):
        return v

    # code for Barge
    s.new_rigidbody(name='Barge',
                    mass=20000.0,
                    cog=(50.0,
                         0.0,
                         2.5),
                    position=(solved(0.0),
                              solved(0.0),
                              solved(-5.0)),
                    rotation=(solved(0.0),
                              solved(0.0),
                              solved(0.0)),
                    fixed=(False, False, False, False, False, False))
    # code for Hydrostatics
    s.new_hydspring(name='Hydrostatics',
                    parent='Barge',
                    cob=(50.0, 0.0, 2.5),
                    BMT=(1 / 12) * 40 ** 3 * 100 / (40 * 100 * 5),
                    BML=(1 / 12) * 100 ** 3 * 40 / (40 * 100 * 5),
                    COFX=0.0,
                    COFY=0.0,
                    kHeave=39240.0,
                    waterline=2.5,
                    displacement_kN=196200.0)
    # code for Poi
    s.new_poi(name='Poi',
              parent='Barge',
              position=(0.0,
                        10.0,
                        0.0))
    # code for Force
    s.new_force(name='Force',
                parent='Poi',
                force=(0.0, 0.0, 0.0),
                moment=(0.0, 0.0, 0.0))
    #
    # code for Visual
    s.new_visual(name='Visual',
                 parent='Barge',
                 path='barge.obj',
                 offset=(0.0, 0.0, 0.0),
                 rotation=(0, 0, 0),
                 scale=(1.0, 1.0, 1.0))


def robot(s):

    def solved(v):
        return v

    # code for base_axis
    s.new_axis(name='base_axis',
               position=(0.0,
                         0.0,
                         4.0),
               rotation=(0.0,
                         0.0,
                         4.0),
               fixed=(True, True, True, True, True, True))

    s.new_visual(name='waldrof',
                 path='robot_body.obj',
                 parent='base_axis')

    # code for Shoulder
    s.new_axis(name='Shoulder',
               parent='base_axis',
               position=(0.0,
                         1.0,
                         0.8),
               rotation=(0.0,
                         1.0,
                         0.8),
               fixed=(True, True, True, True, True, True))
    # code for Upper Arm
    s.new_rigidbody(name='Upper Arm',
                    mass=0.0,
                    cog=(0.0,
                         0.0,
                         0.0),
                    parent='Shoulder',
                    position=(0.0,
                              0.0,
                              0.0),
                    rotation=(0.0,
                              0.0,
                              0.0),
                    fixed=(True, True, True, False, False, False))

    s.new_visual(name='upper_arm',
                 path='wirecube.obj',
                 offset=(0, 1, 0),
                 scale=(0.3, 1, 0.3),
                 parent='Upper Arm')

    # code for elbow
    s.new_axis(name='elbow',
               parent='Upper Arm',
               position=(0.0,
                         2.0,
                         0.0),
               rotation=(0.0,
                         2.0,
                         0.0),
               fixed=(True, True, True, True, True, True))
    # code for Lower Arm
    s.new_rigidbody(name='Lower Arm',
                    mass=0.0,
                    cog=(0.0,
                         0.0,
                         0.0),
                    parent='elbow',
                    position=(0.0,
                              0.0,
                              0.0),
                    rotation=(0.0,
                              solved(0.0),
                              solved(0.0)),
                    fixed=(True, True, True, True, True, False))

    s.new_visual(name='lower arm visual',
                 path='wirecube.obj',
                 offset=(0, 1, 0),
                 scale=(0.3, 1, 0.3),
                 parent='Lower Arm')

    # code for Hand
    s.new_poi(name='Hand',
              parent='Lower Arm',
              position=(0.0,
                        2.0,
                        0.0))
    # code for Beer
    s.new_axis(name='BeerAxis',
               position = (2,5,5))

    s.new_visual(name = 'BeerBottle',
                 path = 'beerbottle.obj',
                 parent = 'BeerAxis')
    s['BeerBottle'].scale = (0.4, 0.4, 0.4)

    s.new_poi(name='Beer',
              parent = 'BeerAxis')



    # code for Action driver
    s.new_cable(name='Action driver',
                poiA='Hand',
                poiB='Beer',
                length=0.001,
                EA=1.0)

def seal(s):

    def solved(number):
        return number

    # code for barge
    s.new_rigidbody(name='Seabert',
                    mass=45.0,
                    cog=(0.0,
                         0.0,
                         -2.0),
                    position=(solved(3.3108571809215213),
                              solved(3.2120928215643465),
                              solved(-0.28003075398497845)),
                    rotation=(solved(-20.40709918636502),
                              solved(29.908831313851124),
                              0.0),
                    fixed=(False, False, False, False, False, True))
    # code for buoyancy
    b = s.new_buoyancy(name='buoyancy',
                   parent='Seabert')

    b.trimesh.load_obj(s.get_resource_path('17919_Seal_baby_happy_V1.obj'))

    s.new_poi(name='Hand',
              parent='Seabert',
              position=(-3.0,
                        -3.0,
                        -2.0))
     # code for HOP
    s.new_poi(name='HOP',
              position=(0.0,
                        0.0,
                        9.0))
    # code for Cable
    s.new_cable(name='Cable',
                poiA='Hand',
                poiB='HOP',
                length=8.0,
                EA=2000.0)

def discrete_beam(s, EI, L, n, P, M):
    K = 2 * EI / (L / n)

    # auto generated pyhton code
    # By Ruben
    # Time: 2019-09-06 17:20:24 UTC

    # To be able to distinguish the important number (eg: fixed positions) from
    # non-important numbers (eg: a position that is solved by the static solver) we use a dummy-function called 'solved'.
    # For anything written as solved(number) that actual number does not influence the static solution
    def solved(number):
        return number

    # code for Axis0
    s.new_axis(name='Axis0',
               position=(0.0,
                         0.0,
                         0.0),
               rotation=(0.0,
                         0.0,
                         0.0),
               fixed=(True, True, True, True, True, True))
    # code for Beam

    for i in range(n):
        s.new_axis(name='Beam{}'.format(i),
                   parent='Axis{}'.format(i),
                   position=(0.0,
                             0.0,
                             0.0),
                   rotation=(0.0,
                             solved(0.0),
                             0.0),
                   fixed=(True, True, True, True, False, True))
        # code for Axis1
        s.new_axis(name='Axis{}'.format(i + 1),
                   parent='Beam{}'.format(i),
                   position=(L / n,
                             0.0,
                             0.0),
                   rotation=(0.0,
                             solved(0.0),
                             0.0),
                   fixed=(True, True, True, True, False, True))
        # code for Beam_right
        s.new_axis(name='Beam{}_right'.format(i),
                   parent='Beam{}'.format(i),
                   position=(L / n,
                             0.0,
                             0.0),
                   rotation=(0.0,
                             0.0,
                             0.0),
                   fixed=(True, True, True, True, True, True))
        # code for ConLeft
        s.new_linear_connector_6d(name='ConLeft{}'.format(i),
                                  master='Axis{}'.format(i),
                                  slave='Beam{}'.format(i),
                                  stiffness=(0.0, 0.0, 0.0,
                                             0.0, K, 0.0))
        # code for ConRight
        s.new_linear_connector_6d(name='ConRight{}'.format(i),
                                  master='Beam{}_right'.format(i),
                                  slave='Axis{}'.format(i + 1),
                                  stiffness=(0.0, 0.0, 0.0,
                                             0.0, K, 0.0))

        # code for Visual
        s.new_visual(name='Visual{}'.format(i),
                     parent='Beam{}'.format(i),
                     path='wirecube.obj',
                     offset=(0.5 * L / n, 0.0, 0.0),
                     rotation=(0, 0, 0),
                     scale=(0.5 * L / n, 0.1, 0.1))

    # ===============

    # code for Poi
    s.new_poi(name='Poi',
              parent='Axis{}'.format(n),
              position=(0.0,
                        0.0,
                        0.0))

    # code for Force
    s.new_force(name='Force',
                parent='Poi',
                force=(0.0, 0.0, 0.0),
                moment=(0.0, 0.0, 0.0))

    f = s['Force']

    f.force = (0, 0, -P)
    f.moment = (0, M, 0)

    print(s._vfc.to_string())

    s.solve_statics()

    last_beam = s['Axis{}'.format(n)]

    delta = -last_beam.global_position[2]
    phi = last_beam.global_rotation[1]

    delta_expected = P * L ** 3 / (3 * EI) + M * L ** 2 / (2 * EI)
    phi_expected = np.rad2deg(P * L ** 2 / (2 * EI) + M * L / (EI))

    print('displacement: expected {} actual {}'.format(delta_expected, delta))
    print('rotation: expected {} actual {}'.format(phi_expected, phi))

    return (last_beam, delta_expected, phi_expected)


# =======================

def discrete_beam_free_in_Z(s, EI, L, n, P, M, KZ_factor):

    K = 2 * EI / (L / n)
    KZ = K * KZ_factor

    def solved(number):
        return number

    # code for Axis0
    s.new_axis(name='Axis0',
               position=(0.0,
                         0.0,
                         0.0),
               rotation=(0.0,
                         0.0,
                         0.0),
               fixed=(True, True, True, True, True, True))
    # code for Beam

    for i in range(n):
        s.new_axis(name='Beam{}'.format(i),
                   parent='Axis{}'.format(i),
                   position=(0.0,
                             0.0,
                             0.0),
                   rotation=(0.0,
                             solved(0.0),
                             0.0),
                   fixed=(True, True, True, True, False, True))
        # code for Axis1
        s.new_axis(name='Axis{}'.format(i + 1),
                   parent='Beam{}'.format(i),
                   position=(L / n,
                             0.0,
                             0.0),
                   rotation=(0.0,
                             solved(0.0),
                             0.0),
                   fixed=(True, True, False, True, False, True))
        # code for Beam_right
        s.new_axis(name='Beam{}_right'.format(i),
                   parent='Beam{}'.format(i),
                   position=(L / n,
                             0.0,
                             0.0),
                   rotation=(0.0,
                             0.0,
                             0.0),
                   fixed=(True, True, True, True, True, True))
        # code for ConLeft
        s.new_linear_connector_6d(name='ConLeft{}'.format(i),
                                  master='Axis{}'.format(i),
                                  slave='Beam{}'.format(i),
                                  stiffness=(0.0, 0.0, KZ,
                                             0.0, K, 0.0))
        # code for ConRight
        s.new_linear_connector_6d(name='ConRight{}'.format(i),
                                  master='Beam{}_right'.format(i),
                                  slave='Axis{}'.format(i + 1),
                                  stiffness=(0.0, 0.0, KZ,
                                             0.0, K, 0.0))

        # code for Visual
        s.new_visual(name='Visual{}'.format(i),
                     parent='Beam{}'.format(i),
                     path='wirecube.obj',
                     offset=(0.5 * L / n, 0.0, 0.0),
                     rotation=(0, 0, 0),
                     scale=(0.5 * L / n, 0.1, 0.1))

    # ===============

    # code for Poi
    s.new_poi(name='Poi',
              parent='Axis{}'.format(n),
              position=(0.0,
                        0.0,
                        0.0))

    # code for Force
    s.new_force(name='Force',
                parent='Poi',
                force=(0.0, 0.0, 0.0),
                moment=(0.0, 0.0, 0.0))

    f = s['Force']

    f.force = (0, 0, -P)
    f.moment = (0, M, 0)

    print(s._vfc.to_string())
    s.solve_statics()

    last_beam = s['Axis{}'.format(n)]

    delta = -last_beam.global_position[2]
    phi = last_beam.global_rotation[1]

    delta_expected = P * L ** 3 / (3 * EI) + M * L ** 2 / (2 * EI)
    phi_expected = np.rad2deg(P * L ** 2 / (2 * EI) + M * L / (EI))

    print('displacement: expected {} actual {}'.format(delta_expected, delta))
    print('rotation: expected {} actual {}'.format(phi_expected, phi))

    return (last_beam, delta_expected, phi_expected)


def discrete_linearbeam(s, EIy, EIz, EA, GIp, L, n):

    def solved(number):
        return number

    # code for Axis0
    s.new_axis(name='Axis0',
               position=(0.0,
                         0.0,
                         0.0),
               rotation=(0.0,
                         0.0,
                         0.0),
               fixed=(True, True, True, True, True, True))
    # code for Beam

    for i in range(n):
        s.new_axis(name='Axis{}'.format(i + 1),
                   position=((i+1)*L / n,
                             0.0,
                             0.0),
                   rotation=(0.0,
                             solved(0.0),
                             0.0),
                   fixed=False)
        s.new_linear_beam(name='Beam{}'.format(i),
                          master='Axis{}'.format(i), slave='Axis{}'.format(i+1),
                          L = L/n,
                          EA=EA,
                          EIy = EIy,
                          EIz = EIz,
                          GIp = GIp )

    # code for Poi
    s.new_poi(name='Poi',
              parent='Axis{}'.format(n),
              position=(0.0,
                        0.0,
                        0.0))

def catenaty(s, EIy, EIz, EA, GIp, L, n):

     # code for Axis0
    s.new_axis(name='Axis0',
               position=(0.0,
                         0.0,
                         0.0),
               rotation=(0.0,
                         0.0,
                         0.0),
               fixed=(True, True, True, True, True, True))
    # code for Beam

    for i in range(n):
        s.new_axis(name='Axis{}'.format(i + 1),
                   position=((i+1)*L / n,
                             0.0,
                             0.0),
                   rotation=(0.0,
                             0.0,
                             0.0),
                   fixed=False)
        s.new_linear_beam(name='Beam{}'.format(i),
                          master='Axis{}'.format(i), slave='Axis{}'.format(i+1),
                          L = L/n,
                          EA=EA,
                          EIy = EIy,
                          EIz = EIz,
                          GIp = GIp )

    s['Axis{}'.format(n)].set_fixed()




def lift_4p(s):
    # auto generated pyhton code
    # By beneden
    # Time: 2019-09-04 11:58:31 UTC

    # To be able to distinguish the important number (eg: fixed positions) from
    # non-important numbers (eg: a position that is solved by the static solver) we use a dummy-function called 'solved'.
    # For anything written as solved(number) that actual number does not influence the static solution
    def solved(number):
        return number

    # code for hook4p
    s.new_rigidbody(name='hook4p',
                    mass=80.0,
                    cog=(0.0,
                         0.0,
                         -1.3),
                    position=(0.0,
                              0.0,
                              0.0),
                    rotation=(0.0,
                              solved(8.289072000610565),
                              0.0),
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
              position=(0.0,
                        1.2,
                        -1.3))
    # code for prong3
    s.new_poi(name='prong3',
              parent='hook4p',
              position=(-1.2,
                        0.0,
                        -1.3))
    # code for prong4
    s.new_poi(name='prong4',
              parent='hook4p',
              position=(0.0,
                        -1.2,
                        -1.3))
    # code for Module
    s.new_rigidbody(name='Module',
                    mass=1000.0,
                    cog=(4.0,
                         2.0,
                         -8.0),
                    position=(solved(-4.394144309416421),
                              solved(0.5367535161192127),
                              solved(-15.23572203377319)),
                    rotation=(solved(5.870642210595144),
                              solved(1.1413016663584672),
                              solved(-44.734473311889985)),
                    fixed=(False, False, False, False, False, False))
    # code for LP1
    s.new_poi(name='LP1',
              parent='Module',
              position=(10.0,
                        10.0,
                        0.0))
    # code for Cable
    s.new_cable(name='Cable',
                poiA='LP1',
                poiB='prong1',
                length=15.0,
                EA=100000.0)
    # code for LP2
    s.new_poi(name='LP2',
              parent='Module',
              position=(-10.0,
                        10.0,
                        0.0))
    # code for Cable_1
    s.new_cable(name='Cable_1',
                poiA='prong2',
                poiB='LP2',
                length=20.0,
                EA=100000.0)
    # code for LP4
    s.new_poi(name='LP4',
              parent='Module',
              position=(10.0,
                        -10.0,
                        0.0))
    # code for Cable_3
    s.new_cable(name='Cable_3',
                poiA='LP4',
                poiB='prong4',
                length=20.0,
                EA=100000.0)
    # code for Padeye1
    s.new_axis(name='Padeye1',
               parent='Module',
               position=(-10.0,
                         -10.0,
                         0.0),
               rotation=(0.0,
                         0.0,
                         50.0),
               fixed=(True, True, True, True, True, True))
    # code for LP3
    s.new_poi(name='LP3',
              parent='Padeye1',
              position=(1.25,
                        0.0,
                        0.7))
    # code for Cable_2
    s.new_cable(name='Cable_2',
                poiA='LP3',
                poiB='prong3',
                length=20.0,
                EA=100000.0)
    # code for Visual2
    s.new_visual(name='Visual2',
                 parent='hook4p',
                 path='hook4p.obj',
                 offset=(0, 0, 0),
                 rotation=(0, 0, 0),
                 scale=(1.0, 1.0, 1.0))
    # code for Visual
    s.new_visual(name='Visual',
                 parent='Module',
                 path='wirecube.obj',
                 offset=(0.0, 0.0, -5.0),
                 rotation=(0, 0, 0),
                 scale=(10.0, 10.0, 5.0))
    # code for Pad1Visual
    s.new_visual(name='Pad1Visual',
                 parent='Padeye1',
                 path='padeye.obj',
                 offset=(0, 0, 0),
                 rotation=(0, 0, 0),
                 scale=(1.25, 2.0, 0.75))


def crane5000(s):
    # auto generated pyhton code
    # By Ruben
    # Time: 2019-07-29 14:19:35 UTC

    # To be able to distinguish the important number (eg: fixed positions) from
    # non-important numbers (eg: a position that is solved by the static solver) we use a dummy-function called 'solved'.
    # For anything written as solved(number) that actual number does not influence the static solution
    def solved(number):
        return number

    # code for Crane5000_mast
    s.new_rigidbody(name='Crane5000_mast',
                    mass=4000.0,
                    cog=(0.0,
                         0.0,
                         25.0),
                    position=(0.0,
                              0.0,
                              0.0),
                    rotation=(0.0,
                              0.0,
                              0.0),
                    fixed=(True, True, True, True, True, True))
    # code for Crane5000_top
    s.new_poi(name='Crane5000_top',
              parent='Crane5000_mast',
              position=(0.0,
                        0.0,
                        61.0))
    # code for Crane_slew
    s.new_axis(name='Crane_slew',
               parent='Crane5000_mast',
               position=(0.0,
                         0.0,
                         15.0),
               rotation=(0.0,
                         0.0,
                         90.0),
               fixed=(True, True, True, True, True, True))
    # code for Crane5000_boom
    s.new_rigidbody(name='Crane5000_boom',
                    mass=1200.0,
                    cog=(33.0,
                         0.0,
                         0.0),
                    parent='Crane_slew',
                    position=(0.0,
                              0.0,
                              0.0),
                    rotation=(0.0,
                              -10,
                              0),
                    fixed=(True, True, True, True, False, True))
    # code for Mast5000_susp_wire_connection
    s.new_poi(name='Mast5000_susp_wire_connection',
              parent='Crane5000_boom',
              position=(49.0,
                        0.0,
                        2.0))
    # code for Crane_susp_wire
    s.new_cable(name='Crane_susp_wire',
                poiA='Mast5000_susp_wire_connection',
                poiB='Crane5000_top',
                length=59.865,
                EA=100000000.0)
    # code for Mast5000_Visual
    s.new_visual(name='Mast5000_Visual',
                 parent='Crane5000_mast',
                 path='crane_mastl.obj',
                 offset=(0, 0, 0),
                 rotation=(0, 0, 0),
                 scale=(1, 1, 1))
    # code for Boom5000_Visual
    s.new_visual(name='Boom5000_Visual',
                 parent='Crane5000_boom',
                 path='crane_boom.obj',
                 offset=(0, 0, 0),
                 rotation=(0, 0, 0),
                 scale=(1, 1, 1))

def turtle(s):

    # code for Turtle
    # code for Turtle
    s.new_rigidbody(name='Turtle',
                    mass=40006.0,
                    cog=(75.0,
                         0.0,
                         7.0),
                    position = (0,0,-20),
                    fixed=(True, True, False, False, False, True))
    # code for buoyancy
    s.new_buoyancy(name='buoyancy',
                   parent='Turtle')
    s['buoyancy'].trimesh.load_obj(s.get_resource_path('buoyancy turtle.obj'), scale=(1.0, 1.0, 1.0),
                                   rotation=(0.0, 0.0, 0.0), offset=(0.0, 0.0, 0.0))
    # code for import_container
    s.new_axis(name='import_container',
               position=(0.0,
                         0.0,
                         0.0),
               rotation=(0.0,
                         0.0,
                         0.0),
               fixed=(True, True, True, True, True, True))
    # code for visual - vessel
    s.new_visual(name='visual - vessel',
                 parent='Turtle',
                 path='visual vessel turtle.obj',
                 offset=(0, 0, 0),
                 rotation=(0, 0, 0),
                 scale=(1.0, 1.0, 1.0))

def cheetah(s):
    # code for Cheetah
    s.new_rigidbody(name='Cheetah',
                    mass=60000.0,
                    cog=(114.0,
                         -2.068,
                         7.0),
                    fixed=(True, True, False, False, False, True))
    # code for buoyancy
    s.new_buoyancy(name='buoyancy',
                   parent='Cheetah')
    s['buoyancy'].trimesh.load_obj(s.get_resource_path('buoyancy cheetah.obj'), scale=(1, 1, 1),
                                   rotation=(0.0, 0.0, 0.0), offset=(0.0, 0.0, 0.0))

    # code for visual - vessel
    s.new_visual(name='visual - vessel',
                 parent='Cheetah',
                 path='visual vessel cheetah.obj',
                 offset=(0, 0, 0),
                 rotation=(0, 0, 0),
                 scale=(1.0, 1.0, 1.0))

    imp = Scene()
    crane(imp)
    s.import_scene(imp)

    mast = s['crane_mast']
    mast.parent = s['Cheetah']
    mast.position = (70.0, 17.0,  12.0)

def crane(s):
    # code for crane_mast
    s.new_rigidbody(name='crane_mast',
                    mass=4000.0,
                    cog=(0.0,
                         0.0,
                         25.0),
                    rotation=(0.0,
                              0.0,
                              0.0),
                    fixed=(True, True, True, True, True, True))


    # code for crane_top
    s.new_poi(name='crane_top',
              parent='crane_mast',
              position=(0.0,
                        0.0,
                        61.0))
    # code for crane_slew
    s.new_axis(name='crane_slew',
               parent='crane_mast',
               position=(0.0,
                         0.0,
                         15.0),
               rotation=(0.0,
                         0.0,
                         -70.0),
               fixed=(True, True, True, True, True, True))
    # code for crane_boom
    s.new_rigidbody(name='crane_boom',
                    mass=1200.0,
                    cog=(33.0,
                         0.0,
                         0.0),
                    parent='crane_slew',
                    position=(0.0,
                              0.0,
                              0.0),
                    rotation=(0.0,
                              -25,
                              0.0),
                    fixed=(True, True, True, True, False, True))
    # code for susp_wire_connection
    s.new_poi(name='susp_wire_connection',
              parent='crane_boom',
              position=(49.0,
                        0.0,
                        2.0))
    # code for crane_Crane_susp_wire
    s.new_cable(name='crane_Crane_susp_wire',
                poiA='susp_wire_connection',
                poiB='crane_top',
                length=50.0,
                EA=100000000.0)

    # code for visual - crane mast
    s.new_visual(name='visual - crane mast',
                 parent='crane_mast',
                 path='visual crane mast and boomrest.obj',
                 offset=(0, 0, 0),
                 rotation=(0, 0, 0),
                 scale=(1, 1, 1))
    # code for visual - crane boom
    s.new_visual(name='visual - crane boom',
                 parent='crane_boom',
                 path='visual crane-boom.obj',
                 offset=(0, 0, 0),
                 rotation=(0, 0, 0),
                 scale=(1, 1, 1))

def octopus(s):
    # code for Cheetah
    s.new_rigidbody(name='Octopus',
                    mass=100000.0,
                    cog=(87.153,
                         0,
                         15),
                    fixed=(True, True, False, False, False, True))
    # code for buoyancy
    s.new_buoyancy(name='buoyancy',
                   parent='Octopus')
    s['buoyancy'].trimesh.load_obj(s.get_resource_path('buoyancy octopus.obj'), scale=(1, 1, 1),
                                   rotation=(0.0, 0.0, 0.0), offset=(0.0, 0.0, 0.0))

    # code for visual - vessel
    s.new_visual(name='visual - vessel',
                 parent='Octopus',
                 path='visual vessel octopus.obj',
                 offset=(0, 0, 0),
                 rotation=(0, 0, 0),
                 scale=(1.0, 1.0, 1.0))

    imp = Scene()
    crane(imp)

    # add the sb crane

    c = s.import_scene(imp, prefix='SB_')
    c.parent = s['Octopus']
    c.position = (10.0, 40.0,  50.0)
    s.dissolve(c)

    # add the PS crane
    c = s.import_scene(imp, prefix='PS_')
    c.parent = s['Octopus']
    c.position = (10.0, -40.0, 50.0)
    s.dissolve(c)

    # Set cranes
    s['SB_crane_slew'].rotation = (0.0, 0.0, 30.0)
    s['PS_crane_slew'].rotation = (0.0, 0.0, -30.0)


def all_node_types(s):

    def solved(number):
        return number

    # code for Axis
    s.new_axis(name='Axis',
               position=(0.0,
                         0.0,
                         0.0),
               rotation=(0.0,
                         0.0,
                         0.0),
               fixed=(True, True, True, True, True, True))
    # code for Poi
    s.new_poi(name='Poi',
              parent='Axis',
              position=(5.0,
                        0.0,
                        -1.0))
    # code for Body
    s.new_rigidbody(name='Body',
                    mass=0.0,
                    cog=(0.0,
                         0.0,
                         0.0),
                    position=(10.0,
                              0.0,
                              -6.0),
                    rotation=(0.0,
                              0.0,
                              0.0),
                    fixed=(True, True, True, True, True, True))
    # code for Poi_1
    s.new_poi(name='Poi_1',
              position=(0.0,
                        0.0,
                        -4.0))
    # code for Cable
    s.new_cable(name='Cable',
                poiA='Poi',
                poiB='Poi_1',
                length=6.4031242374328485,
                EA=0.0)
    # code for Force
    s.new_force(name='Force',
                parent='Poi_1',
                force=(2.0, 1.0, 0.0),
                moment=(0.0, 0.0, -1.0))
    # code for Axis_1
    s.new_axis(name='Axis_1',
               position=(5.0,
                         0.0,
                         -4.0),
               rotation=(0.0,
                         0.0,
                         0.0),
               fixed=(True, True, True, True, True, True))
    # code for Axis_2
    s.new_axis(name='Axis_2',
               position=(10.0,
                         0.0,
                         -3.0),
               rotation=(0.0,
                         -25.0,
                         0.0),
               fixed=(True, True, True, True, True, True))
    # code for Beam
    s.new_linear_beam(name='Beam',
                     master='Axis_1',
                     slave='Axis_2',
                     EIy=0.0,
                     EIz=0.0,
                     GIp=0.0,
                     EA=0.0,
                     L=5.0990195135927845)  # L can possibly be omitted
    # code for Connector2d
    s.new_connector2d(name='Connector2d',
                      master='Axis_1',
                      slave='Axis',
                      k_linear=0.0,
                      k_angular=0.0)
    # code for Axis_3
    s.new_axis(name='Axis_3',
               position=(2.0,
                         0.0,
                         -7.0),
               rotation=(0.0,
                         0.0,
                         0.0),
               fixed=(True, True, True, True, True, True))
    # code for LinCon6d
    s.new_linear_connector_6d(name='LinCon6d',
                              master='Axis_1',
                              slave='Axis_3',
                              stiffness=(0.0, 0.0, 0.0,
                                         0.0, 0.0, 0.0))
    # code for Hydrostatics
    s.new_hydspring(name='Hydrostatics',
                    parent='Axis_3',
                    cob=(0.0, 0.0, 0.0),
                    BMT=0.0,
                    BML=0.0,
                    COFX=0.0,
                    COFY=0.0,
                    kHeave=0.0,
                    waterline=0.0,
                    displacement_kN=0.0)
    # code for Buoyancy mesh
    s.new_buoyancy(name='Buoyancy mesh',
                   parent='Axis_2')
    s['Buoyancy mesh'].trimesh.load_obj(s.get_resource_path('cog.obj'), scale=(1.0, 1.0, 1.0), rotation=(0.0, 0.0, 0.0),
                                        offset=(0.0, 0.0, 3.0))
    # code for Visual
    s.new_visual(name='Visual',
                 parent='Axis_3',
                 path='wirecube.obj',
                 offset=(4.0, 0.0, 0.0),
                 rotation=(0, 0, 0),
                 scale=(1, 1, 1))
