#!/usr/bin/env python3

# https://nvlpubs.nist.gov/nistpubs/legacy/sp/nistspecialpublication800-22r1a.pdf
# 2.15 Random Excursions Variant Test

import math

def test(bits):
    n = len(bits)
    X = [ 2*x - 1 for x in bits ]
    total = 0
    S = []
    for i in range(n):
        total += X[i]
        S.append(total)

    S_dash = [0] + S + [0]
    J = len([ i for i in range(1, len(S_dash)) if S_dash[i] == 0 ])

    ξ = {}
    for x in list(range(-9,0)) + list(range(1,10)):
        ξ[x] = 0
    for state in (S_dash):
        if state == 0: continue
        if abs(state) < 10:
            ξ[state] += 1

    P_value = {}
    for x in range(-9, 10):
        if x == 0: continue
        P_value[x] = \
            math.erfc(abs(ξ[x] - J) / math.sqrt(2 * J * (4 * abs(x) - 2)))

    level = 0.01
    ok = all(P_value[x] >= level for x in list(range(-9,0)) + list(range(1,10)))
    return (P_value, level, ok)


if __name__ == '__main__':
    # example
    bits = "0110110101"
    bits = [ int(c) for c in bits ]
    P_value, level, ok = test(bits)
    print(P_value)
    assert round(P_value[1], 6) ==  0.683091
    assert ok
