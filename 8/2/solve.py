# Tuenti Challenge Edition 8 Level 2
PROBLEM_SIZE = "submit"

# -- jam input/output ------------------------------------------------------- #

def parse_problems(lines):
	""" Given a list of lines, parses them and returns a list of problems. """
	return [len(p) for p in lines]

def solve_all():
	""" Process each test case and generate the output file. """
	res = ""
	with open("%s.in" % PROBLEM_SIZE, "r", encoding="utf-8") as fp:
		lines = fp.read().strip().split("\n")[1:]
	problems = parse_problems(lines)
	for case, problem in enumerate(problems, 1):
		print("Solving Case #%s" % case)
		res += "Case #%s: %s\n" % (case, solve(problem))
	with open("%s.out" % PROBLEM_SIZE, "w", encoding="utf-8") as fp:
		fp.write(res[:-1])

# -- problem specific functions --------------------------------------------- #

def base10(number, base):
	res = 0
	for digit, pos in enumerate(number):
		res += digit * base ** (len(number) - pos - 1)
	return res

def solve(base):
	max_value = list(reversed(range(base)))
	min_value = [1, 0] + list(range(base))[2:]
	return base10(max_value, base) - base10(min_value, base)

# -- entrypoint ------------------------------------------------------------- #

if __name__ == "__main__":
	solve_all()