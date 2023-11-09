"""This is a container for a DC.MomentDiagram object providing plot methods"""

import numpy as np


class LoadShearMomentDiagram:
    def __init__(self, datasource):
        """

        Args:
            datasource: DC.MomentDiagram object
        """

        self.datasource = datasource

    def give_shear_and_moment(self, grid_n=100):
        """Returns (position, shear, moment)"""
        x = self.datasource.grid(grid_n)
        return x, self.datasource.Vz, self.datasource.My

    def give_loads_table(self):
        """Returns a 'table' with all the loads.
        point_loads : (Name, location, force, moment) ; all local
        distributed load : (Name, Fz, mean X, start x , end x
        """

        m = self.datasource  # alias
        n = m.nLoads

        point_loads = []
        distributed_loads = []
        for i in range(n):
            load = list(m.load_origin(i))
            effect = m.load(i)

            plotx = effect[0]

            is_distributed = len(plotx) > 2

            if is_distributed:
                load[0] += " *"  # (add a * to the name))

            if (
                np.linalg.norm(load[2]) > 1e-6 or np.linalg.norm(load[3]) > 1e-6
            ):  # only forces that actually do something
                point_loads.append(load)

            if is_distributed:
                name = effect[-1]  # name without the *
                P = load[1]
                F = load[2]
                M = load[3]

                Fz = F[2]
                My = M[1]

                if abs(Fz) > 1e-10:
                    dx = -My / Fz
                    x = P[0] + dx
                else:
                    x = P[0]

                distributed_loads.append([name, Fz, x, plotx[0], plotx[-1]])

        return point_loads, distributed_loads

    def plot_simple(self, **kwargs):
        """Plots the bending moment and shear in a single yy-plot.
        Creates a new figure

        any keyword arguments are passed to plt.figure(), so for example dpi=150 will increase the dpi

        Returns: figure
        """
        x, Vz, My = self.give_shear_and_moment()
        import matplotlib.pyplot as plt

        plt.rcParams.update({"font.family": "sans-serif"})
        plt.rcParams.update({"font.sans-serif": "consolas"})
        plt.rcParams.update({"font.size": 10})

        fig, ax1 = plt.subplots(1, 1, **kwargs)
        ax2 = ax1.twinx()

        ax1.plot(x, My, "g", lw=1, label="Bending Moment")
        ax2.plot(x, Vz, "b", lw=1, label="Shear Force")

        from DAVE.gui.helpers.align_zeros_of_yyplots import align_y0_axis

        align_y0_axis(ax1, ax2)

        ax1.set_xlabel("Position [m]")
        ax1.set_ylabel("Bending Moment [kNm]")
        ax2.set_ylabel("Shear Force [kN]")

        ax1.tick_params(axis="y", colors="g")
        ax2.tick_params(axis="y", colors="b")

        # fig.legend()  - obvious from the axis

        ext = 0.1 * (np.max(x) - np.min(x))
        xx = [np.min(x) - ext, np.max(x) + ext]
        ax1.plot(xx, [0, 0], c=[0.5, 0.5, 0.5], lw=1, linestyle=":")
        ax1.set_xlim(xx)

        return fig

    def _plot_component(self, ax, i: int, grid_n: int = 1000):
        m = self.datasource  # alias
        x = m.grid(grid_n)
        linewidth = 2

        if i == 0:
            data = m.Vx
            title = "Axial"
            ylabel = "[kN]"
        elif i == 1:
            data = m.Vy
            title = "Shear in Y direction"
            ylabel = "[kN]"
        elif i == 2:
            data = m.Vz
            title = "Shear in Z direction"
            ylabel = "[kN]"
        elif i == 3:
            data = m.Mx
            title = "Torsion around X"
            ylabel = "[kNm]"
        elif i == 4:
            data = m.My
            title = "Bending in XZ"
            ylabel = "[kNm]"
        elif i == 5:
            data = m.Mz
            title = "Bending in XY"
            ylabel = "[kNm]"

        dx = (np.max(x) - np.min(x)) / 20  # plot scale
        ax.plot(x, data, "k-", linewidth=linewidth)

        i = np.argmax(data)
        ax.plot((x[i] - dx, x[i] + dx), (data[i], data[i]), "k-", linewidth=0.5)
        ax.text(x[i], data[i], f"{data[i]:.2f}", va="bottom", ha="center")

        i = np.argmin(data)
        ax.plot((x[i] - dx, x[i] + dx), (data[i], data[i]), "k-", linewidth=0.5)
        ax.text(x[i], data[i], f"{data[i]:.2f}", va="top", ha="center")

        ax.grid()
        ax.set_title(title)
        ax.set_ylabel(ylabel)

    def plot_components(self, grid_n: int = 1000):
        """Plots the shear and bending moments. Returns figure"""
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(3, 2, figsize=(8.27, 11.69), dpi=100)
        for i in range(6):
            axx = ax[i // 2, i % 2]
            self._plot_component(axx, i, grid_n)

            if i == 4 or i == 5:
                axx.set_xlabel("X position [m]")

            try:
                from DAVE_reporting.helpers.format_mpl_plot import format_axes

                format_axes(axx)

            except ImportError:
                pass

        try:
            from DAVE_reporting.helpers.format_mpl_plot import apply_font

            apply_font(fig)
        except:
            pass

        return fig

    def plot(self, grid_n=100, merge_adjacent_loads=True, filename=None, do_show=False):
        """Plots the load, shear and bending moments. Returns figure"""
        m = self.datasource  # alias

        x = m.grid(grid_n)
        linewidth = 1

        n = m.nLoads

        import matplotlib.pyplot as plt

        #
        plt.rcParams.update({"font.family": "sans-serif"})
        plt.rcParams.update({"font.sans-serif": "consolas"})
        plt.rcParams.update({"font.size": 6})

        fig, (ax0, ax1, ax2) = plt.subplots(3, 1, figsize=(8.27, 11.69), dpi=100)
        textsize = 6

        # get loads

        loads = [m.load(i) for i in range(n)]

        texts = []  # for label placement
        texts_second = []  # for label placement

        # merge loads with same source and matching endpoints

        if merge_adjacent_loads:
            to_be_plotted = [loads[0]]

            for load in loads[1:]:
                name = load[2]

                # if the previous load is a continuous load from the same source
                # and the current load is also a continuous load
                # then merge the two.
                prev_load = to_be_plotted[-1]

                if len(prev_load[0]) != 2:  # not a point-load
                    if len(load[0]) != 2:  # not a point-load
                        if prev_load[2] == load[2]:  # same name
                            # merge the two
                            # remove the last (zero) entry of the previous lds
                            # as well as the first entry of these

                            # smoothed
                            xx = [*prev_load[0][:-1], *load[0][2:]]
                            yy = [
                                *prev_load[1][:-2],
                                0.5 * (prev_load[1][-2] + load[1][1]),
                                *load[1][2:],
                            ]

                            to_be_plotted[-1] = (xx, yy, load[2])

                            continue
                # else
                if np.max(np.abs(load[1])) > 1e-6:
                    to_be_plotted.append(load)

        else:
            to_be_plotted = loads

        #
        from matplotlib import cm

        colors = cm.get_cmap("hsv", lut=len(to_be_plotted))

        from matplotlib.patches import Polygon

        ax0_second = ax0.twinx()

        for icol, ld in enumerate(to_be_plotted):
            xx = ld[0]
            yy = ld[1]
            name = ld[2]

            if np.max(np.abs(yy)) < 1e-6:
                continue

            is_concentrated = len(xx) == 2

            # determine the name, default to Force / q-load if no name is present
            if name == "":
                if is_concentrated:
                    name = "Force "
                else:
                    name = "q-load "

            col = [0.8 * c for c in colors(icol)]
            col[3] = 1.0  # alpha

            if is_concentrated:  # concentrated loads on left axis
                lbl = f" {name} {ld[1][1]:.2f}"
                texts.append(
                    ax0.text(
                        xx[0], yy[1], lbl, fontsize=textsize, horizontalalignment="left"
                    )
                )
                ax0.plot(xx, yy, label=lbl, color=col, linewidth=linewidth)
                if yy[1] > 0:
                    ax0.plot(xx[1], yy[1], marker="^", color=col, linewidth=linewidth)
                else:
                    ax0.plot(xx[1], yy[1], marker="v", color=col, linewidth=linewidth)

            else:  # distributed loads on right axis
                lbl = f"{name}"  # {yy[1]:.2f} kN/m at {xx[0]:.3f}m .. {yy[-2]:.2f} kN/m at {xx[-1]:.3f}m"

                vertices = [(xx[i], yy[i]) for i in range(len(xx))]

                ax0_second.add_patch(
                    Polygon(vertices, facecolor=[col[0], col[1], col[2], 0.2])
                )
                ax0_second.plot(xx, yy, label=lbl, color=col, linewidth=linewidth)

                lx = np.mean(xx)
                ly = np.interp(lx, xx, yy)

                texts_second.append(
                    ax0_second.text(
                        lx,
                        ly,
                        lbl,
                        color=[0, 0, 0],
                        horizontalalignment="center",
                        fontsize=textsize,
                    )
                )

        ax0.grid()
        ax0.set_title("Loads")
        ax0.set_ylabel("Load [kN]")
        ax0_second.set_ylabel("Load [kN/m]")

        # plot moments
        # each concentrated load may have a moment as well
        for i in range(m.nLoads):
            mom = m.moment(i)
            if np.linalg.norm(mom) > 1e-6:
                load = m.load(i)
                xx = load[0][0]
                lbl = f"{load[2]}, m = {mom[1]:.2f} kNm"
                ax0.plot(xx, 0, marker="x", label=lbl, color=(0, 0, 0, 1))
                texts.append(
                    ax0.text(
                        xx, 0, lbl, horizontalalignment="center", fontsize=textsize
                    )
                )

        fig.legend(loc="upper right")

        # add a zero-line
        xx = [np.min(x), np.max(x)]
        ax0.plot(xx, (0, 0), "k-")

        from DAVE.gui.helpers.align_zeros_of_yyplots import align_y0_axis

        align_y0_axis(ax0, ax0_second)

        from DAVE.reporting.utils.TextAvoidOverlap import minimizeTextOverlap

        minimizeTextOverlap(
            texts_second,
            fig=fig,
            ax=ax0_second,
            vertical_only=True,
            optimize_initial_positions=False,
            annotate=False,
        )
        minimizeTextOverlap(
            texts,
            fig=fig,
            ax=ax0,
            vertical_only=True,
            optimize_initial_positions=False,
            annotate=False,
        )

        ax0.spines["top"].set_visible(False)
        ax0.spines["bottom"].set_visible(False)

        ax0_second.spines["top"].set_visible(False)
        ax0_second.spines["bottom"].set_visible(False)

        dx = (np.max(x) - np.min(x)) / 20  # plot scale
        ax1.plot(x, m.Vz, "k-", linewidth=linewidth)

        i = np.argmax(m.Vz)
        ax1.plot((x[i] - dx, x[i] + dx), (m.Vz[i], m.Vz[i]), "k-", linewidth=0.5)
        ax1.text(x[i], m.Vz[i], f"{m.Vz[i]:.2f}", va="bottom", ha="center")

        i = np.argmin(m.Vz)
        ax1.plot((x[i] - dx, x[i] + dx), (m.Vz[i], m.Vz[i]), "k-", linewidth=0.5)
        ax1.text(x[i], m.Vz[i], f"{m.Vz[i]:.2f}", va="top", ha="center")

        ax1.grid()
        ax1.set_title("Shear")
        ax1.set_ylabel("[kN]")

        ax2.plot(x, m.My, "k-", linewidth=linewidth)

        i = np.argmax(m.My)
        ax2.plot((x[i] - dx, x[i] + dx), (m.My[i], m.My[i]), "k-", linewidth=0.5)
        ax2.text(x[i], m.My[i], f"{m.My[i]:.2f}", va="bottom", ha="center")

        i = np.argmin(m.My)
        ax2.plot((x[i] - dx, x[i] + dx), (m.My[i], m.My[i]), "k-", linewidth=0.5)
        ax2.text(x[i], m.My[i], f"{m.My[i]:.2f}", va="top", ha="center")

        ax2.grid()
        ax2.set_title("Moment")
        ax2.set_ylabel("[kN*m]")

        try:
            from DAVE_reporting.helpers.format_mpl_plot import format_axes

            format_axes(ax1)
            format_axes(ax2)
        except ImportError:
            pass

        if do_show:
            plt.show()
        if filename is not None:
            fig.savefig(filename)

        return fig
