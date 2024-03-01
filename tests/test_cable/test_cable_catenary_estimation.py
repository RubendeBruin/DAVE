from numpy.testing import assert_allclose

from DAVE import *

"""Symmetrical model of a grommet with a side-load and a weight such that the taut-cat equation can be used to estimate the tension in the cable"""

def model():
    s = Scene()

    def solved(number):
        return number

    # Environment settings
    s.g = 9.80665
    s.waterlevel = 0.0
    s.rho_air = 0.00126
    s.rho_water = 1.025
    s.wind_direction = 0.0
    s.wind_velocity = 0.0
    s.current_direction = 0.0
    s.current_velocity = 0.0

    # code for Body
    s.new_rigidbody(name='Body',
                    mass=20,
                    cog=(0,
                         0,
                         -0.1),
                    position=(solved(0.0),
                              0,
                              solved(-16.429027771357276)),
                    rotation=(0,
                              solved(0),
                              0),
                    fixed=(False, True, False, True, False, True),
                    )

    # code for Point3
    s.new_point(name='Point3',
                position=(0,
                          0,
                          0))

    # code for Point
    s.new_point(name='Point',
                parent='Body',
                position=(0,
                          5,
                          0))

    # code for Circle3
    c = s.new_circle(name='Circle3',
                     parent='Point3',
                     axis=(0, 1, 0),
                     radius=1)

    # code for Circle
    c = s.new_circle(name='Circle',
                     parent='Point',
                     axis=(0, 1, 0),
                     radius=1)

    # code for LoopedCableWithWeight
    s.new_cable(name='LoopedCableWithWeight',
                endA='Circle3',
                endB='Circle3',
                length=40.421,
                mass_per_length=0.00989584,
                EA=19938.641374783227,
                sheaves=['Circle'])
    return s

def test_cable_catenary_estimation_using_model():
    s = model()
    s.solve_statics()
    assert_allclose(s['Point'].my, 0, atol=1e-6)

    # total weight
    mass = s['LoopedCableWithWeight'].mass_per_length * s['LoopedCableWithWeight'].length + s['Body'].mass

    assert_allclose(s['Point3'].fz, -mass * s.g, atol = 1e-6)

def two_point_model():
    s = Scene()

    s.new_frame('world')
    s.new_point(name='Point1', position=(10, 0, 0), parent='world')
    s.new_point(name='Point2', position=(-10, 0, 0), parent='world')

    delta = 0.1
    EA = 10000
    L = 20
    tension = delta * EA / L
    mass = 0.1

    weight = mass * s.g

    ratio = tension / weight

    assert ratio > 50

    s.new_cable(name='Cable', endA='Point1', endB='Point2', length=20-delta, mass=mass, EA=EA)


    return s

def test_run_two_point_model_under_1235_orientations_taut():
    s = two_point_model()
    p1 = s['Point1']
    p2 = s['Point2']
    weight = s.g * s['Cable'].mass

    import numpy as np

    for r in np.linspace(-100, 360, num=1235):
        s['world'].rotation = [r/2, r, r/3]
        s.update()

        assert_allclose(p1.fgx + p2.fgx, 0, atol=1e-6)
        assert_allclose(p1.fgy + p2.fgy, 0, atol=1e-6)
        assert_allclose(p1.fgz + p2.fgz, -weight, atol=1e-6)

        # highest point should take most of the weight (if there is a difference)
        if abs(p1.gz - p2.gz) > 1e-6:
            if p1.gz > p2.gz:
                assert p1.fgz < p2.fgz
            else:
                assert p1.fgz > p2.fgz



def test_run_two_point_model_under_1235_orientations_cat():
    s = two_point_model()
    p1 = s['Point1']
    p2 = s['Point2']
    s['Cable'].length = 20

    weight = s.g * s['Cable'].mass

    import numpy as np

    for r in np.linspace(-100, 360, num=1235):
        s['world'].rotation = [r/2, r, r/3]
        s.update()

        assert_allclose(p1.fgx + p2.fgx, 0, atol=1e-6)
        assert_allclose(p1.fgy + p2.fgy, 0, atol=1e-6)
        assert_allclose(p1.fgz + p2.fgz, -weight, atol=1e-6)

        # highest point should take most of the weight (if there is a difference)
        if abs(p1.gz - p2.gz) > 1e-6:
            if p1.gz > p2.gz:
                assert p1.fgz < p2.fgz
            else:
                assert p1.fgz > p2.fgz

