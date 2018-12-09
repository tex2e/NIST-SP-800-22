#!/usr/bin/env python3

# https://nvlpubs.nist.gov/nistpubs/legacy/sp/nistspecialpublication800-22r1a.pdf
# 2.10 Linear Complexity Test

import math
from fractions import Fraction
from scipy.special import gammaincc as igamc

def berelekamp_massey(bits):
    n = len(bits)
    b = [0 for x in bits]  #initialize b and c arrays
    c = [0 for x in bits]
    b[0] = 1
    c[0] = 1

    L = 0
    m = -1
    N = 0
    while N < n:
        #compute discrepancy
        d = bits[N]
        for i in range(1, L+1):
            d = d ^ (c[i] & bits[N-i])
        if (d != 0):  # If d is not zero, adjust poly
            t = c[:]
            for i in range(0, n-N+m):
                c[N-m+i] = c[N-m+i] ^ b[i]
            if (L <= (N/2)):
                L = N + 1 - L
                m = N
                b = t
        N = N + 1
    # Return length of generator and the polynomial
    return L, c[0:L]

def test(bits, blocklen):
    n = len(bits)
    M = blocklen
    N = n // M
    L = []
    for i in range(N):
        x = bits[i*M : (i+1)*M]
        L.append(berelekamp_massey(x)[0])

    μ = Fraction(M, 2) + Fraction(9 + (-1)**(M+1), 36) \
        - Fraction(Fraction(M, 3) + Fraction(2, 9), 2**M)
    T = []
    for i in range(N):
        T.append(((-1.0)**M) * (L[i] - μ) + (2/9.0))

    ν = [0] * 7
    for t in T:
        if   t <= -2.5: ν[0] += 1
        elif t <= -1.5: ν[1] += 1
        elif t <= -0.5: ν[2] += 1
        elif t <=  0.5: ν[3] += 1
        elif t <=  1.5: ν[4] += 1
        elif t <=  2.5: ν[5] += 1
        else:           ν[6] += 1

    K = 6
    π = [0.010417, 0.03125, 0.125, 0.5, 0.25, 0.0625, 0.020833]
    χ2_obs = sum([ (ν[i] - N * π[i])**2 / (N * π[i]) for i in range(K) ])
    P_value = igamc(K/2.0, χ2_obs/2.0)
    level = 0.01
    return (P_value, level, P_value >= level)

if __name__ == '__main__':
    # example
    bits = "1101011110001"
    bits = [ int(c) for c in bits ]
    P_value, level, ok = test(bits, blocklen=13)
    print(P_value)
    # assert round(P_value, 6) == ???
    assert ok
