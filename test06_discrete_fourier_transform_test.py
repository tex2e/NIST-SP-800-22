#!/usr/bin/env python3

# https://nvlpubs.nist.gov/nistpubs/legacy/sp/nistspecialpublication800-22r1a.pdf
# 2.6 Discrete Fourier Transform (Spectral) Test

import math
import numpy as np

def test(bits):
    n = len(bits)

    X = [ 2*bit-1 for bit in bits ]
    S = np.fft.fft(X)
    M = abs(S[:n//2])
    T = math.sqrt(-math.log(0.05) * n)
    N_0 = 0.95 * n / 2
    N_1 = len(M[M < T])
    d = (N_1 - N_0) / math.sqrt((n * 0.95 * 0.05) / 4)
    P_value = math.erfc(abs(d)/math.sqrt(2))
    level = 0.01
    return (P_value, level, P_value >= level)


if __name__ == '__main__':
    pass

    # # example1
    # bits = "1001010011"
    # bits = [ int(c) for c in bits ]
    # P_value, level, ok = test(bits)
    # print(P_value)
    # assert round(P_value, 6) == 0.029523
    # assert ok
    #
    # # example2
    # bits = "11001001000011111101101010100010001000010110100011" + \
    #        "00001000110100110001001100011001100010100010111000"
    # bits = [ int(c) for c in bits ]
    # P_value, level, ok = test(bits)
    # print(P_value)
    # assert round(P_value, 6) == 0.168669
    # assert ok
