from DAVE import *


def test_obfuscate_names():
    s = Scene()
    f = Frame(s, "f")
    p = s.new_point("p", parent=f)

    s.obfuscate_names()

    assert f.name != "f"
    assert p.name != "p"

    print(f.name)