#!/usr/bin/env python3

# https://nvlpubs.nist.gov/nistpubs/legacy/sp/nistspecialpublication800-22r1a.pdf
# 2.13 Cumulative Sums (Cusum) Test

import math
from scipy.special import gammaincc as igamc

def phi(x):
    return (1.0 + math.erf(x / math.sqrt(2.0))) * 0.5

def test(bits, mode=0):
    n = len(bits)
    order = reversed if mode == 1 else lambda x: x
    X = [ 2*x - 1 for x in order(bits) ]
    total = 0
    max_total = 0
    S = []
    for i in range(n):
        total += X[i]
        S.append(total)
        max_total = max(abs(total), max_total)
    z = float(max_total)

    term2 = 0
    k_start = int((-n/z + 1) * 0.25)
    k_end   = int(( n/z - 1) * 0.25)
    for k in range(k_start, k_end + 1):
        term2 += (phi((4*k+1)*z/math.sqrt(n)) - phi((4*k-1)*z/math.sqrt(n)))

    term3 = 0
    k_start = int((-n/z - 3) * 0.25)
    k_end   = int(( n/z - 1) * 0.25)
    for k in range(k_start, k_end + 1):
        term3 += (phi((4*k+3)*z/math.sqrt(n)) - phi((4*k+1)*z/math.sqrt(n)))

    P_value = 1 - term2 + term3
    level = 0.01
    return (P_value, level, P_value >= level)


if __name__ == '__main__':
    # example1
    bits = "11001001000011111101101010100010001000010110100011" + \
           "00001000110100110001001100011001100010100010111000"
    bits = [ int(c) for c in bits ]
    P_value, level, ok = test(bits, mode=0)
    print(P_value)
    assert round(P_value, 6) == 0.219194
    assert ok

    # example2
    bits = "11001001000011111101101010100010001000010110100011" + \
           "00001000110100110001001100011001100010100010111000"
    bits = [ int(c) for c in bits ]
    P_value, level, ok = test(bits, mode=1)
    print(P_value)
    assert round(P_value, 6) == 0.114866
    assert ok
