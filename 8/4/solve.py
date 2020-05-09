# Tuenti Challenge Edition 8 Level 4
from itertools import permutations
from networkx import DiGraph, shortest_path_length, shortest_path

PROBLEM_SIZE = "submit"

# -- jam input/output ------------------------------------------------------- #

def parse_problems(lines):
	""" Given a list of lines, parses them and returns a list of problems. """
	problems = []
	i = 0
	while i < len(lines):
		h, w = map(int, lines[i].split(" "))
		problems.append((w, h, lines[i + 1:i + h + 1]))
		i += h + 1
	return problems

def solve_all():
	""" Process each test case and generate the output file. """
	res = ""
	with open("%s.in" % PROBLEM_SIZE, "r", encoding="utf-8") as fp:
		lines = fp.read().strip().split("\n")[1:]
	problems = parse_problems(lines)
	for case, problem in enumerate(problems, 1):
		print("Solving Case #%s" % case)
		res += "Case #%s: %s\n" % (case, solve(*problem))
	with open("%s.out" % PROBLEM_SIZE, "w", encoding="utf-8") as fp:
		fp.write(res[:-1])

# -- problem specific functions --------------------------------------------- #

_short_jumps = [j for j in permutations([-2, -1, 1, 2], 2) if abs(j[0]) != abs(j[1])]
_long_jumps = [(x*2, y*2) for x, y in _short_jumps]
_ground = list(".PSD*")
def solve(w, h, board):
	board_graph = DiGraph()
	pos = {}
	for y in range(h):
		for x in range(w):
			value = board[y][x]
			if value in _ground:
				jumps = _long_jumps if value == "*" else _short_jumps
				for jump_x, jump_y in jumps:
					nx, ny = x + jump_x, y + jump_y
					if 0 <= nx < w and 0 <= ny < h and board[ny][nx] in _ground:
						board_graph.add_edge((x, y), (nx, ny))
			pos[value] = (x, y)
	try:
		return shortest_path_length(board_graph, source = pos["S"], target = pos["P"]) + shortest_path_length(board_graph, source = pos["P"], target = pos["D"])
	except:
		return "IMPOSSIBLE"


# -- entrypoint ------------------------------------------------------------- #

if __name__ == "__main__":
	solve_all()