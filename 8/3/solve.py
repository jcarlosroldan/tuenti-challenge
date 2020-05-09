# Tuenti Challenge Edition 8 Level 3
PROBLEM_SIZE = "submit"

# -- jam input/output ------------------------------------------------------- #

def parse_problems(lines):
	""" Given a list of lines, parses them and returns a list of problems. """
	problems = []
	i = 0
	while i < len(lines):
		if int(lines[i]) > 0:
			problems.append(lines[i+1].strip().split(" "))
			i += 2
		else:
			problems.append([])
			i += 1
	return problems

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

_numerical_notes = {"C": 0, "D": 1, "E": 2, "F": 2.5, "G": 3.5, "A": 4.5, "B": 5.5}
def numerical(note):
	res = _numerical_notes[note[0]]
	if note.endswith("b"):
		res -= .5
	elif note.endswith("#"):
		res += .5
	return res % 6

_scales = {}
def init():
	for key, pattern in [("m", "WHWWHWW"), ("M", "WWHWWWH")]:
		for root in ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]:
			scale = [numerical(root)]
			for shift in pattern:
				scale.append(scale[-1] + (1 if shift == "W" else .5))
			_scales[key + root] = set(n % 6 for n in scale)

def solve(notes):
	res = []
	notes = set(numerical(note) for note in notes)
	for scale, scale_notes in _scales.items():
		if scale_notes.issuperset(notes):
			res.append(scale)
	res = " ".join(sorted(res))
	if len(res) == 0: res = "None"
	return res

# -- entrypoint ------------------------------------------------------------- #

if __name__ == "__main__":
	init()
	solve_all()