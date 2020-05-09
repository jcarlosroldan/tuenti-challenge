# Tuenti Challenge Edition 6 Level 4
from re import findall

# all possible combos: long combos are subsumed by shorters one
expr = "^(D-RD-R-[^P]|R-D-RD-[^P]|D-LD-L-[^K])"

def read_file(fname):
	"""Read input file format."""
	with open(fname,"r") as f:
		data = f.read().split("\n")[1:-1]
	return data

def solve_all(fname):
	"""Process each test case."""
	problems = read_file("%s.in" % fname)
	case = 1
	text = ""
	for p in problems:
		print("Solving Case #%s" % case)
		moves = p+"-N"
		res = solve(moves)
		text += "Case #%s: %s\n" % (case, res)
		case+=1
	with open("%s.out" % fname, "w") as out:
		out.write(text[:-1])

def solve(moves):
	"""Solve an individual problem."""
	r = 0
	while "-" in moves:
		r += len(findall(expr,moves[:10]))
		moves = moves.split("-",1)[1]
	return r


solve_all("submit")