# Tuenti Challenge Edition 7 Level 4
from re import match
from numpy import array, concatenate
from math import ceil
from networkx import Graph
# ------------------------------- CONSTANTS --------------------------------- #

FILE = "test"

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
		I, G = map(int, lines[l].split(" "))
		l += 1
		grudges = [list(map(int, g.split(" "))) for g in lines[l:l+G]]
		l += G
		V = int(lines[l])
		l+= 1
		villages = [list(map(int, v.split(" "))) for v in lines[l:l+V]]
		l += V
		g = Graph()
		for n1, v1 in enumerate(villages):
			for n2, v2 in enumerate(villages):
				if n1 == n2 or v1[0] == v2[0]: continue
				if any(v1[0] in g and v2[0] in g for g in grudges):
					g.add_edge(n1, n2, weight = v1[1]+v2[1])
		problems.append((g, [v[1] for v in villages]))
	return problems

def solve_all(fname):
	"""Process each test case."""
	problems = read_file("%s.in" % fname)
	case = 1
	text = ""
	for p in problems:
		print("Solving Case #%s" % case)
		res = solve(*p)
		text += "Case #%s: %s\n" % (case, res)
		case += 1
	with open("%s.out" % fname, "w") as out:
		out.write(text[:-1])

# ----------------------- PROBLEM SPECIFIC FUNCTIONS ------------------------ #

def solve(g, populations):
	print(g.edges())
	print(g.nodes())
	if len(g.edges()) == 0:
		return 0
	print(g[0].values())
	order = [v[0] for v in sorted(enumerate(populations), key = lambda x: x[1])]
	print("order", order)
	res = 0
	for v in order:
		if v not in g:
			continue
		w = max([e['weight'] for e in g[v].values()] + [0])
		print("I take edge with weight %s from village %s" % (w, v))
		res += w
		g.remove_node(v)
	return res

# ------------------------------ ENTRYPOINT --------------------------------- #

solve_all(FILE)