from ctypes import util, c_ulong, CDLL
from tarfile import open as taropen
from zlib import crc32

FNAME = 'submit'
PATH_ANIMALS = 'animals.tar.gz'
CRC32_EMPTY = crc32(bytes([]))
MAX_CHUNK_SIZE = 2**31 - 1  # prevent chunks of zeroes bigger than c_ulong

# --- problem functions -------------------------------------------------------

def main():
	load_context()
	output = ''
	for p, problem in enumerate(load_input(), 1):
		output += '%s\n' % solve(*problem)
	with open('%sOutput.txt' % FNAME, 'w', encoding='utf-8') as fp:
		fp.write(output)

_animal_sizes = {}
def load_context():
	global _animal_sizes
	tar = taropen(PATH_ANIMALS, 'r|gz')
	_animal_sizes = {
		m.name.rsplit('/')[-1]: m.size
		for m in tar.getmembers()
		if not m.name.endswith('.')
	}
	tar.close()

def load_input():
	with open('%sInput.txt' % FNAME, 'r', encoding='utf-8') as fp:
		for line in fp:
			animal, A = line.strip().split(' ')
			additions = [
				tuple(map(int, fp.readline().strip().split(' ')))
				for a in range(int(A))
			]
			yield animal, additions

def solve(animal, additions):
	print(animal)
	genome = Genome(_animal_sizes[animal])
	res = [genome.crc32()]
	for position, value in additions:
		genome.insert(position, value)
		res.append(genome.crc32())
	return '\n'.join('%s %d: %08x' % (animal, c, crc) for c, crc in enumerate(res))

class Genome:
	def __init__(self, zeroes_size):
		remaining_bytes = zeroes_size
		self.data = [(0, 0)]
		while remaining_bytes:
			chunk_size = min(remaining_bytes, MAX_CHUNK_SIZE)
			self.data.append((0, chunk_size))
			remaining_bytes -= chunk_size

	def insert(self, position, value):
		index = 0
		for c, (chunk_value, repetitions) in enumerate(self.data):
			if index + repetitions >= position:
				splitted_chunk = []
				if position > 0:
					splitted_chunk.append((chunk_value, position - index))
				splitted_chunk.append((value, 1))
				if index + repetitions != position:
					splitted_chunk.append((chunk_value, repetitions - position + index))
				self.data = self.data[:c] + splitted_chunk + self.data[c + 1:]
				break
			else:
				index += repetitions
		else:
			raise ValueError('Position is higher than data size.')

	def crc32(self):
		res = CRC32_EMPTY
		for value, repetitions in self.data:
			if value == 0:
				if (repetitions // 2**31) > 1:
					print(repetitions // 2**31)
				res = crc32_combine(res, crc32_zeros(repetitions), repetitions)
			elif repetitions == 1:
				res = crc32_combine(res, crc32(bytes([value])), 1)
			else:
				raise NotImplementedError('Fast CRC is only computed for chunks of zeros or single values.')
		return res

# --- auxiliar functions ------------------------------------------------------

_zlib = None
def crc32_combine(crc1, crc2, len2):
	global _zlib
	if _zlib is None:
		lib = util.find_library('zlib1')
		_zlib = CDLL(lib)
	_zlib.crc32_combine.argtypes = [c_ulong, c_ulong, c_ulong]
	_zlib.crc32_combine.restype = c_ulong
	res = _zlib.crc32_combine(crc1, crc2, len2)
	return res

_crc_zeros_mem = [crc32(bytes([0]))]
def _init_crc32_zeros(max_n):
	n = 2**(len(_crc_zeros_mem) - 1)
	while n < max_n:
		doubled_crc = crc32_combine(_crc_zeros_mem[-1], _crc_zeros_mem[-1], n)
		_crc_zeros_mem.append(doubled_crc)
		n <<= 1

def crc32_zeros(n):
	_init_crc32_zeros(n)
	exp = 0
	res = CRC32_EMPTY
	while n > 0:
		if n & 1:
			res = crc32_combine(res, _crc_zeros_mem[exp], 2**exp)
		n >>= 1
		exp += 1
	return res

if __name__ == '__main__':
	main()