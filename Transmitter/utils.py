import math

def convolution(a, b):
    result = []

    for n in range((len(a) + len(b) - 1)):
        result.append(0)
        for k in range(len(a)):
            if 0 <= n - k < len(b):
                result[n] += a[k] * b[n - k]

    return result

def correlation(a, b):
    b.reverse()
    return convolution(a, b)

def sinusoidal_signal_for_antenna(A, T, t):
    return A * math.sin((2 * math.pi / T) * t) + A * math.sin((2 * math.pi / T * 2) * t)

