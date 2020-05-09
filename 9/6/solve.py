from math import ceil
from networkx import DiGraph, all_topological_sorts

FNAME = 'submit'

def main():
	output = ''
	for p, problem in enumerate(load_input(), 1):
		output += 'Case #%d: %s\n' % (p, solve(problem))
	with open('%sOutput' % FNAME, 'w', encoding='utf-8') as fp:
		fp.write(output)

def load_input():
	with open('%sInput' % FNAME, 'r', encoding='utf-8') as fp:
		problems = int(fp.readline())
		for p in range(problems):
			print(p)
			words = int(fp.readline())
			yield [fp.readline().strip() for _ in range(words)]

def solve(words):
	chars = set(char for word in words for char in word)
	if len(chars) == 1:
		return words[0][0]
	lts = less_than_relations(words)
	dg = DiGraph()
	dg.add_edges_from(lts)
	res = None
	for toposort in all_topological_sorts(dg):
		if len(toposort) < len(chars) or res != None:
			return 'AMBIGUOUS'
		else:
			res = toposort
	return ' '.join(res)

def less_than_relations(words):
	res = set()
	starts = [w[0] for w in words]
	for s1, s2 in zip(starts[:-1], starts[1:]):
		if s1 != s2:
			res.add((s1, s2))
	for start in starts:
		subwords = [w[1:] for w in words if w.startswith(start) and len(w) > 1]
		res.update(less_than_relations(subwords))
	return res

if __name__ == '__main__':
	main()