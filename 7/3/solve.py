# Tuenti Challenge Edition 7 Level 3
from re import match
from numpy import array, concatenate
from math import ceil, log

# ------------------------------- CONSTANTS --------------------------------- #

FILE = "submit"

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
	return int(log(int(p), 2)) + 1

# ------------------------------ ENTRYPOINT --------------------------------- #

solve_all(FILE)