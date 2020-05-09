from re import compile, DOTALL
from dynprog import DynProg
from bisect import insort

FNAME = 'test'

RE_COMPRESS_COMMA = compile(r',+').sub

def main():
	output = ''
	for p, problem in enumerate(load_input(), 1):
		#if p != 57: continue
		print(p)
		output += 'Case #%d: %s\n' % (p, solve(problem))
	with open('%sOutput.txt' % FNAME, 'w', encoding='utf-8') as fp:
		fp.write(output)

def load_input():
	with open('%sInput.txt' % FNAME, 'r', encoding='utf-8') as fp:
		problems = int(fp.readline())
		for p in range(problems):
			L = int(fp.readline())
			yield ''.join(fp.readline() for _ in range(L))[:-1]

def solve(input_text):
	# standarize the string
	text = ''
	for char in input_text:
		if char in '[],':
			text += char
		elif char == '\n':
			text += 'N'
		else:
			text += 'O'
	# base cases
	if len(text) < 3: return 'IMPOSSIBLE'
	# initialise the search
	#print(text)
	t0 = text
	text = '[' + text[1:-1] + ']'
	if penalty(text) == 0: return distance(text, t0)
	to_explore = {(text, distance(text, t0), penalty(text))}
	explored = set()
	limit = len(text)
	best = limit
	while len(to_explore):
		current = min(to_explore, key=lambda c: c[2])
		#print(current)
		to_explore.remove(current)
		explored.add(current)
		alts = {
			(a, distance(a, t0), penalty(a))
			for a in alternatives(current[0])
		}
		alts = {a for a in alts if a not in to_explore and a not in explored and a[1] + a[2] // 2 <= limit}
		to_explore.update(alts)
		for alt, dist, pen in alts:
			if pen == 0 and dist < limit:
				#print(alt, dist, pen)
				limit = dist
				best = dist
				to_explore = {(a, d, p) for a, d, p in to_explore if p + d // 2 <= limit}
	if penalty(text) > best:
		print(text, penalty(text, True), best)
	return best

def alternatives(text):
	for c, char in enumerate(text):
		if char == ']' and c < len(text) - 1:
			yield text[:c] + '[' + text[c + 1:]
			yield text[:c] + ',' + text[c + 1:]
			yield text[:c] + 'O' + text[c + 1:]
		elif char == '[' and c > 0:
			yield text[:c] + ']' + text[c + 1:]
			yield text[:c] + ',' + text[c + 1:]
			yield text[:c] + 'O' + text[c + 1:]
		elif char == 'O':
			yield text[:c] + ']' + text[c + 1:]
			yield text[:c] + '[' + text[c + 1:]
			yield text[:c] + ',' + text[c + 1:]
		elif char == 'N':
			yield text[:c] + ']' + text[c + 1:]
			yield text[:c] + '[' + text[c + 1:]
			yield text[:c] + ',' + text[c + 1:]
			yield text[:c] + 'O' + text[c + 1:]

_penalty_mem = {}
def penalty(text, verbose=False):
	if text in _penalty_mem: return _penalty_mem[text]
	res = 0
	depth = 0
	last_c = len(text) - 1
	for c, char in enumerate(text):
		depth += 1 if char == '[' else -1 if char == ']' else 0
		bad_char = depth > last_c - c
		bad_char = bad_char or char == '[' and c != 0 and text[c - 1] in 'NO]'
		if c != last_c and depth <= 0:
			bad_char = True
			depth += 1
		bad_char = bad_char or char == 'N' and ',' not in text[:c].rsplit('N', 1)[-1]
		bad_char = bad_char or c == last_c and ',' not in text.rsplit('N', 1)[-1]
		bad_char = bad_char or char == 'O' and c > 0 and text[c - 1] == ']'
		bad_char = bad_char or ',' in text and (c == 0 and char != '[' or c == last_c and char != ']')
		if bad_char: res += 1
		if verbose: print(depth, char, bad_char)
	if len(text) < 30:
		_penalty_mem[text] = res
	return res

def distance(seq1, seq2):
	return sum(1 for c1, c2 in zip(seq1, seq2) if c1 != c2)

if __name__ == '__main__':
	main()