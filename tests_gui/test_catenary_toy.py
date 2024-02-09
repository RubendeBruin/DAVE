from DAVEcore import ElasticCatenary
import matplotlib.pyplot as plt
import numpy as np


import matplotlib.pyplot as plt

class DraggableMarker:
    def __init__(self, markers, ax, line, samples):
        self.markers = markers
        self.ax = ax
        self.dragging = None
        self.line = line
        self.samples = samples

    def connect(self):
        'connect to all the events we need'
        self.cidpress = self.ax.figure.canvas.mpl_connect(
            'button_press_event', self.on_press)
        self.cidrelease = self.ax.figure.canvas.mpl_connect(
            'button_release_event', self.on_release)
        self.cidmotion = self.ax.figure.canvas.mpl_connect(
            'motion_notify_event', self.on_motion)

    def on_press(self, event):
        'on button press we will see if the mouse is over us and store some data'
        if event.inaxes != self.markers[0].axes: return

        for i, marker in enumerate(self.markers):
            contains, _ = marker.contains(event)
            if contains:
                self.dragging = i
                return

    def on_motion(self, event):
        'on motion we will move the marker if the mouse is over us'
        if self.dragging is None: return
        if event.inaxes != self.markers[self.dragging].axes: return

        self.markers[self.dragging].set_data([event.xdata, event.ydata])

        # update the plot
        self.update_catenary()

        self.ax.figure.canvas.draw()

    def on_release(self, event):
        'on release we reset the press data'
        self.dragging = None

    def update_catenary(self):
        # get the points
        pts = np.array([marker.get_data() for marker in self.markers])
        p1 = [pts[0][0], 0, pts[0][1]]
        p2 = [pts[1][0], 0, pts[1][1]]
        cat = ElasticCatenary(*p1, *p2, 1000, 2, 0.5)
        pts = cat.GetPoints(100)

        self.line.set_data([p[0] for p in pts], [p[2] for p in pts])

        # loop over the points in self.samples
        colors = []

        for x,z in zip(self.samples.get_offsets()[:,0], self.samples.get_offsets()[:,1]):
            zdist = cat.Contacts(x,0, z)
            colors.append(zdist)

        self.samples.set_array(colors)
        # self.samples.set_cmap('Pastel2')



# create a new figure with an axes
fig, ax = plt.subplots()

# plot two markers
markers = [ax.plot([0], [0], marker='o', markersize=10)[0],
           ax.plot([1], [1], marker='o', markersize=10)[0]]

line = ax.plot([0,1], [0,1], color='k')[0]

xs = np.linspace(-1, 1, 25)
zs = np.linspace(-1, 1, 25)
xx = []
zz = []
cols = []
for x in xs:
    for z in zs:
        xx.append(x)
        zz.append(z)
        cols.append(x*z)


samples = ax.scatter(xx,zz, c = cols, cmap="coolwarm")

# create the draggable marker
dm = DraggableMarker(markers, ax, line, samples)

# connect the event handlers
dm.connect()


ax.set_title('Click and drag a marker to move it')

# show the plot
plt.show()
