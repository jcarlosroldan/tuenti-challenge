from numpy import uint64 as ui, arange

START = 1050

ONE = ui(1)
def carvedToWritten(n):
	n = ui(n)
	r = ui(0)
	for i in arange(64, dtype = ui):
		a = ui(0)
		for j in reversed(arange(n + 1, dtype = ui)):
			b = ui(0)
			for k in arange(i+1, dtype = ui):
				#print("N: {0:064b}".format(n).replace("0"," ")+"|%s" % n)
				#print("I: {0:064b}".format(i).replace("0"," ")+"|%s" % i)
				#print("J: {0:064b}".format(j).replace("0"," ")+"|%s" % j)
				#print("K: {0:064b}".format(k).replace("0"," ")+"|%s" % k)
				c = a ^ (((i&n&~j)|(i&~n&j) & ONE) << k)
				#print("C: {0:064b}".format(c).replace("0"," ")+"|%s" % c)
				a ^= (j & (ONE << k)) ^ b
				#print("A: {0:064b}".format(a).replace("0"," ")+"|%s" % a)
				b = (((c&j) | (c&b) | (j&b)) & (ONE << k)) << ONE
				#print("B: {0:064b}".format(b).replace("0"," ")+"|%s" % b)
				#print("-"*67+"+")
			#print("-"*67+"+")
		r |= (a & (ONE << i))
		#print("R: {0:064b}".format(r).replace("0"," ")+"|%s" % r)
		#print("-"*67+"+")
	return r

n = START
while n < 2**32 -1:
	print(n)
	with open("fromto.txt", "a") as f:
		f.write("%s\t%s\n" % (n, carvedToWritten(n)))
	n += 1