# Tuenti Challenge Edition 7 Level 2
from re import match
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
	return group_list(lines, 2)

def solve_all(fname):
	"""Process each test case."""
	problems = read_file("%s.in" % fname)
	case = 1
	text = ""
	for p in problems:
		print("Solving Case #%s" % case)
		res = solve(p[1])
		text += "Case #%s: %s\n" % (case, res)
		case += 1
	with open("%s.out" % fname, "w") as out:
		out.write(text[:-1])

# ----------------------- PROBLEM SPECIFIC FUNCTIONS ------------------------ #

def solve(p):
	rolls = list(map(int, p.split(" ")))
	game = []
	score = 0
	i = 0
	while True:
		if rolls[i] == 10:
			score += sum(rolls[i:i+3])
			i += 1
		else:
			if sum(rolls[i:i+2]) == 10:
				score += sum(rolls[i:i+3])
			else:
				score += sum(rolls[i:i+2])
			i += 2
		game.append(score)
		if len(game) == 10:
			break
	return " ".join(map(str, game))

# ------------------------------ ENTRYPOINT --------------------------------- #

solve_all(FILE)