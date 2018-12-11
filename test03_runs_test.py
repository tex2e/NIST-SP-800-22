#!/usr/bin/env python3

# https://nvlpubs.nist.gov/nistpubs/legacy/sp/nistspecialpublication800-22r1a.pdf
# 2.3 Runs Test

import math

def test(bits):
    n = len(bits)
    π = sum(bits) / n
    τ = 2 / math.sqrt(n)
    if abs(π - 0.5) > τ:
        return (π - 0.5, τ, False)

    r = lambda k: int(bits[k] != bits[k+1])
    V_obs = sum([ r(k) for k in range(n-1) ]) + 1

    numer = abs(V_obs - 2 * n * π * (1 - π))
    denom = 2 * math.sqrt(2 * n) * π * (1 - π)
    P_value = math.erfc(numer / denom)

    level = 0.01
    return (P_value, level, P_value >= level)


if __name__ == '__main__':
    # example1
    bits = "1001101011"
    bits = [ int(c) for c in bits ]
    P_value, level, ok = test(bits)
    assert round(P_value, 6) == 0.147232
    assert ok

    # example2
    bits = "11001001000011111101101010100010001000010110100011" + \
           "00001000110100110001001100011001100010100010111000"
    bits = [ int(c) for c in bits ]
    P_value, level, ok = test(bits)
    print(P_value)
    assert round(P_value, 6) == 0.500798
    assert ok
