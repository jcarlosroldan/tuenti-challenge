# Tuenti Challenge Edition 6 Level 1

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
	for N in problems:
		print("Solving Case #%s" % case)
		res = solve(int(N))
		text += "Case #%s: %s\n" % (case, res)
		case+=1
	with open("%s.out" % fname, "w") as out:
		out.write(text[:-1])

def solve(N):
	"""Solve an individual problem."""
	if N==0:
		return 0
	elif N<=4:
		return 1
	else:
		return (N-4)//2 + 1 + N%2


solve_all("problem")