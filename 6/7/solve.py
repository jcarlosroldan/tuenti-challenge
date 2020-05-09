# Tuenti Challenge Edition 6 Level 7
from re import match
from numpy import array, concatenate

def kadane(arr, n):
	""" Kadane max submatrix sum algorithm """
	_sum = 0
	max_sum = -float('inf')
	finish = -1
	local_start = 0
	for i in range(n):
		_sum += arr[i]
		if _sum < 0:
			_sum = 0
			local_start = i+1
		elif _sum > max_sum:
			max_sum = _sum
			start = local_start
			finish = i

	if finish != -1:
		return max_sum

	max_sum = arr[0]
	start = finish = 0

	for i in range(1,n):
		if arr[i] > max_sum:
			max_sum = arr[i]
			start = finish = i
	return max_sum
 


def read_file(fname):
	"""Read input file format."""
	with open(fname,"r") as f:
		lines = f.read().split("\n")[1:-1]
		bounds = [i for i in range(len(lines)) if match("\d+ \d+", lines[i])!=None]
		bounds.append(len(lines))
		bounds = [lines[start:end][1:] for start, end in zip(bounds,bounds[1:])]
	return bounds

def solve_all(fname):
	"""Process each test case."""
	problems = read_file("%s.in" % fname)
	case = 1
	text = ""
	for p in problems:
		print("Solving Case #%s" % case)
		res = solve(p)
		text += "Case #%s: %s\n" % (case, res)
		case+=1
	with open("%s.out" % fname, "w") as out:
		out.write(text[:-1])

mask = "zyxwvutsrqponmlkjihgfedcba.ABCDEFGHIJKLMNOPQRSTUVWXYZ"
def solve(p):
	"""Solve an individual problem."""
	M = array([[mask.index(e)-26 for e in list(l)] for l in p])
	if any(M.sum(axis=0)>0) or any(M.sum(axis=1)>0):
		return "INFINITY"
	# wrap 4 arrays as one
	M = concatenate((M,M,),axis=0)
	M = concatenate((M,M,),axis=1)
	cols = len(M[0])
	rows = len(M)
	# correccion -> permitir wrap en los bordes
	max_sum = -float('inf')

	for left in range(cols):
		temp = [0]*rows
		for right in range(left, cols):
			for i in range(rows):
				temp[i] += M[i][right]
			_sum = kadane(temp, rows)
			
			if _sum > max_sum:
				max_sum = _sum
	if max_sum < 0:
		return 0
	else:
		return max_sum


solve_all("submit")