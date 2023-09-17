import pytest
from DAVE import *


def test_scene_solve_no_dofs():
    s = Scene()
    from DAVEcore import BackgroundSolver, DAVECore_runtime

    with pytest.raises(DAVECore_runtime):
        BackgroundSolver(s._vfc)

    try:
        BackgroundSolver(s._vfc)
    except DAVECore_runtime as e:
        assert "Scene has no degrees of freedom" in str(e)