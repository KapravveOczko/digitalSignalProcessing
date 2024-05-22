import numpy as np

OPERATION_TYPES = {
    'D1': 'Dodawanie',
    'D2': 'Odejmowanie',
    'D3': 'Mnożenie',
    'D4': 'Dzielenie',
    'S': "Splot",
}

class TwoSignalOperationGenerator:
    def __init__(self, operation, first_signal, second_signal):
        self.operation = operation
        self.first_signal = first_signal.signal
        self.second_signal = second_signal.signal
        self.first_signal_time = first_signal.time
        self.second_signal_time = second_signal.time
        self.signal = None
        self.original_signal = None
        self.f_multiplier = len(self.first_signal)
        self.time = np.linspace(0, 10, self.f_multiplier, endpoint=False)
        self.parameters = first_signal.parameters
        self.signal_name = '2 sygnałów'
        self.signal_type = 'S0'
        self.hist_bins = 10

    def generate_signal(self):
        if self.operation == 'D1':
            self.signal = np.add(self.first_signal, self.second_signal)
        elif self.operation == 'D2':
            self.signal = np.subtract(self.first_signal, self.second_signal)
        elif self.operation == 'D3':
            self.signal = np.multiply(self.first_signal, self.second_signal)
        elif self.operation == 'D4':
            self.signal = np.divide(self.first_signal, self.second_signal)
        elif self.operation == 'S':
            self.signal = np.convolve(self.first_signal, self.second_signal)

            start = 0
            first_signal_duration = self.first_signal_time[-1] - self.first_signal_time[0]
            second_signal_duration = self.second_signal_time[-1] - self.second_signal_time[0]
            end = first_signal_duration + second_signal_duration

            self.time = np.linspace(start, end, len(self.signal), endpoint=False)

    def return_params(self):
        parameters = [self.signal, self.time, self.hist_bins, self.signal_name]

        if self.operation == 'S':
            parameters.append(True)

        return parameters
