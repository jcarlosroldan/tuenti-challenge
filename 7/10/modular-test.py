def modexp ( g, u, p ):
	"""computes s = (g ^ u) mod p
      args are base, exponent, modulus
      (see Bruce Schneier's book, _Applied Cryptography_ p. 244)"""
	s = 1
	while u != 0:
		if u & 1:
			s = (s * g)%p
		u >>= 1
		g = (g * g)%p;
	return s

secret1 = 5071103
secret2 = 7077255
n = 15

counter = n
for i in range(0, 100000):
	# This loop makes the passwords hard to reverse
	counter = (counter * secret1) % secret2
print("Forma iterativa: ", counter)

counter = n
counter = counter*(secret1**100000) % secret2
print("Forma de fórmula: ", counter)

counter = n
print(counter*modexp(secret1, 100000, secret2)  %  secret2)