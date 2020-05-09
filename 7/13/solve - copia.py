from numpy import uint64 as ui, arange
from random import randint

from nimblenet.activation_functions import sigmoid_function
from nimblenet.cost_functions import cross_entropy_cost
from nimblenet.learning_algorithms import RMSprop
from nimblenet.data_structures import Instance
from nimblenet.neuralnet import NeuralNet


SAMPLE_SIZE = 10**1

ONE = ui(1)

ONE = ui(1)
def carvedToWritten(n):
	n = ui(n)
	r = ui(0)
	for i in arange(64, dtype = ui):
		a = ui(0)
		for j in reversed(arange(n + 1, dtype = ui)):
			b = ui(0)
			for k in arange(i+1, dtype = ui):
				c = a ^ (((i&n&~j)|(i&~n&j) & ONE) << k)
				a ^= (j & (ONE << k)) ^ b
				b = (((c&j) | (c&b) | (j&b)) & (ONE << k)) << ONE
		r |= (a & (ONE << i))
	return r

sample_x = []
sample_y = [ui(randint(1, (2**5)-1)) for _ in range(SAMPLE_SIZE)]
# generate sample x
for instance in sample_y:
	sample_x.append(list(map(int, "{0:064b}".format(carvedToWritten(instance)))))
# adapt sample y
sample_y = [list(map(int, "{0:064b}".format(y))) for y in sample_y]
# generate dataset
dataset = [Instance(x,y) for x, y in zip(sample_x, sample_y)]
# config
settings = {
	"n_inputs": 64,
	"layers": [
		(2, sigmoid_function),
		(1, sigmoid_function)
	]
}


RMSprop(
	NeuralNet(settings),
	dataset,
	dataset,
	cross_entropy_cost
	)