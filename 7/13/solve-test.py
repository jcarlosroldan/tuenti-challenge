from math import log2

get_bit = lambda n, bit: n >> bit & 1

W = 70787
C = [-1]*32

# assign direct bits
C[1] = get_bit(W, 0)
for bit in range(2, 32, 2):
	C[bit] = get_bit(W, bit-1)

# assign upper-bound length bits
(W+1)