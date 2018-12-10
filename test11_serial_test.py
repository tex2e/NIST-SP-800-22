#!/usr/bin/env python3

# https://nvlpubs.nist.gov/nistpubs/legacy/sp/nistspecialpublication800-22r1a.pdf
# 2.11 Serial Test

import math
from fractions import Fraction
from scipy.special import gammaincc as igamc

def block2int(block_bits):
    n = 0
    for bit in block_bits:
        n = (n << 1) + bit
    return n

def test(bits, blocklen=2):
    n = len(bits)
    m = blocklen
    N = n // m
    bits += bits[0:m-1]

    ν_m = [ [ 0 for j in range(2**(m-i)) ] for i in range(3) ]
    for i in range(3):
        for position in range(n):
            idx = block2int(bits[position:position+(m-i)])
            ν_m[i][idx] += 1

    ψ2_m = [0] * 3
    for i in range(3):
        a = Fraction(2**(m-i), n)
        ψ2_m[i] = a * sum([ ν_m[i][j]**2 for j in range(2**(m-i))]) - n

    nabla_ψ2_m = ψ2_m[0] - ψ2_m[1]
    nabla2_ψ2_m = ψ2_m[0] - 2 * ψ2_m[1] + ψ2_m[2]
    P_value1 = igamc(2**(m-2), nabla_ψ2_m/2.0)
    P_value2 = igamc(2**(m-3), nabla2_ψ2_m/2.0)
    level = 0.01
    ok = (P_value1 >= level and P_value2 >= level)
    return ((P_value1, P_value2), level, ok)

if __name__ == '__main__':
    # example
    bits = "0011011101"
    bits = [ int(c) for c in bits ]
    (P_value1, P_value2), level, ok = test(bits, blocklen=3)
    print(P_value1)
    print(P_value2)
    assert round(P_value1, 6) == 0.808792
    assert round(P_value2, 6) == 0.670320
    assert ok
