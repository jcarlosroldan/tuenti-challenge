from math import ceil

FNAME = 'submit'

def main():
	output = ''
	for p, problem in enumerate(load_input(), 1):
		output += 'Case #%d:%s\n' % (p, solve(*problem))
	with open('%sOutput' % FNAME, 'w', encoding='utf-8') as fp:
		fp.write(output)

def load_input():
	with open('%sInput' % FNAME, 'r', encoding='utf-8') as fp:
		problems = int(fp.readline())
		for p in range(problems):
			w, h, f, p = map(int, fp.readline().split(' '))
			folds = [fp.readline().strip() for fold in range(f)]
			punches = [tuple(map(int, fp.readline().split(' '))) for punch in range(p)]
			yield w, h, folds, punches

def solve(w, h, folds, punches):
	res = punches
	for fold in folds:
		if fold == 'T':
			punches = [(x, h - y - 1) for x, y in punches] + [(x, h + y) for x, y in punches]
			h *= 2
		elif fold == 'B':
			punches = punches + [(x, 2 * h - y - 1) for x, y in punches]
			h *= 2
		elif fold == 'L':
			punches = [(w - x - 1, y) for x, y in punches] + [(w + x, y) for x, y in punches]
			w *= 2
		elif fold == 'R':
			punches = punches + [(2 * w - x - 1, y) for x, y in punches]
			w *= 2
	return '\n' + '\n'.join('%s %s' % punch for punch in sorted(punches))

def draw(punches, w, h):
	draw = [['x' for e in range(w)] for _ in range(h)]
	for x, y in punches:
		draw[y][x] = 'o'
	print('\n'.join(''.join(line) for line in draw))

if __name__ == '__main__':
	main()