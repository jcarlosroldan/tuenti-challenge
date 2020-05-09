from math import floor, ceil

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
			yield int(fp.readline().strip())

def solve(n):
	mn = n // 29 + (1 if n % 29 else 0)
	mx = n // 20
	if mn > mx:
		return 'IMPOSSIBLE'
	else:
		return mx

if __name__ == '__main__':
	main()