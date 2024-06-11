import tkinter as tk
from tkinter import ttk
import time
import numpy as np

class SignalTransformationGenerator:
    def __init__(self, container, operation, signal, visualizers):
        self.container = container
        self.sampling_rate_transformation = signal.parameters['sampling_rate_transformation']
        self.visualizers = visualizers

        self.signal, self.time = self.calculate_signal(signal)

        self.transform_last_used = ''
        self.executing_time = 0
        self.transform_x = []

        if operation == 'F1':
            self.transform_f1()
        elif operation == 'T1':
            self.transform_t1()

        self.transform_x = [i / len(self.transform) * self.sampling_rate_transformation for i in range(len(self.transform))]

    def return_tabs(self):
        new_tabs = []

        new_tabs.append(self.visualizers(self.container, self.transform_x, self.transform, self.transform_last_used))
        new_tabs.append(self.visualizers(self.container, self.transform_x, self.transform, self.transform_last_used, False))

        return new_tabs

    def calculate_signal(self, signal):

        process_signal = signal.signal
        process_time = signal.time

        signal = []
        time = []
        sample = process_time[0]
        for i, (x, y) in enumerate(
                zip(process_time, process_signal)):  # Przejście przez wszystkie punkty z listy sygnału oryginalnego
            while round(sample, 5) < round(x, 5):  # Jeśi punkt szukany jest mniejszy od x z listy oryginalnej dodaj punkty pośrednie
                time.append(round(sample, 5))
                signal.append(round(process_signal[i - 1], 5))  # Dodawanie y z poprzedniego x-a
                sample += (1 / self.sampling_rate_transformation)  # Przesuń do kolejnego punktu szukanego na podstawie próbokowania
            if round(sample, 5) == round(x, 5):  # Jeśli punkt szukany znajduje się na liście oryginalnej dodaj go
                time.append(round(sample, 5))
                signal.append(round(y, 5))
                sample += (1 / self.sampling_rate_transformation)

        if process_time[-1] != process_signal[-1]:
            time.append(process_time[-1])
            signal.append(process_signal[-1])

        return signal, time


    def transform_f1(self):
        self.transform_last_used = 'Szybka transformacja Fouriera z decymacją w dziedzinie czasu DIT FFT'
        self.executing_time, self.transform = self.measure(self.dit_fft, self.signal)
        self.transform_last_used += f' (czas: {self.executing_time} ms)'

    def transform_t1(self):
        self.transform_last_used = 'Transformacja kosinusowa typu drugiego DCT II'
        self.executing_time, self.transform = self.measure(self.dct_ii2, self.signal)
        self.transform_last_used += f' (czas: {self.executing_time} ms)'


    def measure(self, f, l):
        start_time = time.perf_counter()
        result = f(l)
        end_time = time.perf_counter()

        execution_time_sec = end_time - start_time

        execution_time_ms = execution_time_sec * 1000

        return execution_time_ms, result

    def zero_padding(self, x):
        N = len(x)
        N_padded = 1 << (N - 1).bit_length()
        padded_x = np.zeros(N_padded, dtype=complex)
        padded_x[:N] = x
        return padded_x

    def bit_reverse_copy(self, x):
        N = len(x)
        j = 0
        y = np.zeros(N, dtype=complex)
        for i in range(N):
            y[j] = x[i]
            m = N // 2
            while m >= 1 and j >= m:
                j -= m
                m //= 2
            j += m
        return y

    def dit_fft(self, x):
        x = self.zero_padding(x)
        N = len(x)
        stages = int(np.log2(N))
        x = self.bit_reverse_copy(x)

        for s in range(1, stages + 1):
            m = 2 ** s
            half_m = m // 2
            W_m = np.exp(-2j * np.pi / m)

            for k in range(0, N, m):
                W = 1
                for j in range(half_m):
                    t = W * x[k + j + half_m]
                    x[k + j + half_m] = x[k + j] - t
                    x[k + j] = x[k + j] + t
                    W *= W_m

        return x * 2 / len(x)

    def hadamard_matrix(self, n):
        if n == 1:
            return np.array([[1]])
        else:
            H_n = self.hadamard_matrix(n // 2)
            top = np.concatenate((H_n, H_n), axis=1)
            bottom = np.concatenate((H_n, -H_n), axis=1)
            H_2n = np.concatenate((top, bottom), axis=0)
            return H_2n

    def dct_ii2(self, x):
        N = len(x)
        X = np.zeros(N)
        factor = np.pi / (2 * N)

        for k in range(N):
            sum_val = 0
            for n in range(N):
                sum_val += x[n] * np.cos((2 * n + 1) * k * factor)
            if k == 0:
                X[k] = sum_val * np.sqrt(1 / N)
            else:
                X[k] = sum_val * np.sqrt(2 / N)

        return X.tolist()

    def fft_decimation_in_time_helper(self, x):
        N = len(x)

        if N <= 1:
            return x

        even = self.fft_decimation_in_time_helper(x[0::2])
        odd = self.fft_decimation_in_time_helper(x[1::2])

        factor = np.exp(-2j * np.pi * np.arange(N) / N)
        return np.concatenate([even + factor[:N // 2] * odd, even + factor[N // 2:] * odd]).tolist()

    def dct_ii2(self, ys):
        ys = self.zero_padding(ys)
        N = len(ys)
        transform = [complex(y) for y in ys]
        X = [0] * N

        for m in range(N):
            suma = 0
            for n in range(N):
                suma += transform[n] * np.cos(np.pi * (2 * n + 1) * m / (2 * N))
            X[m] = (np.sqrt(1 / N) if m == 0 else np.sqrt(2 / N)) * suma
        return X