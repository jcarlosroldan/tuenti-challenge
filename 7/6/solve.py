# Tuenti Challenge Edition 7 Level 6
from re import match
from numpy import array, concatenate
from math import ceil
from networkx import shortest_path_length, shortest_path, DiGraph

# ------------------------------- CONSTANTS --------------------------------- #

FILE = "submit"
MAX_SIDE_LEN = 2**32

# ------------------------ GENERAL PURPOSE UTILITIES ------------------------ #

def group_list(l, each):
	i = 0
	res = []
	while i < len(l):
		res.append(l[i:i+each])
		i += each
	return res

# ------------------------ JAM SPECIFIC FUNCTIONS --------------------------- #

def read_file(fname):
	"""Read input file format."""
	with open(fname,"r") as f:
		lines = f.read().strip().split("\n")[1:]
	l = 0
	problems = []
	while l < len(lines):
		F, S = map(int, lines[l].split(" "))
		shortcuts = lines[l+1:l+1+S]
		shortcuts = [list(map(int, s.strip().split(" "))) for s in shortcuts]
		problems.append((F, shortcuts))
		l += S + 1
	return problems

def solve_all(fname):
	"""Process each test case."""
	problems = read_file("%s.in" % fname)
	case = 1
	text = ""
	for F, shortcuts in problems:
		print("Solving Case #%s" % case)
		if F == 1:
			res = 0
		else:
			res = solve(F, shortcuts)
		text += "Case #%s: %s\n" % (case, res)
		case += 1
	with open("%s.out" % fname, "w") as out:
		out.write(text[:-1])

# ----------------------- PROBLEM SPECIFIC FUNCTIONS ------------------------ #

def solve(F, shortcuts):
	# discard dummy shortcuts
	shortcuts = [s for s in shortcuts if linear_time(s[0], s[1]) > s[2]]
	# create graph points
	points = [1] + [s[0] for s in shortcuts] + [s[1] for s in shortcuts] + [F]
	points = list(sorted(set(points)))
	# create graph edges
	edges = shortcuts
	for i in range(len(points) - 1):
		t = linear_time(points[i], points[i+1])
		edges.append((points[i], points[i+1], t))
		edges.append((points[i+1], points[i], 0))
	# filter edges with same src and dest but different weight
	new_edges = {}
	for edge in edges:
		if (edge[0], edge[1]) not in new_edges or new_edges[(edge[0], edge[1])] > edge[2]:
			new_edges[(edge[0], edge[1])] = edge[2]
	# build graph
	G = DiGraph(data = [(src, dst, {'w': w}) for (src, dst), w in new_edges.items()])

	return shortest_path_length(G, points[0], points[-1], 'w')

def linear_time(n, m):
	return int((m*(m-1) - n*(n-1))/2)

# ------------------------------ ENTRYPOINT --------------------------------- #

solve_all(FILE)