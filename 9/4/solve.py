from math import ceil

FNAME = 'submit'

def main():
	output = ''
	for p, problem in enumerate(load_input(), 1):
		output += 'Case #%d: %s\n' % (p, solve(problem))
	with open('%sOutput' % FNAME, 'w', encoding='utf-8') as fp:
		fp.write(output)

def load_input():
	with open('%sInput' % FNAME, 'r', encoding='utf-8') as fp:
		problems = int(fp.readline())
		for p in range(problems):
			fp.readline()
			yield list(sorted(map(int, fp.readline().split(' '))))

def solve(candies):
	repetitions = 1
	for c in set(candies):
		times = candies.count(c)
		min_repetitions = c / gcd(times, c)
		repetitions = lcm(repetitions, min_repetitions)
	num_candies = len(candies) * repetitions
	num_people = 0
	for c in set(candies):
		num_people += (repetitions * candies.count(c)) / c
	simplify = gcd(num_candies, num_people)
	return '%d/%d' % (num_candies / simplify, num_people / simplify)

def gcd(a, b):
	while b > 0:
		a, b = b, a % b
	return a

def lcm(a, b):
	return a * b / gcd(a, b)

if __name__ == '__main__':
	main()