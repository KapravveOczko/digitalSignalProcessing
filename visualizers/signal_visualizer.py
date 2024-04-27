import numpy as np
import matplotlib.pyplot as plt

class SignalVisualizer:
    def __init__(self, signal, time, hist_bins, signal_name, only_single_points=False):
        self.signal = signal
        self.time = time
        self.hist_bins = hist_bins
        self.signal_name = signal_name
        self.only_single_points = only_single_points

    def plot_signal(self):
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(4, 4), subplot_kw={'frame_on': False})
        fig.subplots_adjust(hspace=0.8)

        if self.only_single_points:
            ax1.plot(self.time, self.signal, 'o')
        else:
            ax1.plot(self.time, self.signal)

        ax1.set_title(f'Wykres funkcji {self.signal_name}')
        ax1.set_xlabel('Czas')
        ax1.set_ylabel('Amplituda')

        ax2.hist(self.signal, bins=self.hist_bins, edgecolor="black", alpha=0.75, density=True)
        ax2.set_title(f'Histogram funkcji {self.signal_name}')
        ax2.set_xlabel('Amplituda')
        ax2.set_ylabel('Częstotliwość')

        mean_value, abs_mean_value, rms_value, variance, power = self.calculate_statistics()
        stats_text = f"Wartość średnia sygnału: {mean_value:.4f}\nWartość średnia bezwzględna sygnału: {abs_mean_value:.4f}\nWartość skuteczna sygnału: {rms_value:.4f}\nWariancja sygnału: {variance:.4f}\nMoc średnia sygnału: {power:.4f}"

        ax3.text(0.3, 0.5, stats_text, ha='left', va="center", fontsize=12, transform=ax3.transAxes)
        ax3.axis('off')

        return fig

    def calculate_statistics(self):
        N = len(self.signal)
        mean_value = sum(self.signal) / N
        abs_mean_value = sum(abs(x) for x in self.signal) / N
        rms_value = (sum(x**2 for x in self.signal) / N)**0.5
        variance = sum((x - mean_value)**2 for x in self.signal) / N
        power = sum(x**2 for x in self.signal) / N
        return mean_value, abs_mean_value, rms_value, variance, power