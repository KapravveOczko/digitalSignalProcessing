import matplotlib.pyplot as plt
import numpy as np
import operator

from utils import sinusoidal_signal_for_antenna, correlation

class Transmitter:
    def __init__(self, amount_of_measurements, time_unit, real_object_speed, signal_speed, signal_period,
                 sampling_frequency, buffers_length, reporting_period):
        self.amount_of_measurements = amount_of_measurements
        self.time_unit = time_unit
        self.real_object_speed = real_object_speed
        self.signal_speed = signal_speed
        self.signal_period = signal_period
        self.sampling_frequency = sampling_frequency
        self.buffers_length = buffers_length
        self.reporting_period = reporting_period
        self.probing_signal = None
        self.feedback_signal = None
        self.correlation_samples = None
        self.time_values = None
        self.px = None
        self.fx = None
        self.px2 = None
        self.duration = None

    def original_distance(self):
        return np.array([i * self.real_object_speed for i in
                         np.arange(0, self.amount_of_measurements * self.reporting_period, self.reporting_period)])

    def distances(self):
        result = []
        amplitude = 3.0
        duration = self.buffers_length / self.sampling_frequency

        self.time_values = []
        for i in np.arange(0, self.amount_of_measurements * self.reporting_period, self.reporting_period):
            self.time_values.append(i)
            current_distance = i * self.real_object_speed
            propagation_time = 2 * current_distance / self.signal_speed

            self.probing_signal, px = self.signal(amplitude, self.signal_period, i - duration, duration, self.sampling_frequency)
            self.feedback_signal, fx = self.signal(amplitude, self.signal_period, i - duration + propagation_time, duration, self.sampling_frequency)
            self.correlation_samples = correlation(self.probing_signal, self.feedback_signal)
            result.append(self.distance(self.correlation_samples, self.sampling_frequency, self.signal_speed))

        return np.array(result)

    def distance(self, correlation_samples, frequency, signal_speed):
        right_half = correlation_samples[int(len(correlation_samples) / 2): len(correlation_samples) - 1]
        max_sample = right_half.index(max(right_half))
        t_delay = max_sample / frequency

        return round(((t_delay * signal_speed) / 2), 6)

    def signal(self, amplitude, period, startTime, duration, frequency):
        samples = []
        new_samples = []

        for j in np.arange(startTime, startTime + duration, 1 / frequency):
            new_samples.append(sinusoidal_signal_for_antenna(amplitude, period, j))
        samples = list(map(operator.add, new_samples, samples)) if len(samples) != 0 else new_samples

        return samples, [j for j in np.arange(startTime, startTime + duration, 1 / frequency)]

    def create_plots(self, start_time = 0.0):
        amplitude = 1.0
        self.duration = self.buffers_length / self.sampling_frequency

        i = self.amount_of_measurements * self.reporting_period + self.reporting_period

        current_distance = start_time * self.real_object_speed
        propagation_time = 2 * current_distance / self.signal_speed
        self.probing_signal, self.px = self.signal(amplitude, self.signal_period, start_time, self.duration, self.sampling_frequency)
        self.feedback_signal, self.fx = self.signal(amplitude, self.signal_period, start_time + propagation_time, self.duration, self.sampling_frequency)
        self.correlation_samples = correlation(self.probing_signal, self.feedback_signal)

        step = round(self.px[1] - self.px[0],5)
        size = len(self.correlation_samples)
        self.px2 = np.linspace(min(self.px), min(self.px) + step * size, size)

    def calculate_all(self, precision = 4):
        original_vales = self.original_distance()
        received_values = self.distances()
        diff = np.round(np.fabs(original_vales - received_values), precision)
        return original_vales, received_values, diff
