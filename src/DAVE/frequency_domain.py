"""
Frequency domain dynamics

Provides frequency domain dynamics for DAVE

Frequency domain dynamics are based on the mass, stiffness and damping matrices which can be obtained from a scene.
These matrices are calculated numerically for a given displacement of the degrees of freedom. This allows to linearize

(Borgman - Ocean wave simulation for engineering design. 1967)
Quadratic components:
 B * u|u|  --> B * const * u
 const = rms * sqrt(8/pi)



 The Mass matrix is constructed as follows:
  M(i,j) is the force or moment that results in dof_i as result of a unit acceleration of dof_j

 This is evaluated as follows:
   1. Displace dof j by delta
   2. For express the displacements of all activated masses of dof_i in the axis system of the parent of dof_i
   3. If dof_i is a force:
          the resulting force is the displacement * mass / delta
   4. If dof_i is a moment:
          the resulting moment is the displacement * mass * distance to dof_i origin / delta

   The distance to the dof_i origin is measured in the axis system of the parent of dof_i and is the
   reference position of the point-mass (ie: the un-displaced position)




"""


"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Ruben de Bruin - 2019

"""

from DAVE.scene import *
import numpy as np
import prettytable as pt
from scipy.linalg import eig
from mafredo.hyddb1 import Hyddb1
from mafredo.helpers import wavelength
from mafredo.rao import Rao


def mode_shapes(scene):
    """Calculates the mode shapes and eigenvalues for scene.

    Returns: V (eigenvalues), D (eigenvectors)"""

    if not scene.verify_equilibrium():
        raise ArithmeticError('Scene is not in static equilibrium, modal analysis aborted')

    print("Mass matrix")
    M = scene.dynamics_M(0.1)
    print(M)
    K = scene.dynamics_K(0.1)
    print("Stiffness matrix")
    print(K)

    if K.size > 0:
        V, D = eig(K, M)

        # sort by increasing eigenvalue
        i_sorted = np.argsort(V)
        V = V[i_sorted]
        D = D[:,i_sorted]

        print("Values = ")
        print(V)
        print("Directions = ")
        print(D)

        check_unconstrained(scene, V,D,K,M)

        return V,D
    else:
        return None, None

def generate_modeshape_dofs(d0, displ, scale, n_frames, scene):
    """Will return a list of DOFs for the given modeshape.
    These can be passed directly to one of the animate functions

    Args:
        d0: mean values of the dofs (static equilibrium)
        displ: modeshape displacement
        scale: scale factor
        n_frames: number of requested frames

    Returns:
        List of np.arrays

    """
    core = scene._vfc
    result = []

    for i_frame in range(n_frames):
        change = np.sin(2 * 3.14159 * i_frame / n_frames) * displ * scale
        core.set_dofs(d0)
        core.change_dofs(change)
        result.append(core.get_dofs())

    return result

def generate_unitwave_response(s, d0, rao, wave_amplitude, n_frames):
    """Will return a list of DOFs for the given modeshape.
        These can be passed directly to one of the animate functions

        Args:
            d0: mean values of the dofs (static equilibrium)
            rao: compelex rao for all dofs
            wave_amplitude : float
            n_frames: number of requested frames

        Returns:
            List of np.arrays

        """
    core = s._vfc
    result = []

    for i_frame in range(n_frames):
        factor = i_frame / n_frames

        t = factor * 2 * np.pi
        change = wave_amplitude * np.abs(rao) * np.cos(t - np.angle(rao))

        core.set_dofs(d0)
        core.change_dofs(change)
        result.append(core.get_dofs())

    return result


def dynamics_summary(scene):
    """Prints and returns an overview of the dynamic properties of the scene"""
    data = dynamics_summary_data(scene)
    _print_summary(data)
    return data

def _print_summary(data):
    if len(data)==0:
        print('Nothing to print. Scene without and degrees of freedom')
        return

    first_line = data[0]
    t = pt.PrettyTable()
    t.field_names = first_line.keys()

    for entry in data:
        t.add_row(entry.values())

    print(t)



def dynamics_summary_data(scene):
    """Returns an overview of the dynamic properties of the scene

    Returns:
        (dict)
        """
    summary = []

    M = scene.dynamics_M(0.1)
    K = scene.dynamics_K(0.1)
    nodes = scene.dynamics_nodes()
    modes = scene.dynamics_modes()

    n = len(nodes)

    for i in range(n):
        node = nodes[i]
        mode = modes[i]

        if mode < 3:
            own = node.inertia
        else:
            pos = node.inertia_position
            pos[mode-3]=0
            dist = np.linalg.norm(pos)
            own = node.inertia * node.inertia_radii[mode-3]**2 + node.inertia * dist**2

        total = M[i,i]
        if abs(total-own) < 1e-9:
            total = own
            other = 0
        else:
            other = total - own

        # print('Node {}; Mode {}; associated inertia {:.3f} (own) +   {:.3f} (children); associated stiffness {:.3f}'.format(node.name, mode, own, other, K[i,i]))

        if K[i,i]<1e-9:
            unc = 'X'
        else:
            unc = ''

        if total<1e-9:
            noi = 'X'
        else:
            noi = ''

        info = {'node':node.name,
                'mode':mode,
                'own_inertia': own,
                'child_inertia':other,
                'total_inertia':total,
                'stiffness': K[i,i],
                'unconstrained': unc,
                'noinertia': noi}

        summary.append(info)

    return summary

def dynamics_quickfix(scene):
    """Attempts to
    1. remove unconstrained modes by adding soft springs
    2. remove zero-inertia modes by adding inertia

    returns an updated summary structure
    """


    K_LOW = 0.000001  # linear or angular stiffness
    I_LOW = 0.001  # linear inertia
    r_LOW = 0.001  # radii of gyration

    data = dynamics_summary_data(scene)
    helper_axis = dict()
    helper_spring = dict()

    summary = list()

    for entry in data:

        name = entry['node']
        node = scene[name]
        mode = entry['mode']

        # --- unconstrained nodes ---

        if entry['unconstrained']: # 'x' or ''
            # add a spring
            try:
                a = helper_axis[name]
            except KeyError:
                name = scene.available_name_like('quickfix_' + entry['node'] + 'axis')
                position = (0,0,0)
                if isinstance(node, RigidBody):
                    position = node.cog
                a = scene.new_axis(name, position = node.to_glob_position(position), rotation = node.global_rotation)
                helper_axis[entry['node']] = a

            try:
                s = helper_spring[name]
            except KeyError:
                name = scene.available_name_like('quickfix_' + entry['node'] + 'connector')
                s = scene.new_linear_connector_6d(name, master=node, slave=a)

            temp = np.array(s.stiffness)
            temp[mode] = K_LOW
            s.stiffness = temp
            entry['unconstrained'] = 'K = {}'.format(K_LOW)

        # --- inertia-less ---

        if entry['noinertia']:
            if mode<3:
                node.inertia = I_LOW
                entry['noinertia'] = 'M = {}'.format(I_LOW)
            else:
                if node.inertia < 1e-9:
                    node.inertia = I_LOW
                    entry['noinertia'] = 'M = {}'.format(I_LOW)

                if node.inertia_radii[mode-3] <= r_LOW:
                    temp = np.array(node.inertia_radii)
                    temp[mode-3] = r_LOW
                    if np.linalg.norm(temp) == r_LOW:  # other two entries are zero
                        temp = (r_LOW, r_LOW, r_LOW)
                    node.inertia_radii = temp
                    entry['noinertia'] = 'M = {}, radii = {},{},{}'.format(I_LOW,*temp)

        print(entry)
        summary.append(entry)

    _print_summary(summary)
    return summary



def check_unconstrained(scene, V, D,K,M):
    """Prints information about errornous mode-shapes.
    Unconstrained nodes come up with a natural period of nan.

    Args:
        scene: scene
        V: eigenvalues
        D: eigenvectors

    Returns:

    """

    for i in range(len(V)):
        v = V[i]
        d = D[i]

        mass_vector = M[i, :] * d
        k_vector = K[i,:] * d

        main_dof = np.argmax(np.abs(d))

        print('=== DOF {} ==='.format(i))

        if np.imag(v):
            print('Complex eigenvalue')

        print('Eigenvalue {}'.format(v))

        # print('Mode {} Omega {} Inertia {} Stiffness {} main dof {}'.format(i, v, np.linalg.norm(mass_vector), np.linalg.norm(k_vector), main_dof))

        if np.isnan(v):
            print("Unconstrained mode - modeshape: " + str(d))

        if np.isinf(v):
            print("Mode without inertia - modeshape: " + str(d))

        if abs(v) < 1e-6:
            print("Very small eigenvalue - probably unconstrained mode")

        for [i,e] in enumerate(d):
            print('{} - {:.2f}'.format(i,e))

def prepare_for_fd(s):
    """Prepares the model for frequency domain analysis.

    WARNING:
        this is a destructive method. Please run this on a copy of a scene.

    All wave-interaction nodes shall be at the origin of an axis system.
    That axis system shall not have a parent
    That axis systen shall have all dofs set to free

    Raises:
        ValueError if the scene can not be prepared.

    """

    wis = s.nodes_of_type(node_class=WaveInteraction1)

    for w in wis:

        # checks
        assert isinstance(w.parent, Axis), ValueError('Parent of "{}" shall be an axis or derived'.format(w.name))
        assert not np.any(w.parent.fixed) , ValueError('Parent of "{}" shall have all its dofs set to free (not fixed)'.format(w.name))

        # loads hydrodynamic data
        try:
            if w._hyddb is not None:
                loaddb = True
            else:
                loaddb = False
        except:
            loaddb = True

        if loaddb:
            w._hyddb = Hyddb1()
            w._hyddb.load_from(s.get_resource_path(w.path))

        if np.all(w.offset == (0,0,0)):
            continue

        # create a new axis system at the global position and orientation of the node
        glob_position = w.parent.to_glob_position(w.offset)
        glob_rotation = w.parent.global_rotation

        name = s.available_name_like('autocreated_parent_for_{}'.format(w.name))

        new_parent = s.new_axis(name, position = glob_position, rotation = glob_rotation, fixed=False)

        w.parent.change_parent_to(new_parent)
        w.parent.fixed = True

        w.parent = new_parent
        w.offset = (0,0,0)

def calc_wave_response(s, omega, wave_direction, waterdepth=0):
    """Calculates the response to a unit-wave

    Phase-angles are relative to the global origin. Waterdepth is needed to
    calculate the wave-lengths for shallow water (default: deep water)
    """

    M = s.dynamics_M(0.1)
    K = s.dynamics_K(0.1)
    nodes = s.dynamics_nodes()
    modes = s.dynamics_modes()
    names = [node.name for node in nodes]

    M = np.array(M, dtype=complex)  # change M to complex
    F = np.zeros(shape=(M.shape[0]),dtype=complex)
    B = np.zeros_like(M)

    wis = s.nodes_of_type(node_class=WaveInteraction1)

    for w in wis:
        # find the corresponding dof numbers
        name = w.parent.name
        inds = [i for i, x in enumerate(names) if x == name] # get all indices where names[i] == name

        # double-check if these yield mode 0 ... 5
        mods = [modes[i] for i in inds]

        assert mods == [0,1,2,3,4,5], ValueError('Parent of "{}" shall have all DOFs free'.format(w.name))

        m_added = w._hyddb.amass(omega)
        B_hyd  = w._hyddb.damping(omega)
        force = w._hyddb.force(omega, wave_direction)

        # Use the dot-product with the wave-direction vector to determine the phase differnce
        pos = w.parent.global_position
        wave_dir = [np.cos(np.deg2rad(wave_direction)), np.sin(np.deg2rad(wave_direction))]
        distance = pos[0]*wave_dir[0] + pos[1]*wave_dir[1]
        phase_difference = 2*np.pi * distance / wavelength(omega, waterdepth=waterdepth)
        phasor = np.exp(-1j * phase_difference)


        # add the components to system matrices
        for i in range(6):
            sys_i = inds[i]

            for j in range(6):
                sys_j = inds[j]

                M[sys_i, sys_j] += m_added[i,j]
                B[sys_i, sys_j] += B_hyd[i, j]

            F[sys_i] += phasor * force[i]

    # solve the system

    A = np.zeros_like(M)

    A += -omega**2 * M   # intertia
    A += 1j * omega * B  # damping
    A += K               # stiffness

    x = np.linalg.solve(A, F)  # solve

    return x










