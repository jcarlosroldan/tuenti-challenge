# Tuenti Challenge Edition 8 Level 10
PROBLEM_SIZE = "submit"

# -- jam input/output ------------------------------------------------------- #

def parse_problems(lines):
	""" Given a list of lines, parses them and returns a list of problems. """
	i = 0
	res = []
	while i < len(lines):
		P, G = map(int, lines[i].split())
		grudges = [tuple(map(int, lines[i + n + 1].split())) for n in range(G)]
		i += G + 1
		res.append((P, grudges))
	return res

def solve_all():
	""" Process each test case and generate the output file. """
	res = ""
	with open("%s.in" % PROBLEM_SIZE, "r", encoding="utf-8") as fp:
		lines = fp.read().strip().split("\n")[1:]
	problems = parse_problems(lines)
	for case, problem in enumerate(problems, 1):
		print("Solving Case #%s" % case)
		sol = solve(*problem)
		print(">> %s" % sol)
		res += "Case #%s: %s\n" % (case, sol)
	with open("%s.out" % PROBLEM_SIZE, "w", encoding="utf-8") as fp:
		fp.write(res[:-1])

# -- problem specific functions --------------------------------------------- #

def solve(P, grudges):
	grudges = tuple(sorted(tuple(sorted(g)) for g in grudges if abs(g[0] - g[1]) % 2))
	print(P, len(grudges))
	if P % 2: return 0
	return ways(P, grudges) % (10**9 + 7)

_ways_mem = {}
def ways(P, grudges):
	if (P, grudges) in _ways_mem:
		return _ways_mem[(P, grudges)]
	elif P == 0:
		res = 1
	elif len(grudges) == 0:
		res = catalan(P / 2)
	else:
		res = 0
		for n in range(1, P, 2):
			if (0, n) not in grudges:
				gs1 = tuple((c1 - 1, c2 - 1) for c1, c2 in grudges if c1 >= 1 and c2 <= n - 1)
				gs2 = tuple((c1 - n - 1, c2 - n - 1) for c1, c2 in grudges if c1 >= n + 1)
				res += ways(n - 1, gs1) * ways(P - n - 1, gs2)
	_ways_mem[(P, grudges)] = res
	return res

_catalan_mem = {}
def catalan(n):
	if n in _catalan_mem: return _catalan_mem[n]
	if n <= 1:
		res = 1
	else:
		res = 0
		for i in range(int(n)): res += catalan(i) * catalan(n - i - 1)
	_catalan_mem[n] = res
	return res

# -- entrypoint ------------------------------------------------------------- #

if __name__ == "__main__":
	solve_all()
	# print(solve(100, [(50,51)]))