from DAVE import *
import numpy as np

def test_blender_animation_output():

    # return True

    # Long test and depending on blender, disabled by default

    from DAVE.io.blender import create_blend_and_open
    from DAVE.visual import WaveField
    from mafredo.helpers import wavelength
    from PySide6.QtCore import QSettings

    # Get blender template and executable
    settings = QSettings("rdbr", "DAVE")

    blender_executable = settings.value(f"blender_executable")
    if blender_executable is None:
        raise "Set blender executable manually"

    blender_templates = settings.value(f"blender_templates")
    if blender_templates is None:
        raise "Set blender template manually"
    blender_template = blender_templates.split(';')[0]


    s = Scene()
    s.import_scene("res: 100x30x8_barge.dave", containerize=False, prefix="")

    # code for Point
    s.new_point(name='Point',
                parent='Barge',
                position=(50,0,40))

    # code for Load
    L =s.new_rigidbody(name='Load',
                    mass=30, fixed = False)
    L.inertia_radii = (1,1,1)

    # code for LP
    s.new_point(name='LP',  parent='Load')

    # code for Cable
    s.new_cable(name='Cable', endA='LP', endB='Point',  length=20,   EA=10000)

    # code for Visual
    s.new_visual(name='Visual',
                 parent='Load',
                 path=r'wirecube.obj',
                 offset=(0, 0, 0),
                 rotation=(0, 0, 0),
                 scale=(1, 1, 1))


    s.solve_statics()
    from DAVE_dynamics.frequency_domain import prepare_for_fd, generate_unitwave_response, RAO_1d

    prepare_for_fd(s)
    s.solve_statics()

    wave_direction = 30
    amplitude = 1
    period = 7
    n_frames = int(2*period)

    # get the initial position
    d0 = s._vfc.get_dofs()

    # get RAO
    x = RAO_1d(s=s, omegas =2 * np.pi / period, wave_direction=wave_direction)

    # generate airy wave response
    dofs = generate_unitwave_response(s=s, d0 = d0, rao=x[:,0], wave_amplitude=amplitude, n_frames=n_frames)

    # convert to list
    animation_dofs = [d for d in dofs]

    # generate wave-field
    wf = WaveField()

    nx = 50
    ny = 50

    wave_length = wavelength(2*np.pi / period,0) # infinite waterdepth

    wf.create_waveplane(wave_direction=wave_direction,
                        wave_amplitude=amplitude,
                        wave_length=wave_length,
                        wave_period=period,
                        nt=n_frames,
                        nx=nx, ny=ny, dx=250, dy=100)


    create_blend_and_open(
                s, animation_dofs=animation_dofs, wavefield=wf,
                blender_base_file=blender_template, blender_exe_path=blender_executable,
                frames_per_step=5
            )
