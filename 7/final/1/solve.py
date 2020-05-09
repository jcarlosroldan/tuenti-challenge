# Tuenti Challenge Edition 7 Level 4
from re import match, sub
from numpy import array, concatenate
from math import ceil

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
	return lines

def solve_all(fname):
	"""Process each test case."""
	problems = read_file("%s.in" % fname)
	case = 1
	text = ""
	for p in problems:
		print("Solving Case #%s" % case)
		res = solve(p)
		text += "Case #%s: %s\n" % (case, res)
		case += 1
	with open("%s.out" % fname, "w") as out:
		out.write(text[:-1])

# ----------------------- PROBLEM SPECIFIC FUNCTIONS ------------------------ #

valid = lambda x: match("[^aeiouy][^aeiouy][^aeiouy]", x)

vocals = list("aeiouy")
def solve(p):
	changes = 0
	consonants = 1
	# step 1: obvious 3-consonant problems
	places = []
	for n, c in enumerate(p):
		if c not in vocals:
			consonants += 1
		else:
			consonants = 0
		if consonants == 3:
			changes += 1
			places.append(n-1)
			consonants = 1
	if consonants == 2:
		changes += 1
		places.append(n-1)
	print(p)
	p = "".join(["a" if n in places else c for n,c in enumerate(p)])
	print(p)
	p = sub("[aeiouy][aeiouy]+", "aa", p)
	p = sub("[aeiouy]", "a", p)
	p = sub("[^aeiouy]", "n", p)
	print(p, changes)
	# step 2: 2-consonant assignment problems
	cons = 0
	vocs = 0
	for n, c in enumerate(p):
		if c in vocals:
			vocs += 1
		else:
			cons += 1
		print(n, cons, vocs)
		if vocs > 0 and cons == 1:
			cons = 0
			vocs = 0

		if cons > 1:
			changes += 1
			vocs = 0
			cons = 0
	if cons > 0:
		changes += 1
	return changes

# ------------------------------ ENTRYPOINT --------------------------------- #

solve_all(FILE)