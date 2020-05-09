# https://crypto.stackexchange.com/questions/1693/is-it-possible-to-figure-out-the-public-key-from-encrypted-text
from rsa.transform import bytes2int
from math import gcd

exp = 65537
P = []
C = []
for n in range(1, 3):
	with open('plaintexts/test%d.txt' % n, 'rb') as fp:
		P.append(bytes2int(fp.read()))
	with open('ciphered/test%d.txt' % n, 'rb') as fp:
		C.append(bytes2int(fp.read()))

with open('res.txt', 'w') as fp:
	fp.write(gcd(P[0]**exp - C[0], P[1]**exp - C[1]))