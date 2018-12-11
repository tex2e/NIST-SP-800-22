#!/usr/bin/env python3

# https://nvlpubs.nist.gov/nistpubs/legacy/sp/nistspecialpublication800-22r1a.pdf
# 2.14 Random Excursions Test

import math
from fractions import Fraction
from scipy.special import gammaincc as igamc

def test(bits, mode=0):
    n = len(bits)
    X = [ 2*x - 1 for x in bits ]
    total = 0
    S = []
    for i in range(n):
        total += X[i]
        S.append(total)

    S_dash = [0] + S + [0]
    zero_positions = [ i for i in range(1, len(S_dash)) if S_dash[i] == 0 ]
    J = len(zero_positions)
    Cycles = []
    pre = 0
    for pos in zero_positions:
        Cycles.append(S_dash[pre:pos+1])
        pre = pos

    states = []
    for cycle in Cycles:
        state = {-4:0, -3:0, -2:0, -1:0, 1:0, 2:0, 3:0, 4:0}
        for x in cycle:
            if   x == -4: state[x] += 1
            elif x == -3: state[x] += 1
            elif x == -2: state[x] += 1
            elif x == -1: state[x] += 1
            elif x == +1: state[x] += 1
            elif x == +2: state[x] += 1
            elif x == +3: state[x] += 1
            elif x == +4: state[x] += 1
            else:         pass
        states.append(state)

    table = {
        -4: [0] * 6, -3: [0] * 6, -2: [0] * 6, -1: [0] * 6,
        +1: [0] * 6, +2: [0] * 6, +3: [0] * 6, +4: [0] * 6}

    for x in (-4, -3, -2, -1, 1, 2, 3, 4): # state x
        for n in range(6): # number of cycles (0..5)
            count = len([ True for state in states if state[x] == n ])
            table[x][n] = count

    πxk = {
        1: [0.5     ,0.25   ,0.125  ,0.0625  ,0.0312 ,0.0312],
        2: [0.75    ,0.0625 ,0.0469 ,0.0352  ,0.0264 ,0.0791],
        3: [0.8333  ,0.0278 ,0.0231 ,0.0193  ,0.0161 ,0.0804],
        4: [0.875   ,0.0156 ,0.0137 ,0.012   ,0.0105 ,0.0733],
        5: [0.9     ,0.01   ,0.009  ,0.0081  ,0.0073 ,0.0656],
        6: [0.9167  ,0.0069 ,0.0064 ,0.0058  ,0.0053 ,0.0588],
        7: [0.9286  ,0.0051 ,0.0047 ,0.0044  ,0.0041 ,0.0531]}

    χ2_obs = {-4:0, -3:0, -2:0, -1:0, 1:0, 2:0, 3:0, 4:0}
    f = lambda obs, exp: (obs - exp)**2 / exp
    for x in (-4, -3, -2, -1, 1, 2, 3, 4):
        χ2_obs[x] = sum([ f(table[x][k], Fraction(J*πxk[abs(x)][k]))
                          for k in range(6) ])

    P_value = {-4:0, -3:0, -2:0, -1:0, 1:0, 2:0, 3:0, 4:0}
    for x in (-4, -3, -2, -1, 1, 2, 3, 4):
        P_value[x] = igamc(5/2.0, χ2_obs[x]/2.0)

    level = 0.01
    ok = all( P_value[x] >= level for x in (-4, -3, -2, -1, 1, 2, 3, 4) )
    return (P_value, level, ok)


if __name__ == '__main__':
    # example1
    bits = "0110110101"
    bits = [ int(c) for c in bits ]
    P_value, level, ok = test(bits, mode=0)
    print(P_value)
    assert round(P_value[1], 6) == 0.502529
    assert ok
