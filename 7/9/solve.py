# Tuenti Challenge Edition 7 Level 9
from re import match
from numpy import array, concatenate
from math import ceil

# ------------------------------- CONSTANTS --------------------------------- #

FILE = "input"
LARGE_NUMBER = 2**16

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
	return [map(int, l.split(" ")) for l in lines]

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

"""operations = [
	[0, 4, 2],#el quiebro de 1
	[0, 0, 2],#la extensión
	[0, 4, 1],
	[2, 2, 1],
	[2, 0, 1],
	[0, 8, 0],
	[2, 4, 0],
	[2, 2, 0],
	[2, 0, 0],
]
def solve(S, C, D):
	print(S,C,D)
	if C < 4:
		return 0
	else:
		S,C,D = S,C-4,D
		tot = 4
		for op in operations:
			s, c, d = op
			if S >= s and C >= c and D >= d:
				times = LARGE_NUMBER
				if s>0: times = min(times, S//s)
				if c>0: times = min(times, C//c)
				if d>0: times = min(times, D//d)
				print("appliying %s %s times" % (op, times))
				S -= s*times
				C -= c*times
				D -= d*times
				tot += (s+c+d)*times
		print(S,C,D)
		print(S < 2 and C <= 4 and D == 0)
		return tot"""

def solve(S,C,D):
	res = 0
	# four corners
	if C < 4:
		return 0
	else:
		C -= 4
		res += 4
	# fit long-line extensors
	n = D//2
	long_lines_placed = n>0
	D -= 2*n
	res += 2*n
	# fit mixed-line extensors
	if D == 1 and S >= 2:
		D = 0
		S -= 2
		res += 3
		short_lines_placed = True
	else:
		short_lines_placed = False
	# fit long-line-and-4-corners extensors
	if D == 1 and C >= 4:
		D = 0
		C -= 4
		res += 5
		long_lines_placed = True
	# eight curves are a 2-corner extensor
	n = C//8
	C -= 8*n
	res += 8*n
	# fit short-line extensors
	n = S//2
	short_lines_placed = short_lines_placed or n > 0
	S -= 2*n
	res += 2*n
	# if at least 2 lines placed, four curves are a break extensor
	if short_lines_placed or long_lines_placed:
		n = C//4
		C -= 4*n
		res += 4*n
	# if at least 2 lines placed, two curves are a 1-corner extensor
	if short_lines_placed:
		n = C//2
		C -= 2*n
		res += 2*n
	print(S,C,D)
	return res


# ------------------------------ ENTRYPOINT --------------------------------- #

solve_all(FILE)