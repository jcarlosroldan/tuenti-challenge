# Tuenti Challenge Edition 8 Level 8
from functools import reduce
from traceback import print_exc
from requests import post
from json import loads
from time import sleep

PROBLEM_SIZE = "submit"

# -- jam input/output ------------------------------------------------------- #

def parse_problems(lines):
	""" Given a list of lines, parses them and returns a list of problems. """
	res = []
	i = 0
	while i < len(lines):
		D = int(lines[i])
		res.append([tuple(map(int, l.split())) for l in lines[i + 1: i + D + 1]])
		i += D + 1
	return res

def solve_all():
	""" Process each test case and generate the output file. """
	res = ""
	with open("%s.in" % PROBLEM_SIZE, "r", encoding="utf-8") as fp:
		lines = fp.read().strip().split("\n")[1:]
	problems = parse_problems(lines)
	for case, problem in enumerate(problems, 1):
		print("Solving Case #%s" % case)
		sol = solve(problem)
		print(sol)
		res += "Case #%s: %s\n" % (case, sol)
	with open("%s.out" % PROBLEM_SIZE, "w", encoding="utf-8") as fp:
		fp.write(res[:-1])

# -- problem specific functions --------------------------------------------- #

def solve(doors):
	print(doors)
	mods = []
	rems = []
	for n, (P, T) in enumerate(doors):
		mods.append(P)
		rems.append(-(T + n) % P)
	#print("\n".join(("x = %s mod %s") % (rem, mod) for rem, mod in zip(rems, mods)))
	try:
		return crt(mods, rems)
	except:
		return alternative_crt(mods, rems)

def inv(a, m):
	m0 = m
	x0 = 0
	x1 = 1
	if (m == 1):
		return 0
	while a > 1:
		q = a // m
		t = m
		m = a % m
		a = t
		t = x0
		x0 = x1 - q * x0
		x1 = t
	if x1 < 0: x1 = x1 + m0
	return x1

def crt(num, rem):
	# see https://www.geeksforgeeks.org/chinese-remainder-theorem-set-2-implementation/
	prod = 1
	for i in range(0, len(num)):
		prod = prod * num[i]
	result = 0
	for i in range(0, len(num)):
		pp = prod // num[i]
		result = result + rem[i] * inv(pp, num[i]) * pp
	result %= prod
	return result

def alternative_crt(mods, rems):
	""" Dirty trick using an online Chinese Remainder Calculator, since this implementation has some problems with NEVER results. """
	headers = {
		"Cookie": "60gpJ=R396254725; PHPSESSID=7d77df9469f2a166b97a5dccb282e4b3",
		"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0",
		"X-Requested-With": "XMLHttpRequest",
		"Accept": "application/json, text/javascript, */*; q=0.01"
	}
	data = {
		"tool": "chinese-remainder",
		"equations": "\n".join(("x = %s mod %s") % (rem, mod) for rem, mod in zip(rems, mods))
	}
	sleep(1.5)
	res = loads(post("https://www.dcode.fr/api/", data=data, headers=headers).text)["results"]
	if "ChineseRemainder" in res:
		return "NEVER"
	else:
		return int(res)


# -- entrypoint ------------------------------------------------------------- #

if __name__ == "__main__":
	solve_all()