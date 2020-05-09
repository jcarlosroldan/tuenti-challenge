# Tuenti Challenge Edition 7 Level 4
from re import match
from numpy import array, concatenate
from math import ceil

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
	return group_list(lines, 1)

def solve_all(fname):
	"""Process each test case."""
	problems = read_file("%s.in" % fname)
	case = 1
	text = ""
	for p in problems:
		print("Solving Case #%s" % case)
		res = solve(p[0])
		text += "Case #%s: %s\n" % (case, res)
		case += 1
	with open("%s.out" % fname, "w") as out:
		out.write(text[:-1])

# ----------------------- PROBLEM SPECIFIC FUNCTIONS ------------------------ #

def solve(p):
	lens = sorted(map(int, p.split(" ")[1:]))
	l = 0
	while l < len(lens):
		n = lens[l]
		if lens[0:l+1].count(n) > 3:
			lens.remove(n)
		l += 1
	N = len(lens)
	smallest = MAX_SIDE_LEN + 1
	for i in range(0, N):
		if lens[i] >= smallest: break
		for j in range(i + 1, N):
			if lens[i] + lens[j] >= smallest: break
			for k in range(j + 1, N):
				tot = lens[i] + lens[j] + lens[k]
				if lens[k] < lens[i] + lens[j] and tot < smallest:
					smallest = tot
				else:
					break
	if smallest == MAX_SIDE_LEN + 1:
		return "IMPOSSIBLE"
	else:
		return smallest

# ------------------------------ ENTRYPOINT --------------------------------- #

solve_all(FILE)