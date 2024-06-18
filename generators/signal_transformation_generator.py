import tkinter as tk
from tkinter import ttk
import time
import numpy as np

class SignalTransformationGenerator:
    def __init__(self, container, operation, signal, visualizers):
        self.container = container
        self.sampling_rate = signal.parameters['frequency']
        self.visualizers = visualizers
        self.signal = signal.signal
        self.signal = self.zero_padding(self.signal)

        self.transform_last_used = ''
        self.executing_time = 0
        self.transform_x = []

        if operation == 'F1':
            self.transform_f1()
        elif operation == 'F1-DIT':
            self.transform_f1_dit()
        elif operation == 'T1':
            self.transform_t1()


        N = len(self.signal)
        self.transform_x = np.linspace(0, self.sampling_rate, N, endpoint=False)
        self.transform = self.transform / N


    def return_tabs(self):
        new_tabs = []

        new_tabs.append(self.visualizers(self.container, self.transform_x, self.transform, self.transform_last_used))
        new_tabs.append(self.visualizers(self.container, self.transform_x, self.transform, self.transform_last_used, False))

        return new_tabs

    def transform_f1(self):
        self.transform_last_used = 'Szybka transformacja Fouriera FFT'
        self.executing_time, self.transform = self.measure(self.fft, self.signal)
        self.transform_last_used += f' (czas: {self.executing_time} ms)'

    def transform_f1_dit(self):
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

    def fft(self, x):
        N = len(x)

        if N == 1:
            return x
        x_even = self.fft(x[::2])
        x_odd = self.fft(x[1::2])
        factor = np.exp(-2j * np.pi * np.arange(N) / N)

        X = np.concatenate([x_even + factor[:N//2] * x_odd, x_even + factor[N//2:] * x_odd])
        return X

    def dit_fft(self, x):
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

        return x

    def dct_ii2(self, ys):
        N = len(ys)
        transform = [complex(y) for y in ys]
        X = np.zeros(N, dtype=complex)

        for m in range(N):
            total_sum = 0
            for n in range(N):
                total_sum += transform[n] * np.cos(np.pi * (2 * n + 1) * m / (2 * N))
            X[m] = (np.sqrt(1 / N) if m == 0 else np.sqrt(2 / N)) * total_sum
        return X