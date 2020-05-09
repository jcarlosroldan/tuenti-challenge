from networkx import DiGraph, all_simple_paths
from math import ceil

FNAME = 'submit'

def main():
	output = ''
	for p, problem in enumerate(load_input(), 1):
		output += 'Case #%d: %d\n' % (p, solve(problem))
	with open('%sOutput' % FNAME, 'w', encoding='utf-8') as fp:
		fp.write(output)

def load_input():
	with open('%sInput' % FNAME, 'r', encoding='utf-8') as fp:
		problems = int(fp.readline())
		for p in range(problems):
			planets = {}
			for planet in range(int(fp.readline())):
				source, destinations = fp.readline().strip().split(':')
				destinations = destinations.split(',')
				planets[source] = destinations
			yield planets

def solve(planets):
	dg = DiGraph(planets)
	return len(list(all_simple_paths(dg, 'Galactica', 'New Earth')))


if __name__ == '__main__':
	main()