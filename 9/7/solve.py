from math import ceil, floor

FNAME = 'submit'
HASH_LEN = 16

def main():
	output = ''
	for p, problem in enumerate(load_input(), 1):
		output += 'Case #%d: %s\n' % (p, solve(*problem))
	with open('%sOutput' % FNAME, 'w', encoding='iso-8859-1') as fp:
		fp.write(output)

def load_input():
	with open('%sInput' % FNAME, 'r', encoding='iso-8859-1') as fp:
		problems = int(fp.readline())
		for p in range(problems):
			res = []
			for _ in range(2):
				doc = [fp.readline() for _ in range(int(fp.readline()))]
				doc = ''.join(line.strip() for line in doc)
				res.append(doc)
			yield res

def solve(original, altered):
	goal = hash([ord(o) for o in original.replace('\n', '')])
	payload_start = original.index('------') + 3
	altered = [ord(o) for o in altered.replace('\n', '')]
	goal = [g - p for g, p in zip(goal, hash(altered[:payload_start]))]
	altered_body = hash(altered[payload_start:])
	min_payload = 'z' * 100
	for payload_offset in range(16):
		new_goal = [(g - b) % 256 for g, b in zip(goal, rot(altered_body, payload_start + payload_offset))]
		new_goal = rot(new_goal, -payload_start)
		for lines in range(10):
			payload = [0] * (payload_offset + lines * 16)
			for i in range(16):
				decomposition = min_decomposition(new_goal[i], lines + (1 if i < payload_offset else 0))
				if decomposition == None:
					break
				else:
					for n, d in enumerate(decomposition):
						payload[i + n * 16] = d
			else:
				payload = ''.join(chr(p) for p in payload)
				if len(payload) < len(min_payload) or len(payload) == len(min_payload) and payload < min_payload:
					min_payload = payload
				break
	return min_payload


def hash(input_text):
	res = [0] * HASH_LEN
	for i in range(len(input_text)):
		res[i % HASH_LEN] = (res[i % HASH_LEN] + input_text[i]) % 2**8
	return res

def rot(seq, offset):
	return seq[-offset % len(seq):] + seq[:-offset % len(seq)]

def min_decomposition(n, elems, min_e=48, max_e=122):
	remaining = n
	while remaining < min_e * elems: remaining += 2**8
	res = []
	for e in range(elems - 1, -1, -1):
		res.append(min(max_e, remaining - e * min_e))
		remaining -= res[-1]
	if remaining > 0:
		return None
	else:
		return list(reversed(res))

if __name__ == '__main__':
	main()