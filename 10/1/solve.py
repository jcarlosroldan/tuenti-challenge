FNAME = 'submit'

def main():
	output = ''
	for p, problem in enumerate(load_input(), 1):
		print('Solving case #%d' % p)
		output += 'Case #%d: %s\n' % (p, solve(*problem))
	with open('%sOutput.txt' % FNAME, 'w', encoding='utf-8') as fp:
		fp.write(output)

def load_input():
	with open('%sInput.txt' % FNAME, 'r', encoding='utf-8') as fp:
		problems = int(fp.readline())
		for p in range(problems):
			yield sorted(fp.readline().strip().split(' '))

def solve(p1, p2):
	if p1 == 'R' and p2 == 'S':
		return 'R'  # rock beats scissors
	elif p1 == 'P' and p2 == 'R':
		return 'P'  # paper beats rock
	elif p1 == 'P' and p2 == 'S':
		return 'S'  # scissors beats paper
	else:
		return '-'  # it's a draw

if __name__ == '__main__':
	main()