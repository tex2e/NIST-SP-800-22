#!/usr/bin/env python3

# https://nvlpubs.nist.gov/nistpubs/legacy/sp/nistspecialpublication800-22r1a.pdf
# 2.4 Test for the Longest Run of Ones in a Block

import math
from scipy.special import gammaincc as igamc

def get_longest_run_of_ones(bits):
    run = 0
    longest = 0
    for bit in bits:
        if bit == 1:
            run += 1
            if run > longest:
                longest = run
        else:
            run = 0

    return longest

def prob_table(M):
    return {
        8:     [0.2148, 0.3672, 0.2305, 0.1875],
        128:   [0.1174, 0.2430, 0.2493, 0.1752, 0.1027, 0.1124],
        512:   [0.1170, 0.2460, 0.2523, 0.1755, 0.1027, 0.1124],
        1000:  [0.1307, 0.2437, 0.2452, 0.1714, 0.1002, 0.1088],
        10000: [0.0882, 0.2092, 0.2483, 0.1933, 0.1208, 0.0675, 0.0727],
    }[M]

def test(bits):
    n = len(bits)
    if n < 128:
        return (-1, -1, False) # Not enough bits length
    elif n < 6272:
        M = 8
    elif n < 750000:
        M = 128
    else:
        M = 10000

    N = n // M
    blocks = [ bits[i*M : (i+1)*M] for i in range(N) ]
    ν = [0] * 7
    for i in range(N):
        longest = get_longest_run_of_ones(blocks[i])

        if M == 8:
            if   longest <= 1:  ν[0] += 1
            elif longest == 2:  ν[1] += 1
            elif longest <= 3:  ν[2] += 1
            else:               ν[3] += 1
        elif M == 128:
            if   longest <= 4:  ν[0] += 1
            elif longest == 5:  ν[1] += 1
            elif longest == 6:  ν[2] += 1
            elif longest == 7:  ν[3] += 1
            elif longest == 8:  ν[4] += 1
            else:               ν[5] += 1
        else:
            if   longest <= 10: ν[0] += 1
            elif longest == 11: ν[1] += 1
            elif longest == 12: ν[2] += 1
            elif longest == 13: ν[3] += 1
            elif longest == 14: ν[4] += 1
            elif longest == 15: ν[5] += 1
            else:               ν[6] += 1

    if M == 8:
        K = 3
        N = 16
    elif M == 128:
        K = 5
        N = 49
    else:
        K = 6
        N = 75

    π = prob_table(M)
    χ2_obs = sum([ (ν[i] - N * π[i])**2 / (N * π[i]) for i in range(K+1) ])
    P_value = igamc(K/2.0, χ2_obs/2.0)
    level = 0.01
    return (P_value, level, P_value >= level)


if __name__ == '__main__':
    # example
    bits = "11001100000101010110110001001100111000000000001001" + \
           "00110101010001000100111101011010000000110101111100" + \
           "1100111001101101100010110010"
    bits = [ int(c) for c in bits ]
    P_value, level, ok = test(bits)
    assert round(P_value, 6) == 0.180598
    assert ok
