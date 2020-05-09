# Tuenti Challenge Edition 7 Level 10
from dateutil.parser import parse
from datetime import timedelta
from binascii import crc32 as _crc32
from hashlib import md5 as _md5
from math import ceil
from numpy import array, concatenate
from os import listdir
from json import load
from re import match

# ------------------------------- CONSTANTS --------------------------------- #

FILE = "submit"
MAX_SIDE_LEN = 2**32
secret_dic = {}

def modexp ( g, u, p ):
	"""computes s = (g ^ u) mod p
      args are base, exponent, modulus
      (see Bruce Schneier's book, _Applied Cryptography_ p. 244)"""
	s = 1
	while u != 0:
		if u & 1:
			s = (s * g)%p
		u >>= 1
		g = (g * g)%p;
	return s

# ------------------------ GENERAL PURPOSE UTILITIES ------------------------ #

crc32 = lambda x: _crc32(str.encode(x)) & 0xffffffff

def md5(text):
	m = _md5()
	m.update(str.encode(text))
	return m.hexdigest()

# ------------------------ JAM SPECIFIC FUNCTIONS --------------------------- #

def read_file(fname):
	"""Read input file format."""
	with open(fname,"r") as f:
		lines = f.read().strip().split("\n")[1:]
	i = 0
	res = []
	while i < len(lines):
		date, times = lines[i].split(" ")
		times = int(times)
		changes = [l.split(" ") for l in lines[i+1:i+1+times]]
		res.append((date, changes))
		i += times +1
	return res

def solve_all(fname):
	"""Process each test case."""
	problems = read_file("%s.in" % fname)
	case = 1
	text = ""
	init_dic()
	for p in problems:
		print("Solving Case #%s" % case)
		res = solve(*p)
		text += "Case #%s: %s\n" % (case, res)
		case += 1
	with open("%s.out" % fname, "w") as out:
		out.write(text[:-1])

# ----------------------- PROBLEM SPECIFIC FUNCTIONS ------------------------ #

def init_dic():
	global secret_dic
	with open("secrets.json", "r") as f:
		secret_dic = load(f)

def encode(date, user_id, hash = None):
	while date not in secret_dic:
		date = (parse(date)-timedelta(1)).strftime("%F")
	secret1, secret2 = secret_dic[date]

	if hash == None:
		# First password for this user
		secret3 = crc32(user_id)
	else:
		# Existing user, password reset
		secret3 = crc32(hash)

	counter = secret3

	# The loop didn't made the passwords hard to reverse :()
	counter = counter * modexp(secret1, 10000000, secret2) % secret2

	password = ""
	for i in range(10):
		# Generate random passwords
		counter = (counter * secret1) % secret2
		password += chr(counter % 94 + 33)

	hash = md5(password)
	return (password, hash)

def solve(user_id, dates):
	hash = None
	for date, times in dates:
		for _ in range(int(times)):
			pw, hash = encode(date, user_id, hash)
	return pw

# ------------------------------ ENTRYPOINT --------------------------------- #

solve_all(FILE)