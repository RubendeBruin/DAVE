import matplotlib.pyplot as plt
import numpy as np

def plot_2dof(s,xx=1,yy=1,n=100, d0 = None, pts=None):
    """Plots a graph of the 2dof results"""

    ec = s._vfc
    if d0 is None:
        d0 = ec.get_dofs()

    x = np.linspace(d0[0]-xx, d0[0]+xx, n)
    y = np.linspace(d0[1] - yy, d0[1] + yy, n)

    E = list()
    E0 = list()
    E1 = list()
    J = list()

    def z(x,y):
        ec.set_dofs([x,y])
        ec.state_update()
        errors = ec.E()
        E0.append(errors[0])
        E1.append(errors[1])

        E.append(np.linalg.norm(errors))
        J.append(ec.J())

    for _x in x:
        for _y in y:
            z(_x,_y)

    E = np.array(E)
    E = E.reshape((n,n))

    E0 = np.array(E)
    E0 = E0.reshape((n,n))

    E1 = np.array(E)
    E1 = E1.reshape((n,n))


    J = np.array(J)
    J = J.reshape((n, n))

    X,Y = np.meshgrid(x,y)

    def pltpts():
        for p in pts:
            print(p)
            plt.plot(p[0], p[1], 'c+')

    plt.subplot(221)
    plt.contourf(X,Y,E)
    plt.plot(d0[0],d0[1], 'k+')
    pltpts()
    plt.title('|E|')

    plt.subplot(222)
    plt.contourf(X, Y, J)
    plt.plot(d0[0], d0[1], 'k+')
    print('lowerst error found = {}'.format(np.min(E)))
    pltpts()
    plt.title('J')

    plt.subplot(223)
    plt.contourf(X, Y, E0)
    plt.plot(d0[0], d0[1], 'k+')
    pltpts()
    plt.title('Error dof 0')

    plt.subplot(224)
    plt.contourf(X, Y, E1)
    plt.plot(d0[0], d0[1], 'k+')
    pltpts()
    plt.title('Error dof 1')






