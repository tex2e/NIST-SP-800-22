#!/usr/bin/env python3

# https://nvlpubs.nist.gov/nistpubs/legacy/sp/nistspecialpublication800-22r1a.pdf
# 2.5 Binary Matrix Rank Test

from numpy.linalg import matrix_rank
from scipy.special import gammaincc as igamc

def test(bits, rowlen=32, collen=32):
    n = len(bits)
    M = rowlen
    Q = collen
    N = n // (M * Q)

    blocks = []
    for j in range(N):
        blocks.append([ bits[(j*Q + i)*M : (j*Q + i+1)*M] for i in range(Q) ])
    R = [ matrix_rank(block) for block in blocks ]

    F_M = 0
    F_M_1 = 0
    for i in range(N):
        if   R[i] == M:   F_M += 1
        elif R[i] == M-1: F_M_1 += 1

    F = [F_M, F_M_1, N - F_M - F_M_1]
    π = [0.2888, 0.5776, 0.1336]

    χ2_obs = sum([ (F[i] - N * π[i])**2 / (N * π[i]) for i in range(3) ])
    print(χ2_obs)

    P_value = igamc(1, χ2_obs/2.0)

    level = 0.01
    return (P_value, level, P_value >= level)


if __name__ == '__main__':
    # example1
    bits = "01011001001010101101"
    bits = [ int(c) for c in bits ]
    P_value, level, ok = test(bits, rowlen=3, collen=3)
    assert round(P_value, 6) == 0.741948
    assert ok
