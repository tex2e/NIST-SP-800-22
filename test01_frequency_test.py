#!/usr/bin/env python3

# https://nvlpubs.nist.gov/nistpubs/legacy/sp/nistspecialpublication800-22r1a.pdf
# 2.1 Frequency (Monobit) Test

import math

def test(bits):
    n = len(bits)
    S_n = sum([ 2*b-1 for b in bits ])
    S_abs = abs(S_n) / math.sqrt(n)
    P_value = math.erfc(S_abs / math.sqrt(2))
    level = 0.01
    return (P_value, level, P_value >= level)


if __name__ == '__main__':
    # example1
    bits = "1011010101"
    bits = [ int(c) for c in bits ]
    P_value, level, ok = test(bits)
    assert round(P_value, 6) == 0.527089
    assert ok

    # example2
    bits = "11001001000011111101101010100010001000010110100011" + \
           "00001000110100110001001100011001100010100010111000"
    bits = [ int(c) for c in bits ]
    P_value, level, ok = test(bits)
    print(P_value)
    assert round(P_value, 6) == 0.109599
    assert ok
