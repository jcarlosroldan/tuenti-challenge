from math import ceil

FNAME = 'submit'

def main():
	output = ''
	for p, problem in enumerate(load_input(), 1):
		output += 'Case #%d: %d\n' % (p, solve(*problem))
	with open('%sOutput' % FNAME, 'w', encoding='utf-8') as fp:
		fp.write(output)

def load_input():
	with open('%sInput' % FNAME, 'r', encoding='utf-8') as fp:
		problems = int(fp.readline())
		for p in range(problems):
			yield map(int, fp.readline().split(' '))

def solve(onion, no_onion):
	return ceil(onion / 2) + ceil(no_onion / 2)

if __name__ == '__main__':
	main()