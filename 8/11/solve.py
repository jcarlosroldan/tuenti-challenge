# Tuenti Challenge Edition 8 Level 11
from igraph import Graph

PROBLEM_SIZE = "submit"

# -- jam input/output ------------------------------------------------------- #

def parse_problems(lines):
	""" Given a list of lines, parses them and returns a list of problems. """
	res = []
	i = 0
	while i < len(lines):
		N, M, I = map(int, lines[i].split())
		items = [tuple(map(int, ln.split())) for ln in lines[i + 1:i + I + 1]]
		i += I + 1
		res.append((N, M, items))
	return res

def solve_all():
	""" Process each test case and generate the output file. """
	res = ""
	with open("%s.in" % PROBLEM_SIZE, "r", encoding="utf-8") as fp:
		lines = fp.read().strip().split("\n")[1:]
	problems = parse_problems(lines)
	for case, problem in enumerate(problems, 1):
		print("Solving Case #%s" % case)
		res += "Case #%s: %s\n" % (case, solve(*problem))
	with open("%s.out" % PROBLEM_SIZE, "w", encoding="utf-8") as fp:
		fp.write(res[:-1])

# -- problem specific functions --------------------------------------------- #

"""def solve(N, M, items):
	print(N, M, len(items))
	g = Graph()
	[g.add_vertex("n%s" % n) for n in range(N)]
	[g.add_vertex("m%s" % m) for m in range(M)]
	[g.add_edge("n%s" % n, "m%s" % m) for n, m in items]
	return g.independence_number()"""

def solve(N, M, items):
	""" Greedy version """
	res = 0
	shoots = [0] * (N + M)
	for n, m in items:
		shoots[n] += 1
		shoots[N + m] += 1
	while any(s != None for s in shoots):
		av = min([(n, s) for n, s in enumerate(shoots) if s != None], key=lambda x: x[1])[0]
		res += 1
		shoots[av] = None
		if av < N:  # is a row
			for n, m in items:
				if n == av and shoots[N + m] != None:
					shoots[N + m] = None
					for n2, m2 in items:
						if m2 == m and shoots[n2] != None:
							shoots[n2] -= 1
		else:  # is a col
			for n, m in items:
				if m == av - N and shoots[n] != None:
					shoots[n] = None
					for n2, m2 in items:
						if n2 == n and shoots[N + m2] != None:
							shoots[N + m2] -= 1
	return res

# -- entrypoint ------------------------------------------------------------- #

if __name__ == "__main__":
	solve_all()