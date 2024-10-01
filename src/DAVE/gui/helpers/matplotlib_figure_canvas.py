"""MplCanvas class for embedding matplotlib figures in Qt widgets
includes fix/workaround for missing window handle when used in combination with ADS
"""
import warnings

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=72, fig = None):
        if fig is None:
            fig = Figure(figsize=(width, height), dpi=dpi)
            self.axes = fig.add_subplot(111)

        super(MplCanvas, self).__init__(fig)
        self.setParent(parent)

    def showEvent(self, event):
        # see https://github.com/githubuser0xFFFF/Qt-Advanced-Docking-System/issues/579
        # for why this is needed

        # check window handle, only execute if it is valid
        window = self.window().windowHandle()
        try:
            a = str(window)
        except:
            warnings.warn("window handle not valid, not executing matplotlib showEvent")
            return

        super().showEvent(event)