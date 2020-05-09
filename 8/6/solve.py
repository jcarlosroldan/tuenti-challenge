# Tuenti Challenge Edition 8 Level 6
PROBLEM_SIZE = "test"

# -- jam input/output ------------------------------------------------------- #

def parse_problems(lines):
	""" Given a list of lines, parses them and returns a list of problems. """
	res = []
	i = 0
	while i < len(lines):
		N = int(lines[i])
		notes = [tuple(map(int, l.split(" "))) for l in lines[i + 1:i + N + 1]]
		res.append((N, notes))
		i += N + 1
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
	with open("%s2.out" % PROBLEM_SIZE, "w", encoding="utf-8") as fp:
		fp.write(res[:-1])

# -- problem specific functions --------------------------------------------- #

def solve(N, notes):
	score = 0
	print("generating")
	# transform notes to a list of (start_t, end_t, score) sorted by start_t
	scores = {}
	for x, l, s, p in notes:
		key = (int(x / s), int((x + l) / s))
		if key in scores:
			scores[key] += p
		else:
			scores[key] = p
	print("delaying")
	# delay a bit start times and promote a bit end times, to disallow overlapping
	notes = [(s * 2 - 1, e * 2 + 1, p) for (s, e), p in scores.items()]
	print("computing with %s elements" % len(notes))
	return compute(notes)

def compute(notes):
	""" O(n^2) solution. Polynomial time could be reached using interval graphs. """
	last_release = max(n[1] for n in notes) + 1
	releases = [[] for _ in range(last_release)]
	for s, e, p in notes:
		releases[e].append((s, p))
	T = [0] * last_release
	for r in range(1, last_release):
		if releases[r]:
			for s, p in releases[r]:
				C = p + T[s]
				if C > T[r]: T[r] = C
			for i in range(r + 1, last_release):
				T[i] = max(T[i], T[r])
	return T[-1]

# -- entrypoint ------------------------------------------------------------- #

if __name__ == "__main__":
	solve_all()