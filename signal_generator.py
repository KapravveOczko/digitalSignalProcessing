import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import numpy as np
import matplotlib.pyplot as plt
import random
import math
import struct

SIGNAL_TYPES = {
    "S1": "szum o rozkładzie jednostajnym",
    "S2": "szum gaussowski",
    "S3": "sygnał sinusoidalny",
    "S4": "sygnał sinusoidalny wyprostowany jednopołówkowo",
    "S5": "sygnał sinusoidalny wyprostowany dwupołówkowo",
    "S6": "sygnał prostokątny",
    "S7": "sygnał prostokątny symetryczny",
    "S8": "sygnał trójkątny",
    "S9": "skok jednostkowy",
    "S10": "impuls jednostkowy",
    "S11": "szum impulsowy",
}

OPERATION_TYPES = {
    'D1': 'Dodawanie',
    'D2': 'Odejmowanie',
    'D3': 'Mnożenie',
    'D4': 'Dzielenie',
}

class SignalGenerator:
    def __init__(self, signal_type_var = None, parameters = None):
        if signal_type_var and parameters:
            self.signal_type = signal_type_var
            self.parameters = parameters
            self.signal = None
            self.f_multiplier = self.parameters['frequency']
            self.time = np.linspace(self.parameters['start_time'], self.parameters['start_time'] + self.parameters['duration'], int(self.f_multiplier))
        else:
            self.signal_type = ""
            self.parameters = {'hist_bins': 10}
            self.signal = None
            self.f_multiplier = None
            self.time = None

    def generate_signal(self):
        if self.signal_type == "S1":
            self.signal = self.generate_uniform_noise()
        elif self.signal_type == "S2":
            self.signal = self.generate_gaussian_noise()
        elif self.signal_type == "S3":
            self.signal = self.generate_sinusoidal()
        elif self.signal_type == "S4":
            self.signal = self.generate_half_wave_rectified_sine()
        elif self.signal_type == "S5":
            self.signal = self.generate_full_wave_rectified_sine()
        elif self.signal_type == "S6":
            self.signal = self.generate_square_wave()
        elif self.signal_type == "S7":
            self.signal = self.generate_symmetric_square_wave()
        elif self.signal_type == "S8":
            self.signal = self.generate_triangular_wave()
        elif self.signal_type == "S9":
            self.signal = self.generate_unit_step()
        elif self.signal_type == "S10":
            self.signal = self.generate_unit_impulse()
        elif self.signal_type == "S11":
            self.signal = self.generate_impulse_noise()

    def generate_signal_from_two_signals(self, operation, first_signal, second_signal):
        self.f_multiplier = len(first_signal)
        self.time = np.linspace(0, 10, self.f_multiplier, endpoint=False)

        if operation == 'D1':
            self.signal = np.add(first_signal, second_signal)
        elif operation == 'D2':
            self.signal = np.subtract(first_signal, second_signal)
        elif operation == 'D3':
            self.signal = np.multiply(first_signal, second_signal)
        elif operation == 'D4':
            self.signal = np.divide(first_signal, second_signal)

    def plot_signal(self):
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(4, 4), subplot_kw={'frame_on': False})
        fig.subplots_adjust(hspace=0.8)

        ax1.plot(self.time, self.signal)

        if not self.signal_type:
            signal_type_name = "2 sygnałów"
        else:
            signal_type_name = SIGNAL_TYPES[self.signal_type]

        ax1.set_title(f'Wykres funkcji {signal_type_name}')
        ax1.set_xlabel('Czas')
        ax1.set_ylabel('Amplituda')

        ax2.hist(self.signal, bins=self.parameters['hist_bins'], edgecolor="black", alpha=0.75, density=True)
        ax2.set_title(f'Histogram funkcji {signal_type_name}')
        ax2.set_xlabel('Amplituda')
        ax2.set_ylabel('Częstotliwość')

        mean_value, abs_mean_value, rms_value, variance, power = self.calculate_statistics(self.signal)
        stats_text = f"Wartość rednia sygnału: {mean_value:.4f}\nWartość średnia bezwzględna sygnału: {abs_mean_value:.4f}\nWartość skuteczna sygnału: {rms_value:.4f}\nWariancja sygnału: {variance:.4f}\nMoc średnia sygnału: {power:.4f}"

        ax3.text(0.3, 0.5, stats_text, ha='left', va="center", fontsize=12, transform=ax3.transAxes)
        ax3.axis('off')

        return fig

    def calculate_statistics(self, signal):
        N = len(signal)
        mean_value = sum(signal) / N
        abs_mean_value = sum(abs(x) for x in signal) / N
        rms_value = (sum(x**2 for x in signal) / N)**0.5
        variance = sum((x - mean_value)**2 for x in signal) / N
        power = sum(x**2 for x in signal) / N
        return mean_value, abs_mean_value, rms_value, variance, power

    def save_to_file(self, path):
        with open(path, 'wb') as file:
            file.write(struct.pack('d', self.parameters['start_time']))
            file.write(struct.pack('d', self.parameters['duration']))
            file.write(struct.pack('d', self.f_multiplier))
            file.write(struct.pack('d', int(self.signal_type[1::])))
            for point in self.signal:
                file.write(struct.pack('d', point))

    def read_from_file(self, path):
        with open(path, 'rb') as file:
            self.signal = []
            self.parameters['start_time'] = struct.unpack('d', file.read(8))[0]
            self.parameters['duration'] = struct.unpack('d', file.read(8))[0]
            self.f_multiplier = struct.unpack('d', file.read(8))[0]
            self.signal_type = 'S' + str(int(struct.unpack('d', file.read(8))[0]))
            self.time = np.linspace(self.parameters['start_time'], self.parameters['start_time'] + self.parameters['duration'], int(self.f_multiplier), endpoint=False)
            while True:
                point = file.read(8)
                if not point:
                    break
                self.signal.append(struct.unpack('d', point)[0])

    def generate_uniform_noise(self):
        return np.random.uniform(-self.parameters['amplitude'], self.parameters['amplitude'], size=self.f_multiplier)

    def generate_gaussian_noise(self):
        return np.random.normal(0, 1, len(self.time))

    def generate_sinusoidal(self):
        return [self.parameters['amplitude'] * math.sin(2 * math.pi * t / self.parameters['period']) for t in self.time]

    def generate_half_wave_rectified_sine(self):
        return [max(self.parameters['amplitude'] * math.sin(2 * math.pi * t / self.parameters['period']), 0) for t in self.time]

    def generate_full_wave_rectified_sine(self):
        return [abs(self.parameters['amplitude'] * math.sin(2 * math.pi * t / self.parameters['period'])) for t in self.time]

    def generate_square_wave(self):
        return [max(self.parameters['amplitude'] * (1 if math.sin(2 * math.pi * t / self.parameters['period']) >= 0 else -1), 0) for t in self.time]

    def generate_symmetric_square_wave(self):
        return [self.parameters['amplitude'] * (1 if math.sin(math.pi * t / self.parameters['period']) >= 0 else -1) for t in self.time]

    def generate_triangular_wave(self):
        return [self.parameters['amplitude'] * abs(2 * ((t / self.parameters['period']) - math.floor(self.parameters['fill_factor'] + t / self.parameters['period']))) for t in self.time]

    def generate_unit_step(self):
        signal = [0] * len(self.time)

        for i in range(len(self.time)):
            if self.time[i] > self.parameters['time_shift']:
                signal[i] = self.parameters['amplitude']
            if self.time[i] == self.parameters['time_shift']:
                signal[i] = self.parameters['amplitude'] / 2

        return signal

    def generate_unit_impulse(self):
        signal = [0] * len(self.time)
        signal[self.parameters['jump_number']] = self.parameters['amplitude']
        return signal

    def generate_impulse_noise(self):
        signal = [0] * len(self.time)
        impulse_indices = [i for i in range(len(self.time)) if random.random() < self.parameters['probability']]
        for i in impulse_indices:
            signal[i] = self.parameters['amplitude']
        return signal
