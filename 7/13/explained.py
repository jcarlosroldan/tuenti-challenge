from numpy import uint64 as ui, arange
ONE = ui(1)

def innerFunct(n, pos):
	#print("n=%s, pos=%s" % (n, pos))
	res = ui(0)
	for m in reversed(arange(n + 1, dtype = ui)):
		b = ui(0)
		for index in arange(pos+1, dtype = ui):
			c = res ^ (((pos&n&~m)|(pos&~n&m) & ONE) << index)
			res ^= (m & (ONE << index)) ^ b
			b = (((c&m) | (c&b) | (m&b)) & (ONE << index)) << ONE
			#print("R: {0:064b}".format(res).replace("0"," ")+"|%s" % (res))
	
	return res & (ONE << pos)

def carvedToWritten(n):
	n = ui(n)
	r = ui(0)
	for pos in arange(64, dtype = ui):
		b_val = innerFunct(n, pos)
		r |= (b_val & (ONE << pos))
	return r

test = [30+2**7, 30+2**8, 30+2**9, 30+2**10]

for c in test:
	continue
	w = carvedToWritten(c)
	print("C: {0:064b}".format(c).replace("0"," ")+"|%s" % (c))
	print("W: {0:064b}".format(w).replace("0"," ")+"|%s" % (w))
	print("-"*67+"+")

print(carvedToWritten(398))