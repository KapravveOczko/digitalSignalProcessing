
PROCESSING_OPERATIONS_TYPES = {
    'P': 'Próbkowanie',
    'Q': 'Kwantyzazja',
    'R': 'Rekonstrukcja',
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

class SignalProcesser:
    def __init__(self, signal):
        self.processed_signal = signal
        self.signal = None
