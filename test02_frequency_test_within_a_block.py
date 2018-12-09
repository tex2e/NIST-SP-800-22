#!/usr/bin/env python3

# https://nvlpubs.nist.gov/nistpubs/legacy/sp/nistspecialpublication800-22r1a.pdf
# 2.2 Frequency Test within a Block

from fractions import Fraction
from scipy.special import gammaincc as igamc

def test(bits, blocklen):
    n = len(bits)
    M = blocklen
    N = n // M
    π = [0] * N
    for i in range(N):
        π[i] = Fraction(sum([ bits[i * M + j] for j in range(M) ]), M)

    χ2_obs = 4 * M * sum([ (π[i] - Fraction(1,2))**2 for i in range(N) ])
    P_value = igamc(N/2.0, χ2_obs/2.0)
    level = 0.01
    return (P_value, level, P_value >= level)


if __name__ == '__main__':
    # example1
    bits = "0110011010"
    bits = [ int(c) for c in bits ]
    P_value, level, ok = test(bits, blocklen=3)
    assert round(P_value, 6) == 0.801252
    assert ok

    # example2
    bits = "11001001000011111101101010100010001000010110100011" + \
           "00001000110100110001001100011001100010100010111000"
    bits = [ int(c) for c in bits ]
    P_value, level, ok = test(bits, blocklen=10)
    assert round(P_value, 6) == 0.706438
    assert ok
