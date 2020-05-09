FILE = "sample"

# -- core --------------------------------------------------

def parse_input():
	""" Return a list of ready-to-solve cases. """
	with open("%s.in" % FILE, "r") as f:
		lines = f.read().strip().split("\n")[1:]
	return lines

def solve_all():
	""" Solve each test case. """
	res = ""
	for case, problem in enumerate(parse_input()):
		print("Solving Case #%s" % (case + 1))
		res += "Case #%s: %s\n" % ((case + 1), solve(problem))
	with open("%s.out" % FILE, "w") as out:
		out.write(res[:-1])

# -- problem specific -------------------------------------

_students = None
def solve(p):
	global _students
	if _students == None:
		with open("students", "r") as fp:
			lines = [l.split(",", 1) for l in fp.read().strip().split("\n")]
		_students = {}
		for name, data in lines:
			if data not in _students:
				_students[data] = [name]
			else:
				_students[data].append(name)
	if p in _students:
		return ",".join(_students[p])
	else:
		return "NONE"


# -- entry point -------------------------------------

solve_all()