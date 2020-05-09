# Tuenti Challenge Edition 8 Level 13
from time import time
from math import ceil
from pprint import pprint

PROBLEM_SIZE = "submit"

# -- jam input/output ------------------------------------------------------- #

def parse_problems(lines):
	""" Given a list of lines, parses them and returns a list of problems. """
	return list(map(int, lines))

def solve_all():
	""" Process each test case and generate the output file. """
	res = ""
	with open("%s.in" % PROBLEM_SIZE, "r", encoding="utf-8") as fp:
		lines = fp.read().strip().split("\n")[1:]
	problems = parse_problems(lines)
	for case, problem in enumerate(problems, 1):
		print("Solving Case #%s" % case)
		sol = solve(problem)
		print(">> %s" % sol)
		res += "Case #%s: %s\n" % (case, sol)
	with open("%s2.out" % PROBLEM_SIZE, "w", encoding="utf-8") as fp:
		fp.write(res[:-1])

# -- problem specific functions --------------------------------------------- #

def solve(N):
	start = time()
	res = ways(*reduce(N, N, N)) % (10**9 + 7)
	print("%d\t%.4f" % (N, time() - start))
	return res

_mem_ways = {}
def ways(smallest, median):
	# key generation
	k = (smallest, median)
	# optimization
	if (median - smallest) > 1:
		base = ways(smallest, smallest)
		diff = ways(smallest, smallest + 1) - base
		return base + diff * (median - smallest)
	# solving
	if k in _mem_ways:
		res = _mem_ways[k]
	else:
		res = 1
		bases = {}
		for t in range(1, smallest):
			for m in range(t, min(smallest, t + 2)):
				y = 0
				for b in range(1, m + 1):
					x = ways(*reduce(t, m, b))
					y += x
				y += (median - m - 1) * x
				bases[t, m] = y
		res += sum(bases[(t, t)] * (2 * (smallest - t) - 1) for t in range(1, smallest))
		diffs = [(bases[(t, t + 1)] - bases[(t, t)]) for t in range(1, smallest - 1)]
		diffs2 = [d // (median - n) for n, d in enumerate(diffs, 2)]
		ns = [smallest - t - 1 for t in range(1, smallest - 1)]
		nns = [diff * (n * (n + 1)) // 2 for diff, n in zip(diffs, ns)]
		res += sum(nn - d * tetrahedral(smallest - n) for n, (d, nn) in enumerate(zip(diffs2, nns), 3))
		_mem_ways[k] = res
	return res

def reduce(top, mid, bot):
	return min(top, mid, bot), max(min(top, mid), bot)

def tetrahedral(n):
	return (n * (n + 1) * (n + 2)) // 6

# -- entrypoint ------------------------------------------------------------- #

if __name__ == "__main__":
	solve_all()