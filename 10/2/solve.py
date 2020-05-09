from networkx import DiGraph, dag_longest_path

FNAME = 'submit'

def main():
	output = ''
	for p, problem in enumerate(load_input(), 1):
		output += 'Case #%d: %s\n' % (p, solve(problem))
	with open('%sOutput.txt' % FNAME, 'w', encoding='utf-8') as fp:
		fp.write(output)

def load_input():
	with open('%sInput.txt' % FNAME, 'r', encoding='utf-8') as fp:
		problems = int(fp.readline())
		for p in range(problems):
			yield [
				map(int, fp.readline().split(' '))
				for _ in range(int(fp.readline()))
			]

def solve(matches):
	players = set()
	losers = set()
	for p0, p1, p1_loser in matches:
		players.update((p0, p1))
		losers.add(p1 if p1_loser else p0)
	return max(players.difference(losers))


if __name__ == '__main__':
	main()