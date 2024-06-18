import tkinter as tk
from tkinter import ttk
import cmath
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

class SignalTransformation(ttk.Frame):
    def __init__(self, container, transform_x, transform, transform_last_used, module_phase = True, line = True):
        super().__init__(container)
        self.transform_x = transform_x
        self.transform = transform
        self.transform_last_used = transform_last_used
        self.module_phase = module_phase
        self.line = line

        self.plot_signals()

    def plot_signals(self):
        x, y = self.transform_x, self.transform

        if len(y) == 0:
            return

        fig = Figure(figsize=(4, 5), dpi=100)
        axes = fig.add_subplot(211)

        fig.suptitle(self.transform_last_used)
        axes.grid(True)

        module_phase = True
        line = True


        if self.module_phase:
            real = np.real(self.transform)
            imag = np.imag(self.transform)

            if self.line:
                axes.plot(x, real , c = 'blue')
            axes.scatter(x, real , c = 'red')
            axes.set_title(f'')
            axes.set_xlabel("Częstotliwość")
            axes.set_ylabel("Część rzeczywista")
            axes2 = fig.add_subplot(212)
            axes2.grid(True)
            if self.line:
                axes2.plot(x, imag, c = 'blue')
            axes2.scatter(x, imag, c = 'red')
            axes2.set_title(f'')
            axes2.set_xlabel("Częstotliwość")
            axes2.set_ylabel("Część urojona")
        else:

            modules = np.abs(self.transform)
            argument = np.angle(self.transform)

            if self.line:
                axes.plot(x, modules, c='blue')
            axes.scatter(x, modules, c='red')
            axes.set_title(f'')
            axes.set_xlabel("Częstotliwość")
            axes.set_ylabel("Moduł")
            axes2 = fig.add_subplot(212)
            axes2.grid(True)
            if self.line:
                axes2.plot(x, argument, c='blue')
            axes2.scatter(x, argument, c='red')
            axes2.set_title(f'')
            axes2.set_xlabel("Częstotliwość")
            axes2.set_ylabel("Faza")



        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)