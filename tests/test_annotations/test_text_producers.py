from DAVE.annotations import TextProducer, ProduceTextAlgorithm

def test_example_as_in_documentation():
    from DAVE import Scene
    s = Scene()
    p = s.new_point("p1", position = (0, 0, 1.23456))
    t1 = TextProducer(p, "Just a text", how = ProduceTextAlgorithm.NOTHING)
    t2 = TextProducer(p, "z", how = ProduceTextAlgorithm.PROPERTY_RAW)
    t3 = TextProducer(p, "z", how = ProduceTextAlgorithm.PROPERTY)
    t4 = TextProducer(p, "z", how = ProduceTextAlgorithm.PROPERTY, ff = "{:.1f}")
    t5 = TextProducer(p, "sdfa", how = ProduceTextAlgorithm.PROPERTY_RAW, ff = "{:.1f}")
    t6 = TextProducer(p, "node.gz", how = ProduceTextAlgorithm.EVAL, ff = "{:.1f}")
    t7 = TextProducer(p, "f'z = {node.z:.3f}m, fx = {node.fz / 9.81} tonnes'", how = ProduceTextAlgorithm.EVAL, ff = "{:.1f}")
    t8 = TextProducer(p, "does not compute", how = ProduceTextAlgorithm.EVAL)

    print(t8.get_text())

def test_raw(cable):
    s = cable
    cable = s["cable"]

    p = TextProducer(node = cable,
                     text = "just this text",
                     how = ProduceTextAlgorithm.NOTHING)

    assert p.get_text() == "just this text"

def test_string_property(cable):
    s = cable
    cable = s["cable"]

    p = TextProducer(cable, "name", ProduceTextAlgorithm.PROPERTY_RAW)

    assert p.get_text() == "cable"

def test_float_property(cable):
    s = cable
    cable = s["cable"]

    p = TextProducer(cable, "length", ProduceTextAlgorithm.PROPERTY_RAW)

    assert float(p.get_text()) > 10

def test_float_property_with_ff(cable):
    s = cable
    cable = s["cable"]

    p = TextProducer(cable, "length", ProduceTextAlgorithm.PROPERTY_RAW, ff ="{:.0f}")

    assert float(p.get_text()) == 10

def test_float_property_nice(cable):
    s = cable
    cable = s["cable"]

    p = TextProducer(cable, "length", ProduceTextAlgorithm.PROPERTY)

    assert p.get_text() == 'length = 10.050 [m]'

def test_re_assing(cable):
    s = cable
    cable = s["cable"]

    p = TextProducer(cable, "length", ProduceTextAlgorithm.PROPERTY)

    assert p.get_text() == 'length = 10.050 [m]'

    p.text = "name"
    assert p.get_text() == 'name = cable'

    p.node = s["p1"]
    assert p.get_text() == 'name = p1'

    p.how = ProduceTextAlgorithm.PROPERTY_RAW
    assert p.get_text() == 'p1'

def test_serialize(cable):
    s = cable
    cable = s["cable"]

    p = TextProducer(cable, "length", ProduceTextAlgorithm.PROPERTY)

    d = p.as_dict()

    p2 = TextProducer.from_dict(d, scene=s)

    assert p.get_text() == p2.get_text()

