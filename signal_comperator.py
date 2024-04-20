import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import math

class SignalComperator(ttk.Frame):
    def __init__(self, container, first_signal, second_signal):
        super().__init__(container)

        self.first_signal = first_signal.signal
        self.second_signal = second_signal.signal
        self.time = first_signal.time
        fig = self.plot_signals()

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def plot_signals(self):
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(4, 4), subplot_kw={'frame_on': False})
        fig.subplots_adjust(hspace=0.8)

        ax1.plot(self.time, self.first_signal, label='Pierwszy sygnał')
        ax1.plot(self.time, self.second_signal, label='Drugi sygnał')

        ax1.set_title(f'Wykres porównania funkcji')
        ax1.set_xlabel('Czas')
        ax1.set_ylabel('Amplituda')

        mse, snr, psnr, md, enob = self.calculate_statistics()
        stats_text = f"Błąd środniokwadratowy: {mse:.4f}\nStosunek sygnał - szum: {snr:.4f}\nSzczytowy stosunek sygnał - szum: {psnr:.4f}\nMaksymalna różnica: {md:.4f}\nEfektywna liczba bitów: {enob:.4f}"

        ax2.text(0.3, 0.5, stats_text, ha='left', va="center", fontsize=12, transform=ax2.transAxes)
        ax2.axis('off')

        return fig

    def calculate_statistics(self):
        mse = sum((x - y)**2 for x, y in zip(self.first_signal, self.second_signal)) / len(self.first_signal)
        if mse == 0:
            snr = float('inf')
            psnr = float('inf')
            enob = float('inf')
        else:
            snr = 10 * math.log10(sum(x**2 for x in self.first_signal) / mse)
            psnr = 10 * math.log10(1 / mse)
            enob = (snr - 1.76) / 6.02
        md = max(abs(x - y) for x, y in zip(self.first_signal, self.second_signal))
        return mse, snr, psnr, md, enob