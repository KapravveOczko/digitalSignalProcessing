import struct
import numpy as np
from signal_generator import SIGNAL_TYPES

class SignalFromFileGenerator:
    def __init__(self, path):
        self.path = path
        self.hist_bins = 10
        self.parameters = {}

    def generate_signal(self):
        with open(self.path, 'rb') as file:
            self.signal = []
            self.parameters['start_time'] = struct.unpack('d', file.read(8))[0]
            self.parameters['duration'] = struct.unpack('d', file.read(8))[0]
            self.f_multiplier = struct.unpack('d', file.read(8))[0]
            self.signal_type = 'S' + str(int(struct.unpack('d', file.read(8))[0]))
            if self.signal_type not in SIGNAL_TYPES:
                self.signal_name = 'Nieznanego typu sygnału'
            else:
                self.signal_name = SIGNAL_TYPES[self.signal_type]
            self.time = np.linspace(self.parameters['start_time'], self.parameters['start_time'] + self.parameters['duration'], int(self.f_multiplier), endpoint=False)
            while True:
                point = file.read(8)
                if not point:
                    break
                self.signal.append(struct.unpack('d', point)[0])

    def return_params(self):
        return self.signal, self.time, self.hist_bins, self.signal_name
