"""
Modal analysis

Frequency domain dynamics are based on the mass, stiffness and damping matrices which can be obtained from a scene.
These matrices are calculated numerically for a given displacement of the degrees of freedom. This allows to linearize


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
from scipy.linalg import eig
import DAVE.settings as ds


def mode_shapes(scene):
    """Calculates the mode shapes and eigenvalues for scene.
    The output is sorted in order of increasing eigenvalue.

    The natural frequency [rad/s] is sqrt(eigenvalue)
    The natural period [s] is 2*pi / sqrt(eigenvalue)

    Returns: V (eigenvalues), D (eigenvectors)"""

    if not scene.verify_equilibrium():
        raise ArithmeticError('Scene is not in static equilibrium, modal analysis aborted')

    print("Mass matrix")
    M = scene.dynamics_M(1e-6)
    print(M)
    K = scene.dynamics_K(1e-6)
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

    try:
        import prettytable as pt
        t = pt.PrettyTable()
        t.field_names = first_line.keys()

        for entry in data:
            t.add_row(entry.values())

        print(t)
    except:
        print('install prettytable for a nicer format')
        print(data)


def dynamics_summary_data(scene):
    """Returns an overview of the dynamic properties of the scene

    Returns:
        (dict)
        """
    summary = []

    M = scene.dynamics_M()
    K = scene.dynamics_K()
    nodes = scene.dynamics_nodes()
    modes = scene.dynamics_modes()

    n = len(nodes)

    for i in range(n):
        node = nodes[i]
        mode = modes[i]

        if node is not None:

            if mode < 3:
                own = node.inertia
            else:
                pos = np.array(node.inertia_position, dtype=float)
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

        else:
            info = {'node': 'internal node of beam',
                    'mode': mode,
                    'own_inertia': 0,
                    'child_inertia': 0,
                    'total_inertia': 0,
                    'stiffness': 0,
                    'unconstrained': False,
                    'noinertia': False}

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
                a = scene.new_frame(name, position = node.to_glob_position(position), rotation = node.global_rotation)

                # if node has a parent, then place the axis there (also works if parent is None)
                a.change_parent_to(node.parent)

                helper_axis[entry['node']] = a

            try:
                s = helper_spring[name]
            except KeyError:
                name = scene.available_name_like('quickfix_' + entry['node'] + 'connector')
                s = scene.new_linear_connector_6d(name, secondary=node, main=a)

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

        # print('Mode {} Omega {} Inertia {} Stiffness {} nodeA dof {}'.format(i, v, np.linalg.norm(mass_vector), np.linalg.norm(k_vector), main_dof))

        if np.isnan(v):
            print("Unconstrained mode - modeshape: " + str(d))

        if np.isinf(v):
            print("Mode without inertia - modeshape: " + str(d))

        if abs(v) < 1e-6:
            print("Very small eigenvalue - probably unconstrained mode")

        for [i,e] in enumerate(d):
            print('{} - {:.2f}'.format(i,e))

