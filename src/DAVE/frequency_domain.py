from DAVE.scene import *
import numpy as np
import prettytable as pt
from scipy.linalg import eig


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
        n_frames: numer of requested frames

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
    t = pt.PrettyTable()
    t.field_names = first_line.keys()

    for entry in data:
        t.add_row(entry.values())

    print(t)



def dynamics_summary_data(scene):
    """Returns an overview of the dynamic properties of the scene"""
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
    1. remove unconstrained nodes by adding soft springs
    2. remove intertia-less nodes by adding inertia

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
    """Unconstrained nodes come up with a natural period of nan

    Args:
        scene:
        V:
        D:

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
