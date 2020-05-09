# Tuenti Challenge Edition 6 Level 3
from re import findall


class Interpreter:
	"""The interpreter of the machine."""
	states = {}

	def load(code):
		"""Load code to an interpreter."""
		lines = code.split("\n")
		# find the lines where states starts and ends
		# states have only 2 spaces of indentation, so line[3]!=" "
		bounds = [n for n in range(len(lines)) if lines[n][3]!=" "]
		bounds.append(len(lines))
		functs = [lines[start:end] for start, end in zip(bounds,bounds[1:])]
		for funct in functs:
			name = funct[0][2:-1]
			Interpreter.states[name] = State()
			Interpreter.states[name].load(funct[1:])

	def process(tape_str):
		"""Process a tape."""
		tape = list(tape_str)
		pos = 0
		st = "start"
		while st != "end":
			tape, pos, st = Interpreter.states[st].apply(tape, pos, st)
		r = "".join(tape)
		return r


class State:
	"""Represents one of the states defined by the interpreter."""

	def load(self, code):
		""" Load the State from the code."""
		self.cases = {}
		bounds = [n for n in range(len(code)) if code[n][4]=="'"]
		bounds.append(len(code))
		cs = [code[start:end] for start, end in zip(bounds,bounds[1:])]
		for c in cs:
			name = c[0][5:-2]
			actions = {}
			for action in c[1:]:
				k,v = findall("([\w#]+)",action)
				actions[k] = v
			self.cases[name] = actions

	def apply(self, tape, pos, state):
		"""Transform the tape applying current state actions."""
		if pos>=0 and pos<len(tape):
			val = tape[pos]
		else:
			val = " "
		if "write" in self.cases[val]:
			if val == " ":
				tape.append("")
			tape[pos] = self.cases[val]["write"]
		if "move" in self.cases[val]:
			if self.cases[val]["move"] == "right":
				pos+=1
			else:
				pos-=1
		if "state" in self.cases[val]:
			state = self.cases[val]["state"]
		return tape, pos, state
				

def read_file(fname):
	"""Read input file format."""
	with open(fname,"r") as f:
		code,tapes = f.read()[10:-5].split("\ntapes:\n")
		Interpreter.load(code)
		tapes = findall("'(.+)'", tapes)
	return tapes


def solve_all(fname):
	"""Process each test case."""
	problems = read_file("%s.in" % fname)
	case = 1
	text = ""
	for p in problems:
		print("Solving Case #%s" % case)
		res = solve(p)
		text += "Tape #%s: %s\n" % (case, res)
		case+=1
	with open("%s.out" % fname, "w") as out:
		out.write(text[:-1])


def solve(code):
	"""Solve an individual problem."""
	return Interpreter.process(code)


solve_all("submit")