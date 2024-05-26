import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        self.setInfo("")
        super(MplCanvas, self).__init__(self.fig)

    def refreshPlot(self, x, y, title, step = 0.1):
        if len(y) == 0:
            return
        self.fig.clear()
        self.axes = self.fig.add_subplot(111)
        self.axes.grid(True)
        self.axes.plot(x, y, c = 'blue')
        self.setInfo(title)
        self.axes.set_xticks(np.arange(x[0], x[-1]+step, step))
        self.draw()


    def setInfo(self, title):
            self.axes.set_title(title)
            self.axes.set_xlabel("Czas [s]")
            self.axes.set_ylabel("Amplituda [A]")
