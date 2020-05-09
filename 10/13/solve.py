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
			yield int(fp.readline())

def solve(rolls):
	if rolls < simple_rolls(3): return 'IMPOSSIBLE'
	h = 3
	while True:
		min_rolls = simple_rolls(h + 1)
		if min_rolls <= rolls:
			h += 1
		else:
			break
	used_rolls = simple_rolls(h)
	s = 0
	while True:
		min_rolls = extra_rolls(s + 1, h)
		if min_rolls <= rolls - used_rolls:
			s += 1
		else:
			break
	used_rolls += extra_rolls(s, h)
	print(s, h, used_rolls)
	return '%d %d' % (h, used_rolls)

def simple_rolls(h):
	return (16 * h**3 - 36 * h**2 - h + 24) // 3

def extra_rolls(s, h):
	if s == 0: return 0
	return (2 * s) * (h**2 - h) - h + h * (s // 2 - 1 + s % 2) * (s // 2 - 1)

if __name__ == '__main__':
	main()