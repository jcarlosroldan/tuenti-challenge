from socket import socket, AF_INET, SOCK_STREAM
from networkx import Graph, shortest_path
from time import sleep
from threading import Thread

HOST = ('52.49.91.111', 2003)
MAX_BOARD = 110
BOARD_SIZE = MAX_BOARD * 2 - 1
JUMPS = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))

class Army:
	def __init__(self, size):
		self.princess = None
		self.map = [['?' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
		self.board = Graph()
		initial_pos = (MAX_BOARD, MAX_BOARD)
		self.board.add_node(initial_pos)
		self.valid = {initial_pos}
		self.unexplored = set()
		self.knights = [Knight(self, n) for n in range(size)]
		self.targets = [None for _ in range(size)]

	def rescue(self):
		threads = [Thread(target=knight.rescue) for knight in self.knights]
		[t.start() for t in threads]
		while any(knight.pos != self.princess for knight in self.knights):
			with open('grid.txt', 'w') as fp:
				fp.write('\n'.join(''.join(line) for line in self.map))
			sleep(1)


class Knight:
	CELL_SCORES = {'P': 1000, '?': 100, '.': 10, '#': 1}

	def __init__(self, army, identifier):
		self.pos = (MAX_BOARD, MAX_BOARD)
		self.sock = socket(AF_INET, SOCK_STREAM)
		self.sock.connect(HOST)
		self.army = army
		self.identifier = identifier

	def rescue(self):
		self.move()
		while self.pos != self.army.princess:
			if self.target() is None or self.target() == self.pos:
				if self.army.princess is not None and self.path_to(self.army.princess):
					self.target(self.army.princess)
				else:
					while True:
						try:
							candidates = {c for c in self.army.unexplored if self.path_to(c) is not None}.difference(self.army.targets)
							if len(candidates):
								self.target(min(candidates, key=lambda k: self.score(k)))
								break
						except:
							continue
						sleep(1)
			self.move()

	def move(self):
		if self.target() is not None:
			dest = self.path_to(self.target())[1]
			if dest in self.army.unexplored:
				self.army.unexplored.remove(dest)
			self.sock.send(self.encode_dest(dest).encode())
			self.pos = dest
		ans = self.sock.recv(1024).decode()
		for r, row in enumerate(ans.split('\n')[:5], self.pos[0] - 2):
			for c, cell in enumerate(row, self.pos[1] - 2):
				pos = (r, c)
				if cell != 'K': self.army.map[r][c] = cell
				if pos not in self.army.board and cell != '#':
					self.army.board.add_node(pos)
					self.army.valid.add(pos)
					self.army.unexplored.add(pos)
					for dx, dy in JUMPS:
						dest = (pos[0] + dx, pos[1] + dy)
						if dest in self.army.board:
							self.army.board.add_edge(pos, dest)
				if self.army.princess is None and cell == 'P':
					self.army.princess = (r, c)
		if pos == self.army.princess:
			print(ans)

	def encode_dest(self, target):
		row_offset = target[0] - self.pos[0]
		col_offset = target[1] - self.pos[1]
		row_offset = str(abs(row_offset)) + ('D' if row_offset > 0 else 'U')
		col_offset = str(abs(col_offset)) + ('R' if col_offset > 0 else 'L')
		return row_offset + col_offset

	def path_to(self, target):
		try:
			return shortest_path(self.army.board, self.pos, target)
		except:
			return None

	def dist(self, pos1, pos2):
		return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

	def score(self, dest):
		path = self.path_to(dest)
		if path is None:
			return -9999
		elif dest in self.army.targets:
			return 0
		else:
			res = 0
			for dx in range(-2, 3):
				for dy in range(-2, 3):
					val = self.army.map[dest[0] + dx][dest[1] + dy]
					res += Knight.CELL_SCORES[val]
			return res / len(path)

	def target(self, new_target=None):
		if new_target is not None:
			self.army.targets[self.identifier] = new_target
		else:
			return self.army.targets[self.identifier]



if __name__ == '__main__':
	army = Army(10)
	army.rescue()