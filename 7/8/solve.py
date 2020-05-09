# Tuenti Challenge Edition 7 Level 4
from re import match
from numpy import array, concatenate
from math import ceil

# ------------------------------- CONSTANTS --------------------------------- #

FILE = "submit"
GOOD_NUMBER_REGEX = "[\d]+$"

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
	with open(fname,"r",encoding="utf-16-le") as f:
		lines = f.read().strip().split("\n")[1:]
	return group_list(lines, 1)

def solve_all(fname):
	"""Process each test case."""
	problems = read_file("%s.in" % fname)
	case = 1
	text = ""
	for p in problems:
		print("Solving Case #%s" % case)
		res = solve(p[0].strip())
		text += "Case #%s: %s\n" % (case, res)
		case += 1
	with open("%s.out" % fname, "w") as out:
		out.write(text[:-1])

# ----------------------- PROBLEM SPECIFIC FUNCTIONS ------------------------ #

def solve(p):
	if match(GOOD_NUMBER_REGEX, p):
		return "%x" % int(p)
	else:
		return "N/A"

# ------------------------------ ENTRYPOINT --------------------------------- #

solve_all(FILE)