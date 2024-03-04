"""run-code can behave wrongly if called recursively. This can happen when the executed code does a scene.copy().
This was caused by the re-assignment of the local variable 's' in the function 'run_code'.
This has been fixed by storing the original value of 's' and restoring it after the code has been executed.
This is a test to check if the issue has been fixed.
"""

from DAVE import Scene

def test_scene_maintained_when_running_code():
    s = Scene()
    s.new_point('just to have something')

    a = str(s)

    s.run_code('s2 = s.copy()')

    b = str(s)

    assert a == b