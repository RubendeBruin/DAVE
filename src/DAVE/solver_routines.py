from DAVE.scene import *

class DebugScene(Scene):

    def solve_statics(self):
        self.solve_hybrid()

    def solve_hybrid(self):
        self._solvedoflog = list()

        self._vfc.state_prepare()
        self._vfc.state_update_forces()

        energy_tolerance = 0

        if self._vfc.n_dofs() == 0:
            print('No degrees of freedom')
            return

        v = self._vfc

        aEnorm = []

        self.solve_statics_robust_step()

        self._solvedoflog.append(v.get_dofs())

        log = ''

        for iter in range(20):

            v.state_update_forces()
            E = v.E()
            print('Iteration {} max error {}, norm error {}, Energy {}  '.format(iter,np.max(np.abs(E)), np.linalg.norm(E), v.J() ))
            aEnorm.append(v.J())

            if np.max(np.abs(E)) < 1e-3:
                print(log)
                print('Solved in {} iterations'.format(iter))
                return True

            v.state_update_energy_dofs()
            v.state_update_forces()
            Jr = v.J() + energy_tolerance
            Dr = v.get_dofs()

            [ichanged, changes] = self.solve_newton_step_silent()
            #
            v.state_update_forces()
            #
            try:
                id = v.J() / Jr
            except:
                id = -1  # div by zero

            if v.J() > Jr:

                v.set_dofs(Dr)

                # see if, with a smaller step, we can reduce the energy
                factor = 0.5

                while True:
                    v.set_dofs(Dr)
                    for i in range(len(changes)):
                        self._vfc.change_dof(ichanged[i], factor * changes[i])
                    v.state_update_forces()

                    if v.J() < Jr:
                        log += "%{}".format(factor)
                        # print('Reduced quick-step worked with factor {}'.format(factor))
                        break

                    factor *= 0.5

                    if factor < 0.1:
                        log += 'x{}'.format(id)
                        v.set_dofs(Dr)
                        # print('smaller step does not work either')
                        ichanged = None
                        break

            else:
                log += "+" + str(len(ichanged))
                # print('Quick-step on ' + str(ichanged))

            for i in range(self._vfc.n_dofs()):
                if ichanged is None:
                    log += '|'
                    self._vfc.state_improve_dof(i, 0.001)
                    self._solvedoflog.append(v.get_dofs())
                else:
                    if i not in ichanged:
                        log += '|'
                        self._vfc.state_improve_dof(i, 0.001)
                        self._solvedoflog.append(v.get_dofs())

            # self.solve_statics_robust_step()
            # if iter%10 == 0:
            #     print('throwing in a newton')
            #     self.solve_newton_step()

            if iter % 100 == 0:
                print(log)
                print(np.max(np.abs(v.E())))
                log = ''
            print(np.max(np.abs(v.E())))
            # print(iter)

        print(log)
        return False


    def solve_statics_robust_step(self):
        self._vfc.state_prepare()
        self._vfc.state_update_forces()
        self._vfc.single_robust_step()


    def solve_newton_step(self):
        self._vfc.state_prepare()
        self._vfc.state_update_forces()
        J0 = self._vfc.J()
        res = self.solve_newton_step_silent()
        self._vfc.state_prepare()
        self._vfc.state_update_forces()
        J = self._vfc.J()

        if J != 0:
            print('Energy change during newton step (Jold / Jnew) = {}'.format(J0 / J))
        else:
            print(res)

        return res


    def solve_newton_step_silent(self):
        self._vfc.state_prepare()
        self._vfc.state_update_forces()

        E = self._vfc.E()
        K = self._vfc.K()

        E = np.array(E)

        i_nonzero_diagonal = K.diagonal() < 0

        if np.sum(i_nonzero_diagonal) == 0:
            return (), ()

        Er = E[i_nonzero_diagonal]
        Kr = K[i_nonzero_diagonal]
        Kr = Kr[:, i_nonzero_diagonal]

        print('Matrix condition = {}'.format(np.linalg.cond(Kr)))

        try:
            y = np.linalg.solve(Kr, -Er)
        except:
            return (), ()

        # check on the relative error
        # relative_error = np.linalg.norm(np.dot(Kr, y) + Er)
        # print('Relative error {}'.format(relative_error))

        # # check on max step-size
        maxy = np.max(np.abs(y))
        if maxy > 5:
            y = y * (5 / maxy)
            # print('Tuning back step-size')

        idofs = np.nonzero(i_nonzero_diagonal)[0]
        for i in range(len(y)):
            self._vfc.change_dof(idofs[i], y[i])

        return idofs, y

