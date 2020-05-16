FNAME = 'test'
DVORAK = '[]\',.pyfgcrl/=oeuidhtns-;qjkxbwvz{}"<>PYFGCRL?+OEUIDHTNS_:QJKXBWVZ'
QWERTY = '-=qwertyuiop[]sdfghjkl;\'zxcvbn,./_+QWERTYUIOP{}SDFGHJKL:"ZXCVBN<>?'
DECODER = str.maketrans(DVORAK, QWERTY)


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
			yield fp.readline()[:-1]

def solve(text):
	return str.translate(text, DECODER)

if __name__ == '__main__':
	main()