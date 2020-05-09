# Tuenti Challenge Edition 8 Level 15
from math import sqrt

PROBLEM_SIZE = "test"

# -- jam input/output ------------------------------------------------------- #

def parse_problems(lines):
	""" Given a list of lines, parses them and returns a list of problems. """
	res = [list(map(int, ln.split(" "))) for ln in lines]
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
	with open("%s2.out" % PROBLEM_SIZE, "w", encoding="utf-8") as fp:
		fp.write(res[:-1])

# -- problem specific functions --------------------------------------------- #

def lcg(S, U, I, O):
	base = S % O
	while True:
		yield base
		base = (base * U + I) % O

def lcg_explicit(S, U, I, O):
	n = 0
	while True:
		# TODO -> U ^ period mod O = 1;
		x = (U**n * S + (U**n - 1) * I // (U - 1)) % O

		yield x
		n += 1

def solve(S, U, I, O):
	print(S, U, I, O)
	print(baby_steps_giant_steps(U, 1 + O, O))
	cg = lcg(S, U, I, O)
	seen = []
	while True:
		n = next(cg)
		if n in seen:
			period = (len(seen) - seen.index(n))
			# print(U ** period % O)
			print("period: %s" % period)
			return len(seen) + 1  # first repeated index
		seen.append(n)

def baby_steps_giant_steps(a, b, p, N=None):
	if not N:
		N = 1 + int(sqrt(p))

	# initialize baby_steps table
	baby_steps = {}
	baby_step = 1
	for r in range(N + 1):
		baby_steps[baby_step] = r
		baby_step = baby_step * a % p

	# now take the giant steps
	giant_stride = pow(a, (p - 2) * N, p)
	giant_step = b
	for q in range(N + 1):
		if giant_step in baby_steps:
			return q * N + baby_steps[giant_step]
		else:
			giant_step = giant_step * giant_stride % p
	return "No Match"

# -- entrypoint ------------------------------------------------------------- #

if __name__ == "__main__":
	solve(7, 11, 19, 29)
	#solve_all()
	# print(solve(15631, 31298, 14740, 245060) == 12255)
	# print(57905 ** 192 % 117344)