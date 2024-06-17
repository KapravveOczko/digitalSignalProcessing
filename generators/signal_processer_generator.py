import numpy as np

PROCESSING_OPERATIONS_TYPES = {
    'P': 'Próbkowanie',
    'Q': 'Kwantyzazja',
    'R': 'Rekonstrukcja',
    'T': 'Transformacja',
}

QUANTIZATION_METHOD = {
    'Q1': 'Kwantyzacja równomierna z obcięciem',
    'Q2': 'Kwantyzacja równomierna z zaokrągleniem',
}

RECONSTRUCTION_METHOD = {
    'R1': 'Ekstrapolacja zerowego rzędu',
    'R2': 'Interpolacja pierwszego rzędu',
    'R3': 'Rekonstrukcja w oparciu o funkcję sinc',
}

TRANSFORMATION_METHOD = {
    'F1': 'F1',
    'F1-DIT': 'F1-DIT',
    'T1': 'T1',
}

class SignalProcesser:
    def __init__(self, operation, signal, parameters):
        self.signal = []
        self.parameters = parameters
        self.processed_signal = signal
        self.processed_time = self.parameters['time']
        self.original_signal = self.parameters['original_signal']
        self.original_time = self.parameters['original_time']
        self.sinc_parameter = self.parameters['sinc_parameter']
        self.f_multiplier = len(signal)
        self.number_of_samples = len(signal)
        if self.original_signal is not None:
            self.f_multiplier = len(self.original_signal)
        self.num_samples = int(self.parameters['duration'] * (self.parameters['sampling_rate'])) + 1
        self.time = np.linspace(self.processed_time[0], self.processed_time[-1], self.num_samples)
        self.operation = operation
        self.signal_type = 'S0'
        self.hist_bins = 10

    def generate_signal(self):
        self.only_single_points = True
        if self.operation == 'P':
            self.signal_name = 'Próbkowananego sygnału'
            self.signal = self.process_sampling()
        elif self.operation == 'Q':
            self.signal_name = 'Kwantyzowanego sygnału'
            self.signal = self.process_quantization()
        elif self.operation == 'R':
            self.only_single_points = False
            self.signal_name = 'Zrekonstruowanego sygnału'
            self.signal = self.process_reconstruction()
            self.time = self.original_time

    def process_sampling(self):
        return np.interp(self.time, self.processed_time, self.processed_signal)

    def process_quantization(self):
        if self.parameters['quantization_method'] == 'Q1':
            self.signal_name += " Q1"
            return self.quantize_truncate()
        elif self.parameters['quantization_method'] == 'Q2':
            self.signal_name += " Q2"
            return self.quantize_round()

    def quantize_truncate(self):
        max_val = max(self.processed_signal)
        min_val = min(self.processed_signal)
        quantization_jump = (max_val - min_val) / (2 ** self.parameters['quantization_level'])
        quantized_signal = [min(max(np.round(sample / quantization_jump) * quantization_jump, min_val), max_val) for sample in self.processed_signal]
        return quantized_signal

    def quantize_round(self):
        max_val = max(self.processed_signal)
        min_val = min(self.processed_signal)
        quantization_jump = (max_val - min_val) / (2 ** self.parameters['quantization_level'])
        quantized_signal = [np.round(sample / quantization_jump) * quantization_jump for sample in self.processed_signal]
        return quantized_signal

    def process_reconstruction(self):
        if self.parameters['reconstruction_method'] == 'R1':
            self.signal_name += " R1"
            return self.reconstruct_zero_order()
        elif self.parameters['reconstruction_method'] == 'R2':
            self.signal_name += " R2"
            return self.reconstruct_first_order()
        elif self.parameters['reconstruction_method'] == 'R3':
            self.signal_name += " R3"
            return self.reconstruct_sinc()

    def reconstruct_zero_order(self):
        reconstructed_signal = [0] * self.f_multiplier
        for i in range(len(reconstructed_signal)):
            reconstructed_signal[i] = self.processed_signal[int(i * len(self.time) / self.f_multiplier)]

        return reconstructed_signal

    def reconstruct_first_order(self):
        reconstructed_signal = [0] * self.f_multiplier
        for i in range(len(reconstructed_signal)):
            t = i * len(self.time) / self.f_multiplier
            t0 = int(t)
            t1 = t0 + 1
            if t1 >= len(self.time):
                t1 = len(self.time) - 1
            reconstructed_signal[i] = self.processed_signal[t0] + (t - t0) * (self.processed_signal[t1] - self.processed_signal[t0])

        return reconstructed_signal


    def reconstruct_sinc(self):
        reconstructed_signal = np.zeros_like(self.original_time)

        T = 1 / self.parameters['sampling_rate']

        for i in range(len(self.processed_signal)):
            start = int(max(0, i - self.sinc_parameter))
            end = int(min(len(self.processed_signal), i + self.sinc_parameter))

            for j in range(start, end):
                ta, xa = self.processed_time[j], self.processed_signal[j]
                reconstructed_signal += xa * self.sinc((self.original_time - ta) / T)


        amplitude_max = max(reconstructed_signal)
        original_amplitude_max = max(self.original_signal)

        return reconstructed_signal / amplitude_max * original_amplitude_max

    def sinc(self, x):
        return np.where(x == 0, 1.0, np.sin(np.pi * x) / (np.pi * x))

    def return_params(self):
        return self.signal, self.time, self.hist_bins, self.signal_name, self.only_single_points

