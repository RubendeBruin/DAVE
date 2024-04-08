from pathlib import Path

from DAVE.visual_helpers.vtkActorMakers import vp_actor_from_file

def test_read_invalid_obj():
    filename = Path(__file__).parent / 'invalid_obj.obj'
    vp_actor_from_file(filename)