def test_run_taut_against_hardcoded_expected():
    s = two_point_model()
    p1 = s['Point1']
    p2 = s['Point2']
    s['Cable'].length = 20


    import numpy as np

    # to generate the expected values

    # gen = []
    #
    # for r in np.linspace(-100, 360, num=20):
    #     s['world'].rotation = [r / 2, r, r / 3]
    #     s.update()
    #
    #     expected = (p1.fgx, p2.fgx, p1.fgy, p2.fgy, p1.fgz, p2.fgz)
    #     gen.append(expected)
    #
    # print(gen)


    expected = [(0.6466527407418021, -0.6466527407418021, -0.980061604660563, 0.980061604660563, -3.8534479013784595, 2.867854936554339), (-0.5515165174170389, 0.5515165174170389, -0.19158823402270514, 0.19158823402270514, -3.1328451931352195, 2.147252228311099), (-3.076290571983225, 3.076290571983225, 0.32983581301867665, -0.32983581301867665, -4.705787482079683, 3.720194517255562), (-5.957266894144695, 5.957266894144695, 0.6492786807285326, -0.6492786807285326, -3.7054708751725602, 2.7198779103484396), (-7.372164057829509, 7.372164057829509, 0.12996977118596126, -0.12996977118596126, -0.9019981404933557, -0.08359482433076507), (-6.562560138159005, 6.562560138159005, -1.0770745926777316, 1.0770745926777316, 1.9572629641483057, -2.9428559289724263), (-4.215886181357546, 4.215886181357546, -2.3215827240540077, 2.3215827240540077, 3.4650392871350184, -4.4506322519591395), (-1.7561611420198608, 1.7561611420198608, -3.349408470432241, 3.349408470432241, 3.720090138710061, -4.705683103534182), (0.5316065612152425, -0.5316065612152425, -4.68206865990072, 4.68206865990072, 3.504154257187592, -4.4897472220117125), (2.9497022827027988, -2.9497022827027988, -5.8572858945227955, 5.8572858945227955, 2.0890072154406973, -3.074600180264818), (4.4906152429191915, -4.4906152429191915, -5.864522070383821, 5.864522070383821, -0.7202586598068815, -0.26533430501723926), (4.171165800338775, -4.171165800338775, -4.487654440593006, 4.487654440593006, -3.577778389298615, 2.5921854244744944), (2.242805723157632, -2.242805723157632, -2.3848649608704813, 2.3848649608704813, -4.718818479730328, 3.7332255149062075), (0.2504579241907266, -0.2504579241907266, -0.6240773772025838, 0.6240773772025838, -3.2705094419818486, 2.284916477157728), (-1.0414068871115263, 1.0414068871115263, -0.09784526137031284, 0.09784526137031284, -3.7289497813167896, 2.743356816492669), (-3.8592923402135453, 3.8592923402135453, 0.4684232838714663, -0.4684232838714663, -4.693778486420896, 3.708185521596775), (-6.511045265715535, 6.511045265715535, 0.604230668263508, -0.604230668263508, -3.100551561582528, 2.1149585967584072), (-7.37414458109614, 7.37414458109614, -0.1342283754084258, 0.1342283754084258, -0.10649273138719804, -0.8791002334369227), (-6.055380193709568, 6.055380193709568, -1.4165889226025856, 1.4165889226025856, 2.497633885048846, -3.483226849872967), (-3.553808727371048, 3.553808727371048, -2.5886868786088946, 2.5886868786088946, 3.606071320879302, -4.591664285703422)]

    for r, expected in zip(np.linspace(-100, 360, num=20), expected):
        s['world'].rotation = [r / 2, r, r / 3]
        s.update()

        assert_allclose((p1.fgx, p2.fgx, p1.fgy, p2.fgy, p1.fgz, p2.fgz), expected, atol=1e-6)
