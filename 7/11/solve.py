# Tuenti Challenge Edition 7 Level 10
from collections import defaultdict
from re import findall
from random import random
# ------------------------------- CONSTANTS --------------------------------- #

FILE = "submit"
START_AT = 366

# ------------------------ GENERAL PURPOSE UTILITIES ------------------------ #

all_in = lambda l1, l2: all(e in l2 for e in l1)

translate = {}
translate_index = 0
def t(text):
	global translate_index
	if text in translate:
		return translate[text]
	else:
		translate_index += 1
		translate[text] = translate_index
		return translate_index

# ------------------------ JAM SPECIFIC FUNCTIONS --------------------------- #

def read_file(fname):
	"""Read input file format."""
	with open(fname,"r") as f:
		data = f.read().strip()
	lines = data.split("\n")[1:]
	i = 0
	res = []
	while i < len(lines):
		# get colors
		K = int(lines[i])
		colors = [l.split(" ") for l in lines[i+1:i+1+K]]
		i += K + 1
		# simplify colors
		colors = {c[0]: tuple(map(t, c[2:])) for c in colors if len(c)>2}
		# get galaxies
		G = int(lines[i])
		i += 1
		galaxies = []
		for g in range(G):
			E = int(lines[i])
			energies = [l.split(" ") for l in lines[i+1:i+E+1]]
			galaxies.append(energies)
			i += E + 1
		# simplify galaxies
		gs = []
		for g in galaxies:
			energies = []
			for e in g:
				if e[0] in colors:
					energies.append( (colors[e[0]], int(e[1])) )
				else:
					energies.append( ((t(e[0]),), int(e[1])) )
			gs.append(energies)
		galaxies = gs
		# get wormholes
		W = int(lines[i])
		wormholes = [l.split(" ") for l in lines[i+1:i+1+W]]
		i += W + 1
		# simplify wormholes
		used_colors = set()
		ws = defaultdict(list)
		for w in wormholes:
			value = w[0]
			if w[0] in colors:
				value = colors[value]
			else:
				value = (t(value),)
			used_colors.update(value)
			ws[int(w[1])].append((int(w[2]), value))
		wormholes = ws
		# remove unused colors from galaxies
		for g in galaxies:
			to_remove = []
			for color in g:
				if not all(c in used_colors for c in color[0]):
					to_remove.append(color)
			for c in to_remove:
				g.remove(c)
		# if color A always appear with B, remove it
		occurrences = set()
		for g in galaxies:
			occurrences.update([c[0] for c in g])
		for w in wormholes.values():
			occurrences.update([c[1] for c in w])
		to_remove = []
		for color1 in used_colors:
			for color2 in used_colors:
				if color1 != color2 and color2 not in to_remove and all(color2 in o for o in occurrences if color1 in o):
					to_remove.append(color1)
					break
		for color in to_remove:
			for g in galaxies:
				for n in range(len(g)):
					if color in g[n][0]:
						g[n] = (tuple(p for p in g[n][0] if p != color), g[n][1])
			for w in wormholes.values():
				for n in range(len(w)):
					if color in w[n][1]:
						w[n] = (w[n][0], tuple(p for p in w[n][1] if p != color))
		# remove subsumed galaxy colors
		for g in galaxies:
			to_remove = []
			for color in g:
				if any(c2[1] < color[1] and all(c1 in c2[0] for c1 in color[0]) for c2 in g):
					to_remove.append(color)
			for c in to_remove:
				g.remove(c)
		# disable unreachable galaxies
		changed = True
		disabled = []
		while changed:
			changed = False
			can_visit = set()
			for gal, ws in wormholes.items():
				if gal in disabled:
					continue
				can_visit.update([c[0] for c in ws])
			for gal in wormholes.keys():
				if gal not in disabled and gal not in can_visit and gal > 0:
					disabled.append(gal)
					changed = True
		# append problem
		res.append((galaxies, wormholes, disabled))
	return res

def solve_all(fname):
	"""Process each test case."""
	problems = read_file("%s.in" % fname)
	case = START_AT
	text = ""
	for p in problems[case-1:]:
		print("Solving Case #%s" % case)
		print(len(p[0]), len(p[1]))
		res = solve(*p)
		print("Case #%s: %s\n" % (case, res))
		text += "Case #%s: %s\n" % (case, res)
		case += 1
	with open("%s.out" % fname, "w") as out:
		out.write(text[:-1])

# ----------------------- PROBLEM SPECIFIC FUNCTIONS ------------------------ #

visited = None
to_visit = None

def next_states(state, galaxies, wormholes):
	states = []
	# states from exploring available nodes
	for dst, colors in wormholes[state[1]]:
		if all(c in state[0] for c in colors):
			states.append((
				[c for c in state[0] if c not in colors],
				dst,
				state[2]
			))	
	# states from taking colors I haven't
	for colors, time in galaxies[state[1]]:
		new_colors = [c for c in colors if c not in state[0]]
		if len(new_colors):
			states.append((
				state[0] + new_colors,
				state[1],
				state[2] + time
			))
	return states

def solve(galaxies, wormholes, disabled):
	to_visit = [([], 0, 0)]
	visited = []
	# set unreachable galaxies as True
	remaining_galaxies = [n for n in range(len(galaxies)) if n not in disabled]
	# start exploring the universe!
	while len(to_visit):
		state = min(to_visit, key = lambda x: (x[2], x[1] not in remaining_galaxies))
		#print("Visiting %s" % list(state))
		to_visit.remove(state)
		visited.append(state)
		if state[1] in remaining_galaxies:
			remaining_galaxies.remove(state[1])
			if not len(remaining_galaxies):
				break
		for st in next_states(state, galaxies, wormholes):
			if any(st[1] == v[1] and st[2]>=v[2] and all_in(st[0], v[0]) for v in visited):
				continue
			else:
				to_visit = [v for v in to_visit if st[1]!=v[1] or st[2]>v[2] or not all_in(v[0], st[0])]
				#print("\tScheduling %s" % list(st))
				to_visit.append(st)
				visited.append(st)
	res = []
	for k in range(len(galaxies)):
		scs = [v[2] for v in visited if v[1] == k]
		if len(scs):
			res.append(min(scs))
		else:
			res.append(-1)
	print(len(visited))
	return " ".join(map(str, res))

# ------------------------------ ENTRYPOINT --------------------------------- #

solve_all(FILE)