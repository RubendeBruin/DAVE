from DAVE import *
from DAVE.settings import SolverSettings


def test_solver_settings_defaults():
    s = Scene()
    info = SolverSettings()
    info2 = SolverSettings()

    assert info == info2
    assert s.solver_settings == info

    assert info.non_default_props() == []

    info.timeout_s = 4
    assert info.non_default_props() == ['timeout_s']

def test_solver_settings_defaults_copy():
    s = Scene()
    s.solver_settings.timeout_s = 4

    s2 = s.copy()

    assert s2.solver_settings.timeout_s == 4


