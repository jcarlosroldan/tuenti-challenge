from math import ceil

FNAME = 'submit'
LAYOUT = '1234567890QWERTYUIOPASDFGHJKL;ZXCVBNM,.-'

def main():
	output = ''
	for p, problem in enumerate(load_input(), 1):
		output += 'Case #%d: %s\n' % (p, solve(*problem))
	with open('%sOutput' % FNAME, 'w', encoding='utf-8') as fp:
		fp.write(output)

def load_input():
	with open('%sInput' % FNAME, 'r', encoding='utf-8') as fp:
		problems = int(fp.readline())
		for p in range(problems):
			yield fp.readline().strip(), fp.readline().strip()

def solve(author, message):
	offset = [a - m for a, m in zip(keyboard_pos(author), keyboard_pos(message[-1]))]
	return ''.join(shift(c, offset) for c in message)

def keyboard_pos(char):
	res = LAYOUT.index(char)
	return res // 10, res % 10

def shift(char, offset):
	if char == ' ': return ' '
	pos = keyboard_pos(char)
	pos = [(pos[0] + offset[0]) % 4, (pos[1] + offset[1]) % 10]
	return LAYOUT[pos[0] * 10 + pos[1]]

if __name__ == '__main__':
	main()