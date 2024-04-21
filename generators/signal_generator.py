import tkinter as tk
from tkinter import ttk
import numpy as np
import random
import math

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

class SignalGenerator:
    def __init__(self, signal_type_var = None, parameters = None):
        self.parameters = {}
        for k in parameters:
            self.parameters[k] = parameters[k].get()

        self.signal = None
        self.original_signal = None
        self.signal_type = signal_type_var
        self.only_single_points = False
        self.hist_bins = self.parameters['hist_bins']
        self.amplitude = self.parameters['amplitude']
        self.f_multiplier = self.parameters['frequency']
        self.time = np.linspace(self.parameters['start_time'], self.parameters['start_time'] + self.parameters['duration'], int(self.f_multiplier))

    def return_params(self):
        return self.signal, self.time, self.hist_bins, self.signal_name, self.only_single_points

    def generate_signal(self):
        self.signal_name = SIGNAL_TYPES[self.signal_type]
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
            self.only_single_points = True
            self.signal = self.generate_unit_impulse()
        elif self.signal_type == "S11":
            self.only_single_points = True
            self.signal = self.generate_impulse_noise()

    def calculate_sine(self, t):
        return math.sin(2 * math.pi * t / self.parameters['period'])

    def calculate_term_position(self, t):
        return t / self.parameters['period'] - math.floor(t / self.parameters['period'])

    def generate_uniform_noise(self):
        return np.random.uniform(-self.parameters['amplitude'], self.parameters['amplitude'], size=self.f_multiplier)

    def generate_gaussian_noise(self):
        return np.random.normal(0, 1, len(self.time))

    def generate_sinusoidal(self):
        return [self.parameters['amplitude'] * self.calculate_sine(t) for t in self.time]

    def generate_half_wave_rectified_sine(self):
        return [0.5 * self.parameters['amplitude'] * (self.calculate_sine(t) + abs(self.calculate_sine(t))) for t in self.time]

    def generate_full_wave_rectified_sine(self):
        return [self.parameters['amplitude'] * abs(self.calculate_sine(t)) for t in self.time]

    def generate_square_wave(self):
        signal = [0] * len(self.time)
        for i, t in enumerate(self.time):
            if self.calculate_term_position(t) < self.parameters['fill_factor']:
                signal[i] = self.parameters['amplitude']
        return signal

    def generate_symmetric_square_wave(self):
        signal = [0] * len(self.time)
        for i, t in enumerate(self.time):
            if self.calculate_term_position(t) < self.parameters['fill_factor']:
                signal[i] = self.parameters['amplitude']
            else:
                signal[i] = -self.parameters['amplitude']
        return signal

    def generate_triangular_wave(self):
        signal = [0] * len(self.time)
        for i, t in enumerate(self.time):
            if self.calculate_term_position(t) < self.parameters['fill_factor']:
                signal[i] = self.calculate_term_position(t) / self.parameters['fill_factor'] * self.parameters['amplitude']
            else:
                signal[i] = (1 - (self.calculate_term_position(t) - self.parameters['fill_factor']) / (1 - self.parameters['fill_factor'])) * self.parameters['amplitude']
        return signal

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
