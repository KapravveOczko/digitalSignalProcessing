import numpy as np
import matplotlib.pyplot as plt

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
    def __init__(self, signal_type_var, parameters):
        self.signal_type = signal_type_var
        self.parameters = parameters
        self.signal = None
        self.f_multiplier = self.parameters['frequency']
        self.time = np.linspace(self.parameters['start_time'], self.parameters['start_time'] + self.parameters['duration'], int(self.f_multiplier * self.parameters['duration']), endpoint=False)

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

    def plot_signal(self):
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8, 8), subplot_kw={'frame_on': False})
        fig.subplots_adjust(hspace=0.4)

        ax1.plot(self.time, self.signal)
        ax1.set_title(f'Wykres funkcji {SIGNAL_TYPES[self.signal_type]}')
        ax1.set_xlabel('Czas')
        ax1.set_ylabel('Amplituda')

        ax2.hist(self.signal, bins=10, density=True, alpha=0.75)
        ax2.set_title(f'Histogram funcki {SIGNAL_TYPES[self.signal_type]}')
        ax2.set_xlabel('Amplituda')
        ax2.set_ylabel('Częstotliwość')

        mean_value, abs_mean_value, rms_value, variance, power = self.calculate_statistics()
        stats_text = f"Wartość rednia sygnału: {mean_value:.4f}\nWartość średnia bezwzględna sygnału: {abs_mean_value:.4f}\nWartość skuteczna sygnału: {rms_value:.4f}\nWariancja sygnału: {variance:.4f}\nMoc średnia sygnału: {power:.4f}"

        ax3.text(0.3, 0.5, stats_text, ha='left', va="center", fontsize=12, transform=ax3.transAxes)
        ax3.axis('off')

        return fig

    def calculate_statistics(self):
        mean_value = np.mean(self.signal)
        abs_mean_value = np.mean(np.abs(self.signal))
        rms_value = np.sqrt(np.mean(np.square(self.signal)))
        variance = np.var(self.signal)
        power = np.mean(np.square(self.signal))
        return mean_value, abs_mean_value, rms_value, variance, power

    def save_to_file(self, signal, filename):
        header = f"Signal type: {self.signal_type}\nTime start: 0\nSampling frequency: {1000}\n"
        header += f"Amplitude type: {self.parameters['amplitude_type']}\nNumber of samples: {len(signal)}\n"

        with open(filename, 'wb') as file:
            file.write(header.encode())
            signal.astype(np.float64).tofile(file)

    def generate_uniform_noise(self):
        return np.random.uniform(-self.parameters['amplitude'], self.parameters['amplitude'], len(self.time))

    def generate_gaussian_noise(self):
        return np.random.normal(0, 1, len(self.time))

    def generate_sinusoidal(self):
        return self.parameters['amplitude'] * np.sin(2 * np.pi * self.time / self.parameters['period'])

    def generate_half_wave_rectified_sine(self):
        return np.maximum(self.parameters['amplitude'] * np.sin(2 * np.pi * self.time / self.parameters['period']), 0)

    def generate_full_wave_rectified_sine(self):
        return np.abs(self.parameters['amplitude'] * np.sin(2 * np.pi * self.time / self.parameters['period']))

    def generate_square_wave(self):
        return np.maximum(self.parameters['amplitude'] * np.sign(np.sin(2 * np.pi * self.time / self.parameters['period'])), 0)

    def generate_symmetric_square_wave(self):
        return self.parameters['amplitude'] * np.sign(np.sin(np.pi * self.time / self.parameters['period']))

    def generate_triangular_wave(self):
        return self.parameters['amplitude'] * np.abs(2 * (self.time - np.floor(0.5 + self.time / self.parameters['period'])))

    def generate_unit_step(self):
        signal = np.zeros_like(self.time)

        for i in range(len(signal)):
            if i / self.f_multiplier > self.parameters['time_shift']:
                signal[i] = self.parameters['amplitude']
            if i / self.f_multiplier == self.parameters['time_shift']:
                signal[i] = self.parameters['amplitude'] / 2

        return signal

    def generate_unit_impulse(self):
        signal = np.zeros_like(self.time)
        signal[self.parameters['jump_number']] = self.parameters['amplitude']
        return signal

    def generate_impulse_noise(self):
        signal = np.zeros_like(self.time)
        impulse_indices = np.where(np.random.rand(len(self.time)) < self.parameters['probability'])[0]
        signal[impulse_indices] = self.parameters['amplitude']
        return signal
