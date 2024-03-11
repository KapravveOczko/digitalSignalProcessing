import numpy as np

def read_from_file(filename):
    with open(filename, 'rb') as file:
        file_content = file.readlines()

    params = {}
    for line in file_content[:5]:
        key, value = line.decode().strip().split(': ')
        params[key] = value

    signal_data = np.frombuffer(file_content[4], dtype=np.float64)

    return params, signal_data