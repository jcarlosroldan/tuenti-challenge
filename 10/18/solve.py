from functools import lru_cache
from math import inf
from sys import setrecursionlimit

setrecursionlimit(10000)  # we need to go deeper
FNAME = 'submit'

def main():
	output = ''
	for p, problem in enumerate(load_input(), 1):
		print('Solving case #%d' % p)
		output += 'Case #%d: %s\n' % (p, solve(problem))
	with open('%sOutput.txt' % FNAME, 'w', encoding='utf-8') as fp:
		fp.write(output)

def load_input():
	with open('%sInput.txt' % FNAME, 'r', encoding='utf-8') as fp:
		problems = int(fp.readline())
		for p in range(problems):
			L = int(fp.readline())
			yield ''.join(fp.readline() for _ in range(L))[:-1]

_text = None
_text_len = None
def solve(text):
	global _text, _text_len
	if len(text) < 3: return 'IMPOSSIBLE'
	_text = standarize(text)
	_text_len = len(_text)
	to_lolmao = all(',' in line for line in _text.split('N'))
	res = 0
	if _text[0] != '[':
		res += 1
		_text = '[' + _text[1:]
	if _text[-1] != ']':
		res += 1
		_text = _text[:-1] + ']'
	if to_lolmao:
		changes.cache_clear()
		res += changes(0, 0, None, False)
	else:
		comma_since_newline = False
		for pos in range(_text_len):
			if _text[pos] == ',':
				comma_since_newline = True
			if _text[pos] == 'N':
				if comma_since_newline:
					comma_since_newline = False
				else:
					comma_since_newline = True
					res += 1
		if not comma_since_newline:
			res += 1
	return res

def standarize(text):
	res = ''
	for char in text:
		if char in '[],':
			res += char
		elif char == '\n':
			res += 'N'
		else:
			res += 'O'
	return res

@lru_cache(None)
def changes(pos, depth, last_char, comma_since_newline):
	if pos == _text_len: return 0 if comma_since_newline else inf
	alts = []
	if pos == 0:
		alts.append('[')
	elif depth >= _text_len - pos:
		alts.append(']')
	else:
		alts.append(',')
		if _text[pos] == 'N' and comma_since_newline and last_char != ']':
			alts.append('N')
		if _text[pos] == 'O' and last_char != ']':
			alts.append('O')
		if last_char not in 'ON]' and depth < _text_len - pos - 1:
			alts.append('[')
		if depth > 1:
			alts.append(']')
	res = min(
		(alt != _text[pos]) + changes(
			pos + 1,
			depth + (alt == '[') - (alt == ']'),
			alt,
			alt != 'N' and comma_since_newline or alt == ','
		)
		for alt in alts
	)
	return res

if __name__ == '__main__':
	main()