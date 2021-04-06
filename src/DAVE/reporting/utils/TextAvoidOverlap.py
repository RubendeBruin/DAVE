import matplotlib.pyplot as plt
import numpy as np

def minimizeTextOverlap(texts, fig, ax, horizontal_only = False, vertical_only = False, maxiter = 100, tolerance = 0.001, annotate =True, optimize_initial_positions=True):

    # get text sizes
    plt.draw()
    r = fig.canvas.get_renderer()
    expand = (1.0, 1.0)

    class Box():
        def __init__(self, position, left, right, bottom, top):
            self.x = position[0]
            self.y = position[1]

            self.x0 = self.x
            self.y0 = self.y

            self.x_best = self.x
            self.y_best = self.y

            self.dl = self.x - left
            self.dr = right - self.x
            self.du = top - self.y
            self.dd = self.y - bottom
            self.to_be_moved = np.array((0,0), dtype=float)



        def move(self, dx, dy):
            self.x += dx
            self.y += dy

        def reset(self):
            self.to_be_moved = np.array((0,0), dtype=float)

        def do_move(self):
            self.move(*self.to_be_moved)

        def set_best(self):
            self.x_best = self.x
            self.y_best = self.y

        # def move_to_best(self):
        #     self.x = self.x_best
        #     self.y = self.y_best

        @property
        def cx(self):
            return self.x + 0.5 * self.dr - 0.5*self.dl

        @property
        def cy(self):
            return self.y + 0.5 * self.du - 0.5*self.dd

        @property
        def width(self):
            return self.dr + self.dl

        @property
        def height(self):
            return self.du + self.dd

        @property
        def r(self):
            return ((0.5*self.width)**2 + (0.5*self.height)**2 ) ** (0.5)

        @property
        def left(self):
            return self.x - self.dl

        @property
        def right(self):
            return self.x + self.dr

        @property
        def top(self):
            return self.y + self.du

        @property
        def bottom(self):
            return self.y - self.dd

        def plot_home(self, ax):
            ax.plot((self.x, self.x0),
                    (self.y, self.y0),
                    linewidth = 1,
                    color = [0.5, 0.5, 0.5])

        def plot_box(self, ax):

            if self.width == 0 or self.height == 0:
                ax.plot(self.cx, self.cy, 'r.')
            else:
                ax.plot([self.left, self.left, self.right, self.right, self.left],
                        [self.bottom, self.top, self.top, self.bottom, self.bottom])

        def add_force_to_home(self, factor = 0.1):
            dx = self.cx - self.x0
            dy = self.cy - self.y0

            self.to_be_moved[0] = self.to_be_moved[0] - factor * dx
            self.to_be_moved[1] = self.to_be_moved[1] - factor * dy

        def add_force_from(self, other, factor = 1.2, vertical_only = False, horizontal_only = False):

            # if not overlap then we are done
            if other.left > self.right:
                return 0
            if other.right < self.left:
                return 0
            if other.top < self.bottom:
                return 0
            if other.bottom > self.top:
                return 0


            ry = 0.5 * (other.height + self.height)
            oy = self.cy - other.cy

            rx = 0.5 * (other.width + self.width)
            ox = self.cx - other.cx

            dx=0
            dy=0

            if not vertical_only:
                ho = rx - abs(ox) # horizontal overlap
                if ho > 0:
                    if ox == 0:  # avoid div by 0
                        if np.random.rand(1) > 0.5:
                            ox = 1
                        else:
                            ox = -1
                    dx = factor * 0.5 * ox * ho / abs(ox)
                    self.to_be_moved[0] += dx


            if not horizontal_only:
                vo = ry - abs(oy)  # vertical overlap
                if vo > 0:
                    if oy == 0:  # avoid div by 0
                        if np.random.rand(1) > 0.5:
                            oy=1
                        else:
                            oy=-1

                    dy =  factor * 0.5 * oy * vo / abs(oy)
                    self.to_be_moved[1] +=dy

                    # print(dy)

            return (dx**2 + dy**2)**(0.5)

    boxes = []
    points = []

    for i in texts:
        ext = i.get_window_extent(r).expanded(*expand).transformed(ax.transData.inverted())
        x, y = i.get_position()

        boxes.append(Box(i.get_position(), left = ext.xmin, right = ext.xmax, top = ext.ymax, bottom = ext.ymin))
        points.append(Box(i.get_position(), x,x,y,y))

    # initial positioning - position each box on the side of its target point where it has the lowest amount of overlap

    if optimize_initial_positions:
        for b in boxes:

            xx = (-0.5*b.width, 0, 0.5*b.width, 0)
            yy = (0, 0.5*b.height, 0, -0.5*b.height)

            r = []
            for dx, dy in zip(xx,yy):
                ri = 0
                for bb in boxes:
                    if b == bb:
                        continue
                    b.move(dx,dy)
                    ri += b.add_force_from(bb)
                    b.move(-dx, -dy)
                r.append(ri)
            b.reset()
            imin = np.argmin(r)
            b.move(xx[imin], yy[imin])


    best = 1e20
    for i in range(maxiter):

        # move text towards point
        # for b in boxes:
        #     dx = b.cx - b.x0
        #     dy = b.cy - b.y0
        #     b.move(-0.05*dx,-0.05*dy)

        # repel from boxes and points
        total_move = 0
        for b in boxes:
            for bb in boxes:
                if b == bb:
                    continue
                total_move += b.add_force_from(bb, vertical_only = vertical_only, horizontal_only=horizontal_only)

            for p in points:
                total_move += b.add_force_from(p, vertical_only = vertical_only, horizontal_only=horizontal_only)

            # move one by one?
            b.do_move()
            b.reset()

        if total_move <= tolerance:
            break

        # print(total_move)

        # and do the actual move
        for b in boxes:
            b.do_move()
            b.reset()

        # print(total_move)
        if total_move < best:  # more than a factor 2 worse
            best = total_move
            for b in boxes:
                b.set_best()

    # only in the end move the text elements
    for t,b in zip(texts, boxes):
        t.set_position((b.x_best, b.y_best))

    # annotation arrows
    if annotate:
        for b in boxes:
            b.plot_home(ax)

if __name__ == '__main__':

    np.random.seed(0)
    x, y = np.random.random((2, 80))

    # adjust text
    fig, ax = plt.subplots()
    plt.plot(x, y, 'bo')
    texts = [plt.text(x[i], y[i], 'Text%s' % i, ha='center', va='center') for i in range(len(x))]

    minimizeTextOverlap(texts, fig, ax, optimize_initial_positions=True)

    plt.show()