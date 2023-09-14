from DAVE import *

s = Scene()
s.new_point("upper1", position=(-1, 0, 10))
s.new_point("upper2", position=(1, 0, 10))

b = s.new_rigidbody("load", mass=100 / s.g, cog=(0, 0, -1), rotation=(0, 0, -90))
b.fixed_z = False
s.new_point("lower1", position=(-1, 0, 0), parent=b)
s.new_point("lower2", position=(1, 0, 0), parent=b)

for p in s.nodes_of_type(Point):
    s.new_circle(f"c_{p.name}", parent=p, radius=1, axis=(1, 0, 0))

# code for Cable
grommet = s.new_cable(
    name="Cable",
    connections=[
        "c_upper1",
        "c_lower1",
        "c_upper2",
        "c_lower2",
        "c_upper1",
    ],
    length=40,
    EA=3000.0,
)
grommet.reversed = (True, False, False, True, False)

# s.solve_statics()
#
# def get_C_matrix(c : Cable):
#     assert c._isloop
#
#     target = 0.1
#     N = len(c.connections) - 1
#
#     C = []
#     delta = []
#
#     Effect0 = c.tension
#
#     for i in range(N):
#         dummy = -target
#         FF = [dummy for _ in range(N)]
#         FF[i] = None
#
#         c.friction = FF
#         s.solve_statics()
#
#         unknown = c.calculated_friction_factor
#         FF[i] = unknown
#
#         # scale
#         Crow = [x * target / unknown for x in FF]
#
#         C.append(Crow)
#         delta.append(c.tension - Effect0)
#
#     return np.array(C), np.array(delta)
#
#
# C, E = get_C_matrix(grommet)
#
# print('C = ')
# print(C)
# print('E = ')
# print(E)
#
# x = [1,1,1,1]
#
# x = np.array(x)
#
# print('x = ')
# print(x)
#
# effect = np.dot(E, x)
# print('effect = ')
# print(effect)
#
# # FF values
# CCt = C.transpose()
# FF = CCt.dot(x)
#
# print('FF = ')
# print(FF)

# This is a non-linear effect, so no way we're going to solve this using linear methods.

target = 0.1
def minimize_me(x):

    friction = [*x, None]
    print(friction)
    grommet.friction = friction
    # grommet.update()
    s.solve_statics()
    # get the unknown factor
    unknown = grommet.calculated_friction_factor

    if abs(unknown) > target:
        # scale again
        x = x * target / abs(unknown)

        grommet.friction = [*x, None]
        s.solve_statics()

    print(grommet.tension)

    return -grommet.tension


# guess = np.array([-target,target,target])  # very good initial guess
guess = np.array([-target,0,0])     # good initial guess
guess = np.array([target,0,0])      # good initial guess
guess = np.array([target,target,target])  # "good" initial guess
guess = np.array([0,0,0])           # bad initial guess
guess = np.array([0.01,0.01,0.01])  # bad initial guess


bounds = [(-target, target) for g in guess]

from scipy.optimize import minimize

# method = 'Nelder-Mead'   # works even for bad initial guess
method = 'L-BFGS-B'     # fails for bad initial guess (but quick)
# method = 'TNC'          # probably works for bad initial guess, but very slow
# method = 'SLSQP'        # fails for bad initial guess
# method = 'Powell'       # fails for bad initial guess
# method = 'trust-constr' # SLOW - fails for bad initial guess
# method = 'COBYLA'      # fails for bad initial guess  #<-- does not use bounds..?

R = minimize(minimize_me, x0 = guess, bounds=bounds, method=method, tol=1e-6)

print(R)
print(grommet.friction)




