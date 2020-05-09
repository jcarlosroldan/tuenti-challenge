from networkx import DiGraph, maximum_flow_value

FNAME = 'submit'

def main():
	output = ''
	for p, problem in enumerate(load_input(), 1):
		output += 'Case #%d: %s\n' % (p, solve(*problem))
	with open('%sOutput.txt' % FNAME, 'w', encoding='utf-8') as fp:
		fp.write(output)

def load_input():
	with open('%sInput.txt' % FNAME, 'r', encoding='utf-8') as fp:
		problems = int(fp.readline())
		for p in range(problems):
			F, G = map(int, fp.readline().split(' '))
			groups = []
			for g in range(G):
				E, _ = map(int, fp.readline().split(' '))
				floors = list(map(int, fp.readline().split(' ')))
				groups.append((E, floors))
			yield F, groups

def solve(F, groups):
	print(F)
	# build the graph of employee flow
	G = DiGraph()
	for g, (e, floors) in enumerate(groups):
		G.add_edge('s', 'g%d' % g, capacity=e)
		[G.add_edge('g%d' % g, f) for f in floors]
	[G.add_edge(f, 't', capacity=1) for f in range(F)]
	# find the minimum wc value by reducing the range
	total_employees = sum(e for e, _ in groups)
	wc_range = [1, total_employees]
	while wc_range[0] != wc_range[1]:
		midpoint = (wc_range[0] + wc_range[1]) // 2
		for f in range(F):
			G[f]['t']['capacity'] = midpoint
		flow = maximum_flow_value(G, 's', 't')
		if flow == total_employees:
			wc_range[1] = midpoint
		else:
			wc_range[0] = midpoint if midpoint != wc_range[0] else wc_range[1]
	return wc_range[0]

if __name__ == '__main__':
	main()