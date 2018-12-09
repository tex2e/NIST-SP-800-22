#!/usr/bin/env python3

# https://nvlpubs.nist.gov/nistpubs/legacy/sp/nistspecialpublication800-22r1a.pdf
# 2.9 Maurer's "Universal Statistical" Test

import math

def block2int(block_bits):
    n = 0
    for bit in block_bits:
        n = (n << 1) + bit
    return n

def test(bits, blocklen, initblock):
    n = len(bits)
    L = blocklen
    Q = initblock
    N = n // L
    K = N - Q  # remaining K blocks
    T = [ 0 for i in range(2**L) ]
    blocks = [ bits[i*L : (i+1)*L] for i in range(N) ]
    for i in range(Q):
        L_bit_value = block2int(blocks[i])
        T[L_bit_value] = i + 1

    total = 0
    for i in range(Q, N):
        L_bit_value = block2int(blocks[i])
        block_i = i + 1
        a = math.log(block_i - T[L_bit_value], 2)
        total += math.log(block_i - T[L_bit_value], 2)
        T[L_bit_value] = i + 1

    f_n = total / K
    table = [(0, 0), (0.73264948, 0.69), (1.5374383, 1.338), (2.40160681, 1.901),
             (3.31122472, 2.358), (4.25342659, 2.705), (5.2177052, 2.954),
             (6.1962507, 3.125), (7.1836656, 3.238), (8.1764248, 3.311),
             (9.1723243, 3.356), (10.170032, 3.384), (11.168765, 3.401),
             (12.16807, 3.41), (13.167693, 3.416), (14.167488, 3.419),
             (15.167379, 3.421)]
    expectedValue, σ2 = table[L]
    P_value = math.erfc(abs((f_n - expectedValue) / (math.sqrt(2 * σ2))))
    level = 0.01
    return (P_value, level, P_value >= level)


if __name__ == '__main__':
    # example
    bits = "01011010011101010111"
    bits = [ int(c) for c in bits ]
    P_value, level, ok = test(bits, blocklen=2, initblock=4)
    print(P_value)
    assert round(P_value, 6) == 0.767189
    assert ok
