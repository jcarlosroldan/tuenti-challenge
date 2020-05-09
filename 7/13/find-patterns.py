from numpy.fft import fft
from matplotlib.pyplot import plot, show

with open("fromto.txt", "r") as f:
	data = f.read().strip().split("\n")
data = [tuple(map(int, d.split("\t"))) for d in data]

get_bit = lambda n, bit: n >> bit & 1

""" remove collisions 
data2 = []
for d in data:
	if d[1] not in [d2[1] for d2 in data2]:
		data2.append(d)
data = data2
"""#"""

"""
for c, w in data:
	text = "{0:064b}".format(w)
	#print(text)
	text = "".join(text[2*n+1] for n in range(31))
	nw = int(text, 2)
	text = text.replace("0"," ")
	text += "|nw = %s, c+1 = %s" % (nw, c+1)
	print(text)
"""#"""


"""

from math import log2
for c, w in data:
	print(c.bit_length(), w.bit_length())
	#print("C: {0:064b}".format(c+1).replace("0"," ")+"|%s" % (c+1))
	#print("W: {0:064b}".format(w).replace("0"," ")+"|%s" % w)
	#print("-"*67+"+")
"""#"""

""""""
for bit in range(64):
	print("W bit: %s" % bit)
	print("".join(map(str,[w>>bit & 1 for c,w in data])))
""" # """

"""
for c, w in data:
	print((c+1)>>1 & 1, w>>0 & 1)
	print((c+1)>>2 & 1, w>>1 & 1)
	print((c+1)>>4 & 1, w>>3 & 1)
	print((c+1)>>6 & 1, w>>5 & 1)
	print((c+1)>>8 & 1, w>>7 & 1)
	print((c+1)>>10 & 1, w>>9 & 1)
"""


"""
elems = {}
for c, w in data:
	key = get_bit(c+1,0), get_bit(w,0),get_bit(w,1), get_bit(w,4), get_bit(w,3), get_bit(c+1,3) # seguir probando combinaciones de bits de c y w para encontrar las dependencias
	if not key in elems:
		elems[key] = []
	elems[key].append((get_bit(c+1,5)))

for k in elems.keys():
	if len(set(elems[k])) > 1:# or True:
		print(k, elems[k])
"""#"""


"""
print(sum(get_bit(w+1,0) == get_bit(w+1,2) == 1 for c, w in data[:1024])/len(data[:1024]))
print(sum(get_bit(w+1,0) == get_bit(w+1,2) == 0 for c, w in data[:1024])/len(data[:1024]))
print(sum(get_bit(w+1,0) != get_bit(w+1,2) == 1 for c, w in data[:1024])/len(data[:1024]))
print(sum(get_bit(w+1,0) != get_bit(w+1,2) == 0 for c, w in data[:1024])/len(data[:1024]))
"""

"""reps = {}
for c, w in data:
	if not w in reps:
		reps[w] = []
	reps[w].append(c)
for k,v in reps.items():
	if len(v)>1:
		print("W: {0:064b}".format(k).replace("0"," ")+"|%s" % k)
		for e in v:
			print("c: {0:064b}".format(e).replace("0"," ")+"|%s" % e)
		print("-"*67+"+")"""