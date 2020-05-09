from collections import Counter
from regex import compile  # unicode-aware regex library, requires pip install
from requests import get

FNAME = 'submit'
URL = 'https://contest.tuenti.net/resources/2020/resources/pg17013.txt'
REMOVE_INVALID = compile(r'[^abcdefghijklmnñopqrstuvwxyzáéíóúü]+').sub
SPACE_SPLIT = compile(r'\s+').split
ALL_DIGITS = compile(r'^\d+$').match

def main():
	load_context()
	output = ''
	for p, problem in enumerate(load_input(), 1):
		output += 'Case #%d: %s\n' % (p, solve(*problem))
	with open('%sOutput.txt' % FNAME, 'w', encoding='utf-8') as fp:
		fp.write(output)

_ctx_by_word = {}
_ctx_by_rank = {}
def load_context():
	global _ctx_by_word, _ctx_by_rank
	text = get(URL).text
	text = SPACE_SPLIT(REMOVE_INVALID(' ', text.lower()).strip())
	text = [word for word in sorted(text) if len(word) >= 3]
	text = Counter(text).most_common()
	for rank, (word, frequency) in enumerate(text, 1):
		_ctx_by_word[word] = '%d #%d' % (frequency, rank)
		_ctx_by_rank[rank] = '%s %d' % (word, frequency)

def load_input():
	with open('%sInput.txt' % FNAME, 'r', encoding='utf-8') as fp:
		problems = int(fp.readline())
		for p in range(problems):
			line = fp.readline().strip()
			yield line, ALL_DIGITS(line) is not None

def solve(line, is_ranking):
	if is_ranking:
		return _ctx_by_rank[int(line)]
	else:
		return _ctx_by_word[line]

if __name__ == '__main__':
	main()