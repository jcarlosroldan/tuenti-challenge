# Tuenti Challenge Edition 6 Level 2
from collections import Counter

with open("corpus.txt", "r") as f:
	corpus = f.read().split(" ")

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
		bounds = p.split(" ")
		res = solve(int(bounds[0]),int(bounds[1]))
		text += "Case #%s: %s\n" % (case, res)
		case+=1
	with open("%s.out" % fname, "w") as out:
		out.write(text[:-1])

def solve(first,last):
	"""Solve an individual problem."""
	words = corpus[first:last+2]
	freqs = Counter(words).most_common(3)
	return ",".join("%s %s"%f for f in freqs)


solve_all("test")