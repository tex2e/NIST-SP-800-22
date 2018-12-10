#!/usr/bin/env python3

# https://nvlpubs.nist.gov/nistpubs/legacy/sp/nistspecialpublication800-22r1a.pdf
# 2.12 Approximate Entropy Test

import math
from scipy.special import gammaincc as igamc

def block2int(block_bits):
    n = 0
    for bit in block_bits:
        n = (n << 1) + bit
    return n

def test(bits, blocklen=2):
    n = len(bits)
    M = blocklen
    C = {}
    φ = {}

    for m in [M, M+1]:
        padded_bits = bits + bits[0:m-1]
        counts = [0] * 2**m
        for j in range(0, n):
            idx = block2int(padded_bits[j:j+m])
            counts[idx] += 1

        C[m] = [ cnt / n for cnt in counts ]
        def f(i):
            if C[m][i] == 0: return 0
            return C[m][i] * math.log(C[m][i])

        φ[m] = sum([ f(i) for i in range(2**m) ])

    ApEn = lambda m: φ[m] - φ[m+1]
    χ2 = 2 * n * (math.log(2) - ApEn(M))
    P_value = igamc(2**(M-1), χ2/2.0)
    level = 0.01
    return (P_value, level, P_value >= level)


if __name__ == '__main__':
    # example1
    bits = "0100110101"
    bits = [ int(c) for c in bits ]
    P_value, level, ok = test(bits, blocklen=3)
    print(P_value)
    assert round(P_value, 6) == 0.261961
    assert ok

    # example2
    bits = "11001001000011111101101010100010001000010110100011" + \
           "00001000110100110001001100011001100010100010111000"
    bits = [ int(c) for c in bits ]
    P_value, level, ok = test(bits, blocklen=2)
    print(P_value)
    assert round(P_value, 6) == 0.235301
    assert ok
