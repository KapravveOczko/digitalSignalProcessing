import tkinter as tk
from tkinter import ttk
import numpy as np
import random

from scipy.signal import butter, filtfilt

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
    "S12": "funkcja S1",
    "S13": "funkcja S2",
    "S14": "funkcja S3",
    "F1": "filtr dolnoprzepustowy",
    "F2": "filtr pasmowy",
    "F3": "filtr górnoprzepustowy",
}

WINDOW_TYPES = {
    "W1": "prostokątne",
    "W2": "Hanninga",
    "W3": "Hamminga",
    "W4": "Blackmana",
}

class SignalGenerator:
    def __init__(self, signal_type_var = None, parameters = None):
        self.parameters = {}
        for k in parameters:
            if k == 'card_to_filter':
                self.parameters['card_to_filter'] = parameters[k]
                continue
            self.parameters[k] = parameters[k].get()

        self.signal = None
        self.original_signal = None
        self.signal_type = signal_type_var
        self.only_single_points = False

        self.fd = self.parameters['sampling_rate']
        self.M = int(np.power(self.parameters['order'], 1/3))

        # if self.M % 2 == 0:
        #     raise Exception("Order of filter must be odd")

        self.f0 = self.parameters['cut_off_frequency']

        windows_types_keys = list(WINDOW_TYPES.keys())
        windows_types_values = list(WINDOW_TYPES.values())
        self.window_type = windows_types_keys[windows_types_values.index(self.parameters['window_type'])]
        self.window = self.get_window()

        self.hist_bins = self.parameters['hist_bins']
        self.amplitude = self.parameters['amplitude']
        self.f_multiplier = self.parameters['frequency']

        start = self.parameters['start_time']
        end = self.parameters['start_time'] + self.parameters['duration']

        self.time = np.linspace(start, end, int(self.f_multiplier * end))

        # if self.signal_type in ["S12", "S13", "S14"]:
        #     self.time = np.linspace(start, end, self.f_multiplier, endpoint=False)

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
        elif self.signal_type == "S12":
            self.signal = self.calculate_s1(self.time)
        elif self.signal_type == "S13":
            self.signal = self.calculate_s2(self.time)
        elif self.signal_type == "S14":
            self.signal = self.calculate_s3(self.time)
        elif self.signal_type == "F1":
            self.signal = self.generate_low_pass_filter()
        elif self.signal_type == "F2":
            self.signal = self.generate_band_pass_filter()
        elif self.signal_type == "F3":
            self.signal = self.generate_high_pass_filter()

        if self.signal_type in ["F1", "F2", "F3"]:
            if self.parameters['card_to_filter'] is not None:
                start = self.parameters['card_to_filter'].time[0]
                end = self.parameters['card_to_filter'].time[-1]
                # self.signal = np.convolve(self.parameters['card_to_filter'].signal, self.signal, mode='full')
                if self.signal_type == "F1":
                    self.signal = self.butter_lowpass_filter(self.parameters['card_to_filter'].signal)
                if self.signal_type == "F2":
                    self.signal = self.butter_bandpass_filter(self.parameters['card_to_filter'].signal)
                if self.signal_type == "F3":
                    self.signal = self.butter_highpass_filter(self.parameters['card_to_filter'].signal)
                self.time = np.linspace(start, end, len(self.signal), endpoint=False)
                self.signal_name = "Przefiltrowanego sygnału"

            else:
                self.only_single_points = True
                self.time = [i * (self.M / len(self.signal)) for i in range(len(self.signal))]


    def butter_lowpass_filter(self, data):
        normal_cutoff = self.f0 / (0.5 * self.fd)
        b, a = butter(self.M, normal_cutoff, btype='lowpass', analog=False)
        y = filtfilt(b, a, data)
        return y

    def butter_highpass_filter(self, data):
        normal_cutoff = self.f0 / (0.5 * self.fd)
        b, a = butter(self.M, normal_cutoff, btype='highpass', analog=False)
        y = filtfilt(b, a, data)
        return y

    def butter_bandpass_filter(self, data):
        normal_cutoff = self.f0 / (0.5 * self.fd)
        b, a = butter(self.M, normal_cutoff, btype='bandpass', analog=False)
        y = filtfilt(b, a, data)
        return y

    def get_window(self):
        if self.window_type == "W1":
            return self.recengle_window
        elif self.window_type == "W2":
            return self.hanning_window
        elif self.window_type == "W3":
            return self.hamming_window
        elif self.window_type == "W4":
            return self.blackman_window

    def recengle_window(self, n):
        return 1.0

    def hanning_window(self, n):
        return 0.5 - 0.5 * np.cos(2 * np.pi * n / self.M)

    def hamming_window(self, n):
        return 0.53836 - 0.46164 * np.cos(2 * np.pi * n / self.M)

    def blackman_window(self, n):
        return 0.42 - 0.5 * np.cos(2.0 * np.pi * n / self.M) + 0.08 * np.cos(4.0 * np.pi * n / self.M)

    def calculate_s1(self, t):
        # return [2 * np.sin(np.pi * t + np.pi / 2) + 5 * np.sin(4 * np.pi * t + np.pi / 2) for t in t]
        return 2 * np.sin((2 * np.pi / 2) * t + np.pi / 2) + 5 * np.sin((2 * np.pi / 0.5) * t + np.pi / 2)

    def calculate_s2(self, t):
        return [2 * np.sin(np.pi * t) + np.sin(2 * np.pi * t) + 5 * np.sin(4 * np.pi * t) for t in t]

    def calculate_s3(self, t):
        return [5 * np.sin(np.pi * t) + 5 * np.sin(8 * np.pi * t) for t in t]

    def calculate_sine(self, t):
        return np.sin(2 * np.pi * t / self.parameters['period'])

    def pass_filter(self, value_function):
        return [value_function(n) for n in range(self.M)]

    def low_pass_filter_value(self, n):
        k = self.fd / self.f0
        c = int((self.M - 1) / 2)
        if n == c:
            result = 2.0 / k
        else:
            result = np.sin(2.0 * np.pi * (n - c) / k) / (np.pi * (n - c))

        return result * self.window(n)


    def band_pass_filter_value(self, n):
        return self.low_pass_filter_value(n) * 2.0 * np.sin(np.pi * n / 2.0)


    def high_pass_filter_value(self, n):
        return self.low_pass_filter_value(n) * np.power(-1, n)


    def generate_low_pass_filter(self):
        return self.pass_filter(self.low_pass_filter_value)

    def generate_band_pass_filter(self):
        return self.pass_filter(self.band_pass_filter_value)

    def generate_high_pass_filter(self):
        return self.pass_filter(self.high_pass_filter_value)

    def calculate_term_position(self, t):
        return t / self.parameters['period'] - np.floor(t / self.parameters['period'])

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
