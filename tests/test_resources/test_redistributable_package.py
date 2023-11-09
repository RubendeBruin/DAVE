from pathlib import Path
from DAVE import *


def test_make_with_nested_components(tmp_path):
    s = Scene()
    path = Path(__file__).parent.parent / 'files'
    s.add_resources_paths(path)
    s.new_component('outer_component', 'res: outer_component.dave')

    target = tmp_path

    filename, log = s.create_standalone_copy(target_dir=target,
                             filename='test',
                             include_visuals=True,)

    print('\n'.join(log))
    assert filename
    assert filename.exists()

    print('wait here')

