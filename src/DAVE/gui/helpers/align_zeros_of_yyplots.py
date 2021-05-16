def align_y0_axis(ax_left, ax_right):
    """Aligns the y=0 axes of the two plots


    """

    y0n, y0p = ax_left.get_ylim()
    y1n, y1p = ax_right.get_ylim()

    y1n = min(y1n, -1e-3)
    y0n = min(y0n, -1e-3)
    y1p = max(y1p, 1e-3)
    y0p = max(y0p, 1e-3)

    a0p = y0p / (y0p - y0n)
    a0n = -y0n / (y0p - y0n)

    a1p = y1p / (y1p - y1n)
    a1n = -y1n / (y1p - y1n)

    a_above = max(a0p, a1p, 0)
    a_below = max(a0n, a1n, 0)

    ax_left.set_ylim(y0n * a_below / a0n, y0p * a_above / a0p)
    ax_right.set_ylim(y1n * a_below / a1n, y1p * a_above / a1p)

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    import numpy as np

    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()

    x = np.linspace(0,10, num=100)
    y1 = 1+np.sin(x)
    y2 = np.cos(x)-3

    ax1.plot(x, y1, 'r')
    ax2.plot(x, y2, 'b')

    align_y0_axis(ax1, ax2)
    ax1.spines['left'].set_color([1,0,0])
    ax2.spines['right'].set_color([0, 0, 1])

    ax1.tick_params(axis='y', colors='red')
    ax2.tick_params(axis='y', colors='blue')

    plt.show()