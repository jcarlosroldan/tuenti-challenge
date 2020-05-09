from math import sqrt

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
			yield map(int, fp.readline().strip().split(' '))

def solve(X, *N):
	res = [1] + [0] * X
	for i in range(1, X):
		if i not in N:
			for j in range(i, X + 1):
				res[j] += res[j - i]
	return res[X]

if __name__ == '__main__':
	main()