from numpy import zeros, array as nparray
from numpy.linalg import norm
import qrtools
from random import randint
from simanneal import Annealer
from PIL import Image
from os.path import exists
from pickle import load, dump

PROBLEM_SIZE = "submit"

_dist_mat = None
_cols = None
_w = _h = None
def init(image_path="img_%s.png" % PROBLEM_SIZE, pickle_path="dist_mat_%s.pk" % PROBLEM_SIZE):
	global _dist_mat, _cols, _w, _h
	im = Image.open(image_path)
	_w, _h = im.size
	cols = [list(im.crop((x, 0, x + 1, _h)).getdata()) for x in range(_w)]
	N = len(cols)
	if exists(pickle_path):
		with open(pickle_path, "rb") as fp:
			res = load(fp)
	else:
		res = zeros((N, N))
		for c1 in range(N):
			res[c1, c1] = 0
			print("%.02f%%" % (100 * c1 / N))
			for c2 in range(c1 + 1, N):

				res[c1, c2] = res[c2, c1] = norm(nparray(cols[c1][836:1171]) - nparray(cols[c2][836:1171]))

		with open(pickle_path, "wb") as fp:
			dump(res, fp, protocol=4)
	_dist_mat = res
	_cols = cols

def show(sequence):
	im = Image.new("RGB", (_w, _h))
	for x in range(_w):
		for y in range(_h):
			im.putpixel((x, y), _cols[sequence[x]][y])
	im.show()
	im.save("last_shown.png")

def distance(c1, c2):
	return _dist_mat[c1, c2]

# -----------------------------------------------------------------------------

class UnscrambleAnnealer(Annealer):

	def move(self):
		""" Swaps two columns in the image. """
		a = randint(0, _w - 1)
		b = randint(0, _w - 1)
		self.state[a], self.state[b] = self.state[b], self.state[a]

	def energy(self):
		return sum(distance(self.state[c], self.state[c + 1]) for c in range(_w - 1))

def annealing_solve():
	# won't work, too many local minimums
	ua = UnscrambleAnnealer(list(range(_w)))
	ua.Tmax = 10000
	ua.Tmin = .1
	ua.steps = 100000
	st, e = ua.anneal()
	show(st)

# -- greedy -------------------------------------------------------------------

def greedy_solve():
	res = [randint(0, _w - 1)]
	while len(res) < _w:
		res.append(
			min([c for c in range(_w) if c not in res], key=lambda x: distance(res[-1], x))
		)
	show(res)
	print(qrtools.QR().decode("last_shown.png").data)

# -----------------------------------------------------------------------------

if __name__ == '__main__':
	init()
	show(range(_w))
	greedy_solve()